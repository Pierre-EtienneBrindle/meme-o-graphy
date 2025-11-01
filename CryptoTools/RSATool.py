from .CryptoTool import CryptoTool
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class RSATool(CryptoTool):

    def encrypt(self, message : str, key : bytes) -> bytes:
        public_key = RSA.import_key(key)
        cipher_rsa = PKCS1_OAEP.new(public_key)
        return cipher_rsa.encrypt(message.encode("utf-8"))

    def decrypt(self, encrypted : bytes, key : bytes) -> str:
        private_key = RSA.import_key(key)
        cipher_rsa = PKCS1_OAEP.new(private_key)
        return cipher_rsa.decrypt(encrypted).decode("utf-8")

    def generateKeyPair(self)-> tuple[bytes, bytes]:
        private_key = RSA.generate(2048)
        return (private_key.export_key(), 
                private_key.public_key().export_key()
                )