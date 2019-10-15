import json
import logging
import time
from collections import defaultdict
from typing import NamedTuple, Tuple, Dict

import allure

import api
import generator
import mapping

LOGGER = logging.getLogger("test.%s" % __name__)
ONYMA = api.onyma


@allure.step("Заполняем паспортные данные")
def setup_passport(account_number: int) -> None:
    val = generator.Value()
    passport_data = [
        {
            "attrid": mapping.agreement.passport_series.onyma_key,
            "val": val.new_value(mapping.agreement.passport_series.onyma_key),
            "avid": "",
            "pos": mapping.agreement.passport_series.position,
        },
        {
            "attrid": mapping.agreement.passport_number.onyma_key,
            "val": val.new_value(mapping.agreement.passport_number.onyma_key),
            "avid": "",
            "pos": mapping.agreement.passport_number.position,
        },
        {
            "attrid": mapping.agreement.passport_issued_by.onyma_key,
            "val": val.new_value(
                mapping.agreement.passport_issued_by.onyma_key
            ),
            "avid": "",
            "pos": mapping.agreement.passport_issued_by.position,
        },
        {
            "attrid": mapping.agreement.passport_date_of_issue.onyma_key,
            "val": val.new_value(
                mapping.agreement.passport_date_of_issue.onyma_key
            ),
            "avid": "",
            "pos": mapping.agreement.passport_date_of_issue.position,
        },
        {
            "attrid": mapping.agreement.date_of_birth.onyma_key,
            "val": val.new_value(mapping.agreement.date_of_birth.onyma_key),
            "avid": "",
            "pos": mapping.agreement.date_of_birth.position,
        },
        {
            "attrid": mapping.agreement.place_of_birth.onyma_key,
            "val": val.new_value(mapping.agreement.place_of_birth.onyma_key),
            "avid": "",
            "pos": mapping.agreement.place_of_birth.position,
        },
        {
            "attrid": mapping.agreement.passport_subdivision_code.onyma_key,
            "val": val.new_value(
                mapping.agreement.passport_subdivision_code.onyma_key
            ),
            "avid": "",
            "pos": mapping.agreement.passport_subdivision_code.position,
        },
        {
            "attrid": mapping.agreement.registration_address.onyma_key,
            "val": val.new_value(
                mapping.agreement.registration_address.onyma_key
            ),
            "avid": "",
            "pos": mapping.agreement.registration_address.position,
        },
    ]
    pattrid: int = 309
    ONYMA.attribute_additional.set_additional_attribute(
        account_number, pattrid, json.dumps(passport_data)
    )


@allure.step("Заполняем данные договора")
def setup_attributes(account_number: int) -> None:
    class AdditionalArgs(NamedTuple):
        attribute_id: int
        value: str

    data = generator.Value()
    ONYMA.attribute.set_attribute(
        account_number,
        mapping.agreement.credit_schema_id.onyma_key,
        data.new_value(mapping.agreement.credit_schema_id.onyma_key),
    )
    # setup additional attributes
    name = data.new_value(mapping.agreement.name.onyma_key)
    additional = [
        AdditionalArgs(mapping.agreement.name.onyma_key, name),
        AdditionalArgs(
            mapping.agreement.email.onyma_key,
            data.new_value(mapping.agreement.email.onyma_key, name),
        ),
        AdditionalArgs(
            mapping.agreement.additional_email.onyma_key,
            data.new_value(
                mapping.agreement.additional_email.onyma_key, name
            ),
        ),
        AdditionalArgs(
            mapping.agreement.telephone_mobile.onyma_key,
            data.new_value(mapping.agreement.telephone_mobile.onyma_key),
        ),
        AdditionalArgs(
            mapping.agreement.telephone.onyma_key,
            data.new_value(mapping.agreement.telephone.onyma_key),
        ),
        AdditionalArgs(
            mapping.agreement.additional_telephone.onyma_key,
            data.new_value(mapping.agreement.additional_telephone.onyma_key),
        ),
        AdditionalArgs(
            mapping.agreement.number_sms_info.onyma_key,
            data.new_value(mapping.agreement.number_sms_info.onyma_key),
        ),
    ]
    for args in additional:
        ONYMA.attribute_additional.set_additional_attribute(
            account_number, *args
        )


@allure.step("Заполняем адрес")
def setup_address(account_number: int) -> None:
    ONYMA.attribute_additional.set_additional_attribute(
        account_number,
        mapping.agreement.vector.onyma_key,
        ONYMA.function.get_vec_id(),
    )


@allure.step("Проводим платеж для активации договора")
def make_payment(account_number: int) -> None:
    ONYMA.function.ins_pay(account_number, float(str(account_number)[:-3]))


