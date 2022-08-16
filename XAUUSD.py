from msilib import datasizemask
from turtle import xcor
import pandas as pd 
import numpy as np 
import MetaTrader5 as mt 
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pickle
import time
import os


##################################################  Logics involved    ###################################################################

#candle type specification
def specify_candle_type7(open_price, close_price):
    if open_price < close_price:
        return 'bullish'
    elif open_price > close_price:
        return 'bearish'
    else:
        return'doji' 


#trend detection
def trend_detection7(data7):
    try:
        x = []
        for i in range(data7.shape[0]):
            counter  = 0
            y = []
            a = []
            z = []
            b = []
            while counter <= 15:
            
                if data7.iloc[i-counter]['candle_type'] == ('bearish'):
                    v = abs(data7.iloc[i-counter]['open'] - data7.iloc[i-counter]['close'])
                    a.append(v)
                    y.append(y)
                elif data7.iloc[i-counter]['candle_type'] == ('bullish'):
                    m = abs(data7.iloc[i-counter]['close'] - data7.iloc[i-counter]['open'])
                    b.append(m)
                    z.append(z)
                counter = counter + 1
            if len(z) < len(y) and sum(b) < sum(a):
                x.append('downtrend')
            elif len(z) > len(y) and sum(b) > sum(a):
                x.append('uptrend')
            else:
                x.append('ranging')
            y.clear()
            a.clear()
            z.clear()
            b.clear()
            counter = 0
    except IndexError:
        pass
        #print('nan')
    trend =  pd.DataFrame(x, columns=['trend'])
    trend.to_csv('trend7.csv')
    return trend

def Pinbar(data7):
    p = []
    pb = []
    pl = []
    try:
        for i in range(data7.shape[0]):
            counter = 0
            while counter <= 15:
                # bullish body
                u = abs(data7.iloc[i-counter]['close'] - data7.iloc[i-counter]['open'])
                # upper wick
                u1 = abs(data7.iloc[i-counter]['high'] - data7.iloc[i-counter]['close'])

                # bearish body
                d = abs(data7.iloc[i-counter]['open'] - data7.iloc[i-counter]['close'])
                # upper wick
                d1 = abs(data7.iloc[i-counter]['high'] - data7.iloc[i-counter]['open'])
                
                if (data7.iloc[i-counter]['low'] < data7.iloc[i-counter-1]['low'] and data7.iloc[i-counter]['low'] < data7.iloc[i-counter+1]['low'] and data7.iloc[i-counter][u] > data7.iloc[i-counter][u1]):
                    return 'bullish pinbar'
                    #pb.append(data7.iloc[i-counter]['time'])
                elif (data7.iloc[i-counter]['high'] > data7.iloc[i-counter-1]['high'] and data7.iloc[i-counter]['high'] > data7.iloc[i-counter+1]['high'] and data7.iloc[i-counter][d] < data7.iloc[i-counter][d1]):
                    return 'bearish pinbar'
                    #pl.append(data7.iloc[i-counter]['time'])
                else:
                    pass
    except IndexError:
        pass
    pinbar =  pd.DataFrame(p, columns=['pinbar'])
    pinbar.to_csv('pinbar7.csv')
    return pinbar


