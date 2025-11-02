from typing import Self
from itertools import batched
from math import prod
import numpy as np

import PIL
from Image import Image
from BitIterator import BitIterator
from nToNSquare import coordonneesChemin


class ImageLossy(Image):
    def __init__(self):
        super().__init__()

    @staticmethod
    def fromPILImage(image: PIL.Image.Image) -> Self:
        image.__class__ = ImageLossy
        return image

    def getFreeSpace(self) -> int:
        return prod(self.size) * len(self.getbands())

    def encode(self, bytes_: bytes):
        bitIterator = BitIterator(bytes_)
        pixels = np.array(self)
        for i in range(min(pixels.shape[2], 3)):
            freqs = np.fft.fft2(pixels[:, :, i], norm="forward")
            for j in range(100 * 100):
                coord = coordonneesChemin(j)
                # coord = (freqs.shape[0] - coord[0] - 1, freqs.shape[1] - coord[1] - 1) # Inverse le sens
                freq = freqs[coord[0], coord[1]]
                a = 2
                freq = np.complex128(freq.real - freq.real % a, freq.imag)
                try:
                    val = next(bitIterator) * a / 2
                    freq = np.complex128(freq.real + val, freq.imag)
                except StopIteration:
                    break
                freqs[coord[0], coord[1]] = freq 
            pixels[:, :, i] = np.fft.ifft2(freqs, s=pixels.shape[:2], norm="forward") # Unchanged almost, diff of 10^-12
            freqs2 = np.fft.fft2(pixels[:, :, i], norm="forward")
            diff = freqs - freqs2
            print(diff.min(), diff.max()) # 10^6

        return ImageLossy.fromPILImage(PIL.Image.fromarray(pixels))


    def decode(self) -> bytes:
        pixels = np.array(self)
        bits = []
        for i in range(pixels.shape[2]):
            freqs = np.fft.rfft2(pixels[:, :, i])
            for j in range(100 * 100):
                coord = coordonneesChemin(j)
                freq = freqs[coord[0], coord[1]]
                bits.append(round(freq.real) & 1)

        data = []
        for batch in batched(bits, 8):
            value = sum(v << i for i, v in enumerate(batch))
            data.append(value)

        return bytes(data)


if __name__ == "__main__":
    test_image = ImageLossy.fromPILImage(PIL.Image.open("/tmp/image.png").copy())
    test_image = test_image.encode(b"Allo" * 4000)
    # data = test_image.decode()
    # print(data)
    test_image.save("/tmp/test.png")
