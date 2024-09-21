import requests
import schedule
import time
from sklearn.linear_model import LinearRegression
import numpy as np
import json

# Initialize a model (for simplicity, using Linear Regression)
model = LinearRegression()

# Placeholder for storing historical data
data = []


def fetch_data(symbol='BITSTAMP:BTCUSD'):
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
        # 'cookie': 'cookiePrivacyPreferenceBannerProduction=notApplicable; _ga=GA1.1.549165104.1725870259; cookiesSettings={"analytics":true,"advertising":true}; _sp_ses.cf1a=*; direct_affiliate_params={"aff_id":"127766","target_link":"https://www.tradingview.com/","source":"admitad","aff_click_id":"cebe14ca9671041f655e79dcaf36ff8d"}; __gads=ID=7a917f7fedf5208a:T=1726814914:RT=1726889565:S=ALNI_MZmsDVVvC_-n_gCaA3uTm8xX6Cj3A; __eoi=ID=561afc0e9d3a9653:T=1726814914:RT=1726889565:S=AA-Afja_97JXSvHdkC5_rFgPot4N; _sp_id.cf1a=d12308a8-1ce8-41af-ad82-35b12a11574f.1725870258.3.1726889677.1726816105.da1699dc-cbae-4bbc-bebb-2c4dc920f815; _ga_YVVRYGL0E0=GS1.1.1726886463.4.1.1726889677.36.0.0',
        'origin': 'https://www.tradingview.com',
        'priority': 'u=1, i',
        'referer': 'https://www.tradingview.com/',
        'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    }

    params = {
        'symbol': symbol,
        'fields': 'Recommend.Other|5,Recommend.All|5,Recommend.MA|5,RSI|5,RSI[1]|5,Stoch.K|5,Stoch.D|5,Stoch.K[1]|5,Stoch.D[1]|5,CCI20|5,CCI20[1]|5,ADX|5,ADX+DI|5,ADX-DI|5,ADX+DI[1]|5,ADX-DI[1]|5,AO|5,AO[1]|5,AO[2]|5,Mom|5,Mom[1]|5,MACD.macd|5,MACD.signal|5,Rec.Stoch.RSI|5,Stoch.RSI.K|5,Rec.WR|5,W.R|5,Rec.BBPower|5,BBPower|5,Rec.UO|5,UO|5,EMA10|5,close|5,SMA10|5,EMA20|5,SMA20|5,EMA30|5,SMA30|5,EMA50|5,SMA50|5,EMA100|5,SMA100|5,EMA200|5,SMA200|5,Rec.Ichimoku|5,Ichimoku.BLine|5,Rec.VWMA|5,VWMA|5,Rec.HullMA9|5,HullMA9|5,Pivot.M.Classic.S3|5,Pivot.M.Classic.S2|5,Pivot.M.Classic.S1|5,Pivot.M.Classic.Middle|5,Pivot.M.Classic.R1|5,Pivot.M.Classic.R2|5,Pivot.M.Classic.R3|5,Pivot.M.Fibonacci.S3|5,Pivot.M.Fibonacci.S2|5,Pivot.M.Fibonacci.S1|5,Pivot.M.Fibonacci.Middle|5,Pivot.M.Fibonacci.R1|5,Pivot.M.Fibonacci.R2|5,Pivot.M.Fibonacci.R3|5,Pivot.M.Camarilla.S3|5,Pivot.M.Camarilla.S2|5,Pivot.M.Camarilla.S1|5,Pivot.M.Camarilla.Middle|5,Pivot.M.Camarilla.R1|5,Pivot.M.Camarilla.R2|5,Pivot.M.Camarilla.R3|5,Pivot.M.Woodie.S3|5,Pivot.M.Woodie.S2|5,Pivot.M.Woodie.S1|5,Pivot.M.Woodie.Middle|5,Pivot.M.Woodie.R1|5,Pivot.M.Woodie.R2|5,Pivot.M.Woodie.R3|5,Pivot.M.Demark.S1|5,Pivot.M.Demark.Middle|5,Pivot.M.Demark.R1|5',
        'no_404': 'true',
        'label-product': 'popup-technicals',
    }

    response = requests.get('https://scanner.tradingview.com/symbol', params=params, headers=headers)
    data = json.loads(response.text)
    return data


def process_data(raw_data):
    # Extract features and target
    features = [value for key, value in raw_data.items() if key != 'close|5']
    target = raw_data['close|5']
    return features, target


def train_model(data):
    global model
    if data:
        X = np.array([d[0] for d in data])
        y = np.array([d[1] for d in data])
        model.fit(X, y)


def predict_price(features):
    global model
    return model.predict([features])


first = True
features=[]

def job(st,symbol=''):
    global first, fetch_data, data,features
    raw_data = fetch_data(symbol)
    if raw_data:
        features, target = process_data(raw_data)
        # if first==True:
        # target=0
        # first=False
        # return
        time.sleep(15)
        raw_data = fetch_data(symbol)
        features2, target2 = process_data(raw_data)
        tup = (features, target2)
        data.append(tup)
        # train_model(data)
        train_model(data)
        # data.append((features, target))
        # print("Trained for the value ",target)
        prediction = predict_price(features2)
        print(f"Predicted close price: {prediction[0]}")
        st.write(f"Predicted close price: {prediction[0]}")
        time.sleep(15)
        raw_data = fetch_data(symbol)
        features3, target3 = process_data(raw_data)
        tup = (features2, target3)
        data.append(tup)
        train_model(data)
        print(f"Actual close price: {target3}")
        st.write(f"Actual close price: {target3}")
        if abs(prediction[0] - target3) > 10000:
            print("Trend change...")
            st.write("Trend change...")
        elif prediction[0] > target3:
            print("Sell")
            st.write("Sell")
        elif prediction[0] < target3:
            print("Buy")
            st.write("Buy")


# x=time.thread_time()
# Schedule the job every 5 minutes
# schedule.every(5).minutes.do(job)

#while True:
    # schedule.run_pending()
    #job()
    #time.sleep(15)