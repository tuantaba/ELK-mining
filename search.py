from elasticsearch import Elasticsearch
import json, requests, sys
from datetime import datetime
from inputs import *

try:
    print("Try to connect to server", ELK_HOST)
    elastic_client = Elasticsearch([ELK_HOST], maxsize=9999, http_auth=(USERNAME, PASSWORD), verify_certs=False)
    print("Connection to ES Server successful")
except Exception as err:
    print("Error: Unable to connect to server ", ELK_HOST)
    print (err)
    exit(1)    

def make_query(INDEX_NAME, filter):        
    try:        
        # pass filter query to the client's search() method
        response = elastic_client.search(index=INDEX_NAME,body=filter,size=9999,track_total_hits=True, request_timeout=30)
        # print the query response
        print ('response["hits"]:', len(response["hits"]))
        print ('response TYPE:', type(response))
        # print (response)
        
    except Exception as err:
        print ("search(index) ERROR", err)
        response = {"error": err}
    return response

