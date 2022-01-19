import itertools
from operator import itemgetter

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#データの正規化
def normalize(data, normalize_rate):
    def f(x):
        return x*normalize_rate    
    return list(map(f,data))


#三時間毎の天気予報を入れると太陽光の発電量を計算してくれて返す
def Weather3hours(tenki, sun):
    #発電量を曇りは1/3倍、雨雪は1/5倍でリストを返す
    def Weather(weather, lst):
        l = [0] * len(lst)
        if weather != 's':#曇りor雨or雪
            for i in range(len(lst)):            
                if weather == 'c':
                    l[i] = int(my_round(lst[i]/3))
                else:
                    l[i] = int(my_round(lst[i]/5))
        else:
            l = lst
        return l
    lst = [Weather(tenki[i], sun[i*3: (i+1)*3]) for i in range(len(tenki))]
    return list(itertools.chain.from_iterable(lst))


#四捨五入する関数
def my_round(val, digit=0):
    p = 10 ** digit
    rounded = (val * p * 2 + 1) // 2 / p
    return int(rounded) if digit == 0 else rounded


#リストを途中から一周する関数
def rotate(start, end, lst):
    l = len(lst)
    nlst = [0] * l
    for i in range(l):
        if start + i < l:    
            nlst[i] = lst[start + i]
        else:
            nlst[i] = lst[start + i - l]        
    nlst = nlst[:end + 1 - start]
    return nlst


# 天気による太陽光発電量の算出
def make_sun_by_weather(solar_data, tenki):
    # 通常の家の発電量
    solar_at_home = normalize(solar_data, 2)
    # 天気で発電量を調整する
    solar_by_weather = Weather3hours(tenki, solar_at_home)
    return solar_by_weather


# リストを四捨五入してカードにする
def rounding(lst, unit):
    # unitで割って
    lst1 = list(normalize(lst, 1 / unit))
    # 小数点を四捨五入
    lst2 = [int(my_round(lst1[i], 0)) for i in range(len(lst1))]
    return lst2


#項目の各種類で必要な数が入ったリストを作る
def komokuGroup(D, Sun, rated_capa, step):
    lst = [0]*6
    #太陽光(sun_sell,sun_use,sun_in)の数
    for i in range(1,4):
        lst[i] = sum(Sun[:step])
    #蓄電池使う(bat_out)の数
    lst[0] = sum(D[:step])
    #商用電源使う(ele_use)の数
    lst[4] = sum(D[:step])
    #商用電源貯める(ele_in)の数
    lst[5] = rated_capa
    return lst


#項目を用意する関数
def newKomokuProduce(grp_lst):
    index = 0
    total = sum(grp_lst)
    komoku = [0]*total
    for k in range(len(grp_lst)):
        for j in range(grp_lst[k]):
            if k == 0:
                komoku[index]=[index,'bat','out']
            elif k==1:
                komoku[index]=[index,'sun','sell']
            elif k==2:
                komoku[index]=[index,'sun','use']
            elif k==3:
                komoku[index]=[index,'sun','in']
            elif k==4:
                komoku[index]=[index,'ele','use']
            else:
                komoku[index]=[index,'ele','in']            
            index += 1    
    return komoku, total


#使わない変数のindexが入ったリストを返す
def disuse(komoku_grp, B_0, B_max, D, step, disuse_lst=[]):
    #蓄電池の項目を用意する（最初は初期蓄電量分だけ使えるようにする）
    def B_komoku(B_0, B_max, D):
        B_lst = [0] * step
        B_lst[0] = B_0
        for t in range(1, step):
            B_lst[t] = sum(D[:step])
        return B_lst
    for k in range(len(komoku_grp)):
        #蓄電池使うx
        if k == 0:
            lst = B_komoku(B_0, B_max, D)            
        else:
            break
        for t in range(step):
            disuse_len = komoku_grp[k] - lst[t] 
            for i in range(disuse_len):
                disuse_lst.append(step * (lst[t] + sum(komoku_grp[:k]) +i) + t)                
    return disuse_lst


