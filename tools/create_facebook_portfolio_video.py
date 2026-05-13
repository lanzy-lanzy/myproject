from __future__ import annotations

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
PROJECT_DIR = ROOT / "media" / "projects"
OUTPUT_DIR = ROOT / "media" / "social"
FRAME_DIR = OUTPUT_DIR / "facebook_promo_frames"
VIDEO_PATH = OUTPUT_DIR / "neuraldev-facebook-portfolio-promo.mp4"
COVER_PATH = OUTPUT_DIR / "neuraldev-facebook-portfolio-cover.png"
CONCAT_PATH = OUTPUT_DIR / "facebook_promo_concat.txt"

WIDTH = 1080
HEIGHT = 1920
FPS = 30

BG = (9, 15, 23)
PANEL = (17, 24, 39)
PRIMARY = (45, 212, 191)
SECONDARY = (96, 165, 250)
ACCENT = (250, 204, 21)
TEXT = (248, 250, 252)
MUTED = (148, 163, 184)


SLIDES = [
    {
        "duration": 2,
        "title": "Need a custom digital solution?",
        "subtitle": "NeuralDev Portfolio",
        "label": "Gerlan B. Dorona",
        "image": "jobhub-job-posting-application-system.png",
    },
    {
        "duration": 3,
        "title": "Web systems. Mobile apps. AI tools.",
        "subtitle": "Practical builds for real-world workflows",
        "label": "Portfolio Showcase",
        "image": "web-based-mobile-fleet-monitoring-system.png",
    },
    {
        "duration": 3,
        "title": "Workflow and LGU systems",
        "subtitle": "Job applications, citizen reports, scholarship processing, planning dashboards",
        "label": "Public Service + Operations",
        "image": "citizen-reporting-lgu-service-management-platform.png",
    },
    {
        "duration": 3,
        "title": "Inventory, delivery, and POS dashboards",
        "subtitle": "QR tracking, dispatch monitoring, reservations, stock counts, and reports",
        "label": "Business Management",
        "image": "smart-supply-management-qr-ai-forecasting.png",
    },
    {
        "duration": 4,
        "title": "AI detection and smart automation",
        "subtitle": "Plant analysis, helmet detection, fire/smoke monitoring, and AI matching",
        "label": "AI Applications",
        "image": "motorcycle-helmet-rider-detection-system.png",
    },
    {
        "duration": 3,
        "title": "Mobile, tracking, and local-first apps",
        "subtitle": "Android voting, marathon tracking, offline POS, and field-ready workflows",
        "label": "Mobile + Tracking",
        "image": "android-voting-application.png",
    },
    {
        "duration": 4,
        "title": "Let us build your next system.",
        "subtitle": "Websites, dashboards, management systems, mobile apps, and AI-assisted tools",
        "label": "Message NeuralDev today",
        "image": "mpdo-integrated-planning-project-management-system.png",
    },
]


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


FONT_HERO = load_font(74, bold=True)
FONT_TITLE = load_font(58, bold=True)
FONT_SUBTITLE = load_font(34)
FONT_LABEL = load_font(28, bold=True)
FONT_SMALL = load_font(24)


def rounded_rectangle_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def draw_wrapped_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    position: tuple[int, int],
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    max_width: int,
    line_gap: int = 10,
) -> int:
    words = text.split()
    lines: list[str] = []
    current = ""

    for word in words:
        test = f"{current} {word}".strip()
        width = draw.textbbox((0, 0), test, font=font)[2]
        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    x, y = position
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y = bbox[3] + line_gap
    return y


def create_gradient_background() -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    pixels = image.load()
    for y in range(HEIGHT):
        blend = y / HEIGHT
        for x in range(WIDTH):
            side = abs((x / WIDTH) - 0.5) * 2
            teal = int(30 * (1 - blend) * (1 - side * 0.55))
            blue = int(42 * blend * (1 - side * 0.4))
            pixels[x, y] = (
                min(255, BG[0] + int(teal * 0.3)),
                min(255, BG[1] + int(teal * 0.8)),
                min(255, BG[2] + blue),
            )
    return image


def paste_project_image(canvas: Image.Image, image_name: str) -> None:
    source = Image.open(PROJECT_DIR / image_name).convert("RGB")
    target_w = 920
    target_h = 900
    fitted = ImageOpsFit(source, (target_w, target_h))

    shadow = Image.new("RGBA", (target_w + 48, target_h + 48), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((24, 24, target_w + 24, target_h + 24), radius=42, fill=(0, 0, 0, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.paste(shadow, (56, 620), shadow)

    image_rgba = fitted.convert("RGBA")
    mask = rounded_rectangle_mask((target_w, target_h), 40)
    frame = Image.new("RGBA", (target_w + 18, target_h + 18), PANEL + (255,))
    frame_mask = rounded_rectangle_mask(frame.size, 46)
    canvas.paste(frame, (81, 645), frame_mask)
    canvas.paste(image_rgba, (90, 654), mask)


def ImageOpsFit(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    src_w, src_h = source.size
    target_w, target_h = size
    scale = max(target_w / src_w, target_h / src_h)
    resized = source.resize((int(src_w * scale), int(src_h * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def create_slide(slide: dict[str, str | int], index: int) -> Path:
    canvas = create_gradient_background().convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle((70, 82, 1010, 174), radius=34, fill=(15, 23, 42, 220), outline=(45, 212, 191, 130), width=2)
    draw.text((108, 109), str(slide["label"]).upper(), font=FONT_LABEL, fill=PRIMARY)
    draw.text((804, 112), "NEURALDEV", font=FONT_SMALL, fill=MUTED)

    title_font = FONT_HERO if index in (0, len(SLIDES) - 1) else FONT_TITLE
    y = draw_wrapped_text(draw, str(slide["title"]), (80, 250), title_font, TEXT, 920, 14)
    draw_wrapped_text(draw, str(slide["subtitle"]), (82, y + 26), FONT_SUBTITLE, MUTED, 890, 12)

    paste_project_image(canvas, str(slide["image"]))

    draw.rounded_rectangle((80, 1632, 1000, 1768), radius=36, fill=(15, 23, 42, 235), outline=(96, 165, 250, 115), width=2)
    draw.text((122, 1668), "Visit my portfolio", font=FONT_LABEL, fill=TEXT)
    draw.text((122, 1710), "Message me for custom websites, systems, apps, and AI tools.", font=FONT_SMALL, fill=MUTED)
    draw.ellipse((902, 1674, 938, 1710), fill=ACCENT)
    draw.ellipse((944, 1674, 980, 1710), fill=PRIMARY)

    output = FRAME_DIR / f"slide_{index:02}.png"
    canvas.convert("RGB").save(output, quality=95)
    return output


def write_concat_file(frames: list[Path]) -> None:
    lines: list[str] = []
    for frame, slide in zip(frames, SLIDES, strict=True):
        lines.append(f"file '{frame.as_posix()}'")
        lines.append(f"duration {slide['duration']}")
    lines.append(f"file '{frames[-1].as_posix()}'")
    CONCAT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_video() -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(CONCAT_PATH),
        "-vf",
        f"fps={FPS},format=yuv420p",
        "-movflags",
        "+faststart",
        str(VIDEO_PATH),
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FRAME_DIR.mkdir(parents=True, exist_ok=True)

    frames = [create_slide(slide, index) for index, slide in enumerate(SLIDES)]
    frames[0].replace(COVER_PATH)
    frames[0] = COVER_PATH
    write_concat_file(frames)
    render_video()

    print(f"Created {VIDEO_PATH}")
    print(f"Created {COVER_PATH}")


if __name__ == "__main__":
    main()
