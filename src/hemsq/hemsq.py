from .situation_params import SituationParams


class HemsQ:
    def __init__(self):
        """
        初期化関数.
        """
        # パラメタ
        self._sp = SituationParams()


    def set_params(self):
        """
        パラメータを設定する.
        """
        pass

    def set_client(self, client):
        """
        マシンの Client を設定する.
        Args:
          client: An object defined in amplify.client.
        """
        pass

    def solve(self):
        pass

    def show_info(self):
        pass

    def show_schedule(self):
        pass

    def show_solar_balance(self):
        pass

    def show_supply_and_demand(self):
        pass

    def show_money_graph(self):
        pass

    def show_all(self):
        self.show_info()
        self.show_schedule()
        self.show_solar_balance()
        self.show_supply_and_demand()
        self.show_money_graph()
