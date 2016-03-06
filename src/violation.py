import sqlite3

from os          import path
from ldui.common import find_log, LogMissingError

# violation database SQL
VIOLATIONS_SELECT  = 'SELECT id, user, proto, binary, dport, dest, handled FROM conn_violation'
VIOLATIONS_DELETE  = 'DELETE FROM conn_violation WHERE id = ? AND handled = 1'
VIOLATIONS_HANDLED = 'SELECT count(id) FROM conn_violation WHERE user = ? AND proto = ? AND binary = ? AND dport = ? AND dest = ? AND handled = 1'
VIOLATIONS_HANDLE  = 'MODIFY conn_violation SET handled = 1 WHERE user = ? AND proto = ? AND binary = ? AND dport = ? AND dest = ?'

class ViolationHandler:
    ''' read, write, delete LockDown violation logs 
    '''
    def __init__(self, log_dir, date):
        ''' Returns a new ViolationHandler
            log_dir - directory where the logs are stored
            date    - a tuple (yyyy, mm, dd) representing the log to be read
        '''
        self.log_name = find_log(date[0], date[1], date[2], log_dir, 'violation')

    def get_all(self):
        ''' Get all violations
            return - a list of violations
        '''
        logs = []
        conn = sqlite3.connect(self.log_name)
        cur  = conn.cursor()

        for ( violation_id, user, proto, binary, dport, dest, handled ) in cur.execute(VIOLATIONS_SELECT).fetchall():
            handled_bool = False
            if handled == 1:
                handled_bool = True
            logs.append({ 'id': violation_id, 'user': user, 'proto': proto, 'bin': binary, 'dport': dport, 'dest': dest, 'handled': handled_bool })
        cur.close()
        conn.close()

        return logs

    def get_not_handled(self):
        ''' Get violations that have not been handled yet
            return - a list of violations
        '''
        return list(( violation for violation in self.get_all() if not violation.get('handled') ))

    def get_handled(self):
        ''' Get violations that have been handled
            return - a list of violations
        '''
        return list(( violation for violation in self.get_all() if violation.get('handled') ))

    def delete_violation(self, vid):
        ''' Delete a violation
            vid - violation ID
        '''
        conn = sqlite3.connect(self.log_name)
        cur  = conn.cursor()
        cur.execute(VIOLATIONS_DELETE, ( vid, ))

    def handled(self, uid, proto, app, dport, dest):
        ''' Check if a violation was already handled
        '''
        return self.conn.execute(VIOLATIONS_HANDLED, (uid, proto, app, dport, dest)).next()[0] > 0

    def handle_violation(self, vid, user, proto, binary, dport, dest):
        ''' Mark a violation as handled
        '''
        if not self.handled(uid, proto, app, dport, dest):
            self.conn.execute(VIOLATIONS_HANDLE, (uid, proto, app, dport, dest))
        self.conn.commit()
