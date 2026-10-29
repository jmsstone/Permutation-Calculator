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
    '''
    This class implements a permutation in the abstract algebra sense

    It represents a bijective mapping from one set to itself. It has composition,
    inverses, order, and cycle notation implemented. Under the hood, it is built
    on top of any mapping in which a cycle is completed. The mapping tells it where
    to send an element x. So the mapping {1:2, 2:3, 3:1} will send 1 to 2 (Very simple).

    Attributes:
        mapping: the underlying mapping structure 
    '''
    # only changes how our output is formatted
    USE_CYCLE_NOTATION: bool = True

    def __init__(self, mapping: Mapping[int, int] | None = None):
        # only store values that don't map to themselves
        # used Mapping instead of dict as it is immutable.
        self.mapping = {k: v for k,v in (mapping or {}).items() if k != v}

    """
        This method tells you where x is sent to by the permutation.

        args:
            x
        output:
            p(x)
    """
    def __call__(self, x:int) -> int:
        # returns where x goes defined by the permutation. x: p(x)
        return self.mapping.get(x,x)

    """
    This method converts the standard mapping format to the cycle format

    args: 
        self
    output:
        cycles: a list of disjoint cycles that represent the permutation
    """
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

    """
    This method returns whether two permutations are equal

    args:
        self
        other
    output:
        Whether they are equivalent or not
    """
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Permutation):
            return NotImplemented
        return self.mapping == other.mapping

    """
    This method returns a hash of the permutation
    Notes:  we overwrite this method because our __eq__ method is based off of 
            attributes of our class and not an instance of the object itself.
    args:
        self
    output:
        hash(mapping)
    """
    def __hash__(self):
        return hash(frozenset(self.mapping.items()))

    """
    This method multiplies two permutations
    Notes:  other is left multiplied by self. In permutations we are not gaurunteed that 
            multiplication is commutative so this is important to note.
    args:
        self
        other
    output:
        self*other
    """
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

    """
    This method returns the order of the permutation

    args:
        self
    output:
        the smallest value k such that p^k = e/IDENTITY
    """
    def order(self) -> int:
        cycles = self.to_cycles()
        if not cycles:
            return 1  # Identity element has order 1

        return math.lcm(*(len(cycle) for cycle in cycles))

    """
    This method returns a printable version of the permutation

    args:
        self
    output:
        string version of the permutation
    """
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

    """
    This method just returns repr(self)

    args:
        self
    output:
        string version of self
    """
    def __str__(self) -> str:
        return repr(self)

    """
    This method calculates the inverse of the permutation

    args:
        self
    output:
        the inverse of self
    """
    def inverse(self) -> Permutation:
        inv = Permutation({v: k for k, v in self.mapping.items()})
        return inv

'''
Singleton instance of the permutation's identity (e)

This class represents the identity permutation or just the permutation that
sends every element to itself. I used a singleton pragmatic as any instance
of the identity should point to the identity. It also comes up quite often
in normal calculations such as order() so to make sure that I didn't just have
a bunch of duplicates of this super common permutation I use a singleton structure
so every time it would just refer to the same one. 
'''
class Identity(Permutation):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    '''
    This method returns a string version of the identity
    
    args:
        self
    output:
        "e"
    '''
    def __repr__(self) -> str:
        return "e"

    '''
    This method returns a string version of the identity

    args:
        self
    output:
        "e"
    '''
    def __str__(self) -> str:
            return "e"

    '''
    This method returns multiplication of the identity by something else

    args:
        self
        other
    output:
        other
    '''
    def __mul__(self, other: object) -> Permutation:
        if not isinstance(other, Permutation):
            return NotImplemented
        return other

    '''
    Same as regular multiplication as Identity commutes with everything

    args:
        self
        other
    output:
        other
    '''
    def __rmul__(self, other: object) -> Permutation:
            if not isinstance(other, Permutation):
                return NotImplemented
            return other

    '''
    Returns hash of the identity
    Notes:  always returns consistant hash so python knows that any instance with
            this hash is the same object.
    args:
        self
    output:
        hash of self
    '''
    def __hash__(self):
        return hash("IDENTITY")

IDENTITY = Identity() 