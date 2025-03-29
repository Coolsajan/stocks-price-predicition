## stock-forcasting-anylisis 💸+🧠

     ->by Sajan Thapa

This is a normal LSTM project to predict the future stock price. It re-uses its onwn predicition to predict it future data so it have the primary feature for self learning which works perfectly great sometimes while it may creates error someother time . So this is just a LSTM project not a investment tools.

### Dataused

y-finace for data pull.

### Steps the programs

(As you request the company ticker and date range)

1. pulls data for {company ticker} from the y-finance api,
2. extract the adjusted close column from the data
3. scales the data with MINMAX scaler,
4. creates the working dataset from the scaled data with stepped price ,
5. feeds the data to lstm model and predict the next price,
6. updates the working dataset with the prediciton and uses the data from next predicition.

### Plots

As the data is pulled from the api different plot are ploted like , candlestick,rsi,ma,macd and few useful plot from the data .
