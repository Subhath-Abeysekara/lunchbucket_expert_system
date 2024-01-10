from getReport import get_orders, collection_name_order_prod, collection_name_order_dev, get_delivery_report
from mongoConnection import connect_mongo_manufactured_dev, connect_mongo_manufactured_prod

collection_name_manufactured_dev = connect_mongo_manufactured_dev()
collection_name_manufactured_prod = connect_mongo_manufactured_prod()

def set_order_place(delivery_place):
    try:
        if "front" in delivery_place.lower():
            return "Front gate"
        else:
            return "Back gate"
    except:
        return "Front gate"

def get_manufacturing_dev(meal , delivery_place , limit):
    docs = collection_name_order_dev.find(
        {'meal': meal, "delivery_status": False, "delivery_place": set_order_place(delivery_place)}).limit(limit)
    print(docs)
    docs = list(docs)
    for doc in docs:
        print(doc)
        collection_name_order_dev.update_one({'_id': doc['_id']}, {'$set': {
            "delivery_status": True
        }})
        collection_name_manufactured_dev.insert_one(doc)
    return get_delivery_report(docs=docs,
                        balance=collection_name_order_dev.count_documents({'meal': meal, "delivery_status": False, "delivery_place": set_order_place(delivery_place)}))

def get_manufacturing_prod(meal , delivery_place , limit):
    docs = collection_name_order_prod.find(
        {'meal': meal, "delivery_status": False, "delivery_place": set_order_place(delivery_place)}).limit(limit)
    print(docs)
    docs = list(docs)
    for doc in docs:
        print(doc)
        collection_name_order_prod.update_one({'_id': doc['_id']}, {'$set': {
            "delivery_status": True
        }})
        collection_name_manufactured_prod.insert_one(doc)
    return get_delivery_report(docs=docs,
                        balance=collection_name_order_prod.count_documents({'meal': meal, "delivery_status": False, "delivery_place": set_order_place(delivery_place)}))
