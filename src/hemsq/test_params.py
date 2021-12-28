from params import Params


def test():
    # 初期化テスト
    p = Params()
    assert isinstance(p, Params)

    # 初期化時の property へのアクセステスト
    assert isinstance(p.unit, int)
    assert isinstance(p.actual_b_max, int)
    assert isinstance(p.actual_b_0, int)
    assert isinstance(p.actual_rated_capa, int)
    assert isinstance(p.cost_ratio, float)
    assert isinstance(p.start_time, int)
    assert isinstance(p.step, int)
    assert isinstance(p.output_len, int)
    assert isinstance(p.resche_span, int)
    assert isinstance(p.tenki, list)
    assert isinstance(p.demand, list)
    assert p.client == None

    # set 関数のテスト
    p.set_unit(50)
    # TODO: unit の変更に伴う他の値の変化のテスト
    assert p.unit == 50
    # TODO: actual -> 計算用の値のテスト
    p.set_actual_b_max(6000)
    assert p.actual_b_max == 6000
    p.set_actual_b_0(3000)
    assert p.actual_b_0 == 3000
    p.set_actual_rated_capa(3000)
    assert p.actual_rated_capa == 3000
    p.set_cost_ratio(1.5)
    assert p.cost_ratio == 1.5
    p.set_start_time(12)
    assert p.start_time == 12
    p.set_step(6)
    assert p.step == 6
    p.set_output_len(12)
    assert p.output_len == 12
    p.set_resche_span(3)
    assert p.resche_span == 3
    p.set_tenki(["c" for i in range(8)])
    assert p.tenki == ["c" for i in range(8)]
    p.set_demand([100 for i in range(24)])
    assert p.demand == [100 for i in range(24)]
    # TODO: client のテスト


if __name__ == "__main__":
    test()
