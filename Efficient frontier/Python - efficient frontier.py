#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 08:32:59 2021

@author: alicjagadowska
"""

import numpy as np
import pandas as pd
from pandas_datareader import stooq
import matplotlib.pyplot as plt


# creating dictionary with top10 NASDAQ companies and theirs symbols
companies = {'MSFT.US':'Microsoft Corporation', 'AAPL.US':'Apple Inc.', 
             'GOOGL.US':'Aplhabet Inc.', 'FB.US':'Facebook', 
             'AMZN':'Amazon.com Inc.', 'INTC':'Intel Corp', 
             'CSCO':'Cisco Systems Inc.', 'CMCSA':'Comcast Corp',
             'PEP':'PepsiCo Inc.', 'ADBE':'Adobe Inc.'}


# creating a list of symbols
tickers = sorted([ticker for ticker in companies.keys()])

# creating a data frame
df = stooq.StooqDailyReader(symbols = tickers, start='JAN-01-2015', 
                            end = 'DEC-31-2020').read()

# selecting only the close price
close_price = df['Close']

# sorting the data by index 2015-2020
close_price = close_price.sort_index(0)

#plotting daily prices changes
daily = close_price.plot(title = 'TOP10 NASDAQ')
daily.set(ylabel = 'Price in $')

# calculating daily % returns - volatility
returns = close_price.pct_change()
returns.plot()

# creating relative series of the companies to the NASDAQ 

# importing Nasaq index price data from csv file
index_price = pd.read_csv('../Efficient Frontier//^IXIC.csv')

# amending the data
index_price['Date'] = pd.to_datetime(index_price['Date'])

index_price = index_price.set_index('Date')
index_price = index_price[:'2020-12-31']
index_price = index_price['Close']
index_price = index_price.rename('Nasdaq')

# joingin the data
nasdaq_prices = pd.concat([close_price, index_price.reindex(close_price.index)], axis = 1)

#removing empty data
nasdaq_prices = nasdaq_prices.dropna(axis=0)

# creating relative series of the companies to the NASDAQ 
relative = pd.DataFrame()
for stock in nasdaq_prices.columns:
    if stock != 'Nasdaq':
        relative[stock + ' rel'] = nasdaq_prices[stock]/nasdaq_prices['Nasdaq']
        
# ploting relative performance of the copanies
rel_perf = relative.plot(title = 'Relative companies performance')
rel_perf.set(ylabel = 'Price')


# %%
# Efficient Frontier Portfolio Optimisation

#chossing the copanies for our portfolio
port_companies = ['AAPL.US', 'AMZN', 'GOOGL.US', 'PEP']
portfolio = close_price[port_companies]

#calculating data required for the analysis
cov_matrix = portfolio.pct_change().cov()
corr_matrix = portfolio.pct_change().corr()

#cacluating random portfolio variance
weights = pd.DataFrame([0.2, 0.4, 0.15, 0.25],
                       index = port_companies, columns=['weight'])


portfolio_var = cov_matrix.mul(weights['weight'], axis = 0).mul(weights['weight'],
                                                                axis = 1).sum().sum()

# calculating the expected annualised portfolio return
expected_re = portfolio.pct_change(250).mean()
port_return = (expected_re*weights.T).sum(axis = 1)

# simulation of random weights, calculating return and volatility
simulations = 10000

port_R = []  # returns
port_V = []   # volaility
port_weights = []

for port in range(simulations):
    w = np.random.random(len(portfolio.columns))
    w = w/np.sum(w)
    port_weights.append(w)
    returns = np.dot(w, expected_re.values)
    port_R.append(returns)
    var = cov_matrix.mul(w, axis = 0).mul(w, axis = 1).sum().sum()
    sd = np.sqrt(var)
    port_V.append(sd*np.sqrt(250))
    
# plotting the efficient frontier

portfolios = pd.DataFrame(port_weights, columns = port_companies)
portfolios['returns'] = port_R
portfolios['volatility'] = port_V
portfolios.plot.scatter('volatility', 'returns', s=5, alpha = 0.4)

# maximazing Sharpe ratio - finding the optimal portfolio

rf = 0.001  # rate for 52 weeks tresury bill in US for 26th jan21

#maxSharp indicates what weight should be used to omtimize the portfolio
maxSharp = portfolios.iloc[((portfolios['returns']-rf)/portfolios['volatility']).idxmax()]

#plotting the results
plt.subplots(figsize=(10,10))
plt.scatter(portfolios['volatility'], portfolios['returns'], s = 5, marker = 'o',
            alpha = 0.4)
plt.scatter(maxSharp['volatility'], maxSharp['returns'],
            color='r', marker='*', s=40)


