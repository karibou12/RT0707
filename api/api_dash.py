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


# print(mydb.list_collection_names())


#***************************     USERS       **************************

#User Routes
# @app.route('/users', methods=['GET'])
# def get_users():
#     cursor.execute('SELECT * FROM users')
#     users = cursor.fetchall()
#     return jsonify({'users': users})


# @app.route('/user/<user_id>', methods=['GET'])
# def get_user(user_id):
#     cursor.execute('SELECT * FROM users WHERE username = ?', (user_id,))
#     user = cursor.fetchone()
#     if user:
#         return jsonify({'user': user})
#     else:
#         return jsonify({'message': 'User not found'}), 404



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
        
    # dbrequest = { 'username':user_id}
    # liste = mycol.find(dbrequest)
    # data = []
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


















# @app.route('/user/<user_id>', methods=['GET','PUT'])
# def update_user(user_id):
#     data = request.get_json()
#     email = data['email']
#     password = data['password']
#     cursor.execute('UPDATE users SET email = ?, password = ? WHERE username = ?', (email,generate_password_hash(password), user_id))
#     conn.commit()
#     return jsonify({'message': 'User updated successfully'})


# @app.route('/user/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     cursor.execute('DELETE FROM users WHERE username = ?', (user_id,))
#     conn.commit()
#     return jsonify({'message': 'User deleted successfully'})



# #************************* Billet ************************************


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
        

# requete = { 'username':'gui'}
# liste = mycol.find(requete)


# # GET film
# @app.route('/film/<int:film_id>', methods=['GET'])
# def get_film(film_id):
#     cursor.execute('SELECT * FROM films WHERE id = ?', (film_id,))
#     film = cursor.fetchone()

#     if film:
#         return jsonify({'film': film})
#     else:
#         return 'Film introuvable', 404
    
 


# # # Add Bunit
# @app.route('/addBillet', methods=['GET', 'POST'])
# def create_Billet():

#     if request.method == 'POST':
#         data = request.get_json()

#         # dateAchat= datetime.datetime.utcnow().strftime("%Y-%m-%d")

#         dbrequest = {"username": data['username']}
       
#         mycol = mydb["users"]
#         liste = mycol.find(dbrequest)
#         for elem in liste:
#             Bunit = elem['Bunit']
#             Bjour = elem['Bjour']
            
#         Bunit += int(data['NbBunit'])
#         Bjour += int(data['NbBjour'])

#         modif = { "$set" : {"Bunit": Bunit, "Bjour": Bjour}}
#         mycol.update_one(dbrequest,modif)


  
#         def create_and_generate_qr(mycol, data, Btype):
#             dateAchat= datetime.datetime.utcnow().strftime("%Y-%m-%d")
#             # Insérer un billet
#             billet_data = {"username": data['username'], "dateAchat": dateAchat, "valid": "true", "Type": Btype}
#             mycol.insert_one(billet_data)
            
#             # Récupérer le dernier billet
#             dbrequest = {'username': data['username']}
#             sort_criteria = [("_id", -1)]
#             last_billet = mycol.find_one(dbrequest, sort=sort_criteria, projection=None)
            
#             # Générer le code QR
#             img = qrcode.make(f"{{'_id': {last_billet['_id']}, 'username': '{data['username']}', 'dateAchat': '{last_billet['dateAchat']}', 'Type': '{Btype}'}}")
          
#             img.save(f"./data/{data['username']}_{Btype}_{last_billet['dateAchat']}_{last_billet['_id']}.png")
            

#         if int(data['NbBunit']) > 0:
#             for _ in range(int(data['NbBunit'])):
#                 create_and_generate_qr(mydb["billets"], data,'Bunit')

     
#         if int(data['NbBjour']) > 0:
           
#             for i in range(int(data['NbBjour'])):
#                 create_and_generate_qr(mydb["billets"], data,'Bjour')
               

#         return jsonify({'message': 'Billet Unitaire Créer'}),201
#     else:
#         return jsonify({'message': 'Film deja existant'}),404














# # Add film
# @app.route('/addfilm', methods=['GET', 'POST'])
# def create_film():

#     if request.method == 'POST':
#         data = request.get_json()
#         id = data['id']
#         headers = {
#             "accept": "application/json",
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2I1NGViM2Q0ZTQyODVkZGUxODFmNGVjMzNjM2RmMyIsInN1YiI6IjY1OTAxMDc0NjRmNzE2NjVkNjhlYThiZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DGoyIxj4tfOLEbFjyFNZIUoKSLMPdNJGzyV4FpJtIGY"
#         }

#         url = "https://api.themoviedb.org/3/movie/" + id +"?language=fr-FR"
#         response = requests.get(url, headers=headers)
#         data = response.json()

#         url2 = "https://api.themoviedb.org/3/movie/" + id + "/credits?language=fr-FR"
#         response = requests.get(url2, headers=headers)
#         data2 = response.json()

#         titre=data['title']
#         genre = data['genres'][0]['name']
#         annee = data['release_date']
#         affiche = "https://image.tmdb.org/t/p/w500" + data['poster_path']
#         realisateur = data2['crew'][0]['name']
#         acteur1 = data2['cast'][0]['name']
#         acteur2 = data2['cast'][1]['name']
#         acteur3 = data2['cast'][2]['name']

                
#         cursor.execute('SELECT films.titre FROM films WHERE titre = ?',(titre,))
#         titredb = cursor.fetchone()
#         if titredb == None:
#             titredb = ''
#         else:
#             titredb = titredb[0]
               
