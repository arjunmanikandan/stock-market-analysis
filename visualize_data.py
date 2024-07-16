import matplotlib.pyplot as plt
import pandas as pd

#handles indicates how data is represented graphically(bars,piecharts,lines)
#plt.legend() by default receives labels from primary x and y axes. 
#To concatenate secondary y axis labels , entire list of labels from both axes should be passed
def visualize_stock_data(stock_data):
    stock_data['TIMESTAMP'] = pd.to_datetime(stock_data['TIMESTAMP'], format='%d-%b-%Y')
    filtered_stock_data = stock_data.query("SYMBOLS == '1018GS2026'")
    stock_series = filtered_stock_data["SERIES"].values[0]
    filtered_stock_data = filtered_stock_data.sort_values(by='TIMESTAMP')
    plt.title(f"(NSE INDIA) 1018GS2026 {stock_series} 23-24(JAN-JULY)")
    plt.xlabel("Date")
    plt.ylabel("Opening Price and Closing Price (₹)")
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["OPEN"], marker='o', linestyle='-', color="#0CC1F6",label="Opening Price")
    plt.plot(filtered_stock_data["TIMESTAMP"], filtered_stock_data["CLOSE"], marker='o', linestyle='-',color="#F6AC0C",label="Closing Price")
    line_handles,line_labels = plt.gca().get_legend_handles_labels()
    secondary_y_axis = plt.gca().twinx()
    secondary_y_axis.bar(filtered_stock_data["TIMESTAMP"], filtered_stock_data["TOTTRDQTY"], color="red", width=10, label="Total Traded Quantity")
    bar_handle,bar_label = plt.gca().get_legend_handles_labels()
    secondary_y_axis.set_ylabel("Total Traded Quantity(Volume)")
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%b-%Y'))
    plt.gcf().autofmt_xdate(rotation=45)
    plt.grid(True)
    plt.legend(line_handles+bar_handle,line_labels+bar_label)
    plt.show()