from flask import Flask, jsonify
from datetime import datetime, timedelta
import os
import requests
import xmltodict
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')
app = Flask(__name__)

@app.route('/weather')
def get_weather():
    # 기준 시간 계산
    now = datetime.now()
    base_time = now.replace(minute=0, second=0, microsecond=0)
    if now.minute < 40:
        base_time -= timedelta(hours=1)

    base_date = base_time.strftime('%Y%m%d')
    base_time_str = base_time.strftime('%H%M')

    # API 요청
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    params = {
        'serviceKey': api_key,
        'pageNo': '1',
        'numOfRows': '100',
        'dataType': 'XML',
        'base_date': base_date,
        'base_time': base_time_str,
        # 기준 지역 서울
        'nx': '60',
        'ny': '127'
    }

    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.content)
    data_json = json.loads(json.dumps(data_dict, ensure_ascii=False))

    items = data_json['response']['body']['items']['item']

    result = {}
    for item in items:
        category = item['category']
        value = item['obsrValue']
        result[category] = value

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
