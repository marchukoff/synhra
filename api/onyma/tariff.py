from . import net
from . import soap
from .soap import Tariff


def get_tariff_id(site_id: int) -> int:
    """tmid"""
    envelope = soap.SoapTariff()
    envelope.builder = soap.SoapBuilder()
    envelope.build_getter(site_id)
    request = envelope.builder.request
    tmid = net.receive(request.xml, "tmid")

    try:
        result = int(tmid)
    except TypeError:
        result = 0
    return result


def set_tariff(tariff: Tariff) -> None:
    envelope = soap.SoapTariff()
    envelope.builder = soap.SoapBuilder()
    envelope.build_setter(tariff)
    request = envelope.builder.request
    net.send(request.xml)


def get_personal_price(site_id: int) -> float:
    """In CRM: gm_onymapersonalcost"""
    envelope = soap.SoapPriceFactor()
    envelope.builder = soap.SoapBuilder()
    envelope.build_getter(site_id)
    request = envelope.builder.request
    cost = net.receive(request.xml, "cost")
    try:
        result = float(cost)
    except TypeError:
        result = -0.03
    return result


def get_price_factor(site_id: int) -> float:
    """In CRM: gm_additionaldiscount"""
    envelope = soap.SoapPriceFactor()
    envelope.builder = soap.SoapBuilder()
    envelope.build_getter(site_id)
    request = envelope.builder.request
    ccntr = net.receive(request.xml, "ccntr")

    try:
        result = float(ccntr)
    except TypeError:
        result = 0.0
    except ValueError:
        result = 0.0

    return result


def set_price(tariff: Tariff) -> None:
    """
    Args:
        tariff:
             price: Персональная цена (pcost)
             or
             factor: Ценовой коэффициент (pccntr)

    """
    envelope = soap.SoapPriceFactor()
    envelope.builder = soap.SoapBuilder()
    envelope.build_setter(tariff)
    request = envelope.builder.request
    net.send(request.xml)
