from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1280
HEIGHT = 720
SCALE = 2
CANVAS = (WIDTH * SCALE, HEIGHT * SCALE)
OUT_DIR = Path(__file__).resolve().parents[1] / "media" / "projects"


PALETTES = [
    ("#07111d", "#19e6ff", "#8b5cf6", "#34d399"),
    ("#080d1f", "#22d3ee", "#a78bfa", "#bef264"),
    ("#050816", "#06b6d4", "#f472b6", "#10b981"),
    ("#0a1023", "#38bdf8", "#c084fc", "#4ade80"),
    ("#071a24", "#2dd4bf", "#818cf8", "#f0abfc"),
]


@dataclass(frozen=True)
class ProjectSpec:
    slug: str
    title: str
    label: str
    mode: str
    palette: int
    metrics: tuple[str, str, str]


PROJECTS = [
    ProjectSpec("jobhub-job-posting-application-system", "JobHub", "Hiring Pipeline", "jobs", 0, ("128", "42", "9")),
    ProjectSpec("web-based-mobile-fleet-monitoring-system", "Mobile Fleet Monitor", "QR Transport Ops", "fleet", 1, ("18", "642", "96%")),
    ProjectSpec("municipal-supply-resource-request-management-system", "Municipal Supply Requests", "LGU Inventory", "supply", 2, ("84", "31", "12")),
    ProjectSpec("mpdo-integrated-planning-project-management-system", "MPDO Project Planning", "Municipal Projects", "planning", 3, ("24", "8.6M", "61%")),
    ProjectSpec("smart-supply-management-qr-ai-forecasting", "Smart Supply AI", "QR Forecasting", "forecast", 4, ("92%", "14", "7d")),
    ProjectSpec("scholarship-management-information-system", "Scholarship MIS", "Student Approvals", "scholarship", 0, ("1.2K", "318", "76%")),
    ProjectSpec("prycegas-lpg-order-delivery-management-system", "Prycegas LPG Delivery", "Cylinder Logistics", "lpg", 1, ("56", "22", "98%")),
    ProjectSpec("lumber-management-system", "Lumber Management", "Board-Foot Inventory", "lumber", 2, ("9.4K", "38", "21%")),
    ProjectSpec("tailoring-management-system", "Tailoring Management", "Orders & Commission", "tailoring", 3, ("73", "19", "42K")),
    ProjectSpec("restobar-reservation-inventory-system", "Restobar Operations", "Tables & Stock", "restobar", 4, ("18", "34", "6")),
    ProjectSpec("sangguniang-bayan-ordinance-management-system", "Ordinance Records", "Council Archive", "ordinance", 0, ("412", "28", "0.8s")),
    ProjectSpec("lost-and-found-management-system-ai-matching", "Lost & Found AI", "Similarity Matching", "lostfound", 1, ("93%", "47", "12")),
    ProjectSpec("android-voting-application", "Android Voting App", "Secure Ballot", "voting", 2, ("8.7K", "12", "100%")),
    ProjectSpec("corn-leaf-nutrient-deficiency-analysis-app", "Corn Leaf Analysis", "NPK Diagnosis", "corn", 3, ("N", "P", "K")),
    ProjectSpec("tomato-leaf-disease-detection-app", "Tomato Disease Detection", "Plant Vision AI", "tomato", 4, ("91%", "4", "2")),
    ProjectSpec("offline-pos-inventory-management-system", "Offline POS Inventory", "Local Sales System", "pos", 0, ("248", "18K", "LOCAL")),
    ProjectSpec("marathon-tracking-trail-visualization-system", "Marathon Trail Tracker", "GPS Race Control", "marathon", 1, ("42.2", "5:18", "214")),
    ProjectSpec("motorcycle-helmet-rider-detection-system", "Helmet Rider Detection", "Traffic Vision", "helmet", 2, ("17", "4", "98%")),
    ProjectSpec("fire-smoke-detection-system", "Fire & Smoke Detection", "Hazard Monitor", "hazard", 3, ("HIGH", "82%", "03")),
    ProjectSpec("citizen-reporting-lgu-service-management-platform", "Citizen Reporting Platform", "LGU Response Desk", "citizen", 4, ("126", "41", "88%")),
]


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip("#")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def rgba(value: str, alpha: int) -> tuple[int, int, int, int]:
    return (*hex_to_rgb(value), alpha)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    size *= SCALE
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def scaled_box(box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(coord * SCALE for coord in box)


def text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], label: str, fill, size: int, bold: bool = False, anchor=None) -> None:
    draw.text((xy[0] * SCALE, xy[1] * SCALE), label, font=font(size, bold), fill=fill, anchor=anchor)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int, fill, outline=None, width: int = 1) -> None:
    draw.rounded_rectangle(scaled_box(box), radius=radius * SCALE, fill=fill, outline=outline, width=width * SCALE)


