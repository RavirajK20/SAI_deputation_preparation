# The SAI–MYAS Systems Handbook

## Important limitation, stated plainly
The finished **PDF** (20 pages, delivered directly to the user via chat) could **not** be pushed to this repository. Testing showed this GitHub connector does not support real binary uploads — a base64-encoded test string was stored as literal 20 bytes of text rather than being decoded, meaning any attempt to push the actual PDF binary through this tool would silently corrupt it. Rather than commit a broken file, only the **HTML source** (`index.html`) is stored here.

## How to get the PDF
Anyone with this repo cloned can regenerate the exact same PDF locally:
```
wkhtmltopdf --enable-local-file-access index.html handbook.pdf
```
`wkhtmltopdf` is a standard, freely available tool. The HTML deliberately uses only locally-available system fonts (Liberation Serif/Sans) rather than a remote Google Fonts link, specifically so this regeneration step doesn't depend on network access at build time.

## What this is
A 20-page visual systems handbook mapping the entire SAI/MYAS governance, funding, implementation, and oversight architecture, with the Assistant Director's role explicitly overlaid throughout. Built with real SVG diagrams (chain of authority, divisions network, money flow, NSGA/SAI separation, a full 9-step "one problem through the system" walkthrough, an AD decision-sequence flowchart) rather than styled bullet lists.

## Version history
- **V1**: initial 17-page build, covering governance chain, SAI's 19 divisions, the talent pipeline, financial flow, NSGA/SAI separation, oversight, external stakeholders, digital architecture, the AD-duty mapping, and three illustrative case studies.
- **V2** (current): two factual corrections, independently re-verified — the Finance Committee is chaired by the Secretary (Sports), MYAS, not the Union Minister (General Body/Governing Body chairmanship by the Minister was re-checked and confirmed correct); and NSGA-2025 regulates the Act's defined "National Sports Bodies" category (Olympic/Paralympic Committees, NSFs, Regional Sports Federations), not NSFs alone. Also added three relational-depth pages addressing "how do the parts interact," not just "what are the parts."

## Source discipline
Every page carries evidence tags (Official—Current, Official—Historical, Independent Evaluation, Parliamentary Oversight, Inference, Interview Prep) and a full source register with deliberately unresolved items listed explicitly (current DG SAI, SAI's exact Regional Centre count, Mission Olympic Cell meeting frequency, and the nonexistent SAI Annual Report 2024-25) rather than guessed at.

## Cross-links
References the Listening Room (`../09-audio/`) and Recall Bench (`../quiz/`) tools, and is itself referenced by The Long Run narrative (`../11-story/`) as the source of its diagrams and factual claims.
