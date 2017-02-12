"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY

    # handle missing values
    prices_all.fillna(method="ffill", inplace=True)
    prices_all.fillna(method="bfill", inplace=True)    
    
    
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio


    #create an erray with the size of portfolio

    sizeOfSyms=len(syms) # get the size of portfolio
    allocs = np.asarray([1./sizeOfSyms] * sizeOfSyms)
    
    def f(allocs):
        port_val = prices_SPY # add code here to compute daily portfolio values
        normalized=prices/prices.ix[0,:]
        alloced=normalized*allocs
        pos_vals=alloced*1
        port_val=pos_vals.sum(axis=1)
        dr=port_val.copy()
        dr[1:]=(port_val[1:]/port_val[:-1].values)-1
        dr.ix[0]=0
        adr=dr[1:].sum()/(len(dr)-1)
        sddr=dr[1:].std()
        sr=-((adr-0)/sddr)*252**0.5
        return sr
    
    cons = ({'type': 'eq', 'fun': lambda x:  1 - sum(x)})
    bnds = tuple((0,1) for x in allocs)
    
    min_result=spo.minimize(f,allocs,method='SLSQP', bounds=bnds, constraints=cons, options={'disp':True})
    
    allocs=min_result.x
    
    port_val = prices_SPY # add code here to compute daily portfolio values
    normalized=prices/prices.ix[0,:]
    alloced=normalized*allocs
    pos_vals=alloced*1
    port_val=pos_vals.sum(axis=1)    
    
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats

    # Get daily portfolio value
    dr=port_val.copy()
    dr[1:]=(port_val[1:]/port_val[:-1].values)-1
    dr.ix[0]=0
    cr=(port_val[len(port_val)-1]/port_val[0])-1
    adr=dr[1:].sum()/(len(dr)-1)
    sddr=dr[1:].std()
    sr=((adr-0)/sddr)*252**0.5 
    
    
    
    
    

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        normalized_price=df_temp/df_temp.ix[0,:]
        plot1=normalized_price.plot(title="Stock Prices")
        plot1.set_xlabel("Date")
        plot1.set_ylabel("Price")
        plt.savefig('comparison_optimal.png')
        pass

    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    start_date = dt.datetime(2008,01,01)
    end_date = dt.datetime(2009,12,31)
    symbols =  ['IBM', 'X', 'HNZ', 'XOM', 'GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
