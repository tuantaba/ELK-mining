from elasticsearch import Elasticsearch
import json, requests, sys
from datetime import datetime
from inputs import *

try:
    print("Try to connect to server", ELK_HOST)
    elastic_client = Elasticsearch([ELK_HOST], sniff_on_start=True, maxsize=250,TimeoutError=100, http_auth=(USERNAME, PASSWORD))
    print("Connection to ES Server successful")
except:
    print("Error: Unable to connect to server ", ELK_HOST)
    exit(1)    

def make_query(filter):    
    index_exists = elastic_client.indices.exists(index=INDEX_NAME)

    # check if the index exists
    if index_exists == True:
        try:        
            # pass filter query to the client's search() method
            response = elastic_client.search(index=INDEX_NAME, body=filter)
            # print the query response
            print ('response["hits"]:', len(response["hits"]))
            print ('response TYPE:', type(response))
            # print (response)
            
        except Exception as err:
            print ("search(index) ERROR", err)
            response = {"error": err}
    # return an empty dict if index doesn't exist
    else:
        response = {}
    return response

