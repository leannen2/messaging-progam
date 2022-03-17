# from NaClProfile import MessengerProfile

class Contact():
    def __init__(self, name=None, msg_log=None):
        self.name = name
        self.msg_log = msg_log

    def get_msg_log(self):
        return self.msg_log