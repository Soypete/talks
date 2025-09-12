# CRUSH.md - Talks Repository Guide

## Build Commands
- **Build single presentation**: `marp talk.md` (from within talk directory)
- **Build all presentations**: `find . -name "talk.md" -exec marp {} \;`
- **Watch mode**: `marp -w talk.md` (auto-rebuild on changes)
- **Export to PDF**: `marp --pdf talk.md`

## Content Structure
- Each talk lives in its own directory (e.g., `generics/`, `local-ai/`)
- Standard files: `talk.md` (source), `talk.html` (generated), `talk.pdf` (optional)
- Shared images in `/images/` directory
- Use relative paths for images: `../images/filename.png`

## Markdown Style Guidelines
- Use Marp frontmatter with theme, pagination, and background settings
- Themes: `gaia`, `default` (prefer gaia for branded talks)
- Standard background: `url('../images/soypete_background.png')` or `url('../images/weave_theme.png')`
- Include footer with relevant links/code examples
- Use `---` for slide breaks
- Use `<!-- _class: lead -->` for title slides

## Naming Conventions
- Talk directories: lowercase with hyphens (e.g., `local-ai`, `go-run-gcp`)
- Files: `talk.md`, `talk.html`, `talk.pdf`
- Images: descriptive names, use PNG for graphics, JPG for photos
- Bio slides should include: role, social handles, GitHub link

## Content Guidelines
- Start with title slide including author name
- Include bio slide with current role and social links
- Add "Who Am I?" or similar personal introduction
- Include relevant company/project promotion slides
- Use consistent footer across slides in a presentation
- Keep slide content concise and visual