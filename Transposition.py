from permutation import Permutation

class Transposition(Permutation):
    def __init__(self,i: int, j: int):
        if i == j:
            raise ValueError("Indices must be distinct")
        self.i = i
        self.j = j
        super().__init__({i: j, j: i})