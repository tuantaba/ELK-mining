import sys, os, configparser

config_path = os.path.join(sys.path[0],'config.ini')
if not os.path.exists(config_path):
    raise Exception("Config file not found: {}".format(config_path))

config = configparser.RawConfigParser()
config.optionxform = lambda option: option
config.read(config_path)

TELEGRAM_TOKEN = config.get('telegram', 'TELEGRAM_TOKEN')
CHAT_ID = config.get('telegram', 'CHAT_ID')
CHAT_ID_FOR_ADMIN = config.get('telegram', 'CHAT_ID_FOR_ADMIN')

ELK_HOST = config.get('DE', 'ELK_HOST')
ELK_PORT = config.get('DE', 'ELK_PORT')
USERNAME = config.get('DE', 'USERNAME')
PASSWORD = config.get('DE', 'PASSWORD')

INDEX_NAME = config.get('DE', 'INDEX_NAME')
TIME_GET_LOG = config.get('DE', 'TIME_GET_LOG')

epayment_event = {
            'query': {
                "bool":{
                    "should":[                                
                        {"match_phrase_prefix": {"message": " epayment.fpt.com.vn"}}
                    ],            
                    "filter":[
                        {"range": {"@timestamp": {"gte": "now-" + TIME_GET_LOG}}}
                    ]
                }
            }
    } #end

# epayment_event = {
#             'query': {
#                 "bool":{
#                     "must":[                                
#                         {"match": {"programname": "rabbit"}},    