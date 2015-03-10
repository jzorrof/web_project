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
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# open a new db connection
def get_db():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
    return top.sqlite_db

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.ROW
    return rv

@app.teardown_appcontext
def close_db_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        pass #top.sqlite_db.close()

if __name__ == '__main__':
    init_db()
    app.run()