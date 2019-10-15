# -*- coding: utf-8 -*-

import random
from time import time
from typing import Dict, Callable

import mapping
from . import generators


class SubscriptionAttribute:
    """Make subscription_old properties."""

    _msisdn = f"9{random.randint(100000000, 800000000)}"
    _func: Dict[int, Callable] = {
        mapping.subscription.cabinetlogin.onyma_key: lambda: str(
            int(time() * 1000)
        ),
        mapping.subscription.cabinetpassword.onyma_key: generators.generate_password,
        mapping.subscription.hhidcas.onyma_key: lambda: "".join(
            ("0", str(int(time())))
        ),  # 11502
        # interra.Orel 46, 72, 127 (создали новый блок)
        mapping.subscription.ipaddress.onyma_key: lambda: generators.generate_ipv4(
            192
        ),
        # interra.Orel 46, 72, 127 (создали новый блок)
        mapping.subscription.ipaddressipoe.onyma_key: lambda: generators.generate_ipv4(
            192
        ),
        mapping.subscription.login.onyma_key: lambda: str(int(time()))[:8],
        mapping.subscription.macaddress.onyma_key: generators.generate_mac_onyma,
        mapping.subscription.macaddressipoe.onyma_key: generators.generate_mac_onyma,
        mapping.subscription.nasport.onyma_key: generators.nasport,
        mapping.subscription.netmask.onyma_key: generators.generate_netmask,
        mapping.subscription.password.onyma_key: lambda: str(int(time()))[:8],
        mapping.subscription.portnumber.onyma_key: lambda: str(
            random.randint(1, 20)
        ),
        mapping.subscription.pppoelogin.onyma_key: lambda: str(
            int(time() * 1000)
        ),
        mapping.subscription.pppoepassword.onyma_key: generators.generate_password,
        mapping.subscription.routermacaddress.onyma_key: generators.generate_mac_onyma,
        mapping.subscription.stbid.onyma_key: lambda: str(
            random.randint(50000, 69999)
        ),
        mapping.subscription.stbmac.onyma_key: generators.generate_mac_onyma,
        mapping.subscription.stbserial.onyma_key: lambda: f"E01510D003{random.randint(1000, 9000)}",
        mapping.subscription.tvdevicetype.onyma_key: lambda: "HZ",
        mapping.subscription.docsismac.onyma_key: generators.generate_mac_docsis,
        mapping.subscription.logindocsis.onyma_key: lambda: f"demo_{random.randint(1, 9999)}",
        mapping.subscription.passwordocsis.onyma_key: generators.generate_password,
        mapping.subscription.portnumbervps.onyma_key: lambda: f"{random.randint(0, 255):02x}",
        mapping.subscription.vps_.onyma_key: generators.generate_vps,
        mapping.subscription.msisdn.onyma_key: lambda: SubscriptionAttribute._msisdn,
        mapping.subscription.imsi.onyma_key: lambda: f"25002{SubscriptionAttribute._msisdn}",
        mapping.subscription.serialnumber.onyma_key: lambda: f"AIPHNCZAA{random.randint(100000000, 999999999)}",
        mapping.subscription.hhid.onyma_key: generators.generate_hhid,
    }

    def __init__(self, opt: dict = {}):
        if opt:
            self._options = dict(opt)
        else:
            self._options: dict = {}

    def make(
        self, subscription: mapping.subscription.Subscription, opt: list = []
    ) -> list:
        if opt:
            return opt
        else:
            pprop: list = []
            for property_ in subscription.properties:
                onyma, crm, is_sync, description = property_
                func = self._func.get(onyma)
                assert (
                    func is not None
                ), "There is no function to new_value value."
                prop = {"prop": onyma, "num": 0, "val": func()}
                pprop.append(prop)
            return pprop
