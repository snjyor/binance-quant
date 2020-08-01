import pandas as pd
import ccxt
from time import sleep
from runtime_interval import sleep_to_next_runtime
from get_binance_kline_date import get_binance_date
from trade_signal import ta_BBANDS_signal
from binance_send_email import send_email

pd.set_option('expand_frame_repr',False)

'''交易流程'''
# 更新账户信息
# 获取实时数据
# 根据最新数据计算交易信号
# 根据目前仓位，买卖信息，结束本次循环，或进行交易
# 交易

'''基本参数'''
time_interval = '1h'
symbol = 'BTC/USDT'
base_coin = symbol.split('/')[-1]
trade_coin = symbol.split('/')[0]

binance = ccxt.binance({'apiKey':'mAvwEZwlRZX14x5DOMz8SPB3QiXFbydRlXjK7TSyt5ZBCS7ybWBCrkUFaCNVISMb',
                        'secret':'kxdPaU4J2Z0QMtaScHX00NAd7zE6DrC0M4MPJyTcqB2K1PZZ2H7i4U2jumwty2vA'})
try:
    binance.load_markets()
except:
    print('交易所加载失败，正在重试……')
    sleep(1)

while True:
    # 邮箱信息
    email_title = ''
    email_content = ''
    try:
        # 获取账户信息
        # balance = binance.fetch_balance()['total']      # 获取现货账户
        balance = binance.fetch_partial_balance('free')

        # print(balance)
        trade_coin_amount = balance[trade_coin]
        base_coin_amount = balance[base_coin]
        print('正在交易币对：{0}'.format(symbol))
        if trade_coin_amount > 0.001:
            print(trade_coin + '的数量为：', trade_coin_amount)
        elif base_coin_amount > 0:
            print(base_coin + '的数量为：', base_coin_amount)
    except:
        print('获取账户信息失败，正在重新获取……')
        sleep(1)
        continue

    # 睡眠到下次运行时间
    next_run_time = sleep_to_next_runtime(time_interval)

    #获取实时数据
    df = get_binance_date(symbol, time_interval)
    #产生交易信号
    df = ta_BBANDS_signal(df,para=[130,2,2,0])
    signal = df.iloc[-1]['signal']
    # print(df)
    print('交易信号：', signal)

    # 买入
    if signal == 1 and trade_coin_amount < 0.001:
        for i in range(5):
            try:
                print('正在执行买入操作……')
                price = binance.fetch_ticker(symbol)['bid']
                amount = base_coin_amount / price
                if base_coin_amount > 10:
                    order = binance.create_order(symbol, type='LIMIT', side='BUY', amount=amount, price=price)
                    email_title += '买入' + trade_coin + '报告'
                    email_content += '买入数量:' + str(order['amount']) + '\n'
                    email_content += '成交价格:' + str(order['price']) + '\n'
                    email_content += '成交时间:' + str(order['datetime'])
                    print('订单信息：\n', order)
                    print('{0}已买入{1}个！单价为{2}USDT/个'.format(trade_coin, order['amount'], order['price']))
                    print(email_title)
                    print(email_content)
                    send_email(email_title, email_content)
                    break
                else:
                    print('买入数量过少，最低为10美元！')
                    break
            except:
                print('创建买入订单失败，1s后重新尝试……')
                sleep(1)
    # 卖出
    elif signal == 0 and trade_coin_amount != 0:
        for i in range(5):
            try:
                print('正在执行卖出操作……')
                price = binance.fetch_ticker(symbol)['ask']
                amount = trade_coin_amount
                sell_mount = price * amount
                if sell_mount > 10:
                    order = binance.create_order(symbol, type='LIMIT', side='SELL', amount=amount, price=price)
                    email_title += '卖出' + trade_coin + '报告'
                    email_content += '卖出数量:' + str(order['amount']) + '\n'
                    email_content += '成交价格:' + str(order['price']) + '\n'
                    email_content += '成交时间:' + str(order['datetime'])
                    print('订单信息：\n', order)
                    print('{0}已卖出{1}个！单价为{2}USDT/个'.format(trade_coin, order['amount'], order['price']))
                    print(email_title)
                    print(email_content)
                    send_email(email_title,email_content)
                    break
                else:
                    print('卖出数量过少，最低价值10美元！')
                    sleep(10)
                    break

                # {'info': {'symbol': 'ETHUSDT', 'orderId': 593664189, 'orderListId': -1, 'clientOrderId': 'XM7CJta6U1llk2v4RyjdiJ', 'transactTime': 1579005692930, 'price': '151.49000000', 'origQty': '0.09365000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'NEW', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL'}, 'id': '593664189', 'timestamp': 1579005692930, 'datetime': '2020-01-14T12:41:32.930Z', 'lastTradeTimestamp': None, 'symbol': 'ETH/USDT', 'type': 'limit', 'side': 'sell', 'price': 151.49, 'amount': 0.09365, 'cost': 0.0, 'average': None, 'filled': 0.0, 'remaining': 0.09365, 'status': 'open', 'fee': None, 'trades': None}
            except:
                print('创建卖出订单失败，1s后重新尝试……')
                sleep(1)
    else:
        print('无交易信号，下一周期重试……')
        continue

    # 每天零点发一次邮件
    # if next_run_time.hour / 1 == 0:
    #     send_email()

    print('*********本次交易结束**********')
