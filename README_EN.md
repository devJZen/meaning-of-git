# git-log-hack

**[한국어](README.md)** | **English**

---

## Reflection

One thought stayed with me after wrapping up this project.

Git's decision to leave commit timestamps in the client's hands — with no server-side verification — is an intentional trade-off. When Linus Torvalds designed Git, the priority was not timestamp accuracy but **a distributed system where many developers can collaborate freely**. That design philosophy is precisely what makes date manipulation technically possible.

Exploring that gap was genuinely interesting as a research exercise. But it led me to a simpler realization: a git history is a record of what you actually did. For that record to be meaningful to the people you work with, what matters isn't the date — it's whether each commit represents real work.

That's why I cleaned up the 600+ Flower commits created purely for the experiment and kept only the commits that carry the research itself. Version control is, in the end, a collaboration tool.

## Overview

GitHub's contribution graph (green squares) is based on **Author Date**, which means you can control both past and future contributions.

This project demonstrates how to manipulate Git commit dates to draw custom patterns on your GitHub contribution graph.

![Example Pattern](https://img.shields.io/badge/Pattern-Customizable-green)

## Quick Start

```bash
# 1. Design your pattern (interactive editor)
cd interactive-cli
python3 github_canvas.py
# → Arrow keys to move, Space to paint, S to save, Q to quit

# 2. Generate Git commits
python3 git_generator.py generate pattern.json 2024

# 3. Push to GitHub
cd ..
git push -f origin main
```

> **Important**: `github_canvas.py` is for pattern design only, `git_generator.py` creates actual commits.

## How It Works

GitHub's contribution graph is generated using the following mechanism:

1. **Local Commit Creation**: Dates can be freely set by the client using `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`
2. **Server Storage**: GitHub (and other Git platforms) stores received commit dates without validation
3. **No Verification**: The server does not verify the authenticity of timestamps

**This applies to all Git platforms**: GitHub, GitLab, Bitbucket, Gitea, etc.

### Technical Details

```bash
# Set custom date for commit
GIT_AUTHOR_DATE="2024-01-15 10:00:00" \
GIT_COMMITTER_DATE="2024-01-15 10:00:00" \
git commit -m "Custom dated commit"
```

The contribution graph displays commits based on **Author Date**, not commit creation time or push time.

## Features

### 1. Basic Script

Create simple patterns with `create_flower_commits.py`

```bash
python3 create_flower_commits.py
```

### 2. Interactive Canvas Editor

Draw custom patterns with a terminal-based interactive editor

```bash
cd interactive-cli
python3 github_canvas.py
```

**Features**:

- Real-time pattern preview
- 5 intensity levels (0-4 commits per day)
- Two display styles (shaded/block)
- Save/load patterns (JSON format)
- Automatic Git commit generation

**Controls**:

- Arrow keys: Move cursor
- Space: Toggle intensity (0→1→2→3→4→0)
- 0-4: Set intensity directly
- T: Toggle display style
- S: Save pattern
- L: Load pattern
- C: Clear canvas
- Q/ESC: Quit

See [interactive-cli/README.md](interactive-cli/README.md) for detailed usage.

## Example

Current `git log` after cleanup (654 commits → 19):

```
e65d8fb  2026-06-15  update: unsigned GPG commit
962dbe0  2024-11-05  scenario-B: commit-3 (gpg+past, date=2024-Nov-05)
374fc25  2027-03-01  scenario-B: commit-2 (gpg+future, date=2027-Mar-01)
dc2c2f0  2025-06-15  scenario-B: commit-1 (gpg+backdated, date=2025-Jun-15)
2be6e98  2026-03-21  scenario-A: commit-3 (no gpg, date=Mar-21)
e2f3c53  2026-02-14  scenario-A: commit-2 (no gpg, date=Feb-14)
20e7ed7  2026-01-10  scenario-A: commit-1 (no gpg, date=Jan-10)
2d96dbb  2026-06-15  update: README.md
6c9531d  2026-01-05  feat: async project - git_generator - github_canvas - README
f0ecd3e  2026-01-05  docs: explain to project
4d124d1  2026-01-05  docs: explain to project
c0beb68  2026-01-02  test: Wiki Date Manipulation
f4ecc3f  2025-12-31  Merge pull request #1 from devJZen/test-pr-date
a1d4ee7  2025-12-31  update: How it works README.md
bb0ff4c  2025-12-31  first commit
```

Previously, 600+ Flower commits (all touching only `flower_commits.txt`) filled this history.

## Project Structure

```
git-log-hack/
├── create_flower_commits.py    # Simple flower pattern script
├── interactive-cli/             # Interactive canvas editor
│   ├── github_canvas.py        # Terminal-based pattern editor
│   ├── git_generator.py        # Pattern → Git commits converter
│   ├── patterns/               # Saved pattern files
│   └── README.md               # Detailed usage guide
├── README.md                   # This file (Korean)
└── README_EN.md                # This file (English)
```

## Intensity Levels

- **0**: Empty (no commits)
- **1**: Light green (1-3 commits)
- **2**: Medium green (4-7 commits)
- **3**: Dark green (8-12 commits)
- **4**: Darkest green (13-20 commits)

## Research & Experiments

This project includes extensive research on Git date manipulation:

### Successful Experiments ✅

- **Commit Date Manipulation**: Fully working
- **Pull Request with Past Dates**: Commits preserve their dates when merged
- **Wiki Date Manipulation**: Works but doesn't affect contribution graph

### Limitations ❌

- **PR Creation Date**: Cannot be backdated (server-generated)
- **PR Merge Date**: Cannot be backdated
- **Issue Creation Date**: Cannot be backdated (API limitation)
- **Star Dates**: Cannot and should not be manipulated (ToS violation)

See research documents:

- `git-date-commands-research.md` - All Git commands supporting date manipulation
- `pr-creation-date-research.md` - PR creation date manipulation research
- `test-pr-experiment.md` - PR date manipulation experiment results
- `wiki-experiment.md` - Wiki date manipulation experiment results

## Important Notes

### ⚠️ Warnings

1. **`git push -f` overwrites history**: Do NOT use on important repositories
2. **Email Configuration**: Ensure your git email matches your GitHub account
   ```bash
   git config user.email "your-github@email.com"
   ```
3. **Private Repositories**: May require "Private contributions" setting enabled
4. **Pattern Size**: 7 rows (days) × 52 columns (weeks)

### Ethical Considerations

This project is for:

- ✅ Educational purposes
- ✅ Understanding Git internals
- ✅ Creating fun patterns on your own profile
- ✅ Demonstrating distributed system trust models

This project is NOT for:

- ❌ Faking work history for employment
- ❌ Misleading contribution statistics
- ❌ Violating GitHub Terms of Service

## How GitHub Contribution Graph Works

**What Counts as Contributions**:

- ✅ Commits (based on Author Date)
- ✅ Pull Requests opened
- ✅ Issues opened
- ✅ Code reviews

**What Doesn't Count**:

- ❌ PR merge date
- ❌ Merge commits (shown as regular commits)
- ❌ Wiki commits (date manipulation works, but not reflected in contribution graph)
- ❌ Fork commits (unless you own the fork)

**Date Used**: Author Date (`GIT_AUTHOR_DATE`), NOT Committer Date or push time

## FAQ

**Q: Will this get my account banned?**
A: Manipulating commit dates alone is not against GitHub ToS. However, use responsibly.

**Q: Why do PRs show as commits, not PR events?**
A: GitHub's contribution graph tracks commits, not PR merge events. The commits within a PR are counted individually based on their Author Date.

**Q: Can I backdate PR creation?**
A: No, PR creation timestamps are server-generated and cannot be modified.

**Q: Does this work on private repositories?**
A: Yes, but you may need to enable "Private contributions" in your GitHub settings.

**Q: Can I use this on other Git platforms?**
A: Yes! GitLab, Bitbucket, and other platforms use similar activity graphs based on commit dates.

## Advanced Usage

### Generate Commits for Multiple Years

```bash
python3 git_generator.py generate pattern.json 2023
python3 git_generator.py generate pattern.json 2024
```

### Preview Pattern Before Generating

```bash
python3 git_generator.py preview pattern.json
```

### Custom Pattern Files

Patterns are stored in JSON format:

```json
{
  "grid": [
    [0, 0, 1, 0, 0, ...],
    [0, 1, 2, 1, 0, ...],
    ...
  ],
  "width": 52,
  "height": 7,
  "created": "2024-12-31T09:00:00"
}
```

## Research Documents

- `git-date-commands-research.md` - Comprehensive Git date manipulation guide
- `PR-vs-COMMIT-FAQ.md` - Why PRs appear as commits

## License

This project is for educational purposes. Use responsibly and ethically.

## Author

[@devJZen](https://github.com/devJZen)

---

**Last Updated**: 2026-06-18