#logic for higherhighs , higherlows , lowerhighs and lower lows
def hh_ll_hl_lh7(data7):
    x =  []
    try:
        for i in range(data7.shape[0]):
            n = 0
            m = 0
            if data7.iloc[i]['trend'] == ('downtrend'):
                if data7.iloc[i-2]['candle_type'] == ('bearish') and data7.iloc[i-1]['candle_type'] == ('bearish') and data7.iloc[i]['candle_type'] == ('bearish'):
                    x.append('motion')
                    #print('motion')
                elif data7.iloc[i-2]['low'] > data7.iloc[i-1]['low'] and data7.iloc[i]['low'] > data7.iloc[i-1]['low']:
                    x.append('lowerlow')
                    #print('lowerlow')
                elif data7.iloc[i-2]['candle_type'] == ('bullish') and data7.iloc[i-1]['candle_type'] == ('bullish') and data7.iloc[i]['candle_type'] == ('bullish'):
                    x.append('motion')
                    #print('motion')
                elif data7.iloc[i-2]['high'] < data7.iloc[i-1]['high'] and data7.iloc[i]['high'] < data7.iloc[i-1]['high']:
                    x.append('lowerhigh')
                   # print('lowerlow')
                else:
                    #print('motion')
                    x.append('motion')
                
            elif data7.iloc[i]['trend'] == ('uptrend'):
                if data7.iloc[i-2]['candle_type'] == ('bullish') and data7.iloc[i-1]['candle_type'] == ('bullish') and data7.iloc[i]['candle_type'] == ('bullish'):
                    x.append('motion')
                    #print('motion')
                elif data7.iloc[i-2]['high'] < data7.iloc[i-1]['high'] and data7.iloc[i]['high'] < data7.iloc[i-1]['high']:
                    x.append('higherhigh')
                    #print('higherhigh')
                elif data7.iloc[i-2]['candle_type'] == ('bearish') and data7.iloc[i-1]['candle_type'] == ('bearish') and data7.iloc[i]['candle_type'] == ('bearish'):
                    x.append('motion')
                    #print('motion')
                elif data7.iloc[i-2]['low'] > data7.iloc[i-1]['low'] and data7.iloc[i]['low'] > data7.iloc[i-1]['low']:
                    x.append('higherlow')
                    #print('higherlow')
                else:
                    x.append('motion')
                    #print('motion')
            elif data7.iloc[i]['trend'] == ('ranging'):
                x.append('motion')
                #print('motion'
    
    

    except IndexError:
        x.append('motion')
    
    highlow = pd.DataFrame(x, columns = ['highlow'])
    highlow.to_csv('highlow7.csv')

    return highlow


#logic Break of Structure
def Break_Of_Struct7(data7):
    x =  []

    try:
        
        for i in range(data7.shape[0]):
            c = 0
            c2 = 0 - c
            if data7.iloc[i-c]['highlow'] == ('higherhigh'):
                
                while  (data7.iloc[i-c]['high'] > data7.iloc[i-c-c2]['high']) and (data7.iloc[i-c-c2]['highlow'] != ('higherhigh')):
                    if (data7.iloc[i-c]['high'] < data7.iloc[i-c-c2]['high']) and (data7.iloc[i-c-c2]['highlow'] == ('higherhigh')) and data7.iloc[i-c]['high'] < data7.iloc[i-c-c2]['close']:
                        break
                    #print("motion")
                    x.append('motion')
                    c2 = c2 - 1
                #print('UP')   
                x.append('UPBOS')
            elif data7.iloc[i-c]['highlow'] == ('lowerlow'):
                while  (data7.iloc[i-c]['low'] < data7.iloc[i-c-c2]['low']) and (data7.iloc[i-c-c2]['highlow'] != ('lowerlow')):
                    if (data7.iloc[i-c]['low'] > data7.iloc[i-c-c2]['low']) and (data7.iloc[i-c-c2]['highlow'] == ('lowerlow')) and data7.iloc[i-c]['low'] > data7.iloc[i-c-c2]['close']:
                        break
                    #print("motion")
                    x.append('motion')
                    c2 = c2 - 1
                #print('DOWN')
                x.append('DOWNBOS')   
            else:
                #print("motion")
                x.append('motion')
            c = c2


    except IndexError:
        x.append('motion')   
    BOS = pd.DataFrame(x, columns = ['BOS'])
    BOS.to_csv('BOS7.csv')
    return BOS



