# Import packages
import pandas as pd 

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

# define map of python-postgresql datatype
pandasToPostgresMap = {
    'int64' : 'INTEGER',
    'int32' : 'INTEGER',
    'float64' : 'DOUBLE PRECISION',
    'float32' : 'DOUBLE PRECISION',
    'boolean' : 'BOOLEAN',
    'bool' : 'BOOLEAN',
    'object' : 'TEXT',
    'datetime64[ns]' : 'TIMESTAMP WITHOUT TIME ZONE'
}

def postWarehouseToDatabaseDataFrame(
        dataFrame : pd.DataFrame,
        table_name : str,
        primaryKey : str
    ):
    # Split dataframe into insert and update dataframe
    # Get already inserted record by the primary key (timestamp)
    queryStmt = f"""
    SELECT a.{primaryKey} 
    FROM {str(table_name).replace(' ','_')} a
    JOIN (SELECT UNNEST(CAST(ARRAY[
        {', '.join(
            ["'"+val+"'" for val in dataFrame[primaryKey].astype('str')]
        )}
        ] AS {pandasToPostgresMap[str(dataFrame[primaryKey].dtype)]}[])) {primaryKey}) b 
        ON a.{primaryKey} = b.{primaryKey}
    """
    try:
        insertedPrimaryKeyList = [tup[0] for tup in SqlUtils().getQuery(queryStmt)]
    except:
        insertedPrimaryKeyList = []
    # Update if there are inserted records
    if dataFrame[
        dataFrame[primaryKey].isin(insertedPrimaryKeyList)
    ].shape[0] > 0:
        SqlUtils().updateTable(
            dataFrame[
                dataFrame[primaryKey].isin(insertedPrimaryKeyList)
            ],
            table_name,
            [primaryKey]
        )
        print(
            "Updating "+
            str(dataFrame[
                dataFrame[primaryKey].isin(insertedPrimaryKeyList)
            ].shape[0])+
            " record(s) in "+
            table_name+
            " table completed!"
        )
    # Insert if there are uninserted records
    if dataFrame[
        ~dataFrame[primaryKey].isin(insertedPrimaryKeyList)
    ].shape[0] > 0:
        SqlUtils().insertIntoTable(
            dataFrame[
                ~dataFrame[primaryKey].isin(insertedPrimaryKeyList)
            ],
            table_name
        )
        print(
            "Inserting "+
            str(dataFrame[
                ~dataFrame[primaryKey].isin(insertedPrimaryKeyList)
            ].shape[0])+
            " record(s) into "+
            table_name+
            " table completed!"
        )