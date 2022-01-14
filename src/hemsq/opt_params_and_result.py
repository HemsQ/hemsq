class OptParamsAndResult:
    def __init__(self,
            sp=None,
            normalize_rate=None,
            sche_times=None,
            D_all=None,
            Sun_all=None,
            C_ele_all=None,
            C_sun_all=None,
            D_op=None,
            Sun_op=None,
            C_ele_op=None,
            C_sun_op=None,
            rotated_demand=None,
            rotated_sun=None,
            rotated_c_ele=None,
            rotated_c_sun=None,
            result_sche=None,
            output_sche=None,
        ):
        self._sp = sp
        self._normalize_rate = normalize_rate
        self._sche_times = sche_times
        self._D_all = D_all
        self._Sun_all = Sun_all
        self._C_ele_all = C_ele_all
        self._C_sun_all = C_sun_all
        self._D_op = D_op
        self._Sun_op = Sun_op
        self._C_ele_op = C_ele_op
        self._C_sun_op = C_sun_op
        self._rotated_demand = rotated_demand
        self._rotated_sun = rotated_sun
        self._rotated_c_ele = rotated_c_ele
        self._rotated_c_sun = rotated_c_sun
        self._result_sche = result_sche
        self._output_sche = output_sche

    def set_sp(self, sp):
        self._sp = sp

    def set_normalize_rate(self, normalize_rate):
        self._normalize_rate = normalize_rate

    def set_sche_times(self, sche_times):
        self._sche_times = sche_times

    def set_D_all(self, D_all):
        self._D_all = D_all

    def set_Sun_all(self, Sun_all):
        self._Sun_all = Sun_all

    def set_C_ele_all(self, C_ele_all):
        self._C_ele_all = C_ele_all

    def set_C_sun_all(self, C_sun_all):
        self._C_sun_all = C_sun_all

    def set_D_op(self, D_op):
        self._D_op = D_op

    def set_Sun_op(self, Sun_op):
        self._Sun_op = Sun_op

    def set_C_ele_op(self, C_ele_op):
        self._C_ele_op = C_ele_op

    def set_C_sun_op(self, C_sun_op):
        self._C_sun_op = C_sun_op

    def set_rotated_demand(self, rotated_demand):
        self._rotated_demand = rotated_demand

    def set_rotated_sun(self, rotated_sun):
        self._rotated_sun = rotated_sun

    def set_rotated_c_ele(self, rotated_c_ele):
        self._rotated_c_ele = rotated_c_ele

    def set_rotated_c_sun(self, rotated_c_sun):
        self._rotated_c_sun = rotated_c_sun

    def set_result_sche(self, result_sche):
        self._result_sche = result_sche

    def set_output_sche(self, output_sche):
        self._output_sche = output_sche

    @property
    def sp(self):
        return self._sp

    @property
    def normalize_rate(self):
        return self._normalize_rate

    @property
    def sche_times(self):
        return self._sche_times

    @property
    def D_all(self):
        return self._D_all

    @property
    def Sun_all(self):
        return self._Sun_all

    @property
    def C_ele_all(self):
        return self._C_ele_all

    @property
    def C_sun_all(self):
        return self._C_sun_all

    @property
    def D_op(self):
        return self._D_op

    @property
    def Sun_op(self):
        return self._Sun_op

    @property
    def C_ele_op(self):
        return self._C_ele_op

    @property
    def C_sun_op(self):
        return self._C_sun_op

    @property
    def rotated_demand(self):
        return self._rotated_demand

    @property
    def rotated_sun(self):
        return self._rotated_sun

    @property
    def rotated_c_ele(self):
        return self._rotated_c_ele

    @property
    def rotated_c_sun(self):
        return self._rotated_c_sun

    @property
    def result_sche(self):
        return self._result_sche

    @property
    def output_sche(self):
        return self._output_sche
