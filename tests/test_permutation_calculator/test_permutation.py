import pytest
from permutation_calculator import Permutation, Transposition, IDENTITY, Identity

class TestPermutationOutput:
    def test_permutation_repr_method(self):
        permutation = Permutation({1:2, 2:3, 3:1})
        hypo = "(1 2 3)"
        assert(hypo == permutation.__repr__())

    def test_permutation_str_method(self):
        permutation = Permutation({1:2, 2:3, 3:1})
        hypo = "(1 2 3)"
        assert(hypo == permutation.__str__())

    def test_IDENTITY_repr_method(self):
        hypo = "e"
        assert(hypo == IDENTITY.__repr__())
    
    def test_IDENTITY_str_method(self):
        hypo = "e"
        assert(hypo == IDENTITY.__str__())
    
    def test_permutation_to_cycles(self):
        permutation = Permutation({1:2, 2:3, 3:1})
        cycles = permutation.to_cycles()
        hypo = [[1,2,3]]
        assert(hypo == cycles)

    def test_disjoint_cycle_permutation__to_cycles(self):
        permutation = Permutation({1:2,2:3,3:1,4:5,5:4})
        cycles = permutation.to_cycles()
        hypo = [[1,2,3],[4,5]]
        assert(hypo == cycles)

    def test_permutation_repr_method_non_cycles(self):
        permutation = Permutation({1:2, 2:3, 3:1})
        permutation.USE_CYCLE_NOTATION = False
        hypo = "Permutation({1: 2, 2: 3, 3: 1})"
        assert(hypo == permutation.__repr__())

    def test_permutation_str_method_non_cycles(self):
        permutation = Permutation({1:2, 2:3, 3:1})
        permutation.USE_CYCLE_NOTATION = False
        hypo = "Permutation({1: 2, 2: 3, 3: 1})"
        assert(hypo == permutation.__str__())

    def test_IDENTITY_repr_method_non_cycles(self):
        IDENTITY.USE_CYCLE_NOTATION = False
        hypo = "e"
        assert(hypo == IDENTITY.__repr__())

    def test_IDENTITY_str_method_non_cycles(self):
        IDENTITY.USE_CYCLE_NOTATION = False
        hypo = "e"
        assert(hypo == IDENTITY.__str__())


class TestPermutationLogic:
    def test_equality_method(self):
        permutation = Permutation({1:2, 2:3, 3:1})
        assert(permutation == permutation)

    def test_identity_equality(self):
        assert(IDENTITY == IDENTITY)

    def test_identity_times_identity(self):
        product = IDENTITY*IDENTITY
        assert(product == IDENTITY)

    def test_identity_rtimes_permutation(self):
        permutation = Permutation({1:2,2:3,3:1})
        product = permutation * IDENTITY
        assert(product == permutation)

    def test_identity_ltimes_permutation(self):
        permutation = Permutation({1:2,2:3,3:1})
        product = IDENTITY * permutation
        assert(product == permutation)

    def test_non_disjoint_permutation_mult(self):
        permutation1 = Permutation({1:2,2:3, 3:1})
        permutation2 = Permutation({1:2,2:4, 4:1})
        product = permutation1 * permutation2
        hypo = Permutation({1:3, 3:1, 2:4, 4:2})
        assert(product == hypo)

    def test_disjoint_permutation_mult(self):
        permutation1 = Permutation({1:2, 2:3, 3:1})
        permutation2 = Permutation({4:5,5:4})
        product = permutation1 * permutation2
        hypo = Permutation({1:2,2:3,3:1,4:5,5:4})
        assert(hypo == product)

    def test_inverse_permutation(self):
        permutation = Permutation({1:2, 2:3, 3:1})
        inv = permutation.inverse()
        hypo = Permutation({1:3, 3:2, 2:1})
        assert(inv == hypo)

    def test_inverse_IDENTITY(self):
        inv = IDENTITY.inverse()
        assert(inv == IDENTITY)

    def test_permutation_and_inverse_mult(self):
        permutation = Permutation({1:2, 2:3, 3:1})
        inv = permutation.inverse()
        product = permutation*inv
        assert(product == IDENTITY)

    def test_permutation_order(self):
        permutation = Permutation({1:2, 2:3, 3:1})
        hypo = 3
        order = permutation.order()
        assert(hypo == order)

    def test_identity_order(self):
        hypo = 1
        order = IDENTITY.order()
        assert(hypo == order)

