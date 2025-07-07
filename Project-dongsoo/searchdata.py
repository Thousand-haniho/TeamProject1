import requests
import xmltodict
import json

### 식물사전에서 데이터 찾기 ###

url = 'http://api.nongsaro.go.kr/service/garden/gardenList'
api_key = '20250626K8HCI4KNPYS4XFEDFUBXVA'

plant_ids = []

# 예: 1~25페이지 돌면서 수집 (200개 이상)
for page in range(1, 26):
    params = {
        'apiKey': api_key,
        'pageNo': page,
    }

    response = requests.get(url, params=params)
    data_dict = xmltodict.parse(response.content)
    data_json = json.loads(json.dumps(data_dict, ensure_ascii=False))

    items = data_json.get('response', {}).get('body', {}).get('items', {}).get('item', [])
    if isinstance(items, dict):  # 하나만 나올 때
        items = [items]

    for item in items:
        cntntsSj = item.get('cntntsSj')
        if cntntsSj:
            plant_ids.append(cntntsSj)

print(f"총 수집된 식물 ID 수: {len(plant_ids)}")
print(plant_ids)  # 이걸 복사해서 리스트로 쓸 수 있음

with open('plant_name.txt', 'w', encoding='utf-8') as f:
    for pid in plant_ids:
        f.write(pid + '\n')