import pandas as pd

df = pd.read_csv('plants_kor.csv')

plant_basicinfo = df[['식물 명', '생육 온도 코드명', '습도 코드명', '광요구도 코드명(콤마(,)로 구분)']]
plant_basicinfo = plant_basicinfo.rename(columns={
    '생육 온도 코드명' : '적정 온도',
    '습도 코드명' : '적정 습도',
    '광요구도 코드명(콤마(,)로 구분)' : '적정 조도'
})

plant_basicinfo.to_csv('plant_basicinfo.csv', index=False, encoding='utf-8-sig')