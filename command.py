__author__='Joe_Fan'
from flask.ext.script import Manager
from myflaskr import app

manager = Manager(app)

@manager.command
def hello():
    print "Hello"

if __name__ == "__main__":
    manager.run()