import logging
from fetch_kamis_data import fetch_kamis_data
import pandas as pd


def fetch_kamis_items_data():
    # 엑셀 파일 로드
    df_items = pd.read_excel("./resData/items.xlsx")
    # 결과 저장 리스트
    all_data = []

    # 반복 조회
    for idx, row in df_items.iterrows():
        itemcategorycode = row["부류코드"]
        itemcode = row["품목코드"]

        logging.basicConfig(level=logging.INFO)
        logging.info(f"Fetching ({itemcategorycode}-{itemcode})...")

        df = fetch_kamis_data(itemcategorycode, itemcode)

        if not df.empty:
            all_data.append(df)

    # 전부 합치기
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        data_records = final_df.to_dict(orient="records")

        평균_rows = [x for x in data_records if x.get("countyname") == "평균"]
        등락률_rows = [x for x in data_records if x.get("countyname") == "등락률"]

        kamis_data_result = []

        # zip으로 평균과 등락률 한 행씩 매칭
        for 평균, 등락률 in zip(평균_rows, 등락률_rows):
            kamis_data_result.append({
                "itemname": 평균.get("itemname"),
                "unit": 평균.get("unit"),
                "price": 평균.get("price"),
                "weekprice": 등락률.get("weekprice")
            })
        return kamis_data_result
    else:
        print("데이터가 하나도 없습니다.")



