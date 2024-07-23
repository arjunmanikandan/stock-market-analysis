import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def visualize_data(filtered_stock_data,stock_data,config):
    stock_series = filtered_stock_data["SERIES"].values[0]
    filtered_stock_data = filtered_stock_data.sort_values(by='TIMESTAMP')
    plt.title(f"(NSE INDIA) {config['stock_symbol']} {stock_series} BETWEEN {config['start_time_stamp']} AND {config['end_time_stamp']}")
    plt.xlabel("Date")
    plt.ylabel("Price(₹)")
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["HIGH"], marker='o', linestyle='-',color="#88F60C",label="Highest Price")
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["LOW"], marker='o', linestyle='-',color="#0C2FF6",label="Lowest Price")
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["CLOSE"], marker='o', linestyle='-',color="#F6AC0C",label="Closing Price")
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["OPEN"], marker='o', linestyle='-', color="#0CC1F6",label="Opening Price")
    line_handles,line_labels = plt.gca().get_legend_handles_labels()
    secondary_y_axis = plt.gca().twinx()
    secondary_y_axis.bar(filtered_stock_data["TIMESTAMP"], filtered_stock_data["TOTTRDQTY"], color="red", width=0.3, label="Total Traded Quantity")
    bar_handle,bar_label = plt.gca().get_legend_handles_labels()
    secondary_y_axis.set_ylabel("Total Traded Quantity(Volume)")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%b-%Y'))
    plt.gcf().autofmt_xdate(rotation=45)
    plt.grid(True)
    plt.legend(line_handles+bar_handle,line_labels+bar_label,loc="upper left")
    plt.show()

def get_df_by_symbol(stock_data,config):
    filtered_stock_data = stock_data.query("SYMBOLS == @config['stock_symbol']").copy()
    filtered_stock_data['TIMESTAMP'] = pd.to_datetime(stock_data['TIMESTAMP'], format='%d-%b-%Y')
    filtered_stock_data = filtered_stock_data[filtered_stock_data["TIMESTAMP"].between(config["start_time_stamp"],
    config["end_time_stamp"],inclusive="both")]
    return filtered_stock_data

def filter_period(df,freq):
    df = pd.concat([df.head(1),df.tail(1)],axis=0).reset_index(drop=True)
    df = df.groupby(f"{freq}").agg({"OPEN":"first","CLOSE":"last",'SYMBOLS':'first', 'SERIES':'first',
    'TOTTRDQTY':"sum", 'TIMESTAMP':'first',"HIGH":"max","LOW":"min"}).reset_index(drop=True)
    return df

def filter_data_daily(filtered_stock_data,stock_data,config):
    visualize_data(filtered_stock_data,stock_data,config)

def filter_data_weekly(filtered_stock_data,stock_data,config):
    filtered_stock_data['Week_No'] = filtered_stock_data["TIMESTAMP"].dt.isocalendar().week
    df_week_wise = filtered_stock_data.groupby("Week_No")
    weekly_df =  filter_period(df_week_wise,"Week_No")
    visualize_data(weekly_df,stock_data,config)

def filter_data_monthly(filtered_stock_data,stock_data,config):
    filtered_stock_data['Month_No'] = filtered_stock_data["TIMESTAMP"].dt.month
    df_month_wise = filtered_stock_data.groupby("Month_No")
    monthly_df =  filter_period(df_month_wise,"Month_No")
    visualize_data(monthly_df,stock_data,config)

def filter_data_yearly(filtered_stock_data,stock_data,config):
    filtered_stock_data['Year'] = filtered_stock_data["TIMESTAMP"].dt.year
    df_year_wise = filtered_stock_data.groupby("Year")
    yearly_df =  filter_period(df_year_wise,"Year")
    visualize_data(yearly_df,stock_data,config)

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
    scale_dict[time_freq](filtered_stock_data,stock_data,config)