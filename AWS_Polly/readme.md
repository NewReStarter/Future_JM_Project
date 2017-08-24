# Polly auto transfer API

### Version 1.0
Fully implemented *GET Method* to retrieve text from certain webpage submitted via url.(By default it is JLB website).
The instance's public DNS is ec2-34-210-46-14.us-west-2.compute.amazonaws.com
You can get corressponding audio's S3 address via ec2-34-210-46-14.us-west-2.compute.amazonaws.com/<blog_id>.
e.g.
ec2-34-210-46-14.us-west-2.compute.amazonaws.com/18 will return you the audio files of http://jlb.jhrnet.com/index.cfm/blog/18

### Dependencies
This project depends on ffmpeg due to the use of *[pydub](https://getithub.com/jiaaro/pydub)*. WAV files can be saved with pure python. Other audio files may require ffmpeg to open.

### Setup
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
#!/usr/bin/python
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

### Reference
[Flask Doc 0.12](http://flask.pocoo.org/docs/0.12/)

[How To Deploy a Flask Application on an Ubuntu VPS](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)
