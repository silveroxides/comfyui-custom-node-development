# Custom Node Testing Rules

## Environment

- Use only the Python executable recorded in the managed `AGENTS.md` context.
- Never fall back to `python`, `python3`, or `pytest` from the system or current shell.
- Follow the repository-owned test runner and documented working directory when present. Otherwise inspect the test configuration and use the configured ComfyUI environment without inventing universal pytest flags or temporary-directory policy.
- Do not run model inference unless explicitly requested. Mock model loading and inference boundaries.

## Repository-owned selector

- Require each custom-node repository to document one repository-owned test
  selector and its working directory in `AGENTS.md`.
- Prefer `tests/run_tests.py` with `tests/test_groups.toml`. The selector must
  invoke pytest through `sys.executable`, run from the configured ComfyUI root,
  use `--import-mode=importlib`, use a unique repository-local `--basetemp`, add
  the repository root to `PYTHONPATH`, and remove only its own temporary run.
- Provide `--group`, `--changed`, `--base`, `--dry-run`, `--list-groups`, and
  `--final` modes. Treat an unmapped production source as an error.
- When the selector is absent after repository activation, create it before
  testing by running `scripts/setup_test_runner.py <repository-root>` with the
  configured ComfyUI Python. It generates `tests/test_groups.toml` from the
  actual source and test inventory. Refine the safe broad mapping into semantic
  groups through bounded source-to-test inspection.
- Add the following repository rules when creating the selector:
  - Use `tests/run_tests.py` for all Python test selection.
  - During iteration, run an exact test or one explicit group.
  - Before handoff, run `--changed` once for accumulated changes.
  - Run `--final` only as a deliberate broader gate and do not repeat a
    successful gate without relevant changes.
  - Stage a new production source before relying on `--changed`, or select its
    group explicitly.
- If a test run emits repeated setup errors or unexpectedly large output, stop.
  Diagnose the selector invocation itself before rerunning anything.

## Python tests

- Start with the smallest repository-supported selection that exercises the changed external contract.
- Run broader gates once after the accumulated change when required by repository instructions or proportional risk; do not repeatedly run unrelated groups.
- Report unrelated existing failures separately and do not change them without scope.
- Use `py_compile` or an equivalent non-inference import/schema check when appropriate.
- Derive assertions from user-visible behavior, installed Core/model protocol, and independent expected values. Do not duplicate the implementation algorithm inside the test or assert an unverified current behavior merely to make it permanent.
- A passing suite establishes only that its assertions passed. Recheck contract coverage when tests and implementation were created from the same plan or assumption.

## Frontend tests

- Use the repository's existing package scripts when present.
- Otherwise run focused `.mjs` tests with the verified Node executable available to the repository.
- Test serialization, queue closure, geometry, widget order, and frontend/backend identifier compatibility when those areas change.

## Cleanup

- Remove only temporary artifacts created by the current task, using the repository's established cleanup behavior when available.
- Do not clean caches or artifacts owned by the user unless requested.
