from typing import Self
from itertools import batched
from math import prod
import numpy as np

import PIL
from Image import Image
from BitIterator import BitIterator
from nToNSquare import coordonneesChemin
from math import ceil

MAX_BLOCK_SIZE = 5

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

        numColor = min(pixels.shape[2], 3)
        numBlockPerColor = ceil(8 * len(payLoad) / numColor)
        blockSize = ((pixels.shape[1] )* (pixels.shape[0]))  // numBlockPerColor
        blockSize = min(blockSize, MAX_BLOCK_SIZE) #make sure the block aren't to great

        allFreqs = []
        for i in range(min(pixels.shape[2], 3)):
            allFreqs.append(np.fft.fftshift(pixels[:, :, i]))

        curr_pos = (-1,0)
        delta = (1,0)
        x_min = 0 
        x_max = pixels.shape[0] - 1
        y_min = 0
        y_max = pixels.shape[1] -  1
        isDone = False
        for i in range(numBlockPerColor) : 
            
            #Get block footstep
            poses = []
            for _ in range(blockSize):
                next_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])

                if next_pos[0] < x_min and delta[0] < 0 :
                    y_max -= 1
                    delta = (-delta[1], delta[0])
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[0] > x_max and delta[0] > 0:
                    y_min += 1
                    delta = (-delta[1], delta[0])
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[1] < y_min and delta[1] < 0 :
                    x_min += 1
                    delta = (-delta[1], delta[0])
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[1] > y_max and delta[1] > 0:
                    x_max -= 1
                    delta = (-delta[1], delta[0])
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                else :
                    curr_pos = next_pos
                
                poses.append(curr_pos)

            for j in range(numColor):
                freqs = []
                for pos in poses:
                    freqs.append(allFreqs[j][pos[0],pos[1]])
                
                norms = [np.linalg.norm(freq) for freq in freqs]

                #Average frequencies or encode them all the same ?
                meanNorm = sum(norms) / blockSize
                a = 2
                try:
                    to_add = next(bitIterator) * a / 2
                except StopIteration:
                    isDone = True
                    break
                
                newNorm = meanNorm - (meanNorm % a) + to_add

                for k in range(blockSize):
                    freq = freqs[k]
                    norm = norms[k]
                    pos = poses[k]
                    if norm == 0:
                        allFreqs[j][pos[0], pos[1]] = newNorm
                    else:
                        allFreqs[j][pos[0], pos[1]] = freq / norm * newNorm

            if(isDone):
                break
        
        maxNorms = 0
        maxNormsColor = -1
        existDifferent = False
        for i in range(numColor):
            normBlock1 = np.linalg.norm(allFreqs[i][0,0])
            normBlock2 = np.linalg.norm(allFreqs[i][blockSize,0])
            if normBlock1 != normBlock2 :
                existDifferent = True
                break
            
            if normBlock1 > maxNorms:
                maxNorms = normBlock1
                maxNormsColor = i
        
        if not existDifferent:
            if maxNorms == 0:
                for i in range(blockSize):
                    allFreqs[maxNormsColor][i + blockSize, 0] = 2
            else:
                for i in range(blockSize):
                    allFreqs[maxNormsColor][i + blockSize,0] *= (maxNorms + 2)  / maxNorms
        

        for i in range(numColor):
            pixels[:, :, i] = np.fft.ifftshift(allFreqs[i])

        return ImageLossy.fromPILImage(PIL.Image.fromarray(pixels))


    def decode(self) -> bytes:
        pixels = np.array(self)
        numColor = min(pixels.shape[2], 3)

        allFreqs = []
        for i in range(numColor):
            allFreqs.append(np.fft.fftshift(pixels[:, :, i]))

        #Finds the block's size
        blockSize = MAX_BLOCK_SIZE #Assume the blocksize is maximal
        for i in range(numColor):
            j = 1
            currNorm = np.linalg.norm(allFreqs[i][0,0])
            while j < blockSize :
                nextNorm = np.linalg.norm(allFreqs[i][j, 0])
                if abs(currNorm - nextNorm )> .5 : 
                    blockSize = j 
                j += 1
        
        numBlockPerColor = ((pixels.shape[1] -2)* (pixels.shape[0]- 2)) // blockSize
        bits = []

        curr_pos = (-1,0)
        delta = (1,0)
        x_min = 0 
        x_max = pixels.shape[0] - 1
        y_min = 0
        y_max = pixels.shape[1] -  1

        for i in range(numBlockPerColor) : 
            
            #Get block footstep
            poses = []
            for _ in range(blockSize):
                next_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])

                if next_pos[0] < x_min and delta[0] < 0 :
                    y_max -= 1
                    delta = (-delta[1], delta[0])
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[0] > x_max and delta[0] > 0:
                    y_min += 1
                    delta = (-delta[1], delta[0])
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[1] < y_min and delta[1] < 0 :
                    x_min += 1
                    delta = (-delta[1], delta[0])
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                elif next_pos[1] > y_max and delta[1] > 0:
                    x_max -= 1
                    delta = (-delta[1], delta[0])
                    curr_pos = (curr_pos[0] + delta[0], curr_pos[1] + delta[1])
                else :
                    curr_pos = next_pos
                
                poses.append(curr_pos)

            for j in range(numColor):
                freqs = []
                for pos in poses:
                    freqs.append(allFreqs[j][pos[0],pos[1]])
                
                norms = [np.linalg.norm(freq) for freq in freqs]
                bits.append(round(sum(norms) / blockSize) % 2)

        data = []
        for batch in batched(bits, 8):
            value = sum(v << i for i, v in enumerate(batch))
            data.append(value)
        fileSize = int.from_bytes(data[0:4], byteorder= "big")
        return bytes(data[4:fileSize + 4])

if __name__ == "__main__":
    test_image = ImageLossy.fromPILImage(PIL.Image.open("./b.webp").copy())
    with open("test.txt", "r") as file :
        text = file.read()
        message = text.encode("utf-8")
    test_image = test_image.encode(message)
    test_image.save("./bee-ception.png")
    data = test_image.decode()
    print(data.decode("utf-8"))
