from test4 import fetch_kamis_all_data


kamis_data = fetch_kamis_all_data()

평균_row = next((x for x in kamis_data if x.get("countyname") == "평균"), None)
등락률_row = next((x for x in kamis_data if x.get("countyname") == "등락률"), None)

if 평균_row:
    itemname = 평균_row.get("itemname")
    unit = 평균_row.get("unit")
    price = 평균_row.get("price")
else:
    itemname = unit = price = None

if 등락률_row:
    weekprice = 등락률_row.get("weekprice")
else:
    weekprice = None

# 결과 출력
print("품목명:", itemname)
print("단위:", unit)
print("가격:", price)
print("등락률:", weekprice)