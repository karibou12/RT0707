from flask import Flask, request, jsonify, flash
import jwt
import datetime
import requests
import pymongo
import qrcode



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# Token generator
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # expiration time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


#***************************     mongodb       **************************
myclient = pymongo.MongoClient('mongodb://172.20.0.1', 27017, username="root", password='1toto;2')
mydb = myclient["Billetterie"]



# sign up route
@app.route('/adduser', methods=['POST'])
def create_user():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        mycol = mydb["users"]
        mycol.create_index("username", unique=True)
        data1 = {"username": username , "email": email , "password" : password}
        mycol.insert_one(data1)
        
        return jsonify({'message': 'Utilisateur créé'}),201
    else:
        return jsonify({'message': 'Utilisateur déja créé'}),500


#login route
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


# #************************* Compte ************************************

# GET specific user's info
@app.route('/userinfo/<user_id>', methods=['GET'])
def get_userinfo(user_id):
    mycol = mydb["users"]
    dbrequest = { 'username': user_id}
    liste = mycol.find(dbrequest)

    for elem in liste:
        data = {
        'username': elem['username']
        }

    def count_billet_type(Type,username):
        mycol = mydb["billets"]
        dbrequest = {'Type': {"$eq": Type}, 'username': username, 'isValid': 'true'}
        liste = mycol.find(dbrequest)
        count = 0
        for _ in liste:
            count += 1
        return count
    
    data.update({'Bunit': count_billet_type('Bunit',elem['username']), 
                 'Bjour': count_billet_type('Bjour',elem['username'])})
 
    return jsonify({'data': data})
    

# # Add billet
@app.route('/addBillet', methods=['GET', 'POST'])
def create_Billet():

    if request.method == 'POST':
        data = request.get_json()

        dbrequest = {"username": data['username']}
    
        mycol = mydb["users"]
        liste = mycol.find(dbrequest)
        try:
            for elem in liste:
                Bunit = elem['Bunit']
                Bjour = elem['Bjour']
                
            Bunit += int(data['NbBunit'])
            Bjour += int(data['NbBjour'])

            modif = { "$set" : {"Bunit": Bunit, "Bjour": Bjour}}
            mycol.update_one(dbrequest,modif)
        except Exception as e:
            print(e)
          
        def create_and_generate_qr(mycol, data, Btype):
            dateAchat= datetime.datetime.utcnow().strftime("%Y-%m-%d")
            # Insérer un billet
            billet_data = {"username": data['username'], "dateAchat": dateAchat, "isValid": "true", "Type": Btype}
            mycol.insert_one(billet_data)
            
            # Récupérer le dernier billet
            dbrequest = {'username': data['username']}
            sort_criteria = [("_id", -1)]
            last_billet = mycol.find_one(dbrequest, sort=sort_criteria, projection=None)
            
            # Générer le code QR
            img = qrcode.make(f"{{'_id': {last_billet['_id']}, 'username': '{data['username']}', 'dateAchat': '{last_billet['dateAchat']}', 'Type': '{Btype}'}}")
          
            img.save(f"./data/{data['username']}_{Btype}_{last_billet['dateAchat']}_{last_billet['_id']}.png")
            

        if int(data['NbBunit']) > 0:
            for _ in range(int(data['NbBunit'])):
                create_and_generate_qr(mydb["billets"], data,'Bunit')

     
        if int(data['NbBjour']) > 0:
            for _ in range(int(data['NbBjour'])):
                create_and_generate_qr(mydb["billets"], data,'Bjour')
               

        return jsonify({'message': 'Billet Unitaire Créer'}),201
    else:
        return jsonify({'message': 'Film deja existant'}),404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
