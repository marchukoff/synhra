import allure
from transliterate import translit
from typing import Tuple
import api
import filters
import mapping


@allure.step('Получаем доп. атрибут "{attribute_key}" из CRM')
def crm_get_attribute_additional(
    account_id: mapping.GUID, attribute_key: str
):
    return api.crm.account.get_attribute(account_id, attribute_key)


@allure.step('Получаем доп. атрибут "{attribute_key}" из Onyma')
def onyma_get_attribute_additional(account_number: int, attribute_key: int):
    return api.onyma.attribute_additional.get_additional_attribute(
        account_number, attribute_key
    )


@allure.step('Получаем атрибут "{attribute_key}" из CRM')
def crm_get_utid(
    account_id: mapping.GUID, agreement_id: mapping.GUID, attribute_key: str
) -> Tuple[int, Tuple[mapping.agreement.Utid]]:
    if attribute_key == mapping.agreement.agreement_type.crm_key:
        crm_utid = api.crm.agreement.get_attribute(
            agreement_id, attribute_key
        )
        select = {
            930660001: (mapping.agreement.Utid.type_12,),
            930660000: (
                mapping.agreement.Utid.type_13,
                mapping.agreement.Utid.type_39,
                mapping.agreement.Utid.type_42,
            ),
        }
    elif attribute_key == mapping.agreement.agreement_form.crm_key:
        crm_utid = api.crm.account.get_attribute(account_id, attribute_key)
        select = {
            930660001: (mapping.agreement.Utid.type_12,),
            930660000: (
                mapping.agreement.Utid.type_13,
                mapping.agreement.Utid.type_39,
            ),
            930670002: (mapping.agreement.Utid.type_42,),
        }
    elif attribute_key == mapping.agreement.customer_type.crm_key:
        crm_utid = api.crm.account.get_attribute(account_id, attribute_key)
        select = {
            930660000: (
                mapping.agreement.Utid.type_12,
                mapping.agreement.Utid.type_13,
            ),
            930660001: (mapping.agreement.Utid.type_39,),
            930660002: (mapping.agreement.Utid.type_42,),
        }
    else:
        raise Exception(f'Unknown type "{attribute_key}"')

    try:
        crm_utid = int(crm_utid)
    except TypeError:
        return 0, (mapping.agreement.Utid.type_err,)
    except ValueError:
        return 0, (mapping.agreement.Utid.type_err,)

    return crm_utid, select.get(crm_utid, (mapping.agreement.Utid.type_err,))


@allure.step('Получаем атрибут "{attribute_key}" из CRM')
def crm_get_attribute(
    account_id: mapping.GUID, agreement_id: mapping.GUID, attribute_key: str
) -> str:
    if attribute_key in (
        mapping.agreement.status.crm_key,
        mapping.agreement.credit_schema_id.crm_key,
    ):
        return api.crm.account.get_attribute(account_id, attribute_key)
    else:
        return api.crm.agreement.get_attribute(agreement_id, attribute_key)


@allure.step('Получаем атрибут "{attribute_key}" из Onyma')
def onyma_get_utid(
    account_number: int, attribute_key: str
) -> mapping.agreement.Utid:
    select = {
        12: mapping.agreement.Utid.type_12,
        13: mapping.agreement.Utid.type_13,
        39: mapping.agreement.Utid.type_39,
        42: mapping.agreement.Utid.type_42,
    }

    try:
        utid = int(
            api.onyma.attribute.get_attribute(account_number, attribute_key)
        )
    except TypeError:
        return mapping.agreement.Utid.type_err
    except ValueError:
        return mapping.agreement.Utid.type_err

    return select.get(utid, mapping.agreement.Utid.type_err)


@allure.step('Получаем атрибут "{attribute_key}" из Onyma')
def onyma_get_attribute(account_number: int, attribute_key: str):
    return api.onyma.attribute.get_attribute(account_number, attribute_key)


@allure.step("Сравниваем значения атрибута в CRM и Onyma")
def check_attribute(crm, onyma, assertion_tag="!") -> None:
    assert (
        crm == onyma
    ), f'[{assertion_tag}] Значение атрибута в CRM "{crm}" отличается от значения в Onyma "{onyma}"'


@allure.step("Сравниваем тип/форму CRM и Onyma")
def check_type_form(
    crm_value: int,
    crm_utids: Tuple[mapping.agreement.Utid],
    onyma: mapping.agreement.Utid,
    attribute: mapping.agreement.Attribute,
) -> None:
    assert onyma in crm_utids, (
        f"[{attribute.crm_key}] Типу договора в Onyma "
        f'"{onyma.value.description}" ({onyma.value.utid}) не '
        f"соответствует значение атрибута в CRM {crm_value}."
    )


def id_attributes(fixture_value):
    return translit(fixture_value.description, "ru", reversed=True)


def filter_crm_attibute_additional() -> filters.crm.CrmFilter:
    filter_ = filters.crm.CrmFilter()
    filter_name = filters.crm.CrmName()
    filter_date = filters.crm.CrmDate()
    filter_telephone = filters.crm.CrmTelephone()
    filter_.set_filter(filter_name).set_filter(filter_telephone).set_filter(
        filter_date
    )
    return filter_


def filter_crm_attribute() -> filters.crm.CrmFilter:
    filter_ = filters.crm.CrmFilter()
    filter_credit = filters.crm.CrmCreditSchema()
    filter_code = filters.crm.CrmDogCode()
    filter_date = filters.crm.CrmDogDate()
    filter_status = filters.crm.CrmStatus()
    filter_.set_filter(filter_credit).set_filter(filter_code).set_filter(
        filter_date
    ).set_filter(filter_status)
    return filter_


def filter_onyma_attribute() -> filters.onyma.OnymaFilter:
    filter_ = filters.onyma.OnymaFilter()
    filter_credit = filters.onyma.OnymaCreditSchema()
    filter_code = filters.onyma.OnymaDogCode()
    filter_date = filters.onyma.OnymaDogDate()
    filter_status = filters.onyma.OnymaStatus()
    filter_.set_filter(filter_credit).set_filter(filter_code).set_filter(
        filter_date
    ).set_filter(filter_status)
    return filter_
