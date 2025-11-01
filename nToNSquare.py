from math import sqrt, floor

def coordonneesChemin(n : int) :
    """Gimme n, I will give you n^2 : Karo-kan"""
    assert(n>0)
    wholePart = floor(sqrt(n-1))
    rest = (wholePart+1)**2 - n
    # Either a is equal to pE, or/and b is
    if rest < wholePart :
        return (wholePart, rest)
    elif rest > wholePart :
        return (2*wholePart - rest, wholePart)
    else :
        return (wholePart, wholePart)