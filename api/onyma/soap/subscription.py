# -*- coding: utf-8 -*-

from .builder import Builder
from ..subscription import Subscription


class SoapSubscription:
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

    def create(self, subscription: Subscription) -> None:
        """Build soap request to create the agreement."""
        option = {
            "fun": "o_mdb_api_change_connection_conn_create_wp",
            "pdmid": subscription.site_id,
            "pserv": subscription.type_id,
            "ptmid": subscription.tariff_id,
            "pprop": subscription.attributes,
            "pstatus": subscription.status,
            "pdate": subscription.date or None,
            "premark": subscription.comment or None,
        }
        self._builder.add_dict(option)

    def close(self, opt: dict) -> None:
        """Build soap request to close the agreement."""
        pass

    def index(self, opt: dict) -> None:
        """Build soap request to get list of sites from Agreement."""
        pass

    def build_getter(self, subscription_id: int, property_id: int) -> None:
        """Soap to get additional field."""
        self._builder.add("fun", "o_mdb_api_client_props")
        self._builder.add("clsrv", {"is": subscription_id})
        self._builder.add("property", {"is": property_id})

    def build_setter(self, opt: dict) -> None:
        """Soap to set additional field."""
        self._builder.add(
            "fun", "o_mdb_api_change_connection_upd_property_value"
        )
        self._builder.add("p_clsrv", opt.get("clsrv"))
        self._builder.add("p_prop", opt)

    def get_status(self, subscription_id: int) -> None:
        self._builder.add("fun", "o_mdb_api_get_connection_get_status")
        self._builder.add("pclsrv", subscription_id)

    def set_status(self, subscription_id: int, status: int) -> None:
        self._builder.add("fun", "o_mdb_api_change_connection_set_status")
        self._builder.add("pclsrv", subscription_id)
        self._builder.add("pstatus", status)