@allure.step("Создаем новое учетное имя")
def create_new_site(
    account_number: int, domain: int, name: str = "new site"
) -> Tuple[int, str]:
    data = generator.Value()
    site_name = data.new_value(
        "site_name", "_".join((str(account_number), name))
    )
    site_id = ONYMA.site.create(account_number, domain, site_name)
    return site_id, site_name


@allure.step('Создаем новое подключение "{name}"')
def create_new_subscription(
    account_number: int,
    domain: int,
    subscription: mapping.subscription.Subscription,
    name: str,
) -> Tuple[int, int]:
    LOGGER.info(f'create subscription "{name}"')
    attributes = generator.SubscriptionAttribute()
    site_id, site_name = create_new_site(
        account_number, domain, subscription.description
    )
    properties = ONYMA.subscription.Subscription(
        site_id,
        subscription.onyma_key,
        subscription.tariff_id,
        attributes.make(subscription),
        mapping.status.active.onyma_id,
    )
    subscription_id = ONYMA.subscription.create(properties)
    attach = {
        "SiteId": site_id,
        "SiteName": site_name,
        "SubscriptionId": subscription_id,
    }
    allure.attach(
        json.dumps(attach), attachment_type=allure.attachment_type.JSON
    )
    return site_id, subscription_id


@allure.step('Создаем подключение "ipoe_juniper"')
def create_subscription_ipoe_juniper(
    account_number: int, domain: int
) -> mapping.SiteIndex:
    site_id, subscription_id = create_new_subscription(
        account_number,
        domain,
        mapping.subscription.ipoe_juniper,
        mapping.subscription.ipoe_juniper.description,
    )
    time.sleep(30)  # это для того, чтобы события не попали в одну пачку!
    # ipoe_juniper: Tariff pers price
    price = ONYMA.tariff.Tariff(
        site_id,
        subscription_id,
        mapping.subscription.Tariff.Wifire_100.value.tmid,
        mapping.subscription.Service.Internet.value.servid,
        100.0,
        0.0,
    )
    ONYMA.tariff.set_price(price)
    return mapping.SiteIndex(
        site_id,
        [
            mapping.SubscriptionId(
                subscription_id, mapping.subscription.ipoe_juniper
            )
        ],
    )


@allure.step('Создаем подключение "juniper_mac"')
def create_subscription_juniper_mac(
    account_number: int, domain: int
) -> mapping.SiteIndex:
    site_id, subscription_id = create_new_subscription(
        account_number,
        domain,
        mapping.subscription.juniper_mac,
        mapping.subscription.juniper_mac.description,
    )
    time.sleep(30)  # это для того, чтобы события не попали в одну пачку!
    # juniper_mac: Tariff price factor
    factor = ONYMA.tariff.Tariff(
        site_id,
        subscription_id,
        mapping.subscription.Tariff.Wifire_100.value.tmid,
        mapping.subscription.Service.Internet.value.servid,
        0.0,
        0.25,
    )
    ONYMA.tariff.set_price(factor)
    return mapping.SiteIndex(
        site_id,
        [
            mapping.SubscriptionId(
                subscription_id, mapping.subscription.juniper_mac
            )
        ],
    )


@allure.step('Создаем подключение "wifi_tv"')
def create_subscription_wifi_tv(
    account_number: int, domain: int
) -> mapping.SiteIndex:
    attributes = generator.SubscriptionAttribute()
    waiting_sec = 120
    prefix = "_".join(
        (
            mapping.subscription.wifi_tv.description,
            mapping.subscription.sale.description,
        )
    )
    site_id, site_name = create_new_site(account_number, domain, prefix)

    properties = ONYMA.subscription.Subscription(
        site_id,
        mapping.subscription.sale.onyma_key,
        mapping.subscription.sale.tariff_id,
        [{}],
        mapping.status.active.onyma_id,
    )
    subscription_sale = ONYMA.subscription.create(properties)
    properties = ONYMA.subscription.Subscription(
        site_id,
        mapping.subscription.wifi_tv.onyma_key,
        mapping.subscription.wifi_tv.tariff_id,
        attributes.make(mapping.subscription.wifi_tv),
        mapping.status.active.onyma_id,
    )
    subscription_wifi_tv_id = ONYMA.subscription.create(properties)
    attach = {
        "SiteId": site_id,
        "SiteName": site_name,
        "SubscriptionId": [subscription_wifi_tv_id, subscription_sale],
    }
    LOGGER.info(f"Waiting for {waiting_sec}sec to get HHID for WiFi TV.")
    time.sleep(waiting_sec)
    try:
        hhid = int(
            ONYMA.subscription.get_property_real(
                subscription_wifi_tv_id, mapping.subscription.hhid.onyma_key
            )
        )
        LOGGER.debug(f"HHID = {hhid}")
    except TypeError:
        LOGGER.error(
            "There is not HHID property in created WiFi TV subscription"
        )
        hhid = 0
    except ValueError:
        LOGGER.error(
            "There is not HHID property in created WiFi TV subscription"
        )
        hhid = 0

    if hhid:
        properties = ONYMA.subscription.Subscription(
            site_id,
            mapping.subscription.wifi_tv_pack.onyma_key,
            mapping.subscription.wifi_tv_pack.tariff_id,
            attributes.make(
                mapping.subscription.wifi_tv_pack,
                opt=[
                    {
                        "prop": mapping.subscription.hhid.onyma_key,
                        "val": hhid,
                        "num": 0,
                    }
                ],
            ),
            mapping.status.active.onyma_id,
        )
        subscription_wifi_tv_pack_id = ONYMA.subscription.create(properties)
        attach["SubscriptionId"].append(subscription_wifi_tv_pack_id)
        allure.attach(
            str(subscription_wifi_tv_pack_id),
            attachment_type=allure.attachment_type.TEXT,
        )
    else:
        subscription_wifi_tv_pack_id = 0

    allure.attach(
        json.dumps(attach), attachment_type=allure.attachment_type.JSON
    )

    return mapping.SiteIndex(
        site_id,
        [
            mapping.SubscriptionId(
                subscription_sale, mapping.subscription.sale
            ),
            mapping.SubscriptionId(
                subscription_wifi_tv_id, mapping.subscription.wifi_tv
            ),
            mapping.SubscriptionId(
                subscription_wifi_tv_pack_id,
                mapping.subscription.wifi_tv_pack,
            ),
        ],
    )


