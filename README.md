OMI Project - Security Module
-----------------------------


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

Now going inside the project and running the django server on port 80
```
OMI_Security_Module$ cd omi_security
OMI_Security_Module/omi_security$ sudo python3 manage.py runserver 0:80
```

### To install pycharm, use the following method

To install pycharm, use the following commands:

```
$ sudo add-apt-repository ppa:mystic-mirage/pycharm
$ sudo apt update
$ sudo apt install pycharm-community
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

### To install and configure Openldap and phpldapadmin , use the following method

Installing ldap server (enter root password at administrator password)
```
sudo apt-get install slapd ldap-utils
```

After installation, go to this file:
```
sudo gedit /etc/ldap/ldap.conf
```

Change only these lines as:
```
BASE	dc=ldap,dc=com
URI	ldap://localhost:389
```

Reconfigure slapd
```
sudo dpkg-reconfigure slapd
```

And make the following choices:
```
select "NO" to Omit Openldap server configuration
set domain name as: ldap.com
organization name to : ldap.com
enter root password at administrator password
select default MDB
select NO when asked "Remove the database when slapd is purged"
select YES for move old database
select NO to allow ldapv2 protocol
```
To test openldap on commandline
```
sudo ldapsearch -x
```

Install  phpLDAPadmin package
```
sudo apt-get install phpldapadmin
```

Open the main configuration file
```
sudo gedit /etc/phpldapadmin/config.php
```

In config.php file, change the lines as:
```
$servers->setValue('server','host','enter host IP address here');
$servers->setValue('server','base',array('dc=ldap,dc=com'));
$servers->setValue('login','bind_id','cn=admin,dc=ldap,dc=com');
```
In config.php file, uncomment the following line and make it true:
```
$config->custom->appearance['hide_template_warning'] = true;
```

Start apache2 service:
```
sudo service apache2 start
```
phpldapadmin can be accessed as http://host/phpldapadmin/.
Follow this link: https://www.techrepublic.com/article/how-to-populate-an-ldap-server-with-users-and-groups-via-phpldapadmin/.
Create Organizational units ("groups" and "users"). Under "groups" create two posix groups "normal-users" and "superuser". Under "users" create generic user accounts,
for example, I made 3 users (Hassaan, Maria and Ruman). Hassaan will be superuser so I added his memberUid in superuser group and other two users in normal-users
group.
In order to add email addresses, go to each user profile, select "Add new attribute" and add email from there. Another method is to do on command line as follows:
```
sudo ldapmodify -H ldap://localhost:389 -D cn=admin,dc=ldap,dc=com -x -W
Enter LDAP Password:
dn: cn=Ruman Khan,ou=users,dc=ldap,dc=com
changetype: modify
add: mail
mail: ruman@aalto.fi
 ```

Now for integrating with django, install the following:
```
sudo apt-get install -y libldap2-dev
sudo apt-get install -y python-dev
sudo apt-get install -y libsasl2-dev
sudo apt-get install -y python-pip
sudo pip3 install python-ldap
sudo pip3 install django-auth-ldap
```
Apache2 is using port 80. Run OMI security module using following command:
```
python3 manage.py runserver 0:8000
```
When you enter username and password of the user from Openldap directory,
the user will be logged in and is added into the User table of Django (if not already exists).










