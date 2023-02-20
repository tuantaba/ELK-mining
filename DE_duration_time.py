from inputs import *
import alert
import json
#import search


JSONFILE = "/home/fimadmin/ELK-mining/prom_exporter/output_epayment.json"
def msg_when_elk_query_fail(error):
    msg = "<strong> ELK query error</strong> \n" \
            "<pre><code> \n" \
            "{} \n" \
            "</code></pre>". format(str(error))
    return msg
try:
    import search  
    print("Try")
except Exception as e:
    print ("Exception: ", e)
    msg =  msg_when_elk_query_fail(e)
    # alert.send_telegram(msg, CHAT_ID_FOR_ADMIN)

def analyze(INDEX_NAME_DURATION_TIME, search_param ):
    try:
        print ("Quering..")
        response =  search.make_query(search_param)
    except Exception as e:
        print ("Exception: ", e)
        msg =  msg_when_elk_query_fail(e)
        # alert.send_telegram(msg, CHAT_ID_FOR_ADMIN)

    msg_list = [] # List intialization

    # print (response)
    COUNTER_ERROR=len(response['hits']['hits'])
    if len(response['hits']['hits']) == 0:
        print ("The query with no matched line, exit analyze() function...")
        exit()

    print ("Analyzing..")

    result_dics = {}  #inital dics()
    for log in response['hits']['hits']:
        print ("----")
        # print (log)
        print ("print _source")
        print(log["_source"])

        try:
            domain =  log["_source"]['url']['domain']
        except:
            domain = "null"

        try:
            path =  log["_source"]['url']['path']
        except:
            path = "null"

        try:
            method =  log["_source"]['http']['request']['method']
        except:
            method = "null"

        try:
            status_code =  log["_source"]['http']['response']['status_code']
        except:
            status_code = "null"

        Timestamp =  log["_source"]['@timestamp']
    #out of for
    if status_code != "null" :         
        msg = msg_for_http(domain,COUNTER_ERROR,status_code,method,path,Timestamp," ")        
        try:
            # print ("alert ! , length is ", len( response['hits']['hits'] ))
            print (msg)
            alert.send_telegram(msg, CHAT_ID_NORMAL)
            
        except Exception as e:
            print  ("Error", e)
            msg =  msg_when_elk_query_fail(e)
            alert.send_telegram(msg, CHAT_ID_FOR_ADMIN)
            pass

def fix_bug_send_telegram(_string):
    _string=_string.replace("<", "tag;")
    _string=_string.replace(">", "tag;")
    _string=_string.replace("&", "tag;")
    _string=_string.replace("#", "tag;")
    return _string

def msg_for_http(arg1, arg2, arg3, arg4, arg5, arg6, arg7):
    msg = "<strong>{}</strong> - {} error 5xx/1m \n" \
            "     http_code: {}\n" \
            "     http_method: {} \n" \
            "     http_url: {} \n" \
            "     Time: {} \n" \
            "<pre><code> \n" \
            "{}\n" \
            "</code></pre>". format(arg1,arg2,arg3,arg4,arg5,arg6,arg7)
    return msg

def main():
    analyze(epayment_duration_event)

if __name__ == "__main__":
    result_dics={} 

    file = open(JSONFILE, "a")
    file.seek(0)
    file.truncate()
    file.write ("[")
    file.close()

    main()

    print(result_dics) #finally print result query in dictionary format

    with open(JSONFILE, "a+") as file:
        file.write(json.dumps(result_dics))
        file.write ("]")
        file.close()    