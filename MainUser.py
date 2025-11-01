from User import User

class MainUser(User) : 
    def __init__(self):
        super().__init__()
        self.privateKey = dict[int, bytes]()

    def addPrivateKey(self, algoScheme : int, key : bytes):
        self.privateKey[algoScheme] = key