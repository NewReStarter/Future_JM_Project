
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"

import requests
from bs4 import BeautifulSoup
@app.route('/text/<int:blog_id>',methods=['GET'])
def webtext(blog_id):
	url = 'http://jlb.jhrnet.com/index.cfm/blog/'+str(blog_id)
	page = requests.get(url)
	soup = BeautifulSoup(page.content,'html.parser')
	content = ''
	for item in soup.find_all('p'):
		content+=item.text
	return content

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
from pydub import AudioSegment
@app.route('/audio/<int:blog_id>', methods=['GET'])
def get_audio(blog_id):
	#check is file exists
	path = '/var/www/FlaskApp/FlaskApp/' + str(blog_id) + '.mp3'
	if(os.path.exists(path)):
		return 'https://s3-us-west-2.amazonaws.com/speechsoundstorage/mp3/' + str(blog_id) + '.mp3'
	url = 'http://jlb.jhrnet.com/index.cfm/blog/'+str(blog_id)
	#grasp text from JLB
	page = requests.get(url)
	soup = BeautifulSoup(page.content,'html.parser')
	content = []
	for item in soup.find_all('p'):
		content.append(item.text)
	
	playlist = []
	#create a polly client to do transfer
	polly = boto3.client('polly', region_name='us-west-2',
		aws_access_key_id= YOUR_ACCESS_KEY_ID,
		aws_secret_access_key= YOUR_SECRET_ACCESS_KEY)
	
	length = len(content)
	count = 1
	 #transfer and store each segment in a list
	for item in content:
		tmp = ''
		tmp+=item
		try:
			response = polly.synthesize_speech(Text=item, OutputFormat="mp3",VoiceId="Russell")
		except(BotoCoreError, ClientError) as Error:
			print(Error)
			sys.exit(-1)
		if 'AudioStream' in response:
			with closing(response["AudioStream"]) as stream:
				file_name = 'speech' + str(blog_id) +str(count) + '.mp3'
				#output = os.path.join(os.getcwd(),file_name)
				output = '/var/www/FlaskApp/FlaskApp/'+file_name
				with open(output, "wb+") as file:
					file.write(stream.read())
				playlist.append(AudioSegment.from_mp3(('/var/www/FlaskApp/FlaskApp/'+file_name)))
				count+=1

	for i in range(len(playlist)):
		if i == 0:
			song = playlist[i]
		else:
			song += playlist[i]
	#export		
	file_name=str(blog_id)+'.mp3'
	song.export(path,format='mp3')

	#create a s3 object ot conduct operation
	s3 = boto3.resource('s3',region_name='us-west-2',
		aws_access_key_id= YOUR_ACCESS_KEY_ID,
		aws_secret_access_key= YOUR_SECRET_ACCESS_KEY)
	output = 'mp3/'+str(blog_id)+'.mp3'
	s3.meta.client.upload_file(path, 'speechsoundstorage', output)
	fileObj = s3.ObjectAcl('speechsoundstorage',output)
	message = fileObj.put(ACL='public-read')
	
	#delete all tmp file
	for i in range(1,count):
		dele_path='/var/www/FlaskApp/FlaskApp/speech'+str(blog_id)+str(i)+'.mp3'
		os.remove(dele_path)
	
	return 'https://s3-us-west-2.amazonaws.com/speechsoundstorage/mp3/' + str(blog_id) + '.mp3'

from flask import json, request
@app.route('/audio', methods=['POST'])
def get_certain_audio():
	#get pure json data without header
	data = request.get_json(force=True)
	
	#retrive data from json
	name = data['name']
	string = data['text']
	Voice = data.get('VoiceId','Russell') #default is Russell
	
	#file preparation
	file_name = '/var/www/FlaskApp/FlaskApp/'+name+'.mp3'
	path = '/var/www/FlaskApp/FlaskApp/'
	playlist = []
	wordlist = string.split()

	polly = boto3.client('polly', region_name='us-west-2',
		aws_access_key_id= YOUR_ACCESS_KEY_ID,
		aws_secret_access_key= YOUR_SECRET_ACCESS_KEY)
	#voice transfer
	count = 1
	word_num = 0
	tmp_str = ''
	for word in wordlist:
		tmp_str+=word
		word_num += 1
		if (len(tmp_str) > 1450) or (word_num == len(wordlist)):
			try:
				response = polly.synthesize_speech(Text=tmp_str, OutputFormat="mp3",VoiceId=Voice)
				tmp_str = ''
			except(BotoCoreError, ClientError) as Error:
				print(Error)
				sys.exit(-1)
			if 'AudioStream' in response:
				with closing(response["AudioStream"]) as stream:
					tmp_file = 'audio' + str(count) + '.mp3'
					#output = os.path.join(os.getcwd(),file_name)
					output = path+tmp_file
					with open(output, "wb+") as file:
						file.write(stream.read())
					playlist.append(AudioSegment.from_mp3(('/var/www/FlaskApp/FlaskApp/'+tmp_file)))
					count+=1	

	for i in range(len(playlist)):
		if i == 0:
			music = playlist[i]
		else:
			music += playlist[i]
	music.export(file_name,format='mp3')

	#upload and then delete local file
	s3 = boto3.resource('s3',region_name='us-west-2',
		aws_access_key_id= YOUR_ACCESS_KEY_ID,
		aws_secret_access_key= YOUR_SECRET_ACCESS_KEY)
	output = 'mp3/'+name+'.mp3'
	s3.meta.client.upload_file(file_name, 'speechsoundstorage', output)
	fileObj = s3.ObjectAcl('speechsoundstorage',output)
	message = fileObj.put(ACL='public-read')
	#delete local file before finish
	for i in range(1,count):
		dele_path='/var/www/FlaskApp/FlaskApp/audio'+str(i)+'.mp3'
		os.remove(dele_path)
	if os.path.exists(file_name):
		os.remove(file_name)

	return 'https://s3-us-west-2.amazonaws.com/speechsoundstorage/mp3/' + name + '.mp3'

if __name__ == "__main__":
    app.run(debug=True)
