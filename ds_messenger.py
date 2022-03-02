import ds_protocol as dsp
import socket
from NaClProfile import NaClProfile

HOST = '168.235.86.101'
PORT = 3021

class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        # self.na = NaClProfile()
        # self.na.generate_keypair()
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = self._get_pub_serv_key()
            
    def send(self, message:str, recipient:str) -> bool:
        # returns true if message successfully sent, false if send failed.
        # encrypted_message = self.na.encrypt_entry(message, self.token)
        # print('encrypted_message: ', encrypted_message)
        direct_message = dsp.gen_direct_message(self.token, message,recipient)
        response_json = self._send_to_server(direct_message)
        response_type = dsp.extract_response_type(response_json)
        if response_type == 'ok':
            return True
        else:
            return False
            
    def retrieve_new(self) -> list:
        # returns a list of DirectMessage objects containing all new messages
        new_message = dsp.gen_get_unread_message(self.token)

    
    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages
        pass
    
    # Sends the join message to the server and returns the token received from the server if the user successfully joins the server, Returns False if the joining was unsuccessful
    def _join(self, client, user, pwd):
        join_msg = dsp.gen_join_message(user, pwd, '')

        client.sendall(join_msg.encode('utf-8'))
        srv_msg = client.recv(4096)
        decoded_msg = srv_msg.decode('utf-8')
        recv_json = dsp.extract_json(decoded_msg)
        if dsp.extract_response_type(recv_json) == 'ok':
            return recv_json['response']['token']
        elif recv_json.type == 'error':
            print(recv_json.message)
            return False

    def _send_to_server(self, message: str):
        # Connects to server, sends message, returns response from server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    
            try:
                client.settimeout(3)
                client.connect((self.dsuserver, PORT))
            except ConnectionRefusedError:
                print('connection refused')

            while True:
                self.token = self._join(client, self.username, self.password)
                if self.token is False:
                    print('connection to server unsuccessful')
                    return
                client.sendall(message.encode('utf-8'))
                srv_msg = client.recv(4096)
                decoded = srv_msg.decode('utf-8')
                recv_json = dsp.extract_json(decoded)
                print(recv_json)
                return recv_json
        
    def _get_pub_serv_key(self):
        # returns the server's public key 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    
            try:
                client.settimeout(3)
                client.connect((self.dsuserver, PORT))
            except ConnectionRefusedError:
                print('connection refused')

            token = self._join(client, self.username, self.password)
            if token is False:
                print('connection to server unsuccessful')
            return token

if __name__ == '__main__':
    messenger = DirectMessenger(HOST, 'lean', 'thisisapwd')
    print('token:',messenger.token)
    print()
    messenger.send('hi', 'lean')
