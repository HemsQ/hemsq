import itertools
import numpy as np


class Weight:
    def __init__(self,
            cost, # コスト項
            p, # 制約項の重み
            ineq, # B(t) <= B_max
        ):
        self._cost = cost
        self._p = p
        self._ineq = ineq

    @property
    def cost(self):
        return self._cost

    @property
    def p(self):
        return self._p

    @property
    def ineq(self):
        return self._ineq


class WeightStore:
    def __init__(self):
        self._store = {}

    def register(self,
            machine,
            cost=1.0, # コスト項
            p=1.0, # 制約項の重み
            ineq=1.0, # B(t) <= B_max
        ):

        def make_range(input):
            if isinstance(input, list) or isinstance(input, tuple):
                return np.arange(input[0], input[1], input[2])
            return [input]

        cost_range = make_range(cost)
        p_range = make_range(p)
        ineq_range = make_range(ineq)

        weights = []
        for cost, p, ineq in itertools.product(cost_range, p_range, ineq_range):
            weights.append(Weight(cost, p, ineq))

        self._store[machine] = weights

    def weights(self, machine):
        return self._store[machine]
