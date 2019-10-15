# -*- coding: utf-8 -*-

import logging
import time
from datetime import datetime, timedelta
import pytest
from typing import Dict
import api
import filters
import mapping
from .steps import (
    create_subscriptions,
    make_payment,
    setup_address,
    setup_attributes,
    setup_passport,
)

LOGGER = logging.getLogger("test.%s" % __name__)
CRM = api.crm
ONYMA = api.onyma
SUBSCRIPTION: Dict[str, mapping.SiteIndex] = {}


@pytest.fixture(scope="session")
def account() -> api.Account:
    global SUBSCRIPTION
    account_number: int = 0
    account_id = mapping.GUID("")
    trials: int = 5
    waiting_sec: int = 60
    filter_ = filters.crm.CrmFilter()
    date_filter = filters.crm.CrmAgreementDate()
    filter_.set_filter(date_filter)
    today = datetime.now().strftime("%d.%m.%Y")

    for trial in range(trials):
        account_number = int(ONYMA.agreement.create())
        LOGGER.debug(f"Create account {account_number}")
        time.sleep(waiting_sec)
        account_id = CRM.account.get_account_guid_by_number(account_number)
        if account_id:
            created_date = filter_.filtrate(
                "createdon",
                CRM.account.get_attribute(account_id, "createdon"),
            )
            LOGGER.debug(
                f"Today is {today}. Agreement created on {created_date}."
            )
            if created_date in (today, ""):
                break
            else:
                LOGGER.warning(f"I think {account_number} is duplicate.")
                ONYMA.agreement.close(account_number)
                LOGGER.debug(f"Close agreement {account_number}")
                account_number = 0
        else:
            break

    account = api.Account(account_number, account_id)
    if account.number:
        # initialize Agreement
        setup_address(account.number)
        setup_attributes(account.number)
        setup_passport(account.number)
        make_payment(account.number)
        time.sleep(
            120
        )  # чтоб изменения подключек не приходили раньше изменения атрибутов
        SUBSCRIPTION = create_subscriptions(account.number)
    else:
        LOGGER.critical("Cannot create account!")
        raise Exception("Cannot create account!")

    if not account.guid:
        for trial in range(trials):
            LOGGER.info(
                f"Waiting for {waiting_sec}sec to get agreement GUID in CRM."
            )
            time.sleep(waiting_sec)
            account_id = CRM.account.get_account_guid_by_number(
                account.number
            )
            if account_id:
                account = api.Account(account.number, account_id)
                break

    if not account.guid:
        LOGGER.warning(
            f"Cannot get GUID {account.guid} for "
            f"account {account_number} from CRM"
        )
        LOGGER.debug(f"Close agreement {account_number}")
        ONYMA.agreement.close(account.number)
        raise Exception("No agreement for testing.")

    LOGGER.info(
        f"Waiting for {trials * waiting_sec}sec to synchronize "
        f"all attributes and all subscriptions."
    )
    time.sleep(trials * waiting_sec)

    LOGGER.info("*" * 55)
    LOGGER.info("BEGIN TESTING")
    yield account
    LOGGER.info("END TESTING")
    LOGGER.info("*" * 55)

    if account.number:
        date = datetime.now() + timedelta(days=1)
        LOGGER.info(
            f"Close account {account_number} at "
            f'{date.strftime("%d.%m.%Y")}'
        )
        ONYMA.agreement.close(
            account.number, date.isoformat(sep="T", timespec="seconds")
        )


@pytest.fixture(scope="session")
def agreement(account: api.Account) -> mapping.GUID:
    guid = CRM.agreement.get_agreement_guid(account.guid)
    if guid:
        return guid
    else:
        raise Exception("No agreement created in CRM")


@pytest.fixture(scope="session")
def cas(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["cas"].site_id,
        SUBSCRIPTION["cas"].subscriptions[0].subscription_id,
        SUBSCRIPTION["cas"].subscriptions[-1].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["cas"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def ipoe_juniper(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["ipoe_juniper"].site_id,
        SUBSCRIPTION["ipoe_juniper"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["ipoe_juniper"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def ipoe_mac(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["ipoe_mac"].site_id,
        SUBSCRIPTION["ipoe_mac"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["ipoe_mac"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def iptv(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["iptv"].site_id,
        SUBSCRIPTION["iptv"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["iptv"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def juniper_mac(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["juniper_mac"].site_id,
        SUBSCRIPTION["juniper_mac"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["juniper_mac"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def pppoe(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["pppoe"].site_id,
        SUBSCRIPTION["pppoe"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["pppoe"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def lk(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["lk"].site_id,
        SUBSCRIPTION["lk"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["lk"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def qinq(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["qinq"].site_id,
        SUBSCRIPTION["qinq"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["qinq"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def wifi_tv(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["wifi_tv"].site_id,
        # SUBSCRIPTION["wifi_tv"].subscriptions[0].subscription_id,  # skip sale
        SUBSCRIPTION["wifi_tv"].subscriptions[1].subscription_id,
        SUBSCRIPTION["wifi_tv"].subscriptions[2].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["wifi_tv"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def docsis(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["docsis"].site_id,
        SUBSCRIPTION["docsis"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["docsis"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def vps(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["vps"].site_id,
        SUBSCRIPTION["vps"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["vps"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def mobile(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["mobile"].site_id,
        SUBSCRIPTION["mobile"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["mobile"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def rent(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["rent"].site_id,
        SUBSCRIPTION["rent"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["rent"]
    else:
        raise Exception("No subscription created")


@pytest.fixture(scope="session")
def close_juniper_mac(account: api.Account) -> mapping.SiteIndex:
    norm = [
        SUBSCRIPTION["close_juniper_mac"].site_id,
        SUBSCRIPTION["close_juniper_mac"].subscriptions[0].subscription_id,
    ]
    if all(norm):
        return SUBSCRIPTION["close_juniper_mac"]
    else:
        raise Exception("No subscription created")
