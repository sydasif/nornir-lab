from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result


def set_ntp(task):
    ntp_server = task.host["ntp"]
    task.run(task=netmiko_send_config, config_commands=[f"ntp server {ntp_server}"])


nr = InitNornir(config_file="config.yaml")
nr = nr.filter(hostname="172.16.10.12")

results = nr.run(task=set_ntp)
print_result(results)
