import talib as ta

def BBANDS_signal(df,para=[100,2]):
    '''
    =====产生交易信号：布林线策略
    ===布林线策略
    布林线中轨：n天收盘价的移动平均线
    布林线上轨：n天收盘价的移动平均线 + m * n天收盘价的标准差
    布林线上轨：n天收盘价的移动平均线 - m * n天收盘价的标准差
    当收盘价由下向上穿过上轨的时候，做多；然后由上向下穿过下轨的时候，平仓。
    当收盘价由上向下穿过下轨的时候，做空；然后由下向上穿过上轨的时候，平仓。
    '''

    # ===计算指标
    n = para[0]
    m = para[1]
    # 计算均线
    df['median'] = df['close'].rolling(n, min_periods=1).mean()

    # 计算上轨、下轨道
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)  # ddof代表标准差自由度
    df['upper'] = df['median'] + m * df['std']
    df['lower'] = df['median'] - m * df['std']

    # ===找出做多信号
    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    df.loc[condition1 & condition2, 'signal'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # ===找出做多平仓信号
    condition1 = df['close'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['close'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    df.loc[condition1 & condition2, 'signal'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # ===找出做空信号
    # condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    # condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    # df.loc[condition1 & condition2, 'signal'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空
    #
    # # ===找出做空平仓信号
    # condition1 = df['close'] > df['median']  # 当前K线的收盘价 > 中轨
    # condition2 = df['close'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    # df.loc[condition1 & condition2, 'signal'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # df.drop(['median', 'std', 'upper', 'lower'], axis=1, inplace=True)

    # =====由signal计算出实际的每天持有仓位
    # signal的计算运用了收盘价，是每根K线收盘之后产生的信号，到第二根开盘的时候才买入，仓位才会改变。
    df['pos'] = df['signal'].shift()
    df['pos'].fillna(method='ffill', inplace=True)
    df['pos'].fillna(value=0, inplace=True)  # 将初始行数的position补全为0
    return df

def ta_BBANDS_signal(df,para=[130,2,2,0]):
    timeperiod = para[0]
    nbdevup = para[1]
    nbdevdn = para[2]
    matype = para[3]

    # 计算均线
    df['upperband'],df['middleband'],df['lowerband'] = ta.BBANDS(df['close'],timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype)
    # ===找出做多信号
    condition1 = df['close'] > df['upperband']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upperband'].shift(1)  # 之前K线的收盘价 <= 上轨
    df.loc[condition1 & condition2, 'signal'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # ===找出做多平仓信号
    condition1 = df['close'] < df['middleband']  # 当前K线的收盘价 < 中轨
    condition2 = df['close'].shift(1) >= df['middleband'].shift(1)  # 之前K线的收盘价 >= 中轨
    df.loc[condition1 & condition2, 'signal'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # ===找出做空信号
    # condition1 = df['close'] < df['lowerband']  # 当前K线的收盘价 < 下轨
    # condition2 = df['close'].shift(1) >= df['lowerband'].shift(1)  # 之前K线的收盘价 >= 下轨
    # df.loc[condition1 & condition2, 'signal'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空
    #
    # # ===找出做空平仓信号
    # condition1 = df['close'] > df['middleband']  # 当前K线的收盘价 > 中轨
    # condition2 = df['close'].shift(1) <= df['middleband'].shift(1)  # 之前K线的收盘价 <= 中轨
    # df.loc[condition1 & condition2, 'signal'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    df.drop(['upperband', 'middleband', 'lowerband'], axis=1, inplace=True)

    # =====由signal计算出实际的每天持有仓位
    # signal的计算运用了收盘价，是每根K线收盘之后产生的信号，到第二根开盘的时候才买入，仓位才会改变。
    df['pos'] = df['signal'].shift()
    df['pos'].fillna(method='ffill', inplace=True)
    df['pos'].fillna(value=0, inplace=True)  # 将初始行数的position补全为0

    return df

def kdj_signal():
    pass
# print(help(ta.MA))
