from inputs import *
import alert
import json
#import search


JSONFILE = "prom_exporter/output_network.json"
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

def analyze(search_param ):
    try:
        print ("Quering..")
        response =  search.make_query(search_param)
    except Exception as e:
        print ("Exception: ", e)
        msg =  msg_when_elk_query_fail(e)
        # alert.send_telegram(msg, CHAT_ID_FOR_ADMIN)

    msg_list = [] # List intialization

    print (response)
    len_hit=len(response['hits']['hits'])
    print ("len_hit is : ", len_hit)
    if len(response['hits']['hits']) == 0:
        print ("The query with no matched line, exit analyze() function...")
        # exit()

    print ("Analyzing..")

    result_dics = {}  #inital dics()
    for log in response['hits']['hits']:
        print ("----")
        print (log)
        
    #     #need to edit
    #     print (log)
        # print ("print _source")
        # print(log["_source"])


        # try:
        #     PROBE_HOSTNAME =  log["_source"]['deviceHostName']            
        # except:
        #     PROBE_HOSTNAME = "null"        
        # try:
        #     DEST_GROUP =  log["_source"]['taskName']
        # except:
        #     DEST_GROUP = "null"
                    
        # try:
        #     LATENCY =  log["_source"]['summary']['latency']
        # except:
        #     LATENCY = "null"

        # try:
        #     LOSS_PERCENT =  log["_source"]['summary']['packetLossPercent']
        # except:
        #     LOSS_PERCENT = "null"

        # if DEST_GROUP != "null":

        #     DEST_GROUP=DEST_GROUP.split("-")[0]            

        #     result_dics['PROBE_HOSTNAME'] = PROBE_HOSTNAME            
        #     result_dics['DEST_GROUP'] = DEST_GROUP        
        #     result_dics['LATENCY'] = LATENCY       
        #     result_dics['LOSS_PERCENT'] = LOSS_PERCENT


        #     print (PROBE_HOSTNAME)
        #     print (DEST_GROUP)
        #     print (LATENCY)
        #     print (LOSS_PERCENT)
        #     print(result_dics)

        #     #rename sgn_ping_to_zabbix_proxy-20221212T1503  -> sgn_ping_to_zabbix_proxy, cut  -

        #     with open(JSONFILE, "a+") as file:
        #         file.write(json.dumps(result_dics))
        #         file.write (",")
        #         file.close()

def main():
    analyze(epayment_event)

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