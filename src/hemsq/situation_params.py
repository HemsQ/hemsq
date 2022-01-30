class SituationParams:
    def __init__(self):
        """
        初期化関数.
        """
        # 項目あたり電力量(W)
        self._unit = 100

        # 実際の貯蓄可能容量 (W)
        self._actual_b_max = 5000
        # 実際の初期蓄電量 actual_b_0 (W)
        self._actual_b_0 = 4500
        # 変換効率
        self._b_in = 0.95
        self._b_out = 0.95
        # 放電率
        self._eta = 0.05

        # 変換効率
        self._conv_eff = 1.0

        # 実際の定格出力 (W) (1時間あたりに貯められる量)
        self._actual_rated_capa = 2000

        # 経費コストと環境コストの比率(ここでは1:1)
        self._cost_ratio = 1.0
        # 環境コスト
        self._c_env = 0.5

        # 商用電源の価格
        self._ele_prices = list(map(lambda x: x / 1000, [12,12,12,12,12,12,12,26,26,26,39,39,39,39,39,39,39,26,26,26,26,26,26,26]))

        # 太陽光の売電価格
        self._sell_price = 0.008
        #1kWの太陽光パネル・快晴・9月
        self._solar_data = [0,0,0,0,0,0,0,100,300,500,600,700,700,700,600,500,400,200,0,0,0,0,0,0]

        # 何時からのスケジュールを作るか
        self._start_time = 0
        # 何時間先まで見てスケジュール作るか
        self._step = 12
        # 何時間のスケジュールを作るか
        self._output_len = 24
        # 何時間ごとに組み直すか
        self._resche_span = 6

        # 天気パターン
        self._tenki = ['r' for i in range(8)]
        # 需要パターン
        self._demand = [207,177,147,157,157,167,228,330,381,391,351,311,341,341,311,310,320,331,372,542,549,509,438,318]

    def validate(self):
        if self._step < self._resche_span:
            self._resche_span = self._step
            print('Set `reschedule_span` to {} '
                'since it must be `step` or less.'.format(self._resche_span))

    def set_unit(self, unit):
        self._unit = unit
    
    def set_actual_b_max(self, actual_b_max):
        self._actual_b_max = actual_b_max

    def set_actual_b_0(self, actual_b_0):
        self._actual_b_0 = actual_b_0

    def set_b_in(self, b_in):
        self._b_in = b_in

    def set_b_out(self, b_out):
        self._b_out = b_out

    def set_eta(self, eta):
        self._eta = eta

    def set_conv_eff(self, conv_eff):
        self._conv_eff = conv_eff

    def set_actual_rated_capa(self, actual_rated_capa):
        self._actual_rated_capa = actual_rated_capa

    def set_cost_ratio(self, cost_ratio):
        self._cost_ratio = cost_ratio

    def set_c_env(self, c_env):
        self._c_env = c_env

    def set_ele_prices(self, ele_prices):
        self._ele_prices = ele_prices

    def set_sell_price(self, sell_price):
        self._sell_price = sell_price

    def set_solar_data(self, solar_data):
        self._solar_data = solar_data

    def set_start_time(self, start_time):
        self._start_time = start_time

    def set_step(self, step):
        self._step = step

    def set_output_len(self, output_len):
        self._output_len = output_len

    def set_resche_span(self, resche_span):
        self._resche_span = resche_span

    def set_tenki(self, tenki):
        self._tenki = tenki

    def set_demand(self, demand):
        self._demand = demand

    @property
    def unit(self):
        return self._unit
    
    @property
    def actual_b_max(self):
        return self._actual_b_max

    @property
    def actual_b_0(self):
        return self._actual_b_0

    @property
    def b_in(self):
        return self._b_in

    @property
    def b_out(self):
        return self._b_out

    @property
    def eta(self):
        return self._eta

    @property
    def conv_eff(self):
        return self._conv_eff

    @property
    def actual_rated_capa(self):
        return self._actual_rated_capa

    @property
    def cost_ratio(self):
        return self._cost_ratio

    @property
    def c_env(self):
        return self._c_env

    @property
    def ele_prices(self):
        return self._ele_prices

    @property
    def sell_price(self):
        return self._sell_price

    @property
    def solar_data(self):
        return self._solar_data

    @property
    def start_time(self):
        return self._start_time

    @property
    def step(self):
        return self._step

    @property
    def output_len(self):
        return self._output_len

    @property
    def resche_span(self):
        return self._resche_span

    @property
    def tenki(self):
        return self._tenki

    @property
    def demand(self):
        return self._demand
    
    @property
    def all_params(self):
        return {
            "unit": self._unit,
            "battery_capacity": self._actual_b_max,
            "initial_battery_amount": self._actual_b_0,
            "b_in": self._b_in,
            "b_out": self._b_out,
            "eta": self._eta,
            "conv_eff": self.conv_eff,
            "rated_output": self._actual_rated_capa,
            "cost_ratio": self._cost_ratio,
            "c_env": self._c_env,
            "electricity prices": self._ele_prices,
            "sell_price": self._sell_price,
            "solar_generation_data": self._solar_data,
            "start_time": self._start_time,
            "step": self._step,
            "output_len": self.output_len,
            "reschedule_span": self._resche_span,
            "weather_list": self._tenki,
            "demand_list": self._demand,
        }

    def reset_params(self):
        """
        パラメタをデフォルト値に戻す
        """
        self.__init__()
