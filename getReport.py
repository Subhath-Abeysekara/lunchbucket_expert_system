import hashlib

from bson import ObjectId

from mongoConnection import connect_mongo_report_dev , connect_mongo_order_dev , connect_mongo_report_prod ,connect_mongo_order_prod
collection_name_report_dev = connect_mongo_report_dev()
collection_name_order_dev = connect_mongo_order_dev()
collection_name_report_prod = connect_mongo_report_prod()
collection_name_order_prod = connect_mongo_order_prod()
from generatePdf import init_pdf , generate_pdf , print_pdf
from sendMail import send_mail

doc_id_dev = '64e4b84c3a17927901c8e001'
doc_id_prod = '64e4d0030affa844f4771d9e'

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
    docs = collection_name.find({'meal':meal})
    return docs

def get_report_dev(meal):
    report = get_report(collection_name_report_dev ,doc_id_dev, meal)
    docs = get_orders(collection_name_order_dev , meal)
    print(docs)
    pdf = init_pdf()
    pdf = generate_pdf(report , pdf,"")
    pdf.add_page()
    report_orders= {
        'ORDERS':''
    }
    pdf = generate_pdf(report_orders, pdf,"")
    i = 0
    for doc in docs:
        i+=1
        print(doc)
        report_new = {
            i:''
        }
        try:
            for item in doc['items']:
                report_new[item] = ''
            report_new['price'] = doc['price']
            report_new['packet_amount'] = doc['packet_amount']
            report_new['customer_code'] = doc['customer_code']
            report_new['order_code'] = generate_code(str(doc['_id']))
            report_new['delivery_time'] = doc['delivery_time']
            report_new['threat'] = doc['threat']
            report_new['printed'] = doc['printed']
        except:
            print("he")
        print(i)
        if doc['printed']:
            state = "printed"
        else:
            state = ""
            collection_name_order_dev.update_one({'_id': doc['_id']}, {'$set': {"printed": True}})
        pdf = generate_pdf(report_new,pdf,"threat" if doc['threat'] else state)
    print_pdf(pdf)
    return send_mail()

def get_report_prod(meal):
    report = get_report(collection_name_report_prod ,doc_id_prod, meal)
    print(report)
    docs = get_orders(collection_name_order_prod , meal)
    print(docs)
    pdf = init_pdf()
    pdf = generate_pdf(report , pdf , "")
    pdf.add_page()
    report_orders= {
        'ORDERS':''
    }
    pdf = generate_pdf(report_orders, pdf,"")
    i = 0
    for doc in docs:
        i+=1
        report_new = {
            i:''
        }
        print(doc)
        try:
            for item in doc['items']:
                report_new[item] = ''
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
        else:
            state = ""
            collection_name_order_prod.update_one({'_id': doc['_id']}, {'$set': {"printed": True}})
        pdf = generate_pdf(report_new,pdf,"threat" if doc['threat'] else state)
    print_pdf(pdf)
    return send_mail()
# get_report_dev('Lunch')