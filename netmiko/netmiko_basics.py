import netmiko

# make ssh session
session = netmiko.ConnectHandler(
  device_type='cisco_ios',
  host='99.99.99.1',
  username='admin',
  password='nutanix/4u',
  secret='nutanix123', # optional
  #port='8022', # optional
  #verbose=False, optional
)

# go to enable mode
session.enable()

# quit enable mode
#session.exit_enable_mode()

# config change
create_loopback100 = ['int loopback100',
 'ip address 100.100.100.100 255.255.255.255',
  'no shut']
session.send_config_set(create_loopback100)
#session.send_config_set(['no int loopback100'])

# show command
output = session.send_command('show ip int bri')
print(output)

# issue trainiling prompt command
# session..send_command_expect('write memory')

session.disconnect()


'''
Document1
https://pynet.twb-tech.com/blog/automation/netmiko.html

Some Netmiko methods that are generally available to you:
    net_connect.config_mode() -- Enter into config mode
    net_connect.check_config_mode() -- Check if you are in config mode, return a boolean
    net_connect.exit_config_mode() -- Exit config mode
    net_connect.clear_buffer() -- Clear the output buffer on the remote device
    net_connect.enable() -- Enter enable mode
    net_connect.exit_enable_mode() -- Exit enable mode
    net_connect.find_prompt() -- Return the current router prompt
    net_connect.commit(arguments) -- Execute a commit action on Juniper and IOS-XR
    net_connect.disconnect() -- Close the SSH connection
    net_connect.send_command(arguments) -- Send command down the SSH channel, return output back
    net_connect.send_config_set(arguments) -- Send a set of configuration commands to remote device
    net_connect.send_config_from_file(arguments) -- Send a set of configuration commands loaded from a file


Document2
https://github.com/ktbyers/netmiko

Supported Devices

Regularly tested
    Arista vEOS
    Cisco ASA
    Cisco IOS
    Cisco IOS-XE
    Cisco IOS-XR
    Cisco NX-OS
    Cisco SG300
    Dell OS10
    HP Comware7
    HP ProCurve
    Juniper Junos
    Linux

Limited testing
    Alcatel AOS6/AOS8
    Avaya ERS
    Avaya VSP
    Brocade VDX
    Brocade MLX/NetIron
    Calix B6
    Cisco WLC
    Dell-Force10
    Dell PowerConnect
    Huawei
    Mellanox
    NetApp cDOT
    Palo Alto PAN-OS
    Pluribus
    Ruckus ICX/FastIron
    Ubiquiti EdgeSwitch
    Vyatta VyOS

CLASS_MAPPER_BASE = {
    'a10': A10SSH,
    'accedian': AccedianSSH,
    'alcatel_aos': AlcatelAosSSH,
    'alcatel_sros': AlcatelSrosSSH,
    'arista_eos': AristaSSH,
    'aruba_os': ArubaSSH,
    'avaya_ers': AvayaErsSSH,
    'avaya_vsp': AvayaVspSSH,
    'brocade_fastiron': RuckusFastironSSH,
    'brocade_netiron': BrocadeNetironSSH,
    'brocade_nos': BrocadeNosSSH,
    'brocade_vdx': BrocadeNosSSH,
    'brocade_vyos': VyOSSSH,
    'checkpoint_gaia': CheckPointGaiaSSH,
    'calix_b6': CalixB6SSH,
    'ciena_saos': CienaSaosSSH,
    'cisco_asa': CiscoAsaSSH,
    'cisco_ios': CiscoIosSSH,
    'cisco_nxos': CiscoNxosSSH,
    'cisco_s300': CiscoS300SSH,
    'cisco_tp': CiscoTpTcCeSSH,
    'cisco_wlc': CiscoWlcSSH,
    'cisco_xe': CiscoIosSSH,
    'cisco_xr': CiscoXrSSH,
    'coriant': CoriantSSH,
    'dell_force10': DellForce10SSH,
    'dell_powerconnect': DellPowerConnectSSH,
    'eltex': EltexSSH,
    'enterasys': EnterasysSSH,
    'extreme': ExtremeSSH,
    'extreme_wing': ExtremeWingSSH,
    'f5_ltm': F5LtmSSH,
    'fortinet': FortinetSSH,
    'generic_termserver': TerminalServerSSH,
    'hp_comware': HPComwareSSH,
    'hp_procurve': HPProcurveSSH,
    'huawei': HuaweiSSH,
    'huawei_vrpv8': HuaweiVrpv8SSH,
    'juniper': JuniperSSH,
    'juniper_junos': JuniperSSH,
    'linux': LinuxSSH,
    'mellanox': MellanoxSSH,
    'mrv_optiswitch': MrvOptiswitchSSH,
    'netapp_cdot': NetAppcDotSSH,
    'ovs_linux': OvsLinuxSSH,
    'paloalto_panos': PaloAltoPanosSSH,
    'pluribus': PluribusSSH,
    'quanta_mesh': QuantaMeshSSH,
    'ruckus_fastiron': RuckusFastironSSH,
    'ubiquiti_edge': UbiquitiEdgeSSH,
    'ubiquiti_edgeswitch': UbiquitiEdgeSSH,
    'vyatta_vyos': VyOSSSH,
    'vyos': VyOSSSH,
}
'''
