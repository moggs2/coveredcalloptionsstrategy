"""This Python script shows 4 charts. The first chart is the price chart of a stock in comparison to a 
chart with dividends included. The second is the same just in percentage.
The third and fourth chart show absolute and in percentage the covered call strategy in comparison to the price chart. One time a month
a Call Option out of the money is sold. How far out of the money can be adjusted with basisstdprc parameter.
If the price is higher than the Basis of the option of last month,
the difference is subtracted, because of expiration. If no 1 month options are available, the script
chooses 3 month options. The script sells at the open on expiration date (3. Friday of every month) the new option. 
If 3. Firday is holiday the script chooses the Thursday before.

Requirements to run this script:
Python 3.6
Packages:
pandas_datareader
matplotlib
numpy
pandas
mibian
datetime"""

START='2015-02-01'     # Start date of the timeseries
END='2017-03-27'       # End date of the timeseries
SYMBOL="aapl"          # Stock, ETF Symbol from Yahoo
basisstdprc=0.5        # For Covered Call: Describes of standard deviation the Basis of the Option is out of the money.
                       # For instance: If the number is 0.5 the basis of the option is 0.5 (50%) of one standard deviation out of the money.
riskfreeinterest=0.5   # For Covered Call: The risk free interest rate.
PR = 20                # For Covered Call: The period for estimating the volatility of the options. For instance 20 means 20 days.

from pandas_datareader.data import get_data_yahoo
import argparse
import sys
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import numpy as np
import pandas as pd
import mibian as mb
from datetime import datetime
from pandas_datareader.data import Options

parser=argparse.ArgumentParser(description='Example')
parser.add_argument('count', action="store", type=int)


datahighlowclosevolume = get_data_yahoo(SYMBOL, start = START, end = END)[['Open','Close','Volume','High','Low']]
dividends=web.DataReader(SYMBOL, 'yahoo-dividends', START, END)
roc=ROC((datahighlowclosevolume), PR)
rocdaily=ROC((datahighlowclosevolume), 2)
std=STDDEV((rocdaily), PR)



def ROC(df, n):
    M = df['Close'].diff(n - 1)
    N = df['Close'].shift(n - 1)
    ROC = pd.Series(M / N*100, name = 'ROC')
    df = df.join(ROC)
    return df

def STDDEV(df, n):
    df = df.join(pd.Series(pd.rolling_std(df['ROC'], n)*15.87450786638754, name = 'STD'))
    return df

def DIVIDENDSROW(df,df2, n):
    df3=pd.merge(df,df2, how='outer', left_index=True, right_index=True)
    df3['Dividends'].fillna(0, inplace=True)
    df3['cum_sum'] = df3.Dividends.cumsum()
    df3['pricediv']=df3['cum_sum']+df3['Close']
    df3['pricedivprc']=df3['pricediv']/df3['Close'].iloc[0]*100-100
    df3['priceprc']=df3['Close']/df3['Close'].iloc[0]*100-100
    riskfreeinterestadj=riskfreeinterest-dividends['Dividends'].sum()*250*100/std['Close'].count()
    
    basisprice=1000000
    option1=[]
    for index, row in df3.iterrows():
        
        if (index.day>20 and index.day<28 and index.weekday()==4):
               
            basispricenew=row['STD']*basisstdprc*row['Open']/100+row['Open']
            riskfreeinterestadjprc=riskfreeinterestadj/row['Open']
            if row['Close']>basisprice:
                option1.append(basisprice-row['Close']+mb.BS([row['Open'], basispricenew, 1, 30], volatility=row['STD']).callPrice)
                basisprice=basispricenew
            else:
                option1.append(mb.BS([row['Open'], basispricenew, riskfreeinterestadjprc, 30], volatility=row['STD']).callPrice)
                basisprice=basispricenew

                    

        elif (index.day>19 and index.day<27 and index.weekday()==3):
            basispricenew=row['STD']*basisstdprc*row['Open']/100+row['Open']
            riskfreeinterestadjprc=riskfreeinterestadj/row['Open']
            if row['Close']>basisprice:
                option1.append(basisprice-row['Close']+mb.BS([row['Open'], basispricenew, 1, 30], volatility=row['STD']).callPrice)
                basisprice=basispricenew
            else:
                option1.append(mb.BS([row['Open'], basispricenew, riskfreeinterestadjprc, 30], volatility=row['STD']).callPrice)
                basisprice=basispricenew        
        else:
            option1.append(0)
    
            
    df3['option1']=option1
     
    
    basisprice=1000000
    option3=[]
    for index, row in df3.iterrows():
        
        if (index.day>20 and index.day<28 and index.weekday()==4):
               
            basispricenew=row['STD']*basisstdprc*row['Open']/100+row['Open']
            riskfreeinterestadjprc=riskfreeinterestadj/row['Open']
            if row['Close']>basisprice:
                option3.append(basisprice-row['Close']+mb.BS([row['Open'], basispricenew, 1, 90], volatility=row['STD']).callPrice)
                basisprice=basispricenew
            else:
                option3.append(mb.BS([row['Open'], basispricenew, riskfreeinterestadjprc, 90], volatility=row['STD']).callPrice)
                basisprice=basispricenew

                    

        elif (index.day>19 and index.day<27 and index.weekday()==3):
            basispricenew=row['STD']*basisstdprc*row['Open']/100+row['Open']
            riskfreeinterestadjprc=riskfreeinterestadj/row['Open']
            if row['Close']>basisprice:
                option3.append(basisprice-row['Close']+mb.BS([row['Open'], basispricenew, 1, 90], volatility=row['STD']).callPrice)
                basisprice=basispricenew
            else:
                option3.append(mb.BS([row['Open'], basispricenew, riskfreeinterestadjprc, 90], volatility=row['STD']).callPrice)
                basisprice=basispricenew        
        else:
            option3.append(0)
            
    df3['option3']=option3
    
    df3['option1_cum']=df3.option1.cumsum()
    df3['option3_cum']=df3.option3.cumsum()
    df3['pricediv_option1']=df3['option1_cum']+df3['pricediv']
    df3['pricediv_option3']=df3['option3_cum']+df3['pricediv']
    
    df3['pricediv_option1_prc']=df3['pricediv_option1']/df3['Close'].iloc[0]*100-100
    df3['pricediv_option3_prc']=df3['pricediv_option3']/df3['Close'].iloc[0]*100-100
                
    return df3

