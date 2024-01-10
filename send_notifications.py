import requests
import os

def send_notification(user_id , message):
    headers = {'project_code': os.environ['PROJECT_CODE'],
               'user_id': user_id , "message":message}
    print(headers)
    url = os.environ['AUTHORIZATION_URL'] + "/sendNotification"
    validate_res = requests.get(url=url, headers=headers)
    print(validate_res.json())
    if not validate_res.json()['data']['state']:
        response = {
            "state": False,
        }
    else:
        response = {
            "state": True,
        }
    return response

def send_notifications(user_ids , message):
    return list(map(lambda user_id:send_notification(user_id , message=message),user_ids))