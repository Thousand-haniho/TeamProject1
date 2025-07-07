import pandas as pd
import os

### 식물사전에 가격(price) 추가 or 덮어쓰기 ###


# 경로 설정
plants_default_path = "./resData/plants_kor.csv"
updated_plants_path = "./saveFiles/plants_with_updated_price.csv"
popular_plants_path = "./saveFiles/popular_plants_20250628_1447442.csv"

# 1. 기존 식물사전 불러오기
if os.path.exists(updated_plants_path):
    plants_df = pd.read_csv(updated_plants_path)
    print("📘 기존 업데이트된 식물사전 불러옴")
else:
    plants_df = pd.read_csv(plants_default_path)
    plants_df['가격'] = pd.NA
    print("📘 기본 식물사전에서 시작")

# 2. 인기 식물 가격 정보 불러오기
popular_df = pd.read_csv(popular_plants_path)
popular_df['price'] = pd.to_numeric(popular_df['price'], errors='coerce')

# 3. 인기 식물에 해당하는 것만 업데이트
for p_idx, plant_row in plants_df.iterrows():
    plant_name = plant_row['컨텐츠 제목']

    if pd.notna(plant_name):
        # popular_df의 title에 plant_name이 포함되어 있으면 평균 계산
        '''
        .str.contains()는 정규표현식(regex)으로 문자열을 해석해서,
        오류발생. 때문에 regex=False를 명시적 지정.'''
        matching_prices = popular_df[
            popular_df['title'].str.contains(plant_name, na=False, regex=False)
        ]['price']

        if not matching_prices.empty:
            average_price = matching_prices.mean()
            rounded_price = round(average_price, -1)
            plants_df.loc[p_idx, '가격'] = rounded_price  # 덮어쓰기 가능!

# 4. 덮어쓰기 저장
plants_df.to_csv(updated_plants_path, index=False, encoding="utf-8-sig")
print(f"✅ 최신 인기 식물 가격으로 덮어쓰기 완료: {updated_plants_path} 저장됨")
