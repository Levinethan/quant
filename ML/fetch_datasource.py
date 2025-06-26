import os
import pandas as pd
import numpy as np
import asyncio
import cybotrade_datasource
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
API_KEY = "CBfBYegqTPaE8qJukLTaBHgt9prjnZmR6Eqtv1rllbxgIdOy"

# ------------------------------------------------------------- Coinglass -------------------------------------------------------------
# TOPIC = 'bybit-linear|candle?symbol=BTCUSDT&interval=1d'
# TOPIC = 'coinglass|coinbase-premium-index?interval=1h'
TOPIC = 'coinglass|futures/top-long-short-account-ratio/history?exchange=Binance&symbol=BTCUSDT&interval=1d'

# ------------------------------------------------------------- Coinglass -------------------------------------------------------------

# ------------------------------------------------------------- Cryptoquant -----------------------------------------------------------
# cryptoquant_endpoint1 = 'cryptoquant|eth/market-data/coinbase-premium-index?window=hour&exchange=binance'
# cryptoquant_endpoint2 = 'cryptoquant|btc/inter-entity-flows/miner-to-miner?from_miner=f2pool&to_miner=all_miner&window=hour'
# ------------------------------------------------------------- Cryptoquant -----------------------------------------------------------

# ------------------------------------------------------------- Glassnode -------------------------------------------------------------


# ------------------------------------------------------------- Glassnode -------------------------------------------------------------


async def main():
    data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY, 
        topic=TOPIC, 
        start_time=datetime(year=2023, month=1, day=1, tzinfo=timezone.utc),
        end_time=datetime(year=2025, month=6, day=1, tzinfo=timezone.utc)
    )
    df = pd.DataFrame(data)
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
    print(df)
    path = f"src/{TOPIC.replace('|', '_').replace('/','_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}.csv"
    df.to_csv(path,index=False)
    

asyncio.run(main())

