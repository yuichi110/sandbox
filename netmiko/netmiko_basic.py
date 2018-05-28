import netmiko

session = netmiko.ConnectHandler(device_type='cisco_ios',
  host='99.99.99.1', username='admin',
  password='nutanix/4u', secret='nutanix123')

session.enable()

# config change
create_loopback100 = ['int loopback100',
 'ip address 100.100.100.100 255.255.255.255',
  'no shut']
session.send_config_set(create_loopback100)
#session.send_config_set(['no int loopback100'])

# show command
output = session.send_command('show ip int bri')
print(output)

session.disconnect()