#スケジュールをまとめる
def makeSchedule(opt_result, step, total, komoku, B_0, eta):
    schedule = [0] * step
    B = B_0 * (1 - eta)
    for t in range(step):
        #tごとの各項目数を計上するための辞書
        do = {'sun_use': 0, 'sun_in': 0, 'sun_sell': 0,\
              'bat_out': 0, 'ele_use': 0, 'ele_in': 0, 'bat':B}
        for i in range(total):
            #項目iが割り当てられていて
            if i in opt_result:
                #項目iの割り当てられたstepがtなら
                if opt_result[i] == t:
                    setsubi = komoku[i][1] #項目iの設備
                    kyodo = komoku[i][2] #項目iの挙動
                    if setsubi == 'sun':
                        if kyodo == 'use': #光使用
                            do['sun_use'] += 1
                        elif kyodo == 'in': #光充電                          
                            do['sun_in'] += 1
                            do['bat'] += 1
                        else: #光売電
                            do['sun_sell'] += 1
                    elif setsubi == 'bat': #蓄電池使用
                        do['bat_out'] += 1
                        do['bat'] -= 1
                    else:
                        if kyodo == 'use':#商用電源使用
                            do['ele_use'] += 1
                        else:             #商用電源充電　
                            do['ele_in'] += 1
                            do['bat'] += 1
        schedule[t] = list(do.values())
        B = int(do['bat'] * (1 - eta))
    #表作成の時のために転置しておく
    schedule = [list(x) for x in zip(*schedule)]
    return schedule


#制約alloc(項目iが割り当てられるのは1枠まで)を判断
def check_alloc(step, sample0, opt_result={}):
    satisfied = True
    for key, val in sample0.items():
        if val == 1:
            i = key // step            
            #項目iが既に割り当てられているなら、制約破り
            if i in opt_result:
                satisfied = False
            #まだ割り当てられていないならopt_result{ID:t}に追加
            else:
                t = key % step
                opt_result[i] = t
    #opt_resultが空なら
    if not opt_result:
        print('opt_resultが空')
        satisfied = False
    return satisfied, opt_result


#制約inout(蓄電池の入出力は同時にしない)を判断
def check_inout(array):
    satisfied = True 
    for t in range(len(array)):
        bat_in = array[t][1]+array[t][5] #太陽光貯める＋商用電源貯める
        bat_out = array[t][3] #蓄電池使う
        if bat_in * bat_out != 0:
            satisfied = False
    return satisfied


#制約demand(需要のバランス)をチェック
def demandBalancePerStep(array, D):
    satisfied = True
    for t in range(len(array)):
        supply = array[t][0] + array[t][3] + array[t][4]
        if supply != D[t]:
            satisfied = False
    return satisfied


#制約sun(太陽光のバランス)をチェック、上とほぼ同じ
def sunBalancePerStep(array, Sun):
    satisfied = True
    for t in range(len(array)):
        if sum(array [t][:3]) != Sun[t]:
            satisfied = False
            break
    return satisfied


#各時間において蓄電量が蓄電池容量を超えていないかを確認する
def batteryCapacity(array, B_max):
    satisfied = True
    for t in range(len(array)):
        B = array[t][6]
        if B < 0 or B > B_max:#蓄電量が負または容量を超えていたらだめ
            satisfied = False
    return satisfied


#！パラメタ調整用！(1/3追加)
#破った制約を追加したリストを返す
def constraint(schedule, Sun, D, B_max, satisfied):  
    schedule = np.array(schedule).T
    broken_lst = []
    if not satisfied:
        broken_lst.append('alloc')
    if not check_inout(schedule): 
        broken_lst.append('inout')
    if not demandBalancePerStep(schedule, D):
        broken_lst.append('demand')
    if not sunBalancePerStep(schedule, Sun):
        broken_lst.append('sun')
    if not batteryCapacity(schedule, B_max):
        broken_lst.append('battery')
    return broken_lst


#項目の電力単位にする
def unitDouble(schedule, unit):
    array = np.array(schedule).T
    array *= unit
    return (array.T).tolist()


#表を作る
def makeTable(start, data, labels, mode, output_len):
    if mode == 0:
        loc = 'lower center'
        data_name = 'input'
    else:
        loc = 'upper center'
        data_name = 'output'
    step_labels = [str((i+start)%24)+':00' for i in list(range(output_len))]  
    fig = plt.figure(dpi=200)    
    ax1 = fig.add_subplot(2, 1, 1)
    df0 = pd.DataFrame(data, index=labels, columns=step_labels)
    df0.applymap(my_round)
    df = df0.astype('int64')
    ax1.axis('off')
    ax1.table(cellText=df.values, colLabels=df.columns,
              rowLabels=df.index, loc=loc, fontsize=15)
    plt.show()

def plot_table(ax, result, items):
    step_lables = list(map(lambda x: x + ':00', result['x_ticks']))
    df = pd.DataFrame(columns=step_lables)
    for item in items:
        data = result[item]
        df.loc[data.name_with_tani] = pd.Series(data.data, dtype=data.dtype)
    ax.axis('off')
    ax.table(cellText=df.values, colLabels=df.columns,
             rowLabels=df.index, fontsize=15)

