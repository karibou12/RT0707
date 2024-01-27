from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import pymongo
from bson import ObjectId


#***************************     mongodb       **************************

myclient = pymongo.MongoClient('mongodb://172.20.0.1', 27017, username="root", password='1toto;2')
mydb = myclient["Billetterie"]

     

app = Flask(__name__)

# MQTT settings
MQTT_BROKER = "172.20.0.10"
MQTT_PORT = 1883
MQTT_TOPIC = "QR/topic"

# Callback when message is received
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    # print(f"Received message: {payload}")
    billetId = payload
    print(f' recu de mqtt ##{billetId}##')


            
    mycol = mydb["billets"]
    dbrequest = {"_id": ObjectId(str(billetId))}
    liste = mycol.find(dbrequest)

    for x in liste:
        valid = x['isValid']
        print(f'Valid de la boucle')

    if valid == 'true':
        print(f'le billet est utilisé. il ne sera plus valide')
        requete = {"_id": ObjectId(str(billetId))}
        print('proutt')
        modif = { "$set" : {"isValid":'false'}}
        mycol.update_one(requete,modif)
    else:
        print('le billet est déja utilisé')




# Connect to MQTT broker and subscribe to topic
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC)
mqtt_client.loop_start()

@app.route('/')
def index():
    return jsonify({'status': 'Flask server is running'})

if __name__ == '__main__':
    app.run(debug=True, port=5050)
