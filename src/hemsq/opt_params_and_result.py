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
    def result_sche(self):
        return self._result_sche

    @property
    def output_sche(self):
        return self._output_sche
