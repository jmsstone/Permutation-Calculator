from __future__ import annotations
from typing import Mapping
from itertools import permutations
import math
'''
Author: James Stone
Date: 10/19/2026
Purpose:    The purpose of this file is to create a Permutation class that implements
            the math behind permutations in a group theoretic sense. That is, that a 
            permutation is some bijection from one set to itself. In this file it uses
            index-based permuting and only works on sets of numbers so far.
'''

class Permutation:

    USE_CYCLE_NOTATION: bool = True

    def __init__(self, mapping: Mapping[int, int] | None = None):
        # only store values that don't map to themselves
        # used Mapping instead of dict as it is immutable.
        self.mapping = {k: v for k,v in (mapping or {}).items() if k != v}

    def __call__(self, x:int) -> int:
        # returns where x goes defined by the permutation. x: p(x)
        return self.mapping.get(x,x)

    def to_cycles(self):
        visited = set()
        cycles = []
        for start in sorted(self.mapping.keys()):
            if start in visited:
                continue
            cycle = []
            curr = start
            while curr not in visited:
                visited.add(curr)
                cycle.append(curr)
                curr = self(curr)
            cycles.append(cycle) # only add a cycle if its not a fixed element.
        return cycles

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Permutation):
            return NotImplemented
        return self.mapping == other.mapping

    def __hash__(self):
        return hash(frozenset(self.mapping.items()))

    def __mul__(self, other:object) -> Permutation:
        if not isinstance(other, Permutation):
            return NotImplemented

        all_keys = set(self.mapping.keys()) | set(other.mapping.keys())

        new_mapping = {}
        for k in all_keys:
            val = self(other(k)) # we defined call method to return where an item maps to
            if k != val:
                new_mapping[k] = val

        # if our new mapping is completely empty that implies that every k == val which is just the identity permutation.
        if not new_mapping:
            return IDENTITY

        return Permutation(new_mapping)

    def order(self) -> int:
        """
        Calculates the order of the permutation, which is the smallest k > 0
        such that self^k == IDENTITY.
        """
        cycles = self.to_cycles()
        if not cycles:
            return 1  # Identity element has order 1

        return math.lcm(*(len(cycle) for cycle in cycles))

    def __repr__(self) -> str:
        if (self.USE_CYCLE_NOTATION):
            cycles = self.to_cycles()
            if not cycles:
                return "e"
            return "".join(f"({' '.join(map(str, c))})" for c in cycles)
        else:
            if not self.mapping:
                return "Permutation({})"
            return f"Permutation({self.mapping})"

    def __str__(self) -> str:
        return repr(self)

    def inverse(self) -> Permutation:
        inv = Permutation({v: k for k, v in self.mapping.items()})
        return inv


class Identity(Permutation):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
    def __repr__(self) -> str:
        return "e"
    
    def __str__(self) -> str:
            return "e"

    def __mul__(self, other: object) -> Permutation:
        if not isinstance(other, Permutation):
            return NotImplemented
        return other
    
    def __rmul__(self, other: object) -> Permutation:
            if not isinstance(other, Permutation):
                return NotImplemented
            return other
    
    def __hash__(self):
        return hash("IDENTITY")

IDENTITY = Identity() 