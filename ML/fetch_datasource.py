import os
import pandas as pd
import numpy as np
import asyncio
import util
import cybotrade_datasource
from datetime import datetime, timezone
from dotenv import load_dotenv
import logging
load_dotenv()
API_KEY = "3FOSdsLW7nQmT8X7a2nRFkBEIwnsQnkjauet8IdBzKB2QDN0"

price_interval = '1h'
coinglass_interval = '1h'
crypto_interval = 'hour'
under_asset = 'eth'
rolling_window = 300

# ---------------------- change exchange ----------------------
exchange = 'binance'
#exchange = 'bybit'
#exchange = 'bitget'
#exchange = 'okx'
price_topic = exchange+'-linear|candle?symbol=BTCUSDT&interval='+price_interval
# ---------------------- change exchange ----------------------

# ------------------------------------------------------------- Coinglass -------------------------------------------------------------
# TOPIC = 'coinglass|coinbase-premium-index?interval=1h'
# TOPIC = 'coinglass|futures/top-long-short-account-ratio/history?exchange=Binance&symbol=BTCUSDT&interval=15m'
# TOPIC = 'coinglass|futures/hyperliquid/whale-alert' failed
# TOPIC = 'coinglass|futures/taker-buy-sell-volume/history?exchange=Binance&symbol=BTC&range=h1&interval=1d'
# TOPIC = 'coinglass|futures/liquidation/history?exchange=Binance&symbol=BTCUSDT&interval=1d'
# TOPIC = 'coinglass|futures/liquidation/aggregated-history?exchange_list=Binance&symbol=BTC&interval=1d'

# ------------------------------------------------------------- Coinglass -------------------------------------------------------------







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
# ------------------------------------------------------------- Coinglass -------------------------------------------------------------

# ------------------------------------------------------------- Cryptoquant -----------------------------------------------------------


# --------------------------- Exchange Flows 交易所流量 ---------------------------
#TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/reserve?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/netflow?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/inflow?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/outflow?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/transactions-count?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/exchange-flows/addresses-count?exchange='+exchange+'&window='+crypto_interval
# --------------------------- Exchange Flows 交易所流量 ---------------------------

# --------------------------- Flow Indicator 流量指标 ---------------------------
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-supply-ratio?exchange=binance&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-shutdown-index?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-whale-ratio?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/fund-flow-ratio?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/stablecoins-ratio?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-inflow-age-distribution?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-inflow-supply-distribution?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-inflow-cdd?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/exchange-supply-ratio?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/miner-supply-ratio?miner=f2pool&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/flow-indicator/bank-supply-ratio?bank=binance_pegged&window='+crypto_interval
# --------------------------- Flow Indicator 流量指标 ---------------------------

# --------------------------- Market Indicator 市场指标 ---------------------------
#TOPIC = 'cryptoquant|'+under_asset+'/market-indicator/estimated-leverage-ratio?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/market-indicator/stablecoin-supply-ratio?'+'&window=day'
#TOPIC = 'cryptoquant|'+under_asset+'/market-indicator/mvrv?'+'&window=day'
#TOPIC = 'cryptoquant|'+under_asset+'/market-indicator/sopr?'+'&window=day'
#TOPIC = 'cryptoquant|'+under_asset+'/market-indicator/sopr-ratio?'+'&window=day'
#TOPIC = 'cryptoquant|'+under_asset+'/market-indicator/realized-price?'+'&window=day'
#TOPIC = 'cryptoquant|'+under_asset+'/market-indicator/utxo-realized-price-age-distribution?'+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/market-indicator/estimated-leverage-ratio?exchange=binance&window=hour'
# --------------------------- Market Indicator 市场指标 ---------------------------


# --------------------------- Network Indicator 链上指标 ---------------------------
#TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/stock-to-flow?window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/nvt?window=day'
#TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/nvt-golden-cross?window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/nvm?window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/puell-multiple?window='+crypto_interval

#TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/spent-output-supply-distribution?window='+crypto_interval

# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/new-addresses?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/large-transactions?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/mean-transaction-value?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/median-transaction-value?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/transactions-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/utxo-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/pnl-utxo?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/utxo-count-supply-distribution?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/fees?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/supply?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/block-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/block-interval?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/difficulty?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/hashrate?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/fees-transaction?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/tokens-transferred?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-indicator/block-bytes?window='+crypto_interval
# --------------------------- Network Indicator 链上指标 ---------------------------

# --------------------------- Miner Flows 矿工流动 ---------------------------
#TOPIC = 'cryptoquant|'+under_asset+'/miner-flows/in-house-flow?miner=f2pool&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/miner-flows/miner-inflow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/miner-flows/miner-netflow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/miner-flows/miner-reserve?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/miner-flows/miner-to-exchange-flow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/miner-flows/miner-to-miner-flow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/miner-flows/miner-revenue?window='+crypto_interval
# --------------------------- Miner Flows 矿工流动 ---------------------------

# --------------------------- Inter-Entity Flows 实体间流动 ---------------------------
# TOPIC = 'cryptoquant|'+under_asset+'/inter-entity-flows/miner-to-miner?from_miner=f2pool&to_miner=all_miner&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/inter-entity-flows/miner-to-exchange?from_miner=f2pool&to_exchange=binance&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/inter-entity-flows/exchange-to-miner?from_exchange=binance&to_miner=f2pool&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/inter-entity-flows/miner-to-entity?from_miner=f2pool&to_entity=all&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/inter-entity-flows/entity-to-miner?from_entity=all&to_miner=f2pool&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/inter-entity-flows/entity-to-entity?from_entity=all&to_entity=all&window='+crypto_interval
# --------------------------- Inter-Entity Flows 实体间流动 ---------------------------

# --------------------------- Bank Flows 银行流动 ---------------------------
#TOPIC = 'cryptoquant|'+under_asset+'/bank-flows/addresses-count?bank=blockfi&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/bank-flows/bank-outflow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/bank-flows/bank-netflow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/bank-flows/bank-reserve?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/bank-flows/bank-to-exchange-flow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/bank-flows/bank-to-bank-flow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/bank-flows/bank-revenue?window='+crypto_interval
# --------------------------- Bank Flows 银行流动 ---------------------------

# --------------------------- Fund Data 基金数据 ---------------------------
#TOPIC = 'cryptoquant|'+under_asset+'/fund-data/market-price-usd?symbol=eth&window=day'
# TOPIC = 'cryptoquant|'+under_asset+'/fund-data/etf-outflow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/fund-data/etf-netflow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/fund-data/etf-reserve?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/fund-data/etf-to-exchange-flow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/fund-data/etf-to-etf-flow?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/fund-data/etf-revenue?window='+crypto_interval
# --------------------------- Fund Data 基金数据 ---------------------------

#TOPIC = 'cryptoquant|'+under_asset+'/eth2/phase0-success-rate?window=hour'
# --------------------------- Network Data 链上数据 ---------------------------
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/utxo-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/fees?window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/network-data/uncle-blockreward?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/transactions-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/addresses-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/tokens-transferred?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/block-bytes?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/block-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/block-interval?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/fees-transaction?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/difficulty?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/hashrate?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/active-addresses?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/new-addresses?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/large-transactions?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/network-data/mean-transaction-value?window='+crypto_interval
# --------------------------- Network Data 链上数据 ---------------------------

# --------------------------- Mempool Statistics 内存池统计 ---------------------------
# TOPIC = 'cryptoquant|'+under_asset+'/mempool-statistics/mempool-size?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/mempool-statistics/mempool-fee?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/mempool-statistics/mempool-count?window='+crypto_interval
# --------------------------- Mempool Statistics 内存池统计 ---------------------------

# --------------------------- Lightning Network Statistics 闪电网络统计 ---------------------------
#TOPIC = 'cryptoquant|'+under_asset+'/lightning/stats-in-total?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/lightning-network-statistics/channel-count?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/lightning-network-statistics/capacity?window='+crypto_interval
# --------------------------- Lightning Network Statistics 闪电网络统计 ---------------------------

