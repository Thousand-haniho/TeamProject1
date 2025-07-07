import os
import requests
import xmltodict
import json
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pandas as pd
import cx_Oracle as cx
import os

os.environ["NLS_LANG"] = ".AL32UTF8"  # 한글 깨짐 방지

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
locations = {
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

for city, (nx, ny) in locations.items():
    params['nx'] = str(nx)
    params['ny'] = str(ny)

    # 딕셔너리 -> JSON 형식으로 변경
    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.content)
    data_json = json.loads(json.dumps(data_dict, ensure_ascii=False))
    # print(data_json)


# 오라클 접속을 위한 정보를 변수로 정의
host_name = '192.168.0.29'
oracle_port = 1521
service_name = 'XEPDB1'
# 연결정보를 객체로 정의
connect_info = cx.makedsn(host_name, oracle_port, service_name)
# 커넥션 객체 생성
conn = cx.connect('dongsoo', '1234', '192.168.0.29:1521/XEPDB1')

# 쿼리문 실행을 위한 커서 생성
cursor = conn.cursor()



# 인파라미터가 있는 insert 쿼리문. ':변수명'과 같이 기술한다.
sql="""insert into weather (
    idx, 지역, 발표일자, 발표시각, 자료구분코드, 예보지점X좌표, 예보지점Y좌표, 실황값
    )
    values (
    seq_board_num.nextval, :지역, :발표일자, :발표시각, :자료구분코드, :예보지점X좌표, :예보지점Y좌표, :실황값
    ) """

# 데이터 수집 및 저장
for city, (nx, ny) in locations.items():
    params['nx'] = str(nx)
    params['ny'] = str(ny)

    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.content)
    items = data_dict.get('response', {}).get('body', {}).get('items', {}).get('item', [])

    for item in items:
        try:
            category_code = item.get('category')
            category_korean = category_map.get(category_code, category_code)

            cursor.execute(sql, {
                '지역': city,
                '발표일자': item.get('baseDate'),
                '발표시각': item.get('baseTime'),
                '자료구분코드': category_korean,
                '실황값': item.get('obsrValue'),
                '예보지점X좌표': int(item.get('nx')),
                '예보지점Y좌표': int(item.get('ny'))
            })

            print(f"[✅ 저장됨] {city} - {item.get('category')} : {item.get('obsrValue')}")
            conn.commit()
        except Exception as e:
            # 예외가 발생했다면 롤백 처리
            conn.rollback()
            print("insert 실행시 오류발생", e)

# DB 연결 해제
conn.close()