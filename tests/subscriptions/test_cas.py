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
def subscription_cas(cas: mapping.SiteIndex) -> mapping.SubscriptionIdGuid:
    subscription_: mapping.SubscriptionId = cas.subscriptions[0]
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
def subscription_cas_pack(
    cas: mapping.SiteIndex
) -> mapping.SubscriptionIdGuid:
    subscription_: mapping.SubscriptionId = cas.subscriptions[-1]
    subscription_guid = api.crm.subscription.get_subscription_guid(
        subscription_.subscription_id
    )
    if subscription_guid:
        return mapping.SubscriptionIdGuid(
            subscription_.subscription_id, subscription_guid
        )
    else:
        pytest.skip("No subscription in CRM")


ATTRIBUTE = (mapping.subscription.hhidcas,)


@pytest.fixture(scope="module", params=ATTRIBUTE, ids=id_attributes)
def attribute(request) -> mapping.subscription.SubscriptionProperty:
    return request.param


@allure.title("CAS. Тест атрибута подключки")
@pytest.mark.subscription
def test_attribute_cas(
    subscription_cas: mapping.SubscriptionIdGuid,
    attribute: mapping.subscription.SubscriptionProperty,
):
    if attribute.is_sync:
        crm = get_crm_attribute(subscription_cas.guid, attribute.crm_key)
        onyma = get_onyma_attribute(
            subscription_cas.number, attribute.onyma_key
        )
        allure.dynamic.title(
            f"CAS. Тест атрибута подключки '{attribute.description}'"
        )
        check_attribute(crm, onyma, attribute.crm_key)


@allure.title("CAS пакет. Тест атрибута подключки")
@pytest.mark.subscription
def test_attribute_cas_pack(
    subscription_cas_pack: mapping.SubscriptionIdGuid,
    attribute: mapping.subscription.SubscriptionProperty,
):
    if attribute.is_sync:
        crm = get_crm_attribute(subscription_cas_pack.guid, attribute.crm_key)
        onyma = get_onyma_attribute(
            subscription_cas_pack.number, attribute.onyma_key
        )
        allure.dynamic.title(
            f"CAS пакет. Тест атрибута подключки '{attribute.description}'"
        )
        check_attribute(crm, onyma, attribute.crm_key)
