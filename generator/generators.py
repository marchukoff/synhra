# -*- coding: utf-8 -*-
"""This module provide values generator for changing ATTRIBUTE."""

import logging
import random
import re
import string
from datetime import datetime, timedelta
from time import time, time_ns
from typing import Optional

from transliterate import exceptions, translit

import mapping

LOGGER = logging.getLogger("test.%s" % __name__)


def generate_hhid(hhid="") -> str:
    return str(int(time()))[:9]


def generate_ipv4(a: int = 0, b: int = 0, c: int = 0, d: int = 0) -> str:
    """Return formatted IP v4 address like 192.168.0.1."""
    a = random.randint(1, 254) if not a else a
    b = random.randint(0, 254) if not b else b
    c = random.randint(0, 254) if not c else c
    d = random.randint(1, 254) if not d else d
    return ".".join(map(str, (a, b, c, d)))


def generate_netmask(a: int = 0, b: int = 0, c: int = 0, d: int = 0) -> str:
    return "255.255.255.255"


def generate_vps() -> str:
    address = [str(random.randint(0, 9)) for _ in range(3)]
    address.append(
        ".".join([str(random.randint(1000, 1999)) for _ in range(2)])
    )
    return "/".join(address)


def generate_mac_onyma() -> str:
    """Return formatted MAC like 288b.b276.3dfa."""
    return ".".join(
        [
            "".join([f"{random.randint(0, 255):02x}" for i in range(2)])
            for i in range(3)
        ]
    )


def generate_mac_docsis() -> str:
    return "".join(
        [f"{random.randint(0, 255):02x}" for i in range(6)]
    ).upper()


def generate_password(length: int = 8) -> str:
    """Return password."""
    symbols = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789"
    ret = "".join(random.sample(symbols, length))
    LOGGER.debug(ret)
    return ret


def multi_password(count: int = 1, length: int = 8) -> set:
    """Return set of passwords with defined length."""
    a: set = set()
    while len(a) < count:
        a.add(generate_password(length))
    LOGGER.debug(", ".join(map(str, (count, length))))
    LOGGER.debug(a)
    return a


def generate_name(sex: Optional[str] = None) -> str:
    """Return abstract person name."""
    consonant = set("бвгджзклмнпрстфхцчшщ")
    vowel = set("ауоыиэяюёе")
    names = {
        "Male_1st": [
            "Александр",
            "Алексей",
            "Альберт",
            "Артём",
            "Борис",
            "Вадим",
            "Валентин",
            "Виктор",
            "Владимир",
            "Герман",
            "Денис",
            "Дмитрий",
            "Егор",
            "Иван",
            "Кирилл",
            "Константин",
            "Леонид",
            "Макар",
            "Максим",
            "Матвей",
            "Никита",
            "Олег",
            "Оскар",
            "Павел",
            "Пётр",
            "Роман",
            "Рудольф",
            "Сергей",
            "Станислав",
            "Хаматнур",
            "Харитон",
            "Эдуард",
        ]
    }
    names["Male_2nd"] = [
        i.replace("ё", "е") + "ович"
        for i in names["Male_1st"]
        if i[-1] in consonant
    ]
    names["Male_2nd"].extend(
        [i[:-1] + "ич" for i in names["Male_1st"] if i[-1] in vowel]
    )
    names["Male_2nd"].extend(
        [i[:-1] + "евич" for i in names["Male_1st"] if i[-1] in {"ь", "й"}]
    )
    names["Female_2nd"] = [
        i.replace("ё", "е") + "овна"
        for i in names["Male_1st"]
        if i[-1] in consonant
    ]
    names["Female_2nd"].extend(
        [i[:-1] + "евна" for i in names["Male_1st"] if i[-1] in {"ь", "й"}]
    )
    names["Female_2nd"].extend(
        [i[:-1] + "ична" for i in names["Male_1st"] if i[-1] in vowel]
    )
    names.update(
        {
            "Male_3rd": [
                "Иванов",
                "Смирнов",
                "Кузнецов",
                "Попов",
                "Васильев",
                "Петров",
                "Соколов",
                "Михайлов",
                "Новиков",
                "Федоров",
                "Морозов",
                "Волков",
                "Алексеев",
                "Лебедев",
                "Семенов",
                "Егоров",
                "Павлов",
                "Козлов",
                "Степанов",
                "Николаев",
                "Орлов",
                "Андреев",
                "Макаров",
                "Никитин",
                "Захаров",
                "Зайцев",
                "Соловьев",
                "Борисов",
                "Яковлев",
                "Григорьев",
                "Романов",
                "Воробьев",
                "Сергеев",
                "Кузьмин",
                "Фролов",
                "Александров",
                "Дмитриев",
                "Королев",
                "Гусев",
                "Киселев",
                "Ильин",
                "Максимов",
                "Поляков",
                "Сорокин",
                "Виноградов",
                "Ковалев",
                "Белов",
                "Медведев",
                "Антонов",
                "Тарасов",
                "Жуков",
                "Баранов",
                "Филиппов",
                "Комаров",
                "Давыдов",
                "Беляев",
                "Герасимов",
                "Богданов",
                "Осипов",
                "Сидоров",
                "Матвеев",
                "Титов",
                "Марков",
                "Миронов",
                "Крылов",
                "Куликов",
                "Карпов",
                "Власов",
                "Мельников",
                "Денисов",
                "Гаврилов",
                "Тихонов",
                "Казаков",
                "Афанасьев",
                "Данилов",
                "Савельев",
                "Тимофеев",
                "Фомин",
                "Чернов",
                "Абрамов",
                "Мартынов",
                "Ефимов",
                "Федотов",
                "Щербаков",
                "Назаров",
                "Калинин",
                "Исаев",
                "Чернышев",
                "Быков",
                "Маслов",
                "Родионов",
                "Коновалов",
                "Лазарев",
                "Воронин",
                "Климов",
                "Филатов",
                "Пономарев",
                "Голубев",
                "Кудрявцев",
            ],
            "Female_1st": [
                "Алёна",
                "Анастасия",
                "Анна",
                "Вера",
                "Вероника",
                "Виктория",
                "Екатерина",
                "Елена",
                "Ирина",
                "Катерина",
                "Ксения",
                "Лариса",
                "Любовь",
                "Людмила",
                "Марина",
                "Мария",
                "Надежда",
                "Наталья",
                "Нина",
                "Оксана",
                "Ольга",
                "Светлана",
                "Татьяна",
                "Эльвира",
                "Юлия",
            ],
        }
    )
    names["Female_3rd"] = [i + "а" for i in names["Male_3rd"]]
    variants = ["male", "female"]
    sex = sex if sex in variants else random.choice(variants)
    if sex == "male":
        slice_ = (names["Male_3rd"], names["Male_1st"], names["Male_2nd"])
    else:
        slice_ = (
            names["Female_3rd"],
            names["Female_1st"],
            names["Female_2nd"],
        )

    name = " ".join([random.choice(i) for i in slice_])
    LOGGER.debug(sex)
    LOGGER.debug(name)
    return name


