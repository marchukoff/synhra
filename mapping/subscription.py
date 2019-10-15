# -*- coding: utf-8 -*-

import enum
from typing import NamedTuple
from collections import namedtuple


class SubscriptionProperty(NamedTuple):
    onyma_key: int
    crm_key: str
    is_sync: bool
    description: str


incident_number = SubscriptionProperty(
    12681, "incident.Number", True, "Incident Number"
)
vlanperswitch = SubscriptionProperty(9602, "gm_vlanperswitch", False, "VLAN")
pppoelogin = SubscriptionProperty(8041, "gm_pppoelogin", True, "Login")
pppoepassword = SubscriptionProperty(
    8042, "gm_pppoepassword", False, "Password"
)
cabinetlogin = SubscriptionProperty(6961, "gm_cabinetlogin", True, "Login")
cabinetpassword = SubscriptionProperty(
    6962, "gm_cabinetpassword", False, "Password"
)
voipphonenumber = SubscriptionProperty(
    9182, "gm_voipphonenumber", True, "Port"
)
voipstation = SubscriptionProperty(
    9184, "gm_voipstation", True, "VoIP station"
)
stbid = SubscriptionProperty(9321, "gm_stbid", True, "STB ID")
stbmac = SubscriptionProperty(9741, "gm_stbmac", True, "STB MAC")
stbserial = SubscriptionProperty(9742, "gm_stbserial", True, "S/N")
tvdevicetype = SubscriptionProperty(
    9743, "gm_tvdevicetype", True, "TV device type"
)
nasport = SubscriptionProperty(9401, "gm_vpu", True, "NAS-Port-Id")
portnumbervps = SubscriptionProperty(
    9601, "gm_portnumbervps", True, "Номер порта (VPS)"
)
vps_ = SubscriptionProperty(9602, "gm_vps", True, "Vlan")
idnomenclature = SubscriptionProperty(
    12281, "gm_idnomenclature", True, "Nomenclature"
)
name = SubscriptionProperty(9841, "gm_name", True, "Name")
price = SubscriptionProperty(10461, "gm_price", True, "Price")
serialnumber = SubscriptionProperty(9861, "gm_serialnumber", True, "S/N")
ipaddressipoe = SubscriptionProperty(10561, "gm_ipaddressipoe", True, "IP")
macaddressipoe = SubscriptionProperty(10562, "gm_macaddressipoe", True, "MAC")
login = SubscriptionProperty(10624, "gm_login", True, "Login")
password = SubscriptionProperty(10625, "gm_password", False, "Password")
imsi = SubscriptionProperty(10642, "gm_imsi", True, "IMSI")
msisdn = SubscriptionProperty(10641, "gm_msisdn", True, "MSISDN")
hhid = SubscriptionProperty(10623, "gm_hhid", True, "HH ID")
macaddress = SubscriptionProperty(11263, "gm_macaddress", True, "MAC")
routermacaddress = SubscriptionProperty(
    11262, "gm_routermacaddress", True, "MAC"
)
portnumber = SubscriptionProperty(11264, "gm_portnumber", True, "Port")
hhidcas = SubscriptionProperty(11502, "gm_hhidcas", True, "HH ID CAS")
ipaddress = SubscriptionProperty(10141, "gm_ipaddress", True, "IP")
netmask = SubscriptionProperty(10162, "gm_netmask", True, "Mask")
vpu = SubscriptionProperty(9601, "gm_vpu", False, "VPU")
docsismac = SubscriptionProperty(
    10401, "gm_docsismac", True, "Docsis MAC address"
)
logindocsis = SubscriptionProperty(
    10521, "gm_logindocsis", True, "Docsis login"
)
passwordocsis = SubscriptionProperty(
    10522, "gm_passwordocsis", False, "Docsis password"
)


_ = namedtuple("ServiceInfo", "servid description")


class Service(enum.Enum):
    """servid"""

    Internet = _(614, "Абонентская плата за Интернет")


_ = namedtuple("TariffInfo", "tmid description")


