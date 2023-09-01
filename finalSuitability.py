import getCsv_dev
import getCsv_prod

csv_dev = getCsv_dev.getCSV()
csv_prod = getCsv_prod.getCSV()

def get_suitability(param_list , df):
    total_suitability = 0
    for i in range(len(param_list) - 1):
        df2 = df.loc[df['number'] == param_list[i]]
        for j in range(i + 1, len(param_list)):
            total_suitability += int(df2[str(param_list[j])])
    return total_suitability / 6

def final_dev(param_list):
    df = csv_dev
    response = {
        "state": True,
        "data": get_suitability(param_list=param_list , df=df)
    }
    return response


def final_prod(param_list):
    df = csv_prod
    response = {
        "state": True,
        "data": get_suitability(param_list=param_list , df=df)
    }
    return response

