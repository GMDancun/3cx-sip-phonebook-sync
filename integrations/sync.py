import logging

from django.utils import timezone

from .models import ThreeCXUser
from .threecx import ThreeCXClient

logger = logging.getLogger("integrations.sync")


def sync_threecx_users():
    client = ThreeCXClient()
    users = client.get_users()

    created = 0
    updated = 0

    for user in users:
        _, was_created = ThreeCXUser.objects.update_or_create(
            threecx_id=user["Id"],
            defaults={
                "extension": user.get("Number", ""),
                "display_name": user.get("DisplayName", ""),
                "is_registered": user.get("IsRegistered", False),
                "enabled": user.get("Enabled", True),
                "primary_group_id": user.get(
                    "PrimaryGroupId"
                ),
                "last_synced_at": timezone.now(),
            },
        )

        if was_created:
            created += 1
        else:
            updated += 1

    result = {
        "created": created,
        "updated": updated,
        "total": len(users),
    }
    logger.info("3CX sync: %s", result)
    return result