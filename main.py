import streamlit as st
import requests
import json
from trend import predict_trend  # Your custom prediction module

trend_data = {}

def job():
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    }
    data = '{"columns":["base_currency","base_currency_desc","update_mode","exchange","crypto_total_rank","Recommend.All"],"symbols":{},"markets":["coin"]}'
    response = requests.post('https://scanner.tradingview.com/coin/scan', headers=headers, data=data)

    trend_data = {}
    columns = json.loads(data)['columns']
    lists = json.loads(response.text)['data']
    for i in lists:
        sub = dict(zip(columns, i['d']))
        try:
            trend, score = predict_trend(sub)
        except Exception as e:
            st.error(f"Error: {e}")
            continue
        trend_data[sub['base_currency_desc']] = {'trend': trend, 'score': score}

    return trend_data

st.title("Crypto Trend Analysis")

if st.button("Run Prediction"):
    with st.spinner('Fetching data and predicting trends...'):
        trend_data = job()
        st.success("Prediction Complete!")

        for currency, info in trend_data.items():
            st.write(f"{currency}: Trend - {info['trend']}, Score - {info['score']}")
