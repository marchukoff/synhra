from . import net
from . import soap
from datetime import datetime
from typing import NamedTuple


class AddressVector(NamedTuple):
    city: str = "Орёл Г"
    street: str = "8 Марта Ул"
    house: str = "19"
    flat: str = str(datetime.now().day)
    vec_5: str = ""
    vec_6: str = ""
    region: str = "Орловская обл"
    vec_8: str = ""
    vec_9: str = ""
    fias_guid: str = "1a71aac0-2704-43b0-a9b6-21c82060cd20"


def group_to_domain(group_id: int) -> str:
    """Equivalent: return group[:-1] + '0' ."""
    envelope = soap.SoapFunction()
    envelope.builder = soap.SoapBuilder()
    envelope.group_to_domain(group_id)
    request = envelope.builder.request
    return net.receive(request.xml, "return")


def ins_pay(account_number: int, amount: float = 1.5) -> str:
    """Add payment."""
    envelope = soap.SoapFunction()
    envelope.builder = soap.SoapBuilder()
    envelope.ins_pay(account_number, amount)
    request = envelope.builder.request
    return net.receive(request.xml, "return")


def get_vec_id(
    vector: AddressVector = AddressVector(), vector_type: int = 6463
) -> str:
    """Return address vector id."""
    envelope = soap.SoapFunction()
    envelope.builder = soap.SoapBuilder()
    envelope.get_vec_id(vector, vector_type)
    request = envelope.builder.request
    return net.receive(request.xml, "return")
