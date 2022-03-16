# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin

HOST = '168.235.86.101'
PORT = 3021

# TODO: Install the pynacl library so that the following modules are available
# to your program.
import json, os
from pathlib import Path

# TODO: Import the Profile and Post classes
from Profile import Profile, DsuFileError, DsuProfileError
from ds_messenger import DirectMessage,DirectMessenger
# TODO: Import the NaClDSEncoder module
    
# TODO: Subclass the Profile class
class MessengerProfile(Profile):
    def __init__(self):
        super().__init__(username='markLeanneYash', password='thisisapwd')
        self.sent_msg = {}
        self.retrieved_msg = {}
        self.add_all_msg()

    def add_sent_msg(self, dir_msg: DirectMessage):
        """
        Appends sent messages as DirectMessage object into sent_msg attribute
        """
        if dir_msg.recipient not in self.retrieved_msg:
            self.retrieved_msg[dir_msg.recipient] = [dir_msg]
        self.retrieved_msg[dir_msg.recipient].append(dir_msg)

    def add_all_msg(self):
        dsm = DirectMessenger(HOST, self.username, self.password)
        new_msg = dsm.retrieve_all()
        for msg in new_msg:
            if msg.sender not in self.retrieved_msg:
                self.retrieved_msg[msg.sender] = [msg]
            else:
                self.retrieved_msg[msg.sender].append(msg)
        self.save_profile('/Users/leannenguyen/Desktop/ics32FinalProject/messages.dsu')

    def add_retrieved_msg(self):
        """
        Appends new retrieved messages as DirectMessage object into sent_msg attribute
        """
        dsm = DirectMessenger(HOST, self.username, self.password)
        new_msg = dsm.retrieve_new()
        for msg in new_msg:
            if msg.sender not in self.retrieved_msg:
                self.retrieved_msg[msg.sender] = [msg]
            else:
                self.retrieved_msg[msg.sender].append(msg)
        self.save_profile('/Users/leannenguyen/Desktop/ics32FinalProject/messages.dsu')


    def get_msg_from_contact(self, contact: str):
        if contact in self.retrieved_msg:
            return self.retrieved_msg[contact]
        else:
            print('contact not in retrived msg')
            return []
    
    def gen_msg_thread(self, contact: str):
        retrieved = self.get_msg_from_contact(contact)
        msg_thread = ''
        for msg in retrieved:
            if msg.recipient == 'me':
                msg_thread += f'{msg.sender}: {msg.message}\n\n'
            else:
                msg_thread += f'me: {msg.message}\n\n'
        return msg_thread

    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                # for msg_obj in obj['sent_msg']:
                #     msg = DirectMessage(msg_obj['recipient'], msg_obj['message'], msg_obj['timestamp'])
                #     self.sent_msg.append(msg)
                messages = obj['retrieved_msg']
                for contact, msg_list in messages.items():
                    for msg in msg_list:
                        msg_obj = DirectMessage(msg['recipient'], msg['message'], msg['timestamp'], msg['sender'])
                        if contact not in self.retrieved_msg:
                            self.retrieved_msg[contact] = [msg_obj]
                        else:
                            self.retrieved_msg[contact].append(msg_obj)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
        

if __name__ == '__main__':
    profile = MessengerProfile()
    # profile.load_profile('/Users/leannenguyen/Desktop/ics32FinalProject/messages.dsu')
    messages = profile.retrieved_msg
    # print(messages)
    # for message in messages:
    #     print(message, messages[message])
    msg_thread = profile.gen_msg_thread('leanyash')
    print(msg_thread)
    