#         if titre != titredb:
#             cursor.execute('INSERT INTO films (titre, genre, annee, realisateur, affiche, acteur1, acteur2, acteur3) VALUES (?, ?, ?, ?,?,?,?,?)', (titre, genre, annee, realisateur, affiche, acteur1, acteur2, acteur3 ))
#             conn.commit()
        
#             return jsonify({'message': 'Film created successfully'}),201
#         else:
#             return jsonify({'message': 'Film deja existant'}),404


















# @app.route('/film/<int:film_id>', methods=['GET','PUT'])
# def update_film(film_id):
#     data = request.get_json()
#     genre = data['genre']
#     annee = data['annee']
#     realisateur = data['realisateur']
#     affiche = data['affiche']
#     cursor.execute('UPDATE films SET genre = ?, annee = ?, realisateur = ?, affiche = ? WHERE id = ? ', (genre, annee, realisateur, affiche, film_id))
#     conn.commit()

#     return jsonify({'message': 'Film updated successfully'})


# @app.route('/film/<int:film_id>', methods=['DELETE'])
# def delete_film(film_id):
#     cursor.execute('DELETE FROM films WHERE id = ?', (film_id,))
#     conn.commit()
#     return jsonify({'message': 'Film deleted successfully'})



# # Search films
# @app.route('/search', methods=['GET', 'POST'])
# def search_film():
#     if request.method == 'POST':
#         data = request.get_json()
#         titre = data['titre']

#         url = f'https://api.themoviedb.org/3/search/movie?query={titre}&include_adult=false&language=fr-FR&page=1'

#         headers = {
#             "accept": "application/json",
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2I1NGViM2Q0ZTQyODVkZGUxODFmNGVjMzNjM2RmMyIsInN1YiI6IjY1OTAxMDc0NjRmNzE2NjVkNjhlYThiZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DGoyIxj4tfOLEbFjyFNZIUoKSLMPdNJGzyV4FpJtIGY"
#         }

#         response = requests.get(url, headers=headers)

#         data = response.json()
         
#         return jsonify(data = data["results"])
    
#     return jsonify({'message': 'Film inexistant'}),404


# #*************************  USER FILMS  ******************************************

# # GET userfilms
# @app.route('/<user_id>/films', methods=['GET'])
# def get_userfilms(user_id):
#     cursor.execute('SELECT * from films INNER JOIN userfilms ON userfilms.film_id = films.titre WHERE userfilms.user_id = ? ORDER BY "titre"', (user_id,))
#     films = cursor.fetchall()
#     return jsonify({'films': films})


# # GET userfilm
# @app.route('/<user_id>/film/<int:film_id>', methods=['GET'])
# def get_userfilm(user_id,film_id):
#     cursor.execute('SELECT * from films INNER JOIN userfilms ON userfilms.film_id = films.titre WHERE userfilms.id = ?', (film_id,))
#     films = cursor.fetchall()
#     return jsonify({'films': films})


# # Add user film
# @app.route('/<user_id>/addfilm', methods=['GET', 'POST'])
# def create_userfilm(user_id):

#     if request.method == 'POST':
#         data = request.get_json()
#         id = data['id']

#         headers = {
#             "accept": "application/json",
#             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmM2I1NGViM2Q0ZTQyODVkZGUxODFmNGVjMzNjM2RmMyIsInN1YiI6IjY1OTAxMDc0NjRmNzE2NjVkNjhlYThiZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.DGoyIxj4tfOLEbFjyFNZIUoKSLMPdNJGzyV4FpJtIGY"
#         }

#         url = "https://api.themoviedb.org/3/movie/" + id +"?language=fr-FR"
#         response = requests.get(url, headers=headers)
#         data = response.json()

#         url2 = "https://api.themoviedb.org/3/movie/" + id + "/credits?language=fr-FR"
#         response = requests.get(url2, headers=headers)
#         data2 = response.json()

#         titre=data['title']
#         genre = data['genres'][0]['name']
#         annee = data['release_date']
#         affiche = "https://image.tmdb.org/t/p/w500" + data['poster_path']
#         realisateur = data2['crew'][0]['name']
#         acteur1 = data2['cast'][0]['name']
#         acteur2 = data2['cast'][1]['name']
#         acteur3 = data2['cast'][2]['name']

#         cursor.execute('SELECT userfilms.film_id FROM userfilms WHERE user_id = ?',(user_id,))
#         film_id= cursor.fetchall()

#         for i in film_id:
#             if titre == i[0]:
#                 film_id = i[0]
#                 break
            
#         cursor.execute('SELECT films.titre FROM films WHERE titre = ?',(titre,))
#         titredb = cursor.fetchone()
#         if titredb == None:
#             titredb = ''
#         else:
#             titredb = titredb[0]
       
#         if titre != film_id:
#             cursor.execute('INSERT INTO userfilms (user_id, film_id) VALUES (?, ?)', (user_id,titre))
#             conn.commit()
        
#         if titre != titredb:
#             cursor.execute('INSERT INTO films (titre, genre, annee, realisateur, affiche, acteur1, acteur2, acteur3) VALUES (?, ?, ?, ?,?,?,?,?)', (titre, genre, annee, realisateur, affiche, acteur1, acteur2, acteur3 ))
#             conn.commit()
        
#         return jsonify({'message': 'Film created successfully'}),201
#     else:
#         return jsonify({'message': 'Film deja existant'}),404


# # DELETE userfilm
# @app.route('/<user_id>/film/<int:film_id>', methods=['DELETE'])
# def delete_userfilm(user_id,film_id):

#     cursor.execute('DELETE FROM userfilms WHERE  user_id = ? AND id = ?', (user_id,film_id))
#     conn.commit()

#     return jsonify({'message': 'Film deleted successfully'})




if __name__ == '__main__':
    app.run(debug=True, port=5001)
