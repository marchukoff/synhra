# -*- coding: utf-8 -*-

from datetime import datetime
from ..function import AddressVector
from .builder import Builder


class SoapFunction:
    """Build soap request to create the site."""

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

    def group_to_domain(self, group_id: int) -> None:
        self._builder.add("fun", "onyma_api_onyma_get_dom_for_gid")
        self._builder.add("pgid", group_id)

    def ins_pay(self, account_number: int, amount: float) -> None:
        now = datetime.now()
        options = {
            "fun": "o_mdb_api_pay_ins_pay",
            "pdogid": account_number,
            "pamount": amount,
            "pbdate": None,
            "pmdate": None,
            "pidate": None,
            "ppaydoc": f"{now:%Y%m%d%H%M%S}",
            "pppdate": None,
            "premark": "Auto-test",
            "pcurrid": 2,
            "pppid": 137,
        }
        self._builder.add_dict(options)

    def get_vec_id(self, vector: AddressVector, vector_type: int) -> None:
        options = [{"column_value": i} for i in vector]
        self._builder.add("fun", "onyma_uni_api_get_vec_id")
        self._builder.add("pvec_type", vector_type)
        self._builder.add("pval", options)
