from django.core.management.base import BaseCommand
from django.utils.text import slugify

from portfolio.models import Project


PROJECTS = [
    {
        "title": "JobHub - Job Posting & Application System",
        "short": "A hiring workflow platform for job posts, applicant screening, interview tracking, and application status management.",
        "tech": ["Django", "HTMX", "Tailwind", "SQLite"],
        "status": "completed",
        "image": "projects/jobhub-job-posting-application-system.png",
    },
    {
        "title": "Web-Based Mobile Fleet Monitoring System",
        "short": "A QR-based transport operations dashboard for route monitoring, terminal activity, passenger counts, and trip status.",
        "tech": ["Django", "QR Tracking", "Maps", "Analytics"],
        "status": "completed",
        "image": "projects/web-based-mobile-fleet-monitoring-system.png",
    },
    {
        "title": "Municipal Supply and Resource Request Management System",
        "short": "An LGU supply request platform for inventory cards, approval workflows, QR tracking, and reporting.",
        "tech": ["Django", "Inventory", "QR Codes", "Reports"],
        "status": "completed",
        "image": "projects/municipal-supply-resource-request-management-system.png",
    },
    {
        "title": "MPDO Integrated Planning and Project Management System",
        "short": "A municipal planning workspace for project timelines, budgets, barangay mapping, and GIS-linked project monitoring.",
        "tech": ["Django", "GIS", "Planning", "Dashboards"],
        "status": "completed",
        "image": "projects/mpdo-integrated-planning-project-management-system.png",
    },
    {
        "title": "Smart Supply Management System with QR-Based Tracking and AI Forecasting",
        "short": "An AI-assisted inventory dashboard for QR supply tracking, stock prediction, forecast charts, and supply analytics.",
        "tech": ["Django", "AI Forecasting", "QR Codes", "Analytics"],
        "status": "completed",
        "image": "projects/smart-supply-management-qr-ai-forecasting.png",
    },
    {
        "title": "Scholarship Management Information System",
        "short": "A scholarship processing system for student applications, document validation, claim cards, and approval workflows.",
        "tech": ["Django", "Workflow", "Documents", "QR Claims"],
        "status": "completed",
        "image": "projects/scholarship-management-information-system.png",
    },
    {
        "title": "Prycegas LPG Order and Delivery Management System",
        "short": "An LPG order and delivery dashboard for cylinder inventory, route tracking, payment status, and dispatch monitoring.",
        "tech": ["Django", "Delivery", "Inventory", "Payments"],
        "status": "completed",
        "image": "projects/prycegas-lpg-order-delivery-management-system.png",
    },
    {
        "title": "Lumber Management System",
        "short": "A lumber business platform for board-foot calculations, stock monitoring, supplier orders, and sales analytics.",
        "tech": ["Django", "Inventory", "Sales", "Calculators"],
        "status": "completed",
        "image": "projects/lumber-management-system.png",
    },
    {
        "title": "Tailoring Management System",
        "short": "A tailoring operations dashboard for garment orders, fabric inventory, task cards, and tailor commission tracking.",
        "tech": ["Django", "Orders", "Inventory", "Commissions"],
        "status": "completed",
        "image": "projects/tailoring-management-system.png",
    },
    {
        "title": "Restobar Reservation and Inventory System",
        "short": "A restaurant operations system for table reservations, order queues, walk-ins, stock counts, and inventory alerts.",
        "tech": ["Django", "Reservations", "POS", "Inventory"],
        "status": "completed",
        "image": "projects/restobar-reservation-inventory-system.png",
    },
    {
        "title": "Sangguniang Bayan Ordinance Management System",
        "short": "A searchable public records dashboard for ordinance archives, document cards, council records, and retrieval workflows.",
        "tech": ["Django", "Search", "Documents", "Records"],
        "status": "completed",
        "image": "projects/sangguniang-bayan-ordinance-management-system.png",
    },
    {
        "title": "Lost and Found Management System with AI Matching",
        "short": "An AI matching platform for found item records, similarity scoring, item scan review, and verification workflows.",
        "tech": ["Django", "AI Matching", "Computer Vision", "Workflow"],
        "status": "completed",
        "image": "projects/lost-and-found-management-system-ai-matching.png",
    },
    {
        "title": "Android Voting Application",
        "short": "A secure mobile voting concept with biometric login, candidate screens, vote counters, and protected ballot flow.",
        "tech": ["Android", "Mobile UI", "Biometrics", "Security"],
        "status": "completed",
        "image": "projects/android-voting-application.png",
    },
    {
        "title": "Corn Leaf Nutrient Deficiency Analysis App",
        "short": "An AI crop analysis app for corn leaf scanning, NPK indicators, deficiency probability, and treatment suggestions.",
        "tech": ["AI", "Computer Vision", "Mobile", "Agriculture"],
        "status": "completed",
        "image": "projects/corn-leaf-nutrient-deficiency-analysis-app.png",
    },
    {
        "title": "Tomato Leaf Disease Detection App",
        "short": "A plant disease detection interface with tomato leaf bounding boxes, disease labels, and model confidence scores.",
        "tech": ["AI", "Computer Vision", "Mobile", "Agriculture"],
        "status": "completed",
        "image": "projects/tomato-leaf-disease-detection-app.png",
    },
    {
        "title": "Offline POS and Inventory Management System",
        "short": "A local-first POS dashboard with product grids, receipt preview, sales reporting, inventory counts, and offline database status.",
        "tech": ["POS", "SQLite", "Inventory", "Sales"],
        "status": "completed",
        "image": "projects/offline-pos-inventory-management-system.png",
    },
    {
        "title": "Marathon Tracking and Trail Visualization System",
        "short": "A GPS race monitoring platform for route maps, runner markers, distance stats, pace analytics, and leaderboards.",
        "tech": ["GPS", "Maps", "Analytics", "Tracking"],
        "status": "completed",
        "image": "projects/marathon-tracking-trail-visualization-system.png",
    },
    {
        "title": "Motorcycle Helmet & Rider Detection System",
        "short": "A traffic computer vision dashboard for helmet detection, rider counting, plate zones, and violation alerts.",
        "tech": ["Computer Vision", "Detection", "Traffic", "AI"],
        "status": "completed",
        "image": "projects/motorcycle-helmet-rider-detection-system.png",
    },
    {
        "title": "Fire and Smoke Detection System",
        "short": "A real-time hazard monitoring system with camera feeds, fire and smoke detection boxes, alerts, and risk meters.",
        "tech": ["Computer Vision", "Alerts", "Monitoring", "AI"],
        "status": "completed",
        "image": "projects/fire-smoke-detection-system.png",
    },
    {
        "title": "Citizen Reporting and LGU Service Management Platform",
        "short": "A civic service dashboard for citizen reports, complaint cards, incident mapping, status tracking, and LGU responses.",
        "tech": ["Django", "Civic Tech", "Maps", "Workflow"],
        "status": "completed",
        "image": "projects/citizen-reporting-lgu-service-management-platform.png",
    },
]


class Command(BaseCommand):
    help = "Seed the portfolio with real project records and showcase images."

    def handle(self, *args, **options):
        active_slugs = []

        for index, project in enumerate(PROJECTS, start=1):
            slug = slugify(project["title"])
            active_slugs.append(slug)

            Project.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": project["title"],
                    "short_description": project["short"],
                    "description": project["short"],
                    "tech_stack": project["tech"],
                    "status": project["status"],
                    "image": project["image"],
                    "live_url": "",
                    "repo_url": "",
                    "order": index,
                    "is_featured": True,
                },
            )

        removed, _ = Project.objects.exclude(slug__in=active_slugs).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(PROJECTS)} projects and removed {removed} old project records."
            )
        )
