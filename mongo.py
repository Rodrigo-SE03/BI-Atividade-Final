import pandas as pd
from pymongo.mongo_client import MongoClient



local_uri = "mongodb://localhost:27017/"
client = MongoClient(local_uri)

db = client['ProjetoBI']
collection = db['notas_fiscais']

notas_fiscais = db['chaves_fiscais']
def aggregate(pipeline):
    result = list(collection.aggregate(pipeline))
    for doc in result:
        doc['_id'] = str(doc['_id'])
    return result

def get_dataframe():
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))
    df.rename(columns={'nome': 'produto',
                        'data_hora':'data', 
                        'forma_de_pagamento':'forma_pagamento'}, inplace=True)
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])
    return df