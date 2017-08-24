# Polly auto transfer API

### Version 1.0
Fully implemented *GET Method* to retrieve text from certain webpage submitted via url.(By default it is JLB website).

### Dependencies
This project depends on ffmpeg due to the use of *[pydub](https://github.com/jiaaro/pydub)*. WAV files can be saved with pure python. Other audio files may require ffmpeg to open.

### Setup
Using **Flask** framework, a **Apache2** framework is recommended to setup the script. **mod-wsgi** module is also needed, while it is enabled as default. 
For Apache2 runs the scripts with another user, **www-data** should obtain the read/write authorization.
``` bash
chmod -R 777 /var/www/
```
is not recommended but useful.


