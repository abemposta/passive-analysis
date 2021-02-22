import pymongo
from pymongo import MongoClient
from bson import json_util
from datetime import datetime
from packets.configuration.mongo import *

# Input: database name
# Output: Mongo connection to db name
def _get_connection(db_name):
    mongo_url = "mongodb://"+MONGO_USER+":"+MONGO_PASSWORD+"@"+MONGO_HOST+":"+MONGO_PORT+"/"+MONGO_DB+"?authSource="+MONGO_AUTH_SOURCE
    connection = MongoClient(mongo_url)
    db = connection[db_name]
    return db

# Input: mongo connection to db, collection name
# Output: Requested mongo collection
def _get_collection(db, collection_name):
    collection = db[collection_name]
    return collection

# Input: mongo db name and collection name 
# Output: environments found
# Output TYPE: LIST
def get_env_list(db_name, collection_name):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    env_list = packets.distinct("environment")
    return env_list

# Input: mongo db name, collection name and environment
# Output: Packets found with protocol
# Output TYPE: LIST
def get_mac_manufacturer(db_name, collection_name, environment, mac, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    filtered_packets = packets.find({ "environment": environment, "mac": mac, "timestamp": { "$gte": inidate, "$lte": enddate }}).limit(1)
    try:
        manufacturer = filtered_packets[0]["eth"]["src_oui_resolved"]
        return manufacturer
    except Exception:
        return None

# Input: mongo db name, collection name and environment
# Output: Packets found with protocol
# Output TYPE: LIST
def get_mac_list(db_name, collection_name, environment, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    filtered_packets = packets.find({ "environment": environment, "timestamp": { "$gte": inidate, "$lte": enddate }})
    mac_list = filtered_packets.distinct("mac")
    return mac_list

# Input: mongo db name, collection name and environment
# Output: Packets found with protocol
# Output TYPE: LIST
def get_protocol_list(db_name, collection_name, environment, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    filtered_packets = packets.find({ "environment": environment, "timestamp": { "$gte": inidate, "$lte": enddate }})
    protocol_list = filtered_packets.distinct("protocol")
    return protocol_list

# Input: Any list of packets
# Output: Number of packets in the list
# Output TYPE: NUMBER
def count_env_packets(db_name, collection_name, environment, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    count = packets.count_documents({ "environment": environment, "timestamp": { "$gte": inidate, "$lte": enddate } })
    return count

# Input: Any list of packets
# Output: Number of packets in the list
# Output TYPE: NUMBER
def count_mac_packets(db_name, collection_name, environment, mac, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    count = packets.count_documents({ "environment": environment, "mac": mac, "timestamp": { "$gte": inidate, "$lte": enddate } })
    return count

# Input: mongo db name and collection name, environment, protocol and date interval
# Output: Number of packets of protocol in the selected environment and time interval
# Output TYPE: NUMBER
def count_protocol_packets(db_name, collection_name, environment, proto, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    count = packets.count_documents({ "environment": environment, "protocol": proto.upper(), "timestamp": { "$gte": inidate, "$lte": enddate }})
    return count

# Input: mongo db name, collection name and protocol
# Output: Packets found with protocol
# Output TYPE: CURSOR
def count_layer_packets(db_name, collection_name, environment, layer, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    layer = layer.lower()
    layer_count = packets.count_documents({ layer: { "$exists": True, "$ne": "null" }, "environment": environment, "timestamp": { "$gte": inidate, "$lte": enddate }})
    return layer_count

# Input: Any list of packets
# Output: Number of packets in the list
# Output TYPE: NUMBER
def count_protocol_mac_packets(db_name, collection_name, environment, mac, proto, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    count = packets.count_documents({ "environment": environment, "mac": mac, "protocol": proto.upper(), "timestamp": { "$gte": inidate, "$lte": enddate }})
    return count

# Input: Any cursor
# Output: Number of values in cursor
# Output TYPE: NUMBER
def count_cursor(cursor):
    count = cursor.count()
    return count

# Input: mongo cursor
# Output: Python list with values in cursor
# Output TYPE: PACKET LIST
def mongo_cursor_to_list(cursor):
    values = []
    for packet in cursor:
        values.append(packet)
    return values


# Input: List of packets, layer to find
# Output: TRUE if has layer, FALSE if not
# Output TYPE: BOOL
def has_layer(db_name, collection_name, environment, mac, layer, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    return packets.find_one({ "environment": environment, "mac": mac, layer: { "$exists": True}, "timestamp": { "$gte": inidate, "$lte": enddate }}) != None

# Input: mongo db name, collection name and environment
# Output: Packets found with protocol
# Output TYPE: CURSOR
def get_environment_packets(db_name, collection_name, environment, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    filtered_packets = packets.find({ "environment": environment, "timestamp": { "$gte": inidate, "$lte": enddate } })
    return filtered_packets


# Input: mongo db name, collection name and protocol
# Output: Packets found with protocol
# Output TYPE: CURSOR
def get_protocol_packets(db_name, collection_name, environment, protocol, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    protocol = protocol.upper()
    filtered_packets = packets.find({ "protocol": protocol, "environment": environment, "timestamp": { "$gte": inidate, "$lte": enddate }})
    return filtered_packets

# Input: mongo db name, collection name and protocol
# Output: Packets found with protocol
# Output TYPE: CURSOR
def get_layer_packets(db_name, collection_name, environment, layer, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    layer = layer.lower()
    filtered_packets = packets.find({ layer: { "$exists": True, "$ne": "null" }, "environment": environment, "timestamp": { "$gte": inidate, "$lte": enddate }})
    return filtered_packets

# Input: mongo db name, collection name and mac
# Output: Packets found with protocol
# Output TYPE: CURSOR
def get_mac_packets(db_name, collection_name, environment, mac, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    filtered_packets = packets.find({ "environment": environment, "mac": mac,  "timestamp": { "$gte": inidate, "$lte": enddate }})
    return filtered_packets

# Input: mongo db name, collection name and mac
# Output: Packets found with protocol
# Output TYPE: CURSOR
def get_mac_protocol_packets(db_name, collection_name, environment, mac, protocol, inidate, enddate):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    filtered_packets = packets.find({ "environment": environment, "mac": mac, "protocol": protocol, "timestamp": { "$gte": inidate, "$lte": enddate }})
    return filtered_packets

# Input: mongo db name, collection name, env and date
# Output: Next packet after date
# Output TYPE: packet
def get_next_env_packet(db_name, collection_name, environment, date):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    packet = packets.find_one({ "environment": environment, "timestamp": { "$gt": date}})
    return packet

# Input: mongo db name, collection name, env and date
# Output: Next packet after date
# Output TYPE: packet
def get_prev_env_packet(db_name, collection_name, environment, date):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    packet = packets.find_one({ "environment": environment, "timestamp": { "$lt": date}})
    return packet

# Input: mongo db name, collection name, env and date
# Output: Next packet after date
# Output TYPE: packet
def get_next_mac_packet(db_name, collection_name, environment, mac, date):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    packet = packets.find_one({ "environment": environment, "mac": mac,"timestamp": { "$gt": date}})
    return packet

# Input: mongo db name, collection name, env and date
# Output: Next packet after date
# Output TYPE: packet
def get_prev_mac_packet(db_name, collection_name, environment, mac, date):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    packet = packets.find_one({ "environment": environment, "mac": mac,"timestamp": { "$lt": date}})
    return packet


# Input: list of packets, datetime of start and datetime of end
# Output: Packets filtered by datetime
# Output TYPE: PACKET LIST
def filter_packets_by_date(packets, ini_date, end_date):
    filtered_packets = []
    for packet in packets:
        date_str = packet["timestamp"]
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        if (date > ini_date and date < end_date):
            filtered_packets.append(packet)
    return filtered_packets

# Input: List of packets, mac to filter
# Output: The list of packets from mac
# Output TYPE: PACKET LIST
def filter_by_mac(packets, mac):
    values = []
    for packet in packets:
        if ( mac == packet["eth"]["src"] ):
            values.append(packet)
    return values

# Input: List of packets, layer to filter
# Output: The list of packets with layer
# Output TYPE: PACKET LIST
def filter_by_protocol_layer(packets, layer):
    layer = layer.lower()
    values = []
    for packet in packets:
        if ( layer in packet ):
            values.append(packet)
    return values

# Input: List of packets, layer and list of fields
# Output: All values fields located layer
# Output TYPE: FIELD VALUE LIST
def get_protocol_layer_field(packets, layer, fields):
    values = []
    for packet in packets:
        for field in fields:
            if ( layer in packet ):
                if ( field in packet[layer] ):
                    values.append(packet[layer][field])
    return values


# Input: List of packets, layer and list of fields
# Output: All unique values fields located layer
# Output TYPE: FIELD VALUE LIST
def get_protocol_layer_field_unique(packets, layer, fields):
    values = []
    for packet in packets:
        for field in fields:
            try:
                if (packet[layer][field] not in values):
                    values.append(packet[layer][field])
            except KeyError:
                pass
    return values

# Input: Any list of packets
# Output: Number of packets in the list
# Output TYPE: NUMBER
def count_packet_list(packets):
    return len(packets)

# Input: Env name
# Output: Oldest timestamp
# Output TYPE: Datetime
def get_oldest_packet(db_name, collection_name):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    timestamp_cursor = packets.find().sort('timestamp', pymongo.ASCENDING).limit(1)
    time_list = mongo_cursor_to_list(timestamp_cursor)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: Env name
# Output: Oldest timestamp
# Output TYPE: Datetime
def get_oldest_env_packet(db_name, collection_name, env):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    timestamp_cursor = packets.find({ "environment": env }).sort('timestamp', pymongo.ASCENDING).limit(1)
    time_list = mongo_cursor_to_list(timestamp_cursor)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: Env name, protocol
# Output: Oldest timestamp
# Output TYPE: Datetime
def get_oldest_protocol_packet(db_name, collection_name, env, protocol):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    timestamp_cursor = packets.find({ "environment": env, "protocol": protocol }).sort('timestamp', pymongo.ASCENDING).limit(1)
    time_list = mongo_cursor_to_list(timestamp_cursor)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: Env name
# Output: Oldest timestamp
# Output TYPE: Datetime
def get_oldest_mac_packet(db_name, collection_name, env, mac):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    timestamp_cursor = packets.find({ "environment": env, "mac": mac }).sort('timestamp', pymongo.ASCENDING).limit(1)
    time_list = mongo_cursor_to_list(timestamp_cursor)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: Env name
# Output: Oldest timestamp
# Output TYPE: Datetime
def get_oldest_protocol_mac_packet(db_name, collection_name, env, protocol, mac):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    timestamp_cursor = packets.find({ "environment": env, "protocol": protocol ,"mac": mac }).sort('timestamp', pymongo.ASCENDING).limit(1)
    time_list = mongo_cursor_to_list(timestamp_cursor)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: Env name
# Output: Newest timestamp
# Output TYPE: Datetime
def get_newest_packet(db_name, collection_name):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    time_list = packets.find().sort('timestamp', pymongo.DESCENDING).limit(1)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: Env name
# Output: Newest timestamp
# Output TYPE: Datetime
def get_newest_env_packet(db_name, collection_name, env):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    time_list = packets.find({ "environment": env }).sort('timestamp', pymongo.DESCENDING).limit(1)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: Env name
# Output: Newest timestamp
# Output TYPE: Datetime
def get_newest_protocol_packet(db_name, collection_name, env, protocol):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    time_list = packets.find({ "environment": env, "protocol": protocol }).sort('timestamp', pymongo.DESCENDING).limit(1)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: Env name
# Output: Newest timestamp
# Output TYPE: Datetime
def get_newest_mac_packet(db_name, collection_name, env, mac):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    time_list = packets.find({ "environment": env, "mac": mac }).sort('timestamp', pymongo.DESCENDING).limit(1)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: Env name
# Output: Newest timestamp
# Output TYPE: Datetime
def get_newest_protocol_mac_packet(db_name, collection_name, env, protocol, mac):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    time_list = packets.find({ "environment": env, "protocol": protocol,"mac": mac }).sort('timestamp', pymongo.DESCENDING).limit(1)
    try:
        datetimeObj = datetime.strptime(time_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        return datetimeObj
    except IndexError:
        return None

# Input: mongo db name, collection name and protocol
# Output: Packets found with protocol
# NOTE: Testing only
def __get_all_packets(db_name, collection_name):
    db = _get_connection(db_name)
    packets = _get_collection(db, collection_name)
    all_packets = packets.find()
    return all_packets

