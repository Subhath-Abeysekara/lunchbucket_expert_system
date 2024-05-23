from datetime import datetime, timedelta
import requests
from bson import ObjectId

from limit_prediction import input_data_limit , prediction
from menu_availability import set_food_availability_one, get_today_menu
from ml_report_generate import create_limit_pdf
from service import connect_mongo_menu

collection_name = connect_mongo_menu()

def get_day_of_week():
    date_obj = datetime.strptime(datetime.today().strftime('%m/%d/%Y'), '%m/%d/%Y')
    day = date_obj.strftime('%A')
    return day

def select_best_limit(meal , food_type , pre_request , day , holiday , whether , temperature):
    input_data_limit['food_type'] = food_type
    input_data_limit['day'] = day
    input_data_limit['holiday'] = holiday
    input_data_limit['whether'] = whether
    input_data_limit['temperature'] = temperature
    input_data_limit['meal'] = meal
    row = set_food_availability_one(food = food_type, meal=meal)
    input_data_limit['menu_matching_rate'] = row['menu_matching_rate']
    input_data_limit['last_menu_availability'] = row['last_menu_availability']
    input_data_limit['pre_request'] = pre_request
    prediction_ = prediction(input_data_limit)
    print(prediction_)
    return prediction_

def select_best_limits(meal , holiday , whether , temperature):
    menu = get_today_menu(meal=meal)
    report = collection_name.find_one({'_id': ObjectId('64e4d0030affa844f4771d9e')})
    reports = report['total_report']
    date = datetime.today().strftime('%Y-%m-%d')
    string = date + meal.lower()
    limits = {}
    day = get_day_of_week()
    for item in menu:
        try:
            amount_obj = reports[string]['foods'][item]
            full_amount = 0
            for amount in amount_obj:
                full_amount += amount_obj[amount]
            pre_request = full_amount
        except:
            pre_request = 0
        prediction_ = select_best_limit(meal=meal, food_type=item,
                                        pre_request=pre_request , day = day,
                                        holiday=holiday,
                                        whether=whether,temperature=temperature)
        limits[item] = {
            'limit':round(abs(prediction_ - pre_request))+3,
            'pre_request':pre_request
        }
    print('limits',limits)
    create_limit_pdf(limits, meal)
    return limits

body = {
    "holiday" :"Yes",
    "whether" :"Partly Cloudy",
    "temperature" : 90,
    "meal":"Dinner"
}

# select_best_limits(body['meal'] , body['holiday'] , body['whether'] , body['temperature'])
#

