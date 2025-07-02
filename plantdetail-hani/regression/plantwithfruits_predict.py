from sklearn.svm import SVR
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np

# 한글 폰트 설정 (필요한 경우만)
font_path = '../resData/malgun.ttf'  # 본인 경로에 맞게 수정
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

def make_SVR_graph(fname):
    # CSV 읽기
    data = pd.read_csv(fname)
    data['week'] = data['date'].astype(str).str.extract(r'(\d+)').astype(int)

    X = data[['week']].values

    # height 예측용 SVR
    svr_height = SVR(kernel='rbf', C=100, epsilon=0.5)
    svr_height.fit(X, data['height'])

    # fruitnum 예측용 SVR
    svr_fruit = SVR(kernel='rbf', C=10, epsilon=0.1)
    svr_fruit.fit(X, data['fruitnum'])

    # 다음 주차 예측 (마지막 주차 + 1)
    next_week = data['week'].max() + 1
    X_pred = np.array([[next_week]])
    pred_height = svr_height.predict(X_pred)[0]
    pred_fruit = svr_fruit.predict(X_pred)[0]

    print(f"SVR 예측 → {next_week}주차 키: {pred_height:.1f} cm / 열매 수: {pred_fruit:.1f} 개")

    # 시각화
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # 키 시각화
    ax1.plot(data['week'], data['height'], 'g-o', label='식물 키(cm)')
    ax1.plot(data['week'], svr_height.predict(X), 'g--', alpha=0.6, label='SVR 키 예측선')
    ax1.scatter([next_week], [pred_height], color='green', marker='^', s=100, label='예측 키')
    ax1.set_xlabel('주차')
    ax1.set_ylabel('키 (cm)', color='g')
    ax1.tick_params(axis='y', labelcolor='g')
    ax1.grid(True)

    # 열매 수 시각화
    ax2 = ax1.twinx()
    ax2.plot(data['week'], data['fruitnum'], 'r-s', label='열매 수')
    ax2.plot(data['week'], svr_fruit.predict(X), 'r--', alpha=0.6, label='SVR 열매 예측선')
    ax2.scatter([next_week], [pred_fruit], color='red', marker='^', s=100, label='예측 열매 수')
    ax2.set_ylabel('열매 수', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # 범례 통합
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('주차별 식물 키 및 열매 수 + SVR 예측')
    fig.tight_layout()
    plt.show()
target_name = '../resData/방울토마토.csv'
make_SVR_graph(target_name)