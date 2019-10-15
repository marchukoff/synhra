from datetime import datetime

import mapping
from .filter_ import AbstractFilter


class OnymaFilter(AbstractFilter):
    _keys = (
        "subscription_status",
        mapping.agreement.credit_schema_id.onyma_key,
        mapping.agreement.dog_code.onyma_key,
        mapping.agreement.dog_date.onyma_key,
        mapping.agreement.dog_group_id.onyma_key,
        mapping.agreement.status.onyma_key,
    )

    def filtrate(self, key: str, value: str) -> str:
        if key not in self._keys:
            return value
        else:
            return super().filtrate(key, value)


class OnymaStatus(AbstractFilter):
    _status = {
        "0": "Active",
        "1": "Inactive",
        "2": "PausedBySystem",
        "3": "PausedByOperator",
        "4": "Closed",
    }

    def filtrate(self, key: str, value: str) -> str:
        if key in ("subscription_status", mapping.agreement.status.onyma_key):
            return self._status.get(value, value)
        else:
            return super().filtrate(key, value)


class OnymaCreditSchema(AbstractFilter):
    _schema = {
        "48": "Credit",  # 48 - Кредит [Onyma]
        "49": "Prepaid",  # 49 - Предоплата [Onyma]
        "77": "Credit",  # 77 - Кредит 50 дней [Onyma]
        "96": "Credit",  # 96 - Кредит 20 дней [Onyma]
    }

    def filtrate(self, key: str, value: str) -> str:
        if key == mapping.agreement.credit_schema_id.onyma_key:
            return self._schema.get(value, value)
        else:
            return super().filtrate(key, value)


class OnymaDogDate(AbstractFilter):
    def filtrate(self, key: str, value: str) -> str:
        if key == mapping.agreement.dog_date.onyma_key:
            try:
                datetime_object = datetime.strptime(value, "%d.%m.%y %H:%M")
                d = datetime_object.isoformat(sep="T")
                ret = ":".join((d.rsplit(":", 1)[0], "00"))
            except ValueError:
                ret = value
            return ret
        else:
            return super().filtrate(key, value)


class OnymaDogCode(AbstractFilter):
    def filtrate(self, key: str, value: str) -> str:
        if key == mapping.agreement.dog_code.onyma_key:
            return value[2:]
        else:
            return super().filtrate(key, value)


class OnymaDogGroup(AbstractFilter):
    _groups = {
        "11991": "inetera.Orel",
        "19271": "inetera.Mcensk",
        "23151": "inetera.Znamenka_Orel",
    }

    def filtrate(self, key: str, value: str) -> str:
        if key == mapping.agreement.dog_group_id.onyma_key:
            return self._groups.get(value, value)
        else:
            return super().filtrate(key, value)
