import streamlit as st
import requests
import json
from trend import predict_trend  # Your custom prediction module

trend_data = {}


# Function to simulate fetching data dynamically when the user expands the section
def fetch_crypto_indicators(currency):
    # Simulate fetching data for the given cryptocurrency
    # This can be replaced with an actual API call or a more complex data-fetching function
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        # 'cookie': '_sp_ses.cf1a=*; _sp_id.cf1a=.1722230816.1.1722234238.1722230816.ac36a3a6-f97b-4c54-a48e-5736d1290571',
        'origin': 'https://www.tradingview.com',
        'priority': 'u=1, i',
        'referer': 'https://www.tradingview.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    params = {
        'symbol': currency,
        'fields': 'Recommend.Other|5,Recommend.All|5,Recommend.MA|5,RSI|5,RSI[1]|5,Stoch.K|5,Stoch.D|5,Stoch.K[1]|5,Stoch.D[1]|5,CCI20|5,CCI20[1]|5,ADX|5,ADX+DI|5,ADX-DI|5,ADX+DI[1]|5,ADX-DI[1]|5,AO|5,AO[1]|5,AO[2]|5,Mom|5,Mom[1]|5,MACD.macd|5,MACD.signal|5,Rec.Stoch.RSI|5,Stoch.RSI.K|5,Rec.WR|5,W.R|5,Rec.BBPower|5,BBPower|5,Rec.UO|5,UO|5,EMA10|5,close|5,SMA10|5,EMA20|5,SMA20|5,EMA30|5,SMA30|5,EMA50|5,SMA50|5,EMA100|5,SMA100|5,EMA200|5,SMA200|5,Rec.Ichimoku|5,Ichimoku.BLine|5,Rec.VWMA|5,VWMA|5,Rec.HullMA9|5,HullMA9|5,Pivot.M.Classic.S3|5,Pivot.M.Classic.S2|5,Pivot.M.Classic.S1|5,Pivot.M.Classic.Middle|5,Pivot.M.Classic.R1|5,Pivot.M.Classic.R2|5,Pivot.M.Classic.R3|5,Pivot.M.Fibonacci.S3|5,Pivot.M.Fibonacci.S2|5,Pivot.M.Fibonacci.S1|5,Pivot.M.Fibonacci.Middle|5,Pivot.M.Fibonacci.R1|5,Pivot.M.Fibonacci.R2|5,Pivot.M.Fibonacci.R3|5,Pivot.M.Camarilla.S3|5,Pivot.M.Camarilla.S2|5,Pivot.M.Camarilla.S1|5,Pivot.M.Camarilla.Middle|5,Pivot.M.Camarilla.R1|5,Pivot.M.Camarilla.R2|5,Pivot.M.Camarilla.R3|5,Pivot.M.Woodie.S3|5,Pivot.M.Woodie.S2|5,Pivot.M.Woodie.S1|5,Pivot.M.Woodie.Middle|5,Pivot.M.Woodie.R1|5,Pivot.M.Woodie.R2|5,Pivot.M.Woodie.R3|5,Pivot.M.Demark.S1|5,Pivot.M.Demark.Middle|5,Pivot.M.Demark.R1|5',
        'no_404': 'true',
    }
    response = requests.get('https://scanner.tradingview.com/symbol', params=params, headers=headers)
    print(response.text)
    data = json.loads(response.text)
    datacp = data.copy()
    # print(data)
    for i in data:
        if '[' in i:
            datacp.pop(i)  # to only take 5 min chart values
    return datacp


def job():
    import requests

    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
        'content-type': 'text/plain;charset=UTF-8',
        # 'cookie': 'cookiePrivacyPreferenceBannerProduction=notApplicable; _ga=GA1.1.549165104.1725870259; cookiesSettings={"analytics":true,"advertising":true}; _sp_ses.cf1a=*; __gads=ID=7a917f7fedf5208a:T=1726814914:RT=1726815467:S=ALNI_MZmsDVVvC_-n_gCaA3uTm8xX6Cj3A; __eoi=ID=561afc0e9d3a9653:T=1726814914:RT=1726815467:S=AA-Afja_97JXSvHdkC5_rFgPot4N; _sp_id.cf1a=d12308a8-1ce8-41af-ad82-35b12a11574f.1725870258.2.1726815707.1725870265.0e721d38-102a-459e-ae20-32e8a2359018; _ga_YVVRYGL0E0=GS1.1.1726814911.2.1.1726815707.55.0.0',
        'origin': 'https://www.tradingview.com',
        'priority': 'u=1, i',
        'referer': 'https://www.tradingview.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    }

    data = '{"columns":["base_currency","base_currency_desc","base_currency_logoid","update_mode","type","typespecs","exchange","crypto_total_rank","close","pricescale","minmov","fractional","minmove2","currency","24h_close_change|5","market_cap_calc","fundamental_currency_code","24h_vol_cmc","circulating_supply","crypto_common_categories.tr"],"ignore_unknown_fields":false,"options":{"lang":"en"},"range":[0,200],"sort":{"sortBy":"24h_close_change|5","sortOrder":"desc","nullsFirst":false},"preset":"coin_gainers"}'

    response = requests.post('https://scanner.tradingview.com/coin/scan', headers=headers, data=data)
    lists = json.loads(response.text)['data']
    cryptos=[]
    for i in lists:
        cryptos.append(i['d'][1])
    print(cryptos)
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
        #print(i['d'])
        if i['d'][1] not in cryptos:
            continue
        sub = dict(zip(columns, i['d']))
        try:
            trend, score = predict_trend(sub)
        except Exception as e:
            st.error(f"Error: {e}")
            continue
        trend_data[sub['base_currency_desc']] = {'trend': trend, 'score': score,'currency':i['s']}

    return trend_data


# Function to style the text based on trend and score
def stylize_text(currency, trend, score):
    color = "green" if score > 0 else "red"

    if abs(score) > 0.5:
        style = f"<strong><span style='color:{color};'>{currency}: Trend - {trend}, Score - {score}</span></strong>"
    else:
        style = f"<span style='color:{color};'>{currency}: Trend - {trend}, Score - {score}</span>"

    st.markdown(style, unsafe_allow_html=True)


# Streamlit UI
st.title("Crypto Trend Analysis")

if st.button("Run Prediction"):
    with st.spinner('Fetching data and predicting trends...'):
        trend_data = job()
        st.success("Prediction Complete!")
        count=0
        for key, info in trend_data.items():
            if count>50:
                break
            stylize_text(key, info['trend'], info['score'])

            # Create an expander for each currency to trigger data fetching when clicked
            with st.expander(f"View Indicators for {info['currency']}"):
                st.write(f"Fetching indicators for {info['currency']}...")

                # Dynamically fetch data when the user opens the expander
                indicators = fetch_crypto_indicators(info['currency'])

                # Display fetched indicators in a table
                if indicators:
                    st.table(indicators)
                else:
                    st.write("No indicators available.")
                count+=1
