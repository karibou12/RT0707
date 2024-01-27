from flask import Flask, render_template, redirect, url_for, request, jsonify
from pyzbar.pyzbar import decode
from PIL import Image
import paho.mqtt.client as mqtt
import os
from flask import Flask, render_template, send_from_directory

#QR folerd
docker_folder = os.path.abspath(os.getcwd())
app_folder = os.path.join(docker_folder, 'data')

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

# MQTT settings
mqtt_broker = "172.20.0.10"
mqtt_port = 1883
mqtt_topic = "QR/topic"

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")

# Set up the MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Start the MQTT client loop in a separate thread
mqtt_client.loop_start()

#specify img path
@app.route('/images/<filename>')
def get_image(filename):
    images_folder = '/app/data/'
    return send_from_directory(images_folder, filename)

#QR reader
@app.route('/', methods=['GET', 'POST'])
def qr():
    files = os.listdir(app_folder)
   
    return render_template('lecteur.html', files = files)


#QR decoder
@app.route('/decodeQr/<qr>', methods=['GET','POST'])
def decode_qr(qr):
    qrd = decode(Image.open(f'{app_folder}/{qr}'))
    id =qrd[0].data.decode()
    
    data = id.split(',')
    data = data[0][8:]
      
    #send to Mosquitto broker
    mqtt_client.publish(mqtt_topic, data)

    #remove QR
    os.remove(f'{app_folder}/{qr}')

         
    return redirect(url_for('qr'))


if __name__ == '__main__':
    app.run(debug=True)