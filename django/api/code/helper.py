from pymongo import  MongoClient
import json
from bson import json_util

# está usando a misma config cuidao
from packets.configuration.mongo import *

def upload_mongo(data):
    mongo_url = "mongodb://"+MONGO_USER+":"+MONGO_PASSWORD+"@"+MONGO_HOST+":"+MONGO_PORT+"/"+MONGO_DB+"?authSource="+MONGO_AUTH_SOURCE
    connection = MongoClient(mongo_url)
    packet_db = connection[MONGO_DB]
    packetcollection = packet_db[MONGO_COLLECTION]
    try:
        for packet in data:
            packet = json.loads(json_util.dumps(packet))
            packetcollection.insert_one(packet)
    except Exception as e:
        print("ERROR UPLOADING PACKETS: ", e)

