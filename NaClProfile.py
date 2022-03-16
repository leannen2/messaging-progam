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
        """
        TODO: Complete the initializer method. Your initializer should create the follow three 
        public data attributes:

        public_key:str
        private_key:str
        keypair:str

        Whether you include them in your parameter list is up to you. Your decision will frame 
        how you expect your class to be used though, so think it through.
        """
        super().__init__()
        self.sent_msg = {}
        self.retrieved_msg = {}
        self.ds_msger = DirectMessenger(HOST, 'markLeanneYash', 'thisisapwd')
        self.add_all_msg()

    def add_sent_msg(self, dir_message: DirectMessage):
        """
        Appends sent messages as DirectMessage object into sent_msg attribute
        """
        self.sent_msg.append(dir_message)

    def add_all_msg(self):
        new_msg = self.ds_msger.retrieve_all()
        print('new', new_msg)
        for msg in new_msg:
            if msg.sender not in self.retrieved_msg:
                self.retrieved_msg[msg.sender] = [msg]
            else:
                self.retrieved_msg[msg.sender].append(msg)
    def add_retrieved_msg(self):
        """
        Appends new retrieved messages as DirectMessage object into sent_msg attribute
        """
        new_msg = self.ds_msger.retrieve_new()
        print('new', new_msg)
        for msg in new_msg:
            if msg.sender not in self.retrieved_msg:
                self.retrieved_msg[msg.sender] = [msg]
            else:
                self.retrieved_msg[msg.sender].append(msg)
    
    """
    TODO: Override the load_profile method to add support for storing a keypair.

    Since the DS Server is now making use of encryption keys rather than username/password attributes, you will 
    need to add support for storing a keypair in a dsu file. The best way to do this is to override the 
    load_profile module and add any new attributes you wish to support.

    NOTE: The Profile class implementation of load_profile contains everything you need to complete this TODO.
    Just copy the code here and add support for your new attributes.
    """

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
                for msg_obj in obj['sent_msg']:
                    msg = DirectMessage(msg_obj['recipient'], msg_obj['message'], msg_obj['timestamp'])
                    self.sent_msg.append(msg)
                for msg_obj in obj['retrieved_msg']:
                    msg = DirectMessage(msg_obj['recipient'], msg_obj['message'], msg_obj['timestamp'])
                    self.retrieved_msg.append(msg)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
        

if __name__ == '__main__':
    profile = MessengerProfile()
    messages = profile.retrieved_msg
    # print(messages)
    for message in messages:
        print(message, messages[message])
    profile.save_profile('/Users/leannenguyen/Desktop/ics32FinalProject/messages.dsu')