from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np

app = Flask(__name__)

MODEL_INFO = {
    '딸기': {
        'path': 'D:/project plantmap/TeamProject1/Project-cheon/딸기/모델/strawberry_cnn_model.h5',
        'categories': ["잿빛곰팡이병", "정상", "흰가루병"],
        'input_size': (64, 64)
    },
    '귤': {
        'path': './models/tangerine_cnn_model.h5',
        'categories': ["정상", "병"],
        'input_size': (64, 64)
    },
    '레몬': {
        'path': './models/lemon_cnn_model.h5',
        'categories': ["정상", "병"],
        'input_size': (64, 64)
    },
    '참외': {
        'path': './models/melon_cnn_model.h5',
        'categories': ["정상", "병"],
        'input_size': (64, 64)
    }
}

# 모델 미리 로드
models = {}
for fruit, info in MODEL_INFO.items():
    models[fruit] = load_model(info['path'])

def preprocess_image(image_file, target_size):
    img = Image.open(image_file).convert('RGB')
    img = img.resize(target_size)
    img_array = img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# 일반 페이지 경로
@app.route('/plant_disease')
def plant_disease():
    fruits = list(MODEL_INFO.keys())
    return render_template('plant_disease.html', fruits=fruits)

@app.route('/plant_disease/api/predict', methods=['POST'])
def api_predict():
    fruit = request.form.get('fruit')
    image = request.files.get('image')

    if fruit not in models:
        return jsonify({'error': '지원하지 않는 과일입니다.'}), 400
    if image is None:
        return jsonify({'error': '이미지를 첨부해주세요.'}), 400

    try:
        info = MODEL_INFO[fruit]
        input_data = preprocess_image(image, info['input_size'])
        prediction = models[fruit].predict(input_data)
        idx = int(np.argmax(prediction))
        confidence = float(prediction[0][idx])
        disease = info['categories'][idx]

        return jsonify({
            'disease': disease,
            'confidence': confidence
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)