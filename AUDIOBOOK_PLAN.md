# Audiobook Production Plan

## Overview

Produce a professional audiobook of *Causal Inference: A Pokemon Approach -- Kanto Region Edition* (~110,000 words, 8 chapters + front/back matter) using **Kokoro TTS**, an open-source 82M-parameter text-to-speech engine.

This project requires a **two-stage pipeline**: first, each textbook chapter is adapted into an audio-native script (equations verbalized, DAGs described relationally, code replaced with conceptual narration, character dialogue formatted for multi-voice). Then the scripts are processed by `generate_audiobook.py` to produce the final audio.

**Expected output:** 12 MP3 files, ~12-13 hours total audio, ~1.0 GB at 192kbps
**Generation time:** ~10-15 minutes on modern hardware
**Primary voice:** `am_michael` (American male, narrator) at speed 0.90
**Multi-voice:** 3 Kokoro voices for narrator, Professor Oak, and Blue/supporting cast

---

## Dependencies

### System (via Homebrew)
```bash
brew install espeak-ng ffmpeg
```
- `espeak-ng` -- phoneme generation backend for Kokoro
- `ffmpeg` -- audio format conversion (WAV to MP3)

### Python (via pip)
```bash
pip3 install kokoro soundfile numpy pydub mutagen pyyaml
```
- `kokoro` -- the TTS engine (auto-downloads ~80MB voice model on first use)
- `soundfile` -- WAV file I/O
- `numpy` -- audio array manipulation
- `pydub` -- MP3 conversion
- `mutagen` -- ID3 tag writing
- `pyyaml` -- parse script frontmatter

---

## Directory Structure

```
audiobook/
  generate_audiobook.py              # Main generation script
  README.md                          # Project overview, chapter list
  
  scripts/                           # Audio-adapted chapter scripts (Stage 1 output)
    00_front_matter.md               # Introduction & how to listen
    ch01_pallet_town.md              # ~9,000 words / ~60 min
    ch02_pewter_city.md              # ~10,500 words / ~70 min
    ch03_cerulean_city.md            # ~13,500 words / ~90 min
    ch04_vermilion_city.md           # ~11,250 words / ~75 min
    ch05_celadon_city.md             # ~10,500 words / ~70 min
    ch06_fuchsia_cinnabar.md         # ~12,750 words / ~85 min
    ch07_saffron_city.md             # ~12,000 words / ~80 min
    ch08_indigo_plateau.md           # ~15,000 words / ~100 min
    appendix_math_foundations.md     # ~6,000 words / ~40 min
    appendix_causal_pokedex.md       # ~3,000 words / ~20 min
  
  templates/
    chapter_template.md              # Standard script scaffold
    transformation_patterns.md       # Content conversion patterns with examples
  
  production/
    character_guide.md               # Voice assignments, speech patterns, example lines
    pronunciation_guide.md           # Technical terms, Greek letters, Pokemon names
  
  output/
    wav/                             # Intermediate WAV files
    mp3/                             # Final MP3 output
    progress.json                    # Resume tracking
    manifest.json                    # Final metadata
```

---

## Stage 1: Script Adaptation

Each textbook chapter (`textbook/chapters/ch*.md`) must be adapted into an audio-native script (`audiobook/scripts/ch*.md`) before audio generation. This is NOT automated -- it requires careful rewriting. The scripts are the creative core of the audiobook.

### What Changes from Textbook to Script

| Textbook Element | Script Treatment |
|---|---|
| LaTeX equations (`$$...$$`, `$...$`) | Verbal explanations (see Pattern 2 below) |
| HTML figure/image tags | Omitted entirely; described in narration where needed |
| Data tables (`\| ... \|`) | Key numbers spoken through character dialogue (Pattern 4) |
| Python code blocks | Conceptual narration of what the analysis reveals (Pattern 5) |
| "Professor Oak Explains" boxes | Oak dialogue with plain-English definitions (Pattern 1) |
| "Blue's Mistake" boxes | Blue dialogue followed by Oak's correction |
| DAG images and ASCII diagrams | Verbal "arrow map" descriptions (Pattern 3) |
| Plots (scatter, Love, RDD) | Shape-and-punchline narration (Pattern 6) |
| Exercises / notebook challenges | Verbal comprehension checks with pauses |
| Bibliography citations | Key citations mentioned by name inline |
| Appendix B (data/environment) | Omitted -- purely technical |
| Appendix C (full DAG reference) | Omitted -- visual reference; content woven into Ch3 |

