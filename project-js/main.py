from flask import Flask, render_template, request, jsonify

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

# ----------------------------- 모델 정보 -----------------------------
# MODEL_INFO = {
#     '딸기': {
#         'path': 'D:\project-js\project-js\딸기\모델\strawberry_cnn_model.h5',
#         'categories': ["잿빛곰팡이병", "정상", "흰가루병"],
#         'input_size': (64, 64)
#     },
#     # 귤, 레몬, 참외 등 필요시 추가
# }

# models = {fruit: load_model(info['path']) for fruit, info in MODEL_INFO.items()}

# def preprocess_image(image_file, target_size):
#     img = Image.open(image_file).convert('RGB')
#     img = img.resize(target_size)
#     img_array = img_to_array(img) / 255.0
#     return np.expand_dims(img_array, axis=0)

# ----------------------------- ROUTES -----------------------------

@app.route('/')
def index():
    return render_template('sds.html')
이부분부터
# @app.route('/plant_disease')
# def plant_disease():
#     fruits = list(MODEL_INFO.keys())
#     return render_template('plant_disease.html', fruits=fruits)

# @app.route('/predict', methods=['POST'])
# def predict():
#     fruit = request.form.get('fruit')
#     image = request.files.get('image')

#     if not fruit or fruit not in models:
#         return jsonify({'error': '지원하지 않는 과일입니다.'}), 400
#     if not image:
#         return jsonify({'error': '이미지를 첨부해주세요.'}), 400

#     try:
#         info = MODEL_INFO[fruit]
#         input_data = preprocess_image(image, info['input_size'])
#         prediction = models[fruit].predict(input_data)
#         idx = int(np.argmax(prediction))
#         confidence = float(prediction[0][idx])
#         disease = info['categories'][idx]

#         return jsonify({'disease': disease, 'confidence': confidence})
#     except Exception as e:
#         return jsonify({'error': '서버 에러 발생: ' + str(e)}), 500
이부분

@app.errorhandler(404)
def page_not_found(error):
    print('오류 로그:', error)
    return "페이지가 없습니다. URL를 확인하세요.", 404

# ----------------------------- 실행 -----------------------------
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    



