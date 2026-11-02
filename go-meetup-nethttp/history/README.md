# Go net/http: a chronological meetup talk

Start with `talk.md`, the Marp source. `talk.html` is its generated presentation; open it in a browser. `research-changelog.md` records the release-by-release research and primary sources, with a research cutoff of October 26, 2026.

`supplied-reference.pptx` is the original supplied PowerPoint, preserved for reference. It predates edits to the Marp source and is not a current export.

Regenerate the HTML with `marp --html talk.md -o talk.html`. To generate an updated PowerPoint, install a supported browser and run `marp --pptx talk.md -o talk.pptx`.

The talk uses Go release numbers to date changes and HTTP/1 and HTTP/2 to describe wire protocols. Code snippets are illustrative; check API availability against the Go version used in your project.
