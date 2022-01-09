# SituationParams のテスト
# GitHub の仮のブランチに一旦アップロードしたあと、
# Google Colab で
# !pip install git+https://github.com/CanonMukai/hemsq-prototype.git@ブランチ
# 動かして動作確認

from hemsq import HemsQ
from hemsq import SituationParams

from amplify.client import FixstarsClient

def test():
    # 初期化テスト
    hq = HemsQ()
    assert isinstance(hq, HemsQ)
    assert isinstance(hq._sp, SituationParams)
    assert hq.results == []

    hq.set_params(
        unit=200,
        battery_capacity=6000,
        initial_battery_amount=5000,
        b_in=0.96,
        b_out=0.96,
        eta=0.1,
        conv_eff=0.9,
        rated_output=3000,
        cost_ratio=1.1,
        c_env=0.5,
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
    assert params["b_in"] == 0.96
    assert params["b_out"] == 0.96
    assert params["eta"] == 0.1
    assert params["conv_eff"] == 0.9
    assert params["rated_output"] == 3000
    assert params["cost_ratio"] == 1.1
    assert params["c_env"] == 0.5
    assert params["start_time"] == 1
    assert params["step"] == 8
    assert params["output_len"] == 12
    assert params["reschedule_span"] == 8
    assert params["weather_list"] == ["c" for i in range(24)]
    assert params["demand_list"] == [100 for i in range(24)]

    hq.set_params(
        cost_ratio=1.0,
    )
    params = hq.params
    assert params["cost_ratio"] == 1.0

    client = FixstarsClient()
    client.token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    client.parameters.timeout = 1000 # タイムアウト1秒
    client.parameters.outputs.num_outputs = 0
    client.parameters.outputs.duplicate = True # エネルギー値が同一の解を重複して出力する
    hq.set_client(client)

    hq.solve()

test()
