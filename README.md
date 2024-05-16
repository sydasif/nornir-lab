# Nornir Network Automation

Nornir is a Python library designed for Network Automation tasks. It enables Network Engineers to use Python to manage and automate their network devices. Unlike tools like Ansible which rely on domain-specific languages, Nornir leverages the full power of Python, giving you more flexibility and control over your automation scripts.

If you're used to Ansible, you know that you first set up your inventory, write tasks, and execute them on all or selected devices concurrently. Nornir operates similarly, but the big difference is you use Python code instead of any Domain Specific Language.

## Prerequisites and Key Points

First off, diving into Nornir assumes you have a fair understanding of Python and its basics. If you're starting from scratch with Python, I highly recommend checking out my study guide to get up to speed. It’s designed to build a solid foundation in Python.

It’s also crucial to remember that Nornir isn’t here to replace tools like Netmiko or Napalm, rather, it's meant to work alongside them. Think of Nornir as a framework that orchestrates your automation tasks. For you to SSH to network devices, you'll still rely on plugins like Netmiko. We'll dive deeper into how these tools integrate with Nornir in the upcoming sections.

Installing Nornir is as simple as running the pip install command.

```bash
pip install nornir
```

## Nornir Introduction

Here's a quick look at the main building blocks of Nornir, together, these components form a robust framework for network automation.

- Inventory - This is where you store information about your devices. Nornir's inventory system is flexible, allowing you to define devices, their credentials, and other details in a structured format.
- Tasks - These are the actions you want to perform on your devices, like sending commands or configurations. In Nornir, you write tasks as Python functions.
- Plugins - Nornir supports plugins to extend its functionality. Plugins can be used for tasks, inventory management, or adding new features.
- Parallel Execution - One of Nornir's strengths is its ability to run tasks in parallel across multiple devices. This built-in feature speeds up network automation tasks significantly, especially when dealing with large networks.
- Results - Nornir has a powerful feature known as Results. After executing tasks on your devices, Nornir collects and stores the outcomes in a Results object.

We will go through each one of them in detail using a few examples.

Here is my directory structure and the files (please ignore nornir.log which get created automatically)

```bash
(.venv) zolo@u22s:~/nornir-lab$ tree
.
├── config.yaml
├── defaults.yaml
├── groups.yaml
├── hosts.yaml
├── nornir.log
├── nornir_test.py
└── README.md

0 directories, 7 files
```

## config.yaml

This config.yml file is a configuration for Nornir that outlines how it should manage its inventory and execute tasks. It's written in YAML, a human-readable data serialization standard, making it straightforward to understand and modify.

```bash
#config.yaml
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

- Inventory - Specifies how Nornir should load information about network devices. It uses the SimpleInventory plugin, pointing to three files (We also have other inventory plugins which can read from Anisble's inventory files or NST tools like NetBox)
  - hosts.yaml for individual device details
  - groups.yaml for settings common to groups of devices, and
  - defaults.yaml for default settings applicable to all devices if not overridden in the other files.
- Runner - Controls how Nornir runs tasks across devices. Here, the threaded plugin is used with num_workers set to 5, meaning tasks will be executed in parallel across up to 5 devices at a time.

### hosts.yaml

This file contains details about each network device. For every device, you can specify parameters such as its hostname, IP address, platform type (e.g., Cisco, Arista), and credentials. Nornir uses this information to connect to and manage the devices individually. For this example, I'm starting out with five devices. (two Ciscos and three Aristas)

```bash
#hosts.yaml
---
sw:
  hostname: 172.16.10.11
  groups:
    - cisco_device

R1:
  hostname: 172.16.10.12
  groups:
    - cisco_device
```

### groups.yaml

The groups.yaml file is used to define common settings for groups of devices. For example, if you have several devices from the same vendor or within the same part of your network, you can group them and assign shared parameters like vendor or credentials. Devices in hosts.yaml can be associated with one or more groups, inheriting the group's settings. Here, I'm defining the platform for each group and the credentials for the 'arista' group.

```bash
#groups.yaml
---
cisco_device:
  platform: cisco_ios
