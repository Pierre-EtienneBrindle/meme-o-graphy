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
        total_0 = 0
        for i in range(min(pixels.shape[2], 3)):
            freqs = np.fft.fftshift(pixels[:, :, i])
            x_min = 0
            x_max = pixels.shape[0] -1
            y_min = 0
            y_max = pixels.shape[1] - 1
            delta = (1,0)
            curr_pos = (-1,0)
            for _ in range((pixels.shape[0] ) * (pixels.shape[1])):
                next_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                if next_pos[0] < x_min and delta[0] < 0 : 
                    delta = (-delta[1], delta[0])
                    y_max -= 1
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[0] > x_max and delta[0] > 0: 
                    delta = (-delta[1], delta[0])
                    y_min += 1
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[1] < y_min and delta[1] < 0:
                    delta = (-delta[1], delta[0])
                    x_min += 1
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[1] > y_max and delta[1] > 0: 
                    delta = (-delta[1], delta[0])
                    x_max -= 1
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                else :
                    curr_pos = next_pos


                freq = freqs[curr_pos[0], curr_pos[1]]
                norm = np.linalg.norm(freq)
                a = 2
                try:
                    to_add = next(bitIterator) * a / 2
                    if norm == 0 : 
                        total_0 += 1
                        freq = to_add 
                    else: 
                        freq = freq / norm * (norm - (norm % a) + to_add)
                except StopIteration:
                    break
                freqs[curr_pos[0], curr_pos[1]] = freq 
            pixels[:, :, i] = np.fft.ifftshift(freqs) # Unchanged almost, diff of 10^-12
            freqs2 = np.fft.fftshift(pixels[:, :, i])
            diff = freqs - freqs2

        return ImageLossy.fromPILImage(PIL.Image.fromarray(pixels))


    def decode(self) -> bytes:
        pixels = np.array(self)
        bits = []
        for i in range(min(pixels.shape[2], 3)):
            freqs = np.fft.fftshift(pixels[:, :, i])
            x_min = 0
            x_max = pixels.shape[0] -1
            y_min = 0
            y_max = pixels.shape[1] - 1
            delta = (1,0)
            curr_pos = (-1,0)
            for _ in range((pixels.shape[0] ) * (pixels.shape[1])):
                next_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                if next_pos[0] < x_min and delta[0] < 0 : 
                    delta = (-delta[1], delta[0])
                    y_max -= 1
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[0] > x_max and delta[0] > 0: 
                    delta = (-delta[1], delta[0])
                    y_min += 1
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[1] < y_min and delta[1] < 0:
                    delta = (-delta[1], delta[0])
                    x_min += 1
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[1] > y_max and delta[1] > 0: 
                    delta = (-delta[1], delta[0])
                    x_max -= 1
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                else :
                    curr_pos = next_pos

                freq = freqs[curr_pos[0], curr_pos[1]]
                norm = np.linalg.norm(freq)
                bits.append(round(norm) % 2)

        data = []
        for batch in batched(bits, 8):
            value = sum(v << i for i, v in enumerate(batch))
            data.append(value)

        return bytes(data)


if __name__ == "__main__":
    test_image = ImageLossy.fromPILImage(PIL.Image.open("./c_change.png").copy())
    #message = b"Allo" * 4000
    #test_image = test_image.encode(b"Allo" * 4000)
    #test_image.save("./c_change.png")
    data = test_image.decode()
    print(data[0:4000 * 4].decode("utf-8"))
