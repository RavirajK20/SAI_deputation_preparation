# Animated Chapter Production Status

| Component | Status |
|---|---|
| Canonical story (`11-story/`) | Locked — source of truth for all narration and on-screen text |
| Video coverage | 12 of 13 narrative units (~22.6 minutes total) |
| ch0 "The Cast & The Map" | Intentionally not produced as video (reference/cast section, not a narrative scene) — covered in the full-story audiobook instead |
| Full-story audiobook | Complete, 13/13 units, 25:33, one continuous file (`09-audio/full_story_narration.mp3`) |

## Method, briefly

Each chapter follows the same pipeline: canonical text → narration → speech-to-text-verified
timestamps → shot timing derived from the real narration audio → rendering → assembly. Visuals mix
three deliberately different techniques depending on what a given passage actually needs:

- **Deterministic, software-rendered graphics** for any institutional, factual, or numeric content
  (organisation charts, statistics, process flows) — this text is never AI-generated, so labels and
  figures are guaranteed to render exactly as written.
- **AI-generated painterly stills with restrained camera movement** for character and setting shots,
  using multiple distinct compositions for a character only where the narrative genuinely shifts what
  the viewer should be looking at, rather than as a default.
- **Short AI-generated motion clips** reserved for the handful of moments with real physical action
  (a race, a throw) — most chapters use none at all, since most of the story is administrative and
  file-driven rather than physical.

Every chapter went through direct frame-by-frame visual inspection and audio transcription QA before
being marked complete — not just an automated pass/fail check.

## Known, disclosed limitations

The text-to-speech voice used for narration has a few consistent, documented pronunciation
limitations that were not chased to a perfect fix, since they don't affect on-screen text or the
story's factual content — only how a small number of words sound when spoken:

- The name **"Ritu"** is pronounced inconsistently across chapters.
- **"Jharkhand"** and **"Toppo"** (Arjun's surname) are only partially corrected.
- **"Khelo"** is consistently heard as "Kilo," and **"lakh"** as "lock."

None of these affect the accuracy of on-screen text, subtitles, or the underlying story content —
they are purely a narration-voice limitation, disclosed here rather than silently left unmentioned.