# --------------------------- Market Data 市场数据 ---------------------------
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/price?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/ohlcv?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/volume?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/volatility?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/price-drawdown?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/price-drawup?window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/market-data/capitalization?window=day'
#TOPIC = 'cryptoquant|'+under_asset+'/market-data/open-interest?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/market-data/funding-rates?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/market-data/taker-buy-sell-stats?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/market-data/liquidations?exchange='+exchange+'&window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/market-data/coinbase-premium-index?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/ohlcv?exchange='+exchange+'&window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/price?window='+crypto_interval
#TOPIC = 'cryptoquant|'+under_asset+'/market-data/volume?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/price-drawdown?window='+crypto_interval
# TOPIC = 'cryptoquant|'+under_asset+'/market-data/price-drawup?window='+crypto_interval
# --------------------------- Market Data 市场数据 ---------------------------


# 其他类型（如 option, futures, etf, alerts, onchain）可根据文档进一步补充

# ------------------------------------------------------------- Cryptoquant -----------------------------------------------------------

# ------------------------------------------------------------- Glassnode -------------------------------------------------------------


# ------------------------------------------------------------- Glassnode -------------------------------------------------------------
async def fetch_datasource_data():
    data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY, 
        topic=TOPIC, 
        start_time=datetime(year=2021, month=1, day=1, tzinfo=timezone.utc),
        end_time=datetime(year=2024, month=12, day=30, tzinfo=timezone.utc)
    )
    df = pd.DataFrame(data)
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
    print(df)
    logging.info("datasource test set done!")
    path = f"src/{TOPIC.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}.csv"
    df.to_csv(path,index=False)

async def fetch_validation_set():
    validation_start = datetime(year=2024, month=12, day=30, tzinfo=timezone.utc)
    validation_end = datetime.now(timezone.utc)
    data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY,
        topic=TOPIC,
        start_time=validation_start,
        end_time=validation_end
    )
    df = pd.DataFrame(data)
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
    
    print(df)
    logging.info("datasource validation set done!")
    path = f"validation_sets/{TOPIC.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}_val.csv"
    df.to_csv(path, index=False)

async def fetch_price_data():
    data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY,
        topic=price_topic,
        start_time=datetime(year=2021, month=1, day=1, tzinfo=timezone.utc),
        end_time=datetime.now(timezone.utc)
    )
    df = pd.DataFrame(data)
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
    if 'close' in df.columns:
        df['change'] = df['close'].pct_change()
    print(df)
    logging.info("price test set done!")
    path = f"price_data/{price_topic.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}.csv"
    df.to_csv(path,index=False)

async def fetch_price_data_validation():
    data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY,
        topic=price_topic,
        start_time=datetime(year=2024, month=12, day=30, tzinfo=timezone.utc),
        end_time=datetime.now(timezone.utc)
    )
    df = pd.DataFrame(data)
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
    if 'close' in df.columns:
        df['change'] = df['close'].pct_change()
    print(df)
    logging.info("price validation set done!")
    path = f"validation_sets/{price_topic.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}_val.csv"
    df.to_csv(path,index=False)

async def main():
    # 测试集
    #await fetch_datasource_data()
    await fetch_price_data()
    #cryptoquant_test_path = f"src/{TOPIC.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}.csv"
    #price_test_path = f"src/{price_topic.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}.csv"
    #output_test_path = f"output/{TOPIC.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}_merged.csv"
    #df_cryptoquant = pd.read_csv(cryptoquant_test_path)
    
    #df_price = pd.read_csv(price_test_path)
    #df_price.to_csv(price_test_path, index=False)


    # 验证集
    #await fetch_validation_set()
    #await fetch_price_data_validation()
    #cryptoquant_val_path = f"validation_sets/{TOPIC.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}_val.csv"
    #price_val_path = f"validation_sets/{price_topic.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}_val.csv"
    #output_val_path = f"output/{TOPIC.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}_val_merged.csv"
    

asyncio.run(main())

