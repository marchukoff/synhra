# -*- coding: utf-8 -*-

import allure
import pytest

import api
import mapping
from .steps import (
    check_attribute,
    id_attributes,
    get_crm_attribute,
    get_onyma_attribute,
)


@pytest.fixture(scope="module")
def subscription(ipoe_mac: mapping.SiteIndex) -> mapping.SubscriptionIdGuid:
    subscription_: mapping.SubscriptionId = ipoe_mac.subscriptions[0]
    subscription_guid = api.crm.subscription.get_subscription_guid(
        subscription_.subscription_id
    )
    if subscription_guid:
        return mapping.SubscriptionIdGuid(
            subscription_.subscription_id, subscription_guid
        )
    else:
        pytest.skip("No subscription in CRM")


ATTRIBUTE = (
    mapping.subscription.ipaddressipoe,
    mapping.subscription.macaddressipoe,
)


@pytest.fixture(scope="module", params=ATTRIBUTE, ids=id_attributes)
def attribute(request) -> mapping.subscription.SubscriptionProperty:
    return request.param


@allure.title("IPoE MAC. Тест атрибута подключки")
@pytest.mark.subscription
def test_attribute(
    subscription: mapping.SubscriptionIdGuid,
    attribute: mapping.subscription.SubscriptionProperty,
):
    if attribute.is_sync:
        crm = get_crm_attribute(subscription.guid, attribute.crm_key)
        onyma = get_onyma_attribute(subscription.number, attribute.onyma_key)
        allure.dynamic.title(
            f"IPoE MAC. Тест атрибута подключки '{attribute.description}'"
        )
        check_attribute(crm, onyma, attribute.crm_key)
