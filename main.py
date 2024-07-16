from visualize_data import visualize_stock_data
import pandas as pd
import json,os

def read_json(json_file):
    with open(json_file,"r") as file:
        file_paths = json.load(file)
        return file_paths

def read_csv(config):
    stock_data = pd.read_csv(config["stock_market_data_path"])
    return stock_data

def main():
    config = read_json(os.getenv("CONFIG_PATH"))
    stock_data = read_csv(config)
    visualize_stock_data(stock_data)

if __name__ == "__main__":
    main()