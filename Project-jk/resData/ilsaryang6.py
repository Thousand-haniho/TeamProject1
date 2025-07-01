import pandas as pd

df = pd.read_csv('backupData/ilsaryang_all.csv')

df.rename(columns={
    'YYMMDDHHMI' : '연월일-날짜',
    'STN' : '관측지점정보',
    'SS' : '일조(hr)',
    'SI' : '일사(MJ/m2)'
}, inplace=True)

station_map = {
    102: '인천',
    108: '서울',
    253: '부산',
    137: '대구',
    156: '광주',
    133: '대전'
}

# 관측지점정보가 station_map 키에 포함된 행만 필터링
df_filtered = df[df['관측지점정보'].isin(station_map.keys())]

# 필요한 컬럼만 선택
df_filtered = df_filtered[['연월일-날짜', '관측지점정보', '일조(hr)', '일사(MJ/m2)']]
df_filtered['관측지점지역'] = df_filtered['관측지점정보'].map(station_map)

# 저장
df_filtered.to_csv('filtered_stations.csv', index=False)