def line(draw: ImageDraw.ImageDraw, pts, fill, width: int = 1) -> None:
    draw.line([(x * SCALE, y * SCALE) for x, y in pts], fill=fill, width=width * SCALE, joint="curve")


def ellipse(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill=None, outline=None, width: int = 1) -> None:
    draw.ellipse(scaled_box(box), fill=fill, outline=outline, width=width * SCALE)


def background(base: str, primary: str, secondary: str, accent: str, seed: int) -> Image.Image:
    random.seed(seed)
    image = Image.new("RGBA", CANVAS, rgba(base, 255))
    pixels = image.load()
    br, bg, bb = hex_to_rgb(base)
    for y in range(CANVAS[1]):
        for x in range(CANVAS[0]):
            vx = x / CANVAS[0]
            vy = y / CANVAS[1]
            glow = int(22 * vx + 18 * (1 - vy))
            pixels[x, y] = (min(255, br + glow), min(255, bg + glow // 2), min(255, bb + glow), 255)

    overlay = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for step in range(0, WIDTH, 48):
        line(draw, [(step, 0), (step + 220, HEIGHT)], rgba("#ffffff", 13), 1)
    for step in range(0, HEIGHT, 48):
        line(draw, [(0, step), (WIDTH, step - 120)], rgba("#ffffff", 10), 1)

    for cx, cy, color, radius in [
        (180, 80, primary, 260),
        (1130, 90, secondary, 300),
        (810, 650, accent, 260),
    ]:
        ellipse(draw, (cx - radius, cy - radius, cx + radius, cy + radius), fill=rgba(color, 36))
    overlay = overlay.filter(ImageFilter.GaussianBlur(24 * SCALE))
    image.alpha_composite(overlay)

    draw = ImageDraw.Draw(image)
    for _ in range(80):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        draw.point((x * SCALE, y * SCALE), fill=rgba("#ffffff", random.randint(18, 55)))
    return image


def panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], primary: str, alpha: int = 74) -> None:
    rounded(draw, box, 18, rgba("#07111d", alpha), rgba("#ffffff", 38), 1)
    x1, y1, x2, y2 = box
    line(draw, [(x1 + 16, y1 + 1), (x2 - 16, y1 + 1)], rgba(primary, 96), 1)


def metric(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: str, label: str, color: str) -> None:
    panel(draw, box, color, 90)
    text(draw, (box[0] + 18, box[1] + 16), value, rgba(color, 255), 25, True)
    text(draw, (box[0] + 18, box[1] + 47), label.upper(), rgba("#dbeafe", 142), 10, True)


def bars(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], colors: tuple[str, str, str], seed: int) -> None:
    random.seed(seed)
    x1, y1, x2, y2 = box
    panel(draw, box, colors[0], 68)
    text(draw, (x1 + 18, y1 + 16), "ACTIVITY", rgba("#e5f9ff", 190), 11, True)
    count = 10
    gap = 9
    bw = (x2 - x1 - 45 - gap * (count - 1)) // count
    for i in range(count):
        h = random.randint(24, y2 - y1 - 70)
        x = x1 + 22 + i * (bw + gap)
        y = y2 - 22 - h
        rounded(draw, (x, y, x + bw, y2 - 22), 5, rgba(colors[i % 3], 135), None)


