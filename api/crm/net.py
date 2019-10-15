# -*- coding: utf-8 -*-

import logging
import warnings
from urllib import parse
import requests
from requests_ntlm import HttpNtlmAuth
from urllib3.exceptions import InsecureRequestWarning

from .. import settings

warnings.simplefilter("ignore", InsecureRequestWarning)

LOGGER = logging.getLogger("test.%s" % __name__)
AUTH = HttpNtlmAuth(f"NBNH\\{settings.user}", settings.password)
TIMEOUT = 10, 10
HEADERS_GET = {
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/71.0.3202.75 Safari/537.36"
    ),
    "OData-MaxVersion": "4.0",
    "connection": "close",
}
HEADERS_PATCH = {
    "OData-MaxVersion": "4.0",
    "Content-Type": "application/json;odata.metadata=minimal",
    "connection": "close",
}


def send(url_suffix: str, parameters: dict = {}) -> bool:
    url = f"{settings.crm}/{url_suffix}"
    try:
        response = requests.patch(
            url,
            json=parameters,
            auth=AUTH,
            headers=HEADERS_PATCH,
            timeout=TIMEOUT,
            verify=False,
        )
        return response.ok
        # response.encoding = "win-1251"
    except requests.ConnectionError as e:
        LOGGER.error(str(e))
        raise Exception
    except requests.Timeout as e:
        LOGGER.error(str(e))
        raise Exception
    except requests.RequestException as e:
        LOGGER.error(str(e))
        raise Exception


def _send(url_suffix: str, parameters: dict = {}) -> requests.Response:
    url = f"{settings.crm}/{url_suffix}"
    try:
        with requests.Session() as session:
            return session.get(
                url,
                params=parameters,
                auth=AUTH,
                headers=HEADERS_GET,
                timeout=TIMEOUT,
                verify=False,
            )
        # response.encoding = "win-1251"
    except requests.ConnectionError as e:
        LOGGER.error(str(e))
        raise Exception
    except requests.Timeout as e:
        LOGGER.error(str(e))
        raise Exception
    except requests.RequestException as e:
        LOGGER.error(str(e))
        raise Exception


def receive_json(url_suffix: str, parameters: dict) -> dict:
    result = {}
    response = _send(url_suffix, parameters)
    if response.ok:
        response_json = response.json()
        try:
            result = response_json["value"][0]
        except IndexError:
            pass
        except KeyError:
            pass

    LOGGER.info(parse.unquote(response.url))
    LOGGER.debug(str(result))
    return result


def receive_text(url_suffix: str) -> str:
    result: str = ""
    response = _send(url_suffix)

    if response.ok:
        response.encoding = "utf-8-sig"  # "win-1251"
        result = response.text

    LOGGER.info(parse.unquote(response.url))
    LOGGER.debug(result)
    return result
