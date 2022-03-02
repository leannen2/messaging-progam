# NaClProfile.py
# An encrypted version of the Profile class provided by the Profile.py module
# 
# for ICS 32
# by Mark S. Baldwin


# TODO: Install the pynacl library so that the following modules are available
# to your program.
import nacl.utils, json, os
from nacl.public import PrivateKey, PublicKey, Box
from pathlib import Path

from NaClDSEncoder import NaClDSEncoder

# TODO: Import the Profile and Post classes
from Profile import Profile, Post, DsuFileError, DsuProfileError
# TODO: Import the NaClDSEncoder module
    
# TODO: Subclass the Profile class
class NaClProfile(Profile):
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
        self.public_key = ''
        self.private_key = ''
        self.keypair = ''

    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.

        TODO: Complete the generate_keypair method.

        This method should use the NaClDSEncoder module to generate a new keypair and populate
        the public data attributes created in the initializer.

        :return: str    
        """
        encode = NaClDSEncoder()
        encode.generate()
        self.public_key = encode.public_key
        self.private_key = encode.private_key
        self.keypair = encode.keypair

    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.

        TODO: Complete the import_keypair method.

        This method should use the keypair parameter to populate the public data attributes created by
        the initializer. 
        
        NOTE: you can determine how to split a keypair by comparing the associated data attributes generated
        by the NaClDSEncoder
        """
        
        index_of_private_key = keypair.find('=') + 1
        public = keypair[:index_of_private_key]
        private = keypair[index_of_private_key:]
        self.public_key = public
        self.private_key = private
        self.keypair = keypair

    # encrypts string given with public and private keys
    def _encrypt(self, message, priv_key, pub_key):
        encoder = NaClDSEncoder()
        private_key = encoder.encode_private_key(priv_key)
        public_key = encoder.encode_public_key(pub_key)
        box = encoder.create_box(private_key, public_key)
        encrypted_message = encoder.encrypt_message(box, message)
        return encrypted_message

    def _decrypt(self, message, priv_key, pub_key):
        encoder = NaClDSEncoder()
        private_key = encoder.encode_private_key(priv_key)
        public_key = encoder.encode_public_key(pub_key)
        box = encoder.create_box(private_key, public_key)
        decrypted_message = encoder.decrypt_message(box, message)
        return decrypted_message

    """
    TODO: Override the add_post method to encrypt post entries.

    Before a post is added to the profile, it should be encrypted. Remember to take advantage of the
    code that is already written in the parent class.

    NOTE: To call the method you are overriding as it exists in the parent class, you can use the built-in super keyword:
    
    super().add_post(...)
    """

    def add_post(self, post: Post) -> None:
        entry = post.get_entry()
        encrypted_entry = self._encrypt(entry, self.private_key, self.public_key)
        new_post = Post(entry = encrypted_entry)
        print(new_post)
        super().add_post(new_post)

    """
    TODO: Override the get_posts method to decrypt post entries.

    Since posts will be encrypted when the add_post method is used, you will need to ensure they are 
    decrypted before returning them to the calling code.

    :return: Post
    
    NOTE: To call the method you are overriding as it exists in the parent class you can use the built-in super keyword:
    super().get_posts()
    """
    def get_posts(self) -> list[Post]:
        posts = super().get_posts()
        decrypted = []
        for post in posts:
            new_post = Post(entry = self._decrypt(post.get_entry(), self.private_key, self.public_key))
            decrypted.append(new_post)
        return decrypted

    
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
                self.private_key = obj['private_key']
                self.public_key = obj['public_key']
                self.keypair = obj['keypair']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()

    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Used to encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.
        
        TODO: Complete the encrypt_entry method.

        NOTE: A good design approach might be to create private encrypt and decrypt methods that your add_post, 
        get_posts and this method can call.
        
        :return: bytes 
        """
        encrypted = self._encrypt(entry, self.private_key, public_key)
        return encrypted
        

if __name__ == '__main__':
    profile = NaClProfile()
    profile.generate_keypair()
    post1 = Post(entry = 'hello')
    print(post1)
    profile.add_post(post1)
    print(profile._posts)
    print(profile.get_posts())
    print('encrypted:', profile.encrypt_entry('hello', profile.public_key))
    profile.save_profile('/Users/leannenguyen/ics32/assignment-5-encrypted-graphical-user-interface-leannen2/new.dsu')
    np2 = NaClProfile()
    np2.load_profile('/Users/leannenguyen/ics32/assignment-5-encrypted-graphical-user-interface-leannen2/new.dsu')
    np2.save_profile('/Users/leannenguyen/ics32/assignment-5-encrypted-graphical-user-interface-leannen2/new2.dsu')
    np2.import_keypair(profile.keypair)
    print(profile.keypair)
    print(np2.keypair)
    print(profile.public_key)
    print(np2.public_key)
    print(profile.private_key)
    print(np2.private_key)