# nornir napalm get interfaces ip script
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")

results = nr.run(task=napalm_get, getters=["interfaces_ip"])
print_result(results)
