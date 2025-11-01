from typing import Self
from itertools import batched
from math import prod

from PIL.Image import Image as PILImage

from Image import Image
from BitIterator import BitIterator


class ImageLossless(Image):
    def __init__(self):
        super().__init__()

    @staticmethod
    def fromPILImage(image: PILImage) -> Self:
        image.__class__ = ImageLossless
        return image

    def getFreeSpace(self) -> int:
        return prod(self.size) * len(self.getbands())

    def encode(self, bits: bytes):
        bitIterator = BitIterator(bits)
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for c in range(len(self.getbands())):
                    pixel = list(self.getpixel((x,y)))
                    pixel[c] &= 0xfe
                    try:
                        pixel[c] |= next(bitIterator)
                    except StopIteration:
                        pass
                    self.putpixel((x, y), tuple(pixel))

    def decode(self) -> bytes:
        bits = []
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for c in range(len(self.getbands())):
                    bits.append(self.getpixel((x, y))[c] & 0x01)

        data = []
        for batch in batched(bits, 8):
            value = sum(v << i for i, v in enumerate(batch))
            data.append(value)

        return bytes(data)


if __name__ == "__main__":
    from PIL import Image

    test_image = ImageLossless.fromPILImage(Image.new("RGB", (200, 200)))
    decoded_bytes = test_image.decode()
    test_image.save("/tmp/test.bmp")
