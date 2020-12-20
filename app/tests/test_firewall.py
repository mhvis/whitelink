import json
from unittest import SkipTest, skip

from django.conf import settings
from django.test import TestCase
from requests import HTTPError

from app.firewall import AzureRuleUpdater


class AzureTestCase(TestCase):

    def setUp(self):
        """Skips the test cases when Azure is not configured."""
        if not settings.AZURE_NETWORK_SECURITY_GROUP:
            raise SkipTest("Azure not configured")
        self.updater = AzureRuleUpdater.from_settings()

    @skip
    def test_get_nsg_rules(self):
        print(self.updater.get_rules())

    @skip
    def test_update(self):
        try:
            r = self.updater.update(['8.8.8.8', '8.8.8.9'])
        except HTTPError as e:
            print(e.response.text)
            raise e
        print(json.dumps(r, indent=4))