### Script Format

Each script uses YAML frontmatter + stage-directed markdown:

```markdown
---
title: "Chapter 1: Pallet Town -- What Is Causal Inference?"
chapter_number: 1
source_file: "textbook/chapters/ch01_pallet_town.md"
estimated_runtime_minutes: 60
key_concepts:
  - correlation vs causation
  - potential outcomes framework
  - average treatment effect
  - selection bias
characters:
  - narrator
  - oak
  - blue
---

# Chapter 1: Pallet Town -- What Is Causal Inference?

## Part 1: The Starter Debate

[SCENE: Morning in Pallet Town.]

NARRATOR: You wake up in a small house at the edge of a quiet 
town. Sunlight filters through the curtains...

BLUE: Professor, the data is clear. Trainers who pick Squirtle 
average six point eight Gym Badges. Charmander trainers average 
only five point nine. Squirtle is obviously superior.

[pause]

OAK: Is it, though?

[Script continues...]
```

### Content Transformation Patterns

These are the 6 repeatable patterns for converting textbook content to audio script.

**Pattern 1: Formal Definition --> Oak Dialogue**

The textbook's `> **Professor Oak Explains:**` boxes become spoken dialogue. Lead with the Pokemon intuition (already in the textbook), then Oak states the definition in plain English, then the narrator restates in everyday language with a concrete example.

```
OAK: The Average Treatment Effect is the answer to a simple 
question: if we could clone every trainer in Kanto and give 
one clone the treatment and the other the control, and then 
average the difference -- that average difference is the ATE.

NARRATOR: In other words, it is the average of what-would-have-been 
compared to what-actually-was, across everyone.
```

**Pattern 2: Equation --> Verbal Decomposition**

Never read symbols. State what the equation means, name it, describe its structure, tie each term to something concrete.

```
OAK: When you compare treated to untreated, that comparison 
captures two things. The first is the real causal effect -- 
the ATT. The second is the selection bias -- the gap that 
would exist even if treatment did nothing. Naive comparison 
equals ATT plus selection bias.
```

**Pattern 3: DAG --> Verbal Arrow Map**

Describe topology relationally: name variables, state what "causes" what, identify structure type (fork/chain/collider), state the implication.

```
BILL: Experience sits at the top. It directly causes two 
things: Cave Training and Badges. That is a fork -- a common 
cause. And that fork creates the illusion that the Cave helps.
```

**Pattern 4: Table --> Character Dialogue with Numbers**

Extract 2-3 key numbers. Deliver through character voice.

```
BLUE: Squirtle trainers average six point eight badges. 
Charmander? Only five point nine. Almost a full badge difference.

OAK: The numbers are correct. The interpretation is not.
```

**Pattern 5: Code --> Conceptual Narration**

No Python syntax. Describe what the analysis does and reveals.

```
NARRATOR: We fit a doubly robust estimator, adjusting for 
experience, wealth, and starter type. The estimated effect 
shrinks from two point six to zero point eight badges.
```

**Pattern 6: Plot --> Shape and Punchline**

Describe the visual shape, then the interpretive takeaway.

```
NARRATOR: Imagine a line of dots going smoothly upward, and 
then right at the threshold -- at exactly two hundred and 
twenty happiness points -- the line jumps. That jump is the 
causal effect.
```

### Pedagogical Adaptations

**Three-Beat Rule:** Every key concept appears three times per chapter:
1. Informally through narrative/story
2. Formally by Professor Oak in plain language
3. Restated in the Chapter Summary

**Callback Phrasing:** When referencing earlier concepts, re-state them -- don't just name-drop. "Remember from Pewter City: randomization makes the selection bias disappear because the coin doesn't know anything about the trainer."

