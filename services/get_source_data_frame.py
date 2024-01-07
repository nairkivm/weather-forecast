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

def getSourceDataFrame(
        gSheetId : str, 
        gSheetGId : str, 
        skiprows : int = 3
    ):
    # Extract Data
    dataFrame = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/"+
        gSheetId+
        "/export?gid="+
        gSheetGId+
        "&format=csv",
        skiprows=skiprows
    )
    return dataFrame