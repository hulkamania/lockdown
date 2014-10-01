import nfqueue

from os      import system
from nfqueue import NFQNL_COPY_PACKET
from socket  import AF_INET


''' All iptables related functionality
'''

IPT_BIN    = 'iptables'
IPT_STATEs = { 'rem' : ( '-D OUTPUT -p tcp -m conntrack --ctstate NEW -j NFQUEUE --queue-num 0',
                         '-D OUTPUT -p udp -m conntrack --ctstate NEW -j NFQUEUE --queue-num 0' ),
               'add' : ( '-I OUTPUT 1 -p tcp -m conntrack --ctstate NEW -j NFQUEUE --queue-num 0',
                         '-I OUTPUT 1 -p udp -m conntrack --ctstate NEW -j NFQUEUE --queue-num 0' ) }

def add_new_hook():
    ''' Add the hook for picking up new outgoing connections
    '''
    return _new_hook('add')

def rem_new_hook():
    ''' Remove the hook for picking up new outgoing connections
    '''
    return _new_hook('rem')

def _new_hook(action):
    code = 0
    for rule in IPT_STATEs[action]: 
        code += system("%s %s" % (IPT_BIN, rule))

    return code

class NFQueueReader:
    ''' Reads data from am NFQueue queue and passes
        it to the supplied callback
    '''
    def __init__(self, queue, callback):
        self.queue = nfqueue.queue()
        self.queue.set_callback(callback)
        self.queue.fast_open(queue, AF_INET)
        self.queue.set_queue_maxlen(1024)
        self.queue.set_mode(NFQNL_COPY_PACKET)

