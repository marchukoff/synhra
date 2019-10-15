# -*- coding: utf-8 -*-

import logging
import re
import xml.dom.minidom
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from builtins import NotImplementedError
from datetime import datetime
from typing import Any, Optional

from api import settings

LOGGER = logging.getLogger("test.%s" % __name__)

namespaces = {
    "xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
    "xmlns:head": "http://www.onyma.ru/services/OnymaApi/heads/",
    "xmlns:fun": "http://www.onyma.ru/services/OnymaApi/funcs/",
}

AUTH = True  # for NoSession API remove credentials


class SoapRequest:
    """SOAP Envelope."""

    def __init__(self) -> None:
        """Initialise an instance with the specified values."""
        self._envelope = ET.Element("soapenv:Envelope", namespaces)
        self._header = ET.SubElement(self._envelope, "soapenv:Header")
        if AUTH:
            self._credentials = ET.SubElement(
                self._header, "head:t_credentials_header"
            )
        self._body = ET.SubElement(self._envelope, "soapenv:Body")

    @property
    def xml(self) -> str:
        """Return property message."""
        dom = xml.dom.minidom.parseString(
            ET.tostring(self._envelope, encoding="UTF-8")
        )
        xml_message = dom.toprettyxml(indent="  ", newl="\n")
        result = xml_message.replace('<?xml version="1.0" ?>\n', "")

        subst = re.compile(r"(<password>)(.*)(</password>)")
        LOGGER.debug("\n%s" % re.sub(subst, r"\1******\3", result))
        return result


class Builder(ABC):
    """Builder interface."""

    @property
    @abstractmethod
    def request(self) -> SoapRequest:
        """Message holder."""
        pass

    @abstractmethod
    def add(self, *args: Any) -> None:
        """Add attribute to soap envelope."""
        pass

    @abstractmethod
    def add_dict(self, params: dict) -> None:
        """Add attribute to soap envelope."""
        pass


class SoapBuilder(Builder):
    """Soap Builder Implementation."""

    _set_fun_attr = set(
        """p_clsrv p_dmid p_no_eps pamount pattr pattrid pattridup pavid
        pccntr pclsrv pcntr pcost pcsid pcurrid pdcost pdescr pdmid pdogcode
        pdogid pdomainid pgid pno_mcost ppaydoc pppid pptmid premark prowid
        pserv pserv_alias pservid psitename pstatus ptdid ptmid putid
        pvec_type utid""".split()
    )
    _set_fun_single_attr = set(
        """id dmid clsrv dogid property enddate""".split()
    )
    _set_fun_double_attr = set(
        """p_comp_attr p_comp_attr_p p_prop pconn pprop""".split()
    )
    _set_fun_date_attr = set(
        """p_date pbdate pbegdate penddate pdate pdogdate pidate pmdate
        pppdate""".split()
    )

    def __init__(self) -> None:
        """Initialise an instance with the specified values."""
        self.reset()

    def reset(self) -> None:
        """Reset."""
        self._message = SoapRequest()

    @property
    def request(self) -> SoapRequest:
        """Return SOAP message."""
        message = self._message
        if AUTH:
            self.add("username", settings.user)
            self.add("password", settings.password)
        self.reset()
        return message

    def _set_fun(self, value: str, tag: str = "<unknown>", root=None) -> None:
        """Create simple element in fun namespace."""
        root = self._fun if root is None else root
        if value is None:
            return
        elif value in ("None", "<unknown>"):
            return
        elif value == tag:
            element = ET.SubElement(root, tag)
        else:
            element = ET.SubElement(root, tag)
            element.text = str(value)

    def _set_credentials(self, value: str, tag: str = "<unknown>") -> None:
        """Create element in credentials namespace."""
        if AUTH:
            self._set_fun(value, tag, self._message._credentials)

    def _set_fun_date(
        self, value: Optional[str], tag="<unknown>", root=None
    ) -> None:
        """Create date element in fun namespace."""
        root = self._fun if root is None else root
        if value is None:
            # Example '2019-05-28T16:11:41'
            value = datetime.now().isoformat(sep="T", timespec="seconds")
        self._set_fun(value, tag, root)

    def _set_fun_single(
        self, opt: dict, tag: str = "<unknown>", root=None
    ) -> None:
        """Create group ATTRIBUTE for single tag in fun namespace.

        <tag>
          <opt_key>opt_value</opt_key>
          . . .
          <opt_key>opt_value</opt_key>
        </tag>
        """
        root = self._fun if root is None else root
        branch = ET.SubElement(root, tag)
        for k, v in opt.items():
            self._set_fun(str(v), k, branch)

    def _set_fun_double(
        self, opt: list, tag: str = "<unknown>", root=None
    ) -> None:
        """Create nested group ATTRIBUTE for single tag in fun namespace.

        <tag>
          <row>
            <opt_key>opt_value</opt_key>
            . . .
            <opt_key>opt_value</opt_key>
          </row>
          . . .
          <row>
            <opt_key>opt_value</opt_key>
            . . .
            <opt_key>opt_value</opt_key>
          </row>
        </tag>
        """
        root = self._fun if root is None else root
        if opt is not None:
            branch = ET.SubElement(self._fun, tag)
            for i in opt:
                self._set_fun_single(i, "row", branch)

    def username(self, value) -> None:
        """Create header attribute: username."""
        self._set_credentials(str(value), "username")

    def password(self, value) -> None:
        """Create header attribute: password."""
        self._set_credentials(str(value), "password")

    def fun(self, value: str) -> None:
        """Create body section: fun."""
        self._fun = ET.SubElement(self._message._body, f"fun:{value}_request")

    def pval(self, value) -> None:
        key = "pval"
        if isinstance(value, list):  # fun == "onyma_uni_api_get_vec_id":
            self._set_fun_double(value, key)
        else:
            self._set_fun(value, key)

    def add(self, key: str, value: Any) -> None:
        """Create attribute."""
        if key in SoapBuilder._set_fun_attr:
            self._set_fun(value, key)
        elif key in SoapBuilder._set_fun_date_attr:
            self._set_fun_date(value, key)
        elif key in SoapBuilder._set_fun_single_attr:
            self._set_fun_single(value, key)
        elif key in SoapBuilder._set_fun_double_attr:
            self._set_fun_double(value, key)
        elif hasattr(self, key):
            getattr(self, key)(value)
        else:
            raise NotImplementedError

    def add_dict(self, params: dict) -> None:
        for k, v in params.items():
            self.add(k, v)

    def __str__(self) -> str:
        """Return soap request as plain text."""
        return self._message.xml
