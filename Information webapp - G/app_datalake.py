# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 19:22:15 2021

@author: tooru
"""

from flask import Flask, render_template, request, url_for
import tierdatalake.querydatalake as qdl
import tierdatalake.dataConnection as dc
import math
import csv
from flask import make_response
import cgi

app = Flask(__name__)

schema = 'Insert Schema Name'

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reporteador')
def reporteador():        
    q_ora_tables = """ SELECT TABLE_NAME, STATUS, LAST_ANALYZED FROM SYS.ALL_TABLES WHERE OWNER = '""" + schema + """' """ 
    df = dc.qDataLakeConn(q_ora_tables)
    return render_template('tableView.html', tablas = df)

@app.route('/search' , methods=['POST'])
def search():      
    stop_words = qdl.stop_words

    search_like = request.form['search_like']
    search_like = search_like.upper()     

    search_split = search_like.split(" ")
    
    search_like = ""
    for i in search_split:
        if i not in stop_words:
            search_like += """ AND ( upper(TABLE_NAME) LIKE '%""" + i + """%' )"""
    
    try:
        q_ora_tables = """ SELECT TABLE_NAME, STATUS, LAST_ANALYZED FROM SYS.ALL_TABLES WHERE OWNER = '""" + schema + """' """ + search_like 
        df = dc.qDataLakeConn(q_ora_tables)
    except:
        q_ora_tables = """ SELECT TABLE_NAME, STATUS, LAST_ANALYZED FROM SYS.ALL_TABLES WHERE OWNER = '""" + schema + """' """
        df = dc.qDataLakeConn(q_ora_tables)
        
    return render_template('tableView.html', tablas = df)

@app.route('/reporte_tabla/<table_name>', methods=['POST','GET'])
def reporte_i(table_name):
    q_reporte = """ SELECT * FROM """ + schema + """.""" + table_name + " WHERE ROWNUM<=100 """
            
    df = dc.qDataLakeConn(q_reporte)
    resp = make_response(df.to_csv(index=False,encoding='utf-8-sig'))
    resp.headers["Content-Disposition"] = "attachment; filename=download_" + table_name + ".csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/reporte_tabla_top/<table_name_top>')
def muestra_i(table_name_top):
    q_reporte = """ SELECT * FROM """ + schema + """.""" +  table_name_top + " WHERE ROWNUM<=100"
    df = dc.qDataLakeConn(q_reporte)
    resp = make_response(df.to_csv(index=False,encoding='utf-8-sig'))
    resp.headers["Content-Disposition"] = "attachment; filename=muestra_" + table_name_top + ".csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

@app.route('/reporte_tabla_json/<table_name_json>')
def reporte_json(table_name_json):
    q_reporte = """ SELECT * FROM """ + schema + """.""" +  table_name_json + " WHERE ROWNUM<=100"
    df = dc.qDataLakeConn(q_reporte)
    jsonfiles = df.to_json(orient='records') 
    return jsonfiles

@app.route('/dashboards')
def dashboards():
    return render_template('dashboards.html')