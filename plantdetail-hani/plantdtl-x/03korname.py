import csv

input_file = 'plants.csv'
output_file = 'plants_kor.csv'

column_mapping = {
    'cntntsNo': '컨텐츠 번호',
    'plntbneNm': '식물학 명',
    'plntzrNm': '식물영 명',
    'distbNm': '유통 명',
    'fmlNm': '과 명',
    'fmlCodeNm': '과 코드명',
    'orgplceInfo': '원산지 정보',
    'adviseInfo': '조언 정보',
    'imageEvlLinkCours': '이미지 평가 링크 경로',
    'growthHgInfo': '성장 높이 정보',
    'growthAraInfo': '성장 넓이 정보',
    'lefStleInfo': '잎 형태 정보',
    'smellCode': '냄새 코드',
    'smellCodeNm': '냄새 코드 명',
    'toxctyInfo': '독성 정보',
    'prpgtEraInfo': '번식 시기 정보',
    'etcEraInfo': '기타 시기 정보',
    'managelevelCode': '관리수준 코드',
    'managelevelCodeNm': '관리수준 코드명',
    'grwtveCode': '생장속도 코드',
    'grwtveCodeNm': '생장속도 코드명',
    'grwhTpCode': '생육 온도 코드',
    'grwhTpCodeNm': '생육 온도 코드명',
    'winterLwetTpCode': '겨울 최저 온도 코드',
    'winterLwetTpCodeNm': '겨울 최저 온도 코드명',
    'hdCode': '습도 코드',
    'hdCodeNm': '습도 코드명',
    'frtlzrInfo': '비료 정보',
    'soilInfo': '토양 정보',
    'watercycleSprngCode': '물주기 봄 코드',
    'watercycleSprngCodeNm': '물주기 봄 코드명',
    'watercycleSummerCode': '물주기 여름 코드',
    'watercycleSummerCodeNm': '물주기 여름 코드명',
    'watercycleAutumnCode': '물주기 가을 코드',
    'watercycleAutumnCodeNm': '물주기 가을 코드명',
    'watercycleWinterCode': '물주기 겨울 코드',
    'watercycleWinterCodeNm': '물주기 겨울 코드명',
    'dlthtsManageInfo': '병충해 관리 정보',
    'speclmanageInfo': '특별관리 정보',
    'fncltyInfo': '기능성 정보',
    'flpodmtBigInfo': '화분직경 대 정보',
    'flpodmtMddlInfo': '화분직경 중 정보',
    'flpodmtSmallInfo': '화분직경 소 정보',
    'WIDTH_BIG_INFO': '가로 대 정보',
    'widthMddlInfo': '가로 중 정보',
    'widthSmallInfo': '가로 소 정보',
    'vrticlBigInfo': '세로 대 정보',
    'vrticlMddlInfo': '세로 중 정보',
    'vrticlSmallInfo': '세로 소 정보',
    'hgBigInfo': '높이 대 정보',
    'hgMddlInfo': '높이 중 정보',
    'hgSmallInfo': '높이 소 정보',
    'volmeBigInfo': '볼륨 대 정보',
    'volmeMddlInfo': '볼륨 중 정보',
    'volmeSmallInfo': '볼륨 소 정보',
    'pcBigInfo': '가격 대 정보',
    'pcMddlInfo': '가격 중 정보',
    'pcSmallInfo': '가격 소 정보',
    'managedemanddoCode': '관리요구도 코드',
    'managedemanddoCodeNm': '관리요구도 코드명',
    'clCode': '분류 코드(콤마(,)로 구분)',
    'clCodeNm': '분류 코드명(콤마(,)로 구분)',
    'grwhstleCode': '생육형태 코드(콤마(,)로 구분)',
    'grwhstleCodeNm': '생육형태 코드명(콤마(,)로 구분)',
    'indoorpsncpacompositionCode': '실내정원구성 코드(콤마(,)로 구분)',
    'indoorpsncpacompositionCodeNm': '실내정원구성 코드명(콤마(,)로 구분)',
    'eclgyCode': '생태 코드(콤마(,)로 구분)',
    'eclgyCodeNm': '생태 코드명(콤마(,)로 구분)',
    'lefmrkCode': '잎무늬 코드(콤마(,)로 구분)',
    'lefmrkCodeNm': '잎무늬 코드명(콤마(,)로 구분)',
    'lefcolrCode': '잎색 코드(콤마(,)로 구분)',
    'lefcolrCodeNm': '잎색 코드명(콤마(,)로 구분)',
    'ignSeasonCode': '발화 계절 코드(콤마(,)로 구분)',
    'ignSeasonCodeNm': '발화 계절 코드명(콤마(,)로 구분)',
    'flclrCode': '꽃색 코드(콤마(,)로 구분)',
    'flclrCodeNm': '꽃색 코드명(콤마(,)로 구분)',
    'fmldeSeasonCode': '과일 계절(콤마(,)로 구분)',
    'fmldeSeasonCodeNm': '과일 계절 코드명(콤마(,)로 구분)',
    'fmldecolrCode': '과일색 코드(콤마(,)로 구분)',
    'fmldecolrCodeNm': '과일색 코드명(콤마(,)로 구분)',
    'prpgtmthCode': '번식방법 코드(콤마(,)로 구분)',
    'prpgtmthCodeNm': '번식방법 코드명(콤마(,)로 구분)',
    'lighttdemanddoCode': '광요구도 코드(콤마(,)로 구분)',
    'lighttdemanddoCodeNm': '광요구도 코드명(콤마(,)로 구분)',
    'postngplaceCode': '배치장소 코드(콤마(,)로 구분)',
    'postngplaceCodeNm': '배치장소 코드명(콤마(,)로 구분)',
    'dlthtsCode': '병충해 코드(콤마(,)로 구분)',
    'dlthtsCodeNm': '병충해 코드(콤마(,)로 구분)',
    'cntntsSj': '식물 명'
}


with open(input_file, 'r', encoding='utf-8-sig') as infile, \
     open(output_file, 'w', encoding='utf-8-sig', newline='') as outfile:

    reader = csv.DictReader(infile)
    fieldnames_eng = reader.fieldnames

    # 컬럼명을 한글로 변환 (없는 항목은 그대로 유지)
    fieldnames_kor = [column_mapping.get(col, col) for col in fieldnames_eng]

    writer = csv.DictWriter(outfile, fieldnames=fieldnames_kor)
    writer.writeheader()

    for row in reader:
        writer.writerow({column_mapping.get(k, k): v for k, v in row.items()})
