import math
import numpy as np
from cybotrade.models import Position, OrderUpdate, OrderSide
from datetime import UTC, datetime
import requests
import pytz
import pandas as pd

def convert_ms_to_datetime(milliseconds):
    seconds = milliseconds / 1000.0
    return datetime.fromtimestamp(seconds, tz=UTC)


def get_mean(array):
    total = 0
    for i in range(0, len(array)):
        total += array[i]
    return total / len(array)


def get_stddev(array):
    total = 0
    mean = get_mean(array)
    for i in range(0, len(array)):
        minus_mean = math.pow(array[i] - mean, 2)
        total += minus_mean
    return math.sqrt(total / (len(array) - 1))


def get_rolling_mean(array, rolling_window):
    arr = [0] * (rolling_window - 1)
    rolling_mean = []
    for i in range(rolling_window, len(array) + 1):
        last_arr = array[i - rolling_window : i]
        rolling_mean.append(get_mean(last_arr))
    remove_nan_rolling_mean = np.nan_to_num(rolling_mean)
    return np.concatenate((arr, remove_nan_rolling_mean), axis=0)


def get_rolling_std(array, rolling_window):
    arr = [0] * (rolling_window - 1)
    rolling_std = []
    for i in range(rolling_window, len(array) + 1):
        last_arr = array[i - rolling_window : i]
        rolling_std.append(get_stddev(last_arr))
    remove_nan_rolling_std = np.nan_to_num(rolling_std)
    return np.concatenate((arr, remove_nan_rolling_std), axis=0)


def get_rolling_zscore(array, mean, stdev):
    rolling_zscore = []
    for i in range(0, len(array)):
        rolling_zscore.append((array[i] - mean[i]) / stdev[i])
    remove_nan_rolling_zscore = np.nan_to_num(rolling_zscore)
    return remove_nan_rolling_zscore


def get_rolling_sum(array, rolling_window):
    arr = [0] * (rolling_window - 1)
    rolling_sum = []
    for i in range(rolling_window, len(array) + 1):
        last_arr = array[i - rolling_window : i]
        rolling_sum.append(np.sum(last_arr))
    remove_nan_rolling_sum = np.nan_to_num(rolling_sum)
    return np.concatenate((arr, remove_nan_rolling_sum), axis=0)


def get_rolling_historical_volatility(array, rolling_window, sr_multiplier):
    price_change = [0]
    for i in range(1, len(array)):
        price_change.append(array[i] / array[i - 1] - 1)

    arr = [0] * (rolling_window - 1)
    rolling_std = []
    for i in range(rolling_window, len(price_change) + 1):
        last_arr = price_change[i - rolling_window : i]
        rolling_std.append(get_stddev(last_arr) * np.sqrt(365 * sr_multiplier))
    remove_nan_rolling_std = np.nan_to_num(rolling_std)
    return np.concatenate((arr, remove_nan_rolling_std), axis=0)


def calculate_ema(data, window):
    ema_values = [0.0]
    multiplier = 2 / (window + 1)  # EMA multiplier
    # Calculate the initial SMA (Simple Moving Average)
    sma = np.mean(data[:window])
    ema_values.append(sma)

    # Calculate the EMA for the remaining data points
    for i in range(window, len(data)):
        ema = (data[i] - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema)

    return np.array(ema_values)


def get_position_info(position: Position, entry_time):
    if position.short.quantity != 0.0:
        return {
            "side": "Short",
            "qty": position.short.quantity,
            "entry_price": position.short.avg_price,
            "entry_time": entry_time,
        }
    elif position.long.quantity != 0.0:
        return {
            "side": "Long",
            "qty": position.long.quantity,
            "entry_price": position.long.avg_price,
            "entry_time": entry_time,
        }
    else:
        return {"side": "Nothing", "qty": 0.0, "entry_price": 0.0, "entry_time": None}


def send_notification(message: str, chat_id: str, token: str):
    url = f"https://api.telegram.org/{token}/sendMessage?chat_id={chat_id}&text={message}"
    response = requests.get(url)
    return response.json()

def timestamp_to_datetime(timestamp: float) -> datetime:
    return datetime.fromtimestamp(timestamp / 1000.0, tz=pytz.timezone("UTC"))

def datetime_to_timestamp(dt: datetime) -> float:
    return int(dt.timestamp() * 1000)

def close(x,y) -> bool:
    QL_Epsilon = 2.2204460492503131e-016
    n = 42.0
    diff = abs(x - y)
    tolerance = QL_Epsilon * n
    return diff <= tolerance * abs(x) and diff <= tolerance * abs(y)

def dropColumn(df) -> pd.DataFrame:
    df_cleaned = df.drop(columns=[col for col in df.columns if 'high' in col or 'low' in col or 'open' in col or 'volume' in col])
    return df_cleaned

def renameColumn(df) -> pd.DataFrame:
    df_cleaned = df.rename(columns={'open':'Open','high':'High','low':'Low','close': 'Close','volume':'Volume'})
    return df_cleaned

