"""Tests for promote.py. Run: python3 -m unittest discover -s scripts"""

from __future__ import annotations

import unittest
from unittest.mock import create_autospec

import promote
from promote import (
    GitHub,
    GitHubError,
    PromotionPR,
    insert_rules,
    make_marker,
    parse_promotion_pr,
    parse_section,
    plan_repo,
    reconcile,
    remove_rules,
    rule_hash,
)

COMMENT = "<!-- Rules for all repos. Keep this heading. -->"

AGENTS = f"""# repo

## Commands

```bash
# SYSTEM.md
## not a rule, inside a fence
```

# SYSTEM.md

{COMMENT}

## Rule one

Text one.

## Rule two

Text two.
"""

SYSTEM = """# Agent conventions

## Commits

- Atomic.

## Promote rules to SYSTEM.md

See `docs/promotion.md`.
"""

RULE_ONE = "## Rule one\n\nText one."
RULE_TWO = "## Rule two\n\nText two."


class ParseSectionTest(unittest.TestCase):
    def test_splits_rules_and_ignores_fenced_headings(self):
        section = parse_section(AGENTS)
        self.assertEqual(section.rules, (RULE_ONE, RULE_TWO))
        self.assertEqual(section.preamble, COMMENT)
        self.assertTrue(section.before.endswith("# SYSTEM.md"))

    def test_empty_section_has_no_rules(self):
        section = parse_section(f"# repo\n\n# SYSTEM.md\n\n{COMMENT}\n")
        self.assertEqual(section.rules, ())

    def test_no_heading(self):
        self.assertIsNone(parse_section("# repo\n\n## Rule\n"))

    def test_hash_ignores_trailing_whitespace(self):
        with_spaces = AGENTS.replace("Text one.", "Text one.   ")
        self.assertEqual(parse_section(with_spaces).rules[0], RULE_ONE)


class EditTest(unittest.TestCase):
    def test_remove_keeps_heading_comment_and_other_rules(self):
        result = remove_rules(AGENTS, {rule_hash(RULE_ONE)})
        section = parse_section(result)
        self.assertEqual(section.rules, (RULE_TWO,))
        self.assertEqual(section.preamble, COMMENT)
        self.assertIn("## not a rule, inside a fence", result)
        self.assertTrue(result.endswith("Text two.\n"))

    def test_remove_all_leaves_empty_section(self):
        result = remove_rules(AGENTS, {rule_hash(RULE_ONE), rule_hash(RULE_TWO)})
        self.assertTrue(result.endswith(f"# SYSTEM.md\n\n{COMMENT}\n"))

    def test_insert_above_promotion_section(self):
        result = insert_rules(SYSTEM, [RULE_ONE])
        self.assertLess(result.index("## Rule one"), result.index("## Promote rules"))
        self.assertGreater(result.index("## Rule one"), result.index("- Atomic."))

    def test_insert_at_end_without_anchor(self):
        result = insert_rules("# Agent conventions\n", [RULE_ONE])
        self.assertTrue(result.endswith("Text one.\n"))


def pull(number, ref, body, state="closed", merged=False):
    return {
        "number": number,
        "head": {"ref": ref},
        "body": body,
        "state": state,
        "merged_at": "2026-11-06T00:00:00Z" if merged else None,
    }


class PlanTest(unittest.TestCase):
    def test_parse_promotion_pr_states(self):
        marker = make_marker("o/r", "abc123", [rule_hash(RULE_ONE)])
        merged = parse_promotion_pr(pull(1, "promote/r-abc", marker, merged=True))
        rejected = parse_promotion_pr(pull(2, "promote/r-abc", marker))
        waiting = parse_promotion_pr(pull(3, "promote/r-abc", marker, state="open"))
        self.assertEqual(
            [merged.state, rejected.state, waiting.state],
            ["merged", "rejected", "open"],
        )
        self.assertEqual(merged.rules, {rule_hash(RULE_ONE)})

    def test_parse_ignores_other_branches_and_missing_marker(self):
        marker = make_marker("o/r", "abc123", ["aaa"])
        self.assertIsNone(parse_promotion_pr(pull(1, "feat/x", marker)))
        self.assertIsNone(parse_promotion_pr(pull(1, "promote/r-abc", "no marker")))

    def test_plan_sorts_rules_by_pr_state(self):
        section = parse_section(AGENTS)
        prs = [
            PromotionPR(7, "merged", "o/r", frozenset({rule_hash(RULE_ONE)})),
            PromotionPR(8, "rejected", "o/other", frozenset({rule_hash(RULE_TWO)})),
        ]
        plan = plan_repo("o/r", section, prs)
        self.assertEqual(plan.promoted, [RULE_ONE])
        self.assertEqual(plan.promoted_by, {7})
        # The rejection was for a different source repo, so rule two is new here.
        self.assertEqual(plan.new, [RULE_TWO])

    def test_merged_wins_over_rejected(self):
        digest = frozenset({rule_hash(RULE_ONE)})
        prs = [
            PromotionPR(1, "rejected", "o/r", digest),
            PromotionPR(2, "merged", "o/r", digest),
        ]
        plan = plan_repo("o/r", parse_section(AGENTS), prs)
        self.assertEqual(plan.promoted, [RULE_ONE])
        self.assertEqual(plan.rejected, [])


