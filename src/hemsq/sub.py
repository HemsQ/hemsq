import itertools

import numpy as np


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


#！パラメタ調整用！(1/3追加)
#破った制約を追加したリストを返す
def constraint(schedule, Sun, D, B_max, satisfied):  
    schedule = np.array(schedule).T
    broken_lst = []
    if not satisfied:
        broken_lst.append('alloc')
    if not check_inout(schedule): 
        broken_lst.append('inout')
    if not demandBalancePerStep(schedule,D):
        broken_lst.append('demand')
    if not sunBalancePerStep(schedule,Sun):
        broken_lst.append('sun')
    if not batteryCapacity(schedule,B_max):
        broken_lst.append('battery')
    return broken_lst