# The Long Run — A Narrative Memory Architecture

A separate learning artifact from the 20-page Systems Handbook, the Listening Room, and Recall Bench — none of those are touched by this.

## What this is
An 11-chapter interactive HTML story. A fictional runner (Arjun Toppo, from a small town in Jharkhand) moves through the entire SAI/MYAS system — NSTC, STC, NCOE, TOPS/MOC, NSGA/NSB — while a parallel fictional character, Assistant Director Ritu Bhargava, gives the reader a second, administrative thread through the same events. The two threads converge in a final master diagram and a self-test recall exercise.

## Format decision
Built as a single self-contained HTML/CSS/JS file (`index.html`), not a PDF. The brief explicitly said PDF wasn't required and an interactive experience was preferred. Progress (which chapters are marked read) is stored in `localStorage` only.

## Animation decision
The brief allowed Lottie animations. This build uses CSS/SVG-based diagrams instead — explicitly one of the brief's own listed alternatives. Hand-authoring genuine Lottie JSON (normally produced by After Effects/Bodymovin export) isn't something that can be done reliably from scratch; SVG diagrams achieve the same teaching goal (showing a relationship, not just naming it) with far less risk of a broken or empty animation.

## Accuracy discipline
Every institutional claim in the story carries one of five tags, shown inline: **Official Fact**, **Parliamentary** (oversight findings), **Inference** (plausible but unconfirmed), **Illustrative Scenario** (invented situation built on real mechanics), or **Fictional** (a name, number, or detail that only exists for the story). Nothing state-changing from the verified Modules 0–8 was altered — this artifact narrativises what's already there; it doesn't introduce new institutional claims.

Specific things the story deliberately does NOT claim, matching the existing fact-trap discipline: no real National Sports Federation is named (a generic "the Federation" stands in, so no real body's governance conduct is implied); the Mission Olympic Cell's meeting frequency is explicitly flagged as unconfirmed; the Parliamentary Committee's ~45% SAI-wide vacancy figure and NIPFP's 56% KISCE fill-rate figure are kept visibly separate.

## QA performed before push
Validated with Playwright + headless Chromium (not just visual inspection): full click-through of all 11 chapters with console/page-error monitoring (zero errors), plus manual full-page screenshots of the home screen, prologue, and several content chapters to check layout, tag rendering, and diagram legibility at mobile width (390px).

## Cross-links
Links out to `../09-audio/index.html` and `../quiz/index.html` from the home screen. Neither of those files links back in yet — worth adding if this proves useful in practice.

## Updating content
All narrative content lives in the `CHAPTERS` array in `index.html`'s `<script>` block — plain JS objects (`scene`, `lesson`, `takeaway`, `diagram`, `cast` section types), no build step.
