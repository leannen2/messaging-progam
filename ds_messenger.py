import ds_protocol as dsp
import socket

HOST = '168.235.86.101'
PORT = 3021

class DirectMessage(dict):
    def __init__(self, recipient=None, message=None, timestamp=None, sender=None):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp
        self.sender = sender

        dict.__init__(self, recipient=self.recipient, message=self.message, timestamp=self.timestamp, sender=self.sender)

class DirectMessenger():
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = self._get_pub_serv_key()
            
    def send(self, message:str, recipient:str) -> bool:
        # returns true if message successfully sent, false if send failed.
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
        response_json = self._send_to_server(new_message)
        response_type = dsp.extract_response_type(response_json)
        messages = []
        if response_type == 'ok':
            for message in response_json['response']['messages']:
                message_object = DirectMessage('me', message['message'], message['timestamp'], message['from'])
                messages.append(message_object)
        
        return messages


    
    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages
        new_message = dsp.gen_all_messages(self.token)
        response_json = self._send_to_server(new_message)
        response_type = dsp.extract_response_type(response_json)
        messages = []
        if response_type == 'ok':
            for message in response_json['response']['messages']:
                message_object = DirectMessage('me', message['message'], message['timestamp'], message['from'])
                messages.append(message_object)
        
        return messages
    
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
    messenger = DirectMessenger(HOST, 'MARK', 'thisisapwd')
    msgs = messenger.send('ltest3', 'markLeanneYash')
    msg = DirectMessenger(HOST, 'markLeanneYash', 'thisisapwd')
    # msgs = msg.retrieve_new()
    # print(msgs)
    # new = messenger.retrieve_new()
    # for message in new:
    #     print(message.message, message.recipient, message.timestamp)
    # messages = messenger.retrieve_all()
    # for message in messages:
    #     print(message.message, message.recipient, message.timestamp, message.sender)
    # print(messages)
