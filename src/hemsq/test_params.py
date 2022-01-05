from situation_params import SituationParams


def test():
    # 初期化テスト
    sp = SituationParams()
    assert isinstance(sp, SituationParams)

    # 初期化時の property へのアクセステスト
    assert isinstance(sp.unit, int)
    assert isinstance(sp.actual_b_max, int)
    assert isinstance(sp.actual_b_0, int)
    assert isinstance(sp.actual_rated_capa, int)
    assert isinstance(sp.cost_ratio, float)
    assert isinstance(sp.start_time, int)
    assert isinstance(sp.step, int)
    assert isinstance(sp.output_len, int)
    assert isinstance(sp.resche_span, int)
    assert isinstance(sp.tenki, list)
    assert isinstance(sp.demand, list)
    assert sp.client == None

    # set 関数のテスト
    sp.set_unit(50)
    assert sp.unit == 50
    sp.set_actual_b_max(6000)
    assert sp.actual_b_max == 6000
    sp.set_actual_b_0(3000)
    assert sp.actual_b_0 == 3000
    sp.set_actual_rated_capa(3000)
    assert sp.actual_rated_capa == 3000
    sp.set_cost_ratio(1.5)
    assert sp.cost_ratio == 1.5
    sp.set_start_time(12)
    assert sp.start_time == 12
    sp.set_step(6)
    assert sp.step == 6
    sp.set_output_len(12)
    assert sp.output_len == 12
    sp.set_resche_span(3)
    assert sp.resche_span == 3
    sp.set_tenki(["c" for i in range(8)])
    assert sp.tenki == ["c" for i in range(8)]
    sp.set_demand([100 for i in range(24)])
    assert sp.demand == [100 for i in range(24)]
    # TODO: client のテスト


if __name__ == "__main__":
    test()
