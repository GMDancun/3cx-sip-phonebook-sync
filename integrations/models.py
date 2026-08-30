from django.db import models

class ThreeCXUser(models.Model):
    threecx_id = models.IntegerField(unique=True)

    extension = models.CharField(max_length=20)

    display_name = models.CharField(max_length=200, blank=True)

    is_registered = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)

    primary_group_id = models.IntegerField(
        null=True,
        blank=True,
    )

    last_synced_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.extension} - {self.display_name}"