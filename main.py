from flask import Flask, request
from flask_cors import CORS, cross_origin
# import getByTwo
# import getByThree
# import finalSuitability
import getReport
import getSnackerReport
import get_manufacturing
from apscheduler.schedulers.background import BackgroundScheduler
from automation import deleteOrders
from select_limits import select_best_limits
from select_menu import select_best_menu

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})

scheduler = BackgroundScheduler()
scheduler.add_job(deleteOrders, trigger='interval', seconds=1800)
scheduler.start()

image_url = "https://firebasestorage.googleapis.com/v0/b/meetingdetecting.appspot.com/o/lunchbucket_special_meal%2Fi2AuthLogo.jpeg?alt=media&token=2cc0abf1-8069-47ad-863b-862be3afe2ed"
image_url_background = "https://firebasestorage.googleapis.com/v0/b/meetingdetecting.appspot.com/o/lunchbucket_special_meal%2Fbackground.jpeg?alt=media&token=94c39cf0-d097-4967-b261-1ac2b6f9e688"

@app.route("/")
def main():
    return "home"

@app.route("/dev/lunch/suitability_for_two/<id1>/<id2>")
@cross_origin()
def suitability_for_two_lunch_dev(id1, id2):
    try:
        return getByTwo.twoSuitability_dev_lunch(id1=id1 , id2=id2)
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/dev/dinner/suitability_for_two/<id1>/<id2>")
@cross_origin()
def suitability_for_two_dinner_dev(id1, id2):
    try:
        return getByTwo.twoSuitability_dev_dinner(id1=id1 , id2=id2)
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/prod/lunch/suitability_for_two/<id1>/<id2>")
@cross_origin()
def suitability_for_two_lunch_prod(id1, id2):
    try:
        return getByTwo.twoSuitability_prod_lunch(id1=id1 , id2=id2)
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/prod/dinner/suitability_for_two/<id1>/<id2>")
@cross_origin()
def suitability_for_two_dinner_prod(id1, id2):
    try:
        return getByTwo.twoSuitability_prod_dinner(id1=id1 , id2=id2)
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/dev/lunch/suitability_for_three/<id1>/<id2>/<id3>")
@cross_origin()
def suitability_for_three_lunch_dev(id1, id2,id3):
    try:
        return getByThree.threeSuitability_dev_lunch(id1=id1 , id2=id2,id3=id3)
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/dev/dinner/suitability_for_three/<id1>/<id2>/<id3>")
@cross_origin()
def suitability_for_three_dinner_dev(id1, id2,id3):
    try:
        return getByThree.threeSuitability_dev_dinner(id1=id1 , id2=id2,id3=id3)
    except:
        return {
            "state": False,
            "message": "error"
        }


@app.route("/prod/lunch/suitability_for_three/<id1>/<id2>/<id3>")
@cross_origin()
def suitability_for_three_lunch_prod(id1, id2, id3):
    try:
        return getByThree.threeSuitability_prod_lunch(id1=id1, id2=id2, id3=id3)
    except:
        return {
            "state": False,
            "message": "error"
        }


@app.route("/prod/dinner/suitability_for_three/<id1>/<id2>/<id3>")
@cross_origin()
def suitability_for_three_dinner_prod(id1, id2, id3):
    try:
        return getByThree.threeSuitability_prod_dinner(id1=id1, id2=id2, id3=id3)
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/dev/getReport/<meal>")
@cross_origin()
def get_report_dev(meal):
    try:
        print(meal)
        return getReport.get_report_dev(meal=meal.lower())
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/prod/getReport/<meal>")
@cross_origin()
def get_report_prod(meal):
    try:
        return getReport.get_report_prod(meal=meal.lower())
    except:
        return {
            "state": False,
            "message": "error"
        }


@app.route("/dev/getSnackersReport")
@cross_origin()
def get_snackers_report_dev():
    try:
        return getSnackerReport.get_report_dev()
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/prod/getSnackersReport")
@cross_origin()
def get_snackers_report_prod():
    try:
        return getSnackerReport.get_report_prod()
    except:
        return {
            "state": False,
            "message": "error"
        }


# ************ MACHINE LEARNING *********************

@app.route("/prod/predict_limits", methods=["POST"])
@cross_origin()
def predict_limits_prod():
    try:
        if request.data:
            body = request.json
            holiday = body['holiday']
            whether = body['whether']
            temperature = body['temperature']
            meal = body['meal']
            return {
                'state': True,
                'data': select_best_limits(meal= meal , holiday =holiday,whether=whether,
                                       temperature=temperature)
            }
        else:
            return {
                "state": False,
                "message": "no body"
            }
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/prod/predict_menu", methods=["POST"])
@cross_origin()
def predict_menu_prod():
    try:
        if request.data:
            body = request.json
            holiday = body['holiday']
            whether = body['whether']
            temperature = body['temperature']
            meal = body['meal']
            return {
                'state': True,
                'data': select_best_menu(meal=meal, holiday=holiday, whether=whether,
                                         temperature=temperature)
            }
        else:
            return {
                "state": False,
                "message": "no body"
            }
    except:
        return {
            "state": False,
            "message": "error"
        }

# ************* MANUFACTURING ***************

@app.route("/dev/manufacture/<meal>/<place>/<limit>/<time>")
@cross_origin()
def get_manufacture_dev(meal,place,limit,time):
    print(meal)
    return get_manufacturing.get_manufacturing_dev(meal=meal, delivery_place=place, limit=int(limit), time=time)

@app.route("/prod/manufacture/<meal>/<place>/<limit>/<time>")
@cross_origin()
def get_manufacture_prod(meal,place,limit,time):
    print(meal)
    return get_manufacturing.get_manufacturing_prod(meal=meal, delivery_place=place, limit=int(limit), time=time)

@app.route("/prod/manufactur_production")
@cross_origin()
def get_manufacture_prod_production():
    return get_manufacturing.get_manufacturing_production_prod()


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)

