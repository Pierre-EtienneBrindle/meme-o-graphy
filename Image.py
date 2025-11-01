from PIL.Image import Image as PILImage

class Image(PILImage):
    def __init__(self):
        super().__init__()

    @staticmethod
    def fromPILImage(image: PILImage) -> Self:
        image.__class__ = Image
        return image

    def getFreeSpace(self) -> int:
        raise NotImplemented

    def encode(self, bits: bytes):
        raise NotImplemented

    def decode(self) -> bytes:
        raise NotImplemented
