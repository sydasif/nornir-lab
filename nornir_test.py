from nornir import InitNornir


def say_hello(task):
    print("Hello, Nornir")


nr = InitNornir(config_file="config.yaml")
nr.run(task=say_hello)
