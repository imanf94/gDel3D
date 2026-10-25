---
name: commit
description: Use this skill when the user wants to commit all changed files individually with conventional commit messages, create a branch and PR into main, and manage GitHub issues, or uses /commit or [COMMIT].
---

# Commit & Pull Request Workflow

Follow these steps exactly whenever `/commit` or `[COMMIT]` is invoked:

## 1. Branch Creation
- Create and switch to a descriptive branch (e.g., `git checkout -b feat/<feature-name>` or `chore/<task-name>`).

## 2. Individual File Commits
- Commit **each** changed and untracked file individually with a dedicated, descriptive commit message.
- Start every commit message with a conventional commit prefix (e.g., `feat:`, `chore:`, `build:`, `refactor:`, `docs:`, `test:`, `fix:`, `perf:`).
- If creating a helper script (e.g. in Python to automate commits), store it strictly in the conversation scratch folder (`<appDataDir>/brain/<conversation-id>/scratch/`), NEVER in the project working directory.

## 3. Push to Remote & Create Pull Request
- Push the branch to GitHub (`git push -u origin <branch-name>`).
- Create a Pull Request targeting `main` using `gh pr create --base main --head <branch-name> --title "<PR Title>" --body "<Detailed description of changes>"`.

## 4. GitHub Issue Synchronization via `gh`
- Check existing issues with `gh issue list`.
- **If a related open issue exists**:
  - Add comprehensive technical comments to the issue (see Comment Requirements below).
  - Link the PR to the issue.
- **If NO related open issue exists**:
  - Check closed issues or create a new issue using `gh issue create --title "<Issue Title>" --body "<Description of feature/task>"`.
  - Add comprehensive technical comments to the issue (see Comment Requirements below).
  - Close the issue once documented (`gh issue close <issue-number> --comment "Implemented and covered by PR."`).

### Detailed Issue Comment Requirements:
When commenting on GitHub issues, write rich, structured technical documentation that includes:
1. **API Usage & Executable Code Snippets**:
   - Clear, copy-pasteable Python examples showing how to import, call, and test the feature (including argument explanations and return types).
2. **Advantages & Core Capabilities**:
   - Key design strengths (e.g. sharp crease preservation, throughput, zero-copy GPU memory layout, differentiability, watertight manifold guarantees).
3. **Disadvantages & Known Trade-offs**:
   - Algorithmic limitations, domain constraints, or edge cases to be aware of (e.g. single dual vertex per voxel cell, narrow-band boundary padding requirements, Hermite normal dependency).
4. **Empirical Benchmarks & Performance Metrics**:
   - Real benchmark metrics run on hardware (e.g. latency in milliseconds, throughput in M faces/s, vertex and face counts across standard test assets like Armadillo, Fandisk, Sphere, or CAD Box at varying grid resolutions such as $64^3$, $256^3$, $1024^3$).
5. **Technical Insights & Architectural Decisions**:
   - Interesting findings, mathematical formulation details, numerical stability improvements, or architectural rationale worth preserving for future development.
