import requests,json

def predict_trend(data):
    """
    Predicts the trend (uptrend or downtrend) based on technical indicators with a weighted system.

    Parameters:
    data (dict): A dictionary containing technical indicators for a cryptocurrency.

    Returns:
    str: 'Uptrend' or 'Downtrend' based on the analysis.
    """
    # Extracting indicators from the dictionary
    rsi = data.get('RSI', 50)
    momentum = data.get('Mom', 0)
    ao = data.get('AO', 0)
    cci20 = data.get('CCI20', 0)
    stoch_k = data.get('Stoch.K', 50)
    stoch_d = data.get('Stoch.D', 50)
    recommend_all = data.get('Recommend.All', 0)
    recommend_ma = data.get('Recommend.MA', 0)

    # Initializing trend score
    trend_score = 0

    # Defining weights
    weights = {
        'RSI': 1,
        'Momentum': 2,
        'AO': 2,
        'CCI20': 1,
        'Stoch': 1,
        'Recommend': 1
    }

    # Analyzing RSI
    if rsi > 70:
        trend_score -= weights['RSI']  # Overbought
    elif rsi < 30:
        trend_score += weights['RSI']  # Oversold

    # Analyzing Momentum
    if momentum > 0:
        trend_score += weights['Momentum'] * momentum
    elif momentum < 0:
        trend_score -= weights['Momentum'] *- momentum

    # Analyzing AO
    if ao > 0:
        trend_score += weights['AO'] #* ao
    elif ao < 0:
        trend_score -= weights['AO'] #*- ao

    # Analyzing CCI20
    if cci20 > 100:
        trend_score -= weights['CCI20']  #* cci20# Overbought
    elif cci20 < -100:
        trend_score += weights['CCI20']  #*- cci20# Oversold

    # Analyzing Stochastic Oscillators
    if stoch_k > 80 or stoch_d > 80:
        trend_score -= weights['Stoch'] #* stoch_k# Overbought
    elif stoch_k < 20 or stoch_d < 20:
        trend_score += weights['Stoch'] #* - stoch_k # Oversold

    # Analyzing Recommendations
    if recommend_all > 0:
        trend_score += weights['Recommend'] * recommend_all
    elif recommend_all < 0:
        trend_score -= weights['Recommend'] * - recommend_all

    if recommend_ma > 0:
        trend_score += weights['Recommend'] * recommend_ma
    elif recommend_ma < 0:
        trend_score -= weights['Recommend'] * - recommend_ma

    # Predicting trend based on trend score
    print("Score of ",data['base_currency_desc']," is ",trend_score)
    #trend_score= "{:.2f}".format(float(trend_score))
    if trend_score>25 or trend_score<-25:
        x= "Strong"
    if trend_score > 0:
        try:
            return x+' Uptrend, RSI:'+str(rsi),trend_score
        except UnboundLocalError:
            return "Uptrend",trend_score
    else:
        try:
            return x+' Downtrend, RSI:'+str(rsi),trend_score
        except UnboundLocalError:
            return "Downtrend",trend_score



if "__main__" == __name__:
    trend_data={}
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'text/plain;charset=UTF-8',
        # 'cookie': '_sp_ses.cf1a=*; cookiePrivacyPreferenceBannerProduction=notApplicable; cookiesSettings={"analytics":true,"advertising":true}; device_t=VzM4MkJROjA.SspaK-SYuJFEXw3VdWneyw2z2b1ao3AhXX3sYIOMraY; png=a6c7e412-3ff7-4572-adce-a91b9e1fa54a; etg=a6c7e412-3ff7-4572-adce-a91b9e1fa54a; cachec=a6c7e412-3ff7-4572-adce-a91b9e1fa54a; tv_ecuid=a6c7e412-3ff7-4572-adce-a91b9e1fa54a; _sp_id.cf1a=0dd66ae0-7190-4c0e-81cf-cc9e7eff41ef.1725847763.1.1725852612.1725847763.c3e8c37d-60d7-4fe2-b72c-32cc7b093379',
        'origin': 'https://www.tradingview.com',
        'priority': 'u=1, i',
        'referer': 'https://www.tradingview.com/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    }
    data = '{"columns":["base_currency","base_currency_desc","base_currency_logoid","update_mode","type","typespecs","exchange","crypto_total_rank","Recommend.All","Recommend.MA","Recommend.Other","RSI","Mom","pricescale","minmov","fractional","minmove2","AO","CCI20","Stoch.K","Stoch.D","Candle.3BlackCrows","Candle.3WhiteSoldiers","Candle.AbandonedBaby.Bearish","Candle.AbandonedBaby.Bullish","Candle.Doji","Candle.Doji.Dragonfly","Candle.Doji.Gravestone","Candle.Engulfing.Bearish","Candle.Engulfing.Bullish","Candle.EveningStar","Candle.Hammer","Candle.HangingMan","Candle.Harami.Bearish","Candle.Harami.Bullish","Candle.InvertedHammer","Candle.Kicking.Bearish","Candle.Kicking.Bullish","Candle.LongShadow.Lower","Candle.LongShadow.Upper","Candle.Marubozu.Black","Candle.Marubozu.White","Candle.MorningStar","Candle.ShootingStar","Candle.SpinningTop.Black","Candle.SpinningTop.White","Candle.TriStar.Bearish","Candle.TriStar.Bullish"],"ignore_unknown_fields":false,"options":{"lang":"en"},"range":[0,100],"sort":{"sortBy":"crypto_total_rank","sortOrder":"asc"},"symbols":{},"markets":["coin"]}'
    response = requests.post('https://scanner.tradingview.com/coin/scan', headers=headers, data=data)
    # print(json.loads(response.text))
    new_data = {}
    #global trend_data
    #trend_data = {}
    columns = dict(json.loads(data))['columns']
    print(columns)
    lists = json.loads(response.text)['data']
    for i in lists:
        try:
            x = i['d'][1]
        except TypeError:
            print(i, ' :Failed')
            continue
        sub = dict(zip(columns, i["d"]))
        try:
            trend, score = predict_trend(sub)
        except Exception as e:
            print(e)
            exit(0)
        print(f'The predicted trend is: {trend}')
        trend_data[x] = {'currency': sub['base_currency_desc'], 'trend': trend, 'score': score}

    print(trend_data)
    print("SUCCESS")
