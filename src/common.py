import re, json

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
