# Import packages
import pandas as pd
import numpy as np
import psycopg2
from psycopg2 import extras

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
from configs.constants import Constants

class SqlUtils:
    def __init__(self, 
                 host = Constants.dbV1Host,
                 database = Constants.dbV1Database,
                 user = Constants.dbV1Username,
                 password = Constants.dbV1Password):
        self.host       = host
        self.database   = database
        self.user       = user 
        self.password   = password
        self.connection = psycopg2.connect(
            host        = host,
            database    = database,
            user        = user,
            password    = password
        )
        self.pandasToPostgresMap = {
            'int64' : 'integer',
            'int32' : 'integer',
            'float64' : 'float',
            'float32' : 'float',
            'boolean' : 'boolean',
            'bool' : 'boolean',
            'object' : 'text',
            'datetime64[ns]' : 'timestamp'
        }

    def runQuery(self, stmt : str):
        if self.connection.closed == 0:
            self.connection = psycopg2.connect(
                host        = self.host,
                database    = self.database,
                user        = self.user,
                password    = self.password
            )
        connection = self.connection
        connectionCursor = connection.cursor()
        connectionCursor.execute(stmt)
        connection.commit()

    def getQuery(self, stmt : str):
        if self.connection.closed == 0:
            self.connection = psycopg2.connect(
                host        = self.host,
                database    = self.database,
                user        = self.user,
                password    = self.password
            )
        connection = self.connection
        connectionCursor = connection.cursor()
        connectionCursor.execute(stmt)
        connection.commit()
        result = connectionCursor.fetchall()
        return result
    
    def insertIntoTable(self, df : pd.DataFrame, table_name : str):
        if self.connection.closed == 0:
            self.connection = psycopg2.connect(
                host        = self.host,
                database    = self.database,
                user        = self.user,
                password    = self.password
            )
        tuples = tuple(df.replace({np.nan: None, '': None}).itertuples(index=False, name=None))
        stmt = f"""
        INSERT INTO {table_name} ({", ".join(['"'+str(col)+'"' for col in df.columns])}) 
        VALUES ({", ".join(['%s' for col in df.columns])})
        """
        connection = self.connection
        connectionCursor = connection.cursor()
        extras.execute_batch(connectionCursor, stmt, tuples)
        connection.commit()

    def updateTable(self, df : pd.DataFrame, table_name : str, primary_keys : list):
        if self.connection.closed == 0:
            self.connection = psycopg2.connect(
                host        = self.host,
                database    = self.database,
                user        = self.user,
                password    = self.password
            )
        columns = list(df.columns)
        stmt = f"""
        UPDATE {table_name} 
        SET {", ".join([col+" = %s" for col in columns if col not in primary_keys])}
        WHERE {" AND ".join([col+" = %s" for col in primary_keys])}
        """
        columns = [col for col in columns if col not in primary_keys] + primary_keys
        df = df[columns]
        tuples = tuple(df.replace({np.nan: None, '': None}).itertuples(index=False, name=None))
        connection = self.connection
        connectionCursor = connection.cursor()
        extras.execute_batch(connectionCursor, stmt, tuples)
        connection.commit()

    def closeConnection(self):
        if self.connection.closed == 0:
            self.connection = psycopg2.connect(
                host        = self.host,
                database    = self.database,
                user        = self.user,
                password    = self.password
            )
        connection = self.connection
        connection.close()