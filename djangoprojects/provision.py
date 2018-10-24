"""Greeter.

    Usage:
      provision.py create <name>
      provision.py list <name>
      provision.py delete <name>
      provision.py (-h | --help)

    Options:
      -h --help     Show this screen.

"""
import sshpubkeys
import time
import requests
import environ
from docopt import docopt

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

environ.Env.read_env()

API_TOKEN = env('API_KEY')
API_URL_BASE = 'https://api.digitalocean.com/v2/'
HEADERS = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(API_TOKEN)}

with open(env('SSH_KEY_PATH'), 'r') as f:
    ssh_key = f.readline()
fingerprint = sshpubkeys.SSHKey(ssh_key)


def list(droplet_name):
    api_droplet = API_URL_BASE + 'droplets?tag_name=' + droplet_name
    response = requests.get(api_droplet, headers=HEADERS)
    jsondata = response.json()
    droplets = jsondata['droplets']
    if not len(droplets) == 0:
        if droplet_name == droplets[0]['tags'][0] and response.status_code == 200 :
            print(response.content.decode('utf-8'))
        else:
            print("FAILED TO GET RESPONSE")
    else:
        print("DROPLET DOESN'T EXIST")


def create(droplet_name):
    data = {
             "name": droplet_name,
             "region": "nyc3",
             "size": "s-1vcpu-1gb",
             "image": "ubuntu-16-04-x64",
             "ssh_keys": [fingerprint.hash_md5().replace("MD5:", "")],
             "backups": False,
             "ipv6": True,
             "user_data": None,
             "private_networking": None,
             "volumes": None,
             "tags": [
                   "name:"+droplet_name
                 ]
            }
    api_url = '{0}droplets'.format(API_URL_BASE)
    response = requests.post(api_url, headers=HEADERS, json=data)
    jsondata = response.json()
    droplet = jsondata['droplet']
    while True:
        time.sleep(20)
        response_status = droplet['status']
        if response_status == 'new':
            print("SUCCESSFULLY CREATED")
            break
        else:
            print("FAILED TO CREATE")


def delete(droplet_name):
    api_droplet = API_URL_BASE + 'droplets?tag_name=' + droplet_name
    get_response = requests.get(api_droplet, headers=HEADERS)
    jsondata = get_response.json()
    droplets = jsondata['droplets']
    if not len(droplets) == 0:
        if droplet_name == droplets[0]['tags'][0]:
            response = requests.delete(api_droplet, headers=HEADERS)
            if response.status_code == 204:
                print("DELETED SUCCESSFULLY")
            else:
                print("FAILED TO GET DELETE")
    else:
        print("DROPLET DOESN'T EXIST")


if __name__ == "__main__":
    arguments = docopt(__doc__)
    if arguments['create']:
        create(arguments['<name>'])
    elif arguments['list']:
        list(arguments['<name>'])
    elif arguments['delete']:
        delete(arguments['<name>'])