from __future__ import annotations

import math
import struct
import subprocess
import wave
from pathlib import Path

from create_facebook_portfolio_video import (
    COVER_PATH,
    FRAME_DIR,
    OUTPUT_DIR,
    ROOT,
    SLIDES,
    create_slide,
)


VOICEOVER_PATH = Path(r"C:\Users\gerla\Downloads\CapCut_TTS_Jessie_D20260512_T150851.mp3")
MUSIC_PATH = OUTPUT_DIR / "neuraldev-marketing-background.wav"
CONCAT_VIDEO_PATH = OUTPUT_DIR / "facebook_promo_voiceover_concat.txt"
MIXED_AUDIO_PATH = OUTPUT_DIR / "neuraldev-voiceover-music-mix.m4a"
FINAL_VIDEO_PATH = OUTPUT_DIR / "neuraldev-facebook-portfolio-promo-voiceover.mp4"
SEGMENT_DIR = OUTPUT_DIR / "facebook_promo_voiceover_segments"

SAMPLE_RATE = 44100
FPS = 30


def ffprobe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def generate_marketing_music(duration: float) -> None:
    MUSIC_PATH.parent.mkdir(parents=True, exist_ok=True)

    chords = [
        (261.63, 329.63, 392.00),  # C
        (196.00, 246.94, 392.00),  # G
        (220.00, 261.63, 329.63),  # Am
        (174.61, 261.63, 349.23),  # F
    ]
    arp_notes = [523.25, 659.25, 783.99, 987.77, 880.00, 783.99, 659.25, 523.25]
    beat = 0.5
    total_samples = int((duration + 0.35) * SAMPLE_RATE)

    with wave.open(str(MUSIC_PATH), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(2)
        output.setframerate(SAMPLE_RATE)

        for sample_index in range(total_samples):
            t = sample_index / SAMPLE_RATE
            chord = chords[int(t // 4) % len(chords)]

            pad = 0.0
            for note in chord:
                pad += math.sin(2 * math.pi * note * t) * 0.055
                pad += math.sin(2 * math.pi * note * 2 * t) * 0.012

            step = int(t / beat) % len(arp_notes)
            step_pos = (t % beat) / beat
            pluck_env = max(0.0, 1.0 - step_pos) ** 2
            pluck = math.sin(2 * math.pi * arp_notes[step] * t) * 0.075 * pluck_env

            hat = 0.0
            hat_pos = (t % 0.25) / 0.25
            if hat_pos < 0.12:
                hat = math.sin(2 * math.pi * 7800 * t) * 0.018 * (1 - hat_pos / 0.12)

            kick_pos = t % 1.0
            kick = 0.0
            if kick_pos < 0.18:
                kick_freq = 90 - (kick_pos / 0.18) * 40
                kick = math.sin(2 * math.pi * kick_freq * t) * 0.12 * (1 - kick_pos / 0.18)

            snare_pos = (t + 0.5) % 1.0
            snare = 0.0
            if snare_pos < 0.10:
                snare = math.sin(2 * math.pi * 1600 * t) * 0.035 * (1 - snare_pos / 0.10)

            fade_in = min(1.0, t / 1.0)
            fade_out = min(1.0, max(0.0, (duration - t) / 1.25))
            sample = (pad + pluck + hat + kick + snare) * fade_in * fade_out
            sample = max(-0.95, min(0.95, sample))
            packed = struct.pack("<hh", int(sample * 32767), int(sample * 32767))
            output.writeframesraw(packed)


def slide_durations(total_duration: float) -> list[float]:
    weights = [0.10, 0.14, 0.14, 0.16, 0.18, 0.14, 0.14]
    durations = [round(total_duration * weight, 2) for weight in weights]
    durations[-1] = round(total_duration - sum(durations[:-1]), 2)
    return durations


def render_segments(frames: list[Path], durations: list[float]) -> list[Path]:
    SEGMENT_DIR.mkdir(parents=True, exist_ok=True)
    segments: list[Path] = []

    for index, (frame, duration) in enumerate(zip(frames, durations, strict=True)):
        segment = SEGMENT_DIR / f"segment_{index:02}.mp4"
        frame_count = max(1, round(duration * FPS))
        fade_duration = min(0.45, max(0.2, duration / 5))
        fade_out_start = max(0, (frame_count / FPS) - fade_duration)
        pan_direction = 1 if index % 2 == 0 else -1
        x_expr = (
            "iw/2-(iw/zoom/2)"
            if pan_direction > 0
            else "iw/2-(iw/zoom/2)-((on/{frames})*18)"
        ).format(frames=frame_count)
        y_expr = "ih/2-(ih/zoom/2)+sin(on/{frames}*PI)*10".format(frames=frame_count)
        zoom_expr = "1+0.035*on/{frames}".format(frames=frame_count)
        video_filter = (
            f"zoompan=z='{zoom_expr}':x='{x_expr}':y='{y_expr}':"
            f"d={frame_count}:s=1080x1920:fps={FPS},"
            f"fade=t=in:st=0:d={fade_duration:.2f},"
            f"fade=t=out:st={fade_out_start:.2f}:d={fade_duration:.2f},"
            "eq=contrast=1.04:saturation=1.08:brightness=0.01,"
            "unsharp=5:5:0.45:3:3:0.15,"
            "format=yuv420p"
        )
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                str(frame),
                "-vf",
                video_filter,
                "-frames:v",
                str(frame_count),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                str(segment),
            ],
            check=True,
            cwd=ROOT,
        )
        segments.append(segment)

    return segments


def concat_segments(segments: list[Path], video_path: Path) -> None:
    lines = [f"file '{segment.as_posix()}'" for segment in segments]
    CONCAT_VIDEO_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(CONCAT_VIDEO_PATH),
            "-c",
            "copy",
            str(video_path),
        ],
        check=True,
        cwd=ROOT,
    )


