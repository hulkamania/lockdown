import sqlite3, time
from os import path

# log database SQL
CREATE_LOG   = 'CREATE TABLE conn_log   (id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER, proto INTEGER, binary TEXT, dport INTEGER, dest STRING)'
CREATE_STAMP = 'CREATE TABLE conn_stamp (id INTEGER PRIMARY KEY AUTOINCREMENT, log_id INTEGER, outcome INTEGER, time DATE)'
INSERT_LOG   = 'INSERT INTO conn_log (user, proto, binary, dport, dest) VALUES (?, ?, ?, ?, ?)'
INSERT_STAMP = 'INSERT INTO conn_stamp (log_id, outcome, time) VALUES (?, ?, ?)'
EXISTS_LOG   = 'SELECT count(id) FROM conn_log WHERE user=? and proto=? and binary=? and dport=? and dest=?'
LOG_ID       = 'SELECT id FROM conn_log WHERE user=? and proto=? and binary=? and dport=? and dest=?'

# violatoin database SQL
CREATE_VIOLATION = 'CREATE TABLE conn_violation (id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER, proto INTEGER, binary TEXT, dport INTEGER, dest STRING)'
CREATE_HANDLED  = 'CREATE TABLE conn_handled   (id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER, proto INTEGER, binary TEXT, dport INTEGER, dest STRING)'
EXISTS_VIOLATION = 'SELECT count(id) FROM conn_violation WHERE user = ? AND proto = ? AND binary = ? AND dport = ? AND dest = ?'
EXISTS_HANDLED   = 'SELECT count(id) FROM conn_handled   WHERE user = ? AND proto = ? AND binary = ? AND dport = ? AND dest = ?'
INSERT_VIOLATION = 'INSERT INTO conn_violation (user, proto, binary, dport, dest) VALUES (?, ?, ?, ?, ?)'

class _Logger:
    ''' Log utility class
    '''
    def __init__(self, suffix, log_dir, tables, use_date=True):
        self.suffix   = suffix
        self.log_dir  = log_dir
        self.tables   = tables
        self.use_date = use_date
        self.conn     = self.open_log()

    def open_log(self):
        ''' Create and/or connect to database
        '''
        log_name = '%s/%s.%s' % (self.log_dir, self._next_log(), self.suffix)
        if not self.use_date:
            log_name = '%s/%s.%s' % (self.log_dir, 'log', self.suffix)

        exists = path.exists(log_name)
        conn   = sqlite3.connect(log_name)

        # create the table structure if the log did not exist
        if not exists:
            for table in self.tables:
                conn.execute(table)
                conn.commit()

        return conn

    def _next_log(self):
        self.date = time.localtime()
        return "%s.%s.%s" % (self.date.tm_year, self.date.tm_mon, self.date.tm_mday)

    def _check_rotate(self):
        return time.localtime() != self.date.tm_mday

    def rotate_log(self):
        ''' Rotate the database (based on day of month)
        '''
        if not self.use_date:
            return
        # close the open connection and open a new database
        self.cleanup()
        self.conn = self.open_log()

    def cleanup(self):
        ''' Cleanup database connections on shutdown
        '''
        self.conn.close()

class ConnectionLogger(_Logger):
    ''' Log utility for connection information gathered
        return - rowid for the timestamp entry
    '''
    def __init__(self, log_dir):
        _Logger.__init__(self, 'log', log_dir, ( CREATE_LOG, CREATE_STAMP ))

    def log_conn(self, uid, proto, app, dport, dest, outcome):
        ''' Log a new outgoing connection
        '''
        # hand log rotation
        if self._check_rotate():
            self.rotate_log()

        last_curr = None
        # another instance of an already seen connection
        if self.conn.execute(EXISTS_LOG, (uid, proto, app, dport, dest)).next()[0] > 0:
            last_curr = self.conn.execute(INSERT_STAMP, (self.conn.execute(LOG_ID, (uid, proto, app, dport, dest)).next()[0], outcome, time.asctime()))
        # a never seen connection
        else:
            curr = self.conn.execute(INSERT_LOG, (uid, proto, app, dport, dest))
            last_curr = self.conn.execute(INSERT_STAMP, (curr.lastrowid, outcome, time.asctime()))
        self.conn.commit()

        return last_curr.lastrowid

# SQL REQUIRED
# HANDLED LOGGER REQUIRED
class ViolationLogger(_Logger):
    ''' Log utility for policy violations
    '''
    def __init__(self, log_dir):
        _Logger.__init__(self, 'violation', log_dir, ( CREATE_VIOLATION, ))
        self.handled = HandledLogger(log_dir)

    def exists(self, uid, proto, app, dport, dest):
        ''' Check if a violation was already logged
        '''
        return self.conn.execute(EXISTS_VIOLATION, (uid, proto, app, dport, dest)).next()[0] > 0

    def log_violation(self, uid, proto, app, dport, dest):
        ''' Log a new violation
        '''
        # hand log rotation
        if self._check_rotate():
            self.rotate_log()

        # add violations that have not yet been recorded
        if not self.handled.exists(uid, proto, app, dport, dest) and not self.exists(uid, proto, app, dport, dest):
            self.conn.execute(INSERT_VIOLATION, (uid, proto, app, dport, dest))
        self.conn.commit()

class HandledLogger(_Logger):
    ''' Log utility for handled policy violations
    '''
    def __init__(self, log_dir):
        _Logger.__init__(self, 'handled', log_dir, ( CREATE_HANDLED, ), use_date=False)

    def exists(self, uid, proto, app, dport, dest):
        ''' Check if a violation was already handled
        '''
        return self.conn.execute(EXISTS_HANDLED, (uid, proto, app, dport, dest)).next()[0] > 0
