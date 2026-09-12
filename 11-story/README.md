# The Long Run — A Narrative Memory Architecture

A separate learning artifact from the 20-page Systems Handbook, the Listening Room, and Recall Bench — none of those are touched by this.

## What this is
A 13-chapter interactive HTML story. A fictional runner (Arjun Toppo, from a small town in Jharkhand) moves through the entire SAI/MYAS system — NSTC, STC, NCOE, TOPS/MOC, NSGA/NSB, NST — while a parallel fictional character, Assistant Director Ritu Bhargava, gives the reader a second, administrative thread through the same events. The two threads converge in a final master diagram and a self-test recall exercise.

## Extension (V1 → V1.1)
Three targeted additions were made to the original 11-chapter story, per an explicitly scoped brief — the original 11 chapters were **not** rewritten:
- **Ch1b — "The Other Door"**: a second athlete (Sunita Marandi, fictional) takes the Khelo India Centre → KISCE route in parallel to Arjun's NSTC → STC route, making the KIC/KISCE vs. SAI's own ladder distinction something the reader watches rather than reads as a definition.
- **Ch7b — "The Selection That Was Challenged"**: a fictional athlete (Farhan Aziz) brings a selection dispute to the National Sports Tribunal, explicitly distinguished from Chapter 7's National Sports Board recognition matter — same NSGA-2025 framework, two different bodies, two different questions. The chapter states directly that NST does not touch SAI's own administrative files.
- **Campus Map**: an alternate home-screen view (toggle, linear chapter list stays the default) with 13 clickable institutional nodes — MYAS, SAI, State Dept./KIC-KISCE, Operations/NCOE, Sports Science, IT/NSRS, Finance/GAD/Procurement, Engineering, TOPS/MOC, Assistant Director, National Sports Board, National Sports Tribunal, Parliament/NIPFP/Audit — each routing straight into the chapter where that institution is actually covered, not a decorative diagram.

## Format decision
Built as a single self-contained HTML/CSS/JS file (`index.html`), not a PDF. The brief explicitly said PDF wasn't required and an interactive experience was preferred. Progress (which chapters are marked read, and which home view — chapters or map — was last selected) is stored in `localStorage` only.

## Animation decision
The brief allowed Lottie animations. This build uses CSS/SVG-based diagrams instead — explicitly one of the brief's own listed alternatives. Hand-authoring genuine Lottie JSON (normally produced by After Effects/Bodymovin export) isn't something that can be done reliably from scratch; SVG diagrams achieve the same teaching goal (showing a relationship, not just naming it) with far less risk of a broken or empty animation.

## Accuracy discipline
Every institutional claim in the story carries one of five tags, shown inline: **Official Fact**, **Parliamentary** (oversight findings), **Inference** (plausible but unconfirmed), **Illustrative Scenario** (invented situation built on real mechanics), or **Fictional** (a name, number, or detail that only exists for the story). Nothing state-changing from the verified Modules 0–8 was altered — this artifact narrativises what's already there; it doesn't introduce new institutional claims.

Specific things the story deliberately does NOT claim, matching the existing fact-trap discipline: no real National Sports Federation is named (a generic "the Federation" stands in, so no real body's governance conduct is implied); the Mission Olympic Cell's meeting frequency is explicitly flagged as unconfirmed; the Parliamentary Committee's ~45% SAI-wide vacancy figure and NIPFP's 56% KISCE fill-rate figure are kept visibly separate; the National Sports Tribunal's actual case procedures/timelines aren't verified, so Farhan's case outcome is deliberately left unresolved rather than invented.

## QA performed before this push
Browser binary downloads (Playwright's Chromium) are blocked by this environment's network egress policy, so the original session's Playwright-based click-through could not be re-run here. Instead: (1) the embedded JavaScript was syntax-checked with `node --check`; (2) full logic QA was run via `jsdom` — every one of the 13 chapters and all 13 campus-map nodes were opened programmatically (via the actual `openChapter`/`jumpToChapterById` functions, not simulated), with zero runtime errors; (3) the campus map and both new chapters were visually rendered at 400px mobile width via `wkhtmltoimage` and checked by eye for overlap/legibility. This is a different QA method than the original Playwright pass, not a lesser standard — it exercises the same code paths, just without a full browser's rendering engine confirming pixel layout on every page (spot-checked instead of exhaustively).

## Cross-links
Links out to `../09-audio/index.html` and `../quiz/index.html` from the home screen. Neither of those files links back in yet — worth adding if this proves useful in practice.

## Updating content
All narrative content lives in the `CHAPTERS` array in `index.html`'s `<script>` block — plain JS objects (`scene`, `lesson`, `takeaway`, `diagram`, `cast` section types), no build step. Campus map nodes live in the separate `MAP_NODES` array; each node's `chapterId` must match a real chapter's `id`.
