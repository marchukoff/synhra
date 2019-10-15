# -*- coding: utf-8 -*-

import json
from typing import Tuple

import allure
import pytest

import api
import mapping
from .steps import (
    check_attribute,
    check_type_form,
    id_attributes,
    filter_crm_attribute,
    filter_onyma_attribute,
    crm_get_attribute,
    onyma_get_attribute,
    crm_get_utid,
    onyma_get_utid,
)

TParam = Tuple[api.Account, mapping.GUID, mapping.agreement.Attribute]


@pytest.fixture(
    scope="module",
    params=[
        mapping.agreement.status,
        mapping.agreement.credit_schema_id,
        mapping.agreement.dog_code,
        mapping.agreement.dog_date,
        mapping.agreement.customer_type,
        mapping.agreement.agreement_form,
        mapping.agreement.agreement_type,
    ],
    ids=id_attributes,
)
def param_test(request, account, agreement) -> TParam:
    if not account.number:
        pytest.skip("There is no Agreement for testing.")

    return account, agreement, request.param


@allure.title("Тест атрибута договора")
@pytest.mark.agreement
def test_attribute(param_test) -> None:
    account, agreement, attribute = param_test

    if attribute in (
        mapping.agreement.customer_type,
        mapping.agreement.agreement_form,
        mapping.agreement.agreement_type,
    ):
        crm_value, crm_utids = crm_get_utid(
            account.guid, agreement, attribute.crm_key
        )
        onyma = onyma_get_utid(account.number, attribute.onyma_key)

        attach = {
            "agreement": {"id": agreement},
            "account": {"number": account.number, "id": account.guid},
            "crm": {"key": attribute.crm_key, "value": crm_value},
            "onyma": {"key": attribute.onyma_key, "value": onyma.value.utid},
        }
        allure.dynamic.title(
            f'Тест атрибута договора "{attribute.description}"'
        )
        allure.attach(
            json.dumps(attach, ensure_ascii=False),
            attachment_type=allure.attachment_type.JSON,
        )
        check_type_form(crm_value, crm_utids, onyma, attribute)
    else:
        content_filter = filter_crm_attribute()
        crm_raw = crm_get_attribute(
            account.guid, agreement, attribute.crm_key
        )
        crm = content_filter.filtrate(attribute.crm_key, crm_raw)

        content_filter = filter_onyma_attribute()
        onyma_raw = onyma_get_attribute(account.number, attribute.onyma_key)
        onyma = content_filter.filtrate(attribute.onyma_key, onyma_raw)

        attach = {
            "agreement": {"id": agreement},
            "account": {"number": account.number, "id": account.guid},
            "crm": {
                "key": attribute.crm_key,
                "value": crm_raw,
                "filtered": crm,
            },
            "onyma": {
                "key": attribute.onyma_key,
                "value": onyma_raw,
                "filtered": onyma,
            },
        }
        allure.dynamic.title(
            f'Тест атрибута договора "{attribute.description}"'
        )
        allure.attach(
            json.dumps(attach, ensure_ascii=False),
            attachment_type=allure.attachment_type.JSON,
        )
        check_attribute(crm, onyma, attribute.crm_key)
