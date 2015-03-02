from flask import Flask, url_for
app = Flask(__name__)

@app.route('/hello')
def hello_world():
	return 'Hello World'

## int float and path
@app.route('/abcd1234/<test>')
def test_via(test):
	return 'test %s' % test

@app.route('/test/<int:testint>')
def test_via_int(testint):
	return 'testint %d' % testint

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		pass
	elif request.method == 'POST':
		pass

with app.test_request_context():
	print url_for('hello_world')
	#print url_for('test_via')
	print url_for('test_via', test='test/')
	print url_for('test_via_int', testint = 123)

if __name__ == '__main__':
	app.run()