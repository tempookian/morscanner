"""
collect tools to interact with Morteza's domains
"""
import configparser
import re
import os

import requests

ip_v4_regex = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"

# templates
# vless_ws_template = "vless://{uuid}@{address}:{port}?sni={host}&security=tls&type=ws&path={path}&host={host}#{name}"
templates = dict(
    vless_ws = "vless://{uuid}@{address}:{port}?path={path}&security=tls&encryption=none&alpn=http/1.1&host={host}&type=ws&sni={host}#{name}",
    vless_grpc = "vless://{uuid}@{address}:{port}?mode=gun&security=tls&encryption=none&alpn=h2&type=grpc&serviceName={servicename}&sni={host}#{name}",
    trojan_grpc = "trojan://{password}@{address}:{port}?mode=multi&security=tls&alpn=h2&type=grpc&serviceName={servicename}&sni={host}#{name}"
)


reserved_sections = [
    "filesconfig"
]


def extract_ips(url="http://bot.sudoer.net/best.cf.iran.all"):
    r = requests.get(url)
    ips = re.findall(ip_v4_regex, r.text, re.MULTILINE)
    return ips


def read_config(config_name):
    confs = configparser.ConfigParser()
    confs.read("../config.ini")

    conf_dict = dict(
        confs[config_name]
    )

    return conf_dict


def ip_to_conf(ip: str):
    config = read_config()
    vless_str = vless_ws_template.format(address=ip, **config)
    return vless_str


if __name__ == "__main__":
    ips = extract_ips()
        
    configini = configparser.ConfigParser()
    configini.read("../config.ini")
    for conf_name in configini.sections():
        if conf_name in reserved_sections:
            continue
        conf = dict(configini[conf_name])
        conf["name"] = conf_name
        template = templates[f"{conf['protocol']}_{conf['type']}"]
        this_confs = [template.format(address=ip, **conf) for ip in ips]
        
        writepath = os.path.join(configini["filesconfig"]["outputpath"], conf_name)
        os.makedirs(configini["filesconfig"]["outputpath"], exist_ok=True)
        with open(writepath, "w") as outfile:
            outfile.write("\n".join(this_confs))
