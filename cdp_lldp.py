# under development.
# not tested yet.

from scapy.all import *
load_contrib('cdp')
load_contrib('lldp')

class CdpLldpReceiver(threading.Thread):
    def __init__(self):
        super(IcmpEchoReplyReceiver, self).__init__()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        eth_cdp = 'ether dst 01:00:0c:cc:cc:cc'
        eth_lldp = 'ether proto 0x88cc'
        filter = '{} or {}'.format(eth_cdp, eth_lldp)

        while not self.stop_event.is_set():
            sniff(filter=filter, prn=self.receive, count=0)

    def receive(self, l2frame):
        src = l2frame.src
        ethtype = l2frame.type
        if src == '01:00:0c:cc:cc:cc':
            receive_cdp(l2frame[CDPv2_HDR])
        elif ethtype == 560140: #0x88cc
            receive_lldp(packet[LLDPDU])

    def receive_cdp(self, cdph):
        # sample https://gist.github.com/y0ug/8ddb697b5b8a243d0a36
        # impl https://github.com/levigross/Scapy/blob/master/scapy/contrib/cdp.py
        pass

    def receive_lldp(self, lldph):
        # sample
        # impl https://github.com/secdev/scapy/blob/master/scapy/contrib/lldp.py
        pass

    def stop(self):
        self.stop_event.set()
        self.thread.join()
