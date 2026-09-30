# Python

Conventions for Python code in any repo that composes this base. The base rules
still apply; this page adds what is specific to Python.

## Tests

Tests exercise the real code against doubles that cannot drift from the real
interfaces. The `python-tests-refactor` skill carries the step-by-step method for
bringing an existing suite up to this standard. The rules below apply to every
new or changed test.

### Rules

1. **Spec-bound mocks, never bare `MagicMock()` or hand-rolled `FakeX`.** Build
   doubles from the real definitions: `create_autospec(RealClass, instance=True)`
   or `create_autospec(real_function)`. They enforce attribute names and call
   signatures, so a rename or signature change in production breaks the test
   instead of passing against a stale copy of the interface.
2. **Dependency injection, not `monkeypatch.setattr`.** The unit under test takes
   its collaborators as keyword arguments with real defaults
   (`def fetch(..., *, connect=IMAPClient)`). Tests pass doubles in directly, and
   production callers get the real behaviour without extra wiring. Patching
   module attributes to swap a dependency hides the wiring and breaks silently when
   an import moves.
3. **One fixture per collaborator; representative inputs are fixtures too.** Each
   fixture returns a spec mock with a neutral default (or one datum). Tests request
   only the fixtures they use, so the signature lists the boundaries each case
   exercises.
4. **Set values in the test, not the fixture.** The test overrides the
   `return_value`/`side_effect` it cares about, then asserts on the result and on
   the recorded calls (`call_args`, `assert_called_once_with`).
5. **Mock only I/O boundaries.** Database, network, model calls, filesystem, clock,
   subprocess. Pure and deterministic logic (parsing, validation, classification,
   gating) stays real. Mocking it tests the mock.
6. **The caller owns resource lifecycles.** When a collaborator is a context
   manager (a DB handle, a session), open it in the caller and inject the open
   object, so the double is a plain object. Where the unit must own the lifecycle
   (e.g. one connection per `fetch`), inject a factory and set
   `mock.__enter__.return_value = mock`.

Configuration read from the environment is not a collaborator: setting it with
`monkeypatch.setenv` is fine. Passing a value as a parameter is still preferable
when the unit can take one.

### Gotchas

- `create_autospec` specs off the class, so attributes assigned in `__init__` are
  not part of the spec. Set them on the instance mock (`m.model = "local"`).
- Generators autospec badly. Inject a plain factory for a record source
  (`documents=lambda **_: iter(docs)`), not a spec mock.
- A test must inject every boundary its input triggers. If a data fixture trips a
  branch that calls a collaborator, inject that collaborator too, or the real one
  runs and does I/O.
- Injecting `store` collides with `from . import store`. Import the needed
  function directly or rename the module import.

### Remove on sight

- `MagicMock()` without a `spec`.
- `class FakeX` re-declaring a collaborator's methods.
- `monkeypatch.setattr(module, "Collaborator", fake)` to swap a dependency.
- One large fixture that patches everything and hides the wiring.
- Mocking the function under test, or a pure function it calls.

Integration tests against a real service (a database or mail server in Docker) are
the complement, not an exception: they cover the boundary the mocks stand in for.
