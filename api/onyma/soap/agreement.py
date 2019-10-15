# -*- coding: utf-8 -*-

from typing import Optional
from .builder import Builder
import mapping


class SoapAgreement:
    """Build soap request to create the agreement."""

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

    def create(self, agreement_type: int = 39, group_id: int = 11991) -> None:
        """Build soap request to create the agreement."""
        self._builder.add("fun", "o_mdb_api_change_dog_dog_create")
        self._builder.add("pgid", group_id)  # 11991 - inetera.Orel
        self._builder.add("pdogdate", None)
        self._builder.add("putid", agreement_type)  # 39 - Служебный
        self._builder.add("premark", "Auto-test creates this agreement.")

    def close(self, account_number: int, date: Optional[str] = None) -> None:
        """Build soap request to close the agreement."""
        self._builder.add("fun", "o_mdb_api_change_dog_set_status")
        self._builder.add("pdogid", account_number)
        self._builder.add("premark", "Auto-test closes this agreement.")
        self._builder.add(
            "pstatus", mapping.status.closed.onyma_id
        )  # type: ignore
        self._builder.add("pdate", date)  # Example '2019-05-28T16:11:41'

    def index(self, account_number: int) -> None:
        """Build soap request to get list of sites from Agreement."""
        self._builder.add("fun", "o_mdb_api_map_main")
        self._builder.add("dogid", {"is": account_number})
