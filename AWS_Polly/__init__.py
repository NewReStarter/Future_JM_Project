
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
	path = '/var/www/FlaskApp/FlaskApp/' + str(blog_id) + '.mp3'
	if(os.path.exists(path)):
		return 'https://s3-us-west-2.amazonaws.com/speechsoundstorage/mp3/' + str(blog_id) + '.mp3'
	url = 'http://jlb.jhrnet.com/index.cfm/blog/'+str(blog_id)
	page = requests.get(url)
	soup = BeautifulSoup(page.content,'html.parser')
	content = []
	for item in soup.find_all('p'):
		content.append(item.text)
	playlist = []
	polly = boto3.client('polly', region_name='YOUR_REGION',
		aws_access_key_id='YOUR_AWS_ACCESS_KEY',
		aws_secret_access_key='YOUR_SECRET_ACCESS_KEY')
	length = len(content)
	count = 1
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
	file_name=str(blog_id)+'.mp3'
	song.export(path,format='mp3')
	for i in range(1,count):
		dele_path='/var/www/FlaskApp/FlaskApp/speech'+str(blog_id)+str(i)+'.mp3'
		os.remove(dele_path)
	s3 = boto3.resource('s3',region_name='YOUR_REGION',
		aws_access_key_id='YOUR_ACCESS_KEY',
		aws_secret_access_key='YOUR_SECRET_ACCESS_KEY')
	output = 'mp3/'+str(blog_id)+'.mp3'
	s3.meta.client.upload_file(path, 'speechsoundstorage', output)
	fileObj = s3.ObjectAcl('speechsoundstorage',output)
	message = fileObj.put(ACL='public-read')
	return 'https://s3-us-west-2.amazonaws.com/speechsoundstorage/mp3/' + str(blog_id) + '.mp3'
		

if __name__ == "__main__":
    app.run(debug=True)
