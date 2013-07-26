"""
this func is used for old_log
because the old_log don't be the out format of json.dumps
we can use this func to trans 'str' to 'dict'
@author by Intery
@time 2013-07-09  17:26:02
"""

import sys
import re

def trans(value):
    value = value.strip()
    m = re.match(r"^u'(.*)'$", value)
    if m:
        return value[2:-1]
    else:
        return value.strip("'")

def to_dict(data):
    r_dict = dict()
    data = data.strip('\n').strip('{}').split(',')
    for k_v in data:
        if len(k_v.split(':')) == 2:
            r_dict[trans(k_v.split(':')[0])] = trans(k_v.split(':')[1])
    return r_dict

if __name__ == '__main__':
    test = "{ u'c': u'201', u'b': u'\\u843d\\u53f6', u'd': 100001, 'ip': '58.18.139.61', u'k': u'2.3.1', u'bi': u'd456a9a37a0548c1bbc6ec2a14e2fd16', u'o': u'1', u's': u'0', u'u': u'66130866', u't': u'download', u'v': u'1', u'x': 1372860243573 }"
    result = to_dict(test)
    print result