def trend(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], colors: tuple[str, str, str], seed: int) -> None:
    random.seed(seed)
    x1, y1, x2, y2 = box
    panel(draw, box, colors[1], 68)
    text(draw, (x1 + 18, y1 + 16), "FORECAST", rgba("#e5f9ff", 190), 11, True)
    points = []
    for i in range(9):
        x = x1 + 28 + i * ((x2 - x1 - 56) / 8)
        y = y2 - 34 - (math.sin(i * 0.7 + seed) * 22 + i * 6 + random.randint(-8, 8) + 34)
        points.append((int(x), int(y)))
    for width, alpha in [(9, 34), (5, 72), (2, 230)]:
        line(draw, points, rgba(colors[1], alpha), width)
    for x, y in points:
        ellipse(draw, (x - 5, y - 5, x + 5, y + 5), fill=rgba(colors[2], 255))


def qr(draw: ImageDraw.ImageDraw, x: int, y: int, size: int, color: str, seed: int) -> None:
    random.seed(seed)
    cell = size // 9
    rounded(draw, (x - 10, y - 10, x + size + 10, y + size + 10), 14, rgba("#07111d", 130), rgba(color, 100))
    for row in range(9):
        for col in range(9):
            edge = (row in (0, 1, 7, 8) and col in (0, 1, 7, 8))
            if edge or random.random() > 0.48:
                rounded(draw, (x + col * cell, y + row * cell, x + col * cell + cell - 3, y + row * cell + cell - 3), 2, rgba(color, 180))


def map_route(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], colors: tuple[str, str, str], seed: int) -> None:
    random.seed(seed)
    x1, y1, x2, y2 = box
    panel(draw, box, colors[0], 66)
    for gx in range(x1 + 26, x2, 52):
        line(draw, [(gx, y1 + 22), (gx - 40, y2 - 20)], rgba("#ffffff", 13))
    for gy in range(y1 + 32, y2, 48):
        line(draw, [(x1 + 20, gy), (x2 - 20, gy - 24)], rgba("#ffffff", 12))
    pts = [(x1 + 45, y2 - 45), (x1 + 135, y1 + 105), (x1 + 240, y1 + 170), (x2 - 120, y1 + 70), (x2 - 45, y2 - 58)]
    for width, alpha in [(13, 32), (7, 90), (3, 235)]:
        line(draw, pts, rgba(colors[0], alpha), width)
    for index, (x, y) in enumerate(pts):
        ellipse(draw, (x - 9, y - 9, x + 9, y + 9), fill=rgba(colors[index % 3], 245))
        ellipse(draw, (x - 22, y - 22, x + 22, y + 22), outline=rgba(colors[index % 3], 86), width=2)


def document_stack(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str) -> None:
    x1, y1, x2, y2 = box
    panel(draw, box, color, 72)
    for i in range(5):
        yy = y1 + 32 + i * 42
        rounded(draw, (x1 + 24, yy, x2 - 24, yy + 28), 8, rgba("#ffffff", 20 + i * 4), rgba("#ffffff", 34))
        rounded(draw, (x1 + 38, yy + 9, x1 + 128, yy + 15), 4, rgba(color, 160))
        rounded(draw, (x2 - 86, yy + 8, x2 - 38, yy + 16), 4, rgba("#34d399", 120))


def kanban(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], colors: tuple[str, str, str], labels: tuple[str, str, str]) -> None:
    x1, y1, x2, y2 = box
    panel(draw, box, colors[0], 66)
    col_w = (x2 - x1 - 58) // 3
    for col in range(3):
        cx = x1 + 22 + col * (col_w + 7)
        text(draw, (cx, y1 + 18), labels[col].upper(), rgba("#e5f9ff", 142), 10, True)
        for row in range(3):
            yy = y1 + 45 + row * 53
            rounded(draw, (cx, yy, cx + col_w, yy + 38), 8, rgba("#ffffff", 22), rgba("#ffffff", 34))
            rounded(draw, (cx + 12, yy + 10, cx + col_w - 32, yy + 15), 3, rgba(colors[(col + row) % 3], 145))
            rounded(draw, (cx + 12, yy + 24, cx + 72, yy + 29), 3, rgba("#ffffff", 48))


def mobile_device(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str, label: str) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, 32, rgba("#030712", 190), rgba(color, 150), 2)
    rounded(draw, (x1 + 18, y1 + 26, x2 - 18, y2 - 28), 22, rgba("#0f172a", 230), rgba("#ffffff", 30))
    text(draw, (x1 + 36, y1 + 52), label, rgba(color, 230), 13, True)
    for i in range(3):
        rounded(draw, (x1 + 36, y1 + 90 + i * 54, x2 - 36, y1 + 126 + i * 54), 12, rgba("#ffffff", 21), rgba("#ffffff", 32))


