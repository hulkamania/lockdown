import nfqueue, asyncore

from os      import system
from nfqueue import NFQNL_COPY_PACKET
from socket  import AF_INET


''' All iptables related functionality
'''

IPT_BIN    = 'iptables'
IPT_STATEs = { 'rem' : ( '-D OUTPUT -m conntrack --ctstate NEW -j lockdown',
                         '-F lockdown',
                         '-X lockdown'),
               'add' : ( '-N lockdown',
                         '-I OUTPUT 1 -m conntrack --ctstate NEW -j lockdown',
                         '-A lockdown -p udp -m udp --dport 53 -j RETURN',
                         '-A lockdown -p tcp -m conntrack --ctstate NEW -j NFQUEUE --queue-num 0',
                         '-A lockdown -p udp -m conntrack --ctstate NEW -j NFQUEUE --queue-num 0' ) }

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

class NFQueueReader(asyncore.file_dispatcher):
    ''' Reads data from am NFQueue queue and passes
        it to the supplied callback
    '''
    def __init__(self, queue, callback):
        self.queue = nfqueue.queue()
        self.queue.set_callback(callback)
        self.queue.fast_open(queue, AF_INET)
        self.queue.set_queue_maxlen(1024)

        self.fd = self.queue.get_fd()
        asyncore.file_dispatcher.__init__(self, self.fd, None)

        self.queue.set_mode(NFQNL_COPY_PACKET)

    def handle_read(self):
        self.queue.process_pending(5)

    def writable(self):
        return False
