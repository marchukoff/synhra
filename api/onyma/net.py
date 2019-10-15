# -*- coding: utf-8 -*-

import time
import json
import logging
import warnings
import xml.etree.ElementTree as ET
import xml.dom.minidom
from xml.parsers.expat import ExpatError
import requests
from urllib3.exceptions import InsecureRequestWarning

from .. import settings

LOGGER = logging.getLogger("test.%s" % __name__)
warnings.simplefilter("ignore", InsecureRequestWarning)


_headers_onyma = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/71.0.3202.75 Safari/537.36"
    ),
    "Content-Type": "text/xml; charset=UTF-8",
    "SOAPAction": "uri",
    "Connection": "close",
}


def error_handler(fault: ET.Element) -> None:
    fault_tags = [
        "faultcode",
        "faultstring",
        ".//detail/exceptionName",
        ".//detail/code",
    ]
    fault_info = [fault.find(f) for f in fault_tags if fault]
    fault_msg = " | ".join([f.text for f in fault_info if f.text])
    LOGGER.error(fault_msg)


def send(query: str) -> str:
    """Send request to Onyma and return response text."""
    encoded_request = query.encode("utf-8")
    _headers_onyma["Content-Length"] = str(len(encoded_request))

    with requests.Session() as session:
        try:
            response = session.post(
                url=settings.onyma,
                headers=_headers_onyma,
                data=encoded_request,
                verify=False,
                timeout=(10, 30),
            )
        except requests.ConnectionError as e:
            LOGGER.error(str(e))
            raise Exception
        except requests.Timeout as e:
            LOGGER.error(str(e))
            raise Exception
        except requests.RequestException as e:
            LOGGER.error(str(e))
            raise Exception

        assert response.status_code == 200, "Response code is not 200"

        root = ET.fromstring(response.text)
        fault = root.find(
            ".//{http://schemas.xmlsoap.org/soap/envelope/}Fault"
        )
        if fault:
            error_handler(fault)

        try:
            dom = xml.dom.minidom.parseString(
                ET.tostring(root, encoding="UTF-8")
            )
            response_xml = dom.toprettyxml(indent="  ", newl="\n")
        except ExpatError:
            response_xml = ""

        if response_xml:
            LOGGER.debug(f"response\n{response_xml}")
        else:
            LOGGER.debug(response.text)

        return response.text


def receive(query: str, tag: str = "return") -> str:
    """Parse response text and return result as value."""
    ret = ""
    data = send(query)
    root = ET.fromstring(data)

    # second chance to get answer
    for element in root.iter("faultstring"):
        if element.text == "Couldn't open Onyma session":
            time.sleep(10)
            root = ET.fromstring(send(query))

    if tag == "row":
        for element in root.iter("row"):
            row_dict = dict()
            for row in element:
                if row.text is not None:
                    row_dict[row.tag] = row.text
            ret = json.dumps(row_dict)
    else:
        for element in root.iter(tag):
            if element is not None:
                ret = str(element.text)
                break

    LOGGER.debug(ret)
    return ret
