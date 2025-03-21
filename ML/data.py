from datetime import datetime, timezone, timedelta
from typing import Dict, List
from cybotrade.strategy import Strategy as BaseStrategy
from cybotrade.runtime import StrategyTrader
from cybotrade.models import (
    ActiveOrder,
    RuntimeConfig,
    RuntimeMode,
    Symbol,
    Exchange,
    OrderSide,
)
from cybotrade.permutation import Permutation
import numpy as np
import asyncio
import logging
import colorlog
import pandas as pd
import util
import re
#import talib
import matplotlib.pyplot as plt
import math
import os
import webbrowser
import pytz

# 画地为牢 
start_time = datetime(2023, 7, 10, 0, 0, 0, tzinfo=timezone.utc)
end_time = datetime(2024, 9, 28, 0, 0, 0, tzinfo=timezone.utc)
# 选择频率
interval="1h"
crytoquant_interval = "hour"

# 数据商目前3家
provider="coinglass"
# 交易所5家
exchange="Bybit"

################################################# 666 ##################################################################################
# ------------------------------------------------- liquidation -------------------------------------------------
endpoint="futures/liquidation/history?exchange=Bybit&symbol=BTCUSDT&interval="+interval # 趋势
# ------------------------------------------------- liquidation -------------------------------------------------

# ------------------------------------------------- takerBuySellVolume -------------------------------------------------
endpoint2="futures/takerBuySellVolume/history?exchange=Bybit&symbol=BTCUSDT&interval="+interval # leading indicator
endpoint3="futures/aggregatedTakerBuySellVolumeRatio/history?exchange=Bybit&symbol=BTCUSDT&interval="+interval # 不会用
# ------------------------------------------------- takerBuySellVolume -------------------------------------------------

# ------------------------------------------------- openInterest -------------------------------------------------
endpoint4="futures/openInterest/ohlc-history?exchange=Bybit&symbol=BTCUSDT&interval="+interval # lagging indicator openInterest 不能merge candle close
endpoint5="futures/openInterest/ohlc-aggregated-history?symbol=BTC&interval="+interval #提供市场规模、流动性、参与度和情绪的综合信息
# ------------------------------------------------- openInterest -------------------------------------------------

# ------------------------------------------------- fundingRate -------------------------------------------------
endpoint6="futures/fundingRate/ohlc-history?exchange=Bybit&symbol=BTCUSDT&interval="+interval # lagging indicator
endpoint7="futures/fundingRate/oi-weight-ohlc-history?symbol=BTC&interval="+interval # 不会用
endpoint8="futures/fundingRate/vol-weight-ohlc-history?symbol=BTC&interval="+interval # 不会用
# ------------------------------------------------- fundingRate -------------------------------------------------

# ------------------------------------------------- LongShortAccountRatio -------------------------------------------------
endpoint9="futures/globalLongShortAccountRatio/history?exchange=Bybit&symbol=BTCUSDT&interval="+interval # 提供市场持仓情绪
endpoint10="futures/topLongShortAccountRatio/history?exchange=Bybit&symbol=BTCUSDT&interval="+interval # leading indicator
# ------------------------------------------------- LongShortAccountRatio -------------------------------------------------
################################################# coinglass ##################################################################################

################################################# crytoquant ##################################################################################

# ------------------------------------------------- invalid enpoint exchange-flows -------------------------------------------------
crytoquant_endpoint1 = "btc/exchange-flows/in-house-flow?exchange=bybit&window="+crytoquant_interval # 该端点会返回 BTC 在同一交易所钱包内的内部流量，最早可追溯到我们追踪的日期。 平均内部流量是指特定日期钱包内流动交易的平均交易价值。
crytoquant_endpoint2 = "btc/exchange-flows/reserve?exchange=bybit&window="+crytoquant_interval # 该端点返回比特币交易所的全部历史链上余额。
crytoquant_endpoint3 = "btc/exchange-flows/netflow?exchange=bybit&window="+crytoquant_interval # 流入交易所的币与流出交易所的币之间的区别。 净流量通常可以帮助我们计算出在一定时间内等待交易的闲置币的增加情况。
crytoquant_endpoint4 = "btc/exchange-flows/inflow?exchange=bybit&window="+crytoquant_interval # 该端点会返回我们所追踪的交易所钱包的 BTC 流入量。 平均流入量是特定日期流入交易所钱包的平均交易价值。
crytoquant_endpoint5 = "btc/exchange-flows/outflow?exchange=bybit&window="+crytoquant_interval # 该端点会返回 BTC 流入交易所钱包的流出量，最早可追溯到我们追踪的日期。 平均流出量是特定日期流入交易所钱包的平均交易价值。
crytoquant_endpoint6 = "btc/exchange-flows/transactions-count?exchange=bybit&window="+crytoquant_interval # 该端点返回流入/流出比特币交易所的交易数量。
crytoquant_endpoint7 = "btc/exchange-flows/addresses-count?exchange=bybit&window="+crytoquant_interval # 该端点返回参与流入/流出交易的地址数。
# ------------------------------------------------- exchange-flows -------------------------------------------------

