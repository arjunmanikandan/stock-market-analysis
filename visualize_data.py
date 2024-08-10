import  matplotlib.patches as mpatches
import matplotlib.pyplot as plt

def plot_labels(filtered_stock_data,config):
    stock_series = filtered_stock_data["SERIES"].unique()
    filtered_stock_data = filtered_stock_data.sort_values(by='TIMESTAMP')
    plt.title(f"(NSE INDIA) {config['symbols_or_industries']} {stock_series} BETWEEN {config['start_time_stamp']} AND {config['end_time_stamp']} ({config['scale']})")
    plt.xlabel("Date")
    plt.ylabel("Price(₹)")

def plot_candle_bars(filtered_stock_data,config):
    plot_labels(filtered_stock_data,config)
    highest_prices = filtered_stock_data[filtered_stock_data['CLOSE'] >= filtered_stock_data['OPEN']]
    lowest_prices = filtered_stock_data[filtered_stock_data['CLOSE'] < filtered_stock_data['OPEN']]
    plt.bar(highest_prices["TIMESTAMP"], highest_prices['CLOSE'] - highest_prices['OPEN'], width=2.5, bottom=highest_prices['OPEN'], color="green")
    plt.bar(highest_prices["TIMESTAMP"], highest_prices['HIGH'] - highest_prices['CLOSE'], width=0.5, bottom=highest_prices['CLOSE'], color="green")
    plt.bar(highest_prices["TIMESTAMP"], highest_prices['LOW'] - highest_prices['OPEN'], width=0.5, bottom=highest_prices['OPEN'], color="green")
    plt.bar(lowest_prices["TIMESTAMP"], lowest_prices['CLOSE'] - lowest_prices['OPEN'], width=2.5, bottom=lowest_prices['OPEN'], color="red")
    plt.bar(lowest_prices["TIMESTAMP"], lowest_prices['HIGH'] - lowest_prices['OPEN'], width=0.5, bottom=lowest_prices['OPEN'], color="red")
    plt.bar(lowest_prices["TIMESTAMP"], lowest_prices['LOW'] - lowest_prices['CLOSE'], width=0.5, bottom=lowest_prices['CLOSE'], color="red")
    green_patch = mpatches.Patch(color='green', label='Closing Price > Opening Price')
    red_patch = mpatches.Patch(color='red', label='Opening Price > Closing Price')
    plt.legend(handles=[green_patch, red_patch])
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%b-%Y'))
    plt.gcf().autofmt_xdate(rotation=45)
    plt.show()

def visualize_data(filtered_stock_data,config):
    plot_labels(filtered_stock_data,config)
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["HIGH"],linestyle='-',color="#88F60C",label="Highest Price")
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["LOW"],linestyle='-',color="#0C2FF6",label="Lowest Price")
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["CLOSE"],linestyle='-',color="#F6AC0C",label="Closing Price")
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["OPEN"],linestyle='-', color="#0CC1F6",label="Opening Price")
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

def moving_average_plot(average_stocks,config):
    plot_labels(average_stocks,config)
    plt.plot(average_stocks["TIMESTAMP"],average_stocks["CLOSE"],label="CLOSING_PRICE")
    plt.plot(average_stocks["TIMESTAMP"],average_stocks["MOVING_AVERAGE_2"],label="MOVING_AVERAGE(2 DAYS)")
    plt.plot(average_stocks["TIMESTAMP"],average_stocks["MOVING_AVERAGE_14"],label="MOVING_AVERAGE(14 DAYS")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%b-%Y'))
    plt.gcf().autofmt_xdate(rotation=45)
    plt.legend()
    plt.show()