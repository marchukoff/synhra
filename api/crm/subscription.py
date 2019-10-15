from typing import Any, Tuple, NamedTuple

from . import net
from mapping.types import GUID


def get_subscription_guid(subscription_number: int) -> GUID:
    options = {
        "$filter": f"gm_integrationguid eq '{subscription_number}'",
        "$select": "gm_subscriptionid",
    }
    response = net.receive_json("gm_subscriptions", options)
    return GUID(response.get("gm_subscriptionid"))


def get_attribute(subscription_id: GUID, attribute_name: str) -> str:
    url = f"gm_subscriptions({subscription_id})/{attribute_name}/$value"
    return net.receive_text(url)


def set_attribute(
    subscription_id: GUID, attribute_name: str, value: Any
) -> bool:
    body = {attribute_name: value}
    url = f"gm_subscriptions({subscription_id})"
    return net.send(url, body)


class Tariff(NamedTuple):
    """gm_tariffs"""

    name: str = ""  # gm_name
    tariff_id: GUID = GUID("")  # gm_tariffid
    tariff_id_onyma: int = 0  # gm_tariffidentifier
    monthly_payment: float = 0.0  # gm_monthlypayment
    monthly_payment_base: float = 0.0  # gm_monthlypayment_base


def get_tariff(subscription_id: GUID) -> Tariff:
    tariff_id = GUID(
        net.receive_text(
            f"gm_subscriptions({subscription_id})/_gm_tariffid_value/$value"
        )
    )
    assert tariff_id, "Can't get tariff ID"

    name = net.receive_text(f"gm_tariffs({tariff_id})/gm_name/$value")
    try:
        tariff_id_onyma = int(
            net.receive_text(
                f"gm_tariffs({tariff_id})/gm_tariffidentifier/$value"
            )
        )
    except ValueError:
        tariff_id_onyma = 0

    monthly_payment = net.receive_text(
        f"gm_tariffs({tariff_id})/gm_monthlypayment/$value"
    )
    try:
        monthly_payment = float(monthly_payment.replace(",", "."))
    except ValueError:
        monthly_payment = 0.0

    monthly_payment_base = net.receive_text(
        f"gm_tariffs({tariff_id})/gm_monthlypayment_base/$value"
    )
    try:
        monthly_payment_base = float(monthly_payment_base.replace(",", "."))
    except ValueError:
        monthly_payment_base = 0.0

    return Tariff(
        name,
        tariff_id,
        tariff_id_onyma,
        monthly_payment,
        monthly_payment_base,
    )
