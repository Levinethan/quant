from cybotrade.strategy import Strategy
from cybotrade.models import RuntimeConfig, RuntimeMode
from datetime import datetime, timezone
from cybotrade.permutation import Permutation
import asyncio
import numpy as np
from cybotrade.runtime import StrategyTrader
import pandas as pd
import re

provider_coinglass = "coinglass"
provider_crytoquant = "cryptoquant"
provider_glassnode = "glassnode"

# Time interval
interval = "1d"
# Exchange Platform
exchange = "Binance"
start_time = datetime(2017, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
end_time = datetime(2025, 4, 1, 0, 0, 0, tzinfo=timezone.utc)

########################################################## coinglass endpoint ##################################################
# ------------------------------------------------- liquidation -------------------------------------------------
endpoint="futures/liquidation/history?exchange="+exchange+"&symbol=BTCUSDT&interval="+interval #从2020-12-23 08:00:00开始才有数据
# ------------------------------------------------- liquidation -------------------------------------------------

# ------------------------------------------------- takerBuySellVolume -------------------------------------------------
endpoint2="futures/takerBuySellVolume/history?exchange="+exchange+"&symbol=BTCUSDT&interval="+interval # 从2019-09-25 08:00:00开始才有数据
endpoint3="futures/aggregatedTakerBuySellVolumeRatio/history?exchange="+exchange+"&symbol=BTCUSDT&interval="+interval # 不会用
# ------------------------------------------------- takerBuySellVolume -------------------------------------------------

# ------------------------------------------------- openInterest -------------------------------------------------
endpoint4="futures/openInterest/ohlc-history?exchange="+exchange+"&symbol=BTCUSDT&interval="+interval #2020-02-27 08:00:00
endpoint5="futures/openInterest/ohlc-aggregated-history?symbol=BTC&interval="+interval #提供市场规模、流动性、参与度和情绪的综合信息
# ------------------------------------------------- openInterest -------------------------------------------------

# ------------------------------------------------- fundingRate -------------------------------------------------
endpoint6="futures/fundingRate/ohlc-history?exchange="+exchange+"&symbol=BTCUSDT&interval="+interval # 2020-03-30 08:00:00
endpoint7="futures/fundingRate/oi-weight-ohlc-history?symbol=BTC&interval="+interval # 2020-03-31 08:00:00
endpoint8="futures/fundingRate/vol-weight-ohlc-history?symbol=BTC&interval="+interval # 2023-04-23 08:00:00
# ------------------------------------------------- fundingRate -------------------------------------------------

# ------------------------------------------------- LongShortAccountRatio -------------------------------------------------
endpoint9="futures/globalLongShortAccountRatio/history?exchange="+exchange+"&symbol=BTCUSDT&interval="+interval # 提供市场持仓情绪
endpoint10="futures/topLongShortPositionRatio/history?exchange="+exchange+"&symbol=BTCUSDT&interval="+interval # leading indicator
# ------------------------------------------------- LongShortAccountRatio -------------------------------------------------
####################################################### coinglass endpoint #######################################################


class MyStrategy(Strategy):
    datasource_data = []
    candle_data = []
    async def on_datasource_interval(self, strategy, topic, data_list):
        model = self.data_map[topic]
        #long_short_ratio = np.array(list(map(lambda c: float(c["longShortRatio"]), model)))
        self.datasource_data.append(super().data_map[topic][-1])
 
    async def on_candle_closed(self, strategy, topic, symbol):
        self.candle_data.append(super().data_map[topic][-1])

    async def on_backtest_complete(self, strategy: StrategyTrader):
        datasource_df = pd.DataFrame(self.datasource_data)
        candle_df = pd.DataFrame(self.candle_data)
        
        df = pd.merge(datasource_df,candle_df)
        # ---------------------- change endpoint ----------------------
        name = re.sub(r'[^a-zA-Z0-9\s]', '', endpoint9) 
        # ---------------------- change endpoint ----------------------
        path = "./src/" + f"{exchange}-" + f"{provider_coinglass}-{start_time}-{name}.csv"
        print("path :",path)
        df.set_index("start_time",inplace=True)
        df.to_csv(path,index=False)

 
config = RuntimeConfig(
    mode=RuntimeMode.Backtest,
    datasource_topics=[
        f"{provider_coinglass}|{endpoint9}"
        ],
    candle_topics=[
        "binance-linear|candle?symbol=BTCUSDT&interval="+interval
        ],
    active_order_interval=1,
    start_time=start_time,
    end_time=end_time,
    data_count=15000,
    api_key="yabyRpmCIUkfFekmvSzCuoBHGz8uWkPIOWthlRUxREJVwXt3",
    api_secret="hiTXS8iyenJSJUivJ4Vw1C2e6zXRIZm5k6fU1Y6M1V90Ngtkf6hArUhREbAAdw76O4CQMTEP"
)
 
permutation = Permutation(config)
hyper_parameters = {}
 
async def start_runtime():
    await permutation.run(hyper_parameters, MyStrategy)
 
asyncio.run(start_runtime())

