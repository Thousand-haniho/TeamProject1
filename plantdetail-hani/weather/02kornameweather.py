import os
import requests
import xmltodict
import json
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('WEATHER_API_KEY')

# 초단기실황조회 서비스
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'

now = datetime.now()
base_time = now.replace(minute=0, second=0, microsecond=0)
if now.minute < 40:
    base_time -= timedelta(hours=1)

base_date = base_time.strftime('%Y%m%d')
base_time_str = base_time.strftime('%H%M')

# 지역별 격자 좌표
locaions = {
    '서울': (60, 127),
    '부산': (98, 76),
    '대구': (89, 90),
    '인천': (55, 124),
    '광주': (58, 74),
    '대전': (67, 100),
    '울산': (102, 84),
    '세종': (66, 103),
    '경기북부' : (61, 130),
    '경기남부': (60, 120),
    '강원': (73, 134),
    '충북': (69, 107),
    '충남': (68, 100),
    '전북': (63, 89),
    '전남': (51, 67),
    '경북': (89, 91),
    '경남': (91, 77),
    '제주': (52, 38)
}

params ={
  'serviceKey' : api_key,
  'pageNo' : '1',
  'numOfRows' : '100',
  'dataType' : 'XML',
  'base_date' : base_date,
  'base_time' : base_time_str,
  # 서울 임시값(반복문 돌면서 바뀔 것)
  'nx' : '60',
  'ny' : '127'
}

# 한국어로 컬럼 매핑
column_mapping = {
    'baseDate' : '발표일자',
    'baseTime' : '발표시각',
    'obsrValue' : '실황 값',
    'category' : '자료구분코드',
    'nx' : '예보지점 X 좌표',
    'ny' : '예보지점 Y 좌표'
}

# 카테고리명 한국어로 매핑
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

# CSV로 저장
with open('weather_forecast_all.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = None

    for city, (nx, ny) in locaions.items():
        params['nx'] = str(nx)
        params['ny'] = str(ny)

        response = requests.get(url, params=params)
        data_dict = xmltodict.parse(response.content)
        data_json = json.loads(json.dumps(data_dict, ensure_ascii=False))
        # print(data_json)

        try:
            # 예보 항목 추출
            items = data_json['response']['body']['items']['item']
        except KeyError:
            print(f"{city} 지역 데이터 없음")
            continue

        if items:  # 데이터가 있을 경우
            if writer is None:
                # 첫 행 한국어 키값으로 헤더 지정
                fieldnames = ['지역'] + [column_mapping[key] for key in items[0].keys()]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

            for item in items:
                row = {'지역' : city}
                for key, value in item.items():
                    if key == 'category':
                        # 카테고리 코드를 한글로 변경
                        row[column_mapping[key]] = category_map.get(value, value)
                    else:
                        # 카테고리 코드가 아니면 값을 그대로
                        row[column_mapping[key]] = value
                writer.writerow(row)