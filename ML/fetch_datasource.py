import os
import pandas as pd
import asyncio
import cybotrade_datasource
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
API_KEY = "CBfBYegqTPaE8qJukLTaBHgt9prjnZmR6Eqtv1rllbxgIdOy"


# TOPIC = 'bybit-linear|candle?symbol=BTCUSDT&interval=1d'
# TOPIC = 'cryptoquant|btc/inter-entity-flows/miner-to-miner?from_miner=f2pool&to_miner=all_miner&window=hour'
TOPIC = 'coinglass|coinbase-premium-index?interval=1h'
#TOPIC = 'cryptoquant|eth/market-data/coinbase-premium-index?window=hour&exchange=binance'
async def main():
    data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY, 
        topic=TOPIC, 
        start_time=datetime(year=2024, month=1, day=1, tzinfo=timezone.utc),
        end_time=datetime(year=2025, month=1, day=1, tzinfo=timezone.utc)
    )
    df = pd.DataFrame(data)
    df['start_time'] = pd.to_datetime(df['start_time'], unit='ms')
    print(df)
    df.to_csv(f"src/{TOPIC.replace('|', '_').replace('?', '_').replace('&', '_').replace('-', '_').replace('=', '_')}.csv",index=False)
    

asyncio.run(main())

