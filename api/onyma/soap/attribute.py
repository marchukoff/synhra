# -*- coding: utf-8 -*-

from typing import NamedTuple

import mapping
from .builder import Builder


class Function(NamedTuple):
    name: str
    parameter: str
    description: str


class SoapAgreementAttribute:
    """Build soap request to set/get the attribute of the agreement."""

    _mapping = {
        mapping.agreement.credit_schema_id.onyma_key: Function(
            "o_mdb_api_change_dog_set_csid", "pcsid", "кредитная схема"
        ),
        mapping.agreement.dog_code.onyma_key: Function(
            "o_mdb.api_change_dog_set_dogcode", "pdogcode", "номер договора"
        ),
        mapping.agreement.dog_date.onyma_key: Function(
            "o_mdb_api_change_dog_set_dogdate",
            "pdogdate",
            "дата заключения договора",
        ),
        mapping.agreement.dog_group_id.onyma_key: Function(
            "o_mdb_api_change_dog_set_gid", "pgid", "группа"
        ),
        mapping.agreement.status.onyma_key: Function(
            "o_mdb_api_change_dog_set_status", "pstatus", "статус"
        ),
        mapping.agreement.customer_type.onyma_key: Function(
            "o_mdb_api_change_dog_set_usertype", "putid", "тип договора"
        ),
    }

    def __init__(self) -> None:
        """Initialise an instance with the specified values."""
        self._builder: Builder = None  # type: ignore

    @property
    def builder(self) -> Builder:
        """Return builder property."""
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """Set builder property."""
        self._builder = builder

    def build_getter(self, account_number: int, attribute_id: str) -> None:
        """Build soap request to get attribute from Onyma."""
        options = {
            "fun": "o_mdb_api_get_dog_get_all_dog_attr",
            "pdogid": account_number,
            "pattr": attribute_id,
        }
        self.builder.add_dict(options)

    def build_setter(
        self, account_number: int, attribute_id: str, value: str
    ) -> None:
        """Soap to set additional field."""
        function = self._mapping.get(attribute_id)
        assert function, "unknown function in 'pattr'"
        options = {
            "fun": function.name,
            "pdogid": account_number,
            function.parameter: value,
        }
        self.builder.add_dict(options)
