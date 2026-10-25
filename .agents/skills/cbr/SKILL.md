---
name: cbr
description: Use this skill when the user wants to commit all changes, build the distribution, and release a new version, or uses /cbr or [CBR].
---

# Commit, Build, and Release (CBR) Workflow

Follow these steps in sequence:

1. **Commit**:
   - Create a separate, individual commit for **each** changed file with a conventional commit prefix (`feat:`, `chore:`, `build:`, `refactor:`, `docs:`, etc.).
   - If using a Python script, place it in `<appDataDir>/brain/<conversation-id>/scratch/`, NOT in the working directory.
   - Ensure all changed files are committed.
   - Push commits to GitHub.

2. **Build**:
   - Run `rm -rf dist`
   - Run `python -m build --sdist`
   - Run `twine upload dist/* --verbose`

3. **Release**:
   - Find the previous version tag: `git describe --tags --abbrev=0`
   - Get commits since the previous tag: `git log <old_tag>..HEAD --oneline`
   - Generate release notes formatted with:
     - **Features**
     - **Refactors & Build**
     - **Examples**
     (Save release notes in `<appDataDir>/brain/<conversation-id>/scratch/`, NOT in the working directory)
   - Run `./release.py --notes "<generated_notes>"`
