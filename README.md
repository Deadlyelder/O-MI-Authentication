OMI Project - Security Module
-----------------------------

### To install pycharm, use the following method

To install pycharm, use the following commands:

```
$ sudo add-apt-repository ppa:mystic-mirage/pycharm
$ sudo apt update
$ sudo apt install pycharm-community
```


### Setup Process for owner

Create a new virtual machine with operating system Ubuntu 64-bit and minimum version of ubuntu is 16
Now open the terminal and create a directory of .ssh and go inside that directory

```
$ mkdir .ssh
$ cd .ssh
```

Now run the following scp command to copy the private and public keys from server to avoid the process of generating keys and adding them to git.
Provide the password for your account of saeeda2

```
.ssh$ scp saeeda2@kosh.aalto.fi:/u/92/saeeda2/unix/sshkeys/* .
```

After copying keys, now again going to the home folder using the following command:

```
.ssh$ cd
```

Now install git using the following command:

```
$ sudo apt-get install git
```

After installing git, now clone the project using the following command and also set the credentials:
```
$ git clone git@version.aalto.fi:saeeda2/OMI_Security_Module.git
$ git config --global user.email "aisha.saeed@aalto.fi"
$ git config --global user.name "Aisha Saeed"
```

Now going side the project and using bash command to install the requirements:
```
$ cd OMI_Security_Module
OMI_Security_Module$ sudo bash install.sh
```

Now going inside the project and running the django server on port 8000.
This world help to configure nginx as proxy and run nginx on port 80.
```
OMI_Security_Module$ cd omi_security
OMI_Security_Module/omi_security$ sudo python3 manage.py runserver 0:8000
```


### To configure NGINX as proxy, use the following method

Install nginx using the following command:

```
$ sudo apt-get install nginx
```
Now go to the following folder and edit the default file

```
$ cd /etc/nginx/sites-enabled
/etc/nginx/sites-enabled$ sudo nano default
```

In the default file: comment out the following lines
```
#root /var/www/html;

# Add index.php to the list if you are using PHP
#index index.html index.htm index.nginx-debian.html;

location / {
    # First attempt to serve request as file, then
    # as directory, then fall back to displaying a 404.
    #try_files $uri $uri/ =404;

```
Inside the location / {   add the following code and save the file
```
proxy_set_header        Host $host;
proxy_set_header        X-Real-IP $remote_addr;
proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header        X-Forwarded-Proto $scheme;
proxy_pass              http://127.0.0.1:8000$request_uri;
proxy_read_timeout  90;

```

Now restart nginx using following command:
```
$ sudo service nginx reload
```
Now you can access the front page of django using 127.0.0.1
Django server should be running on 127.0.0.1:8000

















