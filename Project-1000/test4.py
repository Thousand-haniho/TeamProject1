from test3 import fetch_kamis_data
import pandas as pd


def fetch_kamis_all_data():
    # 엑셀 파일 로드
    df_items = pd.read_excel("./resData/items.xlsx")
    # 결과 저장 리스트
    all_data = []

    # 반복 조회
    for idx, row in df_items.iterrows():
        itemcategorycode = row["부류코드"]
        itemcode = row["품목코드"]

        print(f"Fetching ({itemcategorycode}-{itemcode})...")
        df = fetch_kamis_data(itemcategorycode, itemcode)

        if not df.empty:
            all_data.append(df)

    # 전부 합치기
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        # 콘솔 출력
        # print(final_df)

        # Flask에 넘기려면 DataFrame 그대로 사용하거나, dict 리스트로 변환
        data_records = final_df.to_dict(orient="records")

        # 예: Flask로 넘길 때
        # return render_template("table.html", records=data_records)

        # 또는 그냥 변수에 담아두기
        result_data = data_records
        # print(result_data)
        return result_data
    else:
        print("데이터가 하나도 없습니다.")
        result_data = []



