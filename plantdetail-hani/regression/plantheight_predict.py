from sklearn.svm import SVR
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 폰트 설정
font_path='../resData/malgun.ttf'
font_name=font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# csv 파일 읽기
def make_SVR_graph(fname):
    df = pd.read_csv(fname)
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

    # 선택한 파일에 맞는 이름을 x축에 쓰기 위해 이름 파싱
    str_fname = fname.split('/')
    plant_name = str_fname[len(str_fname) - 1]
    plant_name = plant_name.split('.')
    # print(plant_name)

    # 시각화
    plt.scatter(df['days'], y, label='관측값')
    plt.plot(df['days'], model.predict(X), color='green', label='SVR 예측선')
    plt.scatter([future_days], predicted, color='red', label='예측값')
    plt.xlabel(plant_name[0])
    plt.ylabel('키(cm)')
    plt.title('SVR을 통한 식물 생육 예측')
    plt.legend()
    plt.grid(True)
    plt.show()

target_name = '../resData/몬스테라.csv'
make_SVR_graph(target_name)