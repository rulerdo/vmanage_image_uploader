import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from time import time
import os
from argparse import ArgumentParser

class sdwan_manager():


    def __init__(self,server,port,username,password,image_dir):

        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.image_dir = image_dir
        self.host = server + ':' + port
        self.cookie = self.get_auth_cookie()
        self.token = self.get_auth_token()
        self.image_list = self.get_images_from_folder()


    def get_auth_cookie(self):

        url = f"https://{self.host}/j_security_check"

        payload = f'j_username={self.username}&j_password={self.password}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        cookie = response.cookies.get_dict()['JSESSIONID']

        return cookie


    def get_auth_token(self):

        url = f"https://{self.server}/dataservice/client/token"

        payload={}
        headers = {
        'Cookie': f'JSESSIONID={self.cookie}'
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        token = response.text

        return token


    def upload_image(self,image):

        upload_url = f"https://{self.host}/dataservice/device/action/software/package"

        headers = {
        'X-XSRF-TOKEN': self.token,
        'Cookie': f'JSESSIONID={self.cookie}',
        }

        try:

            upload_file = {'name': open(f"{self.image_dir}\\{image}", "rb")}
            size = int(os.stat(f"{self.image_dir}\\{image}").st_size / 1024)
            print(f"Uploading {image} - {size} KB")

            response = requests.request("POST", url=upload_url, headers=headers, files=upload_file, verify=False)

            if response.status_code == 200:
                print(f"{image} upload finished")


            else:
                print("Status code received: ", response.status_code)
                print(response.text)     

        
        except FileNotFoundError:

                print("File Not Found")

        except Exception as e:

                print("Problems during upload process")
                print(e)


    def logout(self):

        url = f"https://{self.host}/logout?nocache={str(int(time()))}"

        payload={}

        headers = {
        'Cookie': f'JSESSIONID={self.cookie}',
        }

        response = requests.request("GET", url, headers=headers, data=payload, verify=False)

        message = 'Session closed!' if response.status_code == 200 else 'Problems closing session'
        print(message)


    def get_images_from_folder(self):

        try:
            acceptable_extensions = ('bin', 'tar', 'gz')
            dir_list = os.listdir(self.image_dir)
            image_list = [file for file in dir_list if file.endswith(acceptable_extensions)]

        except FileNotFoundError as e:
            image_list = list()

        return image_list


def get_arguments():

    help_description = '''
    Default vManage credentials and image folder work for dcloud session:
    Cisco Secure SD-WAN 20.6.2 - 17.6.2 (Viptela) Single DC v1 ///
    addr = '198.18.1.10'
    port = '443'
    user = 'admin'
    pwd = 'C1sco12345'
    dir = 'C:\\Users\\demouser\\Downloads' ///
    Use the available arguments if you need to overwrite them
    '''
    parser = ArgumentParser(description=help_description)
    parser.add_argument('--add', default='198.18.1.10', help='IP or Hostname of the vmanage')
    parser.add_argument('--port', default='443', help='vmanage port for HTTPs 443 or 8433 commonly')
    parser.add_argument('--user', default='admin', help='vmanage username with API access')
    parser.add_argument('--pwd', default='C1sco12345', help='password for the given vmanage username')
    parser.add_argument('--dir', default='C:\\Users\\demouser\\Downloads', help='Full path for local directory where the images are stored')
    arguments = parser.parse_args()

    return arguments


if __name__ == '__main__':

    args = get_arguments()

    address = args.add
    port = args.port
    username = args.user
    password = args.pwd
    image_dir = args.dir

    session = sdwan_manager(address,port,username,password,image_dir)

    if len(session.image_list) < 1:
        print('No valid images found on:',image_dir)
    
    else:
        print('Images found:',session.image_list)
        for image in session.image_list:
            session.upload_image(image)
    
    session.logout()
