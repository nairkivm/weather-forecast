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

def getWarehouseDataFrame(
        category : str
    ):
    # # Load from data warehouse
    # dataFileDirectory = os.path.abspath(
    #     os.path.join(
    #         os.path.join(
    #             os.getcwd(), '..'
    #         ), 'data_warehouse/'+
    #         str(category).replace(' ','_')
    #     )
    # )
    # Load from data warehouse
    dataFileDirectory = os.path.abspath(
        os.path.join(
            os.getcwd(), 
            'data_warehouse/'+str(category).replace(' ','_')
        )
    )
    print("dataFileDirectory", dataFileDirectory, os.path.isdir(dataFileDirectory))
    dataFileList = os.listdir(dataFileDirectory)
    lastAddedFile = sorted(dataFileList)[-1]
    
    dataFrame = pd.read_csv(
        os.path.join(os.path.dirname(__file__),
            '../data_warehouse/'+
            str(category).replace(' ','_')+
            '/'+
            lastAddedFile
        )
    )
    return dataFrame