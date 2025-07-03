import pandas as pd
from sklearn.svm import SVR

# 데이터 로드(텃밭식물만)
# 실내식물 : 몬스테라, 스투키, 오렌지쟈스민, 홍콩야자
# 텃밭식물 : 방울토마토, 오이, 파프리카
df = pd.read_csv("../resData/방울토마토.csv")

def make_json():
    X = df[['date']].values
    y_height = df['height'].values
    y_fruitnum = df['fruitnum'].values

    # SVR 모델 학습 - 길이
    svr_model = SVR(kernel='rbf', C=100, gamma='scale', epsilon=0.1)
    svr_model.fit(X, y_height)

    # SVR 모델 학습 - 열매 개수
    svr_model = SVR(kernel='rbf', C=100, gamma='scale', epsilon=0.1)
    svr_model.fit(X, y_fruitnum)

    # 다음 주차 예측
    next_week = df['date'].max() + 1
    pred_height = float(round(svr_model.predict([[next_week]])[0], 2))
    pred_fruit = float(round(svr_model.predict([[next_week]])[0]))

    # 원본 데이터 + 예측값 포함 리스트 생성
    data_with_prediction = df.to_dict(orient='records')  # 기존 데이터를 딕셔너리 리스트로 변환
    data_with_prediction.append({
        'date': next_week,
        'height': pred_height,
        'fruitnum' : pred_fruit})

    return data_with_prediction

print(make_json())