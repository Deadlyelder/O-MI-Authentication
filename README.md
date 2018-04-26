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






















