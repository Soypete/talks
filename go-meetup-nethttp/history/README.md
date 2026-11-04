# Go net/http: a chronological meetup talk

Start with `talk.md`, the 30-slide Marp source. It includes attributed excerpts from the Go standard library; `research-changelog.md` preserves the deeper release history. `talk.html` is its generated presentation; open it in a browser. `research-changelog.md` records the release-by-release research and primary sources, with a research cutoff of October 26, 2026.

`supplied-reference.pptx` is the original supplied PowerPoint, preserved for reference. It predates edits to the Marp source and is not a current export.

Regenerate the HTML with `marp --html talk.md -o talk.html`. To generate an updated PowerPoint, install a supported browser and run `marp --pptx talk.md -o talk.pptx`.

The talk uses Go release numbers to date changes and HTTP/1 and HTTP/2 to describe wire protocols. Code snippets are illustrative; check API availability against the Go version used in your project.

The slide examples are runnable in [`examples/`](examples/README.md), including route, HTTP/2, and concurrency tests.

The opening and section timelines are PNG backgrounds in `timeline/`. They progressively reveal the milestones; `timeline/generate.py` regenerates them with Pillow and macOS Arial fonts.

Four demo slides embed silent MP4 recordings from `videos/`; use the playback controls while narrating. Open the generated HTML with the `videos/` directory beside it. The body-limit recording shows the result but the top of the code scrolls out of view.
