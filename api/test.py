import pymongo
import datetime
import jsonify

myclient = pymongo.MongoClient('mongodb://10.11.10.49', 27017, username="root", password='1toto;2')
mydb = myclient["Billetterie"]
    

today = datetime.datetime.utcnow().strftime("%Y-%m-%d")  
    
print(today)



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





print(data)
print(data[0]['buyToday'])



# def dashData():
#     mycol = mydb["billets"]
#     dbrequest = { 'dateAchat': {"$eq": today}}
#     liste = mycol.find()

#     todayBuy = 0 
#     for x in liste:
#         print(x)
#         todayBuy += 1

#     return todayBuy
    
# data = []

# data.append({'buyToday':todayBuy})

