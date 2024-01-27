from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from pyzbar.pyzbar import decode
from PIL import Image
import paho.mqtt.client as mqtt
import os
from flask import Flask, render_template, send_from_directory


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


class QRCodeForm(FlaskForm):
    qrcode_image = FileField(validators=[FileRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = QRCodeForm()

    if form.validate_on_submit():
        # Sauvegarde du fichier téléchargé
        qrcode_image = form.qrcode_image.data
        filename = secure_filename(qrcode_image.filename)
        filepath = app.config['UPLOAD_FOLDER'] + '/' + filename
        qrcode_image.save(filepath)

        # Lecture du QR code
        decoded_objects = decode(Image.open(filepath))
        data = [obj.data.decode("utf-8") for obj in decoded_objects]

        return render_template('result.html', data=data)

    return render_template('index.html', form=form)


@app.route('/qr', methods=['GET', 'POST'])
def qr():
    # form = QRCodeForm()
    files = os.listdir(app_folder)

      

    return render_template('lecteur.html', files = files)




@app.route('/decodeQr/<qr>', methods=['GET','POST'])
def decode_qr(qr):
    qr = decode(Image.open(f'{app_folder}/{qr}'))
    # print(img)
    # print("----")
    # print("data {}, type {}".format(img[0].data,type(img[0].data)))
    # print("------")
    # print("data décodée {}, type {}".format(img[0].data.decode(), type(img[0].data.decode())))
    id =qr[0].data.decode()
    
    # id = json.dumps(id)
    data = id.split(',')
    data = data[0][8:]

    
    mqtt_client.publish(mqtt_topic, data)

    
    return render_template('qr.html', id= id, data = data)











@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        message = request.form['message']
        mqtt_client.publish(mqtt_topic, message)
        return "Message sent successfully!"














if __name__ == '__main__':
    app.run(debug=True)