from flask import Flask, request, jsonify, flash
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
import requests
import pymongo
import qrcode



app = Flask(__name__)
app.config['SECRET_KEY'] = 'dashboardSecret'


# Fonction pour générer le token JWT
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # expiration time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


#***************************     mongodb       **************************

myclient = pymongo.MongoClient('mongodb://10.11.10.49', 27017, username="root", password='1toto;2')
mydb = myclient["Billetterie"]


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        error = None

        mycol = mydb["users"]
        dbrequest = {"username":username,"password":password}
        liste = mycol.find(dbrequest)
        
        for elem in liste:
            user = elem['username']
            passw = elem['username']

        if user is None:
            error = 'Incorrect username.'

        elif not (passw, password):
            error = 'Incorrect password.'
            return jsonify({'message': 'User connecté'}),401

        if error is None:   
            token = generate_token(user)
            return jsonify({'token': token, 'token_id': user})
        
        flash(error)
    return jsonify({'message': 'user connecter'})


@app.route('/userinfo/<user_id>', methods=['GET'])
def get_userinfo(user_id):

    mycol = mydb["users"]
    dbrequest = { 'username': user_id}
    liste = mycol.find(dbrequest)
    for elem in liste:
        data = {
        'username': elem['username']
        }


    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")  
    
    def dashData(type ,param):
        mycol = mydb["billets"]
        dbrequest = { type: {"$eq": param}}
        liste = mycol.find(dbrequest)

        result = 0 
        for _ in liste:
            result += 1
        return result
        
    data = []
    data.append(
        {
        'buyToday': dashData('dateAchat' , today),
        'totalBunit': dashData('Type' , 'Bunit'),
        'totalBjour': dashData('Type' , 'Bjour'),
        'totalValid': dashData('valid' , 'true'),
        
        })

    return (data[0])



# GET Billets Achatés
@app.route('/buyToday', methods=['GET'])
def get_buyToday():
        
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")  
     
    mycol = mydb["billets"]
    dbrequest = { 'dateAchat': {"$eq": today}}
    liste = mycol.find(dbrequest)
    
    buyToday = 0 
    for _ in liste:
            buyToday= buyToday+ 1

    return jsonify({'data': buyToday })
 

if __name__ == '__main__':
    app.run(debug=True, port=5001)
