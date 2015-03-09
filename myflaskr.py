#-*-coding: utf-8 -*-
"""
	myflaskr microblog
	v0.1
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack

#configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRETY_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#crete my app
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MYFLASKR_SETTINGS', silent = True)
# config end

# DATABASE (sqlite)
# create  schema.sql create mybolg's table
#  schema.sql:
"""
drop talbe if exists entries:
create table entries (
	id integer primary key autoincrement,
	title string not null,
	text string not null
);
"""
#init _db from schema.sql
def init_db():
	db = get_db()
	with app.app_context('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()

# open a new db connection
def get_db():
	if not hassattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.ROW
	return rv

@app.cli.command('initdb')
def initdb_command():
	init_db()
	print 'Initialized the database.'

