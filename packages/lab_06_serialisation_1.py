from __future__ import annotations

import typing

import yaml

if __name__ == "__main__":
    with open("ipconfig.yaml") as f:
        data = yaml.safe_load(f)

    for value in typing.cast(typing.Dict, data["network"]["ethernets"]).values():
        addresses: typing.List = value["nameservers"]["addresses"]
        i = addresses.index("192.168.1.1")
        addresses[i] = "8.8.8.8"

    # print(yaml.dump(data))

    with open("ipconfig.yaml", "w") as f:
        yaml.dump(data, f)
