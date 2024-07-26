from visualize_data import plot_labels
import matplotlib.pyplot as plt
import functools

def plot_line_graph(filtered_stock_data,symbol_color_tuple):
    filtered_stock_data =  filtered_stock_data.query("SYMBOLS == @symbol_color_tuple[0]")    
    plt.plot(filtered_stock_data["TIMESTAMP"], 
    filtered_stock_data["CLOSE"], linestyle='-',marker="o",color=f"{symbol_color_tuple[1]}",
    label=f'{symbol_color_tuple[0]}(CLOSING PRICE)')

#functools partial class is used to pass a parameter while using map()
#zip is used to create tuples of symbols and colors
def compare_multiple_symbols(filtered_stock_data,config):
    color_codes = ["#0CACF6","#F67E0C"]
    plot_labels(filtered_stock_data,config)
    list(map(functools.partial(plot_line_graph,filtered_stock_data),
    zip(filtered_stock_data["SYMBOLS"].unique(),color_codes)))
    plt.legend()
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%b-%Y'))
    plt.gcf().autofmt_xdate(rotation=45)
    plt.show()