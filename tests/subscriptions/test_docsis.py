# -*- coding: utf-8 -*-

import allure
import pytest
from typing import Tuple

import api
import mapping
from .steps import (
    check_attribute,
    id_attributes,
    get_crm_attribute,
    get_onyma_attribute,
)


@pytest.fixture(
    scope="module",
    params=[
        mapping.subscription.docsismac,
        mapping.subscription.logindocsis,
        mapping.subscription.passwordocsis,
    ],
    ids=id_attributes,
)
def param_test(
    request, docsis
) -> Tuple[
    mapping.SubscriptionIdGuid, mapping.subscription.SubscriptionProperty
]:
    subscription: mapping.SubscriptionId = docsis.subscriptions[0]
    subscription_id = api.crm.subscription.get_subscription_guid(
        subscription.subscription_id
    )
    if not subscription_id:
        pytest.skip("No subscription in CRM")

    return (
        mapping.SubscriptionIdGuid(
            subscription.subscription_id, subscription_id
        ),
        request.param,
    )


@allure.title("Docsis. Тест атрибута подключки")
@pytest.mark.subscription
def test_attribute(param_test):
    subscription, attribute = param_test
    if attribute.is_sync:
        crm = get_crm_attribute(subscription.guid, attribute.crm_key)
        onyma = get_onyma_attribute(subscription.number, attribute.onyma_key)
        allure.dynamic.title(
            f"Docsis. Тест атрибута подключки '{attribute.description}'"
        )
        check_attribute(crm, onyma, attribute.crm_key)
