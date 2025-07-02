import requests
import csv
import os
import urllib.parse
from datetime import datetime
from dotenv import load_dotenv

### 네이버 쇼핑에서 top 인기 상품명+가격 데이터 가져오기 ###

# .env 파일 불러오기
load_dotenv()

# 환경변수에서 Client ID / Secret 가져오기
CLIENT_ID = os.getenv('NAVER_AD_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('NAVER_AD_API_CLIENT_SECRET')

# 검색어 설정
QUERY = "텃밭식물"
DISPLAY = 10  # 가져올 상품 수 (최대 100까지 가능)
URL = "https://openapi.naver.com/v1/search/shop.json"

# API 요청 헤더
headers = {
    "X-Naver-Client-Id": CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET
}

# 요청 파라미터
params = {
    "query": QUERY,
    "display": DISPLAY,
    "sort": "sim"  # sim: 유사도순, date: 날짜순, asc/desc: 가격순
}

# 요청
response = requests.get(URL, headers=headers, params=params)
if response.status_code != 200:
    print("❌ 요청 실패:", response.status_code, response.text)
    exit()

# 결과 파싱
items = response.json().get('items', [])

# 저장할 데이터 정리
results = []
for item in items:
    results.append({
        'title': item['title'].replace('<b>', '').replace('</b>', ''),
        'brand': item.get('brand', ''),
        'maker': item.get('maker', ''),
        'price': item['lprice'],
        'link': item['link']
    })

# 📂 저장할 폴더 경로 설정
save_directory = "./saveFiles/crop_top10"

# 📝 파일 이름 생성 (폴더 경로 포함)
filename = os.path.join(save_directory, f"popular_plants_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

with open(filename, mode='w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'brand', 'maker', 'price', 'link'])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ 실시간 인기 상품 정보 저장 완료 → '{filename}'")
