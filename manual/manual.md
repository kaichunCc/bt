# Manual

# Orders


# Strategy
## Methods
### related Orders
* buy
* sell
* close
* cancel
* notify_order

# Data feed
## normal data feeds
* Yahoo (online or already saved to a file)
* VisualChart (see www.visualchart.com
* Backtrader CSV (own cooked format for testing)
* Generic CSV support
  
## Lines Expand data

```
from backtrader.feeds import GenericCSVData

class GenericCSV_PE(GenericCSVData):

    # Add a 'pe' line to the inherited ones from the base class
    lines = ('pe',)
```    

## Sizers
```
class SizerFix(SizerBase):
    params = (('stake', 1),)

addsizer(sizercls, *args, **kwargs)
    cerebro = bt.Cerebro()
    cerebro.addsizer(bt.sizers.SizerFix, stake=20)  # default sizer for strategies

addsizer_byidx(idx, sizercls, *args, **kwargs)
    cerebro = bt.Cerebro()
    cerebro.addsizer(bt.sizers.SizerFix, stake=20)  # default sizer for strategies

    idx = cerebro.addstrategy(MyStrategy, myparam=myvalue)
    cerebro.addsizer_byidx(idx, bt.sizers.SizerFix, stake=5)

    cerebro.addstrategy(MyOtherStrategy)
```
## help code
### open file
```
print(datapath)
f = open(datapath)
line = f.readline()
cnt = 0
while line:
    print(line)
    line = f.readline()
    cnt += 1
    if cnt ==5:
        break
f.close()
```

```
#print(self.position.__dict__)
```
