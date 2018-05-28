# under development.
# tested and worked.

# Multiple Ping

import time
import socket
import threading
from scapy.all import *

ICMP_ID = 110

# {Target :
#           num_send,
#           num_received,
#           average_rtt,
#           [(rtt, received?), (rtt, received?)]}

tmap = {}
lock = threading.Lock()
def sync_add_target(target):
    lock.acquire()
    tmap[target] = (0, 0, 0, [])
    lock.release()

def sync_append_sendtime(target, seq):
    lock.acquire()
    (num_send, num_received, average_rtt, tlist) = tmap[target]
    tlist.append((time.time(), False))
    # update map
    tmap[target] = (num_send + 1, num_received, average_rtt, tlist)
    lock.release()

def sync_update_receivetime(target, seq):
    lock.acquire()
    (num_send, num_received, average_rtt, tlist) = tmap[target]
    # update rtt
    (send_time, _) = tlist[seq]
    rtt = time.time() - send_time
    tlist[seq] = (rtt, True)
    # update average_rtt
    average_rtt = (average_rtt * num_received + rtt) / (num_received + 1)
    # update map
    tmap[target] = (num_send, num_received + 1, average_rtt, tlist)
    lock.release()

def sync_get(num_items):
    result_map = {}
    lock.acquire()
    for (key, value) in tmap.items():
        (num_send, num_received, average_rtt, rtt_list) = value
        n = len(rtt_list) - num_items
        if(n < 0):
            n = 0
        result_map[key] = (num_send, num_received, average_rtt, rtt_list[n:])
    lock.release()
    return result_map


class IcmpEchoReplyReceiver(threading.Thread):
    def __init__(self):
        super(IcmpEchoReplyReceiver, self).__init__()
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        filter = 'icmp[icmptype] == 0'
        while not self.stop_event.is_set():
            sniff(filter=filter, prn=self.receive, count=0)

    def receive(self, packet):
        ip = packet[IP]
        icmp = ip[ICMP]
        src = ip.src
        id = icmp.id
        seq = icmp.seq
        if id != ICMP_ID:
            # not this app's
            return
        sync_update_receivetime(src, seq)

    def stop(self):
        self.stop_event.set()
        self.thread.join()


class IcmpEchoRequestSender(threading.Thread):
    def __init__(self, dst, interval):
        super(IcmpEchoRequestSender, self).__init__()
        self.dstip = socket.gethostbyname(dst)
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)
        sync_add_target(self.dstip)
        self.thread.start()

    def run(self):
        id = ICMP_ID
        seq = 0
        while not self.stop_event.is_set():
            ping = IP(dst=self.dstip) / ICMP(id=id, seq=seq)
            sync_append_sendtime(self.dstip, seq)
            send(ping, verbose=0)
            seq += 1
            time.sleep(self.interval)

    def stop(self):
        self.stop_event.set()
        self.thread.join()


class ConsoleGUI(threading.Thread):
    def __init__(self, interval):
        super(ConsoleGUI, self).__init__()
        self.interval = interval
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while not self.stop_event.is_set():
            text = self.make_output()
            self.tprint(text)
            time.sleep(self.interval)

        # last output
        text = self.make_output()
        print(text)


    def make_output(self):
        width = 30
        result = sync_get(30)
        text = ''
        for (key, value) in result.items():
            (num_send, num_received, average_rtt, rtt_list) = value
            blank = ' ' * (width - len(rtt_list))
            line = 'from={} rcv/send={}/{} ave_rtt={} : {}'.format(key, num_received, num_send, average_rtt, blank)
            for (rtt, received) in rtt_list:
                if received:
                    line += 'X'
                else:
                    line += '_'
            text += line + '\n'
        return text

    def tprint(self, text):
        print(text)
        c = text.count('\n')
        for i in range(c + 1):
            sys.stdout.write('\x1b[1A') # cursol up
        sys.stdout.flush()

    def stop(self):
        self.stop_event.set()
        self.thread.join()


# start
receiver = IcmpEchoReplyReceiver()
console = ConsoleGUI(1)
time.sleep(1)

senders = []
dsts = ['www.google.co.jp', 'www.yahoo.co.jp']
for dst in dsts:
    senders.append(IcmpEchoRequestSender(dst, 1))

# end with ctrl-c
'''
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    for sender in senders:
        sender.stop()

    time.sleep(1)
    receiver.stop()
    console.stop()
'''
