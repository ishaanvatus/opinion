from config import D

def F1(pos):
    return sum(pos[d]**3 - 1.5*pos[d] for d in range(D))

def F2(pos):
    return sum(pos[d] for d in range(D))
