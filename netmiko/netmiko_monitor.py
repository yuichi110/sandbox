import netmiko
import threading

class DeviceOutputGetter(threading.Thread):
    def __init__(self, session_map, command_lists, callback):
        super(DeviceOutputGetter, self).__init__()
        self.session_map = session_map
        self.command_lists = command_lists
        self.callback = callback
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        session = netmiko.ConnectHandler(**self.session_map)
        session.enable()
        command_output_pairs = []
        for command in self.command_lists:
            output = session.send_command(command)
            command_output_pairs.append((command, output))
        session.disconnect()
        self.callback(command_output_pairs)


def callback_printall(command_output_pairs ):
    for (command, output) in command_output_pairs :
        print('=' * 30)
        print('#' + command)
        print(output)
        print('\n')


session_map = {
  'device_type':'cisco_ios',
  'host':'99.99.99.1',
  'username':'admin',
  'password':'nutanix/4u',
  'secret':'nutanix123'
}
command_lists = ['show ip int bri', 'show run', 'show cdp neigh']
getter = DeviceOutputGetter(session_map, command_lists, callback_printall)