def POB7(data7):   
    x =  []
    z = []
    l = []
    try:
        
        for i in range(data7.shape[0]):
            c = 0
            c2 = 0 - c
            if data7.iloc[i+c]['highlow'] == ('higherlow'):
                
                while  (data7.iloc[i+c]['low'] > data7.iloc[i+c+c2]['low']) and (data7.iloc[i+c+c2]['highlow'] != ('higherlow')):
                    if (data7.iloc[i+c]['low'] < data7.iloc[i+c+c2]['low']) and (data7.iloc[i+c+c2]['highlow'] == ('higherlow')):
                        break
                    #print("motion")
                    x.append('motion')
                    z.append(data7.iloc[i+c+c2]['time'])
                    c2 = c2 + 1
                #print('UP')   
                x.append('HL')
            elif data7.iloc[i+c]['highlow'] == ('lowerhigh'):
                while  (data7.iloc[i+c]['high'] < data7.iloc[i+c+c2]['high']) and (data7.iloc[i+c+c2]['highlow'] != ('lowerlow')):
                    if (data7.iloc[i+c]['high'] > data7.iloc[i+c+c2]['low']) and (data7.iloc[i+c+c2]['highlow'] == ('lowerlow')) :
                        break
                    #print("motion")
                    x.append('motion')
                    c2 = c2 + 1
                #print('DOWN')
                l.append(data7.iloc[i+c+c2]['time'])
                x.append('LH')   
            else:
                #print("motion")
                x.append('motion')
            c = c2

    except IndexError:
        x.append('motion') 
    pob1 = pd.DataFrame(x, columns = ['OB']) 
    tm = pd.DataFrame(z, columns = ['1minties entries buy'])
    tm2 = pd.DataFrame(l, columns = ['1minties entries sell'])
    tm.to_csv('TM7.csv')
    tm2.to_csv('TM727.csv')
    pob1.to_csv('POB7.csv')
    return pob1,tm,tm2


def sync_time7(data7, BTF, STF,PTM):
    
    pm = np.array(PTM['pinbar']).copy()
    time = np.array(data7['time']).copy()
    time2 = np.array(BTF['1minties entries buy']).copy()
    time7 = np.array(STF['1minties entries sell']).copy()
    x = []
    try:
        for i in time:
            for j in time2:
                if i == j:
                    if len(x) > 1:
                        x.pop()
                    x.append(1)
            for k in time7:
                if k == i:
                    if len(x) > 1:
                        x.pop()
                    x.append(-1)
            for m in pm:
                if m == 'bullish pinbar':
                    if len(x) > 1:
                        x.pop()
                    x.append(1)
                elif m == 'bearish pinbar':
                    if len(x) > 1:
                        x.pop()
                    x.append(-1)
            else:
                x.append(0)         
    except IndexError:
        x.append(0)

    x = pd.DataFrame(x, columns = ['signal'] )
    
    x.to_csv('signal7.csv')   

    return x

#send market order
# function to send a market order
def market_order7(symbol, volume, order_type,):
    if order_type == 'buy':
        tick = mt.symbol_info_tick(symbol)
        order_dict = {'buy': 0, 'sell': 1}
        price_dict = {'buy': tick.ask, 'sell': tick.bid}
        point = mt.symbol_info(symbol).point
        

        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_dict[order_type],
            "price": price_dict[order_type],
            "sl": price_dict[order_type] - 1000 * point,
            "tp": price_dict[order_type] + 2000* point,
            "magic": 100,
            "comment": "python market order",
            "type_time": mt.ORDER_TIME_GTC,
            
        }

        order_result = mt.order_send(request)
        print(order_result)
        logs = ['Order: ', str(order_result),
                '-------\n' ]
        with open('logsXAUUUD.txt', 'a') as f:
            for log in logs:
                f.write(log)
                f.write('\n')
        f.close()


        return order_result
    if order_type == 'sell':
        tick = mt.symbol_info_tick(symbol)
        order_dict = {'buy': 0, 'sell': 1}
        price_dict = {'buy': tick.ask, 'sell': tick.bid}
        point = mt.symbol_info(symbol).point
        

        request = {
            "action": mt.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_dict[order_type],
            "price": price_dict[order_type],
            "sl": price_dict[order_type] + 1000 * point,
            "tp": price_dict[order_type] - 2000 * point,
            "magic": 100,
            "comment": "python market order",
            "type_time": mt.ORDER_TIME_GTC,
            
        }

        order_result = mt.order_send(request)
        print(order_result)
        logs = ['Order: ', str(order_result),
                '-------\n' ]
        with open('logsXAUUSD.txt', 'a') as f:
            for log in logs:
                f.write(log)
                f.write('\n')
        f.close()

        return order_result


