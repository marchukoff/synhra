# -*- coding: utf-8 -*-

from typing import Optional
from . import net
from . import soap


def create() -> int:
    """Create agreement and return account number."""
    envelope = soap.SoapAgreement()
    envelope.builder = soap.SoapBuilder()
    envelope.create()
    request = envelope.builder.request

    try:
        account_number = int(net.receive(request.xml))
    except ValueError:
        account_number = 0

    return account_number


def close(account_number: int, date: Optional[str] = None) -> None:
    """
    Args:
        account_number (int): existing account number
        date (str): date in iso format like '2019-05-28T16:11:41'
    """
    envelope = soap.SoapAgreement()
    envelope.builder = soap.SoapBuilder()
    envelope.close(account_number, date)
    request = envelope.builder.request
    net.send(request.xml)
