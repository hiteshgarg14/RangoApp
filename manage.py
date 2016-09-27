#!/usr/bin/env python
import os
import sys

"""
Run 'manage.py makemigrations' to make new migrations, and then re-run 'manage.py migrate' to apply them.
python manage.py sqlmigrate Rango 0001
"""

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RangoApp.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
