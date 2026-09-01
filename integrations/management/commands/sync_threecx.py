import logging

from django.core.management.base import BaseCommand, CommandError

from integrations.sync import sync_threecx_users

logger = logging.getLogger("integrations.sync")


class Command(BaseCommand):
    """
    Pulls users from the 3CX XAPI and upserts them into PostgreSQL.

    Designed to be run non-interactively on a schedule (cron / systemd timer /
    Celery beat / Kubernetes CronJob):

        python manage.py sync_threecx

    Exits non-zero on failure so the scheduler/monitoring can detect and
    alert on a broken sync (e.g. expired 3CX API credentials).
    """

    help = "Sync users from the 3CX XAPI into PostgreSQL (ThreeCXUser)."

    def handle(self, *args, **options):
        self.stdout.write("Syncing users from 3CX...")

        try:
            result = sync_threecx_users()
        except Exception as exc:
            logger.exception("3CX sync failed")
            raise CommandError(f"3CX sync failed: {exc}") from exc

        logger.info(
            "3CX sync complete: %(total)s total, %(created)s created, %(updated)s updated",
            result,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. total={result['total']} "
                f"created={result['created']} updated={result['updated']}"
            )
        )
