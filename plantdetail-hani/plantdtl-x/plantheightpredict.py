from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from setuptools.command.rotate import rotate

# 폰트 설정
font_path='../resData/malgun.ttf'
font_name=font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 데이터 준비
data = [
    {"date": "20230823", "height": 129.645},
    {"date": "20230829", "height": 130.545},
    {"date": "20230905", "height": 130.665},
    {"date": "20230912", "height": 137.48},
    {"date": "20230919", "height": 144.185},
    {"date": "20230926", "height": 151.0},
    {"date": "20231003", "height": 157.815},
    {"date": "20231010", "height": 160.9},
    {"date": "20231017", "height": 159.54},
]
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
df['days'] = (df['date'] - df['date'].min()).dt.days

# X: 일(day), y: height
X = df[['days']].values
y = df['height'].values

# SVR 모델 학습 (RBF 커널 사용)
model = SVR(kernel='rbf', C=100, epsilon=0.5)
model.fit(X, y)

# 미래 예측: 2023-10-24
future_days = (pd.to_datetime('20231024', format='%Y%m%d') - df['date'].min()).days
predicted = model.predict([[future_days]])

print(f"SVR로 예측한 일주일 뒤 식물 키: {predicted[0]:.2f} cm")

# 시각화
plt.scatter(df['days'], y, label='관측값')
plt.plot(df['days'], model.predict(X), color='green', label='SVR 예측선')
plt.scatter([future_days], predicted, color='red', label='예측값')
plt.xlabel('화분이름')
plt.ylabel('키(cm)')
plt.title('SVR 식물 성장 예측')
plt.legend()
plt.grid(True)
plt.show()
