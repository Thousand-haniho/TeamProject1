import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import pandas as pd
from matplotlib import font_manager, rc

# 폰트 설정
font_path='../resData/malgun.ttf'
font_name=font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 데이터
df = pd.read_csv("../resData/몬스테라.csv")
X = df[['date']].values
y = df['height'].values

# SVR 모델 학습
svr_model = SVR(kernel='rbf', C=100, gamma='scale', epsilon=0.1)
svr_model.fit(X, y)

# 예측 데이터 생성 (부드러운 곡선을 위해)
X_plot = np.linspace(1, 12, 200).reshape(-1, 1)
y_plot = svr_model.predict(X_plot)

# 다음주차 예측
next_week_pred = svr_model.predict([[10]])[0]

# 그래프 생성
plt.figure(figsize=(12, 8))

# 실제 데이터 점들
plt.scatter(X, y, c='#2E86AB', s=120, alpha=0.8, label='실제 데이터', zorder=5, edgecolors='white', linewidth=2)

# SVR 예측 곡선
plt.plot(X_plot, y_plot, color='#F24236', linewidth=3, label='SVR 예측 곡선', alpha=0.8)

# 다음주차 예측 포인트
plt.scatter([10], [next_week_pred], c='#F24236', s=200,
           label=f'10주차 예측: {next_week_pred:.1f}', zorder=6, edgecolors='white', linewidth=2)

# 예측 구간 표시
plt.axvspan(9.5, 12, alpha=0.1, color='red', label='예측 구간')

# 그래프 꾸미기
plt.xlabel('주차 (Week)', fontsize=14, fontweight='bold')
plt.ylabel('길이 (Height)', fontsize=14, fontweight='bold')
plt.title('SVR을 이용한 길이 예측', fontsize=16, fontweight='bold', pad=20)

# 범례
plt.legend(fontsize=12, loc='upper left', frameon=True, fancybox=True, shadow=True)

# 격자
plt.grid(True, alpha=0.3, linestyle='--')

# 축 범위 설정
plt.xlim(0.5, 12.5)
plt.ylim(295, 325)

# 주요 포인트에 값 표시
for i, (x, y_val) in enumerate(zip(X.flatten(), y)):
    plt.annotate(f'{y_val:.1f}', (x, y_val), xytext=(5, 10),
                textcoords='offset points', fontsize=10, alpha=0.7)

# 10주차 예측값 표시
plt.annotate(f'{next_week_pred:.1f}', (10, next_week_pred), xytext=(10, 15),
            textcoords='offset points', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

# 여백 조정
plt.tight_layout()

# 그래프 표시
plt.show()

# 예측 결과 출력
print("=" * 50)
print("SVR 예측 결과")
print("=" * 50)
print(f"현재 길이 (9주차): {y[-1]:.3f}")
print(f"예측 길이 (10주차): {next_week_pred:.3f}")
print(f"변화량: {next_week_pred - y[-1]:.3f}")
print(f"변화율: {((next_week_pred - y[-1]) / y[-1] * 100):.2f}%")
print("=" * 50)

# JSON 데이터 생성 (HTML에서 사용)
import json

# 부드러운 곡선을 위한 더 세밀한 데이터
X_smooth = np.linspace(1, 12, 100).reshape(-1, 1)
y_smooth = svr_model.predict(X_smooth)

# HTML용 JSON 데이터
html_data = {
    "actual_data": {
        "dates": df['date'].tolist(),
        "heights": df['height'].tolist()
    },
    "prediction_curve": {
        "dates": X_smooth.flatten().tolist(),
        "heights": y_smooth.tolist()
    },
    "next_week_prediction": {
        "date": 10,
        "height": float(next_week_pred)
    },
    "statistics": {
        "current_height": float(y[-1]),
        "predicted_height": float(next_week_pred),
        "change": float(next_week_pred - y[-1]),
        "change_rate": float((next_week_pred - y[-1]) / y[-1] * 100)
    }
}

print("\n" + "=" * 50)
print("HTML용 JSON 데이터:")
print("=" * 50)