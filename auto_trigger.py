import streamlit as st
import requests
import json
from trend import predict_trend  # Your custom prediction module
from automation import job
import time

#trend_data = {}

def main():
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
        cryptos.append({i['d'][1]:i['s']})
    combined_dict = {}
    for d in cryptos:
        combined_dict.update(d)
    print(combined_dict)
    st.title("Bitcoin ML Analysis")
    #choice=st.selectbox("Crypto",list(combined_dict.keys()))
    #time.sleep(15)
    #symbol=combined_dict[choice]

    #if st.button("Run Prediction"):
    with st.spinner('Fetching data and predicting trends...'):
        #print(f"Started..{symbol}")
        while True:
            job(st=st,symbol='BITSTAMP:BTCUSD')
            time.sleep(15)
main()