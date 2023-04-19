import requests
import pandas as pd
from datetime import date
from time import sleep
from produce import make_producer, on_delivery
from dsnkafka.config import config, DEFAULT_TOPIC

FIRSTEEDSDATE = date(2023,4,17)

producer = make_producer()

url='https://api.energidataservice.dk/dataset/GasSystemRightNow?offset=0&start=' + FIRSTEEDSDATE.strftime("%Y-%m-%d") + 'T00:00&sort=TimestampUTC%20DESC&timezone=dk'

response = requests.get(url=url)

result = response.json()

records = result.get('records', [])
                                        
df = pd.DataFrame(records)

df = df.drop(['TimestampDK','TYRA_Time','TYRA_Flow','Biogas_Time','Biogas_Flow','CO2Emission','Nybro_Flow','Nybro_GCV','Egtved_GCV','ExitZone_Flow'],axis='columns')

df['TimestampUTC'] = pd.to_datetime(df['TimestampUTC'])

#print(df.dtypes)

# #df['Dragoer_GCV'] = pd.to_numeric(df['Dragoer_GCV'])
# df['Dragoer_GCV'].str.replace('.',',')

df3 = df.to_dict(orient='records')

for item in df3:
    print(item)

    item = {k.upper():v for k,v in item.items()}
    producer.produce(topic=DEFAULT_TOPIC,value=item,on_delivery=on_delivery)
    producer.flush()

# while True:
#     response = requests.get(url=url)

#     result = response.json()

#     records = result.get('records', [])
                                            
#     df1 = pd.DataFrame(records)

#     df1 = df1.drop(['TimestampDK','TYRA_Time','TYRA_Flow','Biogas_Time','Biogas_Flow','CO2Emission','Nybro_Flow','Nybro_GCV','Egtved_GCV','ExitZone_Flow'],axis='columns')

    
#     #print(df1.to_dict(orient='records'))
    
#     df2 = pd.concat([df,df1]).drop_duplicates(keep=False)
#     df2 = df2.to_dict(orient='records')

#     for item in df2:
#         print(item)
#         producer.produce(topic=DEFAULT_TOPIC,value=item,on_delivery=on_delivery)
#         producer.flush()

#     df = df1

#     print(df2)

#     sleep(5)