**Comprehension Checks:** Each chapter ends with 3-5 verbal questions. A pause is inserted before each answer.

```
NARRATOR: Why does randomization eliminate selection bias?

[long pause]

Because the coin flip is independent of potential outcomes. 
The treated and control groups are identical in expectation.
```

---

## Stage 2: Audio Generation -- `generate_audiobook.py`

A single Python file at the project root (`audiobook/generate_audiobook.py`) with these components:

### 1. Configuration Block

| Setting | Value | Rationale |
|---|---|---|
| Narrator voice | `am_michael` | Clear American male; warm, measured tone for primary narration |
| Oak voice | `bm_george` | British male; slightly older feel, professorial authority |
| Blue/supporting voice | `am_adam` | American male (alt); brash energy for rival + supporting male cast |
| Female characters voice | `af_heart` | American female; warm, natural for Misty, Nurse Joy, Erika, etc. |
| Narrator speed | 0.90 | ~150 wpm; slightly slower than default for dense causal reasoning |
| Oak speed | 0.88 | Slightly slower; measured, gives definitions time to land |
| Blue speed | 0.95 | Slightly faster; matches his brash, confident personality |
| Sample rate | 24,000 Hz | Kokoro native rate |
| MP3 bitrate | 192 kbps | High quality for speech clarity |
| Output dir | `audiobook/output/mp3/` and `audiobook/output/wav/` | Keeps audio separate from scripts |

**Chapter ordering:**

```python
CHAPTER_ORDER = [
    "00_front_matter.md",
    "ch01_pallet_town.md",
    "ch02_pewter_city.md",
    "ch03_cerulean_city.md",
    "ch04_vermilion_city.md",
    "ch05_celadon_city.md",
    "ch06_fuchsia_cinnabar.md",
    "ch07_saffron_city.md",
    "ch08_indigo_plateau.md",
    "appendix_math_foundations.md",
    "appendix_causal_pokedex.md",
]
```

**Pause durations (silence inserted between segments):**

| Context | Duration | Why |
|---|---|---|
| After chapter title announcement | 2.5s | Let the title and city name land |
| At `## Part N` boundaries | 2.0s | Major section transition; natural listening break point |
| At `[SCENE: ...]` tags | 1.5s | Scene change; let the listener reset |
| At `[pause]` tags | 1.5s | Emphasis pause within dialogue |
| At `[long pause]` tags | 4.0s | Comprehension check -- time to think |
| At `[TEACHING SECTION]` tags | 1.0s | Shift from narrative to teaching |
| At `[OAK EXPLAINS: ...]` tags | 0.8s | Brief beat before Oak's definition |
| At `[BLUE'S MISTAKE]` tags | 0.8s | Brief beat before Blue's error |
| At `[THINK ABOUT THIS]` tags | 1.0s | Invitation to pause, before the question |
| Before/after `###` headers | 0.7s | Subsection transition |
| Between paragraphs (within a speaker) | 0.4s | Natural breath pause |
| Between speaker changes | 0.5s | Voice transition beat |
| After chapter summary | 2.0s | Breathing room before comprehension check |
| End of chapter | 3.0s | Clean ending before next track |

### 2. Text Preprocessing

The scripts in `audiobook/scripts/` are already adapted for audio (equations verbalized, DAGs described, etc.), but they still contain markdown formatting and stage directions that must be processed before TTS.

#### What Gets Stripped
- `#`, `##`, `###` header markers (text kept as section announcements)
- `**bold**` and `*italic*` emphasis markers
- `---` horizontal rules (replaced with silence)
- Backtick code markers (if any remain)
- YAML frontmatter block

#### What Gets Transformed

