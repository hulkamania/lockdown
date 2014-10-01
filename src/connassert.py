import re, socket, sqlite3
from lockdown.common import read_json
from pwd import getpwnam
from ipaddr import IPv4Network

# regular expressions
IP_RE       = re.compile('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(/([0-9]|[12][0-9]|3[0-2]))?$')

# protocols to be filtered
PROTOCOLS   = ( 'tcp', 'udp' )

# configuration database SQL
APP_TABLE   = 'CREATE TABLE app (app_id INTEGER PRIMARY KEY AUTOINCREMENT, user INTEGER, binary TEXT, port INTEGER, max INTEGER)'
APP_INSERT  = 'INSERT INTO app (user, binary, port, max) VALUES (?, ?, ?, ?)'
DEST_TABLE  = 'CREATE TABLE dest (app_id INTEGER, addr STRING)'
DEST_INSERT = 'INSERT INTO dest (app_id, addr) VALUES (?, ?)'
APP_SELECT  = 'SELECT app_id FROM app WHERE ( user = ? OR user = -1 ) and binary = ? and port <= ? and max >= ?'
DEST_SELECT = 'SELECT addr FROM dest WHERE app_id = ?'

class ApplicationAssertions():
    ''' Configuration information for outgoing connections allowed
    '''
    def __init__(self, conf_dir):
        self.users = {}
        self._findusers()
        self.read_conf(conf_dir)

    def read_conf(self, conf_dir):
        ''' Move the configuration from a json file to an in memory DB
        '''
        db_conns = dict()
        for proto in PROTOCOLS:
            # raw configuartion 
            conf = read_json("%s/%s.conf" % ( conf_dir, proto ))

            # create in memory configuration database
            conn = sqlite3.connect(':memory:')
            setattr(self, '%s_conn' % proto, conn)

            # create the app table
            cur = conn.cursor()
            cur.execute(APP_TABLE)
            cur.execute(DEST_TABLE)

            # add the configuration to the db
            for user in conf.keys():
                for binary in conf[user].keys():
                    for port in conf[user][binary]:
                        # translate username to uid
                        uid = user
                        if user != 'all':
                            try:
                                uid = getpwnam(user)[2]
                            # we don't want to load configurations for unkown users
                            except:
                                continue

                        # makes max port value optional
                        if not port.has_key('max'):
                            port['max'] = port['port']

                        # add the application to db
                        cur.execute(APP_INSERT, ( uid, binary, port['port'], port['max'] ))

                        # add the destinations for the given app to the db
                        app_id = cur.lastrowid
                        for dests in port['destination']:
                            for ip in dests:
                                if not ip.find('/'):
                                    ip = "%s/32" % ip
                                cur.execute(DEST_INSERT, ( app_id, ip ))

                cur.close()

    def check_app(self, uid, proto, app, dport, dest):
        ''' Check the validity of an outgoing connection
        '''
        rtn = False
        if not hasattr(self, '%s_conn' % proto):
            return rtn

        cur = getattr(self, '%s_conn' % proto).cursor()

        # test is done in 2 steps:
        # 1. is there an application allowed to access the given dport as user
        # 2. is the destination in an allowed range
        for ( app_id ) in cur.execute(APP_SELECT, ( uid, app, dport, dport )).fetchall():
            for ( dnet ) in cur.execute(DEST_SELECT, ( app_id )).fetchall():
                if IPv4Network(dest).compare_networks(IPv4Network(dnet)):
                    rtn = True

        cur.close()

        return rtn

    def cleanup(self):
        ''' Cleanup open DB connections on shutdown
        '''
        for proto in PROTOCOLS:
            if hasattr(self, '%s_conn' % proto):
                getattr(self, '%s_conn' % proto).close()

    def _findusers(self):
        f = open('/etc/passwd','r')

        for line in f.readlines():
            (uname, undef, uid, undef, undef, undef, undef) = line.split(':')
            self.users[uname] = uid

