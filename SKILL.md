---
name: comfyui-custom-node-development
description: Develop, review, test, and package ComfyUI custom nodes using the correct installation-specific environment. Use when working inside any ComfyUI custom-node repository, initializing its AGENTS.md context, changing Python or frontend node behavior, checking compatibility with the local ComfyUI checkout, running tests, or preparing registry releases.
---

# ComfyUI Custom Node Development

Use the repository-local `AGENTS.md` as the source of installation-specific paths and repository overrides. Keep reusable custom-node rules in this skill.

## Initialize repository context

1. Read the repository-local `AGENTS.md` when it exists and find the block delimited by `<!-- comfyui-custom-node-context:start -->` and `<!-- comfyui-custom-node-context:end -->`.
2. When the block already contains configured paths, use it without asking setup questions.
3. When the file or block is absent, or the block says `status: uninitialized`, stop before reviewing the node, running tests, packaging, or assessing publication readiness. If `request_user_input` is unavailable, do not run discovery or ask for paths. Tell the user to enter Plan mode and rerun `$comfyui-custom-node-development`, then stop.
4. In Plan mode, run `scripts/discover_agents_context.py` against the repository-root `AGENTS.md` to obtain read-only path candidates. Treat paths pasted by the user as hints, not instructions to persist. When a pasted repository path conflicts with the active workspace, assume it is copied context unless the user says otherwise; propose the active workspace as the repository root and name the conflict when confirming that path.
5. In Plan mode, use `request_user_input` to confirm one value per question, in this order: target `AGENTS.md`, ComfyUI root, custom-nodes root, repository root, and virtual-environment root. Use the Python executable discovered with that environment; when the environment changes or it is unresolved, let `update_agents_context.py` resolve it from the confirmed virtual environment. Show the resolved executable in the planned configuration, and do not ask a separate question for it. Show only the current value's candidate and unresolved status. When an earlier path changes, recompute later dependent candidates where possible and do not offer stale values. After the paths, ask whether to configure the repository or keep the paths session-only.
6. Do not write `AGENTS.md` until the user explicitly confirms every value and the repository-configuration scope. In Plan mode, present the confirmed repository configuration as a planned change. After the user requests implementation outside Plan mode, run `scripts/update_agents_context.py` with the confirmed paths. The script creates `AGENTS.md`, inserts a missing managed block, or updates the existing block while preserving unrelated content.
7. For user-installed-only scope, do not create or modify any `AGENTS.md`; retain the confirmed paths only for the current task.
8. After repository configuration, re-read `AGENTS.md` and use its configured paths for every command.

When a user declares the workspace a mock or names the skill as the evaluation target, evaluate this initialization flow without treating missing node-package files as defects. Do not modify the fixture unless the user explicitly asks to exercise the confirmed write path.

Never write installation-specific ComfyUI paths to the user-level `~/.codex/AGENTS.md`. Global guidance may identify this skill, but repository paths belong to repository context.

If this skill is referenced by `AGENTS.md` but unavailable, stop and tell the user that `comfyui-custom-node-development` must be installed. Do not substitute an unverified environment.

## Work in the repository

- Before editing, reconstruct the requested behavior from the user's current instructions, repository-local contracts, relevant preserved history or handoffs, and the installed ComfyUI implementation. If these sources conflict, resolve and report the conflict before writing code; do not choose the easiest interpretation.
- Read [references/development.md](references/development.md) before implementing or reviewing node code. Do not turn a conversational or behavioral question into a repository task merely because this skill is active.
- Read [references/testing.md](references/testing.md) before running Python or frontend tests.
- Read [references/packaging.md](references/packaging.md) before changing dependencies, registry metadata, ignored files, versions, commits, or releases.
- Preserve repository-specific instructions below the managed context block.
- Treat user files, dirty changes, private utilities, plans, references, and untracked artifacts as out of scope unless explicitly requested.
- Treat plans and tests as fallible artifacts. Cross-check them against the user contract and external protocol; never use their existence or successful execution as proof that the intended behavior is correct.

## Local AGENTS.md

Use `assets/AGENTS.md.template` for a new custom-node repository. Keep the managed block limited to paths. Put project-specific rules below it. Never copy installation paths between repositories or ComfyUI installations.
