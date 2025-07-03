import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
import pandas as pd
from matplotlib import font_manager, rc

# 폰트 설정
font_path = '../resData/malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 데이터 불러오기
df = pd.read_csv("../resData/방울토마토.csv")

# 입력값과 출력값 정의
X = df[['date']].values
y_height = df['height'].values
y_fruit = df['fruitnum'].values

# SVR 모델 정의 및 학습 (길이)
svr_height = SVR(kernel='rbf', C=100, epsilon=0.1)
svr_height.fit(X, y_height)

# SVR 모델 정의 및 학습 (열매 개수)
svr_fruit = SVR(kernel='rbf', C=100, epsilon=0.1)
svr_fruit.fit(X, y_fruit)

# 예측용 데이터 생성
X_plot = np.linspace(X.min(), X.max() + 2, 200).reshape(-1, 1)
y_height_plot = svr_height.predict(X_plot)
y_fruit_plot = svr_fruit.predict(X_plot)

# 다음 주차 예측
next_week = X.max() + 1
pred_height = svr_height.predict([[next_week]])[0]
pred_fruit = svr_fruit.predict([[next_week]])[0]

print("길이 예측값:", pred_height, "열매수 예측값:", pred_fruit)
# 그래프 생성
plt.figure(figsize=(12, 8))

# 실제 데이터 시각화
plt.scatter(X, y_height, c='blue', s=100, edgecolors='white', label='길이 (cm)', zorder=3)
plt.scatter(X, y_fruit, c='green', s=100, edgecolors='white', label='열매 개수', zorder=3)

# 예측 곡선 시각화
plt.plot(X_plot, y_height_plot, color='blue', linewidth=2.5, label='길이 예측')
plt.plot(X_plot, y_fruit_plot, color='green', linewidth=2.5, label='열매 개수 예측')

# 다음 주차 예측 포인트
plt.scatter([next_week], [pred_height], c='blue', s=200, marker='*', label=f'{next_week}주차 길이 예측: {pred_height:.1f}', zorder=5)
plt.scatter([next_week], [pred_fruit], c='green', s=200, marker='*', label=f'{next_week}주차 열매 개수 예측: {pred_fruit:.1f}', zorder=5)

# 축 및 제목 설정
plt.xlabel('주차 (Week)', fontsize=14, fontweight='bold')
plt.ylabel('값 (Height & Fruit)', fontsize=14, fontweight='bold')
plt.title('SVR을 이용한 길이 및 열매 개수 예측', fontsize=16, fontweight='bold')

# 주석 표시
plt.annotate(f'{pred_height:.1f}', (next_week, pred_height), textcoords="offset points", xytext=(10,10), fontsize=12, color='blue')
plt.annotate(f'{pred_fruit:.1f}', (next_week, pred_fruit), textcoords="offset points", xytext=(10,-15), fontsize=12, color='green')

# 기타 설정
plt.grid(True, linestyle='--', alpha=0.3)
plt.legend(fontsize=12, loc='upper left')
plt.xlim(X.min() - 1, next_week + 1)
plt.tight_layout()
plt.show()

# 예측 결과 출력
print("=" * 50)
print(f"{next_week}주차 예측 결과")
print("=" * 50)
print(f"현재 길이 ({X[-1][0]}주차): {y_height[-1]:.1f}cm → 예측: {pred_height:.1f}cm")
print(f"현재 열매 ({X[-1][0]}주차): {y_fruit[-1]:.1f}개 → 예측: {pred_fruit:.1f}개")
print("=" * 50)
