# Permutations in Abstract Algebra

A **permutation** is any bijective function mapping a set to itself. Every element in the set maps to a unique element within that same set.

---

## Cycle Notation
Cycle notation provides an intuitive way to describe permutations by tracing where elements map.

To write a permutation in cycle notation:
1. Start with an element and follow where it maps.
2. Repeat this mapping process until a cycle completes (returns to the starting element).
3. **Fixed points** (elements that map to themselves, $k \mapsto k$) are omitted.

**Example:**
The mapping $\{1 \mapsto 2, 2 \mapsto 3, 3 \mapsto 1, 4 \mapsto 4\}$ is written as:
$$(1\ 2\ 3)$$

---

## Multiplication (Function Composition)
Multiplying two permutations represents **function composition** evaluated **right-to-left**:

$$(f \cdot g)(x) = f(g(x))$$

To compute the product, take an element, evaluate where it goes under the right permutation first, and then follow that result through the left permutation.

### Identity Permutation ($e$)
The **identity permutation** (denoted as `$e$` in code) maps every element to itself and leaves the set unchanged:

$$p \cdot e = e \cdot p = p$$

---

## Order of a Permutation
The **order** of a permutation $p$ is the smallest positive integer $k > 0$ such that raising $p$ to the power of $k$ yields the identity permutation $e$:

$$p^k = e$$

For disjoint cycles $c_1, c_2, \dots, c_m$, the order is computed as the **Least Common Multiple (LCM)** of their cycle lengths:

$$\text{order}(p) = \text{lcm}(|c_1|, |c_2|, \dots, |c_m|)$$
