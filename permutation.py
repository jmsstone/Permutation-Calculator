from __future__ import annotations
from typing import Mapping
from itertools import permutations
import math
from transposition import Transposition

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
            if len(cycle) > 1:
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
        inv = Permutation({v: k for k,v in (self.mapping or {}).items() if k != v})
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

def generateTranspositions(n: int) -> list:
    listOfProducts = []

    for i in range(1,n+1):
        for j in range(i+1,n+1):
            listOfProducts.append(Transposition(i,j))
    return listOfProducts

def printProducts(products: list):
    for transposition in products:
        print(str(transposition))
    return

def multiply_permutations(perms: list[Permutation] | tuple[Permutation, ...]) -> Permutation:
    """
    Recursively computes the product of an ordered list of permutations.
    [p1, p2, p3] evaluates to p1 * p2 * p3.
    """
    # Base Case 1: Empty sequence yields the identity element
    if not perms:
        return IDENTITY

    # Base Case 2: Single permutation yields itself
    if len(perms) == 1:
        return perms[0]

    # Recursive Step: Multiply head by product of tail
    return perms[0] * multiply_permutations(perms[1:])

def setOfProducts(perms: list[Permutation]):
    products = set()
    for permutation_set in permutations(perms):
        products.add(multiply_permutations(permutation_set))
    return products

def setOfProductsDP(perms: list[Permutation]) -> set[Permutation]:
    """Computes the set of products using Bitmask DP in O(2^m) steps."""
    m = len(perms)
    # dp[mask] maps a bitmask subset of used transpositions to reachable permutations
    dp: dict[int, set[Permutation]] = {0: {IDENTITY}}

    for mask in range(1 << m):
        if mask not in dp:
            continue
        current_perms = dp[mask]

        for i, t in enumerate(perms):
            if not (mask & (1 << i)):
                next_mask = mask | (1 << i)
                if next_mask not in dp:
                    dp[next_mask] = set()
                # Accumulate reachable permutations
                for p in current_perms:
                    dp[next_mask].add(p * t)

    full_mask = (1 << m) - 1
    return dp[full_mask]