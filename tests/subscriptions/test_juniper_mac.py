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
    get_crm_factor,
    get_onyma_factor,
)


@pytest.fixture(scope="module")
def subscription(
    juniper_mac: mapping.SiteIndex
) -> mapping.SubscriptionIdGuid:
    subscription_: mapping.SubscriptionId = juniper_mac.subscriptions[0]
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
    mapping.subscription.ipaddress,
    mapping.subscription.netmask,
    mapping.subscription.macaddress,
)


@pytest.fixture(scope="module", params=ATTRIBUTE, ids=id_attributes)
def attribute(request) -> mapping.subscription.SubscriptionProperty:
    return request.param


@allure.title("Juniper MAC. Тест атрибута подключки")
@pytest.mark.subscription
def test_attribute(
    subscription: mapping.SubscriptionIdGuid,
    attribute: mapping.subscription.SubscriptionProperty,
):
    if attribute.is_sync:
        crm = get_crm_attribute(subscription.guid, attribute.crm_key)
        onyma = get_onyma_attribute(subscription.number, attribute.onyma_key)
        allure.dynamic.title(
            f"Juniper MAC. Тест атрибута подключки '{attribute.description}'"
        )
        check_attribute(crm, onyma, attribute.crm_key)


@allure.title("Juniper MAC. Тест ценового коэффициента")
@pytest.mark.subscription
def test_price_factor(
    subscription: mapping.SubscriptionIdGuid, juniper_mac: mapping.SiteIndex
):
    crm = get_crm_factor(subscription.guid)
    onyma = get_onyma_factor(juniper_mac.site_id)
    check_attribute(crm, onyma, "gm_additionaldiscount")
