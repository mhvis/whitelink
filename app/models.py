from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.utils import timezone

from app.firewall import whitelist_ips


class WhitelistEntryManager(models.Manager):
    def update_firewall(self):
        """Updates the firewall with all IPs in the database."""
        whitelist_ips([e.ip for e in self.all()])

    def add(self, **kwargs):
        """Creates a new entry with given parameters and updates the firewall."""
        with transaction.atomic():
            WhitelistEntry.objects.create(**kwargs)
            WhitelistEntry.objects.update_firewall()


class WhitelistEntry(models.Model):
    ip = models.GenericIPAddressField(db_index=True)
    friendly_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    is_admin = models.BooleanField(default=False)  # Currently not used

    objects = WhitelistEntryManager()

    def revoke(self):
        """Deletes entry and synchronously updates firewall."""
        with transaction.atomic():
            self.delete()
            WhitelistEntry.objects.update_firewall()


class WhitelistSettings(models.Model):
    code = models.CharField(max_length=100, default='whitelink')
    max_entries = models.IntegerField(default=20, validators=[MinValueValidator(0), MaxValueValidator(1000)])

    @classmethod
    def get(cls):
        """Returns the whitelist settings instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
