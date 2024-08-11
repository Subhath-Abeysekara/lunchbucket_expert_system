import hashlib

from bson import ObjectId

from mongoConnection import connect_mongo_report_dev, connect_mongo_old_report_dev, connect_mongo_old_report_prod, \
    connect_mongo_order_dev, connect_mongo_report_prod, connect_mongo_order_prod

collection_name_report_dev = connect_mongo_report_dev()
collection_name_order_dev = connect_mongo_order_dev()
collection_name_old_report_dev = connect_mongo_old_report_dev()
collection_name_report_prod = connect_mongo_report_prod()
collection_name_order_prod = connect_mongo_order_prod()
collection_name_old_report_prod = connect_mongo_old_report_prod()
from generatePdf import init_pdf, generate_pdf, print_pdf, PDFWithTable
from sendMail import send_mail

doc_id_dev = '64e4b84c3a17927901c8e001'
reported_id_dev = '65a115a660eeda49275c68f6'
doc_id_prod = '64e4d0030affa844f4771d9e'
reported_id_prod = '65a11bdca6b030cc89a6c1a8'


def generate_code(id):
    hash_object = hashlib.sha256()
    hash_object.update(id.encode('utf-8'))
    hex_digest = hash_object.hexdigest()
    hex_prefix = hex_digest[:4]
    numeric_code = int(hex_prefix, 16)
    return str(numeric_code)


def get_report(collection_name, id, meal):
    report_doc = collection_name.find_one({'_id': ObjectId(id)})
    item_name = meal.lower() + '_item_count'
    return report_doc[item_name]


def get_orders(collection_name, meal):
    if 'lun' in meal.lower():
        meal = "Lunch"
    else:
        meal = "Dinner"
    docs = collection_name.find({'meal': meal, 'order_status': True})
    docs = list(docs)
    print(docs)
    return docs


def create_report(collection_name, docs, pdf, update_state, balance):
    print(docs)
    report_orders = {
        'ORDERS': ''
    }
    pdf = generate_pdf(report_orders, pdf, "")
    i = 0
    gravy_counts = {
        "Milk Gravy":0,
        "Chicken Gravy":0,
        "No Gravy":0
    }
    for doc in docs:
        i += 1
        try:
            report_new = {
                doc['no']: ''
            }
        except:
            report_new = {
                str(i): ''
            }
        print("doc",doc)
        try:
            gravy = doc['gravy']
            gravy_counts[gravy]+=doc['packet_amount']
        except:
            gravy = 'Milk Gravy'
            gravy_counts[gravy] += doc['packet_amount']
        location = 'back gate'
        large = False
        try:
            if doc['order_type'] == "special":
                report_new[doc['type']] = ''
                report_new[doc['category']] = ''
            else:
                for item in doc['items']:
                    report_new[item] = ''
                    try:
                        if 'rice(large)' in item.lower():
                            large = True
                    except:
                        print("")
            report_new['gravy'] = gravy
            report_new['price'] = doc['price']
            report_new['packet_amount'] = doc['packet_amount']
            report_new['customer_code'] = doc['customer_code']
            report_new['order_code'] = generate_code(str(doc['_id']))
            report_new['delivery_time'] = doc['delivery_time']
            report_new['threat'] = doc['threat']
            report_new['printed'] = doc['printed']
            try:
                report_new['contact'] = doc['contact']
            except:
                print("contact error")
            try:
                if doc['location'] and doc['priority']:
                    location = 'priority'
                elif doc['location']:
                    location = 'normal'
                report_new['location'] =  location
            except:
                print("location error")
        except:
            print("error")
        if doc['printed']:
            state = "printed"
            print("printed")
        else:
            state = ""
            print("not printed")
            if update_state:
                print("update")
                collection_name.update_one({'_id': doc['_id']}, {'$set': {"printed": True}})
        if doc['location']:
            state = location
        pdf = generate_pdf(report_new, pdf, "threat" if doc['threat'] else state , large_state=large)
    print("he")
    if not update_state:
        report_orders = {
            'BALANCE ORDERS FOR THIS TIME ': str(balance)
        }
        for gravy_item in gravy_counts:
            report_orders[gravy_item] = gravy_counts[gravy_item]
        pdf.add_page()
        pdf = generate_pdf(report_orders, pdf, "")
    else:
        report_orders = {
            'GRAVY AMOUNTS ': ""
        }
        for gravy_item in gravy_counts:
            report_orders[gravy_item] = gravy_counts[gravy_item]
        pdf.add_page()
        pdf = generate_pdf(report_orders, pdf, "")
    print_pdf(pdf)
    return send_mail()


def create_table(document, collection_name, report_id, meal):
    old_document = collection_name.find_one({'_id': ObjectId(report_id)})[meal.lower()]
    collection_name.update_one({'_id': ObjectId(report_id)}, {'$set': {meal.lower(): document}})
    all_keys = document.keys()
    key_list = list(all_keys)
    print(key_list)
    if meal.lower() == 'lunch':
        data = [['Item', "11:00", "12:30", "1:00", "1:30", "2:00"]]
        time_keys = ["11:00", "12:30", "1:00", "1:30", "2:00"]
    else:
        data = [['Item', "7:30", "8:30", "9:00", "9:30"]]
        time_keys = ["7:30", "8:30", "9:00", "9:30"]
    for key in key_list:
        document_ = document[key]
        data_ = [key]
        for time_key in time_keys:
            try:
                data_.append(old_document[key][time_key])
            except:
                data_.append(0)
            try:
                data_.append(document_[time_key])
            except:
                data_.append(0)
        data.append(data_)
    print(data)
    pdf = PDFWithTable()
    pdf.add_page()
    pdf.add_table(data)
    pdf.add_page()
    return pdf


def get_report_dev(meal):
    report = get_report(collection_name_report_dev, doc_id_dev, meal)
    docs = get_orders(collection_name_order_dev, meal)
    print(docs)
    return create_report(collection_name_order_dev, docs,
                         create_table(document=report, collection_name=collection_name_old_report_dev,
                                      report_id=reported_id_dev, meal=meal), True, 0)


def get_report_prod(meal):
    report = get_report(collection_name_report_prod, doc_id_prod, meal)
    print(report)
    docs = get_orders(collection_name_order_prod, meal)
    print(docs)
    return create_report(collection_name_order_prod, docs, create_table(document=report,
                                                                        collection_name=collection_name_old_report_prod,
                                                                        report_id=reported_id_prod, meal=meal), True, 0)


def get_delivery_report(docs, balance, collection_name):
    pdf = init_pdf()
    return create_report(collection_name, docs, pdf, False, balance)

# get_report_prod(meal = "Dinner")
