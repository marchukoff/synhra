import re
import string
from datetime import datetime, timedelta

import mapping
from .filter_ import AbstractFilter


class CrmFilter(AbstractFilter):
    _keys = (
        "createdon",
        "gm_servicestatus",
        "gm_dateofagreementconclusion",
        mapping.agreement.additional_telephone.crm_key,
        mapping.agreement.credit_schema_id.crm_key,
        mapping.agreement.date_of_birth.crm_key,
        mapping.agreement.dog_code.crm_key,
        mapping.agreement.dog_date.crm_key,
        mapping.agreement.dog_group_id.crm_key,
        mapping.agreement.name.crm_key,
        mapping.agreement.passport_date_of_issue.crm_key,
        mapping.agreement.status.crm_key,
        mapping.agreement.telephone.crm_key,
        mapping.agreement.telephone_mobile.crm_key,
        mapping.subscription.macaddress.crm_key,
        mapping.subscription.macaddressipoe.crm_key,
        mapping.subscription.routermacaddress.crm_key,
        mapping.subscription.stbmac.crm_key,
    )

    def filtrate(self, key: str, value: str) -> str:
        if key not in self._keys:
            return value
        else:
            return super().filtrate(key, value)


class CrmName(AbstractFilter):
    def filtrate(self, key: str, value: str) -> str:
        if key == mapping.agreement.name.crm_key:
            return value.replace("\xa0", " ").strip()
        else:
            return super().filtrate(key, value)


class CrmTelephone(AbstractFilter):
    _keys = (
        mapping.agreement.telephone_mobile.crm_key,
        mapping.agreement.telephone.crm_key,
        mapping.agreement.additional_telephone.crm_key,
    )

    def filtrate(self, key: str, value: str) -> str:
        if key in self._keys:
            return re.sub(r"^\+7", "8", value)
        else:
            return super().filtrate(key, value)


class CrmDate(AbstractFilter):
    _keys = (
        mapping.agreement.date_of_birth.crm_key,
        mapping.agreement.passport_date_of_issue.crm_key,
    )

    def filtrate(self, key: str, value: str) -> str:
        if key not in self._keys:
            return super().filtrate(key, value)

        try:
            datetime_object1 = datetime.strptime(
                value, "%d.%m.%Y %H:%M:%S %z"
            )
        except ValueError:
            return value

        return "T".join((datetime_object1.strftime("%d.%m.%Y"), "12:00:00"))


class CrmAgreementDate(AbstractFilter):
    def filtrate(self, key: str, value: str) -> str:
        if key not in ("createdon", "gm_dateofagreementconclusion"):
            return super().filtrate(key, value)

        try:
            datetime_object = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
        except ValueError:
            try:
                datetime_object = datetime.strptime(
                    value, "%d.%m.%Y %H:%M:%S %z"
                )
            except ValueError:
                return value

        return datetime_object.strftime("%d.%m.%Y")


class CrmDogDate(AbstractFilter):
    def filtrate(self, key: str, value: str) -> str:
        if key == mapping.agreement.dog_date.crm_key:
            try:
                datetime_object1 = datetime.strptime(
                    value, "%Y-%m-%dT%H:%M:%S%z"
                )
            except ValueError:
                try:
                    datetime_object1 = datetime.strptime(
                        value, "%d.%m.%Y %H:%M:%S %z"
                    )
                except ValueError:
                    return value
            datetime_object2 = datetime_object1 + timedelta(hours=3)
            d = datetime_object2.isoformat(sep="T")[0:16]
            return ":".join((d, "00"))
        else:
            return super().filtrate(key, value)


class CrmDogCode(AbstractFilter):
    def filtrate(self, key: str, value: str) -> str:
        if key == mapping.agreement.dog_code.crm_key:
            if value.isdigit():
                return value[2:]
            else:
                return value.split("|")[0]
        else:
            return super().filtrate(key, value)


class CrmMac(AbstractFilter):
    _keys = (
        mapping.subscription.macaddress.crm_key,
        mapping.subscription.macaddressipoe.crm_key,
        mapping.subscription.routermacaddress.crm_key,
        mapping.subscription.stbmac.crm_key,
    )

    def filtrate(self, key: str, value: str) -> str:
        if key in self._keys:
            octets = value.split(":")
            if len(octets) == 6:
                double_octets = [
                    octets[i * 2] + octets[i * 2 + 1]
                    for i in range(len(octets) // 2)
                ]
                return ".".join(double_octets)
            else:
                return value
        else:
            return super().filtrate(key, value)


class CrmStatus(AbstractFilter):
    _status = {
        "930660000": "Active",
        "930660001": "Inactive",
        "930660002": "PausedBySystem",
        "930660003": "PausedByOperator",
        "930660004": "Closed",
        "930660006": "Closed",  # - gm_servicestatus - GRM: "Удален"
        "None": "Inactive",
    }

    def filtrate(self, key: str, value: str) -> str:
        if key in (mapping.agreement.status.crm_key, "gm_servicestatus"):
            return self._status.get(value, value)
        else:
            return super().filtrate(key, value)


class CrmCreditSchema(AbstractFilter):
    # 0 - Постоплатный [CRM]
    # 1 - Предоплатный [CRM]
    _schema = {"930660000": "Prepaid", "930660001": "Credit"}

    def filtrate(self, key: str, value: str) -> str:
        if key == mapping.agreement.credit_schema_id.crm_key:
            return self._schema.get(value, value)
        else:
            return super().filtrate(key, value)


class CrmDogGroup(AbstractFilter):
    _groups = {
        "79e70a00-3198-e611-80c5-005056b40c72": "inetera.Orel",
        "2bfcca17-4a99-e611-80c5-005056b419d0": "inetera.Mcensk",
        "37fcca17-4a99-e611-80c5-005056b419d0": "inetera.Znamenka_Orel",
    }

    def filtrate(self, key: str, value: str) -> str:
        if key == mapping.agreement.dog_group_id.crm_key:
            return self._groups.get(value, value)
        else:
            return super().filtrate(key, value)


class CrmVipStatus(AbstractFilter):
    _vip = ("Да", "Нет")

    def filtrate(self, key: str, value: str) -> str:
        if key == "gm_classofclient":
            return self._vip[int(value[-1])]
        else:
            return super().filtrate(key, value)
