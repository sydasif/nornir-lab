from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result


def get_facts(task):
    task.run(task=napalm_get, getters=["facts"])


nr = InitNornir(config_file="config.yaml")
result = nr.run(task=get_facts)
print_result(result)
