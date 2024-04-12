import requests
from bson import ObjectId
from service import connect_mongo_menu
from datetime import datetime, timedelta

collection_name = connect_mongo_menu()


def get_today_menu():
  url = "https://r36pslzyv8.execute-api.ap-south-1.amazonaws.com/prod/lunch/getMenus"
  validate_res = requests.get(url=url)
  print(validate_res.json())
  data = validate_res.json()['data']['data']
  menu = {}
  for key in data:
    print(data[key])
    for food in data[key]:
      menu[food['type']] = 0
  print(menu)
  return menu


def matching_rate(meal, reports):
  date = datetime.today().strftime('%Y-%m-%d')
  given_date = datetime.strptime(date, '%Y-%m-%d')
  previous_date = given_date - timedelta(days=1)
  previous_date_str = previous_date.strftime('%Y-%m-%d')
  prev_string = previous_date_str + meal.lower()
  amount_obj1 = get_today_menu()
  amount_obj2 = reports[prev_string]['foods']
  union_count = len(set(amount_obj1.keys()) | set(amount_obj2.keys()))
  intersection_count = len(set(amount_obj1.keys()) & set(amount_obj2.keys()))
  matching_rate = intersection_count / union_count
  return matching_rate

def set_food_availability(food, meal):
  date = datetime.today().strftime('%Y-%m-%d')
  row = {}
  report = collection_name.find_one({'_id': ObjectId('64e4d0030affa844f4771d9e')})
  reports = report['total_report']
  for i in range(1,6):
    given_date = datetime.strptime(date, '%Y-%m-%d')
    previous_date = given_date - timedelta(days=1)
    previous_date_str = previous_date.strftime('%Y-%m-%d')
    string = previous_date_str+meal.lower()
    date = previous_date_str
    try:
      amount_obj = reports[string]['foods'][food]
      full_amount = 0
      for amount in amount_obj:
        full_amount += amount_obj[amount]
      row[f'last_menu_availability_{i}'] = full_amount
    except:
      row[f'last_menu_availability_{i}'] = 0
  return row

def set_food_availability_one(food, meal):
  date = datetime.today().strftime('%Y-%m-%d')
  row = {}
  report = collection_name.find_one({'_id': ObjectId('64e4d0030affa844f4771d9e')})
  reports = report['total_report']
  given_date = datetime.strptime(date, '%Y-%m-%d')
  previous_date = given_date - timedelta(days=1)
  previous_date_str = previous_date.strftime('%Y-%m-%d')
  string = previous_date_str+meal.lower()
  try:
    amount_obj = reports[string]['foods'][food]
    full_amount = 0
    for amount in amount_obj:
      full_amount+=amount_obj[amount]
    row['last_menu_availability'] = full_amount
  except:
    row['last_menu_availability'] = 0
  row['menu_matching_rate'] = matching_rate(meal , reports=reports)
  return row

# row = set_limited_request_one(food = "Pol Sambol" , meal="Lunch")
# print(row)
