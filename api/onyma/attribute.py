from . import net
from . import soap


def get_attribute(account_number: int, attribute_id: str) -> str:
    envelope = soap.SoapAgreementAttribute()
    envelope.builder = soap.SoapBuilder()
    envelope.build_getter(account_number, attribute_id)
    request = envelope.builder.request
    return net.receive(request.xml, "value")


def set_attribute(account_number: int, attribute_id: str, value: str) -> None:
    envelope = soap.SoapAgreementAttribute()
    envelope.builder = soap.SoapBuilder()
    envelope.build_setter(account_number, attribute_id, value)
    request = envelope.builder.request
    net.send(request.xml)
