import os
from flask import Flask, url_for, render_template, request, url_for
from flask import redirect
from werkzeug import secure_filename

UPLOAD_FOLDER = '/home/fanzhong/path/to/the/uploads'
ALOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
####upload demo
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
####upload demo

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

#test
with app.test_request_context('/hello', method='POST'):
	assert request.path == '/hello'
	assert request.method == 'POST'

# session
@app.route('/login2', methods=['POST', 'GET'])
def login2():
	error = None
	# if request.method == 'POST':
	# 	if valid_login(request.form['username'],
	# 				   request.form['password']):
	# 		return log_the_user_in(request.form['username'])
	# 	else:
	# 		error = 'Invalid username/password'
	# return render_template('login.html',error = error)
	if request.method =='POST':
		if request.form['username'] != 'JOE':
			error = 'error username'
		elif request.form['password'] != 'abcd1234':
			error = 'error password'
		else:
			print 'login!!'
	return render_template('login.html',error = error)

## upload demo
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	uploaded_filename = None
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],
				filename))
			return redirect(url_for('upload_file'))
	return render_template('upload.html')

if __name__ == '__main__':
	app.run(debug=True)