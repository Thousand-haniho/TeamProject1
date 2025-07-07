import json
import csv

# 1. TXT 파일에서 JSON 데이터 읽기
with open('../resData/방울토마토.txt', 'r', encoding='utf-8') as txt_file:
    data = json.load(txt_file)  # JSON 배열로 파싱됨

# 2. CSV 파일로 저장
with open('../resData/방울토마토.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=['date', 'height','fruitnum'])
    writer.writeheader()
    writer.writerows(data)
