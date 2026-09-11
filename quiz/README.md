# Recall Bench

Standalone, mobile-first HTML/CSS/JS quiz app (no backend, no account, no build step) for the SAI Assistant Director interview prep. Open `index.html` directly on a phone or desktop — or enable GitHub Pages for this repo (Settings → Pages → deploy from `main` branch, `/quiz` folder) to get a shareable link.

## Modes
- **Quick 10** — 5-minute mixed drill across everything
- **Facts Recall** — numbers/statistics
- **Abbreviation Drill**
- **SAI Divisions** — function ↔ division
- **Module Recall** — the 5-question framework (what/why/how/broken/AD-fit) for each of Modules 1–7
- **Fact Traps** — judgment questions on unresolved/risky claims (Regional Centre count discrepancy, DG SAI uncertainty, MOC frequency, etc.) — trains judgment, not memorisation of a guessed answer
- **Weak Areas** — auto-surfaces whatever you've missed most, using locally stored per-item miss rates
- **Board Pressure** — 45s timer, no multiple choice, real board-style personal questions, self-graded against expected talking points
- **Explain It Aloud** — 45s timer, module-level explain-it-yourself before reveal

## Design notes
All content is transcribed directly from the verified `08-reference/` files — the quiz does not introduce any new facts. Every item preserves its provenance discipline: unresolved items (e.g. "how many Regional Centres") appear only as Fact Trap judgment questions, never as a normal fact card with a guessed single answer.

## Data / progress
Progress (streak, items reviewed, per-item miss rates) is stored in the browser's `localStorage` only — nothing leaves the device, nothing syncs across devices/browsers. Clearing browser data resets it.

## Updating content
If a module gets corrected or extended (e.g. DG SAI gets confirmed, the Regional Centre count gets reconciled), update the corresponding array in `index.html`'s `<script>` block directly — the data model is plain JS objects, no build step required.
