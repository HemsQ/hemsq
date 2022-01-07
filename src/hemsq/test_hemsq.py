# SituationParams のテスト
# GitHub の仮のブランチに一旦アップロードしたあと、
# Google Colab で
# !pip install git+https://github.com/CanonMukai/hemsq-prototype.git@ブランチ
# 動かして動作確認

from hemsq import HemsQ
from hemsq import SituationParams

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
    params = hq.params
    assert params["unit"] == 200
    assert params["battery_capacity"] == 6000
    assert params["initial_battery_amount"] == 5000
    assert params["rated_output"] == 3000
    assert params["cost_ratio"] == 1.1
    assert params["start_time"] == 1
    assert params["step"] == 8
    assert params["output_len"] == 12
    assert params["reschedule_paramsan"] == 8
    assert params["weather_list"] == ["c" for i in range(24)]
    assert params["demand_list"] == [100 for i in range(24)]

    hq.set_params(
        cost_ratio=1.0,
    )
    params = hq.params
    assert params["cost_ratio"] == 1.0

test()
