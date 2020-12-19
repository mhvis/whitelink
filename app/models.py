from django.db import models


class WhitelistEntry(models.Model):
    ip = models.GenericIPAddressField(db_index=True)
    friendly_name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
