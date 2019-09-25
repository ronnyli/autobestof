import base64
import dotenv
import os
import requests

dotenv.load_dotenv('./.env')
WP_USER = os.getenv('REDDIT_USER')
WP_PASS = os.getenv('WP_PASS')
WP_ENDPOINT = 'https://thredd.io/wp-json/wp/v2'

token = base64.standard_b64encode(bytes(WP_USER + ':' + WP_PASS, 'utf-8'))
headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

def create_post(post):
    r = requests.post(WP_ENDPOINT + '/posts', headers=headers, json=post)
    return r

def get_posts():
    r = requests.get(WP_ENDPOINT + '/posts')
    return r.json()
