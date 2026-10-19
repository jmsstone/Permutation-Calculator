from permutation import Permutation
from permutation import IDENTITY
from transposition import Transposition
from itertools import permutations

'''
    generateTranspositions(n):  This function generates the transpositions for the set of positive
                            whole numbers up to n (inclusive)
    inputs: This function takes one integer as input.
    Notes:  Since we store transpositions in cycle notation (1 2) and (2 1) are equivalent, thus we
            only need to go one direction in our for loops.
'''
def generateTranspositions(n: int) -> list:
    listOfProducts = []

    for i in range(1,n+1): 
        for j in range(i+1,n+1):
            listOfProducts.append(Transposition(i,j))
    return listOfProducts

'''
    printProducts(products): this function takes in a list of products and prints them out
    Input: should be a list of products but will actually work with most lists of any type.
    Notes: mainly used for debugging purposes.
'''
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

'''
    setOfProducts(perms):   This function takes in a list of permutations and calculates the
                            product of every possible ordering of permutations in that set.
    Input: perms: a list of permutations
    Notes:  Horribly inefficient algorithm O(n!). This was my original function when i was 
            working on understanding computationally why the product of all transpositions
            in a given S_n is always equal to either A_n or S_n / A_n. Highly recomended to 
            use setOfProductsDP instead.
'''
def setOfProducts(perms: list[Permutation]):
    products = set()
    for permutation_set in permutations(perms):
        products.add(multiply_permutations(permutation_set))
    return products

'''
    setOfProductsDP(perms): this function does the exact same thing as setOfProducts but
                            instead uses a dynamic programing approach to reduce the time
                            complexity significantly.
    Input: perms: a list of perms
    Notes:  This function still is O(2^n) so still quite inneficient. In practice if you   
            want to generate the alternating group there are far better ways however this
            was more for proof of concept that you could generate it using this way.
            Normal algorithms for generating A_n are instead O(n!/2) but where n is the length
            of the original set instead of the ammount of transpositions.
'''
# @AI
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