```

### defaults.yaml

defaults.yaml provides default settings that apply to all devices unless explicitly overridden in hosts.yaml or groups.yaml. This is useful for global settings like default credentials, timeout values, or any other parameters you want to apply network-wide. Here, I've defined the default credentials.

```bash
#defaults.yaml
---
username: admin
password: cisco
```

## Creating Our First Nornir Script

Let's look at a simple example to understand how our first Nornir script works, especially using the inventory examples we discussed before (with csr and eos devices).

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

- Importing Nornir - The script starts by importing InitNornir Class from the Nornir library. This is essential for initializing our Nornir environment.

- Defining a Task Function - Next, we define a simple task function say_hello that takes task as an argument. This function merely prints a message, My Task Works! Yaay. In Nornir, tasks are functions that you want to execute on your network devices. The task argument is a key part of this; it represents the task being executed and carries information and context about the current device it's running against.

- Initializing Nornir - We then create an instance of Nornir using InitNornir, specifying our config.yaml as the configuration file. This configuration includes our inventory setup with hosts.yaml, groups.yaml, and defaults.yaml, defining our network devices and their properties.

- Running the Task - Finally, we use the .run() method on our Nornir instance to execute the say_hello task across all devices specified in our inventory. Because our config.yaml specifies a runner with 5 workers, tasks can be executed in parallel across up to 5 devices at a time.

- Output - Given our inventory setup, the script prints My Task Works! Yaay once for each device in the inventory. Since we have five devices (csr-01, csr-02, eos-01, eos-02, eos-03), we see the message printed five times, indicating the task executed successfully on each device.

## print_result plugin

Let's look at our second example on how to use the print_result plug-in. If you have used Ansible before, you would know that it gives a nice output showing what's going on.

You can install the plug-in using pip install command.

```bash
pip install nornir_utils
```

```python
from nornir import InitNornir


def say_hello(task):
    print("Hello, Nornir")


nr = InitNornir(config_file="config.yaml")
nr.run(task=say_hello)
```
In the updated example, the significant addition is the use of print_result from the nornir_utils plugin. This function is designed to neatly display the results of tasks executed by Nornir on your network devices.

Importing print_result - We've added a new import statement to bring in the print_result function. This plug-in is used for formatting and printing the outcome of our tasks in a readable manner.

Storing and Printing Results - Instead of directly printing a message within the say_hello task, we now return the message. The main script captures the output of the nr.run method in a variable named result. This variable holds detailed information about the task execution on each device. Finally, print_result(result) is called to display this information.

```bash
(.venv) zolo@u22s:~/nornir-lab$ python nornir_test2.py 
say_hello***********************************************************************
* R1 ** changed : False ********************************************************
vvvv say_hello ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Hello, Nornir
^^^^ END say_hello ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* sw ** changed : False ********************************************************
vvvv say_hello ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Hello, Nornir
^^^^ END say_hello ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

The output is structured to provide detailed feedback on the task execution across each device in your inventory. Here’s a breakdown.

- Task Name - The script starts by mentioning the task name (say_hello) as a header for the output section.
- Device Name and Change Status - Each device the task was executed on is listed with its name (e.g., csr-01, eos-01) and a change status (changed : False). This status indicates whether the task made any changes to the device's state. In this case, no changes were made.
- Task Outcome: Below each device name, the result of the task is shown. Since our task simply returns a message, "My Task Works! Yaay" is printed under each device.
- Start and End Markers - Each device's result section is enclosed within vvvv and ^^^^ markers, providing clear visual segmentation. The INFO label next to the task name within this block indicates the nature of the output.

## Accessing the host's parameters

The task.host object allows us to access various parameters of the host on which the task is currently executing. You can retrieve specific details like.

- task.host - The name of the current device.
- task.host.groups - The group(s) the device belongs to.
- task.host.hostname - The hostname or IP address of the device.

By using task.host along with its attributes, we're able to dynamically insert each device's specific information into our task's return message.

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
* sw1 ** changed : False *******************************************************
vvvv say_hello ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
Hello, sw1 - [Group: cisco_device] - 172.16.10.11
^^^^ END say_hello ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```

## Filtering Devices

Here is another example of how you can run the tasks on specific devices. For the sake of simplicity, I'm going to run the task only on Arista devices

```python
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result


def say_hello(task):
    return (
        f"My Task Works! Yaay {task.host} - {task.host.groups} - {task.host.hostname}"
    )


nr = InitNornir(config_file="config.yaml")
nr = nr.filter(hostname="172.16.10.11")

result = nr.run(task=say_hello)
print_result(result)
```
