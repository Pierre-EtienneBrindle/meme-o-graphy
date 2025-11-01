from typing import Self
from itertools import batched
from math import prod
import numpy as np

import PIL
from Image import Image
from BitIterator import BitIterator


class ImageLossy(Image):
    def __init__(self):
        super().__init__()

    @staticmethod
    def fromPILImage(image: PIL.Image.Image) -> Self:
        image.__class__ = ImageLossy
        return image

    def getFreeSpace(self) -> int:
        return prod(self.size) * len(self.getbands())

    def encode(self, bits: bytes):
        pixels = np.array(self)
        for i in range(pixels.shape[2]):
            freqs = np.fft.rfft2(pixels[:, :, i])
            print(freqs)

        self = ImageLossy.fromPILImage(PIL.Image.fromarray(pixels))


    def decode(self) -> bytes:
        pixelss = np.array(self)
        bits = []
        for i in range(pixelss.shape[2]):
            pixels = pixelss[:, :, i]
            freqs = np.fft.rfft2(pixels)


if __name__ == "__main__":
    test_image = ImageLossy.fromPILImage(PIL.Image.open("/tmp/image.png").copy())
    data = test_image.decode()
    test_image.encode("Allo")
    print(data)
    test_image.save("/tmp/test.png")
