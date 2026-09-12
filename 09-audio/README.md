# Listening Room

Standalone, mobile-first, no-backend narrated study player for the SAI Assistant Director prep. Open `index.html` directly, or serve via GitHub Pages.

## Scope decision — read this first
The original spec asked for 5–12 minute chapters, up to 8 per module. This build uses **shorter chapters** (roughly 1.5–3 minutes of speech each, 1–3 per module depending on how much that module genuinely has to say) rather than padding thin content to hit a time target. Total: 18 chapters across Modules 0–8. If longer, more granular chapters are wanted, this is the file to extend — the data model supports it without any redesign.

## Phase 1 (this build): browser Web Speech API
No API key, no server, no audio files. Uses `speechSynthesis`, which means:
- Voice quality and availability genuinely vary by device/browser — the app says so on-screen, and never claims to sound professional.
- Voice selection and playback rate (0.75x–2x) are exposed and remembered via `localStorage`.
- **Resume is chapter-level, not timestamp-level.** Precise mid-utterance seek ("resume at 6:32") is not reliably achievable with the Web Speech API across browsers — rather than fake that precision, this tracks which chapters are complete and lets you jump back into any chapter from its start.

## Three listening modes
- **Learn** — full narration, normal pace.
- **Recall** — narration pauses at designated points, asks a question, and only reveals the answer on tap — trains retrieval, not passive listening.
- **Rapid** — skips straight to each chapter's recap line only. Built for interview-morning revision.

## Content discipline
Every line is a curated paraphrase of the already-verified Modules 0–8 — no new facts. Evidence classes (Official-Current, Official-Historical, Independent Evaluation, Parliamentary Oversight, Inference, Interview Prep) are shown on-screen for every chapter, and every unresolved item (Regional Centre count, DG SAI, MOC meeting frequency, the nonexistent 2024-25 Annual Report) is narrated explicitly as unresolved — never smoothed into a confident-sounding claim just because it's being read aloud.

## Loop with the quiz
Linked both directions: this player links to `../quiz/index.html`, and the quiz links back here — so the intended LISTEN → RECALL → QUIZ → REVIEW MISSES loop is actually navigable, not just described.

## Updating content
All chapter data lives in the `CHAPTERS` array in `index.html`'s `<script>` block — plain JS objects, no build step. Add a chapter by adding an object with `modId`, `title`, `lines`, `recall`, `recap`, `sources`, `evidenceClass`, `keyTerms`.
