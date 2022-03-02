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
        self.token = None
            
    def send(self, message:str, recipient:str) -> bool:
        # returns true if message successfully sent, false if send failed.
        direct_message = dsp.gen_direct_message(self.token, message,recipient)
            
    def retrieve_new(self) -> list:
        # returns a list of DirectMessage objects containing all new messages
        pass
    
    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages
        pass
    
    # Sends the join message to the server and returns the token received from the server if the user successfully joins the server, Returns False if the joining was unsuccessful
    def _join(client, user, pwd, user_pub_key):
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

    def _send_to_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    
            try:
                client.settimeout(3)
                client.connect((self.dsuserver, PORT))
            except ConnectionRefusedError:
                print('connection refused')

            print(f"client connected to {HOST} on {PORT}")

            while True:
                na = NaClProfile()
                na.generate_keypair()
                serv_pub_key = self._join(client, self.username, self.password, na.public_key)