class ReconcileTest(unittest.TestCase):
    def make_github(self):
        github = create_autospec(GitHub, instance=True)
        github.read_file.side_effect = lambda repo, path: (
            (AGENTS, "blob-a", "main")
            if path == "AGENTS.md"
            else (SYSTEM, "blob-s", "main")
        )
        github.head_commit.return_value = "abcdef1234567"
        github.open_pull_heads.return_value = set()
        github.propose.return_value = "https://example/pull/1"
        return github

    def test_new_rules_open_one_promotion_pr(self):
        github = self.make_github()
        report = reconcile(github, "o/r", "o/agents", [], set(), dry_run=False)

        github.propose.assert_called_once()
        args = github.propose.call_args.args
        self.assertEqual(
            args[0:4], ("o/agents", "main", "promote/r-abcdef1", "SYSTEM.md")
        )
        self.assertIn("## Rule one", args[4])
        self.assertIn(
            make_marker(
                "o/r", "abcdef1234567", [rule_hash(RULE_ONE), rule_hash(RULE_TWO)]
            ),
            args[8],
        )
        self.assertIn("- opened promotion PR https://example/pull/1", report)

    def test_merged_rules_open_cleanup_pr(self):
        github = self.make_github()
        both = frozenset({rule_hash(RULE_ONE), rule_hash(RULE_TWO)})
        prs = [PromotionPR(5, "merged", "o/r", both)]

        reconcile(github, "o/r", "o/agents", prs, set(), dry_run=False)

        args = github.propose.call_args.args
        self.assertEqual(
            args[0:4], ("o/r", "main", "promote/cleanup-abcdef1", "AGENTS.md")
        )
        self.assertEqual(parse_section(args[4]).rules, ())
        self.assertIn("o/agents#5", args[8])

    def test_open_cleanup_pr_is_not_duplicated(self):
        github = self.make_github()
        github.open_pull_heads.return_value = {"promote/cleanup-0000000"}
        prs = [PromotionPR(5, "merged", "o/r", frozenset({rule_hash(RULE_ONE)}))]

        report = reconcile(github, "o/r", "o/agents", prs, set(), dry_run=True)

        self.assertIn("- cleanup PR already open", report)

    def test_dry_run_changes_nothing(self):
        github = self.make_github()
        report = reconcile(github, "o/r", "o/agents", [], set(), dry_run=True)
        github.propose.assert_not_called()
        self.assertIn("- would promote: Rule one", report)

    def test_used_branch_is_skipped(self):
        github = self.make_github()
        report = reconcile(
            github, "o/r", "o/agents", [], {"promote/r-abcdef1"}, dry_run=False
        )
        github.propose.assert_not_called()
        self.assertIn("- branch promote/r-abcdef1 already used; skipped", report)

    def test_repo_without_agents_md_is_skipped(self):
        github = self.make_github()
        github.read_file.side_effect = None
        github.read_file.return_value = None
        self.assertEqual(reconcile(github, "o/r", "o/agents", [], set(), False), [])


class RunTest(unittest.TestCase):
    def test_one_repo_error_does_not_stop_the_others(self):
        github = create_autospec(GitHub, instance=True)
        github.all_pulls.return_value = []
        github.read_file.side_effect = [GitHubError(500, "boom"), None]

        report, ok = promote.run(
            github, "o", "o/agents", ["o/bad", "o/good"], dry_run=True
        )

        self.assertFalse(ok)
        self.assertIn("- error: boom", report)
        self.assertEqual(github.read_file.call_count, 2)


if __name__ == "__main__":
    unittest.main()
