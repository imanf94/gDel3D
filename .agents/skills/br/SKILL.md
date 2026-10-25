---
name: br
description: Use this skill when the user wants to build the distribution and release a new version, or uses /br or [BR].
---

# Build and Release (BR) Workflow

Follow these steps in sequence:

1. **Build**:
   - Run `rm -rf dist`
   - Run `python -m build --sdist`
   - Run `twine upload dist/* --verbose`

2. **Release**:
   - Find the previous version tag: `git describe --tags --abbrev=0`
   - Get commits since the previous tag: `git log <old_tag>..HEAD --oneline`
   - Generate release notes formatted with:
     - **Features**
     - **Refactors & Build**
     - **Examples**
     (Save release notes in `<appDataDir>/brain/<conversation-id>/scratch/`, NOT in the working directory)
   - Run `./release.py --notes "<generated_notes>"`
