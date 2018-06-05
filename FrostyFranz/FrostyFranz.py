from __future__ import print_function
import sqlite3
import paho.mqtt.client as mqtt
import csv
import datetime
import os
import json
import requests
import sys
from kafka import KafkaProducer
from kafka import SimpleProducer, KafkaClient

smartaqnetHome = os.getenv('smartaqnethome','localhost')
#smartaqnetHome = 'localhost'

def on_connect(client, userdata, flags, rc):
     print ('Starting to log data.')
    
     client.subscribe("v1.0/Things")
     client.subscribe("v1.0/Datastreams")
#     client.subscribe("v1.0/#")
     client.subscribe("v1.0/Locations")
     client.subscribe("v1.0/HistoricalLocations")
     client.subscribe("v1.0/Sensors")
     client.subscribe("v1.0/ObservedProperties")
     client.subscribe("v1.0/FeatureOfInterests")
     client.subscribe("v1.0/Observations")

     if rc==0:
	 print('connection established')

     else:
         print('Bad connection (return code = %d).' % rc)

def on_message(client, userdata, msg):
    payload = msg.payload
    topic = msg.topic.split('/')[-1]

    print("Receiving new message with topic: " + topic)

    data = json.loads(payload.decode("utf-8"))

    iot_id = data.get('@iot.id')
    print(iot_id)
    producer.send(topic, key= str(iot_id), value=data)
    producer.flush()


kafka = KafkaClient( smartaqnetHome +':9092')

#producer = SimpleProducer(kafka, async=True)
#producer.send_messages(b'my-topic', b'async message')
producer = KafkaProducer(bootstrap_servers=smartaqnetHome + ':9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'), compression_type='lz4')

#producer.send('fizzbuzz', key= 'uid', value={'foo': 'bar'})
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(smartaqnetHome, 1883, 60)
client.loop_forever()

