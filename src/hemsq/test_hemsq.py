# SituationParams のテスト
# GitHub の仮のブランチに一旦アップロードしたあと、
# Google Colab で
# !pip install git+https://github.com/CanonMukai/hemsq-prototype.git@ブランチ
# 動かして動作確認

from hemsq import HemsQ
from hemsQ import SituationParams

def test():
    # 初期化テスト
    hq = HemsQ()
    assert isinstance(hq, HemsQ)
    assert isinstance(hq._sp, SituationParams)

    hq.set_params(
        unit=200,
        battery_capacity=6000,
        initial_battery_amount=5000,
        rated_output=3000,
        cost_ratio=1.1,
        start_time=1,
        step=8,
        output_len=12,
        reschedule_span=8,
        weather_list=["c" for i in range(24)],
        demand_list=[100 for i in range(24)],
    )
    sp = hq.situation_params
    assert sp["unit"] == 200
    assert sp["battery_capacity"] == 6000
    assert sp["initial_battery_amount"] == 5000
    assert sp["rated_output"] == 3000
    assert sp["cost_ratio"] == 1.1
    assert sp["start_time"] == 1
    assert sp["step"] == 8
    assert sp["output_len"] == 12
    assert sp["reschedule_span"] == 8
    assert sp["weather_list"] == ["c" for i in range(24)]
    assert sp["demand_list"] == [100 for i in range(24)]

    hq.set_params(
        cost_ratio=1.0,
    )
    sp = hq.situation_params
    assert sp["cost_ratio"] == 1.1

test()
