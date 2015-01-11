import sqlite3

from ldui.common import find_log

# log database SQL
LOGS_SELECT  = 'SELECT conn_log.id, user, proto, binary, dport, dest, outcome, time FROM conn_log JOIN conn_stamp ON conn_stamp.log_id = conn_log.id'

class LogReader:
    ''' Reads information from the LockDown logs 
    '''
    def __init__(self, log_dir, date):
        ''' Returns a new LogReader
            log_dir - directory where the logs are stored
            date    - a tuple (yyyy, mm, dd) representing the log to be read
        '''
        self.log_name = find_log(date[0], date[1], date[2], log_dir, 'log')

    def get_all(self):
        ''' Get all logs
            reuturn - a list of log records
        '''
        logs = []
        conn = sqlite3.connect(self.log_name)
        cur  = conn.cursor()

        for ( conn_id, user, proto, binary, dport, dest, outcome, date ) in cur.execute(LOGS_SELECT).fetchall():
            logs.append({ 'id': conn_id, 'user': user, 'proto': proto, 'bin': binary, 'dport': dport, 'dest': dest, 'outcome': outcome, 'date': date })
        cur.close()
        conn.close()

        return logs

    def get_ports(self):
        ''' Get ports accessed on a per binary basis
            return - a dictionary in the form { '<proto>' : { port : { <binary> : <count>, ... } , ... }, ... }
        '''
        logs = {}
        raw  = self.get_all()

        # reorganize the logs based on binary and protocol
        for log in raw:
            ( binary, proto, dport ) = ( log['bin'], log['proto'], log['dport'] )
            if not logs.has_key(proto):
                # create new entry for not yet identified proto
                logs[proto] = { dport : {} }
            elif not logs[proto].has_key(dport):
                # create new dport entry for proto
                logs[proto][dport] = {}
            # add or increment the binary entry
            logs[proto][dport][binary] = logs[proto][dport].get(binary, 0) + 1

        return logs

    def get_dest(self):
        ''' Get destinations and ports accessed on a per binary basis
        '''
        logs = {}
        raw  = self.get_all()

        # reorganize the logs based on binary and destination
        for log in raw:
            ( binary, proto, dest, dport ) = ( log['bin'], log['proto'], log['dest'], log['dport'] )
            if not logs.has_key(binary):
                # create new entry for not yet identified binaries
                logs[binary] = { dest : { proto : {} } }
            elif not logs[binary].has_key(dest):
                # create new destination entry for binary
                logs[binary][dest] = { proto : {} }
            elif not logs[binary][dest].has_key(proto):
                # create new protocol entry for destination
                logs[binary][dest][proto] = {}
            # add or increment the port entry
            logs[binary][dest][proto][dport] = logs[binary][dest][proto].get(dport, 0) + 1

        return logs
