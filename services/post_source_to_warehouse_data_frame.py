# Import packages
import pandas as pd 
import pytz
from datetime import datetime

# Untuk kembali ke directory utama
import sys
import os
sys.path.insert(
    0, os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..'
        )
    )
)

def postSourceToWarehouseDataFrame(
        dataFrame : pd.DataFrame,
        category : str
    ):
    # # Store into data warehouse
    # dataFrame.to_csv(
    #     '../data_warehouse/'+
    #     str(category).replace(' ','_')+
    #     '/'+
    #     datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime('%Y-%m-%d')+
    #     '-'+
    #     str(category).replace(' ','-')+
    #     '-kab-kupang.csv',
    #     index=False
    # )
    # Store into data warehouse
    dataFrame.to_csv(
        './data_warehouse/'+
        str(category).replace(' ','_')+
        '/'+
        datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime('%Y-%m-%d')+
        '-'+
        str(category).replace(' ','-')+
        '-kab-kupang.csv',
        index=False
    )
    print(
        "Data has been stored at "+
        datetime.now(tz=pytz.timezone("Asia/Jakarta")).strftime('%Y-%m-%d %H:%M:%S')+
        " UTC+7"
    )
