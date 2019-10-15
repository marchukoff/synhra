# -*- coding: utf-8 -*-

from .builder import Builder


class SoapSite:
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

    def create(
        self, account_number: int, domain_id: int, site_name: str
    ) -> None:
        """Build soap request to create the agreement."""
        option = {
            "fun": "o_mdb_api_change_dog_site_create",
            "psitename": site_name,
            "pdomainid": domain_id,
            "pdogid": account_number,
            "premark": "Auto-test creates this site.",
        }
        self._builder.add_dict(option)

    def close(self, opt: dict) -> None:
        """Build soap request to close the agreement."""
        pass

    def index(self, opt: dict) -> None:
        """Build soap request to get list of sites from Agreement."""
        pass