def make_all_table(result, figsize=None):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(2, 1, 1)
    items = ['demand', 'sun_gen', 'cost_ele', 'sun_sell_price', 'sun_use',
             'sun_charge', 'sun_sell', 'bat_out', 'ele_use', 'ele_charge',
             'bat']
    plot_table(ax, result, items)
    return fig, ax

def make2Table(opr):
    # demand = list(map(int, normalize(opr.D_op[:opr.sp.output_len], opr.sp.unit)))
    # sun = list(map(int, normalize(opr.Sun_op[:opr.sp.output_len], opr.sp.unit)))
    # cost = list(map(int, normalize(opr.C_ele_op[:opr.sp.output_len], 1000/opr.normalize_rate/opr.sp.unit)))
    demand = opr.rotated_demand
    sun = opr.rotated_sun
    cost = opr.rotated_c_ele
    label = [
        "Demand (w)",
        "Solar Power Generation (w)",
        "Commercial Electricity Prices (yen)",
    ]
    makeTable(opr.sp.start_time, [demand, sun, cost], label, 0, opr.sp.output_len)
    label = [
        "Use of Solar Power (w)",
        "Charge of Solar Power (w)",
        "Sales of Solar Power (w)",
        "Use of Battery Electricity (w)",
        "Use of Commercial Electricity (w)",
        "Charge of Commercial Electricity (w)",
        "Remaining amount of Battery (w)",
    ]
    makeTable(opr.sp.start_time, opr.output_sche, label, 1, opr.sp.output_len)  

#最適解でかかった経費コストを計上してプリント出力する
def costPrint(opr):
    array = np.array(opr.output_sche)
    cost = 0 # コストの合計
    e_cost = 0
    for t in range(opr.sp.output_len):
        # 商用電源使用は4行目
        from_ele = array[4][t] + array[5][t]
        cost += from_ele * opr.rotated_c_ele[t]
        e_cost += from_ele
        # 太陽光売電は2行目
        cost -= array[2][t] * opr.rotated_c_sun[t]
    # コスト正なら
    if cost >= 0:
        print("Cost:", cost, "(yen)")
    # 負なら
    else:
        print("Sales: ", -cost, "(yen)")
    # CO2排出量（0.445kg/kWh)
    CO2 = my_round(0.445 * e_cost / 1000, 1)
    print("CO2 Emissions:", CO2, "kg")


def set_title(ax, title):
    ax.set_title(title, fontsize=20)

def set_legend(ax, ax_right=None):
    if ax_right:
        hans1, labs1 = ax.get_legend_handles_labels()
        hans2, labs2 = ax_right.get_legend_handles_labels()
        ax.legend(hans1 + hans2, labs1 + labs2, loc="upper left",
                  bbox_to_anchor=(1.2, 1.0), fontsize=15)
    else:
        ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=18)

def set_ax(ax, xlabel, ylabel, ax_right=None, ylabel_right=''):
    if ax_right:
        ax_right.set_ylabel(ylabel_right, fontsize=18)
        ax_right.tick_params(axis='x', labelsize=15)
        ax_right.tick_params(axis='y', labelsize=15)
        y_min, y_max = ax_right.get_ylim()
        ax_right.set_ylim(y_min, y_max)
    ax.set_xlabel(xlabel, fontsize=18)
    ax.set_xticks([i * 3 for i in range(8)])
    ax.set_ylabel(ylabel, fontsize=18)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)

def set_y_ax_right(ax, name):
    ax.set_ylabel(name, fontsize=18)    
    ax.tick_params(axis='y', labelsize=15)
    y_min, y_max = ax.get_ylim()
    ax.set_ylim(y_min, y_max)

def plot_bar(ax, result, items, is_left=False):
    barvalues = []
    for item in items:
        barvalues.append(result[item].data)
    np_barvalues = np.array(barvalues)
    ymax = max(np.sum(np_barvalues, axis=0))
    ax.set_ylim(0, ymax + 10)
    width = 0.3
    if is_left:
        width *= -1
    for i, item in enumerate(items):
        data = result[item]
        ax.bar(result['x_ticks'], data.data, width=width,
               align='edge', bottom=np.sum(np_barvalues[:i], axis=0),
               color=data.color, label=data.name_with_tani)

def plot_line(ax, result, item):
    data = result[item]
    ax.plot(result['x_ticks'], data.data,
            color=data.color, label=data.name_with_tani, alpha=1)

def plot_demand(result, figsize=(6, 4.8)):
    fig, ax = plt.subplots(figsize=figsize)
    plot_bar(ax, result, ['demand'], is_left=True)
    plot_bar(ax, result, ['sun_use', 'bat_out', 'ele_use'])
    # グラフの設定
    set_title(ax, 'Demand and Supply')
    set_legend(ax)
    set_ax(ax, 'Time', 'Electricity (W)')
    return fig, ax

