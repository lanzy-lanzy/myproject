#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def _project_venv_python():
    scripts_dir = "Scripts" if os.name == "nt" else "bin"
    executable = "python.exe" if os.name == "nt" else "python"
    python_path = Path(__file__).resolve().parent / ".venv" / scripts_dir / executable
    return python_path if python_path.exists() else None


def _running_with_python(python_path):
    try:
        return Path(sys.executable).resolve() == python_path.resolve()
    except OSError:
        return False


def _restart_in_project_venv():
    python_path = _project_venv_python()
    if python_path is None or _running_with_python(python_path):
        return

    os.execv(str(python_path), [str(python_path), *sys.argv])


def main():
    """Run administrative tasks."""
    if sys.version_info < (3, 10):
        raise SystemExit(
            "This project requires Python 3.10 or newer. "
            "Activate .venv or run .\\.venv\\Scripts\\python.exe manage.py <command>."
        )

    _restart_in_project_venv()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
