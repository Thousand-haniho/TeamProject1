import os
import requests
import xmltodict
import json
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('KMA_API_KEY')

# 일사량조회 서비스
url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php'

now = datetime.now()
base_date = now.strftime('%Y%m%d')
# print(base_date)

# 6개 지역만
stn_map = {
    102: '인천',
    108: '서울',
    253: '부산',
    137: '대구',
    156: '광주',
    133: '대전'
}

params ={
    'tm' : base_date,
    'stn' : 108,
    'help' : 0,
    'authKey' : api_key
}

columns = [
    "YYMMDDHHMI", "STN", "WD", "WS", "GST_WD", "GST_WS", "GST_TM",
    "PA", "PS", "PT", "PR", "TA", "TD", "HM", "PV", "RN_DAY",
    "RN_JUN", "RN_INT", "RN_HR3", "SD_DAY", "SD_TOT",
    "WC", "WP", "WW", "CA_TOT", "CA_MID", "CA_MIN", "CT_TOP", "CT_MID", "CT_LOW",
    "VS", "SS", "SI_5", "ST_10", "TS_20", "TE_30", "SEA", "WH", "BF", "IR", "IX"
]


for stn, city in stn_map.items():
    params['stn'] = str(stn)
    response = requests.get(url, params=params)

    # print('응답 원문 : ', response.text)

    # 텍스트 파싱
    lines = response.text.strip().split('\n')
    data_lines = [line for line in lines if not line.startswith('#') and line.strip() != '']

    if not data_lines:
        print(f" 데이터 없음 또는 파싱 실패")
        continue

    # 가장 최근 한 줄만 파싱
    data_values = data_lines[0].strip().split()
    data_dict = dict(zip(columns, data_values))

    # JSON 출력
    print(f"파싱 결과 (JSON):")
    print(json.dumps(data_dict, indent=2, ensure_ascii=False))

# lines = response.text.strip().split('\n')
# lines = lines[1:]
#
# # 헤더 추출
# header_line = lines[0].replace('#', '').strip()
# columns = header_line.split()
#
# # 데이터 줄 추출
# data_lines = lines[1:]
#
# parsed_rows = []
# # 첫 번째 열 (날짜)에 작은따옴표 붙이기
# for line in data_lines:
#     row = line.split()
#     # 연월일 뒤에 하이픈 추가
#     if row:
#         if len(row[0]) == 12:
#             row[0] = f"{row[0][:8]}-{row[0][8:]}"
#     parsed_rows.append(row)
#
# print(parsed_rows)
# # CSV로 저장
# with open('backupData/kma_radiation_fixedwidth.csv', 'w', newline='', encoding='utf-8-sig') as f:
#     writer = csv.writer(f)
#     writer.writerow(columns)
#     writer.writerows(parsed_rows)
#
# print("CSV 저장 완료: kma_radiation_fixedwidth.csv")
#
# import pandas as pd
#
# # 원본 CSV 파일 읽기
# with open('backupData/kma_radiation_fixedwidth.csv', 'r', encoding='utf-8') as f:
#     lines = f.readlines()
#
# # 첫 줄 제거 (2.3E+252)
# lines = lines[1:]
#
# # '#'으로 시작하는 줄 제거
# lines = [line for line in lines if not line.strip().startswith('#')]
#
# # 리스트를 다시 DataFrame으로 읽기
# from io import StringIO
# cleaned_data = StringIO(''.join(lines))
# df = pd.read_csv(cleaned_data)
#
# print(df)
# df.columns = ['YYMMDDHHMI', 'STN', 'WD', 'WS', 'GST', 'GST', 'GST', 'PA' , 'PS', 'PT', 'PR' ,
#               'TA', 'TD', 'HM', 'PV', 'RN', 'RN', 'RN', 'RN', 'SD', 'SD', 'SD', 'WC', 'WP', 'WW', 'CA', 'CA', 'CH' ,'CT',
#               'CT', 'CT', 'CT', 'VS', 'SS', 'SI', 'ST', 'TS','TE','TE', 'TE', 'TE', 'ST', 'WH', 'BF', 'IR', 'IX']
# df.to_csv('ilsaryang_all.csv', index=False)
#
#
# import pandas as pd
#
# df = pd.read_csv('backupData/ilsaryang_all.csv')
#
# df.rename(columns={
#     'YYMMDDHHMI' : '연월일-날짜',
#     'STN' : '관측지점정보',
#     'SS' : '일조(hr)',
#     'SI' : '일사(MJ/m2)'
# }, inplace=True)
#
# station_map = {
#     102: '인천',
#     108: '서울',
#     253: '부산',
#     137: '대구',
#     156: '광주',
#     133: '대전'
# }
#
# # 관측지점정보가 station_map 키에 포함된 행만 필터링
# df_filtered = df[df['관측지점정보'].isin(station_map.keys())]
#
# # 필요한 컬럼만 선택
# df_filtered = df_filtered[['연월일-날짜', '관측지점정보', '일조(hr)', '일사(MJ/m2)']]
# df_filtered['관측지점지역'] = df_filtered['관측지점정보'].map(station_map)
#
# # 저장
# df_filtered.to_csv('filtered_stations.csv', index=False)