@allure.step('Создаем подключение "cas"')
def create_subscription_cas(
    account_number: int, domain: int
) -> mapping.SiteIndex:
    attributes = generator.SubscriptionAttribute()
    site_id, site_name = create_new_site(
        account_number, domain, mapping.subscription.cas.description
    )
    properties_cas = ONYMA.subscription.Subscription(
        site_id,
        mapping.subscription.cas.onyma_key,
        mapping.subscription.cas.tariff_id,
        attributes.make(mapping.subscription.cas),
        mapping.status.active.onyma_id,
    )
    subscription_cas = ONYMA.subscription.create(properties_cas)
    properties_cas_pack = ONYMA.subscription.Subscription(
        properties_cas.site_id,
        mapping.subscription.cas_pack.onyma_key,
        mapping.subscription.cas_pack.tariff_id,
        properties_cas.attributes,
        properties_cas.status,
    )
    subscription_cas_pack = ONYMA.subscription.create(properties_cas_pack)
    attach = {
        "SiteId": site_id,
        "SiteName": site_name,
        "SubscriptionId": [subscription_cas, subscription_cas_pack],
    }
    allure.attach(
        json.dumps(attach), attachment_type=allure.attachment_type.JSON
    )
    return mapping.SiteIndex(
        site_id,
        [
            mapping.SubscriptionId(
                subscription_cas, mapping.subscription.cas
            ),
            mapping.SubscriptionId(
                subscription_cas_pack, mapping.subscription.cas_pack
            ),
        ],
    )


@allure.step("Создаем подключения")
def create_subscriptions(account_number: int) -> Dict[str, mapping.SiteIndex]:
    """
    :param account_number:
    :return: created subscription map
    """
    new_subscription = defaultdict(
        lambda: mapping.SiteIndex(0, [mapping.SubscriptionId()])
    )
    dog_group = int(
        ONYMA.attribute.get_attribute(
            account_number, mapping.agreement.dog_group_id.onyma_key
        )
    )
    domain = int(ONYMA.function.group_to_domain(dog_group))
    assert domain, "Cannot resolve domain ID!"
    new_subscription["ipoe_juniper"] = create_subscription_ipoe_juniper(
        account_number, domain
    )
    new_subscription["juniper_mac"] = create_subscription_juniper_mac(
        account_number, domain
    )
    new_subscription["wifi_tv"] = create_subscription_wifi_tv(
        account_number, domain
    )
    new_subscription["cas"] = create_subscription_cas(account_number, domain)
    # create other subscriptions
    subscriptions = {
        "close_juniper_mac": mapping.subscription.juniper_mac,
        "docsis": mapping.subscription.docsis,
        "ipoe_mac": mapping.subscription.ipoe_mac,
        "iptv": mapping.subscription.iptv,
        # "juniper_mac": mapping.subscription.juniper_mac,
        "lk": mapping.subscription.lk,
        "mobile": mapping.subscription.mobile,
        "pppoe": mapping.subscription.pppoe,
        "qinq": mapping.subscription.qinq,
        "rent": mapping.subscription.rent,
        "vps": mapping.subscription.vps,
    }
    for subscription_name, subscription in subscriptions.items():
        time.sleep(20)  # waiting for create subscription
        site_id, subscription_id = create_new_subscription(
            account_number, domain, subscription, subscription_name
        )
        new_subscription[subscription_name] = mapping.SiteIndex(
            site_id, [mapping.SubscriptionId(subscription_id, subscription)]
        )
    return new_subscription
