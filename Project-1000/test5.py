from test4 import fetch_kamis_all_data


kamis_data = fetch_kamis_all_data()

평균_rows = [x for x in kamis_data if x.get("countyname") == "평균"]
등락률_rows = [x for x in kamis_data if x.get("countyname") == "등락률"]

# 평균 데이터 출력
print("--- 평균 데이터 ---")
for row in 평균_rows:
    itemname = row.get("itemname")
    unit = row.get("unit")
    price = row.get("price")
    print("품목명:", itemname, "| 단위:", unit, "| 가격:", price)

# 등락률 데이터 출력
print("--- 등락률 데이터 ---")
for row in 등락률_rows:
    weekprice = row.get("weekprice")
    print("등락률:", weekprice)