# pie.py
import os
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('NAVER_AD_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('NAVER_AD_API_CLIENT_SECRET')


def pie_data(category):
    if category == "foliage":
        category_name = "관엽식물"
        query = "관엽식물"
        plants_path = "./resData/관엽식물사전.csv"
    elif category == "farm":
        category_name = "텃밭식물"
        query = "텃밭식물"
        plants_path = "./resData/텃밭식물사전.csv"
    else:
        return {"error": "잘못된 요청입니다."}

    try:
        plants_df = pd.read_csv(plants_path)
        print("파일 읽기 완료:", plants_path)
    except FileNotFoundError:
        return {"error": "식물 사전 파일을 찾을 수 없습니다."}


    # 🛒 네이버 쇼핑 API 호출
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }
    params = {
        "query": query,
        "display": 50,
        "sort": "sim"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        return {"error": "네이버 쇼핑 API 오류"}

    items = response.json().get('items', [])
    popular_titles = [item['title'].replace(
        '<b>', '').replace('</b>', '') for item in items]

    matched_keywords = []
    for _, row in plants_df.iterrows():
        name = str(row['이름']).strip()
        if pd.notna(name) and any(name in title for title in popular_titles):
            matched_keywords.append(name)

    keywords = [kw for kw in dict.fromkeys(matched_keywords) if pd.notna(kw) and kw]  # 빈 문자열도 제외
    keywords = keywords[:5]

    if not keywords:
        return {"error": "검색 키워드 없음"}

    # 🔍 네이버 Datalab API 호출
    end = datetime.now()
    start = end - timedelta(days=30)
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')

    datalab_url = "https://openapi.naver.com/v1/datalab/search"
    datalab_headers = {
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

    dl_response = requests.post(
        datalab_url,
        headers=datalab_headers,
        json=body
    )
    if dl_response.status_code != 200:
        print("에러 응답:", dl_response.text)
        return {"error": "검색량 API 오류"}

    result = dl_response.json()
    chart_data = []
    for group in result['results']:
        title = group['title']
        total = sum(item['ratio'] for item in group['data'])
        chart_data.append({"label": title, "value": total})

    return {
        "chart_data": chart_data,
        "category_name": category_name
    }


print(pie_data("farm"))