class Tariff(enum.Enum):
    """
    Тариф 12146 подходит для
   	IPoE (ISG NEW 2010)  ...  
 	IPoE+MAC  ...  
 	ISG Svoyo подключение  ...  
 	Juniper  ...  
 	Juniper (Framed Route)  ...  
 	Juniper (MAC)  ...  
 	PPPoE  ...  
 	Q-in-Q подключение  ...  
 	vps подключение  ...

    """

    Technological = _(2, "Technological")  # vps ipoe+mac
    IPTV_all_inclusive = _(3847, "IPTV Все включено (Орел)")
    Wifire_tv_pack_HD = _(5731, "Wifire TV Пакет HD")
    Wifire_100 = _(5942, "Wifire 100")
    Wifire_tv_90 = _(7422, "Wifire TV 90+")
    VoIP = _(8109, "VoIP Комбинированный-350(Орел)(ЮЛ)")
    CAS = _(8169, "CAS Телемикс")  # old: _(8167, "CAS Мультиплекс")
    CAS_pack = _(8180, "CAS - Пакет Дождь")
    Rent = _(9083, "Аренда приставки (169 р.)")
    Docsis = _(10572, "L (inet) (Docsis) (Сургут)")
    LTE = _(
        11451, "Wifire Mobile 1 ГБ Triple monthly"
    )  # old: _(11671, "Эксклюзивный Mobile dual (Unlim)")
    Wifire_100_120 = _(12146, "Включайся с Wifire 100/120+ Пакет")
    Sale = _(12253, "ТВ-приставка рассрочка 36 мес (Рассрочка)(ITINIT-2606)")


class Subscription(NamedTuple):
    description: str
    onyma_key: int
    tariff_id: int
    properties: list


pppoe = Subscription(
    "PPPoE", 6281, Tariff.Wifire_100.value.tmid, [pppoelogin, pppoepassword]
)
lk = Subscription(
    "Личный кабинет",
    7401,
    Tariff.Technological.value.tmid,
    [cabinetlogin, cabinetpassword],
)
voip = Subscription(
    "VoIP", 7501, Tariff.VoIP.value.tmid, [voipstation, voipphonenumber]
)
iptv = Subscription(
    "IPTV",
    7601,
    Tariff.IPTV_all_inclusive.value.tmid,
    [stbid, stbmac, stbserial, tvdevicetype],
)
qinq = Subscription(
    "Q-in-Q", 7741, Tariff.Wifire_100_120.value.tmid, [nasport]
)
vps = Subscription(
    "VPS", 7861, Tariff.Wifire_100_120.value.tmid, [portnumbervps, vps_]
)
sale = Subscription("Продажа оборудования", 8021, Tariff.Sale.value.tmid, [])
docsis = Subscription(
    "Docsis",
    8341,
    Tariff.Docsis.value.tmid,
    [docsismac, logindocsis, passwordocsis],
)
ipoe_mac = Subscription(
    "IPoE MAC",
    8361,
    Tariff.Wifire_100_120.value.tmid,
    [ipaddressipoe, macaddressipoe],
)
wifi_tv = Subscription(
    "WiFi TV", 8381, Tariff.Wifire_tv_90.value.tmid, [login, password]
)
lte = Subscription("LTE", 8401, Tariff.LTE.value.tmid, [imsi, msisdn])
wifi_tv_pack = Subscription(
    "WiFi TV пакет", 8421, Tariff.Wifire_tv_pack_HD.value.tmid, [hhid]
)
ipoe_juniper = Subscription(
    "Juniper (IPoE Juniper)",
    8801,
    Tariff.Wifire_100.value.tmid,
    [routermacaddress, macaddress, portnumber],
)
cas = Subscription("CAS", 8921, Tariff.CAS.value.tmid, [hhidcas])
cas_pack = Subscription(
    "CAS пакет", 8941, Tariff.CAS_pack.value.tmid, [hhidcas]
)
juniper_mac = Subscription(
    "Juniper MAC",
    9361,
    Tariff.Wifire_100.value.tmid,
    [ipaddress, netmask, macaddress],
)
mobile = Subscription("Mobile", 8401, Tariff.LTE.value.tmid, [msisdn, imsi])
rent = Subscription(
    "Аренда оборудования", 8041, Tariff.Rent.value.tmid, [serialnumber]
)
