# Agent Instructions & General Rules

<RULE[user_global]>
If the user provides an instruction without any explicit workflow skills or tags, focus exclusively on building new features.
</RULE[user_global]>

<RULE[user_global]>
If the user's prompt starts with [DISCUSS] or uses the /discuss slash command, you must not generate code or program anything, but you may use tools (e.g. searching the web, viewing files) to inform the discussion. Just discuss the problem with the user.
</RULE[user_global]>

<RULE[user_global]>
If the user's prompt does not start with [DISCUSS] or /discuss, you must scan the changed files via git diff or other available tools to stay updated with any changes the user might have made locally before proceeding.
</RULE[user_global]>

<RULE[user_global]>
If the user uses the `[INSTALL]` tag or `/install` slash command, you are permitted to use the `pip install` command. If there is no `[INSTALL]` tag or `/install` active, you MUST NOT use the `pip install` command.
</RULE[user_global]>

## Available Workspace Skills (Slash Commands)

The following procedural workflows are configured as modular skills under `.agents/skills/` and can be invoked directly with slash commands or their corresponding tags:

- `/3d` or `[3D]`: [`3d skill`](./skills/3d/SKILL.md) — Specialized 3D Vision, Computer Graphics, and Differentiable Geometry planning and execution skill.
- `/scan` or `[SCAN]`: [`scan skill`](./skills/scan/SKILL.md) — Thoroughly scan the workspace to understand repository structure, architecture, philosophy, and active developments.
- `/docs` or `[DOCS]`: [`docs skill`](./skills/docs/SKILL.md) — Comprehensive documentation and docstring generation/refinement skill across all source file types (`.c`, `.h`, `.cpp`, `.cuh`, `.cu`, `.py`) and PyBind11 bindings.
- `/discuss` or `[DISCUSS]`: [`discuss skill`](./skills/discuss/SKILL.md) — Enter discussion-only mode (no code generation; research tools permitted).
- `/commit` or `[COMMIT]`: [`commit skill`](./skills/commit/SKILL.md) — Create a branch, commit changed files individually with conventional prefixes, push to remote, open a PR into main, and manage GitHub issues with `gh`.
- `/build` or `[BUILD]`: [`build skill`](./skills/build/SKILL.md) — Clean `dist/`, build sdist package, and upload to PyPI via twine.
- `/release` or `[RELEASE]`: [`release skill`](./skills/release/SKILL.md) — Merge all open PRs in order into main, summarize commits into 3 formatted sections (Features, Refactors & Build, Examples), tag version, and publish GitHub release.
- `/br` or `[BR]`: [`br skill`](./skills/br/SKILL.md) — Sequential Build and Release.
- `/cbr` or `[CBR]`: [`cbr skill`](./skills/cbr/SKILL.md) — Sequential Commit, Build, and Release.
- `/docker` or `[DOCKER]`: [`docker skill`](./skills/docker/SKILL.md) — Build versioned Docker image and verify installation.
- `/docker-push` or `[DOCKER_PUSH]`: [`docker-push skill`](./skills/docker-push/SKILL.md) — Tag and push Docker image to Docker Hub.
- `/install` or `[INSTALL]`: [`install skill`](./skills/install/SKILL.md) — Grant permission for `pip install`.
