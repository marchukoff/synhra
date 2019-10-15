from typing import Any

from . import net
from mapping.types import GUID


def get_account_guid_by_number(account_number: int) -> GUID:
    options = {
        "$filter": f"accountnumber eq '{account_number}'",
        "$select": "accountid",
    }
    response = net.receive_json("accounts", options)
    return GUID(response.get("accountid"))


def get_attribute(account_id: GUID, attribute_name: str) -> str:
    url = f"accounts({account_id})/{attribute_name}/$value"
    return net.receive_text(url)


def set_attribute(account_id: GUID, attribute_name: str, value: Any) -> bool:
    body = {attribute_name: value}
    url = f"accounts({account_id})"
    return net.send(url, body)