| Pattern | Example | Becomes |
|---|---|---|
| Stage directions | `[SCENE: Morning in Pallet Town.]` | Silence (duration per table above) |
| Pause tags | `[pause]`, `[long pause]` | Silence (1.5s or 4.0s) |
| Teaching tags | `[TEACHING SECTION]`, `[OAK EXPLAINS: Correlation]` | Silence (per table) |
| SFX tags | `[SFX: badge jingle]` | Silence (0.5s) -- placeholder for post-production |
| Character labels | `OAK:` | Triggers voice switch to Oak voice |
| Character labels | `BLUE:` | Triggers voice switch to Blue voice |
| Character labels | `NARRATOR:` | Triggers voice switch to narrator voice |
| Character labels | `MISTY:`, `NURSE JOY:`, `ERIKA:`, etc. | Triggers voice switch to female voice |
| Character labels | `BROCK:`, `BILL:`, `SURGE:`, etc. | Triggers voice switch to Blue/supporting voice |
| Chapter numbers | `Chapter 1:` | `Chapter One:` |
| Section refs | `Chapter 2` (in callbacks) | `Chapter Two` |
| Decimal numbers | `6.8` | `six point eight` (optional; TTS handles most) |
| Acronyms (first use) | `ATE` | Read as spoken in script (already expanded) |
| Abbreviations | `e.g.` | `for example` |
| Abbreviations | `i.e.` | `that is` |
| En-dashes | `--` | Converted to comma or pause depending on context |

#### Character Voice Routing

The preprocessor detects character labels (`CHARACTER:` at line start) and routes subsequent text to the appropriate Kokoro voice until the next label:

```python
VOICE_MAP = {
    "NARRATOR":   {"voice": "am_michael", "speed": 0.90},
    "OAK":        {"voice": "bm_george",  "speed": 0.88},
    "BLUE":       {"voice": "am_adam",     "speed": 0.95},
    # Female characters
    "MISTY":      {"voice": "af_heart",   "speed": 0.92},
    "NURSE JOY":  {"voice": "af_heart",   "speed": 0.90},
    "ERIKA":      {"voice": "af_heart",   "speed": 0.88},
    "SABRINA":    {"voice": "af_heart",   "speed": 0.86},
    "LORELEI":    {"voice": "af_heart",   "speed": 0.88},
    "AGATHA":     {"voice": "af_heart",   "speed": 0.85},
    # Male supporting characters (reuse Blue's voice with speed variation)
    "BROCK":      {"voice": "am_adam",     "speed": 0.88},
    "BILL":       {"voice": "am_adam",     "speed": 0.98},
    "SURGE":      {"voice": "am_adam",     "speed": 0.95},
    "KOGA":       {"voice": "am_adam",     "speed": 0.85},
    "BLAINE":     {"voice": "am_adam",     "speed": 0.93},
    "BRUNO":      {"voice": "am_adam",     "speed": 0.90},
    "LANCE":      {"voice": "am_adam",     "speed": 0.88},
}
```

Supporting characters share base voices but vary speed to create differentiation. This is a practical compromise -- 4 Kokoro voices cover the full cast. The character label itself is NOT spoken aloud; only the dialogue text is synthesized.

#### Processing Order

Transformations run in this sequence to avoid conflicts:
1. Strip YAML frontmatter block
2. Extract H1 as chapter title (remove from body, announce as opening)
3. Identify segment boundaries (character labels, stage directions, headers, rules, paragraphs)
4. For each segment: classify type (dialogue, narration, pause, section header) --> assign voice --> strip remaining markdown formatting --> clean whitespace
5. Return ordered list of typed `TextSegment` objects

### 3. Audio Generation

**Architecture:** Segment-based generation, same approach as the reference pipeline.

```python
TextSegment(type="chapter_title", text="Chapter One. Pallet Town. What Is Causal Inference?", voice="am_michael", speed=0.90)
TextSegment(type="pause", duration=2.5)
TextSegment(type="narration", text="You wake up in a small house...", voice="am_michael", speed=0.90)
TextSegment(type="pause", duration=0.5)
TextSegment(type="dialogue", text="Professor, the data is clear...", voice="am_adam", speed=0.95)
TextSegment(type="pause", duration=1.5)
TextSegment(type="dialogue", text="Is it, though?", voice="bm_george", speed=0.88)
TextSegment(type="pause", duration=0.4)
TextSegment(type="narration", text="Oak sets down the Pokedex...", voice="am_michael", speed=0.90)
...
```

