from PIL.Image import Image as PILImage

class Image(PILImage):
    def __init__(self):
        pass

    def getFreeSpace(self) -> int:
        pass

    def encode(self, bits: bytes):
        pass

    def decode(self) -> bytes:
        pass
