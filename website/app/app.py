 # -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template,jsonify,request
import re
app = Flask(__name__)

file_url_base = "./static/resources/documents/"
origin_url_base ="https://bbs.sjtu.edu.cn/bbstcon,board,LoveBridge,reid,######.html"

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
	#file = open('./static/resources/index.txt','r')
	#text = file.read( ).decode('utf-8')
	#file.close()
	results = []
	show_results = []
	query = request.args['q']
	if query == "":
		return render_template('result.html')
	#use regular expression to split the query
	keywords = re.split('; |, |\*| |\n',query)
	print keywords
	#dic = {}
	#dic['test'] = keywords
	#return jsonify(dic)

	file = open('./static/resources/index.txt','r')
	while True:
		line = file.readline().decode('utf-8')
		#print line
		if not line:
			break  
		if line.find(keywords[0])!=-1:
			start_pos = line.find('\t')
			urls_str = line[start_pos+1:-1]
			urls = re.split(';',urls_str)
			for url_org in urls:
				if url_org!="":
					url = re.split(':',url_org)
					url[1] = int(url[1])
					results.append(url)
			#print line
			#print urls
	file.close()
	results = sorted(results, key=lambda rt : rt[1],reverse = True) 
	#print results
	if len(results) == 0:
		return render_template('result.html')

	for result in results:
		document_file = open(file_url_base+result[0])
		content = document_file.read()
		#print content
		title_start_pos = content.find("2312")
		title_end_pos = content.find("饮水思源")
		title = content[title_start_pos+9:title_end_pos]
		url_start_pos = content.find("回复本文")
		url_end_pos = content.find("原帖")
		url_id = content[url_start_pos+13:url_end_pos]
		url = origin_url_base.replace("######",url_id)
		#content = re.sub(' ', '',content)
		summary_start_pos = content.find(keywords[0].encode('utf-8'))
		summary_end_pos = content.find("※来源")
		summary = content[summary_start_pos:summary_end_pos-2]
		#print summary
		#print title
		keywordLen = len(keywords[0])
		result_content = []
		result_content.append(title.decode("utf-8"))
		result_content.append(url)
		result_content.append(summary.decode("utf-8"))
		result_content.append(keywordLen)
		show_results.append(result_content)
		document_file.close()

	#print text.find(keywords[0])
	if keywords[0] != "":
		return render_template('result.html',result = show_results)
	else:
		return render_template('result.html')
if __name__ == '__main__':
    app.run(debug=True)