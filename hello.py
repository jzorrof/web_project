from flask import Flask, url_for, render_template
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

@app.route('/testtemp/')
@app.route('/testtemp/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

with app.test_request_context():
	print url_for('hello_world')
	#print url_for('test_via')
	print url_for('test_via', test='test/')
	print url_for('test_via_int', testint = 123)
	print url_for('hello')

if __name__ == '__main__':
	app.run(debug=True)