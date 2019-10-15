# -*- coding: utf-8 -*-

import logging
import time

import allure
import pytest

import api
import filters
import mapping
from .steps import check_attribute

LOGGER = logging.getLogger("test.%s" % __name__)


@pytest.fixture(scope="module")
def subscription(
    close_juniper_mac: mapping.SiteIndex
) -> mapping.SubscriptionIdGuid:
    subscription_: mapping.SubscriptionId = close_juniper_mac.subscriptions[0]
    subscription_guid = api.crm.subscription.get_subscription_guid(
        subscription_.subscription_id
    )
    if subscription_guid:
        return mapping.SubscriptionIdGuid(
            subscription_.subscription_id, subscription_guid
        )
    else:
        pytest.skip("No subscription in CRM")


def filter_crm() -> filters.crm.CrmFilter:
    filter_ = filters.crm.CrmFilter()
    filter_status = filters.crm.CrmStatus()
    filter_.set_filter(filter_status)
    return filter_


def filter_onyma() -> filters.onyma.OnymaFilter:
    filter_ = filters.onyma.OnymaFilter()
    filter_status = filters.onyma.OnymaStatus()
    filter_.set_filter(filter_status)
    return filter_


@allure.step("Получаем статус из CRM")
def get_crm_status(subscription_guid: mapping.GUID) -> str:
    result = api.crm.subscription.get_attribute(
        subscription_guid, "gm_servicestatus"
    )
    allure.attach(result, attachment_type=allure.attachment_type.TEXT)
    return result


@allure.step("Получаем статус из Onyma")
def get_onyma_status(subscription_id: int) -> str:
    result = api.onyma.subscription.get_status(subscription_id)
    allure.attach(result, attachment_type=allure.attachment_type.TEXT)
    return result


@allure.title("Juniper MAC. Тест синхронизации закрытия подключки")
@pytest.mark.subscription
def test_status(subscription: mapping.SubscriptionIdGuid,):
    api.onyma.subscription.set_status(
        subscription.number, mapping.status.closed.onyma_id
    )
    LOGGER.info(
        "Wait 5 minutes to synchronize the closure of the subscription."
    )
    time.sleep(300)

    crm_filter = filter_crm()
    crm = crm_filter.filtrate(
        "gm_servicestatus", get_crm_status(subscription.guid)
    )

    onyma_filter = filter_onyma()
    onyma = onyma_filter.filtrate(
        "subscription_status", get_onyma_status(subscription.number)
    )

    check_attribute(crm, onyma, "gm_servicestatus")
