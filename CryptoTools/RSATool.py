from .CryptoTool import CryptoTool
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class RSATool(CryptoTool):

    def encrypt(self, message : bytes, key : bytes) -> bytes:
        publicKey = RSA.import_key(key)
        cipherRSA = PKCS1_OAEP.new(publicKey)
        return cipherRSA.encrypt(message)

    def decrypt(self, encrypted : bytes, key : bytes) -> str:
        privateKey = RSA.import_key(key)
        cipherRSA = PKCS1_OAEP.new(privateKey)
        return cipherRSA.decrypt(encrypted)
    
    def sign(self, message, key):
        privateKey = RSA.import_key(key)
        signer = pkcs1_15.new(privateKey)
        hash = SHA256.new(message)
        return signer.sign(hash)
    
    def verify(self, message, key, signature):
        publicKey = RSA.import_key(key)
        verifier = pkcs1_15.new(publicKey)
        hash = SHA256.new(message)
        try :
            verifier.verify(hash, signature)
            return True
        except :
            return False

    def generateKeyPair(self)-> tuple[bytes, bytes]:
        privateKey = RSA.generate(2048)
        return (privateKey.export_key(), 
                privateKey.public_key().export_key()
                )