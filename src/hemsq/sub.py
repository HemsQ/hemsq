import itertools

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'MS Gothic'
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
    return (val * p * 2 + 1) // 2 / p


def rotateAll(start, end, D_all, Sun_all, C_ele_all, C_sun_all):
    #リストを途中から一周する関数
    def rotate(start, end, lst):
        l = len(lst)
        nlst = [0] * l
        for i in range(l):
            if start + i < l:    
                nlst[i]  = lst[start+i]
            else:
                nlst[i] = lst[start+i-l]        
        nlst = nlst[:end+1-start]
        return nlst    
    D = rotate(start, end, D_all)
    Sun = rotate(start, end, Sun_all)
    C_ele = rotate(start, end, C_ele_all)
    C_sun = rotate(start, end, C_sun_all)
    return D, Sun, C_ele, C_sun


#24時間分の入力データを作る
def makeInput(demand, tenki, normalize_rate, unit):

    #1kWの太陽光パネル・快晴・9月
    sun = [0,0,0,0,0,0,0,100,300,500,600,700,700,700,600,500,400,200,0,0,0,0,0,0]    
    #通常の家の発電量
    sun = normalize(sun, 2)
    #天気で発電量を調整する
    sun = Weather3hours(tenki, sun)
    
    #リストを四捨五入してカードにする
    def rounding(lst):
        #unitで割って
        lst1 = list(normalize(lst, 1 / unit))
        #小数点を四捨五入
        lst2 = [int(my_round(lst1[i], 0)) for i in range(len(lst1))]
        return lst2

    #丸めてunitでわる
    demand = rounding(demand)
    sun = rounding(sun)
    # もともと C_ele = eleCost() だったけど、このように変えた
    C_ele = [12, 12, 12, 12, 12, 12, 12, 26, 26, 26, 39, 39, 39, 39, 39, 39, 39, 12, 12, 12, 12, 12, 12, 12]
    C_sun = [8]*24
    C_ele = normalize(C_ele, normalize_rate * unit / 1000)
    C_sun = normalize(C_sun, normalize_rate * unit / 1000)
    return demand, sun, C_ele, C_sun


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
def makeSchedule(opt_result, step, total, komoku, B_0):
    schedule = [0] * step
    B = B_0
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
        B = do['bat']
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
def unitDouble(schedule, normalize_rate, unit):
    # ここでで定義されていた normalize() は消した
    for i in range(len(schedule)):
        schedule_ = [normalize(schedule[i], unit) for i in range(len(schedule))]
    return schedule_


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
    ax1.axis('off')
    ax1.table(cellText=df0.values, colLabels=df0.columns,\
             rowLabels=df0.index, loc=loc, fontsize=15)
    plt.show()

    
def make2Table(schedule, start, D, Sun, C_ele, unit, normalize_rate, output_len):
    demand = list(map(int, normalize(D[:output_len], unit)))
    sun = list(map(int, normalize(Sun[:output_len], unit)))
    cost = list(map(int, normalize(C_ele[:output_len], 1000/normalize_rate/unit)))
    label = ["需要(w)", "太陽光発電量(w)", "商用電源料金(円)"]
    makeTable(start, [demand, sun, cost], label, 0, output_len)
    label = ["太陽光使用(w)", "太陽光充電(w)", "太陽光売電(w)",\
             "蓄電池使用(w)", "商用電源使用(w)", "商用電源充電(w)",\
             "蓄電池残量(w)"]
    makeTable(start,unitDouble(schedule, normalize_rate, unit), label, 1, output_len)  

#最適解でかかった経費コストを計上してプリント出力する
def costPrint(schedule, normalize_rate, C_ele, C_sun, unit, output_len):
    array = np.array(schedule)
    cost = 0 #コストの合計
    e_cost = 0
    for t in range(output_len):
        #商用電源使用は4行目
        from_ele = (array[4][t] + array[5][t]) * C_ele[t] / normalize_rate 
        cost += from_ele
        e_cost += from_ele
        #太陽光売電は2行目
        cost -= array[2][t] * C_sun[t] / normalize_rate
    #コスト正なら
    if cost >= 0:
        print("かかったコストは", cost, "円")
    #負なら
    else:
        print(-cost, "円の売上")
    #CO2排出量（0.445kg/kWh)
    CO2 = my_round(0.445 * e_cost*unit / 1000, 1)
    print("CO2排出量", CO2, "kg")

#棒グラフ
def plotBar(start, schedule, Data, mode, unit, output_len):
    step_labels = [str((i+start)%24) for i in list(range(output_len))]    
    if mode == 1:
        data_name = "需要"
        barvalue_ = list(itemgetter(0, 3, 4)(schedule))
        pop_lst = [1, 2, 5]
        title = "需要と供給"
    else:
        data_name="太陽光発電量"        
        barvalue_ = list(itemgetter(0, 1, 2)(schedule))
        pop_lst = [3, 4, 5] 
        title = "太陽光の収支"
    how_labels = [data_name, "太陽光使用", "太陽光充電", "太陽光売電",\
                  "蓄電池使用", "商用電源使用", "商用電源充電"]
    color = ['gray', 'orangered', 'deepskyblue', 'limegreen']
    for i in sorted(pop_lst, reverse=True):
        how_labels.pop(i+1)
    barvalue = unitDouble(barvalue_, normalize_rate, unit)      
    data=list(map(int, normalize(Data, unit)))
    df0 = pd.DataFrame(barvalue, index=how_labels[1:])
    ymax = max([sum([[barvalue[i][j] for i in range(len(barvalue))]\
                     for j in range(output_len)][k]) for k in range(output_len)])
    fig, ax = plt.subplots(figsize=(6, 4.8), dpi=150)
    ax.bar(step_labels, data, width=-0.3, align='edge', color=color[0])        
    for i in range(len(df0)):
        ax.bar(step_labels, df0.iloc[i], width=0.3,\
               align='edge', bottom=df0.iloc[:i].sum(), color=color[i+1])
    #凡例
    ax.legend(how_labels, loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=18)
    #x軸
    ax.set_xlabel('時間(時)', fontsize=18)
    ax.set_xticks([i*3 for i in range(8)])    
    ax.tick_params(axis='x', labelsize=5)
    #y軸
    ax.set_ylabel('電力量(W)', fontsize=18)    
    ax.set_ylim(0, ymax + 10)
    ax.tick_params(axis='y', labelsize =15)
    #タイトル
    ax.set_title(title, fontsize=20)
    plt.show()


