from itertools import combinations, permutations

# An abstraction for a factor
class factor:
    def __init__(self,val):
        self.val = val

# An example aggreation rule that adds up all factors
# Note: this rule can be path-dependent, although my example is path-independent
def aggregate(factors):
    return sum([factor.val for factor in factors])

# Using the Shapley decomposition rule, determine the contribution of a specific factor
def decompose(factor, factors, aggregaion_rule):
    factors_indices = list(range(len(factors)))
    del factors_indices[factors.index(factor)]
    count = 0
    total = 0
    for i in range(len(factors)):
        for comb in combinations(factors_indices, i):
            for path in permutations(comb):
                print(str(count) + ": evaluating path: " + str(path))
                f = [factors[p] for p in path]
                total = total + aggregate([factor] + f) - aggregate(f)
                count = count + 1
    return total / count

# A quick test
factor_A = factor(5)
factor_B = factor(23)
factor_C = factor(7)
factor_D = factor(99)
factor_E = factor(10)
factor_F = factor(51)
factor_G = factor(32)
factor_H = factor(97)
factor_I = factor(40)
factor_J = factor(30)
l = [factor_A, factor_B, factor_C, factor_D, factor_E, factor_F, factor_G]#, factor_H, factor_I, factor_J]
print("Total: " + str(aggregate(l)))
print("This factor's contribution: " + str(decompose(factor_C, l, aggregate)))