# function to close an order base don ticket id
def close_order7(ticket):
    positions = mt.positions_get()

    for pos in positions:
        tick = mt.symbol_info_tick(pos.symbol)
        type_dict = {0: 1, 1: 0}  # 0 represents buy, 1 represents sell - inverting order_type to close the position
        price_dict = {0: tick.ask, 1: tick.bid}

        if pos.ticket == ticket:
            request = {
                "action": mt.TRADE_ACTION_DEAL,
                "position": pos.ticket,
                "symbol": pos.symbol,
                "volume": pos.volume,
                "type": type_dict[pos.type],
                "price": price_dict[pos.type],
                "magic": 100,
                "comment": "python close order",
                "type_time": mt.ORDER_TIME_GTC,
                
            }

            order_result = mt.order_send(request)
            print(order_result)

            return order_result

    return 'Ticket does not exist'

def Consolidation(data7):
    x = []
    try:
        for i in range(data7.shape[0]):
            counter = 0
            y = []
            while counter <= 20:
                if data7.iloc[i-counter]['trend'] == ('ranging'):
                    y.append(1)
                else:
                    pass
                counter = counter + 1
                
            if len(y) >= 5:
                x.append('invalid')
            elif len(y) <= 4:
                x.append('valid')      
            counter = 0
    except IndexError:
        x.append('motion')
    consolidation = pd.DataFrame(x, columns = ['consolidation'])
    consolidation.to_csv('consolidation7.csv')
    return consolidation
def Validity(data7):
    print('val')
    x = []
    for i in range(data7.shape[0]):
        if data7.iloc[i]['consolidation'] == ('valid') and data7.iloc[i]['OB'] == ('HL'):
            x.append('sell')
        elif data7.iloc[i]['consolidation'] == ('valid') and data7.iloc[i]['OB'] == ('LH'):
            x.append('buy')
        else:
            x.append('motion')
    validity = pd.DataFrame(x, columns=['validity'])
    validity.to_csv('validity7.csv')
    return validity


def signaling7(data7):   
    data7['candle_type'] = np.vectorize(specify_candle_type7)(data7['open'], data7['close'])

    trend_detection7(data7)

    trend = pd.read_csv('trend7.csv')
    data7 = data7.join(trend,how ='left', lsuffix='_left')
    data7 = data7.dropna()
    data7.drop(labels=['Unnamed: 0'], axis=1)


    hh_ll_hl_lh7(data7)
    highlow = pd.read_csv('highlow7.csv')
    data7 = data7.join(highlow,how ='left', lsuffix='_left')
    data7 = data7.dropna()
    data7.drop(labels=['Unnamed: 0'], axis=1)


    Break_Of_Struct7(data7)
    BOS = pd.read_csv('BOS7.csv')
    data7 = data7.join(BOS,how ='left', lsuffix='_left')
    data7 = data7.dropna()
    data7.drop(labels=['Unnamed: 0'], axis=1)


    POB7(data7)
    pob1 = pd.read_csv('POB7.csv')
    data7 = data7.join(pob1,how ='left', lsuffix='_left')
    data7.drop(labels=['Unnamed: 0'], axis=1)

    Consolidation(data7)
    consolidation =pd.read_csv('consolidation7.csv')
    data7 = data7.join(consolidation,how ='left', lsuffix='_left')
    data7.drop(labels=['Unnamed: 0'], axis=1)

    Validity(data7)
    validity =pd.read_csv('validity7.csv')
    data7 = data7.join(validity,how ='left', lsuffix='_left')
    data7.drop(labels=['Unnamed: 0'], axis=1)

    data7.to_csv('data7.csv')

    Pinbar(data7)
    pinbar = pd.read_csv('pinbar7.csv')
    data7 = data7.join(pinbar,how ='left', lsuffix='_left')
    data7.drop(labels=['Unnamed: 0'], axis=1)


    

def get_data7(symbol, timeframe,roll_period):
    ohlc_data7 = pd.DataFrame(mt.copy_rates_from_pos(symbol,
                                                timeframe,
                                                1,
                                                roll_period))
    #fig = px.line(ohlc_data7, x=ohlc_data7['time'], y=ohlc_data7['close'])
    ohlc_data7['time']=pd.to_datetime(ohlc_data7['time'], unit='s')
    ohlc_data7.to_csv('ohlc_data7.csv')
    return ohlc_data7
