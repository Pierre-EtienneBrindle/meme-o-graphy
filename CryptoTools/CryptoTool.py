class CryptoTool():

    def encrypt(self, message : str, key : bytes) -> bytes:
        """Encrypts the message

        Args:
            message (str): The message to encrypt
            key (bytes): Yhe public key

        Returns:
            bytes: The encrypted message as a byte array
        """
        assert False #Stops if the tool is incomplete

    def decrypt(self, encrypted : bytes, key : bytes) -> str:
        """Decrypts a message

        Args:
            encrypted (bytes): The encrypted message
            key (bytes): The private key

        Returns:
            str: The message decrypted
        """
        assert False #Stops if the tool is incomplete

    def generateKeyPair()-> tuple[bytes, bytes]:
        """Generate the key pair

        Returns:
            tuple[bytes, bytes]: The key generated. 
            Key[0] = private key, Key[1] => public key
        """
        assert False #Stops if the tool is incomplete