# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a collection of technical talk presentations built with [Marp](https://marp.app/), the Markdown presentation ecosystem. Each talk is a self-contained directory with Markdown source files that compile to HTML and PDF presentations.

## Build Commands

### Prerequisites
The repository requires Marp CLI. It is installed via Homebrew:
```bash
brew install marp-cli
```

### Building Presentations
- **Build single presentation**: `marp talk.md` (run from within the talk directory)
- **Build all presentations**: `find . -name "talk.md" -exec marp {} \;`
- **Watch mode for development**: `marp -w talk.md` (auto-rebuild on changes)
- **Export to PDF**: `marp --pdf talk.md`

## Repository Structure

- Each talk lives in its own directory (e.g., `gowest-2025/`, `local-ai/`, `pprof_for_beginners/`)
- Standard files per talk:
  - `talk.md` - Markdown source (this is what you edit)
  - `talk.html` - Generated HTML presentation (built artifact, do not edit directly)
  - `talk.pdf` - Optional PDF export (built artifact)
- `/images/` - Shared image assets used across multiple presentations
- `CRUSH.md` - Original guide with additional style guidelines (retained for reference)

## Marp Presentation Format

### Required Frontmatter
Every `talk.md` file should start with YAML frontmatter:
```yaml
---
marp: true
theme: default  # or gaia for branded talks
paginate: true
title: Your Talk Title
backgroundImage: url('../images/soypete_background.png')
description: Brief description of the talk
---
```

### Common Patterns
- Use `---` to separate slides
- Use `<!-- _class: lead -->` for title/section slides
- Images: Use relative paths from talk directory: `../images/filename.png`
- Background images: `![bg right](../images/image.png)` or `![bg left](../images/image.png)`
- Themes available: `gaia`, `default` (prefer `gaia` for branded talks)
- Standard backgrounds: `soypete_background.png` or `weave_theme.png`

### Content Structure Standards
Most presentations follow this structure:
1. Title slide with `<!-- _class: lead -->`
2. "Who Am I?" bio slide with author info, role, and social links
3. Content slides
4. Q&A or Thank You slide at end

Include consistent footers with relevant links when appropriate.

## File Naming Conventions

- Talk directories: lowercase with hyphens (e.g., `local-ai`, `go-run-gcp`, `gowest-2025`)
- Presentation files: Always named `talk.md`, `talk.html`, `talk.pdf`
- Images: Descriptive names, PNG for graphics, JPG for photos

## Working with Images

- All shared images go in `/images/` at the repository root
- Reference from talk directories using relative path: `../images/filename.png`
- Common images include: `soypete_background.png`, `weave_theme.png`, `pedro.gif`

## Git Workflow

This repository uses:
- Main branch: `main`
- Current branch: `miriah-gowest`
- Repository is a personal talks collection, so commit style is informal but descriptive
