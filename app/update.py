from django.conf import settings

from app.firewall import AzureRuleUpdater, BaseRuleUpdater
from app.models import WhitelistEntry

rule_updater_choices = {
    'base': BaseRuleUpdater,
    'azure': AzureRuleUpdater
}


def update_firewall():
    """Updates the firewall with the whitelisted addresses from the database."""
    ips = [e.ip for e in WhitelistEntry.objects.all()]

    # Use the rule updater that is set in the configuration
    updater = rule_updater_choices[settings.RULE_UPDATER].from_settings()
    updater.update(ips)
