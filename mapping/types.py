from typing import NewType, NamedTuple, List

from mapping import subscription

GUID = NewType("GUID", str)


class SubscriptionId(NamedTuple):
    subscription_id: int = 0
    subscription_type: subscription.Subscription = subscription.lk


class SubscriptionIdGuid(NamedTuple):
    number: int = 0
    guid: GUID = GUID("")


class SiteIndex(NamedTuple):
    site_id: int
    subscriptions: List[SubscriptionId]
