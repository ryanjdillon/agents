# Simplified Technical English

ASD-STE100 Simplified Technical English (STE) is a controlled language. The
aerospace industry made it for maintenance documents. Its rules make text
easy to read for a person who has English as a second language. The rules
also make text easy to read for a machine, and they prevent text that has
two meanings.

This doc gives the STE rules that we use. It also tells how to apply the
same principles to names in code.

## Where to use STE

Use STE for all prose that you write:

- Docs, READMEs, and `AGENTS.md` files.
- Docstrings and code comments.
- Commit messages and PR descriptions.
- Linear issues, comments, and project updates.

Do not use STE for quoted text, error messages from other tools, or legal
text. Do not change these texts.

## Words

- **Use one word for one meaning.** If you use "remove" for an action, do not
  use "delete" for the same action in the same text.
- **Use the same term for the same thing each time.** Do not change a term for
  variety. A reader thinks that a new term is a new thing.
- **Use simple, common words.** Write "use", not "utilise". Write "start", not
  "initiate". Write "help", not "facilitate".
- **Use technical names when they are necessary.** A technical name is a word
  for a thing in your domain, for example `flake`, `migration`, or
  `Linear issue`. STE permits technical names. Use the exact name that the
  tool or code uses.
- **Use verbs for actions.** Write "Examine the log", not "Do an examination of
  the log".
- **Do not use phrasal verbs** when a single verb is available. Write "start",
  not "set up". Write "find", not "look up".

## Sentences

- **Keep sentences short.** Use 20 words or fewer in a procedure. Use 25 words
  or fewer in a description.
- **Write one topic in each sentence.** Write one instruction in each sentence,
  except when two actions occur at the same time.
- **Use the active voice.** Write "The script writes the file", not "The file
  is written by the script".
- **Use the simple tenses:** the present, the past, and the future. Do not use
  "has been", "will have", or "-ing" forms as the verb.
- **Write instructions as commands.** Write "Run `just check`", not "You should
  run `just check`".
- **Put conditions first.** Write "If the check fails, examine the log", not
  "Examine the log if the check fails".
- **Do not leave out words.** Keep "the", "a", and "that" where they make the
  sentence clear.

## Paragraphs and structure

- **Write one topic in each paragraph.** Start the paragraph with that topic.
- **Keep paragraphs short.** Use six sentences or fewer.
- **Use a list for sequential steps.** Use a numbered list when the order is
  important. Use one step in each item.
- **Give warnings before the step** that they apply to, not after it.

## Names in code

STE is for prose, but its principles also make names clear. Apply them to
modules, types, functions, variables, flags, and config keys.

- **One term for one concept across the codebase.** If the code calls a thing
  a `job`, do not call the same thing a `task` in another module.
- **One concept for one term.** Do not use `client` for an HTTP client in one
  module and for a customer in a different module.
- **Use verbs for functions that do an action:** `load_config`, `send_invoice`,
  `parse_header`. Use nouns for values and types: `config`, `Invoice`,
  `header`.
- **Use plain words.** Write `remove_user`, not `obliterate_user`. Write
  `retry_count`, not `reattempt_quantum`.
- **Do not use vague nouns** such as `manager`, `handler`, `helper`, `util`,
  `data`, or `info` when a specific word is available. `InvoiceStore` tells the
  reader more than `InvoiceManager`.
- **Do not abbreviate** unless the abbreviation is more common than the full
  word (`id`, `url`, `http`). Write `message`, not `msg`.
- **Use the domain term.** If the domain calls a thing a `berth`, the code
  calls it a `berth`, not a `slot`.
- **Use the language idiom for case and form.** STE controls the words. The
  language controls the form (`snake_case`, `camelCase`, `PascalCase`).

## Examples

| Do not write | Write |
| --- | --- |
| This function is responsible for handling the initialisation of the cache. | This function starts the cache. |
| The config should be validated before it gets deployed. | Validate the config before you deploy it. |
| Leverage the helper to facilitate retries. | Use `retry_request` to send the request again. |
| `def process_data(d):` | `def parse_invoice(raw_invoice):` |

## References

- ASD-STE100 specification: <https://www.asd-ste100.org/>
