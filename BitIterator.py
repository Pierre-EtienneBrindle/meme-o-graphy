from typing import Optional


class BitIterator:
    def __init__(self, itterableBytes):
        self.it = iter(itterableBytes)
        self.currentByte = 0
        self.currentIndex = 7

    def __iter__(self):
        return self

    def __next__(self) -> Optional[bool]:
        if self.currentIndex == 7:
            self.currentByte = next(self.it)
            self.currentIndex = -1 

        if self.currentByte is None:
            raise StopIteration

        self.currentIndex += 1
        return (self.currentByte >> self.currentIndex) & 0x01 == 0x01


if __name__ == "__main__":
    from itertools import batched

    s = "Allo"
    a = BitIterator(s.encode())

    for b, character in zip(batched(a, 8), s):
        expectedByte = ord(character)
        for i in range(8):
            if b[i] != (expectedByte >> i & 1):
                print(b[i], expectedByte & (1 << i))
