#!/usr/bin/env python
#-*-encoding:utf-8-*-

import os
import time
from flask import Flask, request, session, g, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
import json
import MySQLdb

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')   


@app.route('/temp')
def temp():
	db = MySQLdb.connect( host='localhost', user='root', passwd='bx123456', db='raspberry_info') 
	cursor = db.cursor()
	sql = "SELECT * FROM TEMPERATURE ORDER BY ID DESC LIMIT 10"
	cursor.execute(sql)
	results = cursor.fetchall()
	# 获得每条数据
	rows=[x for x in cursor]
	# 获得字段名称
	cols = [x[0] for x in cursor.description]
	data = []
	for row in rows:
		entry = {}
		for prop, val in zip(cols, row):
			if prop == 'TIME':
				entry[prop] = val.strftime("%Y-%m-%d %H:%M:%S")
			else:
				entry[prop] = val
		data.append(entry)
	cursor.close()
	return render_template('temp.html', message = data)   
	
@app.route('/addtemp')	
def addtemp():
	db = MySQLdb.connect( host='localhost', user='root', passwd='bx123456', db='raspberry_info') 
	cursor = db.cursor()
	sql = "SELECT * FROM TEMPERATURE ORDER BY ID DESC LIMIT 1"
	cursor.execute(sql)
	results = cursor.fetchall()
	# 获得每条数据
	rows=[x for x in cursor]
	# 获得字段名称
	cols = [x[0] for x in cursor.description]
	data = []
	for row in rows:
		entry = {}
		for prop, val in zip(cols, row):
			if prop == 'TIME':
				entry[prop] = val.strftime("%Y-%m-%d %H:%M:%S")
			else:
				entry[prop] = val
		data.append(entry)
	cursor.close()
	data_json = json.dumps(entry)
	return data_json
	

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)
