from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class WhitelistEntry(models.Model):
    ip = models.GenericIPAddressField(db_index=True)
    friendly_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    is_admin = models.BooleanField(default=False)  # Currently not used


class WhitelistSettings(models.Model):
    code = models.CharField(max_length=100, default='whitelink')
    max_entries = models.IntegerField(default=20, validators=[MinValueValidator(0), MaxValueValidator(1000)])

    @classmethod
    def get(cls):
        """Returns the whitelist settings instance."""
        return cls.objects.get_or_create(pk=1)
