import copy
import math

import numpy as np
from amplify import (
    BinarySymbolGenerator,
    Solver,
)

from .situation_params import SituationParams
from .amp import make_qubo_amp as mqa
from .result import make_result
from .sub import *

class HemsQ:
    def __init__(self):
        """
        初期化関数.
        """
        # パラメタ
        self._sp = SituationParams()
        # マシンのクライアント
        self._client = None
        # 結果を格納するリスト
        self._results = []

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
            sell_price=None,
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
        if unit != None:
            self._sp.set_unit(unit)
        if battery_capacity != None:
            self._sp.set_actual_b_max(battery_capacity)
        if initial_battery_amount != None:
            self._sp.set_actual_b_0(initial_battery_amount)
        if b_in != None:
            self._sp.set_b_in(b_in)
        if b_out != None:
            self._sp.set_b_out(b_out)
        if eta != None:
            self._sp.set_eta(eta)
        if conv_eff != None:
            self._sp.set_conv_eff(conv_eff)
        if rated_output != None:
            self._sp.set_actual_rated_capa(rated_output)
        if cost_ratio != None:
            self._sp.set_cost_ratio(cost_ratio)
        if c_env != None:
            self._sp.set_c_env(c_env)
        if sell_price != None:
            self._sp.set_sell_price(sell_price)
        if start_time != None:
            self._sp.set_start_time(start_time)
        if step != None:
            self._sp.set_step(step)
        if output_len != None:
            self._sp.set_output_len(output_len)
        if reschedule_span != None:
            self._sp.set_resche_span(reschedule_span)
        if weather_list != None:
            self._sp.set_tenki(weather_list)
        if demand_list != None:
            self._sp.set_demand(demand_list)

    def reset_params(self):
        self._sp.reset_params()

    @property
    def params(self):
        return self._sp.all_params

    def set_client(self, client):
        """
        マシンの Client を設定する.
        Args:
          client: An object defined in amplify.client.
        """
        self._client = client

    def solve(self):
        sp = self._sp
        sp.validate()
        
        #制約の重み
        w_cost = 1.0 #コスト項
        w_d=1.0 #需要と供給のバランス
        w_a=1.0 #項目は一つ割り当てる 
        w_io=1.0 #蓄電池の入出力は同時にしない
        w_s=1.0 #太陽光の収支を合わせる
        normalize_rate = 0.01 #正規化何倍
        sche_times = math.ceil(sp.output_len / sp.resche_span) #何回組み直すか
        result_sche = [] #スケジュールを追加するリスト
        D_all = rounding(sp.demand, sp.unit)
        solar_by_weather = make_sun_by_weather(sp.solar_data, sp.tenki)
        Sun_all = rounding(solar_by_weather, sp.unit)
        C_ele_all = normalize(sp.ele_prices, normalize_rate * sp.unit / 1000)
        C_sun_all = normalize([sp.sell_price] * 24, normalize_rate * sp.unit / 1000)
        
        # 出力するデータの作成
        start = sp.start_time
        end = sp.start_time + sp.output_len - 1
        rotated_demand = rotate(start, end, sp.demand)
        rotated_sun = rotate(start, end, solar_by_weather)
        rotated_c_ele = rotate(start, end, sp.ele_prices)
        rotated_c_sun = rotate(start, end, [sp.sell_price] * 24)

        B_0 = int(sp.actual_b_0 / sp.unit)
        B_max = int(sp.actual_b_max / sp.unit)
        rated_capa = int(sp.actual_rated_capa / sp.unit)
        y_n = math.floor(math.log2(B_max-1))+1 #不等式のスラック変数の数
        for t in range(sche_times):
            energy_lst = [] #パラメタ調整用(energy)
            weight_lst = [] #パラメタ調整用(w_p,w_ineq1,w_ineq2）
            all_sche = [] #パラメタ調整用(制約を破る・破らないに関わらず全てのスケジュールをここに入れる）
            if t != 0:
                B_0 = int(my_round(result_sche[t-1][-1][-1])) #前のスケジュール作成の時の蓄電量
            resche_start = sp.start_time + sp.resche_span * t #リスケ開始時間
            #入力（太陽光・需要・料金）について組み直し開始時間からstep時間分だけ用意する    
            start = resche_start % 24
            end = (resche_start + sp.step-1) % 24
            D_t = rotate(start, end, D_all)
            Sun_t = rotate(start, end, Sun_all)
            C_ele_t = rotate(start, end, C_ele_all)
            C_sun_t = rotate(start, end, C_sun_all)
            komoku_grp = komokuGroup(D_t, Sun_t, rated_capa, sp.step) #項目の数を決める
            komoku, total = newKomokuProduce(komoku_grp) #項目を作る
            gen = BinarySymbolGenerator()  # BinaryPoly の変数ジェネレータを宣言
            q1 = gen.array(total * sp.step)  # 決定変数xの Binary 配列を生成
            q2 = gen.array(y_n * sp.step)  # スラック変数yの Binary 配列を生成
            #使わない変数を固定
            fix_lst = disuse(komoku_grp, B_0, B_max, D_t, sp.step, [])
            for i in fix_lst:
                q1[i] = 0
            #多項式(f:コスト項,g:制約項,h1:B(t)<=B_max,h2:0<=B(t))
            c = mqa.cost_term(sp.step, total, komoku, sp.cost_ratio,\
                             sp.conv_eff, C_ele_t, C_sun_t, sp.c_env, q1)
            p = mqa.penalty_term(sp.step, total, komoku, sp.cost_ratio,\
                            sp.conv_eff, D_t, Sun_t, w_a, w_io, w_d, w_s, q1)
            ineq1 = mqa.ineq(q1, q2, sp.step, total, komoku,\
                                    sp.eta, sp.b_in, sp.b_out, B_max, B_0, y_n)
            for w_p in np.arange(4.0, 2.5, -0.1): #制約項の重み
                for w_ineq2 in np.arange(1.1, 1.6, 0.1): #0<=B(t)の重み
                    for w_ineq1 in np.arange(1.1, 1.6, 0.1): #B(t)<=B_max
                        #多項式を重みをかけて足し合わす
                        Q = c * w_cost + p * w_p + ineq1 * w_ineq1
                        # ソルバの実行
                        solver = Solver(self._client)
                        result = solver.solve(Q)
                        #結果の取得
                        for solution in result:
                            sample = solution.values
                            break
                        sample0 = dict(sorted(sample.items(), key=lambda x:x[0])[:-len(q2)])
                        #一つの項目が割り当てられる時間は一枠・opt_result取得
                        alloc_satisfied, opt_result = check_alloc(sp.step, sample0, {})
                        #組み直し時間までの結果
                        schedule = makeSchedule(opt_result, sp.step, total, komoku, B_0, sp.eta) 
                        #破った制約を追加する
                        broken_lst = constraint(schedule, Sun_t, D_t, B_max, alloc_satisfied)
                        #重みを追加
                        weight_lst.append([w_p, w_ineq1, w_ineq2])        
                        # print('[w_p,w_ineq1,w_ineq2]:', weight_lst[-1],'\n[broken constraints] :', broken_lst)
                        if not broken_lst:
                            result_sche.append([schedule[j][0: sp.resche_span] for j in range(7)])  
                            # print('success! resche time :', resche_start)
                            # print('[w_p,w_ineq1,w_ineq2]:',weight_lst[-1],'\n[broken constraints]:',broken_lst)
                            break #満たす解があればfor文を抜ける
                    if not broken_lst:
                        break #満たす解があればfor文を抜ける
                if not broken_lst:
                    break #満たす解があればfor文を抜ける
            if broken_lst:
                print('not found time:', resche_start) #満たす解がないのであれば終了する
                break
        print('Done!')

        # 結果の保存
        output_sche = make_output_sche(result_sche, sche_times, sp.output_len)
        unitdoubled_output_sche = unitDouble(output_sche, sp.unit)
        postprocessed_output_sche =\
            post_process(unitdoubled_output_sche, rotated_sun, rotated_demand, sp.output_len)
        result = make_result(
            sp,
            rotated_demand,
            rotated_sun,
            rotated_c_ele,
            rotated_c_sun,
            postprocessed_output_sche[0],
            postprocessed_output_sche[1],
            postprocessed_output_sche[2],
            postprocessed_output_sche[3],
            postprocessed_output_sche[4],
            postprocessed_output_sche[5],
            list(map(lambda x: my_round(x), postprocessed_output_sche[6])),
        )
        self._results.append(result)

    def cost_dict(self, result=None):
        if result == None:
            result = self._results[-1]
        return cost(result)

    def show_cost(self, result=None):
        if result == None:
            result = self._results[-1]
        val = self.cost_dict(result)
        # コスト
        if val['cost'] >= 0:
            print("Cost:", val['cost'], "(yen)")
        else:
            print("Sales: ", -val['cost'], "(yen)")
        # CO2排出量（0.445kg/kWh)
        print("CO2 Emissions:", val['CO2'], "kg")

    def all_table_fig(self, result=None):
        if result == None:
            result = self._results[-1]
        return make_all_table_fig(result)

    def all_table_df(self, result=None):
        if result == None:
            result = self._results[-1]
        return make_all_table_df(result)

    def show_all_schedule(self, result=None):
        if result == None:
            result = self._results[-1]
        fig, ax = self.all_table_fig(result=result)
        plt.show()

    def demand_graph(self, result=None):
        if result == None:
            result = self._results[-1]
        return plot_demand(result)

    def show_demand(self, result=None):
        if result == None:
            result = self._results[-1]
        fig, ax = self.demand_graph(result=result)
        plt.show()

    def solar_graph(self, result=None):
        if result == None:
            result = self._results[-1]
        return plot_solar(result)

    def show_solar(self, result=None):
        if result == None:
            result = self._results[-1]
        fig, ax = self.solar_graph(result=result)
        plt.show()

    def cost_and_charge_graph(self, result=None):
        if result == None:
            result = self._results[-1]
        return plot_cost_charge(result)

    def show_cost_and_charge(self, result=None):
        if result == None:
            result = self._results[-1]
        fig, ax = self.cost_and_charge_graph(result=result)
        plt.show()

    def cost_and_use_graph(self, result=None):
        if result == None:
            result = self._results[-1]
        return plot_cost_use(result)

    def show_cost_and_use(self, result=None):
        if result == None:
            result = self._results[-1]
        fig, ax = self.cost_and_use_graph(result=result)
        plt.show()

    def show_all(self, result=None):
        if result == None:
            result = self._results[-1]
        self.show_cost(result=result)
        self.show_all_schedule(result=result)
        self.show_demand(result=result)
        self.show_solar(result=result)
        self.show_cost_and_charge(result=result)
        self.show_cost_and_use(result=result)
