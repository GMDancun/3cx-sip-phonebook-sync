from django.contrib import admin
from .models import ThreeCXUser


@admin.register(ThreeCXUser)
class ThreeCXUserAdmin(admin.ModelAdmin):
    list_display = (
        "extension",
        "display_name",
        "is_registered",
        "enabled",
        "last_synced_at",
    )

    search_fields = (
        "extension",
        "display_name",
    )

    list_filter = (
        "enabled",
        "is_registered",
    )