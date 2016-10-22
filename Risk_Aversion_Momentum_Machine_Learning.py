"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from collections import deque, Counter
import numpy as np

def initialize(context):
    """
    Called once at the start of the algorithm. 
    """   
    context.spy = symbols('SPY')
    context.stocks = symbols('XLY',
                             'XLF',
                             'XLK',
                             'XLE',
                             'XLV',
                             'XLI',
                             'XLP',
                             'XLB',
                             'XLU')
    context.historical_bars = 100
    context.feature_window = 5
    schedule_function(order_handling, date_rules.week_start())
def order_handling(context,data):
    """
    Called every minute.
    """
    free = 0.0
    winners = []
    # i = 0
    for stock in context.stocks:
        prices = data.history(stock, 'price', context.historical_bars, '1d')
        std = prices.std()
        ma5 = prices[-5:].mean()
        ma10 = prices[-10:].mean()
        ma13 = prices[-13:].mean()
        ma20 = prices[-20:].mean()
        ma50 = prices[-50:].mean()
        ma100 = prices[-100:].mean()
        # record(str(stock), prices[-1])
        # if std > .5:
        window = context.feature_window
        # else:
        #     window = context.feature_window*2
        start_bar = window
        price_list = prices.tolist()
        X = []
        y = []
        bar = start_bar
        while bar < len(price_list) - 1:
            try:
                end_price = price_list[bar+1]
                start_price = price_list[bar]
                
                price_window = price_list[bar-window: bar]
                features = np.around(np.diff(price_window)/price_window[:-1]*100.0,1)
                label = 0
                if end_price > start_price:
                    label = 1
                elif end_price < start_price:
                    label = -1
                X.append(features)
                y.append(label)
                
                    
            except Exception as e:
                print('feature creation', str(e))
            bar += 1
        clf1 = RandomForestClassifier(10) #Use 10 (default) classifiers for machine learning
        clf2 = LinearSVC()
        clf3 = NuSVC()
        clf4 = LogisticRegression()
        
        last_prices = price_list[-window:]
        current_features = np.around(np.diff(last_prices)/last_prices[:-1]*100.0,1)
        
        X.append(current_features)
        X = preprocessing.scale(X) # try best to scale everything relative to each other
        
        current_features = X[-1]
        X = X[:-1]
        clf1.fit(X, y)
        clf2.fit(X, y)
        # clf3.fit(X, y)
        clf4.fit(X, y)
        p1 = clf1.predict(current_features)[0] # one-element np array
        p2 = clf2.predict(current_features)[0]
        # p3 = clf3.predict(current_features)[0]
        p4 = clf4.predict(current_features)[0]
        # print(Counter([p1,p2,p4]).most_common(1))
        p = Counter([p1,p2,p4]).most_common(1)[0][0]
        allocation = .11
        # if i != 8: # if not at last stock
        #     extra = free/(9-(i+1))
        # else:
        #     extra = free
        if data.can_trade(stock):
            if p > 0:
                print("open long" + str(stock))
                # order_target_percent(stock,allocation)
                winners.append(stock)
                # free -= extra
            elif p < 0:
                print("close long" + str(stock))
                order_target_percent(stock,0)
                free += allocation
        # i += 1
    if len(winners) > 0:
        extra_alloc =  free/len(winners)
        for stock in winners:
            order_target_percent(stock, .11 + extra_alloc)
            
                

                
    
