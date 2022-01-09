import numpy as np


#コスト項
def cost_term(step, total, komoku, cost_ratio,
              conv_eff, C_ele, C_sun, C_env, q1):
    poly = 0
    C_max = max(max(C_ele), max(C_sun))
    C_min = min(min(C_ele), min(C_sun))
    bunbo = C_max - C_min

    #第１項：H_expence_cost(経費コスト)
    for t in range(step):
        for i in range(total):
            k1 = step * i + t
            #項目iが電源使用または充電
            if komoku[i][1]=='ele':
                #経費コスト
                poly += q1[k1] * (C_ele[t]-C_min) / bunbo*cost_ratio
                #環境コスト
                poly += q1[k1] * C_env * (1 - cost_ratio)
            #項目iが光売電
            elif komoku[i][2]=='sell':
                poly += q1[k1] * (C_sun[t]-C_min) / bunbo * cost_ratio * conv_eff
    return poly


#制約項
def penalty_term(step, total, komoku, cost_ratio, conv_eff,
                 D, Sun, w_a, w_io, w_d, w_s, q1):
    poly = 0
    #第３項：H_alloc(項目iが割り当てられるのは1枠)
    for i in range(total):
        for t in range(step):
            for t_ in range(step):
                k1 = step * i + t
                k2 = step * i + t_
                if k1 != k2:
                    poly += w_a * q1[k1] * q1[k2]

    #第４項：H_inout(蓄電池の入出力を同時に行わない)
    for t in range(step):
        for i in range(total):
            for j in range(total):
                k1 = step * i + t
                k2 = step * j + t
                if (komoku[i][2]=='in')and(komoku[j][2]=='out'):
                    poly += w_io * q1[k1] * q1[k2]

    #第５項：H_demand(電力需要のバランス)
    for t in range(step):
        for i in range(total):
            for j in range(total):
                k1 = step * i + t
                k2 = step * j + t
                #項目i,jがuse/outのとき
                if (komoku[i][2]=='use' or komoku[i][2]=='out')\
                    and (komoku[j][2]=='use' or komoku[j][2]=='out'):
                    if i != j:
                        if komoku[i][1]=='sun' and komoku[j][1]=='sun':
                            poly += w_d * conv_eff**2 * q1[k1] * q1[k2]
                        # 多分 elif komoku[i][1]=='sun' or komoku[j][1]=='sun' でOK
                        elif (komoku[i][1]=='sun' and komoku[j][1]!='sun')\
                            or (komoku[i][1]!='sun' and komoku[j][1]=='sun'):
                            poly += w_d * conv_eff * q1[k1] * q1[k2]
                        else:
                            poly += w_d * q1[k1] * q1[k2]
                    else:
                        if komoku[i][1]=='sun':
                            poly += (1-2*D[t]) * w_d * conv_eff**2 * q1[k1] * q1[k2]
                        else:
                            poly += (1-2*D[t]) * w_d * q1[k1] * q1[k2]

    #第６項：H_sun(太陽光のバランス)
    for t in range(step):
        for i in range(total):
            for j in range(total):
                k1 = step * i + t
                k2 = step * j + t
                #項目i,jがsunのとき
                if komoku[i][1]=='sun' and komoku[j][1]=='sun':
                    if i != j:
                        poly += w_s * q1[k1] * q1[k2]
                    else:
                        poly += (1-2*Sun[t]) * w_s * q1[k1] * q1[k2]
    return poly


#B(t)の多項式を出す
def B_t_poly(time, B_0, step, total, b_in, b_out, q):
    poly = B_0
    def func(poly, t=1):
        #終了条件
        if t==time+1:
            return poly
        #変数部分
        poly *= (1-eta)
        #シグマの部分
        for i in range(total):
            k = step * i + (t-1)
            if komoku[i][2]=='in':
                poly += b_in * q1[k]
            elif komoku[i][2]=='out':
                poly -= b_out * q1[k]
        return func(poly, t+1)
    poly = func(poly)
    return poly


#不等式制約項
def ineq(q1, q2, q3, step, total, komoku, eta, b_in, b_out, B_max, B_0, y_n):
    #B(t)を計算
    def B_t_poly(time, B_0):
        poly = B_0
        def func(poly, t=1):
            #終了条件
            if t==time+1:
                return poly
            #変数部分
            poly *= (1-eta)
            #シグマの部分
            for i in range(total):
                k = step * i + (t-1)
                if komoku[i][2]=='in':
                    poly += b_in * q1[k]
                elif komoku[i][2]=='out':
                    poly -= b_out * q1[k]
            return func(poly, t+1)
        poly = func(poly)
        return poly

    #スラック変数の多項式
    def slack_poly(time, q):
        poly = 0
        for i in range(y_n):
            k = step * i + (time-1)
            poly += 2**i * q[k]
        return poly

    #poly1はB(t)=<B_max
    #poly2は0=<B(t)を表す
    poly1, poly2 = 0, 0
    for t in range(1, step+1):
        poly1 += (B_max - B_t_poly(t,B_0) - slack_poly(t,q2))**2
        poly2 += (-B_t_poly(t,B_0) + slack_poly(t,q3))**2
    return poly1, poly2