# ------------------------------------------------- market-data -------------------------------------------------
crytoquant_endpoint9 = "btc/market-data/open-interest?exchange=bybit&window="+crytoquant_interval # 此端点从衍生品交易所返回 BTC 永久未平仓合约。 支持未平仓合约的交易所如下。 请注意，我们将每个交易所的回报值单位统一为美元，但其合约规格可能有所不同。
crytoquant_endpoint10 = "btc/market-data/funding-rates?exchange=bybit&window="+crytoquant_interval # 资金利率代表交易者在永续掉期市场上押注哪种头寸的情绪。 正资金利率意味着许多交易者看涨，多头交易者向空头交易者支付资金。 负资金利率意味着许多交易者看跌，空头交易者向多头交易者支付资金。
crytoquant_endpoint11 = "btc/market-data/taker-buy-sell-stats?exchange=bybit&window="+crytoquant_interval # 买方买入/卖出统计量代表买方在市场中采取何种仓位的情绪。 该指标根据每个交易所的永久掉期交易计算得出。
crytoquant_endpoint12 = "btc/market-data/liquidations?exchange=bybit&window="+crytoquant_interval # 爆仓统计量代表在某个时间段内，由于资金不足而强制平仓的次数。 该指标根据每个交易所的永久掉期交易计算得出。

# Currently we support day and block.
crytoquant_endpoint13 = "btc/market-data/capitalization?window=day" #  资产规模统计量代表在某个时间段内，所有交易对中，所有币种的总资产。 该指标根据每个交易所的永久掉期交易计算得出。

crytoquant_endpoint14 = "btc/market-data/coinbase-premium-index?window="+crytoquant_interval # 币本位指数统计量代表在某个时间段内，币本位指数的变化情况。 该指标根据每个交易所的永久掉期交易计算得出。
# ------------------------------------------------- market-data -------------------------------------------------

# ------------------------------------------------- entity-flows -------------------------------------------------
crytoquant_endpoint15 = "btc/entity-flows/whale-movements?entity_type=whale&entity_name=chrislarsen&window=hour"
crytoquant_endpoint16 = "btc/entity-flows/addresses-count?entity_name=bybit&window=day&from=20191001&limit=2"
crytoquant_endpoint17 = "btc/entity-flows/outflow?entity_name=bybit&window=day&from=20191001&limit=2"
crytoquant_endpoint18 = "btc/entity-flows/inflow?exchange=bybit&window=day&from=20191001&limit=2"
crytoquant_endpoint19 = "btc/entity-flows/share?entity_name=bybit&window=day&from=20191001&limit=2"
crytoquant_endpoint20 = "btc/entity-flows/reserve?entity_name=bybit&window=day&from=20191001&limit=2"
# ------------------------------------------------- entity-flows -------------------------------------------------

#-------------------------------------------- 为什么btc与eth有区别? --------------------------------------
crytoquant_endpoint21 = "btc/network-data/tokens-transferred?window=day&limit=2"
crytoquant_endpoint27 = "eth/network-data/tokens-transferred-count?window=day"
#-------------------------------------------- ? --------------------------------------

