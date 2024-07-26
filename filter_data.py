import pandas as pd
import numpy as np

def get_df_by_symbol(stock_data,config):
    filtered_stock_data = stock_data[stock_data["SYMBOLS"].isin(config['stock_symbols'])].copy()
    filtered_stock_data['TIMESTAMP'] = pd.to_datetime(stock_data['TIMESTAMP'], format='%d-%b-%Y')
    filtered_stock_data = filtered_stock_data[filtered_stock_data["TIMESTAMP"].between(config["start_time_stamp"],
    config["end_time_stamp"],inclusive="both")]
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
    filtered_stock_data['Week_No'] = filtered_stock_data["TIMESTAMP"].dt.isocalendar().week
    df_week_wise = filtered_stock_data.groupby("Week_No")
    weekly_df =  filter_period(df_week_wise,"Week_No")
    return weekly_df

def filter_data_monthly(filtered_stock_data):
    filtered_stock_data['Month_No'] = filtered_stock_data["TIMESTAMP"].dt.month
    df_month_wise = filtered_stock_data.groupby("Month_No")
    monthly_df =  filter_period(df_month_wise,"Month_No")
    return monthly_df

def filter_data_yearly(filtered_stock_data):
    filtered_stock_data['Year'] = filtered_stock_data["TIMESTAMP"].dt.year
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