def get_data72(symbol, timeframe,roll_period):
    ohlc_data7 = pd.DataFrame(mt.copy_rates_from_pos(symbol,
                                                timeframe,
                                                1,
                                                roll_period))
    #fig = px.line(ohlc_data7, x=ohlc_data7['time'], y=ohlc_data7['close'])
    ohlc_data7['time']=pd.to_datetime(ohlc_data7['time'], unit='s')
    ohlc_data7.to_csv('ohlc_data727.csv')
    return ohlc_data7

def get_exposure7(symbol):
    positions = mt.positions_get(symbol=symbol)
    if positions:
        pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        exposure = pos_df['volume'].sum()

        return exposure



print('code complete')
###################################################### Beginning of code (runtime)###########################################################
if __name__ == '__main__':
    symbol = 'XAUUSDm'
    timeframe = mt.TIMEFRAME_M30
    VOLUME = 0.01
    roll_period = 100
    
    mt.initialize()
    #mt.login(63556488, password='Pass1234')
    while True:
        cwd = os.getcwd()
        mydir = cwd
        for f in os.listdir(mydir):
            if not f.endswith("7.csv"):
                continue
            os.remove(os.path.join(mydir, f))


        exposure = get_exposure7(symbol)
        
        get_data7(symbol, timeframe,roll_period)
        ohlc_data7 = pd.read_csv('ohlc_data7.csv')
        data7 = ohlc_data7.copy()
        print('code complete')

        signaling7(data7)
        print('code complete')
        
        symbol = 'XAUUSDm'
        timeframe = mt.TIMEFRAME_M1
        get_data72(symbol, timeframe, roll_period)

        ohlc_data7 = pd.read_csv('ohlc_data727.csv')
        data7 = ohlc_data7.copy()
        tm = pd.read_csv('TM7.csv')
        tm2 = pd.read_csv('TM727.csv')
        pinbar = pd.read_csv('pinbar7.csv')
        print('code complete')


        sync_time7(data7, tm, tm2, pinbar)

        real = pd.read_csv('signal7.csv')
        data7 = data7.join(real,how ='left', lsuffix='_left')
        print('code complete')
        
        sig = pd.read_csv('data7.csv')
        
        last_close = sig.iloc[-1].validity

        direction = 'flat'
        if last_close == 'buy':
            direction = 'buy'
        elif last_close == "sell":
            direction = 'sell'
        elif last_close == 'motion':
            direction = 'pass'


        
        # trading logic
        if direction == 'buy':
            # if we have a BUY signal, close all short positions
            #for pos in mt.positions_get():
            #    if pos.type == 1:  # pos.type == 1 represent a sell order
                #    close_order7(pos.ticket)

            # if there are no open positions, open a new long position
            #if not mt.positions_total():
            market_order7(symbol, VOLUME, direction)

        elif direction == 'sell':
            # if we have a SELL signal, close all short positions
            #for pos in mt.positions_get():
            #    if pos.type == 0:  # pos.type == 0 represent a buy order
            #        close_order7(pos.ticket)

            # if there are no open positions, open a new short position
            #if not mt.positions_total():
            market_order7(symbol, VOLUME, direction)

                
        
        elif direction == 'pass':
            pass

        current_time = datetime.now()
        str_current_time = str(current_time)
        logs = ['time: ', str_current_time,
                '-------\n' 
                'symbol: ', str(symbol),
                '-------\n'
                'exposure: ', str(exposure),
                '-------\n'
                'signal: ', str(direction),
                '-------\n',
                '-------\n']
        with open('logsXAUUSD.txt', 'a') as f:
            for log in logs:
                f.write(log)
                f.write('\n')
        f.close()
        print('time: ', datetime.now())
        print('symbol: ', symbol)
        print('exposure: ', exposure)
        print('signal: ', direction)
        print('-------\n')


        cwd = os.getcwd()
        mydir = cwd
        for f in os.listdir(mydir):
            if not f.endswith("7.csv"):
                continue
            os.remove(os.path.join(mydir, f))
        time.sleep(60)

    #fig.show()
    #ohlc_data7
    

#######################################################