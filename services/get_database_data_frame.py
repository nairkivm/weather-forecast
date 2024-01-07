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

from utils.sql_utils import SqlUtils

def getDatabaseDataFrame(
        table_name : str,
        columns : list,
        conditions : list = None
    ):
    if conditions == None:
        conditionsStmt = ""
    else:
        conditionsStmt = f"""
        WHERE {" AND ".join(str(cnd) for cnd in conditions)}
        """
    # Load from database
    queryStmt = f"""
    SELECT {", ".join('"'+str(col)+'"' for col in columns)}
    FROM "{table_name}"
    {conditionsStmt}
    ;
    """
    dataFrame = pd.DataFrame(SqlUtils().getQuery(queryStmt), columns = columns)
    return dataFrame