import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# 구글 트렌드
from pytrends.request import TrendReq
# 폰트 설정
font_path = "resData/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 1. pytrends 객체 생성
pytrends = TrendReq(hl='ko', tz=540)

# 📁 파일 경로 설정
plants_path = "./resData/농작물사전.csv"
# 📦 CSV 파일 불러오기
plants_df = pd.read_csv(plants_path)

keywords = []
for idx, plant_row in plants_df.iterrows():
    plant_name = str(plant_row['품목명']).strip()
    keywords.append(plant_name)

# 2. 검색 키워드 리스트
keywords = ["몬스테라", "스투키", "선인장", "아레카야자"]

# 3. 데이터 요청
pytrends.build_payload(keywords, timeframe='today 12-m')  # 최근 12개월

# 4. 데이터 가져오기
data = pytrends.interest_over_time()
data_clean = data.drop(columns=['isPartial'])
print(data_clean)

# 키워드별 총합 계산
keyword_sums = data_clean.sum().sort_values(ascending=False).reset_index()
keyword_sums.columns = ['식물명', '총 검색량']
keyword_sums['순위'] = keyword_sums.index + 1

# 등락률 예시(랜덤값)
import numpy as np
np.random.seed(0)
keyword_sums['등락률'] = np.random.randint(-5,6, size=len(keyword_sums))

# 컬럼 순서 맞추기
keyword_sums = keyword_sums[['순위','식물명','총 검색량','등락률']]

# 테이블 표시
fig, ax = plt.subplots(figsize=(6, len(keyword_sums)*0.6 + 1))
ax.axis('off')

# 컬러 테마
colors = [['#e1f5fe' if i%2==0 else '#b3e5fc']*4 for i in range(len(keyword_sums))]

# 테이블 생성
table = ax.table(
    cellText=keyword_sums.values,
    colLabels=keyword_sums.columns,
    cellColours=colors,
    cellLoc='center',
    loc='center'
)

table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1, 1.5)

# 헤더 스타일
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#0277bd')

plt.title("식물 키워드 12개월 검색 순위", fontsize=14, weight='bold')
plt.tight_layout()
plt.show()