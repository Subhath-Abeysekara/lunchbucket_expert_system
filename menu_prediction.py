import numpy as np
import joblib
from menu_availability import set_food_availability

Features = {
  "food_type" : {'white rice': 0, 'Pol Sambol': 1, 'Dhal Curry Thelata': 2, 'Fish Kiri Hodi': 3, 'Chicken Mixed Vege Salad': 4, 'Creamy Chicken Curry Regular': 5, 'Soya meat curry': 6, 'Battered Mushroom Salad': 7, 'Fried Fish (Salaya - 3)': 8, 'Ala Halmasso Thelata': 9, 'Halmassan Themparaduwa': 10, 'Vege Salad': 11, 'Chicken Themparaduwa': 12, 'Vatakolu curry': 13, 'Vegetable Egg Omlet': 14, 'Creamy Chicken Curry Large': 15, 'Dhal Curry Kirata': 16, 'Chicken Baduma': 17, 'Mushroom curry': 18, 'Prawns Thelata': 19, 'Kunisso Baduma': 20, 'Fried Chicken Favor Piece': 21, 'Malu Miris Thelata': 22, 'red rice': 23, 'NoodlesChicken Egg Noodle': 24, 'Ala Kiri Hodi': 25, 'Fried Paraa Fish': 26, 'Carrot curry': 27, 'Halmassan Thelata': 28, 'Paraa Malu Kirata': 29, 'Fried RiceTHREE FIFTY Pack': 30, 'Dhal curry Thelata': 31, 'Kochchi Pol Sambal': 32, 'Chicken Cutlet': 33, 'Maalu Miris Pirawuma Kirata': 34, 'Fried RiceMeaty Mighty - 2 Persons': 35, 'Red rice': 36, 'Kadala curry': 37, 'Gowa malluma': 38, 'Pathola Curry': 39, 'Muhudu Kukula Karawala Baduma': 40, 'White rice': 41, 'Sausage Mixed Vege Salad': 42, 'Chicken Curry Regular Piece': 43, 'Kiri Kos Curry': 44, 'Gowa mal curry kirata': 45, 'Chicken Curry Favor Piece': 46, 'Mushroom curry Mirisata': 47, 'Gotukola Sambal': 48, 'Gizzard Curry Regular': 49, 'Mushroom Thelata': 50, 'Mixture': 51, 'Cucumber curry': 52, 'Bonchi curry kirata': 53, 'Annasi Curry': 54, 'Fish Bistek': 55, 'Kadala Parippu Curry': 56, 'Bonchi Malluma': 57, 'Bandakka curry': 58, 'Thumba Karawila curry': 59, 'Kankun Thelata (Srilankan)': 60, 'Manioc Ala Malluma': 61, 'Linna Karawala Baduma': 62, 'Salmon Thelata (Premier Brand)': 63, 'Annasi curry': 64, 'Kadala Parippu curry': 65, 'Wambatu mojuwa': 66, 'Mushroom Cutlet': 67, 'Mugunuwanna Malluma': 68, 'Fried Fish (Bolla)': 69, 'Beetroot Curry': 70, 'Dambala Mallum': 71, 'Karawila Salad': 72, 'Mushroom curry Kirata': 73, 'Prawn Salad': 74, 'Arthapal Thelata': 75, 'Chicken Curry Kirata': 76, 'Battered Prawn Salad': 77, 'Athu Gowa Malluma': 78, 'Wattakka kalupola': 79, 'Wambatu curry': 80, 'Fried Potato Salad': 81, 'Bala Karawala Baduma': 82, 'Mushroom themparaduwa': 83, 'VegetarianVege Delight': 84, 'Kawpi Curry': 85, 'Ambarella Curry': 86, 'Nelum Ala curry': 87, 'Kankun Malluma': 88, 'Kos malluma': 89, 'Egg Vege Cutlet': 90, 'Chicken Curry': 91, 'Karawala Baduma': 92, 'Thalapath Karawala Baduma': 93, 'Mora karawala baduma': 94, 'Malu Miris Pirawuma Kirata': 95, 'Vege Mixed Battered Cuttlefish Sala': 96, 'Vege Mixed Battered Cuttlefish Salad': 97, 'Chicken White Curry': 98, 'Wambatu themparaduwa': 99, 'Wambatu Badala Kirata': 100, 'Kumbala Karawala Baduma': 101, 'Sausage Thelata (2)': 102, 'Fried Papadam Miris(2)': 103, 'Mixed Meat Vege Salad': 104, 'Fried Cuttlefish': 105, 'Fish Badala': 106, 'Prawns Cutlet': 107, 'Watu Biththara Thelata': 108, 'Mushroom Salad': 109, 'Sausage Cutlet': 110, 'Halmassan Curry Kirata': 111, 'Simple and SuperBattered Chicken Meal': 112, 'Gizzard Curry Large': 113, 'Bandakka Fried Salad': 114, 'Kunissan Sambol': 115, 'Chicken Bistek Regular': 116, 'Egg Bulls Eye': 117, 'Malu Miris Kirata': 118, 'Arthapal Baduma': 119,
                 'Leeks Thelata': 120, 'VegetarianVege Balanced Meal': 121 , 'Nan':122},
  "meal" : {'Dinner': 0, 'Lunch': 1 , 'Nan':3},
  "last_menu_availability_1" : {True: 0, False: 1},
  "last_menu_availability_2" : {True: 0, False: 1},
  "last_menu_availability_3" : {True: 0, False: 1},
  "last_menu_availability_4" : {True: 0, False: 1},
  "last_menu_availability_5" : {True: 0, False: 1},
  "whether" : {'Partly Cloudy': 0, 'Scattered Thunderstromes': 1, 'Scattered Showers': 2, 'Mostly Sunny': 3 , 'Nan':4},
  "day" : {'Wednesday': 0, 'Thursday': 1, 'Friday': 2, 'Monday': 3, 'Saturday': 4, 'Tuesday': 5, 'Sunday': 6 , 'Nan':7},
  "holiday" : {'No': 0, 'Yes': 1,'Nan':3}
}
Row_features = {
    "temperature" : 90,
}

input_data = {
    "food_type" : "Kankun Thelata (Srilankan)",
    "meal" : "Lunch",
    "whether" : "Mostly Sunny",
    "temperature" : 90,
    "day" : 'Wednesday',
    "holiday" : 'No',
    "last_menu_availability_1" : 0,
    "last_menu_availability_2" : 0,
    "last_menu_availability_3" : 0,
    "last_menu_availability_4" : 0,
    "last_menu_availability_5" : 0,
}
def prediction(input_data):
  datapoint = []
  row = set_food_availability(food=input_data['food_type'], meal=input_data['meal'])
  for key in input_data:
    if 'last_menu' in key:
        datapoint.append(row[key])
    else:
        try:
            print(Row_features[key])
            datapoint.append(input_data[key])
        except:
            try:
                datapoint.append(Features[key][input_data[key]])
            except:
                datapoint.append(Features[key]['Nan'])
  datapoint = np.array(datapoint)
  datapoint = datapoint.reshape(1, -1)
  # print(datapoint)
  load_model = joblib.load('lb_menu_predict_model_advance.h5')
  y_pred = load_model.predict(datapoint)
  # print(y_pred[0])
  return y_pred[0]

# prediction(input_data)