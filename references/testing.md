# Custom Node Testing Rules

## Environment

- Use only the Python executable recorded in the managed `AGENTS.md` context.
- Never fall back to `python`, `python3`, or `pytest` from the system or current shell.
- Follow the repository-owned test runner and documented working directory when present. Otherwise inspect the test configuration and use the configured ComfyUI environment without inventing universal pytest flags or temporary-directory policy.
- Do not run model inference unless explicitly requested. Mock model loading and inference boundaries.

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