# ------------------------------------------------- network-data -------------------------------------------------
crytoquant_endpoint22 = "btc/network-data/addresses-count?window="+crytoquant_interval # 该端点返回与已使用比特币地址数量相关的指标。 我们提供了几个指标：addsress_count_active，即区块链上活跃（发送者或接收者）的唯一地址总数；addsress_count_sender，即作为发送者活跃的地址数；addsress_count_receiver，即作为接收者活跃的地址数。
crytoquant_endpoint23 = "btc/network-data/transactions-count?window="+crytoquant_interval # 该端点返回与事务数量相关的指标。 我们提供了几个指标：transactions_count_total（事务总数）和 transactions_count_mean（事务平均数）。
crytoquant_endpoint24 = "btc/network-data/velocity?window="+crytoquant_interval # 该端点返回与比特币速度相关的指标。 比特币速度的计算方法是，用追踪 1 年的估计交易量（已转移代币的累计总和）除以当前供应量。 速度是衡量货币在市场上流通活跃程度的指标。
crytoquant_endpoint25 = "btc/network-data/supply?window="+crytoquant_interval # 该终点返回与比特币供应量相关的指标，即比特币的现存量。 我们目前提供两个指标：supply_total，比特币的总量（coinbase reward 发行的所有比特币的总和）；supply_new，在给定窗口中新发行的代币数量。
crytoquant_endpoint26 = "btc/network-data/block-bytes?window="+crytoquant_interval # 生成的所有数据块的平均大小（以字节为单位）。
crytoquant_endpoint28 = "btc/network-data/block-count?window="+crytoquant_interval # 在给定窗口中生成的区块数。
crytoquant_endpoint29 = "btc/network-data/block-interval?window="+crytoquant_interval # 以秒为单位显示生成区块的平均间隔时间。
crytoquant_endpoint30 = "btc/network-data/utxo-count?window="+crytoquant_interval # 在指定时间点存在的未用交易输出总数。
crytoquant_endpoint31 = "btc/network-data/fees?window="+crytoquant_interval # 该端点返回与支付给比特币矿工的费用有关的统计数据。 一般来说，费用的计算方法是从每个区块的总奖励中减去新发行的比特币。 我们提供三种统计数据：fee_total（所有费用的总和）、fee_block_mean（每个区块的平均费用）和fee_reward_percent（费用占区块总奖励的百分比）。 此外，这些数据还可以用美元表示。
crytoquant_endpoint32 = "btc/network-data/fees-transaction?window="+crytoquant_interval # 该端点返回支付给比特币矿工的每笔交易费用的相关统计数据。 一般来说，费用的计算方法是从每个区块的总奖励中减去新发行的比特币，再除以交易次数，从而计算出每个区块中每笔交易的平均费用。 我们提供两个统计数据：fees_transaction_mean（每笔交易的平均费用）和fees_transaction_median（每笔交易的费用中位数）。 此外，这些值可以美元为单位计算。
crytoquant_endpoint33 = "btc/network-data/blockreward?window="+crytoquant_interval # 区块奖励的总和（包括挖矿或定金奖励和交易费用）。 我们还提供以美元为单位的数值。
crytoquant_endpoint34 = "btc/network-data/difficulty?window="+crytoquant_interval # 开采一个新区块的平均难度。
crytoquant_endpoint35 = "btc/network-data/hashrate?window="+crytoquant_interval # 区块链的当前算力。
# ------------------------------------------------- network-data -------------------------------------------------

################################################# crytoquant ##################################################################################



################################################# coinglass Not supported yet ##################################################################################

endpoint8="futures/liquidation/order?exchange=Bybit&symbol=BTC&minLiquidationAmount=10000"
endpoint13="futures/takerBuySellVolume/exchange-list?symbol=BTC&range=h1"
endpoint14="futures/coins-markets"
endpoint15="futures/coins-price-change"
endpoint16="index/bitcoin-bubble-index"
endpoint17="index/ahr999"
endpoint18="index/tow-year-ma-multiplier"
endpoint19="index/tow-hundred-week-moving-avg-heatmap"
endpoint20="index/puell-multiple"
endpoint21="index/stock-flow"
endpoint22="index/pi"
endpoint23="index/golden-ratio-multiplier"
endpoint24="index/bitcoin-profitable-days"
endpoint25="index/bitcoin-rainbow-chart"
endpoint26="index/fear-greed-history"

######################################### Analyst Model #############################################

