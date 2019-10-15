# -*- coding: utf-8 -*-

import allure
from transliterate import translit
import time
import api
import filters
import mapping


def id_attributes(fixture_value):
    return translit(fixture_value.description, "ru", reversed=True)


def filter_crm_attribute() -> filters.crm.CrmFilter:
    filter_ = filters.crm.CrmFilter()
    filter_mac = filters.crm.CrmMac()
    filter_.set_filter(filter_mac)
    return filter_


@allure.step("Ожидаем синхронизацию {timeout}с.")
def awaiting_sync(timeout: int) -> None:
    time.sleep(timeout)


@allure.step('Получаем атрибут "{attribute_name}" из CRM')
def get_crm_attribute(subscription_guid: mapping.GUID, attribute_name: str):
    result = api.crm.subscription.get_attribute(
        subscription_guid, attribute_name
    )
    allure.attach(result, attachment_type=allure.attachment_type.TEXT)
    content_filter = filter_crm_attribute()
    return content_filter.filtrate(attribute_name, result)


@allure.step('Получаем атрибут "{attribute_id}" из Onyma')
def get_onyma_attribute(subscription_number: int, attribute_id: int):
    if attribute_id == mapping.subscription.hhid:
        result = api.onyma.subscription.get_property_real(
            subscription_number, attribute_id
        )
    else:
        result = api.onyma.subscription.get_property(
            subscription_number, attribute_id
        )
    allure.attach(result, attachment_type=allure.attachment_type.TEXT)
    return result


@allure.step("Получаем цену из CRM")
def get_crm_price(subscription_guid: mapping.GUID) -> float:
    cost = api.crm.subscription.get_attribute(
        subscription_guid, "gm_onymapersonalcost"
    )
    allure.attach(cost, attachment_type=allure.attachment_type.TEXT)
    try:
        result = float(cost.replace(",", "."))
    except TypeError:
        result = 0.0
    except ValueError:
        result = 0.0
    return result


@allure.step("Получаем цену из Onyma")
def get_onyma_price(site_id: int) -> float:
    result = api.onyma.tariff.get_personal_price(site_id)
    allure.attach(str(result), attachment_type=allure.attachment_type.TEXT)
    return result


@allure.step("Получаем ценовой коэффициент из CRM")
def get_crm_factor(subscription_guid: mapping.GUID) -> float:
    cost = api.crm.subscription.get_attribute(
        subscription_guid, "gm_additionaldiscount"
    )
    allure.attach(cost, attachment_type=allure.attachment_type.TEXT)
    try:
        discount = float(cost.replace(",", "."))
        result = 1.0 - discount / 100.0
    except TypeError:
        result = 0.0
    except ValueError:
        result = 0.0
    return result


@allure.step("Получаем ценовой коэффициент из Onyma")
def get_onyma_factor(site_id: int) -> float:
    result = api.onyma.tariff.get_price_factor(site_id)
    allure.attach(str(result), attachment_type=allure.attachment_type.TEXT)
    return result


@allure.step("Сравниваем значения атрибута в CRM и Onyma")
def check_attribute(crm, onyma, assertion_tag="!"):
    assert (
        crm == onyma
    ), f'[{assertion_tag}] Значение атрибута в CRM "{crm}" отличается от значения в Onyma "{onyma}"'
