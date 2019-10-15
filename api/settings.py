import os
import json

config_file = os.path.join(os.path.dirname(__file__), "settings.json")
crm = "127.0.0.1"
onyma = "127.0.0.1"
password = "password"
user = "user"


def _init():
    global crm
    global onyma
    global password
    global user

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {
            "crm": crm,
            "onyma": onyma,
            "password": password,
            "user": user,
        }
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        exit(0)
    else:
        crm = config["crm"]
        onyma = config["onyma"]
        password = config["password"]
        user = config["user"]


_init()
