from __future__ import print_function
import sqlite3
import paho.mqtt.client as mqtt
import csv
import datetime
import os
import json
import requests
import sys

basepath = '/root/sftp/volumes/saqn/'
smartaqnetHome = 'smartaqnet-dev.teco.edu'
def on_connect(client, userdata, flags, rc):
     print ('Starting to log data.')
    
     client.subscribe("v1.0/Things")
     client.subscribe("v1.0/Datastreams")
     print ('Subscribed to Things and Datastreams.')
     #client.subscribe("v1.0/Locations")

     if rc==0:
         print('Connected OK (return code = %d).' % rc)
     else:
         print('Bad connection (return code = %d).' % rc)

def on_message(client, userdata, msg):
    payload = msg.payload
    topic = msg.topic.split('/')[-1]
    print("Receiving new message with topic: " + topic)

    data = json.loads(payload.decode("utf-8"))

    properties = data.get('properties',{})
    if not properties:
        print("WARNING: No properties specified, not creating a new path for Entity.", file=sys.stderr)
    else:
        uid = properties.get('@iot.id',{})
        if not uid: 
            print("WARNING: No @iot.id specified, not creating a new path for Entity.", file=sys.stderr)
        else:
            print(uid)
            path = None
            if uid[0] != '/':
                uid = '/' + uid
            if uid[-1] != '/':
                uid = uid + '/'
            if topic == 'Things':
                path = basepath + topic + uid
            elif topic == 'Datastreams':
                datastream_id = data.get('@iot.id')
                thing = json.loads(requests.get('http://' + smartaqnetHome +':8080/SensorThingsService/v1.0/Datastreams(%d)/Thing' % datastream_id).content)
                thing_uid = thing.get('properties',{}).get('@iot.id',{})
                if not thing_uid:
                    print("WARNING: Thing for datastream has no UID set, not creating a new path for Entity.", file=sys.stderr)
                    #thing_uid = thing.get('@iot.id')
                    path = None
                else:
                    if thing_uid[0] != '/':
                        thing_uid = '/' + thing_uid
                    if thing_uid[-1] != '/':
                        thing_uid = thing_uid + '/'
                    path = basepath + 'Things' + thing_uid + topic + uid
            if path:
                print("Creating path..." + path)
                if os.path.exists(path):
                    print("WARNING: Another Entity with the same name may already exist or a race condition already triggered path creation before!", file=sys.stderr)
                else:
                    os.makedirs(path)
                print('Setting permissions...')
                pathlist = os.path.relpath(path, basepath).split('/')
                walkpath = basepath
                for folder in pathlist:
                    walkpath = os.path.join(walkpath, folder)
                    os.chmod(walkpath, 0o744)
                    print(folder)
                fh = os.path.join(path, 'SensorThings.json') 
                print('Saving JSON into file...')
                with open(fh, 'w') as outfile:
                    outfile.write(msg.payload)
 

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(smartaqnetHome, 1883, 60)
client.loop_forever()

