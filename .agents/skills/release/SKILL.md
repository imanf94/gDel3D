---
name: release
description: Use this skill when the user wants to merge all open PRs, generate release notes, tag a version, and create a GitHub release, or uses /release or [RELEASE].
---

# Release Workflow

Follow these steps exactly to release a new version:

## 1. Merge All Open Pull Requests
- Check for open pull requests using `gh pr list`.
- If there are open pull requests, merge all of them into `main` in chronological order (from oldest up to now):
  ```bash
  gh pr merge <pr-number> --merge --auto
  ```
- Switch to the `main` branch and ensure local is fully up-to-date:
  ```bash
  git checkout main
  git pull origin main
  ```

## 2. Commit Discovery & History
- Find the previous version tag by running `git describe --tags --abbrev=0`.
- Get all commits from that previous tag to the current `HEAD` (e.g., `git log <old_tag>..HEAD --oneline`).

## 3. Formatted Release Notes
- Generate a release note summarizing those commits formatted strictly into three sections:
  - **Features**
  - **Refactors & Build**
  - **Examples**
- Store the release notes file strictly in the conversation scratch folder (`<appDataDir>/brain/<conversation-id>/scratch/release_notes.txt`), NOT in the project working folder.

## 4. Tag & Publish Release
- Run `./release.py --notes "<generated_notes>"` (or pass the notes file) to bump version, create git tag, and publish the GitHub release.
