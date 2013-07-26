from to_dict import to_dict
import os
import re,json
import happybase

log_path = ['log003','duokan_ebook_hb_log-2013-07']

def gen_rowkey(time_stamp):
    action = struct.pack('>px','01')
    reverse_timestamp = struct.pack('>Q',2**48-long(time_stamp))
    return  action + reverse_timestamp + uuid.uuid4().bytes[0:8]

#the func to parse old format log
def parse_hb_oldlog(f, table):
    try:
        row_key = gen_rowkey(data['cf:timestamp'])
        while 1:
            content = f.readline()
            if not content:
                break
            data = content.split('\t')
            m = re.match(r'^\[download\]$',data[0])
            if len(data) == 2 and m:
                down_tuple = dict()
                result = to_dict(data[1])
                key_list = result.keys()
                #print result
                if result.get('o','') == '3':
                    #get user id
                    down_tuple['user_id'] = result.get('u','')
                    
                    #get device id
                    down_tuple['device_type'] = result.get('d','')

                    #get action type
                    down_tuple['action'] = result.get('t','')

                    #get book id
                    down_tuple['book_id'] = result.get('u','')

                    #get ref uri
                    #down_tuple['ref'] = result['']

                    #get time
                    down_tuple['timestamp'] = result.get('x','')
                    table.put(str(row_key), down_tuple)
    finally:
        pass

#the func to parse new format log
def parse_hb_newlog(f, table):
    try:
        while 1:
            content = f.readline()
            if not content:
                break
            data = content.split('\t')
            m = re.match(r'^\[download\]$',data[0])
            if len(data) == 2 and m:
                down_tuple = dict()
                result = json.loads(data[1])
                key_list = result.keys()
                #print result
                if result.get('o','') == '3':
                    #get user id
                    down_tuple['user_id'] = result.get('u','')
                    
                    #get device id
                    down_tuple['device_type'] = result.get('d','')

                    #get action type
                    down_tuple['action'] = result.get('t','')

                    #get book id
                    down_tuple['book_id'] = result.get('u','')

                    #get ref uri
                    #down_tuple['ref'] = result['']

                    #get time
                    down_tuple['timestamp'] = result.get('x','')
                    table.put(str(row_key), down_tuple)
    finally:
        pass


if __name__ == '__main__':
    try:
        conn = happybase.Connection('localhost')
        table = conn.table('trail_tuple')
        f_o = open(log_path[0], 'r')
        f_n = open(log_path[1], 'r')
        parse_hb_oldlog(f_o, table)
        parse_hb_newlog(f_n, table)
    exception Exception:
        print "error!"
