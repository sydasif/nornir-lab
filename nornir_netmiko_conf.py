# nornir config cmd script
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result


nr = InitNornir(config_file="config.yaml")
nr = nr.filter(hostname="172.16.10.12")
results = nr.run(task=netmiko_send_config, config_commands=["ntp server 1.1.1.1"])
print_result(results)
