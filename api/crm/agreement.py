from typing import Any

from . import net
from mapping.types import GUID


def get_agreement_guid(account_id: GUID) -> GUID:
    url = f"accounts({account_id})/_gm_agreementid_value/$value"
    return GUID(net.receive_text(url))


def get_attribute(agreement_id: GUID, attribute_name: str) -> str:
    url = f"gm_agreements({agreement_id})/{attribute_name}/$value"
    return net.receive_text(url)


def set_attribute(
    agreement_id: GUID, attribute_name: str, value: Any
) -> bool:
    body = {attribute_name: value}
    url = f"gm_agreements({agreement_id})"
    return net.send(url, body)