Each text segment is fed to Kokoro's `KPipeline` with the assigned voice, which returns audio at 24kHz. Silence segments are generated as zero-arrays. All segments for a chapter are concatenated into one audio file.

**Voice switching:** A `KPipeline` instance is created for each unique voice. The generator caches these and switches between them per segment. Since Kokoro pipelines are lightweight (~80MB model shared), this adds minimal overhead.

### 4. Output & Metadata

**File naming:** `00_FRONT_MATTER.mp3`, `01_CH01_PALLET_TOWN.mp3`, ..., `08_CH08_INDIGO_PLATEAU.mp3`, `09_APPENDIX_MATH.mp3`, `10_APPENDIX_POKEDEX.mp3`

**ID3 tags on every file:**
- Title: chapter title (e.g., "Chapter 1: Pallet Town -- What Is Causal Inference?")
- Album: "Causal Inference: A Pokemon Approach -- Kanto Region Edition"
- Artist / Album Artist: author name
- Track number: sequential
- Genre: "Education"
- Year: 2026

### 5. Progress Tracking & Resume

A `progress.json` file in the output directory tracks:
- Which chapters are completed
- Which chapter is currently in progress
- Duration of each completed chapter

The `--resume` flag skips completed chapters, allowing the script to be stopped and restarted without losing work.

### 6. Manifest

After generation, a `manifest.json` is created with:
- Total duration and formatted time
- Voice and speed settings used
- Per-track metadata (title, file path, duration, word count)

### 7. Full Audiobook Combination

Optional `--combine` flag concatenates all chapter MP3s into a single `full_audiobook.mp3` with 3s silence between chapters.

---

## CLI Interface

```bash
python generate_audiobook.py                    # Generate all chapters
python generate_audiobook.py --resume           # Resume from last checkpoint
python generate_audiobook.py --chapter ch01     # Generate single chapter
python generate_audiobook.py --combine          # Combine existing chapters into one file
python generate_audiobook.py --narrator-voice af_heart  # Override narrator voice
python generate_audiobook.py --speed 1.0        # Override all speeds
python generate_audiobook.py --single-voice     # Use narrator voice for all characters
python generate_audiobook.py --preview ch01     # Show preprocessed text segments (no audio)
python generate_audiobook.py --dry-run          # Show segment count and estimated duration per chapter
```

---

## Voice Options

### Primary Voices (Multi-Voice Mode)

| Role | Voice | Description | Speed |
|---|---|---|---|
| Narrator | `am_michael` | Clear American male. Warm, curious, carries the story. | 0.90 |
| Professor Oak | `bm_george` | British male. Measured, professorial, authoritative. | 0.88 |
| Blue / Male supporting | `am_adam` | American male (alt). Brash, confident energy. | 0.95 |
| Female characters | `af_heart` | American female. Natural, warm. | 0.90 |

### Single-Voice Mode (`--single-voice`)

Uses only the narrator voice for everything. Simpler, faster generation. Character names are prepended to their lines ("Professor Oak says:") for clarity.

### Alternative Voices

| Voice | Description | Notes |
|---|---|---|
| `af_bella` | American female (alt) | Another female option for narrator |
| `bf_emma` | British female | Could replace `af_heart` for female cast |
| `bm_lewis` | British male (alt) | Could replace `bm_george` for Oak |
| `am_echo` | American male (alt) | Another option for Blue |

Any voice can be changed at any time and individual chapters regenerated.

---

## Edge Cases Handled

