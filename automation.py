import requests
from bson import ObjectId

from getReport import reported_id_prod, collection_name_old_report_prod
from time_utc import get_utc_time_count

def call_delete_api(meal):
        url = f"https://2tbtjpgj61.execute-api.ap-south-1.amazonaws.com/prod/deleteOrders/{meal}"
        response = requests.delete(url=url)
        print(response)
        return

def deleteOrders():
    try:
        lunch_time_lower = 10 * 60
        lunch_time_upper = 10 * 60 + 45
        dinner_time_lower = 16 * 60 + 30
        dinner_time_upper = 17 * 60 + 15
        breakfast_time_lower = 6 * 60 + 30
        breakfast_time_upper = 7 * 60 + 15
        current_time = get_utc_time_count()
        print(current_time)
        if current_time>=lunch_time_lower and current_time<lunch_time_upper:
            call_delete_api("Lunch")
            collection_name_old_report_prod.update_one({'_id': ObjectId(reported_id_prod)}, {'$set': {"lunch": {}}})
        elif current_time>=breakfast_time_lower and current_time<breakfast_time_upper:
            call_delete_api("Breakfast")
            collection_name_old_report_prod.update_one({'_id': ObjectId(reported_id_prod)}, {'$set': {"breakfast": {}}})
        elif current_time>=dinner_time_lower and current_time<dinner_time_upper:
            call_delete_api("Dinner")
            collection_name_old_report_prod.update_one({'_id': ObjectId(reported_id_prod)}, {'$set': {"dinner": {}}})
        return
    except:
        print("error in operation")
        return