# vmanage_image_uploader

Script used to automate the process of uploading sdwan devices images to vManage for the software upgrade process


## Install instructions

Open your terminal or git-bash and clone the repository

    git clone git@www-github.cisco.com:rgomezbe/vmanage_image_uploader.git

Move to the repository folder

    cd vmanage_image_uploader

Use pip to install the requirements file with the required python external modules

    pip install -r requirements.txt

Download all the images you want to upload from software.cisco.com

    https://software.cisco.com/


## Base parameters

Script support cli arguments to provide vmanage credentials and work directory directly from execution

Integrated help is available to verify the use of the arguments

    python uploader.py -h

Output:

    ➜ python uploader.py -h
    usage: uploader.py [-h] [--add ADD] [--port PORT] [--user USER] [--pwd PWD] [--dir DIR]
    
    Use arguments to provide the required vManage info

    optional arguments:
    -h, --help   show this help message and exit
    --add ADD    IP or Hostname of the vmanage
    --port PORT  vmanage port for HTTPs 443 or 8433 commonly
    --user USER  vmanage username with API access
    --pwd PWD    password for the given vmanage username
    --dir DIR    Full path for local directory where the images are stored

    Ex. python uploader.py --add 198.18.1.10 --port 443 --user admin --pwd C1sco12345 --dir C:\Users\demouser\Downloads

In case any of the required arguments is missed, user will be prompted to provide the info on the terminal

    ➜ python uploader.py
    vManage address: 198.18.10.1
    vManage port: 443
    username: admin
    password: 
    image directory: C:\\Users\\demouser\\Downloads

## Execute script

Execute uploader.py file to run the script

Ex 1. (Running the script from jump host at dcloud session: Cisco Secure SD-WAN 20.6.2 - 17.6.2 (Viptela) Single DC v1)

    python uploader.py --add 198.18.1.10 --port 443 --user admin --pwd C1sco12345 --dir C:\\Users\\demouser\\Downloads

Ex 2. (Running the script locally)

    python uploader.py --add my_vmanage.cisco.com --port 8443 --user rgomezbe --pwd cisco123 --dir /Users/rgomezbe/Downloads

Output:

    ➜ python uploader.py --add 198.18.1.10 --port 443 --user admin --pwd C1sco12345 --dir C:\Users\demouser\Downloads
    Images found: ['viptela-20.6.3-x86_64.tar.gz', 'viptela-20.7.2-x86_64.tar.gz', 'viptela-20.8.1-x86_64.tar.gz']
    Uploading viptela-20.6.3-x86_64.tar.gz - 166437 KB
    viptela-20.6.3-x86_64.tar.gz upload finished
    Uploading viptela-20.7.2-x86_64.tar.gz - 167662 KB
    viptela-20.7.2-x86_64.tar.gz upload finished
    Uploading viptela-20.8.1-x86_64.tar.gz - 175852 KB
    viptela-20.8.1-x86_64.tar.gz upload finished
    Session closed!

## Author

For any support or comments please reach out to the author Raul Gomez

    rgomezbe@cisco.com
