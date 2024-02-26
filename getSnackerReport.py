import hashlib

from bson import ObjectId

from mongoConnection import connect_mongo_report_dev ,connect_mongo_old_report_dev,connect_mongo_old_report_prod, connect_mongo_order_dev , connect_mongo_report_prod ,connect_mongo_order_prod
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

def get_report(collection_name , id , meal):
   report_doc = collection_name.find_one({'_id':ObjectId(id)})
   item_name = meal.lower()+'_item_count'
   return report_doc[item_name]

def get_orders(collection_name , meal):
    docs = collection_name.find({'meal':meal,'order_status':True})
    return docs
def create_report(collection_name,docs,pdf):
    print(docs)
    report_orders= {
        'ORDERS':''
    }
    pdf = generate_pdf(report_orders, pdf,"")
    i = 0
    for doc in docs:
        if "spe" in doc['order_type'].lower() and "lunch bucket authentic" in doc['category'].lower():
            i += 1
            report_new = {
                i: ''
            }
            print(doc)
            try:
                report_new[doc['type']] = ''
                report_new[doc['category']] = ''
                report_new['price'] = doc['price']
                report_new['packet_amount'] = doc['packet_amount']
                report_new['customer_code'] = doc['customer_code']
                report_new['order_code'] = generate_code(str(doc['_id']))
                report_new['delivery_time'] = doc['delivery_time']
                report_new['threat'] = doc['threat']
                report_new['printed'] = doc['printed']
            except:
                print("error")
            if doc['printed']:
                state = "printed"
                print("printed")
            else:
                state = ""
                print("not printed")
                print("update")
                collection_name.update_one({'_id': doc['_id']}, {'$set': {"printed": True}})
            pdf = generate_pdf(report_new, pdf, "threat" if doc['threat'] else state)
    print("he")
    print_pdf(pdf)
    return send_mail()

def create_table(document,collection_name,report_id,meal):
    old_document = collection_name.find_one({'_id':ObjectId(report_id)})[meal.lower()]
    collection_name.update_one({'_id': ObjectId(report_id)}, {'$set': {meal.lower():document}})
    all_keys = document.keys()
    key_list = list(all_keys)
    print(key_list)
    data = [['Item', "3:30", "4:30", "5:30"]]
    time_keys = ["3:30", "4:30", "5:30"]
    for key in key_list:
        if "lunch bucket authentic" in key.lower():
            print(key)
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
def get_report_dev():
    report = get_report(collection_name_report_dev ,doc_id_dev, "Dinner")
    docs = get_orders(collection_name_order_dev , "Dinner")
    print(docs)
    return create_report(collection_name_order_dev,docs,create_table(document=report,collection_name=collection_name_old_report_dev,
                                                                     report_id=reported_id_dev,meal="Dinner"))

def get_report_prod():
    report = get_report(collection_name_report_prod ,doc_id_prod, "Dinner")
    print(report)
    docs = get_orders(collection_name_order_prod , "Dinner")
    print(docs)
    return create_report(collection_name_order_prod,docs,create_table(document=report,
                                                                      collection_name=collection_name_old_report_prod,
                                                                      report_id=reported_id_prod,meal="Dinner"))

def get_delivery_report(docs,collection_name):
    pdf = init_pdf()
    return create_report(collection_name,docs, pdf)

# get_report_dev()
