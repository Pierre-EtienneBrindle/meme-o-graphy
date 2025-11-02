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

    def encode(self, payLoad: bytes):
        payLoad = len(payLoad).to_bytes(4, byteorder="big") + payLoad
        bitIterator = BitIterator(payLoad)
        pixels = np.array(self)

        maxBlockSize = np.floor(pixels.shape[1] * pixels.shape[0] * 3 / 8 / len(payLoad))
        maxBlockSize = np.min(maxBlockSize, 5) #make sure the block aren't to great
         
        for i in range(min(pixels.shape[2], 3)):
            freqs = np.fft.fftshift(pixels[:, :, i])
            for x in range(pixels.shape[0]):
                for y in range(pixels.shape[1]):
                    freq = freqs[x, y]
                    norm = np.linalg.norm(freq)
                    a = 2
                    try:
                        to_add = next(bitIterator) * a / 2
                        if norm == 0 : 
                            freq = to_add 
                        else: 
                            freq = freq / norm * (norm - (norm % a) + to_add)
                    except StopIteration:
                        break
                    freqs[x, y] = freq 
            pixels[:, :, i] = np.fft.ifftshift(freqs)

        return ImageLossy.fromPILImage(PIL.Image.fromarray(pixels))


    def decode(self) -> bytes:
        pixels = np.array(self)
        bits = []
        for i in range(min(pixels.shape[2], 3)):
            freqs = np.fft.fftshift(pixels[:, :, i])
            for x in range(pixels.shape[0]):
                for y in range(pixels.shape[1]):
                    freq = freqs[x, y]
                    norm = np.linalg.norm(freq)
                    bits.append(round(norm) % 2)
        data = []
        for batch in batched(bits, 8):
            value = sum(v << i for i, v in enumerate(batch))
            data.append(value)
        fileSize = int.from_bytes(data[0:4], byteorder= "big")
        return bytes(data[4:fileSize + 4])


if __name__ == "__main__":
    test_image = ImageLossy.fromPILImage(PIL.Image.open("./bee-ception.png").copy())
    #with open("test.txt", "r") as file :
        #text = file.read()
        #message = text.encode("utf-8")
    #test_image = test_image.encode(message)
    #test_image.save("./bee-ception.png")
    data = test_image.decode()
    print(data.decode("utf-8"))
