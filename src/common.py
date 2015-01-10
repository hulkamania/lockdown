import re, json, struct

from socket import inet_ntoa

COMMENT_RE  = re.compile('^\s*[^#]{1}')

def reduce_256(orig):
	''' Reduce a number to a value less than 255
	'''
	val = (orig >> 24) ^ (orig >> 16) ^ (orig >> 8) ^ orig
	return val & (256 - 1)

def read_json(filename):
    ''' Read a json object from a file
    '''
    f = open(filename)

    # remove comments and whitespace
    lines   = filter(lambda line: re.match(COMMENT_RE, line.replace("\t", "")), f.readlines())
    content = ''.join(lines)
    content = content.replace("\n", "").replace("\t", "").replace("'", "\"")

    f.close()
    return json.loads(content)

def pack_conn (uid, proto, dport, outcome, dst, app):
    ''' Pack connection information to be sent to
        to the logger process
    '''
    if uid is None:
        uid = '666'
    if app is None:
        app = '666'

    primitives = struct.pack('>IIIII', int(uid), int(proto), int(dport), int(outcome), len(app))
    binary     = struct.pack(">%ds" % len(app), app)

    return "%s%s%s" % ( primitives, dst, binary )

def unpack_conn(primitives):
    ''' Unpack the primitives in the connection information
        received from the daemon
    '''
    # primitives = uid (I) + proto (I) + dport (I) + outcome (I) + app_len (I) + dip (do not unpack)
    ( uid, proto, dport, outcome, app_len ) = struct.unpack('>IIIII', primitives[:20])
    dip = inet_ntoa(primitives[20:])

    return ( uid, proto, dport, outcome, app_len, dip )

def unpack_binary(length, packed):
    ''' Unpack the binary name received from the daemon
    '''
    # binary (<length>s)
    ( binary, ) = struct.unpack(">%ds" % length, packed)

    return binary
