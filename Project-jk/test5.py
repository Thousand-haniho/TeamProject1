from fetch_kamis_items_data import fetch_kamis_items_data


kamis_data = fetch_kamis_items_data()

평균_rows = [x for x in kamis_data if x.get("countyname") == "평균"]
등락률_rows = [x for x in kamis_data if x.get("countyname") == "등락률"]

kamis_data_result = []

# zip으로 평균과 등락률 한 행씩 매칭
for 평균, 등락률 in zip(평균_rows, 등락률_rows):
    kamis_data_result.append({
        "itemname": 평균.get("itemname"),
        "unit": 평균.get("unit"),
        "price": 평균.get("price"),
        "weekprice": 등락률.get("weekprice")
    })

# print(kamis_data_result)