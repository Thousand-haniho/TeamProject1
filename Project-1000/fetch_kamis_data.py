import requests
import xmltodict
import pandas as pd
from datetime import datetime
import json


def fetch_kamis_data(itemcategorycode, itemcode):
    url = "http://www.kamis.or.kr/service/price/xml.do?action=ItemInfo"

    # 오늘 날짜
    today = datetime.today()

    # 원하는 형식으로 문자열로 변환
    today_str = today.strftime("%Y-%m-%d")

    # 필요하면 파라미터나 헤더
    params = {
    "p_cert_key": "85b4970a-81f2-417f-8bc2-b6815c6b3cf6",
        "p_productclscode": "01",
        "p_countycode": "1101", # 시군구 코드
        "p_regday": today_str,
        "p_itemcategorycode": str(itemcategorycode), # 부류코드
        "p_itemcode": str(itemcode), # 품목코드
        # "p_kindcode": "00", # 품종코드
        "p_productrankcode": "04", # 등급코드
        "p_convert_kg_yn": "Y",
        "p_cert_id": "5910",  # 요청자id
        "p_returntype": "xml",
    }
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml"
    }

    try:
        # GET 요청으로 XML 가져오기
        response = requests.get(url, params=params, headers=headers)
        # 응답 상태 체크
        response.raise_for_status()
        # response.text에 XML 문자열이 들어있음
        xml_string = response.text

        data_dict = xmltodict.parse(xml_string)
        # 'document' -> 'data' -> 'item'에 데이터 리스트가 있음
        items = data_dict["document"]["data"].get("item")

        # DataFrame으로 변환
        df = pd.DataFrame(items)
        df = df.bfill()

        # 콘솔에 출력
        # pd.set_option('display.max_rows', None)
        # print(df)
        return df

    except Exception as e:
        print(f"[{itemcode}] 오류 발생: {e}")
        return pd.DataFrame()

