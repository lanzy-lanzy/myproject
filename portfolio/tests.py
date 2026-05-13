from pathlib import Path
import re

from django.conf import settings
from django.test import SimpleTestCase


class BrandAndParticleRegressionTests(SimpleTestCase):
    def _home_template(self):
        return (
            Path(settings.BASE_DIR)
            / "portfolio"
            / "templates"
            / "portfolio"
            / "home.html"
        ).read_text(encoding="utf-8")

    def test_logo_wordmark_has_theme_independent_contrast_outline(self):
        logo = (
            Path(settings.BASE_DIR)
            / "portfolio"
            / "static"
            / "portfolio"
            / "img"
            / "neuraldev_logo.svg"
        ).read_text(encoding="utf-8")

        self.assertIn('paint-order="stroke fill"', logo)
        self.assertIn('stroke="#0B1220"', logo)

    def test_particle_canvas_is_not_painted_behind_page_background(self):
        css = (Path(settings.BASE_DIR) / "static_src" / "input.css").read_text(
            encoding="utf-8"
        )

        canvas_block = re.search(
            r"\.neural-particle-canvas\s*\{(?P<body>.*?)\n  \}",
            css,
            flags=re.DOTALL,
        )

        self.assertIsNotNone(canvas_block)
        self.assertIn("z-index: 0;", canvas_block.group("body"))

    def test_particle_trail_uses_responsive_pointer_and_bounded_connection_work(self):
        template = self._home_template()

        pointer_ease = re.search(r"pointerEase:\s*(?P<value>[\d.]+)", template)
        max_particles = re.search(r"maxParticles:\s*(?P<value>\d+)", template)
        connection_checks = re.search(
            r"maxConnectionChecks:\s*(?P<value>\d+)", template
        )

        self.assertIsNotNone(pointer_ease)
        self.assertIsNotNone(max_particles)
        self.assertIsNotNone(connection_checks)
        self.assertGreaterEqual(float(pointer_ease.group("value")), 0.65)
        self.assertLessEqual(int(max_particles.group("value")), 260)
        self.assertLessEqual(int(connection_checks.group("value")), 1000)
        self.assertIn("maxConnectionChecks", template)
