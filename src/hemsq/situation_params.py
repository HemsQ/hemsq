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

        # 実際の定格出力 (W) (1時間あたりに貯められる量)
        self._actual_rated_capa = 2000

        # 経費コストと環境コストの比率(ここでは1:1)
        self._cost_ratio = 1.0

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

        self._client = None

    def set_unit(self, unit):
        self._unit = unit
    
    def set_actual_b_max(self, actual_b_max):
        self._actual_b_max = actual_b_max

    def set_actual_b_0(self, actual_b_0):
        self._actual_b_0 = actual_b_0

    def set_actual_rated_capa(self, actual_rated_capa):
        self._actual_rated_capa = actual_rated_capa

    def set_cost_ratio(self, cost_ratio):
        self._cost_ratio = cost_ratio

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

    def set_client(self, client):
        self._client = client

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
    def actual_rated_capa(self):
        return self._actual_rated_capa

    @property
    def cost_ratio(self):
        return self._cost_ratio

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
    def client(self):
        return self._client

    def reset_params(self):
        """
        ユーザーが指定した client を除くパラメタをデフォルト値に戻す
        """
        client = self._client
        self.__init__()
        self.set_client(client)
