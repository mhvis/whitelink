"""API for setting the whitelist rules on a firewall.

The only concrete implementation is for Azure virtual networks but it's possible to add
other implementations, e.g. for iptables using the python-iptables package.
"""
import json
from typing import List

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from requests import HTTPError, Response


class BaseRuleUpdater:
    """Base class for updating firewall rules.

    The base implementation is a no-op.
    """

    def update(self, allowed_ips: List[str]):
        """Updates the firewall to allow access to the given IPs."""
        # No-op
        pass

    @classmethod
    def from_settings(cls):
        """Initialize class with configuration from Django settings.

        This is used for subclasses that have a constructor with required
        parameters.
        """
        return cls()


def raise_for_status(r: Response):
    """Raises exception for HTTP 4XX or 5XX status codes."""
    # Overrides Response.raise_for_status() to include the response body.
    try:
        r.raise_for_status()
    except HTTPError as e:
        msg = "{}\n{}".format(str(e), e.response.text)
        raise HTTPError(msg, response=e.response)


class AzureRuleUpdater(BaseRuleUpdater):
    """Updates the firewall rules of an Azure Network Security group.

    Usage:

    1. Register an application (service principal) in Azure portal and
        configure this app with the required settings (subscription ID,
        resource group name, NSG name, tenant ID, client ID and client secret.
    2. Grant the application contributor access to the NSG in Azure portal.

    Note: this class overwrites all user created rules on the network security
    group. To have additional custom rules, e.g. for allowing HTTP access, add
    them to the AZURE_DEFAULT_RULES setting.
    """

    def __init__(self,
                 tenant_id: str,
                 client_id: str,
                 client_secret: str,
                 subscription_id: str,
                 resource_group: str,
                 network_security_group: str):
        """Construct with the required parameters."""
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.subscription_id = subscription_id
        self.resource_group = resource_group
        self.network_security_group = network_security_group

    @classmethod
    def from_settings(cls):
        """Initializes with configuration from Django settings."""
        if not settings.AZURE_NETWORK_SECURITY_GROUP:
            raise ImproperlyConfigured("Azure not configured")
        return cls(settings.AZURE_TENANT_ID, settings.AZURE_CLIENT_ID, settings.AZURE_CLIENT_SECRET,
                   settings.AZURE_SUBSCRIPTION_ID, settings.AZURE_RESOURCE_GROUP, settings.AZURE_NETWORK_SECURITY_GROUP)

    def get_access_token(self):
        """Returns an access token for Azure API."""
        token_url = 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'.format(tenant=self.tenant_id)
        body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://management.azure.com/.default',
            'grant_type': 'client_credentials',
        }
        r = requests.post(token_url, data=body)
        r.raise_for_status()
        token_data = r.json()
        return token_data['access_token']

    def auth(self, r):
        """Modifies a request to add authorization.

        Can be given as callable to the `auth` parameter of the requests
        library.
        """
        token = self.get_access_token()
        r.headers['Authorization'] = 'Bearer {}'.format(token)
        return r

    def get_network_security_group_url(self):
        """Returns the API URL of the network security group."""
        return ('https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers'
                '/Microsoft.Network/networkSecurityGroups/{network_security_group}?api-version=2020-07-01').format(
            subscription_id=self.subscription_id,
            resource_group=self.resource_group,
            network_security_group=self.network_security_group,
        )

    def get_network_security_group(self):
        r = requests.get(self.get_network_security_group_url(), auth=self.auth)
        r.raise_for_status()
        return r.json()

    def update(self, allowed_ips: List[str]):
        """Updates the Azure network security group rules.

        This retrieves the current configuration first, extracts the existing
        rules, and update the rules for Whitelink while keeping the other
        existing rules.
        """
        # Retrieve NSG definition
        nsg = self.get_network_security_group()

        # Construct Whitelink rules
        whitelink_rules = [
            {
                'name': 'Whitelink',
                'properties': {
                    'protocol': '*',
                    'sourceAddressPrefixes': allowed_ips,
                    'destinationAddressPrefix': '*',
                    'access': 'Allow',
                    'destinationPortRanges': [str(p) for p in settings.ALLOW_PORTS],
                    'sourcePortRange': '*',
                    'priority': 1234,
                    'direction': 'Inbound',
                    'description': "This rule is automatically configured using Whitelink.",
                },
            },
        ]

        # Extract non-Whitelink existing rules
        other_rules = []
        for rule in nsg['properties']['securityRules']:
            # Ignore Whitelink rule
            if rule['name'] == 'Whitelink':
                continue
            # Get rid of provisioningState in the property dict
            props = rule['properties']
            del props['provisioningState']
            # Store rule
            other_rules.append({
                'name': rule['name'],
                'properties': props
            })

        # Update NSG
        body = {
            'properties': {
                'securityRules': whitelink_rules + other_rules,
            },
            'location': nsg['location'],
        }
        r = requests.put(self.get_network_security_group_url(), json=body, auth=self.auth)
        raise_for_status(r)
        return r.json()


_rule_updater_choices = {
    'base': BaseRuleUpdater,
    'azure': AzureRuleUpdater
}


def whitelist_ips(ips: List[str]):
    """Whitelists given IPs using the rule updater set in the configuration."""
    updater = _rule_updater_choices[settings.RULE_UPDATER].from_settings()
    updater.update(ips)
