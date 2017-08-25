# Polly auto Text-to-Speech API

### Introduction
This project is mainly built to solve the constraint of AWS Polly's limited character input that only allows no more than 1600 chars at a time. This project is an experiment for future integration of AWS service.

-----------

### Version 1.1 Updated on Aug 25th, 2017
Implement *POST Method* of transfering giving text to an audio file. This method will return an AWS S3 address that stores the audio file. Request's Content-type should be application/json and the body data format are given as follows.
```json
{
 "name":"example",
 "text":"The text you would like to transfer",
 "VoiceId":"Amy"
 }
```
The first two key is required while the last one "VoiceId" is optional. Default VoiceId will be "Russell". To see more VoiceId, see [Available Voices](http://docs.aws.amazon.com/polly/latest/dg/voicelist.html) or use command 
`<aws polly describe-voices>` after installing AWS Command Line Interface.

Example of request sent by curl
```
curl -H "Content-type: application/json" -X POST ec2-34-210-46-14.us-west-2.compute.amazonaws.com/audio -d '{"name":"audio1","text":"I want to have a test"}'
```

### Version 1.0
Implemente *GET Method* to retrieve text from certain webpage submitted via url.(By default it is JLB website).
The instance's public DNS is ec2-34-210-46-14.us-west-2.compute.amazonaws.com

You can get corressponding audio's S3 address via ec2-34-210-46-14.us-west-2.compute.amazonaws.com/<blog_id>.

e.g.

ec2-34-210-46-14.us-west-2.compute.amazonaws.com/18 will return you the audio files of http://jlb.jhrnet.com/index.cfm/blog/18

---------

### Dependencies
This project depends on ffmpeg due to the use of *[pydub](https://getithub.com/jiaaro/pydub)*. WAV files can be saved with pure python. Other audio files may require ffmpeg to open. 

---------

### Setup
You will need an AWS account to use the "Polly" Text-to-Speech service provided by the AWS. You should obtain your own **aws_access_key_id** and **aws_secret_access_key** to replace the variables in the script(display as **YOUR_ACCESS_KEY_ID** and **YOUR_SECRET_ACCESS_KEY**). These two key can be obtained via the following process. If you run the script on your own ubuntu instance or whatever, you should change the return addess to your own public DNS as well.

AWS -> Move the cursor to My Account -> Security Credentials -> Access Keys (Access Key ID and Secret Access Key)


After setup the server properly
```
sudo apt-get install ffmpeg
sudo pip3 install requirements.txt
```
to install all the packages needed.

Using **Flask** framework, a **Apache2** framework is recommended to setup the script. **mod-wsgi** module is also needed, while it is enabled as default. 
For Apache2 runs the scripts with another user, **www-data** should obtain the read/write authorization.
``` bash
chmod -R 777 /var/www/
```
is not recommended but useful.

--------------

### Steps to setup apache2 mod-wsgi

#### Step 1: Install Apache2 and mod-wsgi
```Linux Kernel Module
$ sudo apt-get update
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-wsgi python3-dev
$ sudo apt-get install libapache2-mod-wsgi-py3
```
To enable the module
```Linux Kernel Module
$ sudo a2enmod wsgi
```

#### Step 2: Create the App
direct to /var/www with
```Linux Kernel Module
$ cd /var/www
$ sudo mkdir FlaskApp
$ cd FlaskApp
$ sudo mkdir FlaskApp
$ cd FlaskApp
$ sudo mkdir static templates
```
The Application Stored in the inside FlaskApp, while the first FlaskApp stands for all the App with Flask. You can put future flask App packages inside /var/www/FlaskApp along with the /var/www/FlaskApp/FlaskApp

```Linux Kernel Module
$ sudo nano __init__.py
```
to create the index file and append the following code to the file.
```python
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World"
if __name__ == "__main__":
    app.run(debug=True)
```

#### Step 3: Install Flask Framework
```Linux Kernel Module
$ sudo apt-get install python3-pip
```
(Optional)
```Linux Kernel Module
$ sudo pip3 install virtualenv
```
You can use virtualenv to create a independent environment for running each Application instead of installing all kinds of packages together.

```Linux Kernel Module
$ sudo pip install Flask
```
it should be able to run.

#### Step 4: Configure and Enable Virtual Host
```Linux Kernel Module
$ sudo nano /etc/apache2/sites-available/FlaskApp.conf
```
add following code to the file and save
```
<VirtualHost *:80>
		ServerName mywebsite.com
		ServerAdmin admin@mywebsite.com
		WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
		<Directory /var/www/FlaskApp/FlaskApp/>
			Require all granted
		</Directory>
		Alias /static /var/www/FlaskApp/FlaskApp/static
		<Directory /var/www/FlaskApp/FlaskApp/static/>
			Require all granted
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
Every time you add an Application Package to the folder, you should adjust this config file accordingly.
```Linux Kernel Module
$ sudo a2ensite FlaskApp
$ cd /var/www/FlaskApp
$ sudo nano flaskapp.wsgi
```
Add the following code to the flaskapp.wsgi file stated in the above file.
```python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = 'Add your secret key'
```

#### Step 5: Restart Apache
```Linux Kernel Module
sudo service apache2 restart 
```
Then it is accessible via public DNS.

#### FYI:
to debug
```Linux Kernel Module
$ nano /var/log/apache2/error.log
```
The log is sorted by time asc.

-------------

### Reference
[Flask Doc 0.12](http://flask.pocoo.org/docs/0.12/)

[How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