def plotBar_bat(start, schedule, mode, C_ele, normalize_rate, output_len):
    step_labels = [str((i+start)%24) for i in list(range(output_len+1))] 
    #充電のグラフ
    if mode==0:       
        data_name = "充電&料金"           
        barvalue_ = list(itemgetter(1, 5)(schedule))
        title = "商用電源料金の推移と充電"
        how_labels = [data_name, "太陽光充電", "商用電源充電", "商用電源料金"]
    #使用のグラフ
    else:
        data_name = "使用&料金"           
        barvalue_ = list(itemgetter(0, 3, 4)(schedule))
        title = "商用電源料金の推移と電力使用"
        how_labels = [data_name, "太陽光使用", "商用電源使用", "蓄電池使用", "商用電源料金"]
    barvalue = unitDouble(barvalue_, normalize_rate, unit) 
    color = ['orange', 'deepskyblue', 'limegreen']
    #時間ごとの充電・使用量の最大値を求めておきy軸の上限を定めておく
    ymax = max([sum([[barvalue[i][j] for i in range(len(barvalue))] \
                     for j in range(output_len)][k]) for k in range(output_len)])
    c_ele = normalize(C_ele, 1/normalize_rate)
    df0 = pd.DataFrame(barvalue, index=how_labels[1: len(how_labels)-1])
    #ax1:使用・充電の棒グラフ
    fig, ax1 = plt.subplots(figsize=(6, 4.8), dpi=150)
    for i in range(len(df0)):
        ax1.bar(step_labels[:-1], df0.iloc[i], width=0.3, align='edge',
                bottom=df0.iloc[:i].sum(), label=how_labels[1+i], color=color[i])
    #凡例
    ax1.legend(how_labels, loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=18)
    #タイトル
    ax1.set_title(title, fontsize=20)
    ax1.set_ylim(0, ymax + 10)
    hans1, labs1 = ax1.get_legend_handles_labels()    
    #x軸
    ax1.set_xlabel('時間(時)', fontsize=18)
    ax1.tick_params(axis='x', labelsize=15)
    #y軸
    ax1.set_ylabel('電力量(W)', fontsize=18)    
    ax1.tick_params(axis='y', labelsize=15)
    #ax2:商用電源の折れ線グラフ
    ax2 = ax1.twinx()
    ax2.plot(step_labels[:-1], c_ele, color='r', alpha=1, label=how_labels[len(how_labels)-1])
    ax2.set_ylabel('料金(円)', fontsize=18)    
    ax2.tick_params(axis='x', labelsize=15)
    ax2.tick_params(axis='y', labelsize=15)
    y_min, y_max = ax2.get_ylim()
    ax2.set_ylim(y_min, y_max)
    #凡例
    hans2, labs2 = ax2.get_legend_handles_labels()
    ax1.legend(hans1+hans2, labs1+labs2, loc="upper left", bbox_to_anchor=(1.2, 1.0), fontsize=15)
    ax1.set_xticks([i*3 for i in range(8)])    
    plt.show()


#グラフ4つ表示
def makeBar(schedule, start, D, Sun, C_ele, unit, normalize_rate, output_len):
    #太陽光の収支
    plotBar(start, schedule, Sun, 0, unit, output_len)
    #需要と供給
    plotBar(start, schedule, D, 1, unit, output_len)
    #商用電源料金と充電量
    plotBar_bat(start, schedule, 0, C_ele, normalize_rate, output_len)
    #商用電源料金と使用量
    plotBar_bat(start, schedule, 1, C_ele, normalize_rate, output_len)


#予測モデル型の場合の出力
def output(schedule, start, D_all, Sun_all, C_ele_all, C_sun_all,\
          unit, normalize_rate, output_len):
    #outputしたい時間分のデータ
    D_op, Sun_op, C_ele_op, C_sun_op =\
        rotateAll(start, (start+output_len-1)%24, D_all, Sun_all,\
                  C_ele_all, C_sun_all)        
    #値段表示
    # costPrint(schedule, normalize_rate, C_ele_op, C_sun_op,unit, output_len)
    #表表示
    make2Table(schedule, start, D_op, Sun_op, C_ele_op, unit, normalize_rate,\
               output_len)
    #棒グラフ表示
    makeBar(schedule, start, D_op, Sun_op, C_ele_op, unit, normalize_rate,\
            output_len)


def marge_sche(result_sche, sche_times, start_time, D_all, Sun_all, C_ele_all,\
               C_sun_all, unit, normalize_rate, output_len):
    #時間ごとに組み直したスケジュールを24時間にまとめる
    output_sche = []
    for k in range(7):
        a = [result_sche[i][k] for i in range(sche_times)]
        b = []
        for i in range(sche_times):
            b += a[i]
        output_sche.append(b)
    output(output_sche, start_time, D_all, Sun_all, C_ele_all, C_sun_all,\
           unit, normalize_rate, output_len)
