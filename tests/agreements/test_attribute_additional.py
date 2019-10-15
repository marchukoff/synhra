# -*- coding: utf-8 -*-

import json
from typing import Tuple

import allure
import pytest

import api
import mapping
from .steps import (
    check_attribute,
    id_attributes,
    filter_crm_attibute_additional,
    crm_get_attribute_additional,
    onyma_get_attribute_additional,
)

TParam = Tuple[api.Account, mapping.agreement.AdditionalAttribute]


@pytest.fixture(
    scope="module",
    params=[
        mapping.agreement.name,
        mapping.agreement.email,
        mapping.agreement.additional_email,
        mapping.agreement.telephone_mobile,
        mapping.agreement.telephone,
        mapping.agreement.additional_telephone,
        mapping.agreement.number_sms_info,
        mapping.agreement.passport_number,  # passport
        mapping.agreement.passport_series,  # passport
        mapping.agreement.place_of_birth,  # passport
        mapping.agreement.passport_subdivision_code,  # passport
        mapping.agreement.passport_issued_by,  # passport
        mapping.agreement.date_of_birth,  # passport
        mapping.agreement.passport_date_of_issue,  # passport
        mapping.agreement.registration_address,  # passport
    ],
    ids=id_attributes,
)
def param_test(request, account) -> TParam:
    if not account.number:
        pytest.skip("There is no Account for testing.")

    return account, request.param


@allure.title("Тест дополнительного атрибута договора")
@pytest.mark.agreement
def test_attribute_additional(param_test):
    account, attribute_additional = param_test

    content_filter = filter_crm_attibute_additional()
    crm_raw = crm_get_attribute_additional(
        account.guid, attribute_additional.crm_key
    )
    crm = content_filter.filtrate(attribute_additional.crm_key, crm_raw)

    onyma = onyma_get_attribute_additional(
        account.number, attribute_additional.onyma_key
    )

    attach = {
        "account": {"number": account.number, "id": account.guid},
        "crm": {
            "key": attribute_additional.crm_key,
            "value": crm_raw,
            "filtered": crm,
        },
        "onyma": {"key": attribute_additional.onyma_key, "value": onyma},
    }
    allure.dynamic.title(
        f"Тест дополнительного атрибута договора '{attribute_additional.description}'"
    )
    allure.attach(
        json.dumps(attach, ensure_ascii=False),
        attachment_type=allure.attachment_type.JSON,
    )
    check_attribute(crm, onyma, attribute_additional.crm_key)
