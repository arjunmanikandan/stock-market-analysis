import pandas as pd
import numpy as np
import math

def get_df_by_symbol(stock_data,config):
    filtered_stock_data = stock_data[stock_data["SYMBOLS"].isin(config['symbols_or_industries']) | 
    stock_data["INDUSTRY"].isin(config['symbols_or_industries']) | stock_data["SYMBOL_INDUSTRY"].isin(config['symbols_or_industries']) ].copy()
    filtered_stock_data['TIMESTAMP'] = pd.to_datetime(stock_data['TIMESTAMP'], format='%d-%b-%Y')
    filtered_stock_data = filtered_stock_data.sort_values(by=["TIMESTAMP"])
    return filtered_stock_data

def filter_period(df,freq):
    df = pd.concat([df.head(1),df.tail(1)],axis=0).reset_index(drop=True)
    df = df.groupby(f"{freq}").agg({"OPEN":"first","CLOSE":"last",'SYMBOLS':'first', 'SERIES':'first',
    'TOTTRDQTY':"sum", 'TIMESTAMP':'first',"HIGH":"max","LOW":"min"}).reset_index(drop=True)
    return df

def filter_data_daily(filtered_stock_data):
    return filtered_stock_data

def filter_data_weekly(filtered_stock_data):
    start_date_index = filtered_stock_data.head(1).index[0]
    start_date = filtered_stock_data.loc[start_date_index,"TIMESTAMP"]
    filtered_stock_data['Week_No'] = (((filtered_stock_data["TIMESTAMP"].dt.isocalendar().year - start_date.year) * 52) 
    + filtered_stock_data['TIMESTAMP'].dt.isocalendar().week)
    df_week_wise = filtered_stock_data.groupby("Week_No")
    weekly_df =  filter_period(df_week_wise,"Week_No")
    return weekly_df

def filter_data_monthly(filtered_stock_data):
    start_month_index = filtered_stock_data.head(1).index[0]
    start_date = filtered_stock_data.loc[start_month_index,"TIMESTAMP"]
    filtered_stock_data['Month_No'] = (((filtered_stock_data["TIMESTAMP"].dt.isocalendar().year - start_date.year) * 12) 
    + filtered_stock_data['TIMESTAMP'].dt.month)
    df_month_wise = filtered_stock_data.groupby("Month_No")
    monthly_df =  filter_period(df_month_wise,"Month_No")
    return monthly_df

def filter_data_yearly(filtered_stock_data):
    filtered_stock_data['Year'] = filtered_stock_data["TIMESTAMP"].dt.isocalendar().year
    df_year_wise = filtered_stock_data.groupby("Year")
    yearly_df =  filter_period(df_year_wise,"Year")
    return yearly_df

def filter_data(stock_data,config):
    #scale: daily or weekly or monthly or yearly in config.json
    time_freq = config["scale"]
    scale_dict = {
        "daily":filter_data_daily,
        "weekly":filter_data_weekly,
        "monthly":filter_data_monthly,
        "yearly":filter_data_yearly
    }
    filtered_stock_data = get_df_by_symbol(stock_data,config)
    stock_data_with_time_freq = scale_dict[time_freq](filtered_stock_data)
    return stock_data_with_time_freq

def profit_attributes(row,config):
    stocks_purchasable = math.floor(config["amt_invested"]/row["BUYING_PRICE_PER_STOCK"])
    total_buying_price = stocks_purchasable*row["BUYING_PRICE_PER_STOCK"]
    total_selling_price = stocks_purchasable*row["SELLING_PRICE_PER_STOCK"]
    net_balance = (total_buying_price+total_selling_price)
    profit_or_loss = total_selling_price-total_buying_price
    columns = pd.Series({
        "AMT_INVESTED":config["amt_invested"],
        "STOCKS_PURCHASABLE": stocks_purchasable,
        "TOTAL_BUYING_PRICE": total_buying_price,
        "TOTAL_SELLING_PRICE": total_selling_price,
        "NET_BALANCE":net_balance,
        "PROFIT/LOSS(₹)":profit_or_loss,
        "ACCOUNT_BALANCE":total_selling_price+ (config["amt_invested"]-total_buying_price)
    })
    return columns

#Profit based on symbols,industry or symbol and industry ADANIGREEN or RE or ADANIGREEN,RE
#Stock Profitability for one stock , calculated using high and low
#Amt Invested > BuyingPrice per stock
def calc_profit(filtered_stock_data,config):
    profitable_stocks = filtered_stock_data.groupby("SYMBOLS").agg({"HIGH":"first","LOW":"last","TIMESTAMP":["first","last"],"INDUSTRY":"first","SYMBOL_INDUSTRY":"first"})
    profitable_stocks = profitable_stocks.reset_index().droplevel(axis=1,level=1)
    profitable_stocks.columns = ["SYMBOLS","BUYING_PRICE_PER_STOCK","SELLING_PRICE_PER_STOCK","BUYING_DATE","SELLING_DATE","INDUSTRY","SYMBOL_INDUSTRY"]
    profitable_stocks = profitable_stocks.query("BUYING_PRICE_PER_STOCK < @config['amt_invested']").copy()
    profitable_stocks[["AMT_INVESTED","STOCKS_PURCHASABLE","TOTAL_BUYING_PRICE","TOTAL_SELLING_PRICE","NET_BALANCE","PROFIT/LOSS(₹)",
                       "ACCOUNT_BALANCE"]] = profitable_stocks.apply(profit_attributes,args=(config,),axis=1)
    profitable_stocks = profitable_stocks.sort_values(by="ACCOUNT_BALANCE",ascending=False).reset_index(drop=True)
    return profitable_stocks

#Groupby symbols based on closing price
#Calculated moving avg based on user input
#Transform function is used to generate a single column on the existing df
#apply method collects all the grouped objects together and converts them back into a df

def group_by_symbols(symbol_group):
    return symbol_group 

def calc_moving_average(filtered_stock_data,config):
    group_symbols = []
    for size in config["window_sizes"]:
        filtered_stock_data[f'MOVING_AVERAGE_{size}'] = filtered_stock_data.groupby('SYMBOLS')['CLOSE'].transform(lambda x: x.rolling(window=size).mean())
    stock_data_symbols = filtered_stock_data.groupby("SYMBOLS").apply(group_by_symbols)
    group_symbols.append(stock_data_symbols)
    grouped_df = pd.concat(group_symbols,axis=1).reset_index(drop=True)
    grouped_df = grouped_df[grouped_df["TIMESTAMP"].between(config["start_time_stamp"],
    config["end_time_stamp"],inclusive="both")]
    return grouped_df

def calculate_max_profit_period(average_stocks):
    average_stocks = average_stocks.query("CLOSE > MOVING_AVERAGE_2 & CLOSE > MOVING_AVERAGE_14 ")
    return average_stocks