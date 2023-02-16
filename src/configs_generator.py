"""
collect tools to interact with Morteza's domains
"""
import configparser
import re

import requests

ip_v4_regex = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
vless_template = "vless://{uuid}@{address}:{port}?sni={host}&security=tls&type=ws&path={path}&host={host}#{name}"


def extract_ips(url="http://bot.sudoer.net/best.cf.iran.all"):
    r = requests.get(url)
    ips = re.findall(ip_v4_regex, r.text, re.MULTILINE)
    return ips


def read_config(config_name="baseconfig"):
    conf = configparser.ConfigParser()
    conf.read("../config.ini")
    name = conf[config_name]["name"]
    uuid = conf[config_name]["uuid"]
    path = conf[config_name]["path"]
    host = conf[config_name]["host"]
    port = conf[config_name]["port"]

    conf_dict = dict(
        name=name,
        uuid=uuid,
        path=path,
        host=host,
        port=port
    )

    return conf_dict


def ip_to_conf(ip: str):
    config = read_config()
    vless_str = vless_template.format(address=ip, **config)
    return vless_str


if __name__ == "__main__":
    ips = extract_ips()
    configs = [ip_to_conf(ip) for ip in ips]

    with open("/tmp/results.conf", "w") as outf:
        outf.write("\n".join(configs))
