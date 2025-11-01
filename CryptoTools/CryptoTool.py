class CryptoTool():

    def encrypt(self, message : bytes, key : bytes) -> bytes:
        """Encrypts the message

        Args:
            message (bytes): The message to encrypt
            key (bytes): The public key

        Returns:
            bytes: The encrypted message as a byte array
        """
        assert False, "NOT IMPLEMENTED"

    def decrypt(self, encrypted : bytes, key : bytes) -> str:
        """Decrypts a message

        Args:
            encrypted (bytes): The encrypted message
            key (bytes): The private key

        Returns:
            str: The message decrypted
        """
        assert False, "NOT IMPLEMENTED"

    def sign(self, message : bytes, key : bytes) -> bytes:
        """Returns the signature for the given message

        Args:
            message (bytes): The message
            key (bytes): The private key

        Returns:
            bytes: The signature
        """
        assert False, "NOT IMPLEMENTED"

    def verify(self, message: bytes, key : bytes, signature : bytes) -> bool:
        """Verifies if the signature is valid

        Args:
            message (bytes): The message signed 
            key (bytes): The public key of the sender
            signature (bytes): The signature of the sender

        Returns:
            bool: True iff the signature is valid 
        """
        assert False, "NOT IMPLEMENTED"

    def generateKeyPair(self)-> tuple[bytes, bytes]:
        """Generate the key pair

        Returns:
            tuple[bytes, bytes]: The key generated. 
            Key[0] = private key, Key[1] => public key
        """
        assert False, "NOT IMPLEMENTED"