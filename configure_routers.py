#!/usr/bin/env python

from getpass import getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

#getting username and password for SSH connection to the devices
username = input('Enter your SSH username: ')
password = getpass()

# reading coomands that will be issued to the routers and saving it into a commands_list variable
with open('commands_file') as f:
    commands_list = f.read().splitlines()

# list of devices ip addresses will be read from devices_list file
with open('devices_file') as f:
    devices_list = f.read().splitlines()

# iterating through the devices ip address in the file
for device in devices_list:
    print ('Connecting to device" ' + device)
    ip_address_of_device = device
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device, 
        'username': username,
        'password': password
    }

# connecting to each device while catching any exception
    try:
        net_connect = ConnectHandler(**ios_device)
    except (AuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + ip_address_of_device)
        continue
    except (EOFError):
        print ('End of file while attempting device ' + ip_address_of_device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

# sending the configurations command to the CLI
    output = net_connect.send_config_set(commands_list)
 # printing these commands out
    print (output)
