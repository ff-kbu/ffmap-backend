#!/usr/bin/env python3
import argparse
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('registerNodesjson', help='http://register.kbu.freifunk.net/nodes.json')

args = parser.parse_args()

options = vars(args)

with open(options['registerNodesjson'], 'r') as f:
        content = f.read()
f.closed

scont = str(content)

try:
        jsonData = json.loads(scont)
except:
        sys.exit(0)

nodes = {'dump':'dump'}

for i in range(len(jsonData)):
        mac = jsonData[i]["node"]["mac"]
        mac = "{0}:{1}:{2}:{3}:{4}:{5}".format(mac[:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:12])
        name = jsonData[i]["node_registration"]["name"]
        gps = str(jsonData[i]["node_registration"]["latitude"])+" "+str(jsonData[i]["node_registration"]["longitude"])
        firmware = jsonData[i]["node"]["fw_version"]
        nodes[mac] = {"name": name, "gps": gps, "firmware": firmware}
        
print(json.dumps(nodes))

