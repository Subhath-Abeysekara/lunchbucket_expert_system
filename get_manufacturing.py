from getReport import get_orders, collection_name_order_prod, collection_name_order_dev, get_delivery_report
from mongoConnection import connect_mongo_manufactured_dev, connect_mongo_manufactured_prod
from collections import Counter

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
def set_order_time(time):
    try:
        if "11" in time.lower():
            return "11:00 AM"
        elif "12" in time.lower():
            return "12:30 PM"
        elif "2" in time.lower():
            return "2:00 PM"
        elif "7" in time.lower():
            return "7:30 PM"
        elif "8" in time.lower():
            return "8:30 PM"
        elif "3" in time.lower():
            return "3:30"
        elif "4" in time.lower():
            return "4:30"
        elif "5" in time.lower():
            return "5:30"
    except:
        return "11:00 AM"

def document(doc):
    doc['id'] = str(doc['_id'])
    del doc['_id']
    return doc
def documents(docs):
    return list(map(lambda doc:document(doc),docs))

def find_nearest_key(dictionary, target):
    nearest_key = min(dictionary, key=lambda x: abs(dictionary[x] - target))
    return nearest_key
def get_optimal_manufactures(collection ,meal , delivery_place , limit,time):
    print(delivery_place)
    print(set_order_place(delivery_place))
    print(set_order_time(time))
    cursor = collection.find({'meal': meal,"delivery_status": False,
                              "delivery_place": set_order_place(delivery_place),
                              "delivery_time": set_order_time(time),
                              'order_status': True
                              })
    cursor = list(cursor)
    print(cursor)
    codes = [doc["customer_code"] for doc in cursor]
    print(codes)
    counter = Counter(codes)
    unique_values_with_frequency = counter.items()
    print(unique_values_with_frequency)
    unique_values_dict = dict(unique_values_with_frequency)
    print(f"unique_packets {unique_values_dict}")
    documents = []
    try:
        max_code = max(unique_values_dict, key=unique_values_dict.get)
        print(max_code)
        filtered_objects = list(filter(lambda obj: obj.get("customer_code") == max_code, cursor))
        print(len(filtered_objects))
        documents += filtered_objects
        print(len(documents))
        del unique_values_dict[max_code]
        print(unique_values_dict)
        while True:
            if unique_values_dict == {}:
                break
            max_code = max(unique_values_dict, key=unique_values_dict.get)
            print(max_code)
            filtered_objects = list(filter(lambda obj: obj.get("customer_code") == max_code, cursor))
            print(len(filtered_objects))
            if len(documents) + unique_values_dict[max_code] > limit + 4:
                while True:
                    if unique_values_dict == {}:
                        break
                    nearest_key = find_nearest_key(unique_values_dict, limit - len(documents) + 4)
                    print(nearest_key)
                    print(unique_values_dict[nearest_key])
                    if len(documents) + unique_values_dict[nearest_key] > limit + 4:
                        del unique_values_dict[nearest_key]
                        continue
                    filtered_objects = list(filter(lambda obj: obj.get("customer_code") == nearest_key, cursor))
                    print(len(filtered_objects))
                    documents += filtered_objects
                    print(len(documents))
                    del unique_values_dict[nearest_key]
                    print(unique_values_dict)
                break
            documents += filtered_objects
            print(len(documents))
            del unique_values_dict[max_code]
            print(unique_values_dict)
        return documents
    except:
        return documents

def manufacturing(collection_name_manufactured , collection_name_order , meal , delivery_place , limit,time):
    docs = get_optimal_manufactures(collection=collection_name_order, meal=meal,
                                    delivery_place=delivery_place,
                                    limit=limit, time=time)
    print(docs)
    docs = list(docs)
    collection_name_manufactured.delete_many(
        {'meal': meal, "delivery_place": set_order_place(delivery_place=delivery_place)})
    for doc in docs:
        print(doc)
        collection_name_order.update_one({'_id': doc['_id']}, {'$set': {
            "delivery_status": True
        }})
        collection_name_manufactured.insert_one(doc)
    get_delivery_report(docs=docs,
                        balance=collection_name_order.count_documents({'meal': meal, "delivery_status": False,
                                                                           "delivery_place": set_order_place(
                                                                               delivery_place),
                                                                           "delivery_time": set_order_time(time),
                                                                           'order_status': True}),
                        collection_name=collection_name_order)
    print(len(docs))
    return documents(docs)
def get_manufacturing_dev(meal , delivery_place , limit,time):
    return manufacturing(collection_name_manufactured_dev , collection_name_order_dev ,
                         meal , delivery_place , limit,time)

def get_manufacturing_prod(meal , delivery_place , limit,time):
    return manufacturing(collection_name_manufactured_prod , collection_name_order_prod,
                         meal , delivery_place , limit,time)

# print(get_optimal_manufactures(collection_name_order_dev,"Lunch","front",2,"11:30 AM"))
# get_manufacturing_dev("Lunch" , "Back gate" , 20,"2")