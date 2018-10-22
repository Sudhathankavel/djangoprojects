"""Greeter.

    Usage:
      provision.py create <name>
      provision.py list <name>
      provision.py delete <name>
      provision.py (-h | --help)

    Options:
      -h --help     Show this screen.

"""
import json
import time
import requests
import environ
from docopt import docopt

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# reading .env file
environ.Env.read_env()

api_token = env('API_KEY')
api_url_base = 'https://api.digitalocean.com/v2/'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(api_token)}


def list(droplet_name):
    api_droplet = api_url_base + 'droplets?tag_name=' + droplet_name
    response = requests.get(api_droplet, headers=headers)
    jsondata = json.loads(response.text)
    try:
        if droplet_name == "Name:" + (jsondata.get("droplets")[0]).get("name") and response.status_code == 200 :
            print(response.content.decode('utf-8'))
        else:
            print("FAILED TO GET RESPONSE")
    except IndexError:
        print("DROPLET DOESNT EXIST")


def create(droplet_name):
    data = {
             "name": droplet_name,
             "region": "nyc3",
             "size": "s-1vcpu-1gb",
             "image": "ubuntu-16-04-x64",
             "ssh_keys": [23341984],
             "backups": False,
             "ipv6": True,
             "user_data": None,
             "private_networking": None,
             "volumes": None,
             "tags": [
                   "Name:"+droplet_name
                 ]
            }
    api_url = '{0}droplets'.format(api_url_base)
    response = requests.post(api_url, headers=headers, json=data)
    time.sleep(25)  # delays for 25 seconds
    if response.status_code == 202:
        print("SUCCESSFULLY CREATED")
        jsondata = json.loads(response.text)
        response_id = (jsondata.get("droplet")).get("id")
        response_status = (jsondata.get("droplet")).get("status")
        data = {'id': response_id, 'status': response_status}
    else:
        print("FAILED TO CREATE")
    return data


def delete(droplet_name):
    api_droplet = api_url_base + 'droplets?tag_name=' + droplet_name
    get_response = requests.get(api_droplet, headers=headers)
    jsondata = json.loads(get_response.text)
    try:
        if droplet_name == "Name:" + (jsondata.get("droplets")[0]).get("name"):
            response = requests.delete(api_droplet, headers=headers)
            if response.status_code == 204:
                print("DELETED SUCCESSFULLY")
            else:
                print("FAILED TO GET DELETE")
    except IndexError:
        print("DROPLET DOESNT EXIST")


if __name__ == "__main__":
    arguments = docopt(__doc__)
    if arguments['create']:
        create(arguments['<name>'])
    elif arguments['list']:
        list(arguments['<name>'])
    elif arguments['delete']:
        delete(arguments['<name>'])