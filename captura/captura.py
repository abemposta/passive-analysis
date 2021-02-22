#! /usr/bin/python3

import pyshark
import datetime
import argparse
from pathlib import Path

def capture_traffic (path, interface):
    date = datetime.datetime.now()
    datestr = date.strftime('%Y-%m-%dT%H:%M')
    file = path + "/" + "capture_" + datestr + "h.pcap"

    output = open(file, "w")
    time = 3600
    capture = pyshark.LiveCapture(interface=interface, output_file=file, bpf_filter="broadcast or multicast")
    capture.sniff(timeout=time)
    output.close()

def main():

    __author__ = 'a.bemposta@udc.es'
    parser = argparse.ArgumentParser(description='Passive analysis capturer')
    parser.add_argument('-p', '--path', help='Directory where captures will be saved', required=True)
    parser.add_argument('-i','--net-interface',help='Name of the network interface to capture', required=True)
    args = parser.parse_args()

    if (Path(args.path).is_dir()):
        capture_traffic(args.path, args.net_interface)
    else:
        print ("Enter a valid directory")



if __name__ == "__main__":
   main()
