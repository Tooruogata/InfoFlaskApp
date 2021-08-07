# -*- coding: utf-8 -*-
"""
Created on Fri Aug  6 20:39:13 2021

@author: tooru
"""

import pandas as pd
import cx_Oracle
from sqlalchemy import types, create_engine
import time

client_path = r"D:\Programas\instantclient_19_9"

user        = 'Insert schema name'
password    = 'Password of schema'
ip          = 'IP number'
port        = 'Port number'
sid         = 'SID'

engine_str  = 'oracle://' + user + ':' + password + '@' + ip + '/' + sid


cx_Oracle.init_oracle_client(lib_dir = client_path)
engine = create_engine(engine_str, echo=False)

def qDataLakeConn(query):

    db_tables = pd.read_sql_query(query,engine)
    return db_tables
