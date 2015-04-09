#-*-coding: utf-8 -*-
"""
    myflaskr microblog
    v0.1
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack

# DATABASE = '/tmp/flaskr.db'
# DEBUG = True
# SECRET_KEY = 'development key'
# USERNAME = 'admin'
# PASSWORD = 'default'

#crete my app
app = Flask(__name__)

#configuration
#load setting as dict
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'flaskr.db'),
    DEBUG = True,
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = 'default'
))
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
    """init database"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('init_db')
def initdb_command():
    init_db()
    print('Initialized the database.')

# open a new db connection
def get_db():
    # top = _app_ctx_stack.top
    # if not hasattr(top, 'sqlite_db'):
    #     sqlite_db = sqlite3.connect(app.config['DATABASE'])
    #     sqlite_db.row_factory = sqlite3.Row
    #     top.sqlite_db = sqlite_db
    # return top.sqlite_db
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# @app.teardown_appcontext
# def close_db_connection(exception):
#     top = _app_ctx_stack.top
#     if hasattr(top, 'sqlite_db'):
#         top.sqlite_db.close()
@app.teardown_appcontext
def close_db(error):
    """Close the database"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('myflaskr/myf_show_entries.html', entries = entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
                [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error=None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'InValid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'InValid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('myflaskr/myf_login.html',error = error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))