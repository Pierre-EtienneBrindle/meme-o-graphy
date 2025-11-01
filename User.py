
class User :

    def __init__(self):
        self.publicKeys = dict[int, bytes]()
    
    def addPublicKey(self, algoScheme : int, key : bytes):
        self.publicKeys[algoScheme] = key