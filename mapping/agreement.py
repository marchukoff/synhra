# -*- coding: utf-8 -*-

import enum
from collections import namedtuple
from typing import NamedTuple


_ = namedtuple(
    "UtidCRM",
    "description utid gm_agreementtype gm_agreementform gm_customertype",
)


class Utid(enum.Enum):
    type_err = _("ERROR", 0, 0, 0, 0)
    type_12 = _("Юр.Лицо", 12, 930660001, 930660001, 930660000)
    type_13 = _("Физ.лицо", 13, 930660000, 930660000, 930660000)
    type_39 = _("Служебный", 39, 930660000, 930660000, 930660001)
    type_42 = _("Конвергентый", 42, 930670002, 930660000, 930660002)


class Attribute(NamedTuple):
    onyma_key: str
    crm_key: str
    description: str


credit_schema_id = Attribute("csid", "gm_categoryofclient", "Кредитная схема")
dog_code = Attribute("dogcode", "gm_name", "Номер договора")
dog_date = Attribute(
    "dogdate", "gm_dateofagreementconclusion", "Дата начала договора"
)
dog_end_date = Attribute("dogend", "<unknown>", "Дата окончания")
dog_group_id = Attribute("gid", "_gm_onimagidid_value", "Группа")
eps_oper_id = Attribute("operid", "<unknown>", "Оператор")
status = Attribute("status", "gm_agreementstatus", "Статус договора")
tax_schema_id = Attribute("tsid", "<unknown>", "Налоговая схема")
agreement_type = Attribute(
    "utid", "gm_agreementtype", "Тип договора"
)  # [Onyma] Тип договора - [CRM] Gm_Aggrement.gm_agreementtype
customer_type = Attribute(
    "utid", "gm_customertype", "Тип клиента"
)  # [Onyma] Тип договора - [CRM] Account.gm_customertype
agreement_form = Attribute(
    "utid", "gm_agreementform", "Форма договора"
)  # [Onyma] Тип договора - [CRM] Account.gm_agreementform


class AdditionalAttribute(NamedTuple):
    onyma_key: int
    position: int
    crm_key: str
    description: str


additional_email = AdditionalAttribute(
    425, 0, "emailaddress2", "Дополнительный e-mail"
)
additional_telephone = AdditionalAttribute(
    426, 0, "address1_telephone1", "Дополнительный телефон"
)
bonus_status = AdditionalAttribute(394, 0, "<unknown>", "Бонусный статус")
comments = AdditionalAttribute(310, 0, "<unknown>", "Комментарий")
date_of_birth = AdditionalAttribute(
    306, 50, "gm_dateofbirth", "Дата рождения"
)
email = AdditionalAttribute(21, 0, "emailaddress1", "e-mail.newest_packages")
fax = AdditionalAttribute(25, 0, "<unknown>", "Факс")
name = AdditionalAttribute(12, 0, "name", "Название организации")
number_sms_info = AdditionalAttribute(
    402, 0, "gm_numberforsmsinforming", "Номер СМС информирования"
)
old_sys_dog_code = AdditionalAttribute(404, 0, "<unknown>", "Старый ЛС")
passport_date_of_issue = AdditionalAttribute(
    308, 40, "gm_passportdateofissue", "Дата выдачи паспорта"
)
passport_issued_by = AdditionalAttribute(
    307, 30, "gm_issuedby", "Кем выдан паспорт"
)
passport_number = AdditionalAttribute(
    304, 20, "gm_passportnumber", "Номер паспорта"
)
passport_series = AdditionalAttribute(
    305, 10, "gm_passportseries", "Серия паспорта"
)
passport_subdivision_code = AdditionalAttribute(
    452, 70, "gm_subdivisioncode", "Код подразделения выдавшего паспорт"
)
place_of_birth = AdditionalAttribute(
    390, 60, "gm_placeofbirth", "Место рождения"
)
registration_address = AdditionalAttribute(
    454, 80, "gm_registrationaddress", "Адрес регистрации"
)
telephone = AdditionalAttribute(24, 0, "telephone3", "Телефон")
telephone_mobile = AdditionalAttribute(
    311, 0, "telephone1", "Телефон мобильный"
)
vector = AdditionalAttribute(349, 0, "<unknown>", "Адрес-вектор")
# vector_flat = AdditionalAttribute(
#     "vector_flat", 0, "<unknown>", "Квартира из адрес вектора"
# )
# vector_house_fias = AdditionalAttribute(
#     "vector_fias", 0, "<unknown>", "Фиас дома из адрес Вектора"
# )
# vip = AdditionalAttribute(419, 0, "<unknown>", "Статус VIP")
