from . import net
from . import soap


def get_additional_attribute(account_number: int, attribute_id: int) -> str:
    envelope = soap.SoapAgreementAttributeAdditional()
    envelope.builder = soap.SoapBuilder()
    envelope.build_getter(account_number, attribute_id)
    request = envelope.builder.request
    return net.receive(request.xml, "return")


def set_additional_attribute(
    account_number: int, attribute_id: int, value: str
) -> None:
    envelope = soap.SoapAgreementAttributeAdditional()
    envelope.builder = soap.SoapBuilder()
    envelope.build_setter(account_number, attribute_id, value)
    request = envelope.builder.request
    net.send(request.xml)
