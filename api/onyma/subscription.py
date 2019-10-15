import json
from typing import NamedTuple

from . import net
from . import soap


class Subscription(NamedTuple):
    site_id: int
    type_id: int
    tariff_id: int
    attributes: list
    status: int
    date: str = ""
    comment: str = ""


def create(subscription: Subscription) -> int:
    envelope = soap.SoapSubscription()
    envelope.builder = soap.SoapBuilder()
    envelope.create(subscription)
    request = envelope.builder.request

    try:
        subscription_id = int(net.receive(request.xml))
    except ValueError:
        subscription_id = 0

    return subscription_id


def get_property_set(subscription_id: int, property_id: int) -> str:
    envelope = soap.SoapSubscription()
    envelope.builder = soap.SoapBuilder()
    envelope.build_getter(subscription_id, property_id)
    request = envelope.builder.request
    return net.receive(request.xml, "row")


def get_property(subscription_id: int, property_id: int) -> str:
    envelope = soap.SoapSubscription()
    envelope.builder = soap.SoapBuilder()
    envelope.build_getter(subscription_id, property_id)
    request = envelope.builder.request
    return net.receive(request.xml, "value")


def get_property_real(subscription_id: int, property_id: int) -> str:
    envelope = soap.SoapSubscription()
    envelope.builder = soap.SoapBuilder()
    envelope.build_getter(subscription_id, property_id)
    request = envelope.builder.request
    return net.receive(request.xml, "real_value")


def get_property_json(subscription_id: int, property_id: int) -> str:
    pass  # TODO see get_property above


def set_property(subscription_id: int, property_id: int, value: str) -> None:
    try:
        params: dict = json.loads(
            get_property_json(subscription_id, property_id)
        )
    except TypeError:
        return
    params["real_value"] = value
    envelope = soap.SoapSubscription()
    envelope.builder = soap.SoapBuilder()
    envelope.build_setter(params)
    request = envelope.builder.request
    net.send(request.xml)


def get_status(subscription_id: int) -> str:
    envelope = soap.SoapSubscription()
    envelope.builder = soap.SoapBuilder()
    envelope.get_status(subscription_id)
    request = envelope.builder.request
    return net.receive(request.xml, "return")


def set_status(subscription_id: int, status: int) -> str:
    envelope = soap.SoapSubscription()
    envelope.builder = soap.SoapBuilder()
    envelope.set_status(subscription_id, status)
    request = envelope.builder.request
    return net.send(request.xml)