class Strategy(BaseStrategy):
    datasource_data = []
    candle_data = []
    exchange = Exchange.BybitLinear
    # 技术指标参数
    ATR_PERIOD = 14  # ATR周期
    ATR_MULTIPLIER = 2.0  # ATR乘数用于计算动态止损
    
    # 移动平均窗口
    FAST_WINDOW = 12  # 快速移动平均线窗口
    SLOW_WINDOW = 72  # 慢速移动平均线窗口
    
    # 策略参数
    USE_DYNAMIC_LOSS = True  # 是否使用动态止损
    STATIC_LOSS_RATIO = 0.05  # 静态止损比例(5%)
    
    # 信号选择配置
    USE_PRICE_SIGNALS = True  # 是否使用价格信号（MA交叉等）
    USE_LONG_SHORT_RATIO = False  # 是否使用多空比率信号
    
    # 信号阈值
    # 以下值将动态计算，不再使用固定阈值
    LONG_SHORT_RATIO_STD_DEV_MULTIPLIER = 1.2  # 标准差乘数
    RATIO_CALCULATION_WINDOW = 24  # 计算基准线和标准差的窗口(一天=6个4小时K线)
    
    # 持仓超时设置（小时）
    MAX_HOLDING_HOURS = 48  # 最大持仓时间
    MIN_PROFIT_THRESHOLD = 0.005  # 最小利润阈值(0.5%)
    
    
    # 交易成本设置
    SLIPPAGE_PCT = 0.0005  # 滑点
    COMMISSION_PCT = 0.005  # 手续费
    # 总交易成本（滑点+手续费）为千分之二
    total_pnl = 0.0
    quantity = 0.031
    start_time = datetime.utcnow()
    entry_time = datetime.now(pytz.timezone("UTC"))
    pair = Symbol(base="BTC", quote="USDT")
    def __init__(self):
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(f"%(log_color)s{Strategy.LOG_FORMAT}")
        )

        # ---------------------- change endpoint ----------------------
        name = re.sub(r'[^a-zA-Z0-9\s]', '', crytoquant_endpoint4) 
        # ---------------------- change endpoint ----------------------
        path = "./logs/" + f"{provider}-{name}.log"
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.INFO)
        super().__init__(log_level=logging.INFO, handlers=[handler, file_handler])

            
    async def on_datasource_interval(self, strategy: StrategyTrader, topic: str, data_list):
        logging.info("datasource data {}".format(super().data_map[topic][-1]))
        model = self.data_map[topic]
        current_price = await strategy.get_current_price(symbol=self.pair, exchange=Exchange.BinanceLinear)
        current_pos = await strategy.position(symbol=self.pair, exchange=Exchange.BinanceLinear)
        long_short_ratio = np.array(list(map(lambda c: float(c["longShortRatio"]), model)))
        avg = util.get_rolling_mean(long_short_ratio,11)
        print("long_short_ratio_avg :",avg[-1])
        
        if avg[-1] > 1.40 and current_pos.long.quantity == 0:
            try:
                await strategy.open(exchange=Exchange.BinanceLinear,
                        side=OrderSide.Buy, 
                        quantity=self.quantity, 
                        symbol=self.pair, 
                        limit=None, 
                        take_profit=None, 
                        stop_loss=None, 
                        is_hedge_mode=False, 
                        is_post_only=False) 
                logging.info(
                    f"current total_pnl: {self.total_pnl}, current position: {util.get_position_info(current_pos, self.entry_time)}  , long_short_ratio: {long_short_ratio[-1]}"
                )
            except Exception as e:
                logging.error(f"Failed to open long: {e}")
        elif avg[-1] > 1.40 and current_pos.long.quantity != 0:
            try:
                await strategy.close(exchange=Exchange.BinanceLinear,
                        side=OrderSide.Buy,
                        quantity=abs(current_pos.long.quantity),
                        symbol=self.pair,
                        is_hedge_mode=False
                         )
                 # 实盘Pnl 计算
                pnl = (current_price - current_pos.long.avg_price) * abs(current_pos.long.quantity)
                self.total_pnl += pnl
                logging.info(
                    f"current total_pnl: {self.total_pnl}, current position: {util.get_position_info(current_pos, self.entry_time)} ,long_short_ratio: {long_short_ratio[-1]}"
                )
            except Exception as e:
                    logging.error(f"Failed to close long: {e}")
        else:
            logging.info("no signal")

    async def on_candle_closed(self, strategy: StrategyTrader, topic: str, symbol: Symbol):
        logging.info("candle closed {}".format(super().data_map[topic][-1]))
        model = self.data_map[topic]
        # -------------------------------- logic --------------------------------
        close = np.array(list(map(lambda c: float(c["close"]), model)))
        # -------------------------------- logic --------------------------------
        self.candle_data.append(super().data_map[topic][-1])


config = RuntimeConfig(
            mode=RuntimeMode.LiveTestnet,
            # ---------------------- change endpoint ----------------------
            datasource_topics=[
                    "coinglass|futures/topLongShortAccountRatio/history?exchange=Binance&symbol=BTCUSDT&interval=1m"
                ],
            candle_topics=["binance-linear|candle?symbol=BTCUSDT&interval=1m"],
            # ---------------------- change endpoint ----------------------
            active_order_interval=1,
            initial_capital=10000.0,
            exchange_keys="./credentials.json",
            start_time=start_time,
            end_time=end_time,
            data_count=1500,
            api_key="yabyRpmCIUkfFekmvSzCuoBHGz8uWkPIOWthlRUxREJVwXt3",
            api_secret="hiTXS8iyenJSJUivJ4Vw1C2e6zXRIZm5k6fU1Y6M1V90Ngtkf6hArUhREbAAdw76O4CQMTEP"
        )

permutation = Permutation(config)
hyper_parameters = {}
async def start():
  await permutation.run(hyper_parameters, Strategy)
 
asyncio.run(start())


