from sklearn.model_selection import train_test_split
from PIL import Image
import glob
import numpy as np

# 분류 대상 카테고리
root_dir = "./download/참외데이터/Training/01.원천데이터"
categories = ["nogunbyeong", "normal", "hyngalubyeong"]
# 카테고리 갯수
nb_classes = len(categories)
# 이미지 크기
image_size = 224

# 이미지 및 레이블 데이터를 저장할 리스트
X = []
Y = []
# 각 카테고리별로 이미지 파일을 불러와서 처리
for idx, cat in enumerate(categories):
    # 경로를 조립한 후 jpg 파일 가져오기
    image_dir = root_dir + "/" + cat
    # 각 카테고리 폴더에 있는 모든 jpg 파일을 리스트로 반환
    files = glob.glob(image_dir + "/*.jpg")
    # 파일 갯수만큼 반복
    for i, f in enumerate(files):
        print(i, image_dir, f, "처리중")
        # 이미지 파일 오픈 및 변환
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_size, image_size))
        # 이미지 픽셀값을 넘파이 배열로 변환
        data = np.asarray (img)
        # 넘파이 배열로 변환된 이미지와 카테고리 인덱스 추가
        X.append(data)
        Y.append (idx)
        # if i== 1:
        #       print(idx, data)

# 리스트를 Numpy 배열로 변환
X = np.array(X) # 이미지 데이터
Y = np.array(Y) # 레이블 데이터

# 학습 전용 데이터와 테스트 전용 데이터 분류
'''
X_train : 훈련용 입력 데이터 (학습용)
X_test : 테스트용 입력 데이터
Y_train : 훈련용 정답 레이블
Y_test : 테스트용 정답 레이블
'''
X_train, X_test, Y_train, Y_test = train_test_split(X, Y)

# 파일로 저장
np.savez("./saveFiles/koreanmelon.npz", X_train=X_train, X_test=X_test,
         Y_train=Y_train, Y_test=Y_test)
print("Task Finished..!!", len(Y))