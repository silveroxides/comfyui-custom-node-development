"""Provision a safe repository-owned test selector for a custom-node repository."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
RUNNER_ASSET = SKILL_ROOT / "assets" / "run_tests.py"


def quoted_list(values: list[str]) -> str:
    return "\n".join(f'  "{value}",' for value in values)


def production_patterns(repository_root: Path) -> list[str]:
    patterns: list[str] = []
    if (repository_root / "__init__.py").is_file():
        patterns.append("__init__.py")
    if (repository_root / "nodes").is_dir():
        patterns.append("nodes/*.py")
    root_python = [
        path for path in repository_root.glob("*.py")
        if path.name != "__init__.py"
    ]
    if root_python:
        patterns.append("*.py")
    if (repository_root / "web").is_dir():
        patterns.append("web/*.js")
    return patterns


def test_inventory(repository_root: Path) -> tuple[list[str], list[str]]:
    tests_root = repository_root / "tests"
    python_tests = sorted(
        path.relative_to(repository_root).as_posix()
        for path in tests_root.glob("test_*.py")
    )
    frontend_tests = sorted(
        path.relative_to(repository_root).as_posix()
        for path in tests_root.glob("test_*.mjs")
    )
    return python_tests, frontend_tests


def initial_manifest(repository_root: Path) -> str:
    paths = production_patterns(repository_root)
    python_tests, frontend_tests = test_inventory(repository_root)
    if not paths:
        raise ValueError("No supported production source layout found")
    if not python_tests and not frontend_tests:
        raise ValueError("No tests/test_*.py or tests/test_*.mjs files found")
    return (
        "# Safe broad mapping generated during skill activation.\n"
        "# Refine into semantic groups after verifying source-to-test coverage.\n"
        "[groups.repository]\n"
        "paths = [\n"
        f"{quoted_list(paths)}\n"
        "]\n"
        "python_tests = [\n"
        f"{quoted_list(python_tests)}\n"
        "]\n"
        "frontend_tests = [\n"
        f"{quoted_list(frontend_tests)}\n"
        "]\n"
    )


def provision(repository_root: Path) -> tuple[Path, Path]:
    repository_root = repository_root.resolve()
    tests_root = repository_root / "tests"
    tests_root.mkdir(exist_ok=True)
    runner = tests_root / "run_tests.py"
    manifest = tests_root / "test_groups.toml"
    existing = [path for path in (runner, manifest) if path.exists()]
    if existing:
        names = ", ".join(str(path) for path in existing)
        raise FileExistsError(f"Refusing to overwrite existing test contract: {names}")
    manifest_text = initial_manifest(repository_root)
    shutil.copyfile(RUNNER_ASSET, runner)
    try:
        manifest.write_text(manifest_text, encoding="utf-8", newline="\n")
    except Exception:
        runner.unlink(missing_ok=True)
        raise
    return runner, manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository_root", type=Path)
    return parser.parse_args()


def main() -> int:
    runner, manifest = provision(parse_args().repository_root)
    print(runner)
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
