from bson import ObjectId

import getCsv_dev
import getCsv_prod

csv_dev = getCsv_dev.getCSV()
csv_prod = getCsv_prod.getCSV()

from mongoConnection import connect_mongo_expert_dev , connect_mongo_expert_prod
from env_variables import TODAY_MENU_ID_DEV ,TODAY_MENU_ID_PROD
from entities import returnSuitabilityOBJ
collection_name_dev = connect_mongo_expert_dev()
collection_name_prod = connect_mongo_expert_prod()

def get_suitability(id1 , id2, df , vege_menu , stew_menu , meat_menu):
    meat_suitability = []
    stew_suitability = []
    vegi_suitability = []
    for i in meat_menu:
        df2 = df.loc[df['number'] == i['number']]
        suitability = (int(df2[id1]) + int(df2[id2])) / 2
        meat_suitability.append(returnSuitabilityOBJ(i, suitability))
    for i in stew_menu:
        df2 = df.loc[df['number'] == i['number']]
        suitability = (int(df2[id1]) + int(df2[id2])) / 2
        stew_suitability.append(returnSuitabilityOBJ(i, suitability))
    for i in vege_menu:
        df2 = df.loc[df['number'] == i['number']]
        suitability = (int(df2[id1]) + int(df2[id2])) / 2
        vegi_suitability.append(returnSuitabilityOBJ(i, suitability))
    return {
        "vegi_suitability":vegi_suitability,
        "stew_suitability":stew_suitability,
        "meat_suitability":meat_suitability
    }

def twoSuitability_dev_lunch(id1,id2):
    df = csv_dev
    item = collection_name_dev.find_one({'_id': ObjectId(TODAY_MENU_ID_DEV)})
    response = {
        "state": True,
        "data": get_suitability(id1=id1, id2=id2, df=df, meat_menu=item['meat_lunch'],stew_menu=item['stew_lunch'],vege_menu=item['vege_lunch'])
    }
    return response

def twoSuitability_dev_dinner(id1,id2):
    df = csv_dev
    item = collection_name_dev.find_one({'_id': ObjectId(TODAY_MENU_ID_DEV)})
    response = {
        "state": True,
        "data": get_suitability(id1=id1, id2=id2, df=df, meat_menu=item['meat_dinner'],stew_menu=item['stew_dinner'],vege_menu=item['vege_dinner'])
    }
    return response

def twoSuitability_prod_lunch(id1,id2):
    df = csv_prod
    item = collection_name_prod.find_one({'_id': ObjectId(TODAY_MENU_ID_PROD)})
    response = {
        "state": True,
        "data": get_suitability(id1=id1, id2=id2, df=df, meat_menu=item['meat_lunch'],stew_menu=item['stew_lunch'],vege_menu=item['vege_lunch'])
    }
    return response

def twoSuitability_prod_dinner(id1,id2):
    df = csv_prod
    item = collection_name_prod.find_one({'_id': ObjectId(TODAY_MENU_ID_PROD)})
    response = {
        "state": True,
        "data": get_suitability(id1=id1, id2=id2, df=df, meat_menu=item['meat_dinner'],stew_menu=item['stew_dinner'],vege_menu=item['vege_dinner'])
    }
    return response