def main():

    optionschain = Options(SYMBOL, 'yahoo')
    dataoptionschain=optionschain.get_all_data()
    optionsexpiries=optionschain.expiry_dates

    if (optionsexpiries[1].month-optionsexpiries[0].month)>1:
        take3=1
    else:
        take3=0    

    
    

    
    
    
    divacc=DIVIDENDSROW(std,dividends,PR)

    plt.figure(1,figsize=(8, 12))
    plt.subplot(211)
    plt.title("Price/Price Dividend Comparison")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.plot(datahighlowclosevolume['Close']);
    plt.ylim(datahighlowclosevolume['Close'].min()*0.98,datahighlowclosevolume['Close'].max()*1.02)

    plt.figure(1,figsize=(8, 12))
    plt.subplot(211)
    plt.plot(divacc['pricediv']);
    plt.ylim(divacc['Close'].min()*0.98,divacc['pricediv'].max()*1.02)

    plt.figure(2,figsize=(8, 12))
    plt.subplot(211)
    plt.title("Price/Price Dividend Comparison in %")
    plt.xlabel("Date")
    plt.ylabel("%")
    plt.plot(divacc['priceprc']);
    plt.ylim(divacc['priceprc'].min()*0.98,divacc['pricedivprc'].max()*1.02)

    plt.figure(2,figsize=(8, 12))
    plt.subplot(211)
    plt.plot(divacc['pricedivprc']);
    plt.ylim(divacc['priceprc'].min()*0.98,divacc['pricedivprc'].max()*1.02)

    plt.figure(3,figsize=(8, 12))
    plt.subplot(211)
    plt.title("Price/Price + Dividend + Call Option Short (Covered Call) Comparison")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.plot(datahighlowclosevolume['Close']);
    plt.ylim(datahighlowclosevolume['Close'].min()*0.98,datahighlowclosevolume['Close'].max()*1.02)

    if take3==0:

        plt.figure(3,figsize=(8, 12))
        plt.subplot(211)
        plt.plot(divacc['pricediv_option1']);
        plt.ylim(divacc['Close'].min()*0.98,divacc['pricediv_option1'].max()*1.02)
        
    else:
        plt.figure(3,figsize=(8, 12))
        plt.subplot(211)
        plt.plot(divacc['pricediv_option3']);
        plt.ylim(divacc['Close'].min()*0.98,divacc['pricediv_option3'].max()*1.02)

    plt.figure(4,figsize=(8, 12))
    plt.subplot(211)
    plt.title("Price/Price + Dividend + Call Option Short (Covered Call) Comparison in %")
    plt.xlabel("Date")
    plt.ylabel("%")
    plt.plot(divacc['priceprc']);
    plt.ylim(divacc['priceprc'].min()*0.98,divacc['pricedivprc'].max()*1.02)

    if take3==0:

        plt.figure(4,figsize=(8, 12))
        plt.subplot(211)
        plt.plot(divacc['pricediv_option1_prc']);
        plt.ylim(divacc['priceprc'].min()*0.98,divacc['pricediv_option1_prc'].max()*1.02)
        
    else:
        plt.figure(4,figsize=(8, 12))
        plt.subplot(211)
        plt.plot(divacc['pricediv_option3_prc']);
        plt.ylim(divacc['priceprc'].min()*0.98,divacc['pricediv_option3_prc'].max()*1.02)

if __name__=="__main__":
    sys.exit(main())
