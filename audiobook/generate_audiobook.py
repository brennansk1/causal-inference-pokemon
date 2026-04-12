#!/usr/bin/env python3
"""
Generate audiobook from adapted chapter scripts using Kokoro TTS.

Usage:
    python generate_audiobook.py                    # Generate all chapters
    python generate_audiobook.py --resume           # Resume from last checkpoint
    python generate_audiobook.py --chapter ch01     # Generate single chapter
    python generate_audiobook.py --combine          # Combine into one file
    python generate_audiobook.py --single-voice     # Use narrator voice for all
    python generate_audiobook.py --preview ch01     # Show preprocessed text (no audio)
    python generate_audiobook.py --dry-run          # Show segments and estimated duration
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np
import soundfile as sf
import yaml
from pydub import AudioSegment
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, TRCK, TCON, TDRC
from mutagen.mp3 import MP3

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SAMPLE_RATE = 24_000
MP3_BITRATE = "192k"
ALBUM_TITLE = "Causal Inference: A Pokemon Approach -- Kanto Region Edition"
ARTIST = "Causal Inference Textbook Project"
GENRE = "Education"
YEAR = "2026"

SCRIPTS_DIR = Path(__file__).parent / "scripts"
OUTPUT_DIR = Path(__file__).parent / "output"
WAV_DIR = OUTPUT_DIR / "wav"
MP3_DIR = OUTPUT_DIR / "mp3"

# Chapter ordering (matches textbook structure)
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

# Voice assignments per character
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
    # Male supporting characters
    "BROCK":      {"voice": "am_adam",     "speed": 0.88},
    "BILL":       {"voice": "am_adam",     "speed": 0.98},
    "SURGE":      {"voice": "am_adam",     "speed": 0.95},
    "KOGA":       {"voice": "am_adam",     "speed": 0.85},
    "BLAINE":     {"voice": "am_adam",     "speed": 0.93},
    "BRUNO":      {"voice": "am_adam",     "speed": 0.90},
    "LANCE":      {"voice": "am_adam",     "speed": 0.88},
}

# Pause durations in seconds
PAUSE_DURATIONS = {
    "chapter_title": 2.5,
    "part_header": 2.0,
    "scene": 1.5,
    "pause": 1.5,
    "long_pause": 4.0,
    "teaching_section": 1.0,
    "oak_explains": 0.8,
    "blues_mistake": 0.8,
    "think_about_this": 1.0,
    "subsection_header": 0.7,
    "paragraph_break": 0.4,
    "speaker_change": 0.5,
    "chapter_end": 3.0,
    "sfx": 0.5,
    "horizontal_rule": 1.5,
}


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class TextSegment:
    """A segment of audio to generate."""
    type: str  # "speech", "pause", "chapter_title", "section_header"
    text: str = ""
    voice: str = "am_michael"
    speed: float = 0.90
    duration: float = 0.0  # for pauses


@dataclass
class ChapterMeta:
    """Metadata parsed from script frontmatter."""
    title: str = ""
    chapter_number: int = 0
    source_file: str = ""
    estimated_runtime_minutes: int = 0
    key_concepts: list = field(default_factory=list)
    characters: list = field(default_factory=list)


# ---------------------------------------------------------------------------
# Text Preprocessing
# ---------------------------------------------------------------------------

# Regex for stage directions
RE_SCENE = re.compile(r"^\[SCENE:.*?\]$", re.MULTILINE)
RE_PAUSE = re.compile(r"^\[pause\]$", re.MULTILINE)
RE_LONG_PAUSE = re.compile(r"^\[long pause\]$", re.MULTILINE)
RE_TEACHING = re.compile(r"^\[TEACHING SECTION\]$", re.MULTILINE)
RE_OAK_EXPLAINS = re.compile(r"^\[OAK EXPLAINS:.*?\]$", re.MULTILINE)
RE_BLUES_MISTAKE = re.compile(r"^\[BLUE'S MISTAKE\]$", re.MULTILINE)
RE_THINK = re.compile(r"^\[THINK ABOUT THIS\]$", re.MULTILINE)
RE_SFX = re.compile(r"^\[SFX:.*?\]$", re.MULTILINE)
RE_SPEAKER = re.compile(r"^([A-Z][A-Z\s]+?):\s*(.*)$")
RE_HEADER_H1 = re.compile(r"^#\s+(.+)$", re.MULTILINE)
RE_HEADER_H2 = re.compile(r"^##\s+(.+)$", re.MULTILINE)
RE_HEADER_H3 = re.compile(r"^###\s+(.+)$", re.MULTILINE)
RE_HR = re.compile(r"^---+$", re.MULTILINE)


def parse_frontmatter(text: str) -> tuple[ChapterMeta, str]:
    """Extract YAML frontmatter and return metadata + body."""
    if not text.startswith("---"):
        return ChapterMeta(), text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return ChapterMeta(), text

    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return ChapterMeta(), text

    meta = ChapterMeta(
        title=data.get("title", ""),
        chapter_number=data.get("chapter_number", 0),
        source_file=data.get("source_file", ""),
        estimated_runtime_minutes=data.get("estimated_runtime_minutes", 0),
        key_concepts=data.get("key_concepts", []),
        characters=data.get("characters", []),
    )
    body = parts[2].strip()
    return meta, body


def clean_markdown(text: str) -> str:
    """Strip remaining markdown formatting from speech text."""
    # Bold and italic
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    # Backticks
    text = re.sub(r"`(.+?)`", r"\1", text)
    # Common abbreviations
    text = text.replace("e.g.", "for example")
    text = text.replace("i.e.", "that is")
    text = text.replace("etc.", "and so on")
    text = text.replace("vs.", "versus")
    # En-dashes (double hyphen) to comma or space
    text = text.replace(" -- ", ", ")
    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def number_to_words_chapter(text: str) -> str:
    """Convert 'Chapter N' references to words."""
    word_map = {
        "0": "Zero", "1": "One", "2": "Two", "3": "Three",
        "4": "Four", "5": "Five", "6": "Six", "7": "Seven",
        "8": "Eight", "9": "Nine", "10": "Ten",
    }
    def replace_chapter(m):
        n = m.group(1)
        return f"Chapter {word_map.get(n, n)}"
    text = re.sub(r"Chapter (\d+)", replace_chapter, text)
    return text


def preprocess_script(body: str, single_voice: bool = False) -> list[TextSegment]:
    """Convert a script body into a list of TextSegments for TTS."""
    segments: list[TextSegment] = []
    current_voice = VOICE_MAP["NARRATOR"]
    current_speaker = "NARRATOR"

    lines = body.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1

        # Skip empty lines
        if not line:
            continue

        # --- Horizontal rules ---
        if RE_HR.match(line):
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["horizontal_rule"]))
            continue

        # --- H1: Chapter title ---
        m = RE_HEADER_H1.match(line)
        if m:
            title = clean_markdown(m.group(1))
            title = number_to_words_chapter(title)
            segments.append(TextSegment(
                type="chapter_title", text=title,
                voice=current_voice["voice"], speed=current_voice["speed"],
            ))
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["chapter_title"]))
            continue

        # --- H2: Part header ---
        m = RE_HEADER_H2.match(line)
        if m:
            header = clean_markdown(m.group(1))
            header = number_to_words_chapter(header)
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["part_header"]))
            segments.append(TextSegment(
                type="section_header", text=header,
                voice=current_voice["voice"], speed=current_voice["speed"],
            ))
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["part_header"]))
            continue

        # --- H3: Subsection header ---
        m = RE_HEADER_H3.match(line)
        if m:
            header = clean_markdown(m.group(1))
            header = number_to_words_chapter(header)
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["subsection_header"]))
            segments.append(TextSegment(
                type="section_header", text=header,
                voice=current_voice["voice"], speed=current_voice["speed"],
            ))
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["subsection_header"]))
            continue

        # --- Stage directions ---
        if RE_SCENE.match(line):
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["scene"]))
            continue
        if RE_PAUSE.match(line):
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["pause"]))
            continue
        if RE_LONG_PAUSE.match(line):
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["long_pause"]))
            continue
        if RE_TEACHING.match(line):
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["teaching_section"]))
            continue
        if RE_OAK_EXPLAINS.match(line):
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["oak_explains"]))
            continue
        if RE_BLUES_MISTAKE.match(line):
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["blues_mistake"]))
            continue
        if RE_THINK.match(line):
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["think_about_this"]))
            continue
        if RE_SFX.match(line):
            segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["sfx"]))
            continue

        # --- Speaker dialogue ---
        m = RE_SPEAKER.match(line)
        if m:
            speaker = m.group(1).strip()
            text = m.group(2).strip()

            # Collect continuation lines (indented or plain text until next speaker/direction)
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line:
                    i += 1
                    break
                if RE_SPEAKER.match(next_line):
                    break
                if next_line.startswith("[") or next_line.startswith("#") or RE_HR.match(next_line):
                    break
                text += " " + next_line
                i += 1

            text = clean_markdown(text)
            text = number_to_words_chapter(text)

            if not text:
                continue

            # Voice routing
            if single_voice:
                voice_cfg = VOICE_MAP["NARRATOR"]
                if speaker != "NARRATOR":
                    text = f"{speaker.title()} says: {text}"
            else:
                voice_cfg = VOICE_MAP.get(speaker, VOICE_MAP["NARRATOR"])

            # Speaker change pause
            if speaker != current_speaker:
                segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["speaker_change"]))
                current_speaker = speaker

            segments.append(TextSegment(
                type="speech", text=text,
                voice=voice_cfg["voice"], speed=voice_cfg["speed"],
            ))
            current_voice = voice_cfg
            continue

        # --- Plain text (narration without speaker tag) ---
        text = clean_markdown(line)
        text = number_to_words_chapter(text)
        if text:
            segments.append(TextSegment(
                type="speech", text=text,
                voice=current_voice["voice"], speed=current_voice["speed"],
            ))

    # End-of-chapter pause
    segments.append(TextSegment(type="pause", duration=PAUSE_DURATIONS["chapter_end"]))
    return segments


# ---------------------------------------------------------------------------
# Audio Generation
# ---------------------------------------------------------------------------

def generate_silence(duration: float, sample_rate: int = SAMPLE_RATE) -> np.ndarray:
    """Generate silence as a zero array."""
    return np.zeros(int(duration * sample_rate), dtype=np.float32)


def generate_chapter_audio(
    segments: list[TextSegment],
    pipelines: dict,
    sample_rate: int = SAMPLE_RATE,
) -> np.ndarray:
    """Generate audio for all segments, concatenating into one array."""
    audio_parts: list[np.ndarray] = []
    total = len(segments)

    for idx, seg in enumerate(segments):
        if seg.type == "pause":
            audio_parts.append(generate_silence(seg.duration, sample_rate))
        elif seg.type in ("speech", "chapter_title", "section_header"):
            if not seg.text:
                continue
            pipeline = pipelines[seg.voice]
            # Kokoro generates audio from text; voice passed per call
            try:
                generator = pipeline(seg.text, voice=seg.voice, speed=seg.speed)
                for _, _, audio in generator:
                    audio_parts.append(audio)
            except Exception as e:
                print(f"  WARNING: TTS failed for segment {idx}: {e}")
                print(f"    Text: {seg.text[:80]}...")
                # Insert silence equivalent to estimated duration
                est_duration = len(seg.text.split()) / 150 * 60  # rough estimate
                audio_parts.append(generate_silence(est_duration, sample_rate))

        if (idx + 1) % 50 == 0:
            print(f"  Processed {idx + 1}/{total} segments...")

    if not audio_parts:
        return np.zeros(sample_rate, dtype=np.float32)  # 1s silence fallback

    return np.concatenate(audio_parts)


def wav_to_mp3(wav_path: Path, mp3_path: Path, bitrate: str = MP3_BITRATE) -> None:
    """Convert WAV to MP3 using pydub."""
    audio = AudioSegment.from_wav(str(wav_path))
    audio.export(str(mp3_path), format="mp3", bitrate=bitrate)


def tag_mp3(mp3_path: Path, title: str, track_number: int, total_tracks: int) -> None:
    """Write ID3 tags to an MP3 file."""
    try:
        audio = MP3(str(mp3_path))
        if audio.tags is None:
            audio.add_tags()
        audio.tags.add(TIT2(encoding=3, text=title))
        audio.tags.add(TALB(encoding=3, text=ALBUM_TITLE))
        audio.tags.add(TPE1(encoding=3, text=ARTIST))
        audio.tags.add(TPE2(encoding=3, text=ARTIST))
        audio.tags.add(TRCK(encoding=3, text=f"{track_number}/{total_tracks}"))
        audio.tags.add(TCON(encoding=3, text=GENRE))
        audio.tags.add(TDRC(encoding=3, text=YEAR))
        audio.save()
    except Exception as e:
        print(f"  WARNING: Could not tag {mp3_path}: {e}")


# ---------------------------------------------------------------------------
# Progress Tracking
# ---------------------------------------------------------------------------

def load_progress(output_dir: Path) -> dict:
    """Load progress from JSON file."""
    progress_file = output_dir / "progress.json"
    if progress_file.exists():
        return json.loads(progress_file.read_text())
    return {"completed": [], "current": None, "durations": {}}


def save_progress(output_dir: Path, progress: dict) -> None:
    """Save progress to JSON file."""
    progress_file = output_dir / "progress.json"
    progress_file.write_text(json.dumps(progress, indent=2))


def save_manifest(output_dir: Path, tracks: list[dict]) -> None:
    """Save manifest with all track metadata."""
    total_duration = sum(t.get("duration", 0) for t in tracks)
    hours = int(total_duration // 3600)
    minutes = int((total_duration % 3600) // 60)
    total_words = sum(t.get("word_count", 0) for t in tracks)

    manifest = {
        "album": ALBUM_TITLE,
        "artist": ARTIST,
        "total_duration_seconds": round(total_duration, 1),
        "total_duration_formatted": f"{hours}h {minutes}m",
        "total_words": total_words,
        "total_tracks": len(tracks),
        "voice_config": VOICE_MAP,
        "tracks": tracks,
    }
    manifest_file = output_dir / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2))
    print(f"\nManifest written to {manifest_file}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def init_pipelines(voices: set[str]) -> dict:
    """Initialize Kokoro TTS pipelines per language code.

    Kokoro uses one pipeline per language (a=American, b=British).
    The voice name is passed per generation call, not at init time.
    Returns a dict mapping voice name -> pipeline instance.
    """
    try:
        from kokoro import KPipeline
    except ImportError:
        print("ERROR: kokoro not installed. Run: pip install kokoro")
        sys.exit(1)

    # Determine unique language codes needed
    lang_pipelines = {}
    voice_to_pipeline = {}
    for voice in voices:
        lang_code = "a" if voice.startswith("a") else "b"
        if lang_code not in lang_pipelines:
            print(f"  Loading pipeline: lang={lang_code}")
            lang_pipelines[lang_code] = KPipeline(lang_code=lang_code)
        voice_to_pipeline[voice] = lang_pipelines[lang_code]
    return voice_to_pipeline


def get_file_label(filename: str) -> str:
    """Convert script filename to output label."""
    stem = Path(filename).stem
    return stem.upper()


def process_chapter(
    script_path: Path,
    track_number: int,
    total_tracks: int,
    pipelines: dict,
    single_voice: bool = False,
) -> Optional[dict]:
    """Process a single chapter: preprocess, generate audio, convert to MP3."""
    print(f"\n{'='*60}")
    print(f"Processing: {script_path.name} (track {track_number}/{total_tracks})")
    print(f"{'='*60}")

    text = script_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    segments = preprocess_script(body, single_voice=single_voice)

    word_count = sum(len(s.text.split()) for s in segments if s.text)
    speech_segments = [s for s in segments if s.type == "speech"]
    pause_segments = [s for s in segments if s.type == "pause"]
    total_pause = sum(s.duration for s in pause_segments)

    print(f"  Title: {meta.title}")
    print(f"  Segments: {len(segments)} ({len(speech_segments)} speech, {len(pause_segments)} pauses)")
    print(f"  Words: {word_count}")
    print(f"  Pause time: {total_pause:.1f}s")
    est_minutes = word_count / 150 + total_pause / 60
    print(f"  Estimated duration: ~{est_minutes:.0f} min")

    # Generate audio
    t0 = time.time()
    audio = generate_chapter_audio(segments, pipelines)
    gen_time = time.time() - t0
    duration = len(audio) / SAMPLE_RATE

    print(f"  Generated: {duration:.1f}s ({duration/60:.1f} min) in {gen_time:.1f}s")

    # Save WAV
    label = get_file_label(script_path.name)
    wav_path = WAV_DIR / f"{track_number:02d}_{label}.wav"
    sf.write(str(wav_path), audio, SAMPLE_RATE)
    print(f"  WAV: {wav_path}")

    # Convert to MP3
    mp3_path = MP3_DIR / f"{track_number:02d}_{label}.mp3"
    wav_to_mp3(wav_path, mp3_path)
    print(f"  MP3: {mp3_path}")

    # Tag MP3
    tag_mp3(mp3_path, meta.title or script_path.stem, track_number, total_tracks)

    return {
        "track_number": track_number,
        "title": meta.title or script_path.stem,
        "file": str(mp3_path.name),
        "duration": round(duration, 1),
        "word_count": word_count,
        "segments": len(segments),
    }


def combine_audiobook(mp3_dir: Path, output_path: Path) -> None:
    """Concatenate all chapter MP3s into a single file."""
    print(f"\nCombining all chapters into {output_path}...")
    mp3_files = sorted(mp3_dir.glob("*.mp3"))
    if not mp3_files:
        print("ERROR: No MP3 files found to combine.")
        return

    combined = AudioSegment.empty()
    silence_between = AudioSegment.silent(duration=3000)  # 3s between chapters

    for mp3_file in mp3_files:
        print(f"  Adding: {mp3_file.name}")
        chapter = AudioSegment.from_mp3(str(mp3_file))
        if len(combined) > 0:
            combined += silence_between
        combined += chapter

    combined.export(str(output_path), format="mp3", bitrate=MP3_BITRATE)
    duration = len(combined) / 1000
    print(f"  Total: {duration/3600:.1f} hours ({duration/60:.0f} min)")
    print(f"  Output: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate audiobook from chapter scripts.")
    parser.add_argument("--resume", action="store_true", help="Resume from last checkpoint")
    parser.add_argument("--chapter", type=str, help="Generate a single chapter (e.g., ch01)")
    parser.add_argument("--combine", action="store_true", help="Combine existing chapters into one file")
    parser.add_argument("--single-voice", action="store_true", help="Use narrator voice for all characters")
    parser.add_argument("--narrator-voice", type=str, help="Override narrator voice")
    parser.add_argument("--speed", type=float, help="Override all voice speeds")
    parser.add_argument("--preview", type=str, help="Show preprocessed segments (no audio)")
    parser.add_argument("--dry-run", action="store_true", help="Show segment counts and estimates")
    args = parser.parse_args()

    # Apply overrides
    if args.narrator_voice:
        VOICE_MAP["NARRATOR"]["voice"] = args.narrator_voice
    if args.speed:
        for v in VOICE_MAP.values():
            v["speed"] = args.speed

    # Ensure output dirs exist
    WAV_DIR.mkdir(parents=True, exist_ok=True)
    MP3_DIR.mkdir(parents=True, exist_ok=True)

    # --- Combine mode ---
    if args.combine:
        combine_audiobook(MP3_DIR, OUTPUT_DIR / "full_audiobook.mp3")
        return

    # --- Preview mode ---
    if args.preview:
        matches = [f for f in CHAPTER_ORDER if args.preview in f]
        if not matches:
            print(f"ERROR: No chapter matching '{args.preview}'")
            return
        script_path = SCRIPTS_DIR / matches[0]
        text = script_path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        segments = preprocess_script(body, single_voice=args.single_voice)
        for idx, seg in enumerate(segments):
            if seg.type == "pause":
                print(f"  [{idx:04d}] PAUSE {seg.duration:.1f}s")
            else:
                print(f"  [{idx:04d}] {seg.type.upper()} [{seg.voice} @{seg.speed}] {seg.text[:100]}")
        return

    # --- Dry-run mode ---
    if args.dry_run:
        print(f"\n{'Chapter':<40} {'Words':>8} {'Segments':>10} {'Est. Min':>10}")
        print("-" * 70)
        total_words = 0
        total_est = 0
        for filename in CHAPTER_ORDER:
            script_path = SCRIPTS_DIR / filename
            if not script_path.exists():
                print(f"  {filename:<40} {'MISSING':>8}")
                continue
            text = script_path.read_text(encoding="utf-8")
            _, body = parse_frontmatter(text)
            segments = preprocess_script(body, single_voice=args.single_voice)
            word_count = sum(len(s.text.split()) for s in segments if s.text)
            total_pause = sum(s.duration for s in segments if s.type == "pause")
            est = word_count / 150 + total_pause / 60
            total_words += word_count
            total_est += est
            print(f"  {filename:<40} {word_count:>8} {len(segments):>10} {est:>10.0f}")
        print("-" * 70)
        print(f"  {'TOTAL':<40} {total_words:>8} {'':>10} {total_est:>10.0f}")
        print(f"\n  Estimated total: ~{total_est/60:.1f} hours")
        return

    # --- Determine which chapters to process ---
    if args.chapter:
        matches = [f for f in CHAPTER_ORDER if args.chapter in f]
        if not matches:
            print(f"ERROR: No chapter matching '{args.chapter}'")
            return
        chapters_to_process = matches
    else:
        chapters_to_process = list(CHAPTER_ORDER)

    # --- Resume: skip completed ---
    progress = load_progress(OUTPUT_DIR)
    if args.resume:
        chapters_to_process = [c for c in chapters_to_process if c not in progress["completed"]]
        if not chapters_to_process:
            print("All chapters already completed!")
            return
        print(f"Resuming: {len(progress['completed'])} completed, {len(chapters_to_process)} remaining")

    # --- Collect required voices ---
    required_voices = set()
    if args.single_voice:
        required_voices.add(VOICE_MAP["NARRATOR"]["voice"])
    else:
        for v in VOICE_MAP.values():
            required_voices.add(v["voice"])

    # --- Initialize TTS ---
    print(f"\nInitializing Kokoro TTS with {len(required_voices)} voices...")
    pipelines = init_pipelines(required_voices)
    print("TTS ready.\n")

    # --- Process chapters ---
    total_tracks = len(CHAPTER_ORDER)
    tracks: list[dict] = []

    for filename in chapters_to_process:
        script_path = SCRIPTS_DIR / filename
        if not script_path.exists():
            print(f"\nWARNING: Script not found: {script_path}")
            continue

        track_number = CHAPTER_ORDER.index(filename) + 1
        progress["current"] = filename
        save_progress(OUTPUT_DIR, progress)

        track_info = process_chapter(
            script_path, track_number, total_tracks,
            pipelines, single_voice=args.single_voice,
        )
        if track_info:
            tracks.append(track_info)
            progress["completed"].append(filename)
            progress["durations"][filename] = track_info["duration"]
            progress["current"] = None
            save_progress(OUTPUT_DIR, progress)

    # --- Save manifest ---
    if tracks:
        save_manifest(OUTPUT_DIR, tracks)

    print(f"\n{'='*60}")
    print("AUDIOBOOK GENERATION COMPLETE")
    print(f"{'='*60}")
    total_duration = sum(t["duration"] for t in tracks)
    print(f"  Tracks: {len(tracks)}")
    print(f"  Total duration: {total_duration/3600:.1f} hours ({total_duration/60:.0f} min)")
    print(f"  Output: {MP3_DIR}")


if __name__ == "__main__":
    main()