def change_last_symbol(param: str) -> str:
    """Return param with changed last symbol."""
    ret = param
    if ret.isdigit:
        while param == ret:
            ret = "".join((param[0:-1], random.choice(string.digits)))
    elif all(i in string.hexdigits for i in ret):
        while param == ret:
            ret = "".join((param[0:-1], random.choice(string.hexdigits)))
    else:
        while param == ret:
            ret = "".join(
                (param[0:-1], random.choice(string.ascii_lowercase))
            )
    LOGGER.debug(param)
    LOGGER.debug(ret)
    return str(ret)


def _variant(variant: Optional[str], variants: set, default: str = "") -> str:
    """Return random value from arg sequence."""
    if variant in variants:
        variants -= {variant}
        ret = random.choice(list(variants))
    elif variant not in variants:
        ret = default

    if not ret:
        ret = random.choice(list(variants))

    return ret


def name(sex: Optional[str] = None) -> str:
    """Return random name."""
    return generate_name(sex)


def email(name: Optional[str] = None) -> str:
    """Return email."""
    mail_domains = (
        "mail.ru",
        "list.ru",
        "yandex.ru",
        "rambler.ru",
        "google.com",
        "outlook.com",
        "hotmail.com",
        "live.com",
        "ukr.net",
        "yahoo.com",
    )
    if name:
        try:
            name_user = translit(name, "ru", reversed=True)
            name_user = name_user.translate(str.maketrans(" ", ".", "'"))
        except exceptions.LanguageDetectionError:
            name_user = str(int(time() * 1000))

    name_domain = random.choice(mail_domains)
    email = "@".join([name_user, name_domain])
    return email


def telephone(arg: Optional[str] = None) -> str:
    """Return phone number."""
    return "89" + "".join(random.choices(string.digits, k=9))


def sms_telephone(arg: Optional[str] = None) -> str:
    """Return SMS phone number."""
    return "9" + "".join(random.choices(string.digits, k=9))


def passport_series(arg: Optional[str] = None) -> str:
    """Return Passport series."""
    return f"{random.randint(1, 9999):04d}"


def passport_number(arg: Optional[str] = None) -> str:
    """Return Passport number."""
    return f"{random.randint(1, 999999):06d}"


