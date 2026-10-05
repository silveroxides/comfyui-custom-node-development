# ComfyUI Custom Node Development Skill

A Codex skill for developing, reviewing, testing, and packaging ComfyUI custom nodes with the correct local ComfyUI installation and virtual environment.

It keeps installation-specific paths in each custom-node repository's `AGENTS.md`, so a skill installation can safely support multiple ComfyUI checkouts and nodes.

## Before initialization

- A local ComfyUI installation.
- A custom-node repository, normally under that installation's `custom_nodes` directory.
- The virtual environment used by that ComfyUI installation. Discovery checks `.venv` and `venv` inside the ComfyUI root; Codex prompts for another location when needed.

## Install

### Via Skills CLI (Universal)

Install globally from GitHub into all supported agent environments (OpenCode, Codex, Cursor, etc.):

```bash
npx skills add silveroxides/comfyui-custom-node-development -g
```

Or using the full repository URL:

```bash
npx skills add https://github.com/silveroxides/comfyui-custom-node-development -g
```

To limit installation to specific agents:

```bash
npx skills add silveroxides/comfyui-custom-node-development -g --agent opencode codex
```

### Conversational Install (Codex)

Copy this query into Codex:

```text
Install the skill from https://github.com/silveroxides/comfyui-custom-node-development
```

## Initialize a custom-node repository

Open the custom-node repository in Codex and copy this query:

```text
$comfyui-custom-node-development
```

The skill writes a managed local context block to that node repository's `AGENTS.md`. It records the ComfyUI installation, the paired custom-nodes directory, the node repository, virtual environment, and its Python executable.

Do not copy this context between node repositories or ComfyUI installations. Each node repository must be initialized against its own local ComfyUI checkout and environment.

## License

[MIT](LICENSE)
