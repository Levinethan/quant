import os
import pandas as pd
import glob
import re

# 交易所列表，可根据需要扩展
EXCHANGES = ['binance', 'bybit', 'okx', 'bitget']

def extract_exchange(filename):
    for ex in EXCHANGES:
        if ex in filename.lower():
            return ex
    return None

def find_candle_files(exchange, directory):
    # 查找该交易所的所有candle/ohlcv/price文件
    files = glob.glob(os.path.join(directory, '*.csv'))
    return [
        f for f in files
        if exchange in os.path.basename(f).lower() and
        (re.search(r'candle|ohlcv|price', f, re.IGNORECASE))
    ]

def batch_merge_with_close(main_dir='validation_sets', output_dir='validation_sets/merged'):
    os.makedirs(output_dir, exist_ok=True)
    main_files = glob.glob(os.path.join(main_dir, '*.csv'))
    merged_count = 0

    for main_file in main_files:
        base = os.path.basename(main_file)
        exchange = extract_exchange(base)
        if not exchange:
            print(f"⚠️ 未识别到交易所: {base}")
            continue

        # 查找该交易所的所有价格文件
        price_files = find_candle_files(exchange, main_dir)
        if not price_files:
            print(f"⚠️ 未找到价格文件: {exchange} for {base}")
            continue

        # 合并所有价格数据
        price_dfs = []
        for pf in price_files:
            try:
                price_dfs.append(pd.read_csv(pf))
            except Exception as e:
                print(f"❌ 读取价格文件失败: {pf} {e}")
        if not price_dfs:
            print(f"⚠️ 没有可用的价格数据: {base}")
            continue
        df_price = pd.concat(price_dfs, ignore_index=True)
        # 取收盘价列名
        close_col = None
        for col in ['close', 'close_price', 'price', 'c']:
            if col in df_price.columns:
                close_col = col
                break
        if close_col is None:
            print(f"⚠️ 价格文件未找到收盘价列: {price_files}")
            continue
        # 合并
        df_price = df_price[['start_time', close_col]].rename(columns={close_col: 'close'})
        df_price['start_time'] = pd.to_datetime(df_price['start_time'])
        df_price = df_price.drop_duplicates('start_time')
        df_main = pd.read_csv(main_file)
        df_main['start_time'] = pd.to_datetime(df_main['start_time'])
        df_merged = pd.merge(df_main, df_price, on='start_time', how='left')
        out_file = os.path.join(output_dir, base)
        df_merged.to_csv(out_file, index=False)
        print(f"✅ 合并完成: {out_file}")
        merged_count += 1

    print(f"\n🎉 共合并 {merged_count} 个主数据文件（自动匹配交易所和收盘价）")

if __name__ == '__main__':
    batch_merge_with_close()
