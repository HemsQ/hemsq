class Data:
    def __init__(self,
            name,
            data,
            tani,
            color,
        ):
        self._name = name
        self._data = data
        self._tani = tani
        self._color = color
        self._name_with_tani = '{} ({})'.format(name, tani)

    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    @property
    def tani(self):
        return self._tani

    @property
    def color(self):
        return self._color

    @property
    def name_with_tani(self):
        return self._name_with_tani


def make_result(
        sp,
        demand_list,
        sun_gen_list,
        cost_ele_list,
        sun_sell_price_list,
        sun_use_list,
        sun_charge_list,
        sun_sell_list,
        bat_out_list,
        ele_use_list,
        ele_charge_list,
        bat_list,
    ):
    return {
        'sp': sp,
        'demand':
            Data('Demand', demand_list, 'W', 'gray'),
        'sun_gen':
            Data('Solar Power Generation', sun_gen_list, 'W', 'black'),
        'cost_ele':
            Data('Commercial Electricity Prices', cost_ele_list, 'yen', 'red'),
        'sun_sell_price':
            Data('Solar-Sell Prices', sun_sell_price_list, 'yen', 'green'),
        'sun_use':
            Data('Use of Solar Power', sun_use_list, 'W', 'orangered'),
        'sun_charge':
            Data('Charge of Solar Power', sun_charge_list, 'W', 'orange'),
        'sun_sell':
            Data('Sales of Solar Power', sun_sell_list, 'W', 'blue'),
        'bat_out':
            Data('Use of Battery Electricity', bat_out_list, 'W', 'deepskyblue'),
        'ele_use':
            Data('Use of Commercial Electricity', ele_use_list, 'W', 'limegreen'),
        'ele_charge':
            Data('Charge of Commercial Electricity', ele_charge_list, 'W', 'yellow'),
        'bat':
            Data('Remaining amount of Battery', bat_list, 'W', 'pink'),
    }


class OptParamsAndResult:
    def __init__(self,
            sp=None,
            normalize_rate=None,
            rotated_demand=None,
            rotated_sun=None,
            rotated_c_ele=None,
            rotated_c_sun=None,
            output_sche=None,
        ):
        self._sp = sp
        self._normalize_rate = normalize_rate
        self._rotated_demand = rotated_demand
        self._rotated_sun = rotated_sun
        self._rotated_c_ele = rotated_c_ele
        self._rotated_c_sun = rotated_c_sun
        self._output_sche = output_sche

    def set_sp(self, sp):
        self._sp = sp

    def set_normalize_rate(self, normalize_rate):
        self._normalize_rate = normalize_rate

    def set_rotated_demand(self, rotated_demand):
        self._rotated_demand = rotated_demand

    def set_rotated_sun(self, rotated_sun):
        self._rotated_sun = rotated_sun

    def set_rotated_c_ele(self, rotated_c_ele):
        self._rotated_c_ele = rotated_c_ele

    def set_rotated_c_sun(self, rotated_c_sun):
        self._rotated_c_sun = rotated_c_sun

    def set_output_sche(self, output_sche):
        self._output_sche = output_sche

    @property
    def sp(self):
        return self._sp

    @property
    def normalize_rate(self):
        return self._normalize_rate

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
    def output_sche(self):
        return self._output_sche
