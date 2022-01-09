from .situation_params import SituationParams


class HemsQ:
    def __init__(self):
        """
        初期化関数.
        """
        # パラメタ
        self._sp = SituationParams()


    def set_params(self,
            unit=None,
            battery_capacity=None,
            initial_battery_amount=None,
            b_in=None,
            b_out=None,
            eta=None,
            conv_eff=None,
            rated_output=None,
            cost_ratio=None,
            c_env=None,
            start_time=None,
            step=None,
            output_len=None,
            reschedule_span=None,
            weather_list=None,
            demand_list=None,
        ):
        """
        パラメータを設定する.
        """
        if unit:
            self._sp.set_unit(unit)
        if battery_capacity:
            self._sp.set_actual_b_max(battery_capacity)
        if initial_battery_amount:
            self._sp.set_actual_b_0(initial_battery_amount)
        if b_in:
            self._sp.set_b_in(b_in)
        if b_out:
            self._sp.set_b_out(b_out)
        if eta:
            self._sp.set_eta(eta)
        if conv_eff:
            self._sp.set_conv_eff(conv_eff)
        if rated_output:
            self._sp.set_actual_rated_capa(rated_output)
        if cost_ratio:
            self._sp.set_cost_ratio(cost_ratio)
        if c_env:
            self._sp.set_c_env(c_env)
        if start_time:
            self._sp.set_start_time(start_time)
        if step:
            self._sp.set_step(step)
        if output_len:
            self._sp.set_output_len(output_len)
        if reschedule_span:
            self._sp.set_resche_span(reschedule_span)
        if weather_list:
            self._sp.set_tenki(weather_list)
        if demand_list:
            self._sp.set_demand(demand_list)

    @property
    def params(self):
        return self._sp.all_params

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