def leaf_scan(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], colors: tuple[str, str, str], tomato: bool = False) -> None:
    x1, y1, x2, y2 = box
    panel(draw, box, colors[0], 66)
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    leaf_color = "#ef4444" if tomato else "#84cc16"
    for angle in range(-70, 80, 35):
        rx = int(math.cos(math.radians(angle)) * 75)
        ry = int(math.sin(math.radians(angle)) * 36)
        ellipse(draw, (cx - 78 + rx // 3, cy - 35 + ry // 3, cx + 78 + rx // 3, cy + 35 + ry // 3), fill=rgba(leaf_color, 52), outline=rgba(colors[2], 110), width=2)
    line(draw, [(cx - 110, cy + 58), (cx + 112, cy - 58)], rgba(colors[1], 190), 3)
    for rect in [(cx - 112, cy - 64, cx - 18, cy + 4), (cx + 12, cy - 20, cx + 122, cy + 62)]:
        rounded(draw, rect, 8, None, rgba("#f8fafc", 190), 2)


def cylinders(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], colors: tuple[str, str, str]) -> None:
    x1, y1, x2, y2 = box
    panel(draw, box, colors[0], 66)
    for i in range(4):
        x = x1 + 42 + i * 78
        y = y1 + 80 + (i % 2) * 24
        ellipse(draw, (x, y, x + 48, y + 18), fill=rgba(colors[i % 3], 130), outline=rgba("#ffffff", 50))
        rounded(draw, (x, y + 9, x + 48, y + 112), 12, rgba("#ffffff", 22), rgba(colors[i % 3], 130))
        ellipse(draw, (x, y + 101, x + 48, y + 121), fill=rgba("#020617", 130), outline=rgba(colors[i % 3], 90))


def lumber(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], colors: tuple[str, str, str]) -> None:
    x1, y1, x2, y2 = box
    panel(draw, box, colors[0], 66)
    for i in range(7):
        y = y2 - 42 - i * 22
        rounded(draw, (x1 + 58 + i * 7, y, x2 - 64 + i * 7, y + 16), 5, rgba("#c084fc" if i % 2 else "#22d3ee", 76), rgba("#ffffff", 34))
    rounded(draw, (x1 + 42, y1 + 38, x1 + 160, y1 + 95), 12, rgba("#ffffff", 22), rgba(colors[2], 110))
    text(draw, (x1 + 60, y1 + 57), "BF", rgba(colors[2], 230), 20, True)


def table_map(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], colors: tuple[str, str, str]) -> None:
    x1, y1, x2, y2 = box
    panel(draw, box, colors[0], 66)
    for row in range(2):
        for col in range(4):
            cx = x1 + 58 + col * 76
            cy = y1 + 68 + row * 88
            fill = colors[(row + col) % 3]
            ellipse(draw, (cx - 24, cy - 24, cx + 24, cy + 24), fill=rgba(fill, 70), outline=rgba(fill, 175), width=2)
            rounded(draw, (cx - 10, cy - 36, cx + 10, cy - 28), 3, rgba("#ffffff", 32))
            rounded(draw, (cx - 10, cy + 28, cx + 10, cy + 36), 3, rgba("#ffffff", 32))


def vision_feed(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], colors: tuple[str, str, str], mode: str) -> None:
    x1, y1, x2, y2 = box
    panel(draw, box, colors[0], 66)
    text(draw, (x1 + 22, y1 + 18), "LIVE VISION", rgba("#e5f9ff", 160), 11, True)
    for i, rect in enumerate([(x1 + 56, y1 + 72, x1 + 180, y1 + 170), (x1 + 218, y1 + 64, x1 + 346, y1 + 182)]):
        rounded(draw, rect, 10, rgba("#ffffff", 12), rgba(colors[i % 3], 220), 3)
        if mode == "hazard":
            ellipse(draw, (rect[0] + 34, rect[1] + 22, rect[2] - 34, rect[3] - 20), fill=rgba("#f97316", 58), outline=rgba("#f87171", 230), width=2)
        else:
            ellipse(draw, (rect[0] + 36, rect[1] + 14, rect[0] + 86, rect[1] + 64), fill=rgba(colors[2], 90), outline=rgba(colors[2], 180), width=2)
            rounded(draw, (rect[0] + 22, rect[1] + 72, rect[2] - 22, rect[3] - 12), 16, rgba("#ffffff", 16), rgba(colors[0], 150))


