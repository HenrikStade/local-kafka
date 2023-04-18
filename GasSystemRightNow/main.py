import requests
import pandas as pd
from datetime import date
from time import sleep

FIRSTEEDSDATE = date(2023,4,17)

url='https://api.energidataservice.dk/dataset/GasSystemRightNow?offset=0&start=' + FIRSTEEDSDATE.strftime("%Y-%m-%d") + 'T00:00&sort=TimestampUTC%20DESC&timezone=dk'

response = requests.get(url=url)

result = response.json()

records = result.get('records', [])
                                        
df = pd.DataFrame(records)

df = df.drop(['TimestampDK','TYRA_Time','TYRA_Flow','Biogas_Time','Biogas_Flow','CO2Emission','Nybro_Flow','Nybro_GCV','Egtved_GCV','ExitZone_Flow'],axis='columns')

sleep(5)

print(df)

while True:
    response = requests.get(url=url)

    result = response.json()

    records = result.get('records', [])
                                            
    df1 = pd.DataFrame(records)

    df1 = df1.drop(['TimestampDK','TYRA_Time','TYRA_Flow','Biogas_Time','Biogas_Flow','CO2Emission','Nybro_Flow','Nybro_GCV','Egtved_GCV','ExitZone_Flow'],axis='columns')

    df2 = pd.concat([df,df1]).drop_duplicates(keep=False)

    df = df1

    print(df2)

    sleep(5)
