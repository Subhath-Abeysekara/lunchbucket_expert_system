from pymongo import MongoClient
import os

def connect_mongo_expert_dev():
    CONNECTION_STRING = "mongodb+srv://lunchbucket:root@cluster0.pzgdm0e.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['expert-system']
    collection_name = db_Name["today-menu"]
    return collection_name

def connect_mongo_expert_prod():
    CONNECTION_STRING = "mongodb+srv://lunchbucketofficial:tLJyGjIoBq558dgK@lunchbucket.plo5voq.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['expert-system']
    collection_name = db_Name["today-menu"]
    return collection_name