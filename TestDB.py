import pymongo






client = pymongo.MongoClient("mongodb+srv://USER:PASSWORD@seacluster.f3vdv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['Test']


tools = db["Tools"]

#mydict = { "Name": "Peter", "Description": "Lowstreet 27","Path": "C:/tacos.wav", "Options": "-r newName", "Output": ".xml", "Specification": "here.txt"}
#mydict = { "Name": "Paul", "Description": "It's a great Tool","Path": "C:/tacos.wav", "Options": "-w newName", "Output": ".xml", "Specification": "here.txt"}

#x = tools.insert_one(mydict)

#print(x)

for i in tools.find():
    print("Description", i["Description"])
    print("Name: ", i["Name"])
#x = tools.delete_many({})

print(client.list_database_names())

