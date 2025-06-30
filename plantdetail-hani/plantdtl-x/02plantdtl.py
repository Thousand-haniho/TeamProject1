import requests
import xmltodict
import json
import csv
import time
import os
from dotenv import load_dotenv

load_dotenv()
url = 'http://api.nongsaro.go.kr/service/garden/gardenDtl'
api_key = os.getenv('PLANT_API_KEY')

# cntntsNo와 cntntsSj 불러오기
plant_meta = {}
with open('plant_meta.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        plant_meta[row['cntntsNo']] = row['cntntsSj']

# 기존 필드 + cntntsSj 추가
fields = ['cntntsNo', 'cntntsSj', 'plntbneNm', 'plntzrNm', 'distbNm', 'fmlNm', 'fmlCodeNm', 'orgplceInfo',
    'adviseInfo', 'imageEvlLinkCours', 'growthHgInfo', 'growthAraInfo', 'lefStleInfo',
    'smellCode', 'smellCodeNm', 'toxctyInfo', 'prpgtEraInfo', 'etcEraInfo', 'managelevelCode',
    'managelevelCodeNm', 'grwtveCode', 'grwtveCodeNm', 'grwhTpCode', 'grwhTpCodeNm','winterLwetTpCode',
    'winterLwetTpCodeNm', 'hdCode', 'hdCodeNm', 'frtlzrInfo', 'soilInfo', 'watercycleSprngCode',
    'watercycleSprngCodeNm', 'watercycleSummerCode', 'watercycleSummerCodeNm', 'watercycleAutumnCode',
    'watercycleAutumnCodeNm', 'watercycleWinterCode', 'watercycleWinterCodeNm', 'dlthtsManageInfo',
    'speclmanageInfo', 'fncltyInfo', 'flpodmtBigInfo', 'flpodmtMddlInfo', 'flpodmtSmallInfo',
    'WIDTH_BIG_INFO', 'widthMddlInfo', 'widthSmallInfo', 'vrticlBigInfo', 'vrticlMddlInfo', 'vrticlSmallInfo',
    'hgBigInfo','hgMddlInfo','hgSmallInfo','volmeBigInfo','volmeMddlInfo','volmeSmallInfo','pcBigInfo',
    'pcMddlInfo','pcSmallInfo','managedemanddoCode','managedemanddoCodeNm','clCode','clCodeNm','grwhstleCode',
    'grwhstleCodeNm','indoorpsncpacompositionCode','indoorpsncpacompositionCodeNm','eclgyCode','eclgyCodeNm',
    'lefmrkCode', 'lefmrkCodeNm','lefcolrCode','lefcolrCodeNm','ignSeasonCode','ignSeasonCodeNm','flclrCode',
    'flclrCodeNm', 'fmldeSeasonCode','fmldeSeasonCodeNm','fmldecolrCode','fmldecolrCodeNm', 'prpgtmthCode',
    'prpgtmthCodeNm','lighttdemanddoCode','lighttdemanddoCodeNm','postngplaceCode','postngplaceCodeNm',
    'dlthtsCode','dlthtsCodeNm'
]

with open('plants.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()

    for cntntsNo, cntntsSj in plant_meta.items():
        params = {'apiKey': api_key, 'cntntsNo': cntntsNo}
        response = requests.get(url, params=params)
        data_dict = xmltodict.parse(response.content)
        data_json = json.loads(json.dumps(data_dict, ensure_ascii=False))
        body = data_json.get('response', {}).get('body', {})
        item = body.get('item', {})

        row = {field: item.get(field, '') for field in fields}
        row['cntntsNo'] = cntntsNo
        row['cntntsSj'] = cntntsSj  # 리스트 단계에서 가져온 제목

        writer.writerow(row)
        print(f"저장 완료: {cntntsNo} - {cntntsSj}")
        time.sleep(0.3)