1. **Chapter 8 is ~16,000 source words** (longest chapter, ~100 min audio) -- generator processes incrementally by segment, no memory issues
2. **Multi-paragraph character dialogue** -- consecutive paragraphs under the same character label stay on the same voice until a new label appears
3. **Comprehension check pauses** -- `[long pause]` tags insert 4s silence; enough time for the listener to formulate a thought
4. **Nested stage directions** -- `[OAK EXPLAINS: Correlation]` is stripped and replaced with an 0.8s pause; the actual explanation follows as Oak dialogue
5. **Numbers in dialogue** -- decimals like `6.8` are left as-is for TTS (Kokoro handles "six point eight" naturally); scripts can also pre-expand them
6. **Acronyms** -- Terms like ATE, ATT, RDD, DiD, IPW are spelled out on first use in scripts and spoken as words thereafter (Kokoro pronounces short acronyms well)
7. **Greek-origin terms** -- "heteroscedasticity", "homoscedasticity" etc. handled via pronunciation guide; Kokoro generally handles these correctly
8. **Pokemon names** -- standard English pronunciation; Kokoro handles these natively
9. **En-dash pairs** (`--`) -- preprocessor converts to commas or removes depending on syntactic position
10. **Empty paragraphs / whitespace** -- stripped; no silent segments generated for blank lines
11. **YAML frontmatter** -- stripped before processing; metadata used only for ID3 tags and manifest

---

## Script Adaptation Order (Writing Phases)

The scripts must be written before audio can be generated. This is the creative work.

### Phase 1: Templates & Guides
Create scaffolding files:
- `audiobook/templates/chapter_template.md`
- `audiobook/templates/transformation_patterns.md`
- `audiobook/production/character_guide.md`
- `audiobook/production/pronunciation_guide.md`

### Phase 2: Chapters 1-2 (Pilot Scripts)
Write `ch01_pallet_town.md` and `ch02_pewter_city.md`. These set every convention for the entire audiobook -- narrator voice, Oak's teaching style, Blue's mistake pattern, equation verbalization, comprehension check format, pacing. Also write `00_front_matter.md`.

Source: `textbook/chapters/ch01_pallet_town.md` (9,571 words) and `ch02_pewter_city.md` (10,557 words)

### Phase 3: Chapter 3 (DAG Stress Test)
Write `ch03_cerulean_city.md`. The hardest adaptation -- DAGs are inherently visual. If the verbal arrow map approach works here, it works everywhere. Also introduces the largest cast (Misty, Bill, Blue, Oak).

Source: `textbook/chapters/ch03_cerulean_city.md` (12,162 words)

### Phase 4: Chapters 4-5
Write `ch04_vermilion_city.md` and `ch05_celadon_city.md`. Moderately visual (Love plots, regression output) but more straightforward than DAGs.

Source: `ch04_vermilion_city.md` (10,265 words) and `ch05_celadon_city.md` (10,499 words)

### Phase 5: Chapters 6-7
Write `ch06_fuchsia_cinnabar.md` and `ch07_saffron_city.md`. Ch6 spans two cities (natural two-act structure). Ch7 introduces panel data / time-series concepts.

Source: `ch06_fuchsia_cinnabar.md` (13,408 words) and `ch07_saffron_city.md` (12,095 words)

### Phase 6: Chapter 8 (Finale)
Write `ch08_indigo_plateau.md`. Longest chapter (~16,000 words), 10+ sections, culminates in the Champion Battle where Blue makes 6 final causal fallacies. The most naturally audio-native content in the entire book.

Source: `textbook/chapters/ch08_indigo_plateau.md` (16,153 words)

### Phase 7: Back Matter & Generation Script
- Write `appendix_math_foundations.md` and `appendix_causal_pokedex.md`
- Build `generate_audiobook.py`
- Generate all audio
- Review and iterate

---

## Estimated Output

| Metric | Value |
|---|---|
| Total chapters | 11 files (8 chapters + front matter + 2 appendices) |
| Source word count | ~110,000 (textbook), ~105,000 (adapted scripts) |
| Total audio | ~12-13 hours |
| Total file size | ~1.0 GB (MP3 192kbps) |
| Average chapter | ~70 minutes |
| Longest chapter | Ch8 Indigo Plateau (~100 minutes) |
| Shortest chapter | Front Matter (~10 minutes) |
| Shortest main chapter | Ch1 Pallet Town (~60 minutes) |
| Voice count | 4 Kokoro voices (narrator, Oak, Blue/male, female) |
| Generation time | ~10-15 minutes |
