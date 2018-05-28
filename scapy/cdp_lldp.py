# under development.
# tested and worked.

import traceback
from scapy.all import *
load_contrib('cdp')
load_contrib('lldp')

class CdpLldpReceiver(threading.Thread):
    def __init__(self):
        super(CdpLldpReceiver, self).__init__()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        eth_cdp = 'ether dst 01:00:0c:cc:cc:cc'
        eth_lldp = 'ether proto 0x88cc'
        filter = '{} or {}'.format(eth_cdp, eth_lldp)

        while not self.stop_event.is_set():
            sniff(iface = 'en8', filter=filter, prn=self.receive, count=0)

    def receive(self, l2frame):
        try:
            dst = l2frame.dst
            if dst == '01:00:0c:cc:cc:cc':
                print('cdp')
                cdp = l2frame[CDPv2_HDR]
                self.receive_cdp(cdp)
            elif '01:80:c2:00:00:0' in dst:
                print('lldp')
                lldp = l2frame[LLDPDU]
                self.receive_lldp(lldp)
        except:
            print(traceback.format_exc())



    def receive_cdp(self, cdp):
        # sample https://gist.github.com/y0ug/8ddb697b5b8a243d0a36
        # impl https://github.com/levigross/Scapy/blob/master/scapy/contrib/cdp.py
        print(cdp[CDPMsgDeviceID].val)
        print(cdp[CDPMsgPortID].iface)
        print(cdp[CDPMsgSoftwareVersion].val)
        print(cdp[CDPMsgPlatform].val)
        print(cdp[CDPMsgNativeVLAN].vlan)

    def receive_lldp(self, lldp):
        # sample
        # impl https://github.com/secdev/scapy/blob/master/scapy/contrib/lldp.py
        print(lldp[LLDPDUSystemName].system_name)
        print(lldp[LLDPDUPortID].id)
        print(lldp[LLDPDUSystemDescription].description)
        print(lldp[LLDPDUPortDescription].description)

    def stop(self):
        self.stop_event.set()
        self.thread.join()

receiver = CdpLldpReceiver()
