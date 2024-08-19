from dotenv import load_dotenv
import filter_data as fd
from visualize_data import visualize_data,plot_candle_bars,moving_average_plot
from comparison import compare_multiple_symbols
import pandas as pd
import json,os,sqlite3

def display_df(profitable_stocks):
    print(profitable_stocks)

def read_json(json_file):
    with open(json_file,"r") as file:
        file_paths = json.load(file)
        return file_paths

def read_csv(config):
    df = pd.read_csv(config["nifty_50_path"])
    return df

def merge_df(stock_data,nifty_50_stocks):
    filtered_stock_data = pd.merge(stock_data,nifty_50_stocks,on=["SYMBOLS"],how="left")
    filtered_stock_data["SYMBOL_INDUSTRY"] = filtered_stock_data["SYMBOLS"] + "," + filtered_stock_data["INDUSTRY"]
    return filtered_stock_data

#To filter out prices which are lower than low
def filter_inconsistent_data(stock_data):
    stock_data_copy = stock_data.copy()
    stock_data_copy = stock_data_copy[stock_data_copy["CLOSE"]<stock_data_copy["LOW"]]
    stock_data_copy.loc[stock_data_copy.index,["CLOSE"]] = stock_data_copy["LOW"]
    return stock_data

def read_sqlite_db(config):
    conn = sqlite3.connect(config["stock_market_data_path"])
    stock_data = pd.read_sql_query("SELECT * FROM STOCK_DATA",conn)
    stock_data.drop([0],axis=0,inplace=True)
    stock_data = stock_data.reset_index(drop=True)
    return stock_data

#Profit period can be calculated for nifty 50 stocks only.
def main():
    load_dotenv()
    config = read_json(os.getenv("CONFIG_PATH"))
    stock_data = read_sqlite_db(config)
    stock_data = filter_inconsistent_data(stock_data)
    nifty_50_stocks = read_csv(config)
    merged_df = merge_df(stock_data,nifty_50_stocks)
    filtered_stock_data = fd.filter_data(merged_df,config)
    moving_avg_stocks = fd.calc_moving_average(filtered_stock_data,config)    
    stocks_in_time_range = fd.get_stocks_within_timestamp(moving_avg_stocks,config)
    tradable_stocks = fd.identify_stock_advice(stocks_in_time_range)
    tradable_stocks = fd.add_initial_values(tradable_stocks,config)
    stocks_balance_sheet = fd.calc_stock_balance_sheet(tradable_stocks,config)
    display_df(stocks_balance_sheet)

if __name__ == "__main__":
    main()