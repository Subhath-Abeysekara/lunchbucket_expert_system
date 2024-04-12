from pymongo import MongoClient

def connect_mongo_food():
    CONNECTION_STRING = "mongodb+srv://lunchbucketofficial:tLJyGjIoBq558dgK@lunchbucket.plo5voq.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['menu']
    collection_name = db_Name["food"]
    return collection_name

def connect_mongo_menu():
    CONNECTION_STRING = "mongodb+srv://lunchbucketofficial:tLJyGjIoBq558dgK@lunchbucket.plo5voq.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['expert-system']
    collection_name = db_Name["todayAmounts"]
    return collection_name