def plot_solar(result, figsize=(6, 4.8)):
    fig, ax = plt.subplots(figsize=figsize)
    plot_bar(ax, result, ['sun_gen'], is_left=True)
    plot_bar(ax, result, ['sun_use', 'sun_charge', 'sun_sell'])
    # グラフの設定
    set_title(ax, 'Balance of Solar Power')
    set_legend(ax)
    set_ax(ax, 'Time', 'Electricity (W)')
    return fig, ax

def plot_cost_charge(result, figsize=(6, 4.8)):
    fig, ax = plt.subplots(figsize=figsize)
    plot_bar(ax, result, ['sun_charge', 'ele_charge'])
    ax_right = ax.twinx()
    plot_line(ax_right, result, 'cost_ele')
    # グラフの設定
    set_title(ax, 'Balance of Solar Power')
    set_legend(ax, ax_right=ax_right)
    set_ax(ax, 'Time', 'Electricity (W)', ax_right=ax_right, ylabel_right='Prices (yen)')
    return fig, ax

def plot_cost_use(result, figsize=(6, 4.8)):
    fig, ax = plt.subplots(figsize=figsize)
    plot_bar(ax, result, ['sun_use', 'ele_use', 'bat_out'])
    ax_right = ax.twinx()
    plot_line(ax_right, result, 'cost_ele')
    # グラフの設定
    set_title(ax, 'Commercial Electricity and Use of Electricity')
    set_legend(ax, ax_right=ax_right)
    set_ax(ax, 'Time', 'Electricity (W)', ax_right=ax_right, ylabel_right='Prices (yen)')
    return fig, ax


def make_output_sche(result_sche, sche_times):
    #時間ごとに組み直したスケジュールを24時間にまとめる
    output_sche = []
    for k in range(7):
        a = [result_sche[i][k] for i in range(sche_times)]
        b = []
        for i in range(sche_times):
            b += a[i]
        output_sche.append(b)
    return output_sche


def align_sun(schedule, Sun, output_len):
    # schedule はすでに unit を全要素にかけたもの
    array = np.array(schedule).T
    for t in range(output_len):
        # 出力-入力
        dif = Sun[t] - sum(array[t][:3])
        # 出力＞発電量
        if dif > 0:
            array[t][2] += dif #発電量が余っているなら売る
        # そうでなければ
        # まず足りない dif を「太陽光を売る」から確保
        if dif < 0 and array[t][2] > 0:
            val = min(array[t][2], -dif)
            array[t][2] -= val
            dif += val
        # それでも足りなければ dif を「太陽光を貯める」から確保
        if dif < 0 and array[t][1] > 0:
            val = min(array[t][1], -dif)
            array[t][1] -= val
            array[t][6] -= val  # 蓄電池容量から減らすことも忘れずに
            dif += val
        # それでも足りなければ dif を「太陽光を使う」から確保
        if dif < 0 and array[t][0] > 0:
            val = min(array[t][0], -dif)
            array[t][0] -= val
            dif += val
        # ここで多分 dif == 0 が保証されている？
    schedule = (array.T).tolist()
    return schedule

# 需要の収支を揃える後処理
def align_demand(schedule, D, output_len):
    # schedule はすでに unit を全要素にかけたもの
    array = np.array(schedule).T
    for t in range(output_len):
        # 需要-供給
        dif = D[t] - array[t][0] - array[t][3] - array[t][4]
        # 需要＞供給なら
        if dif > 0:
            array[t][4] += dif  #商用電源を買う
        # 供給＞需要
        # まず供給過多分をなるべく「商用電源の使用(購入)」から引く
        if dif < 0 and array[t][4] > 0:
            val = min(array[t][4], -dif)
            array[t][4] -= val
            dif += val
        # それでも供給過多なら「蓄電池の使用」から引けるだけ引く
        if dif < 0 and array[t][3] > 0:
            val = min(array[t][3], -dif)
            array[t][3] -= val
            array[t][6] -= val  # 蓄電池容量から減らすことも忘れずに
            dif += val
        # それでも供給過多なら「太陽光の使用」から引けるだけ引く
        if dif < 0 and array[t][0] > 0:
            val = min(array[t][0], -dif)
            array[t][3] -= val
            dif += val             
    schedule = (array.T).tolist()       
    return schedule

#後処理をまとめて行う
def post_process(schedule, Sun, D, output_len):
    schedule = align_sun(schedule, Sun, output_len)
    schedule = align_demand(schedule, D, output_len)
    return schedule
