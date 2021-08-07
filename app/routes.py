from app import app
from flask import request, render_template, redirect
import json
import calendar
import time
import os
import translators as ts
import json
from textblob import TextBlob

@app.route('/')
def root():
	
	
	files_data = []
	if os.path.isfile('./data.csv'):
		with open('data.csv', 'r') as file:
			lines = file.readlines()
			for line in lines:
				files_data.append(line)

	print(files_data)
	return render_template('index.html', files = files_data)

@app.route('/translate', methods=['POST'])
def translate():
	text = request.files['untranslated']
	text.save('./untranslated/'+ text.filename)
	def tb(strg):
		lang = TextBlob(strg)
		detected_lang=lang.detect_language()
		return detected_lang

	with open('./untranslated/'+ text.filename, encoding='utf-8') as file:
		utext = file.read()
		language = tb(utext)
		with open('./translated/'+ text.filename, 'w', encoding='utf-8') as new_file:
			with open('data.csv', 'a') as file:
				file.write(f'{text.filename},{language}, ,{"./untranslated/"+ text.filename},{text.filename}\n')
			# db.insert_one({
			# 		'name' : text.filename,
			# 		'lang' : language,
			# 		'summary' : '',
			# 		'ref' : './untranslated/'+ text.filename,
			# 		'ref_name' : text.filename
			# 	})
			try:
				new_file.write(ts.google(utext, from_language = language, to_language='en'))
			except:
				return 'Error'
	return redirect('/')


@app.route('/view/<filename>')
def view(filename):
	text = ''
	ref_text = ''
	file_data = ''
	with open('data.csv', 'r') as file:
		lines = file.readlines()
		for line in lines:
			if line.split(',')[0] == filename:
				file_data = line
	# file_data = db.find_one({'name': filename})
	print(file_data)
	with open('./translated/'+filename, 'r') as file:
		text = file.read().split('\n')
	with open(file_data.split(',')[3] , 'r', encoding='utf8') as file:
		ref_text = file.read().split('\n')
	return render_template('view.html', data= file_data, body=text, ref_body=ref_text)

@app.route('/edit/<filename>')
def edit(filename):
	
	file_data = ''
	with open('data.csv', 'r') as file:
		lines = file.readlines()
		for line in lines:
			if line.split(',')[0] == filename:
				file_data = line
	ref_text = ''
	text = ''
	with open(file_data.split(',')[3] , 'r', encoding='utf8') as file:
		ref_text = file.read().split('\n')
	with open('./translated/'+filename, 'r') as file:
		text = file.read()
	return render_template('edit.html', data=file_data,  body=text, ref_body=ref_text)


@app.route('/save-edit', methods=['POST'])
def save_edit():
	with open('data.csv', 'a') as file:
		file.write(f"{'new_' + request.form['file']},{request.form['lang']},{request.form['summary']},{'./translated/'+request.form['file']},{request.form['file']}\n")
			
	# db.insert_one({
	# 				'name' : 'new_' + request.form['file'],
	# 				'lang' : request.form['lang'],
	# 				'summary' : request.form['summary'],
	# 				'ref' : './translated/'+request.form['file'],
	# 				'ref_name': request.form['file']
	# 			})
	with open('./translated/new_'+request.form['file'], 'w') as file:
		file.write(request.form['body'])
		file.flush()
	return redirect('/')

@app.route('/delete/<filename>')
def delete(filename):
	# db.delete_one({'name' : filename})
	os.remove('./translated/'+filename)
	if os.path.isfile('./untranslated/'+filename):
		os.remove('./untranslated/'+filename)
	return redirect('/')

# @app.route('/search', methods=['POST'])
# def search():
# 	keyword = request.form['search'].lower()
# 	files_data = []
# 	for data in db.find():
# 		if (data['name'].lower().find(keyword) != -1):
# 			files_data.append(data)
# 		with open('./translated/'+ data['name'],  'r') as file:
# 			text = file.read().lower().split(' ')
# 			if keyword in text:
# 				files_data.append(data)
# 	return render_template('index.html', files = files_data, search=keyword)
