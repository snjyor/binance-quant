import ccxt
from time import sleep
import pandas as pd
from datetime import timedelta
from runtime_interval import next_run_interval_time
pd.set_option('expand_frame_repr',False)

binance = ccxt.binance()
binance.load_markets()


def get_binance_date(symbol='BTC/USDT',time_interval='1h'):
    next_run_time = next_run_interval_time(time_interval)
    while True:
        try:
            ohlcv = binance.fetch_ohlcv(symbol=symbol, timeframe=time_interval)
            df = pd.DataFrame(ohlcv)
            df.rename(columns={0: 'candle_begin_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'},
                      inplace=True)
            df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'], unit='ms') + timedelta(hours=8)
            # print(df)
            df = df[df['candle_begin_time'] < pd.to_datetime(next_run_time)]  # 取运行时间之前的数据，因为运行时间的K根还没结束，没有收盘价
            return df
        except:
            print('价格数据获取失败，正在重新获取……')
            sleep(1)
        no_newest_date = df[df['candle_begin_time'] == next_run_time - timedelta(minutes=int(time_interval.strip('m')))]   # 与整列时间进行对比找出符合的时间
        if no_newest_date.empty:
            print('没有最新数据，尝试重新获取……')
            continue
        else:
            break

# get_bitfinex_date('ETH/USD','1h')
