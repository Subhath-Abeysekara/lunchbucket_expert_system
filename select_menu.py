from bson import ObjectId
import pandas as pd
import random
from menu_prediction import prediction, input_data
from select_limits import get_day_of_week
from service import connect_mongo_food

collection_name = connect_mongo_food()

def get_maximum_packets(A):
  packets = 0
  while len(A) >= 3:
    min_index = A.index(min(A))
    min_value = A.pop(min_index)
    A = [x - min_value for x in A]
    packets+= min_value
  return packets

def get_possible_mixed_pairs(A , B , C):
  pairs = []
  for a in A:
    for b in B:
        for c in C:
            pair = {
                'vege':a,
                'condiment':b,
                'meat':c
            }
            pairs.append(pair)
  for pair in pairs:
    print(pair)
  return pairs

def select_best_menu(meal , holiday , whether , temperature):
    items = collection_name.find()
    veges = []
    condiments = []
    meats = []
    day = get_day_of_week()
    for item in items:
        input_data['food_type'] = item['type']
        input_data['meal'] = meal
        input_data['day'] = day
        input_data['holiday'] = holiday
        input_data['whether'] = whether
        input_data['temperature'] = temperature
        print(input_data)
        prediction_ = round(prediction(input_data))
        if item['category'] == "vege":
            object_ = {
                "type": item['type'],
                "prediction": prediction_,
                "id": str(item['_id'])
            }
            veges.append(object_)
        elif item['category'] == "stew":
            object_ = {
                "type": item['type'],
                "prediction": prediction_,
                "id": str(item['_id'])
            }
            condiments.append(object_)
        else:
            object_ = {
                "type": item['type'],
                "prediction": prediction_,
                "id": str(item['_id'])
            }
            meats.append(object_)
    df = pd.read_csv("lb_suitability_dataset.csv")
    filter_veges_used = []
    filter_veges_nused = []
    for vege in veges:
        try:
            print(df[vege['type']])
            filter_veges_used.append(vege)
        except:
            filter_veges_nused.append(vege)

    print(len(filter_veges_used))
    print(len(filter_veges_nused))
    filter_condiments_used = []
    filter_condiments_nused = []
    for condiment in condiments:
        try:
            print(df[condiment['type']])
            filter_condiments_used.append(condiment)
        except:
            filter_condiments_nused.append(condiment)

    print(len(filter_condiments_used))
    print(len(filter_condiments_nused))
    filter_meats_used = []
    filter_meats_nused = []
    for meat in meats:
        try:
            print(df[meat['type']])
            filter_meats_used.append(meat)
        except:
            filter_meats_nused.append(meat)

    print(len(filter_meats_used))
    print(len(filter_meats_nused))

    data = filter_veges_used
    random.shuffle(data)
    pairs_vege = [data[i:i + 10] for i in range(0, len(data), 10)]
    if len(pairs_vege[-1]) == 1:
        pairs_vege[-2].extend(pairs_vege[-1])
        pairs_vege.pop()
    for idx, pair in enumerate(pairs_vege, 1):
        print(f"Group {idx}: {len(pair)}")
        print(pair)
        if len(pair) < 8:
            pairs_vege.remove(pair)

    data = filter_condiments_used
    random.shuffle(data)
    pairs_condiment = [data[i:i + 6] for i in range(0, len(data), 6)]
    if len(pairs_condiment[-1]) == 1:
        pairs_condiment[-2].extend(pairs_condiment[-1])
        pairs_condiment.pop()
    for idx, pair in enumerate(pairs_condiment, 1):
        print(f"Group {idx}: {len(pair)}")
        print(pair)
        if len(pair) < 5:
            pairs_condiment.remove(pair)

    data = filter_meats_used
    random.shuffle(data)
    pairs_meat = [data[i:i + 6] for i in range(0, len(data), 6)]
    if len(pairs_meat[-1]) == 1:
        pairs_meat[-2].extend(pairs_meat[-1])
        pairs_meat.pop()
    for idx, pair in enumerate(pairs_meat, 1):
        print(f"Group {idx}: {len(pair)}")
        print(pair)
        if len(pair) < 5:
            pairs_meat.remove(pair)

    pairs = get_possible_mixed_pairs(C=pairs_meat, B=pairs_condiment, A=pairs_vege)

    pairs_combined = []
    for pair in pairs:
        print(pair)
        new_pair = []
        new_pair.extend(pair['vege'])
        new_pair.extend(pair['condiment'])
        new_pair.extend(pair['meat'])
        print(new_pair)
        pairs_combined.append(new_pair)

    groups = []
    for idx, pair in enumerate(pairs_combined, 1):
        print(f"Group {idx}: {len(pair)}")
        total_suitability = 0
        total_count = []
        for i in range(len(pair)):
            total_count.append(pair[i]['prediction'])
            for j in range(i + 1, len(pair)):
                total_suitability += list(df[df['Unnamed: 0'] == pair[i]['type']][pair[j]['type']])[0]
        print(get_maximum_packets(total_count), total_suitability)
        object_ = {
            'group': pair,
            'max_packets': get_maximum_packets(total_count),
            'suitability': total_suitability
        }
        groups.append(object_)

    sorted_groups = sorted(groups, key=lambda x: x['max_packets'] * x['suitability'])

    best_group1 = sorted_groups.pop()
    best_group2 = sorted_groups.pop()
    print(best_group1 , best_group2)
    return {
        "best1" : best_group1,
        "best2" : best_group2
    }
