from src.scripts.data_fetching import GetData
from src.scripts.predicition import PredictPrice
from src.utils import *
from datetime import date
import mplcursors
from streamlit_lottie import st_lottie



import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

predict=PredictPrice()
data=GetData()
#this is the list to top 25 company from us market
list_of_company=("AAPL","MSFT","NVDA","AMZN","GOOG","META","BRK-B","TSLA","AVGO","LLY","WMT","JPM","V","XOM","MA","UNH","COST",
                 "NFLX","JNJ","PG","ORCL","ABBV","HD","BAC","KO")
#some animitation to make the page attractive
animation=load_lottiefile(filepath="lottie/stocks.json")
error=load_lottiefile(filepath="lottie/waiting.json")

#page layout stats here
st.header("WELCOME INVESTER 📉🚀🤩 ")
st.markdown(
    """
    :rainbow[*NOTE: This is not a financial tool to totally rely on it . Its just a test project .
    So use your own skill and knowledge for investment.]

    """
    )

col1 , col2  = st.columns([1,3],border=True)

with col1:
    company_name = st.selectbox(
        "Select the company you want to analysis",
        list_of_company,
        index=None,
        placeholder="Comany Tickers ID...",
        
    )

    START=st.date_input("Start Date", date(2019, 7, 5))
    END=st.date_input("End Date", date.today())
    


if col1.button("Predict 💸"):
    try:
        dataset,Company_name=data.get_data(company_name,START,END)
        #dataset=dataset.tail(500)
        prediciton_data=predict.prediction(company_name,100,10)

    except:
        with col2:
            st.header("Please Select Any Company.")
            st_lottie(error,
              speed=1,
              height=400,
              width=400)
            

    
    else:
        with col2:
            st.dataframe(prediciton_to_df(prediciton_data),hide_index=True)


        st.subheader(f"Candlestick {Company_name}", divider=True)
        st.plotly_chart(plot_candlestick(dataset,Company_name))
        st.text("A candlestick chart is a graphical representation used in financial analysis to display the price movement of an asset. This may include a stock, currency, or commodity, over a specified period of time. It consists of individual candlesticks, each representing a specific time frame (e.g., a day, hour, or minute).")

        mplcursors.cursor(hover=True)  # Enable hover and zoom features

        st.subheader(f"Trendline {Company_name}", divider=True)
        st.pyplot(plot_trendline(dataset),Company_name)
        st.text("Trend lines are straight lines that connect two or more price points on a chart to identify and confirm trends. In technical analysis, trend lines are a fundamental tool that traders and analysts use to identify and anticipate the general pattern of price movement in a market.")

        st.subheader(f"Bollinger Bands {Company_name}", divider=True)
        st.pyplot(plot_bollinger_bands(dataset),Company_name)
        st.text("Bollinger Bands are envelopes plotted at a standard deviation level above and below a simple moving average of the price. Because the distance of the bands is based on standard deviation, they adjust to volatility swings in the underlying price. Bollinger Bands use 2 parameters, Period and Standard Deviations, StdDev.")

        st.subheader(f"Moving Average {Company_name}", divider=True)
        st.pyplot(plot_moving_average(dataset),Company_name)
        st.text("A stock moving average (MA) is a technical analysis tool that smooths out price fluctuations by calculating the average price over a specific period, helping traders identify trends and potential support/resistance levels. ")

        st.subheader(f"RSI-plot {Company_name}", divider=True)
        st.pyplot(plot_rsi(dataset),Company_name)
        st.text("The Relative Strength Index (RSI) is one of the most widely used momentum indicators in technical analysis. It helps traders identify overbought and oversold conditions and generates potential buy and sell signals. Developed by J. Welles Wilder Jr., the RSI measures the speed and magnitude of recent price changes.")

        st.subheader(f"MACD-plot {Company_name}", divider=True)
        st.pyplot(plot_macd(dataset),Company_name)
        st.text("Moving average convergence/divergence (MACD) is a technical indicator to help investors identify entry points for buying or selling. The MACD line is calculated by subtracting the 26-period exponential moving average (EMA) from the 12-period EMA. The signal line is a nine-period EMA of the MACD line.")

else:
    with col2:
        st_lottie(animation,
              speed=1,
              reverse=False,
              height=400,
              width=400,
                )





