#!/usr/bin/python

import inet_diag, optparse

def get_conn_process(proto, sip, sport, dip, dport):
    ''' Get the process information for a given connection
    '''
    found = (None, None, None)
    sock  = ''

    idiag = inet_diag.create(states = inet_diag.default_states, socktype=proto, src=sip, sport=sport, dst=dip, dport=dport, proc=1)
    try:
        sock = idiag.get()
        found = ( sock.pid(), sock.process(), sock.uid() )
    except:
        pass
    del sock
    del idiag

    return found

def get_list_process(proto, sip, sport):
    ''' Get the process information for a server
    '''
    found = (None, None, None)
    sock  = ''

    idiag = inet_diag.create(states=inet_diag.listen_states, socktype=proto, ge_spt=sport, le_spt=sport, proc=1)
    try:
        sock = idiag.get()
        found = ( sock.pid(), sock.process(), sock.uid() )
    except:
        pass
    del sock
    del idiag

    return found

def main():
    ''' Test code
    '''
    ( pid, process, uid ) = get_conn_process(1, '127.0.0.1', 100, '127.0.0.1', 10001)

    print "%d: %s" % ( pid, process, uid )

if __name__ == '__main__':
    main()
