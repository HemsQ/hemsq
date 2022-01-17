class OptParamsAndResult:
    def __init__(self,
            sp=None,
            normalize_rate=None,
            sche_times=None,
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
