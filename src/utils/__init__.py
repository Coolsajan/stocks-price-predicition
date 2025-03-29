import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
import datetime
import json
import pickle

def plot_trendline(comp_dataframe, stock_name="Stock"):
    """Plots the trendline of the selected stock."""
    df = comp_dataframe.copy()  
    df = df.reset_index()  
    
    plt.figure(figsize=(10, 5))
    sns.regplot(x=df.index, y=df["Close"], scatter_kws={"s": 5}, line_kws={"color": "red"})
    
    unique_years = df["Date"].dt.year.unique()
    year_ticks = [df[df["Date"].dt.year == year].index[0] for year in unique_years]

    plt.xticks(ticks=year_ticks, labels=unique_years, rotation=0)
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.title(f"{stock_name} Stock Trend Line")
    plt.grid(True)
    plt.show()
    return plt

def plot_moving_average(comp_dataframe, stock_name="Stock", window_sma=20, window_ema=20):
    """Plots stock closing price with SMA & EMA indicators."""
    df = comp_dataframe.copy()
    df = df.reset_index()

    df["SMA"] = df["Close"].rolling(window=window_sma).mean()  # Simple Moving Average
    df["EMA"] = df["Close"].ewm(span=window_ema, adjust=False).mean()  # Exponential Moving Average

    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Close"], label="Closing Price", color="blue", alpha=0.5)
    plt.plot(df["Date"], df["SMA"], label=f"{window_sma}-day SMA", color="green", linestyle="--")
    plt.plot(df["Date"], df["EMA"], label=f"{window_ema}-day EMA", color="red", linestyle="--")

    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{stock_name} - SMA & EMA Trend")
    plt.legend()
    plt.grid(True)
    plt.show()

    return plt

def plot_bollinger_bands(comp_dataframe, stock_name="Stock", window=20):
    """Plots Bollinger Bands along with closing prices."""
    df = comp_dataframe.copy()
    df = df.reset_index()

    df["SMA"] = df["Close"].rolling(window=window).mean()
    df["Upper Band"] = df["SMA"] + (df["Close"].rolling(window=window).std() * 2)
    df["Lower Band"] = df["SMA"] - (df["Close"].rolling(window=window).std() * 2)

    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Close"], label="Closing Price", color="blue", alpha=0.5)
    plt.plot(df["Date"], df["SMA"], label="Middle Band (SMA)", color="green", linestyle="--")
    plt.plot(df["Date"], df["Upper Band"], label="Upper Band", color="red", linestyle="--")
    plt.plot(df["Date"], df["Lower Band"], label="Lower Band", color="red", linestyle="--")

    plt.fill_between(df["Date"], df["Lower Band"], df["Upper Band"], color="gray", alpha=0.2)

    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{stock_name} - Bollinger Bands")
    plt.legend()
    plt.grid(True)
    

    return plt

def plot_rsi(comp_dataframe, stock_name="Stock", window=14):
    """Plots Relative Strength Index (RSI)."""
    df = comp_dataframe.copy()
    df["Change"] = df["Close"].diff()
    df["Gain"] = df["Change"].apply(lambda x: x if x > 0 else 0)
    df["Loss"] = df["Change"].apply(lambda x: -x if x < 0 else 0)

    df["Avg Gain"] = df["Gain"].rolling(window=window).mean()
    df["Avg Loss"] = df["Loss"].rolling(window=window).mean()
    df["RS"] = df["Avg Gain"] / df["Avg Loss"]
    df["RSI"] = 100 - (100 / (1 + df["RS"]))

    plt.figure(figsize=(12, 4))
    plt.plot(df.index, df["RSI"], label="RSI", color="purple")
    plt.axhline(70, linestyle="--", color="red", label="Overbought (70)")
    plt.axhline(30, linestyle="--", color="green", label="Oversold (30)")

    plt.xlabel("Date")
    plt.ylabel("RSI Value")
    plt.title(f"{stock_name} - Relative Strength Index (RSI)")
    plt.legend()
    plt.grid(True)
    plt.show()

    return plt


def plot_candlestick(comp_dataframe, stock_name="Stock"):
    """Plots candlestick chart using Plotly."""

    if not isinstance(comp_dataframe, pd.DataFrame):
        raise ValueError("Input data must be a Pandas DataFrame.")
    
    df = comp_dataframe.copy()
    df = df.reset_index()
    df['Date'] = pd.to_datetime(df['Date'])

    fig = go.Figure(data=[go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        increasing_line_color="green",
        decreasing_line_color="red"
    )])
    
    fig.update_layout(title=f"{stock_name} Candlestick Chart", xaxis_rangeslider_visible=False)

    return fig


def plot_macd(data, fast_period=12, slow_period=26, signal_period=9, title="MACD Plot"):
    """
    Calculates and plots the MACD indicator for a given dataset.

    Args:
        data (pd.DataFrame): DataFrame with a 'Close' column.
        fast_period (int): Period for the fast EMA (default: 12).
        slow_period (int): Period for the slow EMA (default: 26).
        signal_period (int): Period for the signal line EMA (default: 9).
        title (str): Title of the plot (default: "MACD Plot").

    Returns:
        None (displays the plot).
    """
    if 'Close' not in data.columns:
        raise ValueError("DataFrame must contain a 'Close' column.")

    # Calculate MACD
    fast_ema = data['Close'].ewm(span=fast_period, adjust=False).mean()
    slow_ema = data['Close'].ewm(span=slow_period, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line

    # Plotting
    plt.figure(figsize=(10, 6))

    plt.plot(data.index, macd_line, label='MACD', color='blue')
    plt.plot(data.index, signal_line, label='Signal', color='orange')
    plt.bar(data.index, histogram, color=['green' if val > 0 else 'red' for val in histogram], label='MACD Histogram', alpha=0.5)

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('MACD Value')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    return plt

def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)
    
def load_model(filepath:str):
    with open(filepath,'rb') as f:
        return pickle.load(f)
    

def prediciton_to_df(prediciton_data):
    global result
    results=[]
    for i,data in enumerate(prediciton_data):
        result={"DAY":f"Day {i+1}","PREDICTED CLOSE":data[0]}
        results.append(result)

    return pd.DataFrame(results,columns=["DAY","PREDICTED CLOSE"])
    