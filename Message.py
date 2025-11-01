from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import CryptoTools
from CryptoTools.CryptoTool import CryptoTool
from User import User
from MainUser import MainUser
from math import log2, ceil

#Symmetric key constants 
SYM_KEY_SIZE = 16
SYM_KEY_MODE_USED = AES.MODE_CFB

#List of all encryption schemes supported
RSA = 0
ECC = 1

class Message:

    def __init__(self, algoAsyScheme = -1, users : list[User] = [], text = ""):
        """Generates the Message structure

        Args:
            algoAsyScheme (int, optional): Enum value of the asymmetric key scheme to use. Defaults to -1.
            users (list[User], optional): The user's the message is send to. Defaults to [].
            text (str, optional): The text to send. Defaults to "".
        """
        self.algoAsyScheme = algoAsyScheme #Error value by default
        self.users = users #Error value by default (could change latter)
        self.text = text #Empty string be default


    def encode(self, sender : MainUser) -> bytes :
        """Encodes the message into a byte string

        Returns:
            bytes: The encoded message following this pattern : 
                    byte 1 => Asymmetric key scheme used
                    byte 2 => Number of users 
                    bytes 3 to 3 + 16 * num users =>  the symmetric key encoded for each user
        """
        RSA = 0
        ECC = 1

        #Validations before proceeding
        assert self.algoAsyScheme in [RSA,ECC] , "Invalid asymmetric scheme used"
        assert self.algoAsyScheme in sender.privateKey.keys(), "No key created for current user"
        assert self.text != "", "Empty message"
        assert self.users != [] or len(self.users) >= 256, "Invalid number of users to send to"


        #Adding the asymmetric key scheme used
        result = bytearray()
        result.append(self.algoAsyScheme)

        print(f"Added the scheme {self.algoAsyScheme}")
        print(result[0])
        print(result)

        #Choosing the correct scheme
        tool : CryptoTool = None
        match(self.algoAsyScheme):
            case 0 : 
                tool = CryptoTools.RSATool.RSATool()
            case 1:
                tool = CryptoTools.ECCTool.ECCTool()
        

        #Adding the number of keys that will be stored
        result.append(len(self.users))

        print(f"Added the number of users {len(self.users)}")
        print(result[1])
        print(result)

        #Create the key used for the symmetric encryption
        symmetricKey = get_random_bytes(SYM_KEY_SIZE)

        #Adds the length of a symmetric key once encoded 
        encryptedSymmetricKeyLength = len(tool.encrypt(symmetricKey, sender.publicKeys[self.algoAsyScheme]))
        result += encryptedSymmetricKeyLength.to_bytes(2)

        print(f"Added the length of the symmetric key {encryptedSymmetricKeyLength}")
        print(result[2:4])
        print(result)

        #Iterate over each user and add the symmetric key encrypted 
        for user in self.users: 
            assert self.algoAsyScheme in user.publicKeys.keys(), "User doesn't have key scheme"
            userKey = user.publicKeys[self.algoAsyScheme]
            encryptedKey = tool.encrypt(symmetricKey,userKey)
            result += encryptedKey


        print("Added the symmetric key encoded")
        print(result[4:4 + len(self.users) * encryptedSymmetricKeyLength])
        print(result)

        #Get the current message (asymmetric scheme + number keys + hashed keys) to create a signature
        currentMessage = bytes(result)
        signature = tool.sign(currentMessage, sender.privateKey[self.algoAsyScheme])

        #Adds the signature length 
        signatureLength = len(signature)
        result += signatureLength.to_bytes(4)

        print(f"Added signature length {signatureLength}")
        print(result[4 + len(self.users) * encryptedSymmetricKeyLength : 4 + len(self.users) * encryptedSymmetricKeyLength + 4])
        print(result)

        #Adds the signature
        result += signature

        #Uses the cipher on the text
        cipher = AES.new(symmetricKey, SYM_KEY_MODE_USED)
        cipheredText = cipher.encrypt(self.text.encode("utf-8"))

        #Adds the text length 
        cipheredTextLength = len(cipheredText)
        result += cipheredTextLength.to_bytes(59)

        print(f"Added text length {cipheredTextLength}")
        print(result[ 4 + len(self.users) * encryptedSymmetricKeyLength + 4 : 4 + len(self.users) * encryptedSymmetricKeyLength + 63])
        print(result)

        #Adds the text
        result += cipheredText

        #MISSING ERROR CORRECTION 
        return bytes(result)

        
