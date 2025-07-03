import requests
import pandas as pd
import time

# Kakao API Key 설정
KAKAO_API_KEY = "8b89e1627df2cc9bf9a9bdd5dae1baa0"  # 카카오 디벨로퍼
headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}

# CSV 파일 불러오기
file_path = "./농림수산식품교육문화정보원_도시농업 교육기관 정보_20191108..csv"
df = pd.read_csv(file_path, encoding="cp949")  # 인코딩 문제 있을 경우 "cp949" 또는 "utf-8-sig"로 시도

# 기관명 리스트 추출
places = df["교육기관명"].dropna().unique().tolist()

results = []

# Kakao API로 검색
for place in places:
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    params = {
        "query": place,
        "size": 3  # 결과 여러 개일 경우 상위 3개만
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        data = res.json()
    except Exception as e:
        print(f"[JSON 디코딩 실패] {place}: {e}")
        continue

    if 'documents' in data and data['documents']:
        for doc in data['documents']:
            results.append({
                "검색어": place,
                "표시이름": doc['place_name'],
                "주소": doc.get('address_name', ''),
                "위도": doc['y'],
                "경도": doc['x'],
                "전화번호": doc.get('phone', ''),
                "카테고리": doc.get('category_name', '')
            })
    else:
        print(f"[검색 실패] {place} → 응답: {data}")
        results.append({
            "검색어": place,
            "표시이름": "검색 실패",
            "주소": "",
            "위도": "",
            "경도": "",
            "전화번호": "",
            "카테고리": ""
        })

    time.sleep(0.3)  # 속도 제한 고려

# 결과 저장
df_result = pd.DataFrame(results)
df_result.to_csv("도시농업_교육기관_좌표_결과.csv", index=False, encoding="cp949")
print("✅ CSV 저장 완료: 도시농업_교육기관_좌표_결과.csv")