def passport_place_of_birth(arg: Optional[str] = None) -> str:
    """Return Place Of Birth."""
    return random.choice(
        ("Москва", "Санкт-Петербург", "Воронеж", "Фергана", "Астана")
    )


def passport_subdivision(arg: Optional[str] = None) -> str:
    """Return Passport Subdivision Code."""
    return f"{random.randint(1, 999):03d}-{random.randint(1, 99):03d}"


def passport_issued_by(arg: Optional[str] = None) -> str:
    """Return Passport Issued By."""
    return random.choice(("ПВС МВД", "УВД", "ГУВД", "ФМС", "УФМС"))


def passport_birthdate(arg: Optional[str] = None) -> str:
    """Return Date OfBirth."""
    age = random.randint(14, 45)
    date_of_birth = (
        f"{random.randint(1, 28):02d}."
        f"{random.randint(1, 12):02d}."
        f"{datetime.now().year - age}"
        "T12:00:00"
    )
    return date_of_birth


def passport_issued(arg: Optional[str] = None) -> str:
    """Return Passport Date Of Issue."""
    shift = random.randint(1, 5)
    date_of_issue = (
        f"{random.randint(1, 28):02d}."
        f"{random.randint(1, 12):02d}."
        f"{datetime.now().year - shift}"
        "T12:00:00"
    )
    return date_of_issue


def passport_address(arg: Optional[str] = None) -> str:
    """Return Registration Address."""
    return f"Орел, ул. 8 Марта, 19, {datetime.now().day}"


def dog_date(arg: Optional[str] = None) -> str:
    """Return Dog Date."""
    try:
        datetime_object1 = datetime.strptime(  # type: ignore
            arg, "%Y-%m-%dT%H:%M:%S"
        )
        datetime_object2 = datetime_object1 + timedelta(
            minutes=random.randint(-10, 10)
        )
    except ValueError:
        datetime_object1 = datetime.now()
        datetime_object2 = datetime_object1 - timedelta(
            days=random.randint(5, 10)
        )
    return datetime_object2.isoformat(sep="T")


def status(arg: Optional[str] = None) -> str:
    """Return status."""
    status_old = arg
    status_pool = {
        str(mapping.status.active.onyma),  # type: ignore
        str(mapping.status.paused_by_operator.onyma),  # type: ignore
    }
    default = str(mapping.status.active.onyma)  # type: ignore
    return _variant(status_old, status_pool, default)


def credit_schema(arg: Optional[str] = None) -> str:
    """Return phone number."""
    # 48 - Кредит
    # 49 - Предоплата
    # 77 - Кредит 50 дней
    # 96 - Кредит 20 дней
    return _variant(arg, {"48", "49", "77", "96"}, "48")


def agreement_type(arg: Optional[str] = None) -> str:
    """Return agreement type."""
    # 12 - Юридическое лицо
    # 13 - Физическое лицо
    # 39 - Служебный
    # 42 - Конвергентный
    return _variant(arg, {"12", "13", "39", "42"}, "39")


def gid(arg: Optional[str] = None) -> str:
    """Return agreement type."""
    # 11991 - inetera.Orel
    # 19271 - inetera.Mcensk
    # 23151 - inetera.Znamenka_Orel
    return _variant(arg, {"11991", "19271", "23151"}, "11991")


def site(arg: Optional[str] = None) -> str:
    """Return site name.

    Название учетного имени может иметь длину от 3 до 100 символов и
    должно состоять только из строчных букв латинского алфавита,
    арабских цифр и символов ~=.#$+_ -
    """
    arg_formatted = translit(arg, "ru", reversed=True).lower()
    technology_name = re.sub(r"[^\w\d]", "_", arg_formatted)
    return "-".join((technology_name, str(time_ns())[-6:]))


def fias(arg: Optional[str] = None) -> str:
    """Return fias guid."""
    default = "15fcddd7-a515-468b-85c8-ecb1f4a78239"
    fias = {
        "15fcddd7-a515-468b-85c8-ecb1f4a78239",
        "07349b4a-bff7-494a-b423-8f2d45ad8a92",
        "7e5b1b84-8596-43a3-8d02-e07ccb4bf402",
    }
    return _variant(arg, fias, default)


def get_vec(arg: Optional[str] = None) -> str:
    """Return address vector id."""
    return ""


def prop(arg) -> list:
    """Return tariff."""
    pprop = {
        8801: [
            {"prop": 11263, "val": generate_mac_onyma(), "num": 0},
            {"prop": 11264, "val": random.randint(1, 20), "num": 0},
        ]
    }
    return pprop  # type: ignore


def nasport(arg: Optional[str] = None) -> str:
    return f"9/0/0/1472.4{random.randint(10, 99)}"  # 0/0/0/1472.413
