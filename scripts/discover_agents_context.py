#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def is_within(path, parent):
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def find_comfy_root(repo_root):
    for candidate in (repo_root, *repo_root.parents):
        if (candidate / "folder_paths.py").is_file():
            return candidate
    return None


def find_custom_nodes_root(repo_root, comfy_root):
    if comfy_root is None:
        return None
    for candidate in (repo_root, *repo_root.parents):
        if candidate.name == "custom_nodes" and is_within(repo_root, candidate):
            return candidate
    candidate = comfy_root / "custom_nodes"
    if candidate.is_dir() and is_within(repo_root, candidate):
        return candidate
    return None


def find_venv(comfy_root):
    if comfy_root is None:
        return None, None
    for name in (".venv", "venv"):
        venv_root = comfy_root / name
        if not venv_root.is_dir():
            continue
        for relative_path in (Path("Scripts/python.exe"), Path("bin/python")):
            python_executable = venv_root / relative_path
            if python_executable.is_file():
                return venv_root, python_executable
        return venv_root, None
    return None, None


def discover_context(agents):
    agents_path = Path(agents).expanduser().resolve()
    repo_root = agents_path.parent
    comfy_root = find_comfy_root(repo_root)
    custom_nodes_root = find_custom_nodes_root(repo_root, comfy_root)
    venv_root, python_executable = find_venv(comfy_root)
    candidates = {
        "comfyui_root": comfy_root,
        "custom_nodes_root": custom_nodes_root,
        "repository_root": repo_root,
        "virtual_environment_root": venv_root,
        "python_executable": python_executable,
    }
    return {
        "agents_path": str(agents_path),
        "candidates": {key: str(value) if value is not None else None for key, value in candidates.items()},
        "unresolved": [key for key, value in candidates.items() if value is None],
    }


def main():
    parser = argparse.ArgumentParser(description="Discover read-only ComfyUI context candidates for AGENTS.md.")
    parser.add_argument("--agents", required=True)
    args = parser.parse_args()
    print(json.dumps(discover_context(args.agents), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
