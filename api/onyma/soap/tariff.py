# -*- coding: utf-8 -*-
from typing import NamedTuple

from .builder import Builder


class Tariff(NamedTuple):
    site_id: int  # id учетного имени
    subscription_id: int = 0  # id подключения
    tariff_id: int = 5942  # Tariff ID - WiFire 100
    service_id: int = 614  # Service ID - Абонентская плата за интернет
    price: float = 0.5  # SETUP pcost OR pccntr!
    factor: float = 0.0  # 0 < pccntr <= 1.0


class SoapTariff:
    """Build soap request to set/get additional attribute of the subscription."""

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

    def build_getter(self, site_id: int) -> None:
        """Soap to get tariff."""
        self._builder.add("fun", "o_mdb_api_dog_serv_f")
        self._builder.add("dmid", {"is": site_id})
        self._builder.add("enddate", {"is_null": 1})

    def build_setter(self, tariff: Tariff) -> None:
        """Soap to set tariff."""
        self._builder.add("fun", "o_mdb_api_change_connection_set_tmid")
        self._builder.add("pclsrv", tariff.subscription_id)
        self._builder.add("ptmid", tariff.tariff_id)


class SoapPriceFactor(SoapTariff):
    """Build soap request to set/get additional attribute of the subscription."""

    def build_setter(self, tariff: Tariff) -> None:
        """Soap to set personal tariff."""
        fun = "o_mdb_api_map_main_p_save_personal_tariff"

        if all((tariff.price, tariff.factor)):
            tariff.price = 0.0
            tariff.factor = 0.5

        self._builder.add("fun", fun)
        options = {
            "prowid": "prowid",
            "pdmid": tariff.site_id,
            "pptmid": tariff.tariff_id,
            "pservid": tariff.service_id,
            "ptdid": "ptdid",
            "pclsrv": "pclsrv",
            "pbegdate": None,
            "penddate": "penddate",
            "pdcost": "pdcost",
            "pcost": tariff.price or "pcost",
            "pcntr": "pcntr",
            "pccntr": tariff.factor or "pccntr",
            "pserv_alias": "pserv_alias",
            "premark": "Auto-test",
            "pno_mcost": "pno_mcost",
            "p_no_eps": "p_no_eps",
        }

        self._builder.add_dict(options)
