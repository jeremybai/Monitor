#!/usr/bin/env python
#-*-encoding:utf-8-*-

import os
import time
from flask import Flask, request, session, g, redirect, url_for, render_template, flash
from flask_bootstrap import Bootstrap
import json
import MySQLdb
import re
import hashlib


app = Flask(__name__)

app.config.update(dict(
    DEBUG = True,
    SECRET_KEY = '\xa3y\xf8\x17\xc7\n\xf1\x95\xbbZ\xa5\xf2\xe2\x16\xb4\xf9\xf4\x97G[JZ\xc4\xe8'
))

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
		email = request.form['email']
		passwd = request.form['passwd']
		if email and passwd :
			if validateemail( email ):
				db = MySQLdb.connect( host='localhost', user='root', passwd='bx123456', db='raspberry_info') 
				cursor = db.cursor()
				sql = "SELECT * FROM USER WHERE EMAIL = '%s'" % (email)
				cursor.execute(sql)
				results = cursor.fetchall()
				if results: 
					# 获得每条数据
					rows=[x for x in cursor]
					# 获得字段名称
					cols = [x[0] for x in cursor.description]
					data = []
					for row in rows:
						entry = {}
						for prop, val in zip(cols, row):
							entry[prop] = val
						data.append(entry)					
					# 对密码进行2次md5加密
					passwd_md5 = hashlib.md5(hashlib.md5(passwd).hexdigest()).hexdigest()
					if entry['PASSWD'] == passwd_md5:
						cursor.close()
						db.close()
						session['logged_in'] = True
						flash('You were logged in')
						return redirect(url_for('index')) 
				cursor.close()
    return render_template('index.html', error=error)
	
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
		email = request.form['email']
		passwd = request.form['passwd']
		if email and passwd :
			if validateemail( email ):
				# 对密码进行2次md5加密
				passwd_md5 = hashlib.md5(hashlib.md5(passwd).hexdigest()).hexdigest()
				db = MySQLdb.connect( host='localhost', user='root', passwd='bx123456', db='raspberry_info') 
				cursor = db.cursor()
				sql = "INSERT INTO USER(EMAIL, PASSWD) VALUES ('%s','%s')" % (email, passwd_md5)
				cursor.execute(sql)
				db.commit()
				cursor.close()
				session['logged_in'] = True
				flash('You were logged in')
				return redirect(url_for('index'))  
    return render_template('index.html', error=error)	
	
@app.route('/logout')
def logout():
    error = None
    session.pop('logged_in', None)
    return redirect(url_for('index'))

def createdb():
	db = MySQLdb.connect( host='localhost', user='root', passwd='bx123456')
	cursor = db.cursor()
	cursor.execute('create database if not exists raspberry_info')
	db.select_db('raspberry_info')
	sql = '''CREATE TABLE IF NOT EXISTS TEMPERATURE (
		ID    INT      AUTO_INCREMENT NOT NULL PRIMARY KEY,
		TIME  DATETIME  ,
		CPU_TEMP  FLOAT ,
		GPU_TEMP  FLOAT  )'''
	cursor.execute(sql)
	sql = '''CREATE TABLE IF NOT EXISTS USER (
		ID     INT      AUTO_INCREMENT NOT NULL PRIMARY KEY,
		NAME   VARCHAR(32)  ,
		PASSWD VARCHAR(32)  ,
		EMAIL  VARCHAR(32)  )'''
	cursor.execute(sql)	

def validateemail(email):
	if len(email) > 7:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
			return True
	return False	
	
if __name__ == '__main__':
	#createdb()
	app.run(host='0.0.0.0', port=5001)
