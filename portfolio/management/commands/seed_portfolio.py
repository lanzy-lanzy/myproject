from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from portfolio.models import Project


PROJECTS = [
    {
        "title": "Neural Ops Console",
        "short": "A live operations dashboard for AI-assisted support, alerts, and workflow triage.",
        "tech": ["Django", "HTMX", "Celery", "OpenAI"],
        "status": "maintained",
        "colors": ("#07111d", "#18f0ff", "#b27dff"),
    },
    {
        "title": "Vector Knowledge Hub",
        "short": "A searchable internal knowledge base with embeddings, source trails, and admin controls.",
        "tech": ["Python", "Django", "PostgreSQL", "pgvector"],
        "status": "completed",
        "colors": ("#0a1023", "#8bf7ff", "#7cff9b"),
    },
    {
        "title": "Autonomous QA Lab",
        "short": "A testing cockpit that runs browser journeys, captures failures, and explains regressions.",
        "tech": ["Playwright", "Django", "Redis", "AI"],
        "status": "in_progress",
        "colors": ("#111827", "#f0abfc", "#38bdf8"),
    },
    {
        "title": "Signal CRM",
        "short": "A sales workspace that scores leads, summarizes history, and recommends next actions.",
        "tech": ["Django", "Tailwind", "HTMX", "LLM"],
        "status": "completed",
        "colors": ("#08131f", "#22d3ee", "#a78bfa"),
    },
    {
        "title": "AI Content Studio",
        "short": "A production tool for briefs, drafts, approvals, and brand-safe content generation.",
        "tech": ["Django", "Queues", "S3", "OpenAI"],
        "status": "maintained",
        "colors": ("#120d22", "#c084fc", "#67e8f9"),
    },
    {
        "title": "Inference Cost Monitor",
        "short": "A cost intelligence dashboard for model usage, spend anomalies, and team budgets.",
        "tech": ["Django", "Charts", "PostgreSQL", "APIs"],
        "status": "completed",
        "colors": ("#071a24", "#2dd4bf", "#bef264"),
    },
    {
        "title": "Agent Task Board",
        "short": "A workflow board for human review, tool calls, approvals, and async agent status.",
        "tech": ["Django", "Channels", "HTMX", "Redis"],
        "status": "in_progress",
        "colors": ("#090b1a", "#60a5fa", "#f472b6"),
    },
    {
        "title": "Document Intelligence Portal",
        "short": "A document intake platform that extracts fields, flags risk, and routes reviews.",
        "tech": ["Python", "OCR", "Django", "AI"],
        "status": "completed",
        "colors": ("#0d1325", "#93c5fd", "#34d399"),
    },
    {
        "title": "Realtime Insight Wall",
        "short": "A full-screen analytics wall for product telemetry, incidents, and executive signals.",
        "tech": ["Django", "WebSockets", "Charts", "Postgres"],
        "status": "maintained",
        "colors": ("#050816", "#06b6d4", "#f0abfc"),
    },
    {
        "title": "Prompt Governance Suite",
        "short": "A versioned prompt registry with evals, approvals, rollback, and audit history.",
        "tech": ["Django", "Evals", "SQLite", "OpenAI"],
        "status": "completed",
        "colors": ("#0b1020", "#a3e635", "#22d3ee"),
    },
]


class Command(BaseCommand):
    help = "Seed the portfolio with AI-inspired projects and generated thumbnails."

    def handle(self, *args, **options):
        image_dir = Path(settings.MEDIA_ROOT) / "projects"
        image_dir.mkdir(parents=True, exist_ok=True)

        for index, project in enumerate(PROJECTS, start=1):
            slug = slugify(project["title"])
            filename = f"{slug}.png"
            self.create_project_image(
                image_dir / filename,
                project["title"],
                project["tech"],
                project["colors"],
                index,
            )

            Project.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": project["title"],
                    "short_description": project["short"],
                    "description": project["short"],
                    "tech_stack": project["tech"],
                    "status": project["status"],
                    "image": f"projects/{filename}",
                    "live_url": "",
                    "repo_url": "",
                    "order": index,
                    "is_featured": True,
                },
            )

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(PROJECTS)} projects."))

    def create_project_image(self, path, title, tech_stack, colors, index):
        width, height = 1280, 720
        base, primary, secondary = colors
        image = Image.new("RGB", (width, height), base)
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        draw.ellipse((-240, -220, 620, 520), fill=self.hex_rgba(primary, 92))
        draw.ellipse((640, -180, 1520, 520), fill=self.hex_rgba(secondary, 84))
        draw.ellipse((420, 280, 1320, 980), fill=self.hex_rgba(primary, 48))

        for step in range(0, width, 64):
            draw.line((step, 0, step + 320, height), fill=(255, 255, 255, 16), width=1)
        for step in range(64, height, 64):
            draw.line((0, step, width, step - 180), fill=(255, 255, 255, 10), width=1)

        center = (width // 2 + 130, height // 2)
        for radius, alpha, color in [
            (250, 96, primary),
            (185, 84, secondary),
            (110, 120, primary),
        ]:
            box = (
                center[0] - radius,
                center[1] - radius // 2,
                center[0] + radius,
                center[1] + radius // 2,
            )
            draw.ellipse(box, outline=self.hex_rgba(color, alpha), width=4)

        for node_index, (x, y) in enumerate(
            [(280, 180), (920, 150), (1030, 475), (460, 535), (735, 320)]
        ):
            color = primary if node_index % 2 == 0 else secondary
            draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=self.hex_rgba(color, 255))
            draw.ellipse((x - 34, y - 34, x + 34, y + 34), outline=self.hex_rgba(color, 64), width=2)

        overlay = overlay.filter(ImageFilter.GaussianBlur(0.2))
        image = Image.alpha_composite(image.convert("RGBA"), overlay)
        draw = ImageDraw.Draw(image)

        title_font = self.load_font(58, bold=True)
        meta_font = self.load_font(24, bold=True)
        small_font = self.load_font(22)

        draw.rounded_rectangle((72, 76, 540, 158), radius=24, fill=(7, 12, 28, 168), outline=(255, 255, 255, 36), width=2)
        draw.text((104, 100), f"PROJECT {index:02d}", font=meta_font, fill=self.hex_rgba(primary, 255))

        wrapped = self.wrap_text(title, title_font, 740)
        draw.multiline_text((76, 458), wrapped, font=title_font, fill=(238, 248, 255, 255), spacing=8)
        draw.text((80, 640), " / ".join(tech_stack[:4]), font=small_font, fill=(190, 211, 230, 220))

        image.convert("RGB").save(path, "PNG", optimize=True)

    def load_font(self, size, bold=False):
        candidates = [
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        ]
        for candidate in candidates:
            if Path(candidate).exists():
                return ImageFont.truetype(candidate, size)
        return ImageFont.load_default()

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current = ""
        probe = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(probe)
        for word in words:
            attempt = f"{current} {word}".strip()
            if draw.textlength(attempt, font=font) <= max_width:
                current = attempt
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return "\n".join(lines)

    def hex_rgba(self, value, alpha):
        value = value.lstrip("#")
        return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4)) + (alpha,)
