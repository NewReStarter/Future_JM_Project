import pandas as pd
from pandas import DataFrame, Series

df = pd.read_json('../Desktop/data.json')

import json
def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    except JSONDecodeError:
        return False
    else:
        return True


for i in range(0,df.index.max()+1):
    if(is_json(df['json_data'][i])):
        data = json.loads(df['json_data'][i])
        del data['personal_info']
        df['json_data'][i] = json.dumps(data)
    else:
        df['json_data'][i] = 'invalid'


df.to_csv('../Desktop/data2.csv')