# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Leanne Nguyen and Yash Chordia
# leannen2@uci.edu and ychordia@uci.edu
# 26766612 and 20485372

import json, Profile, time
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])

# Extracts a json string into a dictionary
def extract_json(json_msg:str) -> DataTuple:
    try:
        json_obj = json.loads(json_msg)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    return json_obj

def extract_response_type(response_dict: dict) -> str:
    return response_dict['response']['type']

# returns the messages from the response dictionary in a list
def extract_messages(response_dict: dict) -> list:
    if response_dict['response']['type'] == 'ok':
        messages = response_dict['response']['messages']
        return messages
    else:
        print('No messages to extract.')
        return False

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
    all_dict = {"token": client_pub_key, "directmessage": "all"}
    message = json.dumps(all_dict)
    return message

if __name__ == "__main__":
    print(gen_post_message('user_token', 'hello world'))
    print(gen_bio_message('server_token', 'helloooo'))
    print(gen_join_message('leanne', 'pwd', 'my_pub_key'))