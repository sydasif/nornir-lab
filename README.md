# Nornir - Python Network Automation

Nornir is a Python library designed for network automation tasks. It allows Network Engineers to manage and automate their network devices using Python. Unlike tools like Ansible that use domain-specific languages, Nornir leverages the full power of Python, providing more flexibility and control over your automation scripts.

If you're familiar with Ansible, you know that you first set up your inventory, write tasks, and then execute them on all or selected devices concurrently. Nornir works similarly, but the key difference is that you use Python code instead of a domain-specific language.

### Prerequisites and Key Points

Before diving into Nornir, you should have a good understanding of Python basics. If you're new to Python, check out my [Python Book](https://asifsyd.gumroad.com/l/tjoza) to build a solid foundation.

Remember, Nornir isn't meant to replace tools like Netmiko or Napalm; it's designed to work alongside them. Think of Nornir as a framework that organizes your automation tasks. For example, to SSH into network devices, you'll still use plugins like Netmiko. We'll cover how these tools integrate with Nornir in the upcoming sections.

Installing Nornir is easy. Just run the following `pip` install command:

```bash
pip install nornir
```

## Nornir Introduction

Here’s a quick overview of the main components of Nornir. Together, these elements create a powerful framework for network automation.

- **Inventory**: This is where you store information about your devices. Nornir’s inventory system is flexible, allowing you to define devices, their credentials, and other details in a structured format.
- **Tasks**: These are the actions you want to perform on your devices, like sending commands or configurations. In Nornir, you write tasks as Python functions.
- **Plugins**: Nornir supports plugins to extend its functionality. Plugins can be used for tasks, inventory management, or adding new features.
- **Parallel Execution**: One of Nornir’s strengths is its ability to run tasks in parallel across multiple devices. This feature speeds up network automation tasks significantly, especially for large networks.
- **Results**: Nornir has a powerful feature called Results. After executing tasks on your devices, Nornir collects and stores the outcomes in a Results object.

We will go through each of these components in detail with some examples.

Here is my directory structure and the files (ignore nornir.log, which is created automatically):

```bash
(.venv) zolo@u22s:~/nornir-lab$ tree
.
├── config.yaml
├── defaults.yaml
├── groups.yaml
├── hosts.yaml
├── nornir.log
└── nornir_test.py

0 directories, 6 files
```

### Configuration File

The `config.yaml` file is a configuration for Nornir that outlines how it should manage its inventory and execute tasks. It’s written in YAML, a human-readable data format, making it easy to understand and modify.

```bash
# config.yaml
---
inventory:
  plugin: SimpleInventory
  options:
    host_file: 'hosts.yaml'
    group_file: 'groups.yaml'
    defaults_file: 'defaults.yaml'

runner:
  plugin: threaded
  options:
    num_workers: 5
```

