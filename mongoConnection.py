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

def connect_mongo_report_dev():
    CONNECTION_STRING = "mongodb+srv://lunchbucket:root@cluster0.pzgdm0e.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['expert-system']
    collection_name = db_Name["todayAmounts"]
    return collection_name

def connect_mongo_order_dev():
    CONNECTION_STRING = "mongodb+srv://lunchbucket:root@cluster0.pzgdm0e.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['menu']
    collection_name = db_Name["order"]
    return collection_name

def connect_mongo_manufactured_dev():
    CONNECTION_STRING = "mongodb+srv://lunchbucket:root@cluster0.pzgdm0e.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['menu']
    collection_name = db_Name["manufactured"]
    return collection_name

def connect_mongo_report_prod():
    CONNECTION_STRING = "mongodb+srv://lunchbucketofficial:tLJyGjIoBq558dgK@lunchbucket.plo5voq.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['expert-system']
    collection_name = db_Name["todayAmounts"]
    return collection_name
def connect_mongo_order_prod():
    CONNECTION_STRING = "mongodb+srv://lunchbucketofficial:tLJyGjIoBq558dgK@lunchbucket.plo5voq.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['menu']
    collection_name = db_Name["order"]
    return collection_name

def connect_mongo_manufactured_prod():
    CONNECTION_STRING = "mongodb+srv://lunchbucketofficial:tLJyGjIoBq558dgK@lunchbucket.plo5voq.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db_Name = client['menu']
    collection_name = db_Name["manufactured"]
    return collection_name