def mix_audio(voice_duration: float) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(VOICEOVER_PATH),
            "-i",
            str(MUSIC_PATH),
            "-filter_complex",
            (
                f"[0:a]volume=1.0[a0];"
                f"[1:a]volume=0.18,afade=t=out:st={max(0, voice_duration - 1.2):.2f}:d=1.2[a1];"
                "[a0][a1]amix=inputs=2:duration=first:dropout_transition=0[aout]"
            ),
            "-map",
            "[aout]",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(MIXED_AUDIO_PATH),
        ],
        check=True,
        cwd=ROOT,
    )


def combine_video_audio(video_path: Path) -> None:
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(MIXED_AUDIO_PATH),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            "-movflags",
            "+faststart",
            str(FINAL_VIDEO_PATH),
        ],
        check=True,
        cwd=ROOT,
    )


def main() -> None:
    if not VOICEOVER_PATH.exists():
        raise FileNotFoundError(f"Voiceover file not found: {VOICEOVER_PATH}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAME_DIR.mkdir(parents=True, exist_ok=True)

    voice_duration = ffprobe_duration(VOICEOVER_PATH)
    frames = [create_slide(slide, index) for index, slide in enumerate(SLIDES)]
    frames[0].replace(COVER_PATH)
    frames[0] = COVER_PATH

    video_only_path = OUTPUT_DIR / "neuraldev-facebook-portfolio-promo-voiceover-video-only.mp4"
    durations = slide_durations(voice_duration)
    segments = render_segments(frames, durations)
    concat_segments(segments, video_only_path)

    generate_marketing_music(voice_duration)
    mix_audio(voice_duration)
    combine_video_audio(video_only_path)

    print(f"Voiceover duration: {voice_duration:.2f}s")
    print(f"Created {MUSIC_PATH}")
    print(f"Created {MIXED_AUDIO_PATH}")
    print(f"Created {FINAL_VIDEO_PATH}")


if __name__ == "__main__":
    main()
