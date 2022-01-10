class OptParamsAndResult:
    def __init__(self,
            sp,
            client,
            normalize_rate,
            sche_times,
            D_all,
            Sun_all,
            C_ele_all,
            C_sun_all,
            result_sche,
        ):
        self._sp = sp
        self._client = client
        self._normalize_rate = normalize_rate
        self._sche_times = sche_times
        self._D_all = D_all
        self._Sun_all = Sun_all
        self._C_ele_all = C_ele_all
        self._C_sun_all = C_sun_all
        self._result_sche = result_sche

    @property
    def sp(self):
        return self._sp

    @property
    def client(self):
        return self._client

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
    def result_sche(self):
        return self._result_sche
