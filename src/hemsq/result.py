class Data:
    def __init__(self,
            name,
            data,
            tani,
            color,
            dtype='int64',
        ):
        self._name = name
        self._data = data
        self._tani = tani
        self._color = color
        self._name_with_tani = '{} ({})'.format(name, tani)
        self._dtype = dtype

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

    @property
    def dtype(self):
        return self._dtype


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
    x_ticks = [str((i+sp.start_time) % 24) for i in list(range(sp.output_len))]
    return {
        'sp': sp,
        'x_ticks': x_ticks,
        'demand':
            Data('Demand', demand_list, 'W', 'gray'),
        'sun_gen':
            Data('Solar Power Generation', sun_gen_list, 'W', 'lightgray'),
        'cost_ele':
            Data('Commercial Electricity Prices', cost_ele_list, 'yen/W',
                 'midnightblue', dtype='float64'),
        'sun_sell_price':
            Data('Solar-Sell Prices', sun_sell_price_list, 'yen/W', '',
                 dtype='float64'),
        'sun_use':
            Data('Use of Solar Power', sun_use_list, 'W', 'coral'),
        'sun_charge':
            Data('Charge of Solar Power', sun_charge_list, 'W', 'gold'),
        'sun_sell':
            Data('Sales of Solar Power', sun_sell_list, 'W', 'aqua'),
        'bat_out':
            Data('Use of Battery Electricity', bat_out_list, 'W',
                 'deepskyblue'),
        'ele_use':
            Data('Use of Commercial Electricity', ele_use_list, 'W',
                 'limegreen'),
        'ele_charge':
            Data('Charge of Commercial Electricity', ele_charge_list, 'W',
                 'pink'),
        'bat':
            Data('Remaining amount of Battery', bat_list, 'W', 'mediumpurple'),
    }
