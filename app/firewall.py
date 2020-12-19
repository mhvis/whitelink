"""API for setting the whitelist rules on a firewall.

The only concrete implementation is for Azure Firewall but it's possible to add
other implementations, e.g. for iptables using the python-iptables package.
"""


class RuleUpdater:
    """Interface for updating firewall rules."""
    pass


class AzureRuleUpdater:


    pass
