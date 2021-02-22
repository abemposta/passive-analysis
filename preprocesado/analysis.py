#! /usr/bin/python3
import pyshark
import json
from bson import json_util
import argparse
import requests

UPLOAD_ENDPOINT = "/api/upload"
TOKEN_ENDPOINT = "/api/token-auth"
UPLOADNUM = 200

def upload_mongo(data, token, url):
    data = json.loads(json_util.dumps(data))
    headers = {'Authorization': 'Token '+ token}
    req_url = url + UPLOAD_ENDPOINT
    r = requests.post(url = req_url, json = data, headers=headers)
    print(r)



# Entrada: Archivo e tipo de tráfico a analizar
# Salida: Chamada a función que analiza un tipo de tráfico concreto
def mpacketanalysis(pcapfile, environment, token, url, uploadnum):

    try:
        capture = pyshark.FileCapture(pcapfile)
    except Exception as e:
        print("ERROR pcapfile not valid: ", e)
        exit(-1)

    packetlist = []
    try:
        for packet in capture:
            processd_packet = generic_analyze_packet(environment, packet, token, url)
            packetlist.append(processd_packet)
            # Upload UPLOADNUM packets
            if (len(packetlist) >= uploadnum):
                try:
                    upload_mongo(packetlist, token, url)
                    packetlist = []
                except Exception as e:
                    print("MONGO UPLOAD error: ", e)

    except Exception as e:
        print("Error analyzing some packet in a capture, maybe the capture has been cut short in the middle of a packet")
        print("Full error: ", e)

    # Upload remaining packets
    try:
        print("Uploading remaining packets")
        upload_mongo(packetlist, token, url)
    except Exception as e:
        print("Remaining packets could not be uploaded: ", e)



# Recibe: Unha única capa de un paquete
# Devolve: Json cos campos desa capa
def layer_analysis(layer):
    jlayer={}
    for attribute in layer.field_names:
        attribute_name = attribute
        if (attribute == ""):
            attribute_name = "extra"
        jlayer[attribute_name]=layer.get_field(attribute)
    return jlayer

# Entrada: pcap filtrado con paquetes dunha mac e un tipo de tráfico concreto, e un string con ese tipo de tráfico concreto
# Salida: chamada á función que analiza ese tipo de tráfico concreto
def generic_analyze_packet(environment, packet, token, url):

    # timestamp
    packet_datetime=packet.sniff_time
    timestamp = packet_datetime.isoformat()
    jpacket={}
    jpacket['timestamp'] = timestamp
    jpacket['protocol'] = packet.highest_layer
    jpacket['environment'] = environment
    jpacket['mac'] = packet.eth.src

    # Attributes
    for layer in packet.layers:
        jpacket[layer.layer_name]=layer_analysis(layer)

    return jpacket



def main():

    __author__ = 'a.bemposta@udc.es'
    parser = argparse.ArgumentParser(description='Passive analysis processor')
    parser.add_argument('-n', '--num-uploaded', help='Simultaneous packets to upload', required=False)
    parser.add_argument('-e','--environment',help='Name of the environment of the traffic', required=True)
    parser.add_argument('-t', '--token', help='Your auth token', required=True)
    parser.add_argument('-u', '--url', help='URL of your installation', required=True)
    parser.add_argument('-i', '--inputfile',help='PCAP to analyze', required=True)
    args = parser.parse_args()

    uploadnum = UPLOADNUM

    if (args.num_uploaded):
        try:
            uploadnum = int(args.num_uploaded)
        except ValueError as e:
            print("--num-uploaded must be int. Full error: ", e)
            exit(1)

    mpacketanalysis(args.inputfile, args.environment.lower(), args.token, args.url, uploadnum)

if __name__ == "__main__":
   main()
