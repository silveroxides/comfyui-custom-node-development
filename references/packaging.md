# Packaging and Release Rules

- Follow the configured repository's `pyproject.toml`, registry metadata, and existing release convention.
- Keep runtime dependencies minimal and compatible with the configured ComfyUI checkout.
- Follow the repository's existing package-inclusion mechanism. Exclude private development files, large local references, temporary artifacts, and files not needed at runtime without imposing a particular ignore file on repositories that do not use it.
- Address registry scanner findings directly. Do not obfuscate network, filesystem, subprocess, or dynamic-execution calls to bypass scanners.
- Keep model downloads explicit, user-authorized, limited to documented artifacts, and compatible with registry policy.
- Do not include private files, local plans, reference repositories, generated test artifacts, or unrelated working-tree changes in commits.
- Stage exact relevant files. Inspect the staged diff before committing.
- Keep commits coherent and version bumps separate when the repository convention requires it.
- Push or publish only when the user explicitly requests it.
