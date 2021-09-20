
from flask import Flask, render_template, url_for, request 
import requests
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure, graph, output_file, show
from bokeh.embed import components
from bokeh.resources import CDN 


def load_data(ticker):
    function = 'TIME_SERIES_DAILY_ADJUSTED'
    apikey = 'T7AOU52SI2T0ADDJ'

    url = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' + ticker + '&apikey=' + apikey
    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame(data['Time Series (Daily)']).T[['1. open', '5. adjusted close']]
    df.index = pd.to_datetime(df.index)
    df.index.name = 'Date'
    df.sort_index(inplace=True)
    df.rename(columns={'1. open': 'open', '5. adjusted close': 'close'}, inplace=True)
    return df


def get_graph(df, ticker):
    source = ColumnDataSource(df)
    selection = 'close'

    p = figure(x_axis_type='datetime', x_axis_label='Date', title='Stock Price',
               plot_width=800, plot_height=600)

    p.line('Date', selection, source=source, legend_label=ticker+' : '+selection)
    
    return p


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        ticker_content = request.form['ticker_input']
        ticker_df = load_data(ticker_content)
        
        graph = get_graph(ticker_df, ticker_content)

        script, div = components(graph)
        return render_template("graph.html", the_div=div, the_script=script)
    else:
        return render_template('index.html')
     

if __name__ == '__main__':
    app.run(debug=True)

