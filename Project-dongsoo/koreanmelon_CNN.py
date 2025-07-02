from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras import utils
import numpy as np

# 카테고리 정의
categories = ["nogunbyeong", "normal", "hyngalubyeong"]
nb_classes = len(categories)
image_size = 224

def main():
    # 데이터 로드
    data = np.load("./saveFiles/koreanmelon_dataset.npz")
    X_train = data["X_train"]
    X_test = data["X_test"]
    Y_train = data["Y_train"]
    Y_test = data["Y_test"]

    # 정규화
    X_train = X_train.astype("float32") / 255.0
    X_test = X_test.astype("float32") / 255.0

    # 원-핫 인코딩
    Y_train = utils.to_categorical(Y_train, nb_classes)
    Y_test = utils.to_categorical(Y_test, nb_classes)

    # 모델 학습 및 평가
    model = model_train(X_train, Y_train)
    model_eval(model, X_test, Y_test)

def build_model(input_shape=(224, 224, 3)):
    # 전이학습용 MobileNetV2
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_tensor=Input(shape=input_shape))
    base_model.trainable = False  # 기존 가중치 고정

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.5)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.3)(x)
    predictions = Dense(nb_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def model_train(X, Y):
    model = build_model(X.shape[1:])
    model.fit(X, Y, batch_size=32, epochs=20)
    model.save_weights("./saveFiles/koreanmelon_mobilenet.hdf5")
    return model

def model_eval(model, X, Y):
    score = model.evaluate(X, Y)
    print(f"🔍 손실값 (loss): {score[0]:.4f}")
    print(f"✅ 정확도 (accuracy): {score[1]*100:.2f}%")

if __name__ == "__main__":
    main()


# loss= 0.5503638982772827
# accuracy= 0.7840818166732788

# loss= 0.12748952209949493
# accuracy= 0.96334308385849