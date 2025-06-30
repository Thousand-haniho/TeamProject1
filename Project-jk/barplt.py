import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc


plt.style.use('default')

font_path = './resData/malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


# cp949 인코딩으로 읽기 (Windows 엑셀 CSV 대부분은 이거)
df = pd.read_csv("./resData/2022_환경_통합.csv", encoding='cp949')


df_filtered = df[['품목', '온도_내부','상대습도_내부','일사량_외부']]

df_filtered_5up = df_filtered[df_filtered['일사량_외부'] >= 5]

average_temp = df_filtered.groupby('품목')[['온도_내부','상대습도_내부','일사량_외부']].mean().reset_index()

out_data = ['가지','국화']

average_temp = average_temp[~average_temp['품목'].isin(out_data)]

df2 = average_temp.set_index('품목')


ax = df2.plot(kind='bar', figsize=(20,10), width=0.7,
              color=['#FF6B6B', '#4ECDC4', '#FFE66D'])

ax.set_xlabel('')  # 빈 문자열로 설정해서 x축 레이블 제거


for container in ax.containers:
    ax.bar_label(container, fmt='%.1f', label_type='edge', padding=3)

ax.set_title('품목별 평균 온도, 습도, 일사량', fontsize=20, pad=10)
ax.legend(['온도_내부 (°C)', '상대습도_내부 (%)', '일사량_외부 (W/m²)'], title='항목')
ax.tick_params(axis='x', rotation=0, pad=15,labelsize=12)

plt.show()




