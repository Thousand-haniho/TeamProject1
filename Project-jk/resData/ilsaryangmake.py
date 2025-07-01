import os
import requests
import json
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('KMA_API_KEY')

# 일사량조회 서비스
url = f'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php'

now = datetime.now()
base_date = now.strftime('%Y%m%d')
# print(base_date)

params = {
    'tm' : base_date,
    'stn' : 0,
    'help' : 0,
    'authKey' : api_key
}

# GET 요청
response = requests.get(url, params=params)
print('응답 원문 : ', response.text)


lines = response.text.strip().split('\n')
lines = lines[1:]

# 헤더 추출
header_line = lines[0].replace('#', '').strip()
columns = header_line.split()

# 데이터 줄 추출
data_lines = lines[1:]

parsed_rows = []
# 첫 번째 열 (날짜)에 작은따옴표 붙이기
for line in data_lines:
    row = line.split()
    # 연월일 뒤에 하이픈 추가
    if row:
        if len(row[0]) == 12:
            row[0] = f"{row[0][:8]}-{row[0][8:]}"
    parsed_rows.append(row)

print(parsed_rows)
# CSV로 저장
with open('backupData/kma_radiation_fixedwidth.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(parsed_rows)

print("CSV 저장 완료: kma_radiation_fixedwidth.csv")

import pandas as pd

# 원본 CSV 파일 읽기
with open('backupData/kma_radiation_fixedwidth.csv', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 첫 줄 제거 (2.3E+252)
lines = lines[1:]

# '#'으로 시작하는 줄 제거
lines = [line for line in lines if not line.strip().startswith('#')]

# 리스트를 다시 DataFrame으로 읽기
from io import StringIO
cleaned_data = StringIO(''.join(lines))
df = pd.read_csv(cleaned_data)

print(df)
df.columns = ['YYMMDDHHMI', 'STN', 'WD', 'WS', 'GST', 'GST', 'GST', 'PA' , 'PS', 'PT', 'PR' ,
              'TA', 'TD', 'HM', 'PV', 'RN', 'RN', 'RN', 'RN', 'SD', 'SD', 'SD', 'WC', 'WP', 'WW', 'CA', 'CA', 'CH' ,'CT',
              'CT', 'CT', 'CT', 'VS', 'SS', 'SI', 'ST', 'TS','TE','TE', 'TE', 'TE', 'ST', 'WH', 'BF', 'IR', 'IX']
df.to_csv('ilsaryang_all.csv', index=False)

