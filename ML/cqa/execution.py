from cybotrade.strategy import Strategy as BaseStrategy
from cybotrade.models import (
    RuntimeConfig,
    RuntimeMode,
    Exchange,
    Symbol,
    OrderSide,
    Position,
)
from cybotrade.permutation import Permutation

from datetime import datetime, timezone
import asyncio
import colorlog
import logging
import pandas as pd
import numpy as np
import util

TELEGRAM_TOKEN = ""
TELEGRAM_CHAT_ID = ""


# This is the strategy class you've written.
class Strategy(BaseStrategy):
    rolling_window = 10
    threshold = 0.001
    qty = 0.01
    symbol = Symbol(base="BTC", quote="USDT")
    exchange = Exchange.BybitLinear
    entry_exit_logic = "trend"
    column_name = "c"
    model = "zscore"

    def __init__(self):
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(f"%(log_color)s{Strategy.LOG_FORMAT}")
        )
        file_handler = logging.FileHandler("example.log")
        file_handler.setLevel(logging.INFO)
        super().__init__(log_level=logging.INFO, handlers=[handler, file_handler])
        util.send_msg_telegram_bot(
            bot_token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID, msg="Start BOT"
        )

    async def on_candle_closed(self, strategy, topic, symbol):
        logging.info(f"topic: {topic}")
        # candles closed what u want to do
        data = self.data_map[topic]
        # get data from self
        # convert into dataframe
        df = pd.DataFrame(data)
        # do calculation
        df["mean"] = df["close"].rolling(window=self.rolling_window).mean()
        df["std"] = df["close"].rolling(window=self.rolling_window).std()
        df["model_data"] = (df["close"] - df["mean"]) / df["std"]
        # generate latest signal
        model_data = df["model_data"].values
        pos = [0]
        for i in range(1, len(model_data)):
            # current model_data more than threshold , pos = 1
            if model_data[i] >= self.threshold:
                pos.append(1)
            # current model_data less than negative theshold , pos = -1
            elif model_data[i] <= -self.threshold:
                pos.append(-1)
            # current model_data within theshold and negative threshold , pos = previous pos
            else:
                pos.append(pos[-1])
        # check porduction position
        prod_pos = await strategy.position(exchange=self.exchange, symbol=self.symbol)
        logging.info(f"{topic} = {df}")
        logging.info(f"latest pos : {pos[-1]} and prod_pos : {prod_pos}")
        # if not placed, we open position
        # 1.) live position == long , latest signal == long ==> no need place order
        # 2.) live position == long , latest signal == short ==> close long open short
        # 3.) live position == short , latest signal == long ==> close short open long
        # 4.) live position == short , latest signal == short ==> no need place order
        # 5.) live position == nothing , latest signal == long ==> open long
        # 6.) live position == nothing , latest signal == short ==> open short
        if pos[-1] == 1:
            if prod_pos.short.quantity != 0.0:  # 3
                # close short open long
                need_to_place = (
                    prod_pos.short.quantity + self.qty
                )  # sum of short qty to close and new order qty to open
                await strategy.open(
                    exchange=self.exchange,
                    symbol=self.symbol,
                    side=OrderSide.Buy,
                    quantity=need_to_place,
                )
                logging.info(
                    f"[CLOSE_SHORT_OPEN_LONG] Placed {need_to_place} to {self.symbol} at {self.exchange}"
                )
                util.send_msg_telegram_bot(
                    bot_token=TELEGRAM_TOKEN,
                    chat_id=TELEGRAM_CHAT_ID,
                    msg=f"[CLOSE_SHORT_OPEN_LONG] Placed {self.qty} to {self.symbol.base} at {self.exchange}",
                )
            elif prod_pos.long.quantity == 0.0:  # 5
                # place long
                await strategy.open(
                    exchange=self.exchange,
                    symbol=self.symbol,
                    side=OrderSide.Buy,
                    quantity=self.qty,
                )
                logging.info(
                    f"[OPEN_LONG] Placed {self.qty} to {self.symbol.base} at {self.exchange}"
                )
                util.send_msg_telegram_bot(
                    bot_token=TELEGRAM_TOKEN,
                    chat_id=TELEGRAM_CHAT_ID,
                    msg=f"[OPEN_LONG] Placed {self.qty} to {self.symbol.base} at {self.exchange}",
                )
        elif pos[-1] == -1:
            if prod_pos.long.quantity != 0.0:  # 2
                # close long open short
                need_to_place = (
                    prod_pos.long.quantity + self.qty
                )  # sum of long qty to close and new order qty to open
                await strategy.open(
                    exchange=self.exchange,
                    symbol=self.symbol,
                    side=OrderSide.Sell,
                    quantity=need_to_place,
                )
                logging.info(
                    f"[CLOSE_LONG_OPEN_SHORT] Placed {need_to_place} to {self.symbol} at {self.exchange}"
                )
                util.send_msg_telegram_bot(
                    bot_token=TELEGRAM_TOKEN,
                    chat_id=TELEGRAM_CHAT_ID,
                    msg=f"[CLOSE_LONG_OPEN_SHORT] Placed {self.qty} to {self.symbol.base} at {self.exchange}",
                )
            elif prod_pos.short.quantity == 0.0:  # 6
                # open short
                await strategy.open(
                    exchange=self.exchange,
                    symbol=self.symbol,
                    side=OrderSide.Sell,
                    quantity=self.qty,
                )
                logging.info(
                    f"[OPEN_SHORT] Placed {self.qty} to {self.symbol} at {self.exchange}"
                )
                util.send_msg_telegram_bot(
                    bot_token=TELEGRAM_TOKEN,
                    chat_id=TELEGRAM_CHAT_ID,
                    msg=f"[OPEN_SHORT] Placed {self.qty} to {self.symbol.base} at {self.exchange}",
                )

    async def on_datasource_interval(self, strategy, topic, data_list):
        # candles closed what u want to do
        data = self.data_map[topic]
        # get data from self
        # convert into dataframe
        df = pd.DataFrame(data)
        df[self.column_name] = df[self.column_name].astype(float)
        # do calculation
        if self.model == "zscore":
            df["mean"] = df[self.column_name].rolling(window=self.rolling_window).mean()
            df["std"] = df[self.column_name].rolling(window=self.rolling_window).std()
            df["model_data"] = (df[self.column_name] - df["mean"]) / df["std"]
        elif self.model == "min_max_scaling":
            # write the formula
            # x_scaled = 2 * (x - x_min) / (x_max - x_min) - 1
            df["rolling_min"] = df[self.column_name].rolling(self.rolling_window).min()
            df["rolling_max"] = df[self.column_name].rolling(self.rolling_window).max()
            df["model_data"] = (
                2
                * (df[self.column_name] - df["rolling_min"])
                / (df["rolling_max"] - df["rolling_min"])
                - 1.0
            )
        # generate latest signal
        model_data = df["model_data"].values
        pos = [0]
        if self.entry_exit_logic == "trend":
            for i in range(1, len(model_data)):
                # current model_data more than threshold , pos = 1
                if model_data[i] >= self.threshold:
                    pos.append(1)
                # current model_data less than negative theshold , pos = -1
                elif model_data[i] <= -self.threshold:
                    pos.append(-1)
                # current model_data within theshold and negative threshold , pos = previous pos
                else:
                    pos.append(pos[-1])
        elif self.entry_exit_logic == "trend_close_at_zero":
            for i in range(1, len(model_data)):
                # current model_data more than threshold , pos = 1
                if model_data[i] >= self.threshold:
                    pos.append(1)
                # current model_data less than negative theshold , pos = -1
                elif model_data[i] <= -self.threshold:
                    pos.append(-1)
                elif (pos[-1] == 1 and model_data[i] <= 0.0) or (
                    pos[-1] == -1 and model_data[i] >= 0.0
                ):
                    pos.append(0)
                # current model_data within theshold and negative threshold , pos = previous pos
                else:
                    pos.append(pos[-1])
        elif self.entry_exit_logic == "mr":
            for i in range(1, len(model_data)):
                # current model_data more than threshold , pos = -1
                if model_data[i] >= self.threshold:
                    pos.append(-1)
                # current model_data less than negative theshold , pos = 1
                elif model_data[i] <= -self.threshold:
                    pos.append(1)
                # current model_data within theshold and negative threshold , pos = previous pos
                else:
                    pos.append(pos[-1])
        elif self.entry_exit_logic == "mr_close_at_zero":
            for i in range(1, len(model_data)):
                # current model_data more than threshold , pos = -1
                if model_data[i] >= self.threshold:
                    pos.append(-1)
                # current model_data less than negative theshold , pos = 1
                elif model_data[i] <= -self.threshold:
                    pos.append(1)
                # if current pos == 1 , model_data >= 0.0 , close long
                # if current pos == -1 , model_data <= 0.0 , close short
                elif (model_data[i] >= 0.0 and pos[-1] == 1) or (
                    model_data[i] <= 0.0 and pos[-1] == -1
                ):
                    pos.append(0)
                # current model_data within theshold and negative threshold , pos = previous pos
                else:
                    pos.append(pos[-1])
        # check porduction position
        try:
            prod_pos = await strategy.position(
                exchange=self.exchange, symbol=self.symbol
            )
            logging.info(f"{topic} = {df}")
            logging.info(f"latest pos : {pos[-1]} and prod_pos : {prod_pos}")
            # if not placed, we open position
            # 1.) live position == long , latest signal == long ==> no need place order
            # 2.) live position == long , latest signal == short ==> close long open short
            # 3.) live position == short , latest signal == long ==> close short open long
            # 4.) live position == short , latest signal == short ==> no need place order
            # 5.) live position == nothing , latest signal == long ==> open long
            # 6.) live position == nothing , latest signal == short ==> open short
            # 7.) live position == long , latest signal == nothing ==> close long
            # 8.) live position == short , latest signal == nothing ==> close short
            if pos[-1] == 1:
                if prod_pos.short.quantity != 0.0:  # 3
                    # close short open long
                    need_to_place = (
                        prod_pos.short.quantity + self.qty
                    )  # sum of short qty to close and new order qty to open
                    try:
                        await strategy.open(
                            exchange=self.exchange,
                            symbol=self.symbol,
                            side=OrderSide.Buy,
                            quantity=need_to_place,
                        )
                        logging.info(
                            f"[CLOSE_SHORT_OPEN_LONG] Placed {need_to_place} to {self.symbol} at {self.exchange}"
                        )
                        util.send_msg_telegram_bot(
                            bot_token=TELEGRAM_TOKEN,
                            chat_id=TELEGRAM_CHAT_ID,
                            msg=f"[CLOSE_SHORT_OPEN_LONG] Placed {self.qty} to {self.symbol.base} at {self.exchange}",
                        )
                    except Exception as e:
                        logging.error(f"Failed to CLOSE_SHORT_OPEN_LONG due to {e}")
                        util.send_msg_telegram_bot(
                            bot_token=TELEGRAM_TOKEN,
                            chat_id=TELEGRAM_CHAT_ID,
                            msg=f"[CLOSE_SHORT_OPEN_LONG] Failed to place order",
                        )
                elif prod_pos.long.quantity == 0.0:  # 5
                    try:
                        # place long
                        await strategy.open(
                            exchange=self.exchange,
                            symbol=self.symbol,
                            side=OrderSide.Buy,
                            quantity=self.qty,
                        )
                        logging.info(
                            f"[OPEN_LONG] Placed {self.qty} to {self.symbol} at {self.exchange}"
                        )
                        util.send_msg_telegram_bot(
                            bot_token=TELEGRAM_TOKEN,
                            chat_id=TELEGRAM_CHAT_ID,
                            msg=f"[OPEN_LONG] Placed {self.qty} to {self.symbol.base} at {self.exchange}",
                        )
                    except Exception as e:
                        logging.error(f"Failed to OPEN_LONG due to {e}")
            elif pos[-1] == -1:
                if prod_pos.long.quantity != 0.0:  # 2
                    try:
                        # close long open short
                        need_to_place = (
                            prod_pos.long.quantity + self.qty
                        )  # sum of long qty to close and new order qty to open
                        await strategy.open(
                            exchange=self.exchange,
                            symbol=self.symbol,
                            side=OrderSide.Sell,
                            quantity=need_to_place,
                        )
                        logging.info(
                            f"[CLOSE_LONG_OPEN_SHORT] Placed {need_to_place} to {self.symbol} at {self.exchange}"
                        )
                        util.send_msg_telegram_bot(
                            bot_token=TELEGRAM_TOKEN,
                            chat_id=TELEGRAM_CHAT_ID,
                            msg=f"[CLOSE_LONG_OPEN_SHORT] Placed {self.qty} to {self.symbol.base} at {self.exchange}",
                        )
                    except Exception as e:
                        logging.error(f"Failed to CLOSE_LONG_OPEN_SHORT due to {e}")
                elif prod_pos.short.quantity == 0.0:  # 6
                    try:
                        # open short
                        await strategy.open(
                            exchange=self.exchange,
                            symbol=self.symbol,
                            side=OrderSide.Sell,
                            quantity=self.qty,
                        )
                        logging.info(
                            f"[OPEN_SHORT] Placed {self.qty} to {self.symbol} at {self.exchange}"
                        )
                        util.send_msg_telegram_bot(
                            bot_token=TELEGRAM_TOKEN,
                            chat_id=TELEGRAM_CHAT_ID,
                            msg=f"[OPEN_SHORT] Placed {self.qty} to {self.symbol.base} at {self.exchange}",
                        )
                    except Exception as e:
                        logging.error(f"Failed to OPEN_SHORT due to {e}")
            else:
                if prod_pos.long.quantity != 0.0:
                    # close long
                    try:
                        await strategy.open(
                            exchange=self.exchange,
                            symbol=self.symbol,
                            side=OrderSide.Sell,
                            quantity=prod_pos.long.quantity,
                        )
                        logging.info(
                            f"[CLOSE_LONG] Placed {prod_pos.long.quantity} to {self.symbol} at {self.exchange}"
                        )
                        util.send_msg_telegram_bot(
                            bot_token=TELEGRAM_TOKEN,
                            chat_id=TELEGRAM_CHAT_ID,
                            msg=f"[CLOSE_LONG] Placed {prod_pos.long.quantity} to {self.symbol.base} at {self.exchange}",
                        )
                    except Exception as e:
                        logging.error(f"Failed to CLOSE_LONG due to {e}")
                elif prod_pos.short.quantity != 0.0:
                    # close short
                    try:
                        await strategy.open(
                            exchange=self.exchange,
                            symbol=self.symbol,
                            side=OrderSide.Buy,
                            quantity=prod_pos.short.quantity,
                        )
                        logging.info(
                            f"[CLOSE_SHORT] Placed {prod_pos.short.quantity} to {self.symbol} at {self.exchange}"
                        )
                        util.send_msg_telegram_bot(
                            bot_token=TELEGRAM_TOKEN,
                            chat_id=TELEGRAM_CHAT_ID,
                            msg=f"[CLOSE_SHORT] Placed {prod_pos.short.quantity} to {self.symbol.base} at {self.exchange}",
                        )
                    except Exception as e:
                        logging.error(f"Failed to CLOSE_SHORT due to {e}")

        except Exception as e:
            logging.error(f"Failed to fetch position due to {e}")


permutation = Permutation(
    RuntimeConfig(
        mode=RuntimeMode.LiveTestnet,
        candle_topics=[
            # "bybit-linear|candle?symbol=BTCUSDT&interval=1m"
        ],
        datasource_topics=[
            # "coinglass|futures/fundingRate/ohlc-history?exchange=Binance&symbol=BTCUSDT&interval=1h",
            "coinglass|futures/openInterest/ohlc-history?exchange=Binance&symbol=BTCUSDT&interval=1m",
            # "cryptoquant|btc/market-data/coinbase-premium-index?window=min"
        ],
        active_order_interval=1,
        data_count=1000,
        # api_key=api_key,
        api_key="",
        api_secret="",
        exchange_keys="./credentials.json",
    )
)

hyper_parameters = {}


async def start():
    await permutation.run(hyper_parameters, Strategy)


asyncio.run(start())