def central_visual(draw: ImageDraw.ImageDraw, spec: ProjectSpec, box: tuple[int, int, int, int], colors: tuple[str, str, str]) -> None:
    mode = spec.mode
    if mode in {"fleet", "planning", "marathon", "citizen"}:
        map_route(draw, box, colors, len(spec.slug))
    elif mode in {"jobs", "scholarship", "supply"}:
        labels = ("Queue", "Review", "Approved") if mode != "jobs" else ("Applied", "Interview", "Hired")
        kanban(draw, box, colors, labels)
    elif mode in {"forecast", "pos"}:
        trend(draw, box, colors, len(spec.title))
    elif mode == "lpg":
        cylinders(draw, box, colors)
    elif mode == "lumber":
        lumber(draw, box, colors)
    elif mode == "tailoring":
        kanban(draw, box, colors, ("Cut", "Sew", "Done"))
    elif mode == "restobar":
        table_map(draw, box, colors)
    elif mode == "ordinance":
        document_stack(draw, box, colors[0])
    elif mode == "lostfound":
        vision_feed(draw, box, colors, "match")
    elif mode == "voting":
        mobile_device(draw, (box[0] + 110, box[1] + 20, box[0] + 295, box[3] - 18), colors[1], "BALLOT")
    elif mode in {"corn", "tomato"}:
        leaf_scan(draw, box, colors, tomato=mode == "tomato")
    elif mode in {"helmet", "hazard"}:
        vision_feed(draw, box, colors, mode)
    else:
        bars(draw, box, colors, len(spec.slug))


def render(spec: ProjectSpec, index: int) -> Image.Image:
    base, primary, secondary, accent = PALETTES[spec.palette]
    colors = (primary, secondary, accent)
    image = background(base, primary, secondary, accent, index * 41)
    draw = ImageDraw.Draw(image)

    rounded(draw, (56, 52, 1224, 668), 28, rgba("#030712", 44), rgba("#ffffff", 30), 1)
    rounded(draw, (82, 82, 392, 156), 22, rgba("#07111d", 112), rgba(primary, 92), 1)
    text(draw, (106, 101), spec.title, rgba("#f8fafc", 238), 21, True)
    text(draw, (107, 132), spec.label.upper(), rgba(primary, 210), 10, True)

    metric(draw, (86, 190, 214, 270), spec.metrics[0], "Active", primary)
    metric(draw, (232, 190, 360, 270), spec.metrics[1], "Pending", secondary)
    metric(draw, (378, 190, 506, 270), spec.metrics[2], "Signal", accent)

    central_visual(draw, spec, (548, 116, 1178, 438), colors)
    bars(draw, (84, 306, 506, 530), colors, index + 8)
    trend(draw, (548, 466, 866, 620), colors, index + 16)
    qr(draw, 930, 486, 92, accent, index + 12)

    panel(draw, (1040, 466, 1178, 620), primary, 76)
    text(draw, (1062, 486), "STATUS", rgba("#dbeafe", 150), 10, True)
    rounded(draw, (1062, 515, 1152, 540), 12, rgba(accent, 95), rgba(accent, 150))
    text(draw, (1076, 521), "ONLINE", rgba("#f8fafc", 220), 11, True)
    for i in range(3):
        rounded(draw, (1062, 558 + i * 16, 1158 - i * 18, 564 + i * 16), 3, rgba(colors[i], 130))

    for cx, cy, color in [(464, 116, primary), (1180, 124, secondary), (506, 610, accent)]:
        ellipse(draw, (cx - 4, cy - 4, cx + 4, cy + 4), fill=rgba(color, 255))
        ellipse(draw, (cx - 16, cy - 16, cx + 16, cy + 16), outline=rgba(color, 70), width=1)

    return image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGB")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for index, spec in enumerate(PROJECTS, start=1):
        image = render(spec, index)
        path = OUT_DIR / f"{spec.slug}.png"
        image.save(path, "PNG", optimize=True)
        print(path)


if __name__ == "__main__":
    main()
