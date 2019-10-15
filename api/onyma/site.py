from . import net
from . import soap


def create(account_number: int, domain_id: int, site_name: str) -> int:
    """Return ID created object."""
    envelope = soap.SoapSite()
    envelope.builder = soap.SoapBuilder()
    envelope.create(account_number, domain_id, site_name)
    request = envelope.builder.request

    try:
        site_id = int(net.receive(request.xml))
    except ValueError:
        site_id = 0
    return site_id
