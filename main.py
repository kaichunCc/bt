from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime
from os import spawnl
import os.path
import sys

import backtrader as bt

'''
    数据清洗：
        删除抖动点

    趋势: (时间跨度变化幅度，曲线斜率，时间跨度)
'''
class TrendStrategy(bt.Strategy):
    params = dict(buyRateStd = 0.005, statSpan = 8, stopSurplusStd = 0.1, stopLossStd = -0.08, positionDuration = 10)

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        now = self.data.openinterest[0]
        statSpanBegin = self.data.openinterest(-1 * self.params.statSpan)
        self.percent = (now - statSpanBegin) * 1.0 / now

        self.order = None
        self.buyPrice = None
        self.gain = 0

    def next(self):
        #self.log('Close, %.2f' % self.data.close[0])
        
        if self.order:
            return
        
        # 没有持仓
        if not self.position:
            if self.percent > self.params.buyRateStd:
                self.order = self.buy()
                self.log('trigger Buy')
        else:
            stopSurplus = False
            stopLoss = False

            gain_price = self.data.openinterest[0] - self.buyPrice
            gain_percent = gain_price * 1.0 / self.buyPrice
            
            if (gain_price > 0 and gain_percent > self.params.stopSurplusStd):
                stopSurplus = True
            elif(gain_price < 0 and gain_percent > self.params.stopLossStd):
                stopLoss = True

            if len(self) >= (self.bar_executed + self.params.positionDuration) or (stopSurplus or stopLoss):
                self.order = self.sell()
                self.log('trigger Sell')            

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % (order.executed.price))
                
                self.gain += order.executed.pnl

            self.bar_executed = len(self)
            self.buyPrice = self.data.close[0]
            
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
   
class SizerFix(bt.SizerBase):
    params = (('stake', 1), )

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    
    cerebro.addstrategy(TrendStrategy)
    cerebro.addsizer(bt.sizers.SizerFix, stake = 300)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, '..\\backtrader\datas\orcl-1995-2014.txt')

    data = bt.feeds.GenericCSVData(
        dataname=datapath,
        fromdate=datetime.datetime(2000, 1, 1),
        todate=datetime.datetime(2000, 3, 30),
        dtformat=('%Y-%m-%d'),
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        openinterest=5,
        volume=6,
        reverse=False,
        separator=",",
        headers=True)
    
    cerebro.adddata(data)

    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(commission=0.0001)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Finnal Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.plot()