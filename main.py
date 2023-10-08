from flask import Flask, request
from flask_cors import CORS, cross_origin
import getByTwo
import getByThree
import finalSuitability
import getReport

app = Flask(__name__)
CORS(app, resources={r"/": {"origins": "*"}})

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
        return getReport.get_report_dev(meal=meal)
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/prod/getReport/<meal>")
@cross_origin()
def get_report_prod(meal):
    try:
        return getReport.get_report_prod(meal=meal)
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/dev/finalSuitability", methods=["POST"])
@cross_origin()
def finalSuitability_dev():
    try:
        if request.data:
            print(request.json)
            return finalSuitability.final_dev(request.json['ids'])
        else:
            return {
                "state": False,
                "message": "error no body"
            }
    except:
        return {
            "state": False,
            "message": "error"
        }

@app.route("/prod/finalSuitability", methods=["POST"])
@cross_origin()
def finalSuitability_prod():
    try:
        if request.data:
            print(request.json)
            return finalSuitability.final_prod(request.json['ids'])
        else:
            return {
                "state": False,
                "message": "error no body"
            }
    except:
        return {
            "state": False,
            "message": "error"
        }


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)

