import time
import pytz
import requests
import pandas as pd
from datetime import datetime

endpoints = [
        "coinglass|1d|futures/topLongShortAccountRatio/history?exchange=Bybit&symbol=BTCUSDT&interval=1h",
        #"coinglass|1d|futures/openInterest/ohlc-history?exchange=Binance&symbol=BTCUSDT&interval=1h",
        #"cryptoquant|btc/market-data/funding-rates?window=hour&exchange=binance"
]

API_URL = "https://api.datasource.cybotrade.rs"

start_time = int(
    datetime(year=2023, month=1, day=1, tzinfo=pytz.timezone("UTC")).timestamp() * 1000
)
current_quota = 0
reset_time = 0
all_quota = 10000
for topic in endpoints:
    try:
        print(
            f"all_quota: {all_quota}, current_quota : {current_quota}, reset_time: {reset_time}"
        )
        if all_quota - current_quota <= 0:
            time.sleep(reset_time / 1000)
            print(f"Sleep for {reset_time}")
        provider = topic.split("|")[0]
        endpoint = topic.split("|")[-1]
        url = f"{API_URL}/{provider}/{endpoint}&start_time={start_time}&limit=50000"
        print(f"--------------------------------")
        print(f"{url}")
        response = requests.get(
            url,
            headers={"X-API-KEY": "yabyRpmCIUkfFekmvSzCuoBHGz8uWkPIOWthlRUxREJVwXt3"},
        )
        print(response.reason)
        print(response.status_code)
        print(response.text)
        all_quota = int(response.headers["X-Api-Limit"])
        current_quota = int(response.headers["X-Api-Limit-Remaining"])
        reset_time = int(response.headers["X-Api-Limit-Reset-Timestamp"])
        print(
            f"all_quota: {all_quota}, current_quota : {current_quota}, reset_time: {reset_time}"
        )
        data = response.json()["data"]
        df = pd.DataFrame(data)
        print(f"Done fetch {topic}")
        print(df)
    except Exception as e:
        print(response.status_code)
        print(f"Failed to fetch {topic} : {e}")

