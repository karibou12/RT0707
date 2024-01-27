import paho.mqtt.client as mqtt
import pymongo
from bson import ObjectId


#***************************     mongodb       **************************

myclient = pymongo.MongoClient('mongodb://172.20.0.1', 27017, username="root", password='1toto;2')
mydb = myclient["Billetterie"]

 

# MQTT settings
MQTT_BROKER = "172.20.0.10"
MQTT_PORT = 1883
MQTT_TOPIC = "QR/topic"

# # Callback when message is received
# def on_message(client, userdata, message):
#     payload = message.payload.decode("utf-8")
#     # print(f"Received message: {payload}")
#     billerId = payload
#     print(f' recu de mqtt {billerId}')


# ## a revoir
#     mycol = mydb["billet"]
#     dbrequest = {"_id": {"$eq" : billerId}}
#     liste = mycol.find(dbrequest)
#     for elem in liste:
#             print(elem)
                        
        


mycol = mydb["billets"]
billet_id = '65aa9794de12cfd9db4bb716'
dbrequest = {"_id": ObjectId(billet_id)}
liste = mycol.find(dbrequest)

for elem in liste:
    print(elem['valid'])

# def count_billet_type(Type,username):
#     dbrequest = {'Type': {"$eq": Type}, 'username': username}
#     liste = mycol.find(dbrequest)
#     count = 0
#     for _ in liste:
#         count += 1
#     return count

# print(count_billet_type('Bunit','gui'))









# mycol.create_index("username", unique=True)


# requete = {"username":"gui","password":'toto'}
# liste = mycol.find(requete)


# for x in liste:
#     username = x['username']
    



# dbrequest = {"username":"gui", "email":"gui@test.fr"}

# Bunit = 1

# liste = mycol.find(requete)
# for elem in liste:
#     titreActif = elem['titreActif']
# titreActif += Bunit

# modif = { "$set" : {"titreActif": titreActif}}
# mycol.update_one(requete,modif)



# data =  {"nom":"flauzac" , "prenom":"olivier" , "noteTP" : 18}

# mycol.insert_one(data)
        
# mycol = mydb["billets"]
# dbrequest = {'Type': {"$eq":'Bunit'}, 'username':'gui'}

# liste = mycol.find(dbrequest)

# count = 0
# for elem in liste:
#     count += 1



# def count_billet_type(Type,username):
#     dbrequest = {'Type': {"$eq": Type}, 'username': username}
#     liste = mycol.find(dbrequest)
#     count = 0
#     for _ in liste:
#         count += 1
#     return count

# print(count_billet_type('Bunit','gui'))












#
# print(count)

# for x in data:
#     print(x)
# Compter les occurrences de la valeur "a"
# counter = Counter(data[''])
# print(counter)

# Afficher le nombre d'occurrences de "a"


    # print(username)

# for x in mycol.find({},{ "username": 'toto'}):
#     print(x)

# try:
#     data1 = {"username":"toto" , "email":"toto@test.fr" , "password" : 'toto', "titreActif":1, "titreRestant":0}
#     mycol.insert_one(data1)
# except:
#     print('utilisateur deja présent')


# x = mycol.find_one({ "username": 'toto'})
# print(x)

# collection_name = "ticket"
# ma_collection = mydb.get_collection(collection_name)
# resultats = ma_collection.find({'gui'})
# print(resultats)
    


# requete = { 'username':'gui'}
# liste = mycol.find(requete)
# for elem in liste:
#     username = elem['username']
#     titreActif = elem['titreActif']
#     titreRestant = elem['titreRestant']
    
# print(username,titreActif,titreRestant)


# requete = { 'username':'gui'}
# liste = mycol.find(requete)
# for elem in liste:
#     data = {
#     'username': elem['username'],
#     'titreActif':elem['titreActif'],
#     'titreRestant': elem['titreRestant']
#     }
    
    
# print(data)

# data = []
# dbrequest = { 'username':'gui'}
# liste = mycol.find(dbrequest)
# for elem in liste:
#     data.append({
#     'username': elem['username'],
#     'titreActif':elem['titreActif'],
#     'titreRestant': elem['titreRestant']
#     })
    
    
# print(data)


# dbrequest = { 'username': 'toto'}
# liste = mycol.find(dbrequest)
# # for elem in liste:
#     data.append({
#     'username': elem['username'],
#     'titreActif':elem['titreActif'],
#     'titreRestant': elem['titreRestant']
#     })
    

# for elem in liste:

#     data = {
#     'username': elem['username'],
#     'titreActif':elem['titreActif'],
#     'titreRestant': elem['titreRestant']
#     }

# print(data)

# if data['titreActif'] == None:
#     data['titreActif'] = 0
