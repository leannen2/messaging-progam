# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Leanne Nguyen and Yash Chordia
# leannen2@uci.edu and ychordia@uci.edu
# 26766612 and 20485372

import socket
from NaClProfile import MessengerProfile
import ds_protocol as dsp

# HOST = '127.0.0.1'
# PORT = 2020

HOST = '168.235.86.101'
PORT = 3021

# Sends the join message to the server and returns the token received from the server if the user successfully joins the server, Returns False if the joining was unsuccessful
def join(client, user, pwd, user_pub_key):
    join_msg = dsp.gen_join_message(user, pwd, user_pub_key)

    client.sendall(join_msg.encode('utf-8'))
    srv_msg = client.recv(4096)
    decoded_msg = srv_msg.decode('utf-8')
    recv_json = dsp.extract_json(decoded_msg)
    print('recv_json: ',recv_json)
    if recv_json.type == 'ok':
        print('join successful')
        return recv_json.token
    elif recv_json.type == 'error':
        print(recv_json.message)
        return False

# Sends a message to the server to publish a post, Returns True if the publishing was successful and False if the publishing was unsuccessful
def send_message(client, message, serv_pub_key, na: MessengerProfile):
    encrypted_message = na.encrypt_entry(message, serv_pub_key)
    print('encrypted_message: ', encrypted_message)
    send_msg = dsp.gen_post_message(na.public_key, encrypted_message)
    client.sendall(send_msg.encode('utf-8'))
    srv_msg = client.recv(4096)
    decoded = srv_msg.decode('utf-8')
    recv_json = dsp.extract_json(decoded)
    if recv_json.type == 'ok':
        return True
    elif recv_json.type == 'error':
        print('json for sent message: ', recv_json)
        print(recv_json.message)
        return False

# Sends a message to the server to publish a bio, Returns True if the publishing was successful and False if the publishing was unsuccessful
def send_bio(client, bio, serv_pub_key, na: MessengerProfile):
    encrypted_bio = na.encrypt_entry(bio, serv_pub_key)
    print('encrypted_bio: ', encrypted_bio)
    bio_msg = dsp.gen_bio_message(na.public_key, encrypted_bio)
    client.sendall(bio_msg.encode('utf-8'))
    srv_msg = client.recv(4096)
    decoded = srv_msg.decode('utf-8')
    recv_json = dsp.extract_json(decoded)
    if recv_json.type == 'ok':
        return True
    elif recv_json.type == 'error':
        print(recv_json.message)
        return False

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    #TODO: return either True or False depending on results of required operation

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    
        try:
            client.settimeout(3)
            client.connect((HOST, PORT))
        except ConnectionRefusedError:
            print('connection refused')

        print(f"client connected to {HOST} on {PORT}")

        while True:
            na = MessengerProfile()
            na.generate_keypair()
            serv_pub_key = join(client, username, password, na.public_key)
            print('serv pub key:', serv_pub_key)
            if serv_pub_key is False:
                return False
            if message:
                if not send_message(client, message, serv_pub_key, na):
                    print('message not sent')
                    return False
                print('message sent successfully')
            if bio:
                if not send_bio(client, bio, serv_pub_key, na):
                    return False
            
            return True

if __name__ == "__main__":
    print(send(HOST, PORT, 'lean', 'thisisapwd', 'last post', 'bio yay!'))