# -*- coding: utf-8 -*-

import json

from .builder import Builder


class SoapAgreementAttributeAdditional:
    """Build soap request to set/get additional attribute of the agreement."""

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

    def build_getter(self, account_number: int, attribute_id: int) -> None:
        """Soap to get additional field."""
        self._builder.add("fun", "o_mdb_api_func_get_add_dog_attrib")
        self._builder.add("pdogid", account_number)
        self._builder.add("pattrid", attribute_id)

        if attribute_id in (304, 305, 306, 307, 308, 390, 452, 454):
            self._builder.add("pattridup", 309)

        self._builder.add("pdate", None)

    def build_setter(
        self, account_number: int, attribute_id: int, value: str
    ) -> None:
        """Soap to set additional field."""
        if attribute_id == 309:
            options = {
                "fun": "o_mdb_api_change_dog_add_comp_dog_attrib_insert_p",
                "pdogid": account_number,
                "pattrid": attribute_id,
                "p_comp_attr_p": json.loads(value),  # pval
                "pdate": None,
            }
            self._builder.add_dict(options)  # type: ignore
        else:
            self._builder.add(
                "fun", "o_mdb_api_change_dog_add_dog_attrib_insert"
            )
            self._builder.add("pdogid", account_number)
            self._builder.add("pattrid", attribute_id)
            self._builder.add("pval", value)

            if attribute_id == 419:
                pavid: int = 4402 if value == "Да" else 4403
                self._builder.add("pavid", pavid)

            self._builder.add("pdate", None)
