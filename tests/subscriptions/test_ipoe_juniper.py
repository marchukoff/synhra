# -*- coding: utf-8 -*-
import time
import allure
import pytest
import logging
import api
import mapping
from .steps import (
    check_attribute,
    id_attributes,
    get_crm_attribute,
    get_onyma_attribute,
    get_onyma_price,
    get_crm_price,
    awaiting_sync,
)


LOGGER = logging.getLogger("test.%s" % __name__)


@pytest.fixture(scope="module")
def subscription(
    ipoe_juniper: mapping.SiteIndex
) -> mapping.SubscriptionIdGuid:
    subscription_: mapping.SubscriptionId = ipoe_juniper.subscriptions[0]
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
    mapping.subscription.portnumber,
    mapping.subscription.macaddress,
    mapping.subscription.routermacaddress,
)


@pytest.fixture(scope="module", params=ATTRIBUTE, ids=id_attributes)
def attribute(request) -> mapping.subscription.SubscriptionProperty:
    return request.param


@allure.title("IPoE Juniper. Тест атрибута подключки")
@pytest.mark.subscription
def test_attribute(
    subscription: mapping.SubscriptionIdGuid,
    attribute: mapping.subscription.SubscriptionProperty,
):
    if attribute.is_sync:
        crm = get_crm_attribute(subscription.guid, attribute.crm_key)
        onyma = get_onyma_attribute(subscription.number, attribute.onyma_key)
        allure.dynamic.title(
            f"IPoE Juniper. Тест атрибута подключки '{attribute.description}'"
        )
        check_attribute(crm, onyma, attribute.crm_key)


@allure.title("IPoE Juniper. Тест персцены")
@pytest.mark.subscription
def test_personal_price(
    subscription: mapping.SubscriptionIdGuid, ipoe_juniper: mapping.SiteIndex
):
    crm = get_crm_price(subscription.guid)
    onyma = get_onyma_price(ipoe_juniper.site_id)
    check_attribute(crm, onyma, "gm_onymapersonalcost")


@allure.title("IPoE Juniper. Тест смены тарифа")
@allure.description(
    """Проверка смены тарифа

1. Сначала проверяется, что тарифы одинаковы. Затем изменяется тариф в Onyma.

2. После таймаута проверяется, что новый тариф установлен в обеих системах.
"""
)
@pytest.mark.subscription
def test_tariff_change(
    subscription: mapping.SubscriptionIdGuid, ipoe_juniper: mapping.SiteIndex
):
    old_tariff_onyma: int = api.onyma.tariff.get_tariff_id(
        ipoe_juniper.site_id
    )
    tariff_crm: api.crm.subscription.Tariff = api.crm.subscription.get_tariff(
        subscription.guid
    )
    old_tariff_crm: int = tariff_crm.tariff_id_onyma
    check_attribute(old_tariff_crm, old_tariff_onyma, "gm_tariffid")

    new_tariff = api.onyma.tariff.Tariff(
        ipoe_juniper.site_id,
        subscription.number,
        mapping.subscription.Tariff.Wifire_100_120.value.tmid,
        mapping.subscription.Service.Internet.value.servid,
        0.0,
        0.0,
    )
    api.onyma.tariff.set_tariff(new_tariff)  # change tariff in onyma
    awaiting_sync(300)

    new_tariff_onyma: int = api.onyma.tariff.get_tariff_id(
        ipoe_juniper.site_id
    )
    assert (
        old_tariff_onyma != new_tariff_onyma
    ), f"Новый тариф не установлен в Onyma!"

    tariff_crm = api.crm.subscription.get_tariff(subscription.guid)
    new_tariff_crm: int = tariff_crm.tariff_id_onyma
    check_attribute(new_tariff_crm, new_tariff_onyma, "gm_tariffid")
