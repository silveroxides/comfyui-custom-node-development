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

## Verify live Comfy Registry status

- Read the node ID and target version from the repository metadata. Do not infer
  live Registry state from a successful publish workflow, validation, security
  check, or upload.
- Query the live records directly:

  ```powershell
  $nodeId = '<node ID>'
  $version = '<version>'
  Invoke-RestMethod "https://api.comfy.org/nodes/$nodeId" |
      Select-Object id, status, status_detail
  Invoke-RestMethod "https://api.comfy.org/nodes/$nodeId/versions/$version" |
      Select-Object version, status, createdAt
  Invoke-RestMethod "https://api.comfy.org/nodes/$nodeId/install" |
      Select-Object version, status, createdAt
  ```

- Report node status and target-version status separately. The `/install`
  record identifies the version currently selected for installation; it does
  not replace checking the requested version directly.
- Report returned enums exactly, including prefixes such as `NodeStatusActive`
  and `NodeVersionStatusPending`. A pending status does not reveal whether
  scanning, review, or another stage is responsible. Do not claim scanner
  clearance or explain the cause unless a live record exposes that evidence.
- Use `/nodes/search?search=<node ID>&limit=10` only to check discoverability.
  A search result does not prove that the target version is active.
- Include the decisive live endpoint or reusable command in the result so the
  status can be checked again without rediscovering the API.
