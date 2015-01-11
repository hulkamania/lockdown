import sqlite3, re
from os import path

DAY_RE   = re.compile('^([1-9]|[12][0-9]|30|31)$')
MON_RE   = re.compile('^([1-9]|1[0-2])$')
YEAR_RE  = re.compile('^20\d\d$')

OUTCOMES = { 0 : 'BLOCKED',
             1 : 'ALLOWED',
             2 : 'NO_APP' }

OC_VALS = { 'BLOCKED' : 0,
            'ALLOWED' : 1,
            'NO_APP'  : 2 }

class LogDateError(Exception):
    def __init__(self, value):
        self.value = value
        self.msg   = 'Valid Tuple Is (yyyy, mm, dd)'

    def __str__(self):
        return "%s : %s" % ( self.msg, repr(self.value) )

class LogMissingError(Exception):
    def __init__(self, filename):
        self.msg = "Cannot find logfile: %s" % filename

    def __str__(self):
        return self.msg

def find_log(year, month, day, log_dir, suffix):
    try:
        if not ( re.search(YEAR_RE, year) and re.search(MON_RE, month) and re.search(DAY_RE, day) ): 
            raise Exception()
    except:
        raise LogDateError(date)

    log_name = '%s/%s.%s.%s.%s' % ( log_dir, year, month, day, suffix )

    if not path.exists(log_name):
        raise LogMissingError(log_name)
    
    return log_name

def print_protos(proto_map, proto_names, prefix, prespace):
    ''' pretty print a protocols map { <proto> : { <port> : { <binary> : <count, ... }, ... }, ... }
    '''

    for ( proto, ports ) in proto_map.iteritems():
        # ports in ascending order
        for port in sorted(ports):
            bins = ports.get(port)
            # binary counts in descending order
            b    = sorted(bins, key=bins.__getitem__).pop()

            print "%s%5s %5s %5s %s"  % ( prefix, proto_names[proto], port, bins.pop(b), b )

            for binary in sorted(bins, key=bins.__getitem__, reverse=True):
                print "%s%5s %s" % ( prespace, bins.get(binary), binary )
