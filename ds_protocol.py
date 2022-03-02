# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Leanne Nguyen and Yash Chordia
# leannen2@uci.edu and ychordia@uci.edu
# 26766612 and 20485372

import json, Profile, time
from collections import namedtuple
from NaClProfile import NaClProfile

DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])

# Extracts a json string into a dictionary and then returns the values as a DataTuple
def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object
    '''
    try:
        json_obj = json.loads(json_msg)
            
        d_type = json_obj['response']['type']
        d_message = json_obj['response']['message']
        try:
            d_token = json_obj['response']['token']
        except:
            d_token = ''
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(d_type, d_message, d_token)

# Generates the join message to send to the server
def gen_join_message(username, password, client_pub_key):
    join_dict = {"join": {"username": username, "password": password, "token": client_pub_key}}
    json_string = json.dumps(join_dict)
    return json_string

# Generates a message that is sent to the server to publish a post
def gen_post_message(client_pub_key, encrypted_message):
    post_dict = {"token": client_pub_key, "post": {"entry": encrypted_message, "timestamp": time.time()}}
    message = json.dumps(post_dict)
    return message

# Generates a message that is sent to the server to publish a bio
def gen_bio_message(client_pub_key, bio):
    bio_dict = {"token":client_pub_key, "bio": {"entry": bio,"timestamp": time.time()}}
    message = json.dumps(bio_dict)
    return message

def gen_direct_message(client_pub_key, message, recipient_usr):
    message_dict = {"token": client_pub_key, "directmessage": {"entry": message, "recipient": recipient_usr, "timestamp": time.time()}}
    message = json.dumps(message_dict)
    return message

def gen_get_unread_message(client_pub_key):
    unread_dict = {"token": client_pub_key, "directmessage": "new"}
    message = json.dumps(unread_dict)
    return message

def gen_all_messages(client_pub_key):
    all_dict = {"token": client_pub_key, "directmessage": "new"}
    message = json.dumps(all_dict)
    return message

if __name__ == "__main__":
    print(gen_post_message('user_token', 'hello world'))
    print(gen_bio_message('server_token', 'helloooo'))
    print(gen_join_message('leanne', 'pwd', 'my_pub_key'))