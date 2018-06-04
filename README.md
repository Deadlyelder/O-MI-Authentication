OMI Project - Authentication module
===============================


Basic configuration
-------

1. Setup authentication settings in `omi_security/omi_security/settings.py`
2. In O-MI Node `/etc/o-mi-node/application.conf`, inside `omi-service` object:
```
authAPI.v2 {
  enable = true

  # Url to do authentication (checking if the consumer have valid credentials or session)
  authentication-url = "http://localhost:8000/omi_authquery"

  # Url to do authorization (checking what data a given user has permissions to read or write)
  authorization-url = "<put authorization module url here>"
}
```


Running
-------

1. Install python and pip: `sudo apt-get install python3 python3-pip`
1. Install dependencies: `pip3 install -r requirements.txt`
2. Run: `python3 omi_security/manage.py runserver 0:8000`



To configure NGINX as proxy, use the following method
------------------------------------------------


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



To install and configure Openldap and phpldapadmin , use the following method
-----------------------------------------------------------------


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










