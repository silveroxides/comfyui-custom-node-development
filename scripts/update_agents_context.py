#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import re
import sys


START = "<!-- comfyui-custom-node-context:start -->"
END = "<!-- comfyui-custom-node-context:end -->"
BLOCK_PATTERN = re.compile(
    rf"{re.escape(START)}.*?{re.escape(END)}",
    re.DOTALL,
)
PYTHON_EXECUTABLE_PATHS = (Path("Scripts/python.exe"), Path("bin/python"))


def resolved_directory(value, label):
    path = Path(value).expanduser().resolve()
    if not path.is_dir():
        raise ValueError(f"{label} is not a directory: {path}")
    return path


def resolved_file(value, label):
    path = Path(value).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"{label} is not a file: {path}")
    return path


def is_within(path, parent):
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def find_python_executable(venv_root):
    for relative_path in PYTHON_EXECUTABLE_PATHS:
        python_executable = venv_root / relative_path
        if python_executable.is_file():
            return python_executable
    return None


def validated_paths(args):
    comfy_root = resolved_directory(args.comfy_root, "ComfyUI root")
    custom_nodes_root = resolved_directory(args.custom_nodes_root, "Custom-nodes root")
    repo_root = resolved_directory(args.repo_root, "Repository root")
    venv_root = resolved_directory(args.venv_root, "Virtual-environment root")
    if args.python_executable:
        python_executable = resolved_file(args.python_executable, "Python executable")
    else:
        python_executable = find_python_executable(venv_root)
        if python_executable is None:
            raise ValueError(f"Virtual environment does not contain a Python executable: {venv_root}")
    agents_path = Path(args.agents).expanduser().resolve()

    if not (comfy_root / "folder_paths.py").is_file():
        raise ValueError(f"ComfyUI root does not contain folder_paths.py: {comfy_root}")
    if not is_within(custom_nodes_root, comfy_root):
        raise ValueError("Custom-nodes root must be inside the configured ComfyUI root.")
    if not is_within(repo_root, custom_nodes_root):
        raise ValueError("Repository root must be inside the configured custom-nodes root.")
    allowed_targets = {(repo_root / name).resolve() for name in ("AGENTS.md", "AGENTS-LOCAL.md")}
    if agents_path not in allowed_targets:
        raise ValueError(
            f"AGENTS.md target does not match repository root: {agents_path}; "
            "expected AGENTS-LOCAL.md (preferred) or legacy AGENTS.md in that repository."
        )
    if not is_within(python_executable, venv_root):
        raise ValueError("Python executable must be inside the configured virtual environment.")

    return {
        "comfyui_root": comfy_root,
        "custom_nodes_root": custom_nodes_root,
        "repository_root": repo_root,
        "virtual_environment_root": venv_root,
        "python_executable": python_executable,
    }, agents_path


def managed_block(paths, newline):
    lines = [START]
    lines.extend(f"{key}: {value}" for key, value in paths.items())
    lines.append(END)
    return newline.join(lines)


def update_agents(args):
    paths, agents_path = validated_paths(args)
    template_name = "AGENTS-LOCAL.md.template" if agents_path.name == "AGENTS-LOCAL.md" else "AGENTS.md.template"
    template_path = Path(__file__).resolve().parents[1] / "assets" / template_name
    source_path = agents_path if agents_path.exists() else template_path
    with source_path.open("r", encoding="utf-8", newline="") as handle:
        source = handle.read()
    matches = list(BLOCK_PATTERN.finditer(source))
    if len(matches) > 1:
        raise ValueError("AGENTS.md contains multiple managed ComfyUI context blocks.")

    newline = "\r\n" if "\r\n" in source else "\n"
    replacement = managed_block(paths, newline)
    if matches:
        updated = BLOCK_PATTERN.sub(lambda _match: replacement, source, count=1)
    else:
        separator = "" if not source else newline if source.endswith(("\n", "\r")) else newline * 2
        updated = f"{source}{separator}{replacement}{newline}"
    if args.check:
        if not agents_path.exists() or source != updated:
            raise ValueError("AGENTS.md context is not initialized with the supplied paths.")
        return False

    if agents_path.exists() and source == updated:
        return False
    agents_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = agents_path.with_name(f".{agents_path.name}.tmp-{os.getpid()}")
    try:
        with temporary_path.open("w", encoding="utf-8", newline="") as handle:
            handle.write(updated)
        os.replace(temporary_path, agents_path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
    return True


def parse_args():
    parser = argparse.ArgumentParser(description="Initialize the managed ComfyUI context in a repository AGENTS.md.")
    parser.add_argument("--agents", required=True)
    parser.add_argument("--comfy-root", required=True)
    parser.add_argument("--custom-nodes-root", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--venv-root", required=True)
    parser.add_argument("--python-executable")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main():
    try:
        changed = update_agents(parse_args())
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print("updated" if changed else "unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
