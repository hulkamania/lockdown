import sqlite3

from ldui.common import find_log, OC_VALS

# log database SQL
LOGS_SELECT  = 'SELECT conn_log.id, user, proto, binary, dport, dest, outcome, time FROM conn_log JOIN conn_stamp ON conn_stamp.log_id = conn_log.id %s'

class LogReader:
    ''' Reads information from the LockDown logs
    '''
    def __init__(self, log_dir, date, exclude=[], outcomes=[]):
        ''' Returns a new LogReader
            log_dir  - directory where the logs are stored
            date     - a tuple (yyyy, mm, dd) representing the log to be read
            exclude  - exclude logs with a binary containing this text
            outcomes - only retrieve logs for the given outcomes
        '''
        self.log_name = find_log(date[0], date[1], date[2], log_dir, 'log')
        self.exclude  = exclude
        self.outcomes = outcomes

    def get_all(self):
        ''' Get all logs
            return - a list of dictionaries with the keys id, user, proto, bin, dport, dest, outcome, date
        '''
        logs = []
        conn = sqlite3.connect(self.log_name)
        cur  = conn.cursor()

        for ( conn_id, user, proto, binary, dport, dest, outcome, date ) in cur.execute(LOGS_SELECT % self._outcomes_where()).fetchall():
            if self._is_excluded(binary):
                continue
            logs.append({ 'id': conn_id, 'user': user, 'proto': proto, 'bin': binary, 'dport': dport, 'dest': dest, 'outcome': outcome, 'date': date })
        cur.close()
        conn.close()

        return logs

    def get_ports(self):
        ''' Get ports accessed on a per binary basis
            return - a dictionary in the form { '<proto>' : { <port> : { <binary> : <count>, ... } , ... }, ... }
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
            return - a dictionary in the form { '<dest>' : { <proto> : { <port> : { <binary> : <count>, ... }, ... } , ... }, ... }
        '''
        logs = {}
        raw  = self.get_all()

        # reorganize the logs based on binary and destination
        for log in raw:
            ( binary, proto, dest, dport ) = ( log['bin'], log['proto'], log['dest'], log['dport'] )
            if not logs.has_key(dest):
                # create new entry for not yet identified destinations
                logs[dest] = { proto : { dport : {} } }
            elif not logs[dest].has_key(proto):
                # create new protocol entry for destination
                logs[dest][proto] = { dport : {} }
            elif not logs[dest][proto].has_key(dport):
                # create new dport entry for protocol
                logs[dest][proto][dport] = {}
            # add or increment the binary entry
            logs[dest][proto][dport][binary] = logs[dest][proto][dport].get(binary, 0) + 1

        return logs

    def _is_excluded(self, binary):
        for text in self.exclude:
            if binary.find(text) != -1:
                return True

        return False

    def _outcomes_where(self):
        checks = []
        for outcome in self.outcomes:
            checks.append("outcome=%d" % OC_VALS.get(outcome))

        if len(checks) > 0:
            return " WHERE %s" % ' AND '.join(checks)
        else:
            return ''