- **Inventory**: Specifies how Nornir should load information about network devices. It uses the SimpleInventory plugin and points to three files (other inventory plugins can read from Ansible's inventory files or tools like NetBox):
  - `hosts.yaml` for individual device details
  - `groups.yaml` for settings common to groups of devices
  - `defaults.yaml` for default settings applicable to all devices unless overridden in the other files.
- **Runner**: Controls how Nornir runs tasks across devices. Here, the threaded plugin is used with `num_workers` set to 5, meaning tasks will be executed in parallel on up to 5 devices at a time.

### Host File

This file contains details about each network device. For every device, you can specify parameters such as its hostname, IP address, platform type (e.g., Cisco, Arista), and credentials. Nornir uses this information to connect to and manage the devices individually.

```bash
# hosts.yaml
---
sw1:
  hostname: 172.16.10.11
  groups:
    - cisco_switch

R1:
  hostname: 172.16.10.12
  groups:
    - cisco_router
```

### Groups File

The `groups.yaml` file is used to define common settings for groups of devices. For example, if you have several devices from the same vendor or within the same part of your network, you can group them and assign shared parameters like vendor or credentials. Devices in `hosts.yaml` can be associated with one or more groups, inheriting the group's settings.

```bash
# groups.yaml
---
cisco_switch:
  platform: cisco_ios

cisco_router:
  platform: cisco_ios
```

### Defaults File

The `defaults.yaml` file provides default settings that apply to all devices unless explicitly overridden in `hosts.yaml` or `groups.yaml`. This is useful for global settings like default credentials, timeout values, or any other parameters you want to apply network-wide. Here, I've defined the default credentials.

```bash
# defaults.yaml
---
username: admin
password: cisco
```

## Creating Our First Nornir Script

Let's look at a simple example to understand how our first Nornir script works, using the inventory examples we discussed before (with Cisco devices).

```python
from nornir import InitNornir

def say_hello(task):
    print("Hello, Nornir")

nr = InitNornir(config_file="config.yaml")
nr.run(task=say_hello)
```

```bash
(.venv) zolo@u22s:~/nornir-lab$ python nornir_test.py 
Hello, Nornir
Hello, Nornir
```

- **Importing Nornir**: The script starts by importing the `InitNornir` class from the Nornir library. This is essential for initializing our Nornir environment.

- **Defining a Task Function**: Next, we define a simple task function, `say_hello`, that takes `task` as an argument. This function simply prints a message, "Hello, Nornir". In Nornir, tasks are functions that you want to execute on your network devices. The `task` argument represents the task being executed and carries information about the current device it's running on.

- **Initializing Nornir**: We then create an instance of Nornir using `InitNornir`, specifying `config.yaml` as the configuration file. This configuration includes our inventory setup with `hosts.yaml`, `groups.yaml`, and `defaults.yaml`, defining our network devices and their properties.

- **Running the Task**: Finally, we use the `.run()` method on our Nornir instance to execute the `say_hello` task across all devices specified in our inventory. Because our `config.yaml` specifies a runner with 5 workers, tasks can be executed in parallel on up to 5 devices at a time.

- **Output**: Given our inventory setup, the script prints "Hello, Nornir" once for each device in the inventory. Since we have two devices (sw1 and R1), we see the message printed twice, indicating the task executed successfully on each device.

### The `print_result` Plugin

Let's look at our second example to see how to use the `print_result` plugin. If you have used Ansible before, you know it provides a nice output showing what's going on.

You can install the plugin using the `pip install` command:

```bash
pip install nornir_utils
```

```python
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result

def say_hello(task):
    return "Hello, Nornir"

nr = InitNornir(config_file="config.yaml")
result = nr.run(task=say_hello)
print_result(result)
```

In this updated example, the significant addition is the use of `print_result` from the `nornir_utils` plugin. This function is designed to neatly display the results of tasks executed by Nornir on your network devices.

- **Importing `print_result`**: We've added a new import statement to bring in the `print_result` function. This plugin is used for formatting and printing the outcome of our tasks in a readable manner.

- **Storing and Printing Results**: Instead of directly printing a message within the `say_hello` task, we now return the message. The main script captures the output of the `nr.run` method in a variable named `result`. This variable holds detailed information about the task execution on each device. Finally, `print_result(result)` is called to display this information.

```bash
(.venv) zolo@u22s:~/nornir-lab$ python nornir_test2.py 
say_hello***********************************************************************
* R1 ** changed : False ********************************************************
vvvv say_hello ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Hello, Nornir
^^^^ END say_hello ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* sw1 ** changed : False ********************************************************
vvvv say_hello ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Hello, Nornir
^^^^ END say_hello ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

This output shows the task results in a clear and organized format for each device.

The output is structured to provide detailed feedback on the task execution across each device in your inventory. Here’s a breakdown.

- Task Name - The script starts by mentioning the task name (say_hello) as a header for the output section.
- Device Name and Change Status - Each device the task was executed on is listed with its name (e.g., csr-01, eos-01) and a change status (changed : False). This status indicates whether the task made any changes to the device's state. In this case, no changes were made.
- Task Outcome: Below each device name, the result of the task is shown. Since our task simply returns a message, "My Task Works! Yaay" is printed under each device.
- Start and End Markers - Each device's result section is enclosed within vvvv and ^^^^ markers, providing clear visual segmentation. The INFO label next to the task name within this block indicates the nature of the output.

### Accessing the Host's Parameters

The `task.host` object allows us to access various parameters of the host on which the task is currently executing. You can retrieve specific details like:

- `task.host`: The name of the current device.
- `task.host.groups`: The group(s) the device belongs to.
- `task.host.hostname`: The hostname or IP address of the device.

By using `task.host` along with its attributes, we can dynamically insert each device's specific information into our task's return message.

```python
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result

def say_hello(task):
    return f"Hello, {task.host} - {task.host.groups} - {task.host.hostname}"

nr = InitNornir(config_file="config.yaml")
result = nr.run(task=say_hello)
print_result(result)
```

```bash
(.venv) zolo@u22s:~/nornir-lab$ python nornir_test3.py 
say_hello***********************************************************************
* R1 ** changed : False ********************************************************
vvvv say_hello ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Hello, R1 - [Group: cisco_device] - 172.16.10.12
^^^^ END say_hello ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* sw1 ** changed : False ********************************************************
vvvv say_hello ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Hello, sw1 - [Group: cisco_device] - 172.16.10.11
^^^^ END say_hello ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

This script shows how to use `task.host` to access and display details about each device, including its name, groups, and hostname.

### Filtering Devices

Here's another example of how you can run tasks on specific devices.

```python
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result


def say_hello(task):
    return f"Hello, {task.host} - {task.host.groups} - {task.host.hostname}"


nr = InitNornir(config_file="config.yaml")
nr = nr.filter(hostname="172.16.10.11")

result = nr.run(task=say_hello)
print_result(result)
```

In this script, we're using the `filter` method to narrow down the devices based on their hostname. Specifically, we're filtering for devices with the hostname "172.16.10.11", which corresponds to switchs in our inventory. Then, we run the `say_hello` task only on these filtered devices. Finally, we print the results using the `print_result` function.
