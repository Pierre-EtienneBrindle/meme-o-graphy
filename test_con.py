from CryptoTools.RSATool import RSATool
from Message import Message
from User import User
from MainUser import MainUser

tempTool = RSATool()
mainUser = MainUser()
otherUser1 = User()
otherUser2 = User()

mainUserKeys = tempTool.generateKeyPair()
mainUser.addPrivateKey(0, mainUserKeys[0])
mainUser.addPublicKey(0, mainUserKeys[1])

otherUserKeys1 = tempTool.generateKeyPair()
otherUser1.addPublicKey(0, otherUserKeys1[1])

otherUserKeys2 = tempTool.generateKeyPair()
otherUser2.addPublicKey(0, otherUserKeys2[1])

text = "a"

message = Message(0, [otherUser1, otherUser2], text)

encoded = message.encode(mainUser)
print(encoded)
print(len(encoded) * 8)
