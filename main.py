from dotenv import load_dotenv
from filter_data import filter_data,calc_profit
from visualize_data import visualize_data,plot_candle_bars
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

def main():
    load_dotenv()
    config = read_json(os.getenv("CONFIG_PATH"))
    stock_data = read_sqlite_db(config)
    stock_data = filter_inconsistent_data(stock_data)
    nifty_50_stocks = read_csv(config)
    merged_df = merge_df(stock_data,nifty_50_stocks)
    filtered_stock_data = filter_data(merged_df,config)
    profitable_stocks = calc_profit(filtered_stock_data,config)
    display_df(profitable_stocks)

if __name__ == "__main__":
    main()