class TestPermutationEvaluationAndInit:
    def test_call_method_mapped_and_unmapped(self):
        permutation = Permutation({1: 2, 2: 3, 3: 1})
        assert(permutation(1) == 2)
        assert(permutation(2) == 3)
        assert(permutation(99) == 99)

    def test_init_strips_fixed_points(self):
        permutation = Permutation({1: 1, 2: 3, 3: 2})
        hypo = {2: 3, 3: 2}
        assert(hypo == permutation.mapping)

    def test_init_empty_or_none(self):
        permutation_empty = Permutation({})
        permutation_none = Permutation(None)
        hypo = {}
        assert(hypo == permutation_empty.mapping)
        assert(hypo == permutation_none.mapping)

    def test_order_lcm_multiple_disjoint_cycles(self):
        permutation = Permutation({1: 2, 2: 1, 3: 4, 4: 5, 5: 3})
        hypo = 6
        assert(hypo == permutation.order())

    def test_permutation_init_none_or_empty(self):
        permutation_default = Permutation()
        permutation_none = Permutation(None)
        assert(permutation_default.mapping == {})
        assert(permutation_none.mapping == {})

class TestTranspositionLogic:
    def test_valid_transposition(self):
        transposition = Transposition(1, 2)
        hypo_mapping = {1: 2, 2: 1}
        hypo_cycles = [[1, 2]]
        hypo_order = 2
        assert(hypo_mapping == transposition.mapping)
        assert(hypo_cycles == transposition.to_cycles())
        assert(hypo_order == transposition.order())

    def test_transposition_self_inverse(self):
        transposition = Transposition(1, 3)
        product = transposition * transposition
        assert(product == IDENTITY)

    def test_transposition_identical_indices_raises_value_error(self):
        with pytest.raises(ValueError, match="Indices must be distinct"):
            Transposition(2, 2)

class TestPermutationEdgeCasesAndTypes:
    def test_hash_equality_and_set_membership(self):
        permutation1 = Permutation({1: 2, 2: 1})
        permutation2 = Permutation({1: 2, 2: 1})
        assert(hash(permutation1) == hash(permutation2))

        permutation_set = {permutation1, IDENTITY}
        assert(permutation2 in permutation_set)

    def test_equality_with_non_permutation_type(self):
        permutation = Permutation({1: 2, 2: 1})
        assert((permutation == "not_a_permutation") is False)
        assert((permutation == 42) is False)

    def test_invalid_multiplication_raises_type_error(self):
        permutation = Permutation({1: 2, 2: 1})
        with pytest.raises(TypeError):
            _ = permutation * "invalid_operand"

        with pytest.raises(TypeError):
            _ = IDENTITY * 10

    def test_identity_singleton_existing_instance(self):
        second_identity = Identity()
        assert(second_identity is IDENTITY)

class TestPermutationMissingBranches:
    def test_identity_mul_invalid_type(self):
        with pytest.raises(TypeError):
            _ = IDENTITY * "invalid_type"

    def test_identity_rmul_direct_and_invalid(self):
        assert(IDENTITY.__rmul__("invalid_type") == NotImplemented)

    def test_empty_permutation_order_branch(self):
        permutation = Permutation({})
        hypo = 1
        assert(hypo == permutation.order())

    def test_empty_permutation_repr_non_cycle_branch(self):
        permutation = Permutation({})
        permutation.USE_CYCLE_NOTATION = False
        hypo = "Permutation({})"
        assert(hypo == permutation.__repr__())

    def test_empty_permutation_repr_cycle_notation(self):
        permutation = Permutation({})
        hypo = "e"
        assert(hypo == permutation.__repr__())