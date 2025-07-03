import os
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from matplotlib import font_manager, rc

# 📁 .env 파일 불러오기
load_dotenv()
CLIENT_ID = os.getenv('NAVER_AD_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('NAVER_AD_API_CLIENT_SECRET')

# 📁 파일 경로 설정
plants_default_path = "./resData/텃밭식물사전.csv"
popular_plants_path = "./saveFiles/crop_top10/popular_plants_20250702_170416.csv"

# 📦 CSV 파일 불러오기
plants_df = pd.read_csv(plants_default_path)
popular_df = pd.read_csv(popular_plants_path)

# ✅ 겹치는 식물 이름만 추출
matched_keywords = []
for _, plant_row in plants_df.iterrows():
    plant_name = str(plant_row['이름']).strip()

    if pd.notna(plant_name):
        matched = popular_df['title'].str.contains(plant_name, na=False, regex=False)
        if matched.any():
            matched_keywords.append(plant_name)

# 중복 제거 및 최대 5개만 사용
keywords = list(dict.fromkeys(matched_keywords))[:5]

if not keywords:
    print("❌ 겹치는 식물 키워드가 없습니다.")
    exit()

print("✅ 검색할 식물 키워드:", keywords)

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

# 🖋 폰트 설정 (한글용)
font_path = "./resData/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font',  family=font_name)

# 📊 결과 시각화
if response.status_code == 200:
    result = response.json()
    total_search_counts = []

    for group in result['results']:
        keyword = group['title']
        total = sum(item['ratio'] for item in group['data'])
        total_search_counts.append(total)

    plt.figure(figsize=(8, 8))
    plt.pie(total_search_counts, labels=keywords, autopct='%1.1f%%', startangle=140)
    plt.title("사람들이 많이 검색한 식물 키워드 (최근 30일 기준)")
    plt.axis('equal')

    # 이미지로 저장 (밑에 plt.show()보다 먼저 실행되어야 함.)
    save_path = "./saveFiles/crop_pie_chart.png"
    plt.savefig(save_path)
    print(f"✅ 차트 이미지 저장 완료: {save_path}")

    plt.show()

else:
    print("API 요청 실패:", response.status_code)
    print(response.text)

