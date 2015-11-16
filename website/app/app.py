from flask import Flask
from flask import render_template,jsonify,request
import re
app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello_world(name = None):
    return render_template('hello.html', name=name)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search',methods=['GET'])
def search(result = None):
	query = request.args['q']
	#use regular expression to split the query
	keywords = re.split('; |, |\*| |\n',query)
	print keywords
	#dic = {}
	#dic['test'] = keywords
	#return jsonify(dic)
	if keywords[0] != "":
		return render_template('result.html',result = keywords)
	else:
		return render_template('result.html')
if __name__ == '__main__':
    app.run(debug=True)