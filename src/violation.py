import sqlite3

from os          import path
from ldui.common import find_log, LogMissingError

# violation database SQL
VIOLATIONS_SELECT  = 'SELECT id, user, proto, binary, dport, dest FROM conn_violation'
VIOLATIONS_DELETE  = 'DELETE FROM conn_violation WHERE id = ?'

# handled database SQL
HANDLED_SELECT  = 'SELECT id, user, proto, binary, dport, dest FROM conn_handled'
HANDLED_DELETE  = 'DELETE FROM conn_handled WHERE id = ?'
EXISTS_HANDLED   = 'SELECT count(id) FROM conn_handled   WHERE user = ? AND proto = ? AND binary = ? AND dport = ? AND dest = ?'
INSERT_HANDLED   = 'INSERT INTO conn_handled (user, proto, binary, dport, dest) VALUES (?, ?, ?, ?, ?)'

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
            return - a list of vilations
        '''
        logs = []
        conn = sqlite3.connect(self.log_name)
        cur  = conn.cursor()

        for ( violation_id, user, proto, binary, dport, dest ) in cur.execute(VIOLATIONS_SELECT).fetchall():
            logs.append({ 'id': violation_id, 'user': user, 'proto': proto, 'bin': binary, 'dport': dport, 'dest': dest })
        cur.close()
        conn.close()

        return logs

    def delete_violation(self, vid):
        ''' Delete a violation
            vid - violation ID
        '''
        conn = sqlite3.connect(self.log_name)
        cur  = conn.cursor()
        cur.execute(VIOLATIONS_DELETE, ( vid, ))

class HandledHandler:
    ''' read, write, delete LockDown records for violations that have been handled
    '''
    def __init__(self, log_dir):
        ''' Returns a new ViolationHandler
            log_dir - directory where the logs are stored
            date    - a tuple (yyyy, mm, dd) representing the log to be read
        '''
        self.log_name = 'log.handled'

        if not path.exists(self.log_name):
            raise LogMissingError(self.log_name)

    def get_all(self):
        ''' Get all violations that have already been handled
            return - a list of vilations
        '''
        logs = []
        conn = sqlite3.connect(self.log_name)
        cur  = conn.cursor()

        for ( violation_id, user, proto, binary, dport, dest ) in cur.execute(HANDLED_SELECT).fetchall():
            logs.append({ 'id': violation_id, 'user': user, 'proto': proto, 'bin': binary, 'dport': dport, 'dest': dest })
        cur.close()
        conn.close()

        return logs

    def exists(self, uid, proto, app, dport, dest):
        ''' Check if a violation was already handled
        '''
        return self.conn.execute(EXISTS_HANDLED, (uid, proto, app, dport, dest)).next()[0] > 0

    def add_violation(self, vid, user, proto, binary, dport, dest):
        ''' Add a violation to the handled list
        '''

        if not self.exists(uid, proto, app, dport, dest):
            self.conn.execute(INSERT_HANDLED, (uid, proto, app, dport, dest))
        self.conn.commit()


    def delete_violation(self, hid):
        ''' Delete a violation
            hid - violation ID
        '''
        conn = sqlite3.connect(self.log_name)
        cur  = conn.cursor()
        cur.execute(HANDLED_DELETE, ( hid, ))

