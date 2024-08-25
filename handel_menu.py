from bson import ObjectId
from env_variables import TODAY_MENU_ID_PROD
from mongoConnection import connect_mongo_expert_prod
collection_name = connect_mongo_expert_prod()

def reset_menu(meal):
    data = collection_name.find_one({'_id': ObjectId(TODAY_MENU_ID_PROD)})
    print(data)
    for item in data:
        if meal.lower() in item:
            print(item, data[item])
            data[item] = []
    del data['_id']
    print(data)
    collection_name.update_one({'_id': ObjectId(TODAY_MENU_ID_PROD)},{'$set':data})
    return

# reset_menu(meal = 'Dinner')