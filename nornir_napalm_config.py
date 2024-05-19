# nornir napalm configure script
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")


def configure_ntp(task):
    ntp_config = """
    ntp server 1.1.1.1
    """
    task.run(task=napalm_configure, configuration=ntp_config)


results = nr.run(task=configure_ntp)
print_result(results)
