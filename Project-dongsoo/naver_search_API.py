import os

import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from matplotlib import font_manager, rc

# .env 파일 불러오기
load_dotenv()

CLIENT_ID = os.getenv('NAVER_AD_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('NAVER_AD_API_CLIENT_SECRET')

# ✅ 검색할 식물 키워드
keywords = ["홍콩야자", "오렌지자스민", "필레아페페", "몬스테라", "스투키"]

# 📅 최근 30일 날짜 범위
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

start_str = start_date.strftime('%Y-%m-%d')
end_str = end_date.strftime('%Y-%m-%d')

# 📦 API 요청용 headers & body
url = "https://openapi.naver.com/v1/datalab/search"

headers = {
    "X-Naver-Client-Id": CLIENT_ID,
    "X-Naver-Client-Secret": CLIENT_SECRET,
    "Content-Type": "application/json"
}

# 검색어 그룹
keyword_groups = [{"groupName": kw, "keywords": [kw]} for kw in keywords]

body = {
    "startDate": start_str,
    "endDate": end_str,
    "timeUnit": "date",
    "keywordGroups": keyword_groups,
    "device": "pc",
    "ages": [],
    "gender": ""
}

response = requests.post(url, headers=headers, data=json.dumps(body))

# 폰트설정
font_path = "./resData/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font',  family=font_name)

if response.status_code == 200:
    result = response.json()
    total_search_counts = []

    for group in result['results']:
        keyword = group['title']
        total = sum(item['ratio'] for item in group['data'])  # 'ratio'는 검색 비율
        total_search_counts.append(total)

    # 🎨 파이차트 그리기
    plt.figure(figsize=(8, 8))
    plt.pie(total_search_counts, labels=keywords, autopct='%1.1f%%', startangle=140)
    plt.title("사람들이 많이 검색한 식물 키워드 (최근 30일 기준)")
    plt.axis('equal')
    plt.show()
else:
    print("API 요청 실패:", response.status_code)
    print(response.text)
