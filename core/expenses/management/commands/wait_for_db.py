"""
Django command to wait for the database to be available
"""

import time
from typing import Any, Optional

from psycopg2 import OperationalError as Psycopg2opError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to wait for the database"""

    def handle(self, *args: Any, **options: Any) -> str | None:
        """Entrypoint for command"""
        self.stdout.write('Waiting for database')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2opError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database ready"))