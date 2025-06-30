from datetime import datetime, timedelta
from dotenv import load_dotenv
import os, xmltodict, requests, json

def weather_data():
    load_dotenv()
    api_key = os.getenv('WEATHER_API_KEY')

    # 기준 시간 계산
    now = datetime.now()
    base_time = now.replace(minute=0, second=0, microsecond=0)
    if now.minute < 40:
        base_time -= timedelta(hours=1)

    base_date = base_time.strftime('%Y%m%d')
    base_time_str = base_time.strftime('%H%M')

    # 초단기실황조회 서비스 API 요청
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

    # 예보 항목 추출
    items = data_json['response']['body']['items']['item']

    # 컬럼명 한국어로 매핑
    column_mapping = {
        'baseDate': '발표일자',
        'baseTime': '발표시각',
        'obsrValue': '실황 값',
        'category': '자료구분코드',
        'nx': '예보지점 X 좌표',
        'ny': '예보지점 Y 좌표'
    }

    # 카테고리 코드를 한국어로 매핑
    category_map = {
        'T1H': '기온',
        'RN1': '1시간 강수량',
        'UUU': '동서바람성분',
        'VVV': '남북바람성분',
        'REH': '습도',
        'PTY': '강수형태',
        'VEC': '풍향',
        'WSD': '풍속'
    }

    # 테이블에 보여줄 데이터를 리스트로 정리
    weather_data = []
    for item in items:
        row = {}
        for key, value in item.items():
            if key == 'category':
                row[column_mapping[key]] = category_map.get(value, value)
            else:
                row[column_mapping[key]] = value
        weather_data.append(row)

    temp_value = next(
        (item['실황 값'] for item in weather_data if item['자료구분코드'] == '기온'),
        None
    )

    humi_value = next(
        (item['실황 값'] for item in weather_data if item['자료구분코드'] == '습도'),
        None
    )

    rain_value = next(
        (item['실황 값'] for item in weather_data if item['자료구분코드'] == '1시간 강수량'),
        None
    )

    wind_value = next(
        (item['실황 값'] for item in weather_data if item['자료구분코드'] == '풍속'),
        None
    )

    weather_dict = {
        'temp_value': temp_value,
        'humi_value': humi_value,
        'rain_value': rain_value,
        'wind_value': wind_value,
    }

    return weather_dict
