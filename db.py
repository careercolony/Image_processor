from pymongo import MongoClient

db_name = 'users'
db_host_mongo = '209.97.186.65'
db_port_mongo = '30001'
mongo_uri = "mongodb://{db_host}:{db_port_mongo}/{db_name}".format(
    #username=username, password=password, db_host=db_host_mongo,
    db_host=db_host_mongo,
    db_port_mongo=db_port_mongo, db_name=db_name)
client = MongoClient(mongo_uri)
database = client[db_name]
