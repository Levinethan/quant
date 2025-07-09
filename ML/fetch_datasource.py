import os
import pandas as pd
import numpy as np
import asyncio
import cybotrade_datasource
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
API_KEY = "3FOSdsLW7nQmT8X7a2nRFkBEIwnsQnkjauet8IdBzKB2QDN0"

coinglass_interval = 'h'
crypto_interval = 'day'

under_asset = 'btc'

# ------------------------------------------------------------- Exchange -------------------------------------------------------------
# OPIC = 'binance-linear|candle?symbol=BTCUSDT&interval=1d'
# TOPIC = 'bybit-linear|candle?symbol=BTCUSDT&interval=1d'
# TOPIC = 'bitget-linear|candle?symbol=BTCUSDT&interval=1d'
# TOPIC = 'okx-linear|candle?symbol=BTCUSDT&interval=1d'
# ------------------------------------------------------------- Coinglass -------------------------------------------------------------
# TOPIC = 'coinglass|coinbase-premium-index?interval=1h'
# TOPIC = 'coinglass|futures/top-long-short-account-ratio/history?exchange=Binance&symbol=BTCUSDT&interval=1d'
# TOPIC = 'coinglass|futures/hyperliquid/whale-alert' failed
# TOPIC = 'coinglass|futures/taker-buy-sell-volume/history?exchange=Binance&symbol=BTC&range=h1&interval=1d'
# TOPIC = 'coinglass|futures/liquidation/history?exchange=Binance&symbol=BTCUSDT&interval=1d'
# TOPIC = 'coinglass|futures/liquidation/aggregated-history?exchange_list=Binance&symbol=BTC&interval=1d'



# --------------------------------------------- No work ----------------------------------------------------------
# TOPIC = 'coinglass|hk-etf/bitcoin/flow-history'
# TOPIC = 'coinglass|exchange/chain/tx/list'
# TOPIC = 'coinglass|exchange/assets?exchange=Binance'
# TOPIC = 'coinglass|option/max-pain?symbol=BTC&exchange=Deribit'
# TOPIC = 'coinglass|option/info?symbol=BTC'
# TOPIC = 'coinglass|option/exchange-oi-history?symbol=BTC&unit=USD&range=h1'
# TOPIC = 'coinglass|option/exchange-vol-history?symbol=BTC&unit=USD'
# TOPIC = 'coinglass|hyperliquid/whale-position'
# TOPIC = 'coinglass|futures/orderbook/large-limit-order?exchange=Binance&symbol=BTCUSDT'
# TOPIC = 'coinglass|futures/orderbook/history?exchange=Binance&symbol=BTCUSDT&interval=1h&limit=1'
# TOPIC = 'coinglass|futures/liquidation/coin-list?exchange=Binance'
# TOPIC = 'coinglass|futures/liquidation/order?exchange=Binance&symbol=BTC&min_liquidation_amount=10000'
# TOPIC = 'coinglass|futures/liquidation/map?exchange=Binance&symbol=BTCUSDT&range=1d'
TOPIC = ''
# ------------------------------------------------------------- Coinglass -------------------------------------------------------------

# ------------------------------------------------------------- Cryptoquant -----------------------------------------------------------

# TOPIC = 'cryptoquant|'+under_asset+'/inter-entity-flows/miner-to-miner?from_miner=f2pool&to_miner=all_miner&window=hour'
# TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/reserve?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/netflow?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/inflow?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/outflow?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/transactions-count?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/addresses-count?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/in-house-flow?exchange=binance&window='+crypto_interval


#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/mpi?window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-shutdown-index?exchange=binance&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-whale-ratio?exchange=binance&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/fund-flow-ratio?exchange=binance&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/stablecoins-ratio?exchange=binance&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-inflow-age-distribution?exchange=binance&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-inflow-supply-distribution?exchange=binance&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-inflow-cdd?exchange=binance&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-supply-ratio?exchange=binance&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/miner-supply-ratio?miner=f2pool&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/bank-supply-ratio?bank=binance_pegged&window='+crypto_interval


# TOPIC = 'cryptoquant|'+under_asset+'/network-data/utxo-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/fees?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/supply?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/transactions-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/addresses-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/tokens-transferred?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/block-bytes?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/block-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/block-interval?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/fees-transaction?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/difficulty?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/hashrate?window='+crypto_interval


# TOPIC = 'cryptoquant|'+under_asset+'/network-data/?window='+crypto_interval

# TOPIC = 'cryptoquant|'+under_asset+'/market-data/capitalization?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/open-interest?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/funding-rates?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/taker-buy-sell-stats?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/liquidations?exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/coinbase-premium-index?window='+crypto_interval


# ------------------------------------------------------------- Cryptoquant -----------------------------------------------------------

# ------------------------------------------------------------- Glassnode -------------------------------------------------------------


# ------------------------------------------------------------- Glassnode -------------------------------------------------------------


async def main():
    data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY, 
        topic=TOPIC, 
        start_time=datetime(year=2021, month=1, day=1, tzinfo=timezone.utc),
        end_time=datetime(year=2024, month=11, day=30, tzinfo=timezone.utc)
    )
    df = pd.DataFrame(data)
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
    print(df)
    path = f"src/{TOPIC.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}.csv"
    df.to_csv(path,index=False)
    

asyncio.run(main())

