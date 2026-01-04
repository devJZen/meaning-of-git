# git-log-hack

**[한국어](README.md)** | **English**

---

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

```
55fd317 - devJZen, 1 year ago : Flower commit 52
7e81ed7 - devJZen, 12 months ago : Flower commit 51
341ddee - devJZen, 1 year ago : Flower commit 50
b2c4066 - devJZen, 1 year ago : Flower commit 49
9af3713 - devJZen, 1 year ago : Flower commit 48
```

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

**Last Updated**: 2026-01-05

**Key Insight**: GitHub contribution graphs are based on Git's distributed trust model - clients set dates, servers store them without validation. This is a feature, not a bug! 🎨
