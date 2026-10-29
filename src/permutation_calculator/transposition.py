'''
Author: James Stone
Date: 10/15/2026
Purpose:    The purpose of this file is to create a subclass of permutations that represents
            a transposition.
'''
from permutation_calculator import Permutation

'''
Simple subclass of Permutations that represents any permutation that only swaps two elements
'''
class Transposition(Permutation):
    def __init__(self,i: int, j: int):
        if i == j:
            raise ValueError("Indices must be distinct")
        self.i = i
        self.j = j
        # creating a permutation with the mapping of swapping i and j
        super().__init__({i: j, j: i})