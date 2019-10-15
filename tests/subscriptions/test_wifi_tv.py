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


# Note: wifi_tv.subscriptions[0] - это приставка wifitv в рассрочку


@pytest.fixture(scope="module")
def subscription_wifi_tv(
    wifi_tv: mapping.SiteIndex
) -> mapping.SubscriptionIdGuid:
    subscription_: mapping.SubscriptionId = wifi_tv.subscriptions[1]
    subscription_guid = api.crm.subscription.get_subscription_guid(
        subscription_.subscription_id
    )
    if subscription_guid:
        return mapping.SubscriptionIdGuid(
            subscription_.subscription_id, subscription_guid
        )
    else:
        pytest.skip("No subscription in CRM")


@pytest.fixture(scope="module")
def subscription_wifi_tv_pack(
    wifi_tv: mapping.SiteIndex
) -> mapping.SubscriptionIdGuid:
    subscription_: mapping.SubscriptionId = wifi_tv.subscriptions[2]
    subscription_guid = api.crm.subscription.get_subscription_guid(
        subscription_.subscription_id
    )
    if subscription_guid:
        return mapping.SubscriptionIdGuid(
            subscription_.subscription_id, subscription_guid
        )
    else:
        pytest.skip("No subscription in CRM")


ATTRIBUTE_WIFI_TV = (
    mapping.subscription.login,
    mapping.subscription.password,
)
ATTRIBUTE_WIFI_TV_PACK = (mapping.subscription.hhid,)


@pytest.fixture(scope="module", params=ATTRIBUTE_WIFI_TV, ids=id_attributes)
def attribute_wifi_tv(request) -> mapping.subscription.SubscriptionProperty:
    return request.param


@pytest.fixture(
    scope="module", params=ATTRIBUTE_WIFI_TV_PACK, ids=id_attributes
)
def attribute_wifi_tv_pack(
    request
) -> mapping.subscription.SubscriptionProperty:
    return request.param


@allure.title("WiFi Tv. Тест атрибута подключки")
@pytest.mark.subscription
def test_attribute_wifi_tv(
    subscription_wifi_tv: mapping.SubscriptionIdGuid,
    attribute_wifi_tv: mapping.subscription.SubscriptionProperty,
):
    if attribute_wifi_tv.is_sync:
        crm = get_crm_attribute(
            subscription_wifi_tv.guid, attribute_wifi_tv.crm_key
        )
        onyma = get_onyma_attribute(
            subscription_wifi_tv.number, attribute_wifi_tv.onyma_key
        )
        allure.dynamic.title(
            f"WiFi Tv. Тест атрибута подключки '{attribute_wifi_tv.description}'"
        )
        check_attribute(crm, onyma, attribute_wifi_tv.crm_key)


@allure.title("WiFi Tv пакет. Тест атрибута подключки")
@pytest.mark.subscription
def test_attribute_wifi_tv_pack(
    subscription_wifi_tv_pack: mapping.SubscriptionIdGuid,
    attribute_wifi_tv_pack: mapping.subscription.SubscriptionProperty,
):
    if attribute_wifi_tv_pack.is_sync:
        crm = get_crm_attribute(
            subscription_wifi_tv_pack.guid, attribute_wifi_tv_pack.crm_key
        )
        onyma = get_onyma_attribute(
            subscription_wifi_tv_pack.number, attribute_wifi_tv_pack.onyma_key
        )
        allure.dynamic.title(
            f"WiFi Tv пакет. Тест атрибута подключки '{attribute_wifi_tv_pack.description}'"
        )
        check_attribute(crm, onyma, attribute_wifi_tv_pack.crm_key)
