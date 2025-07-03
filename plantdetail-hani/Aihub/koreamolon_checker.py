import koreamelon_CNN as kmelon
import sys, os
from PIL import Image
import cv2
import numpy as np
from datetime import datetime

# 명령줄에서 파일이름 지정
if len(sys.argv) <= 1:
    print("소스파일.py (<파일 이름>)")
    quit()
image_size = 224
categories = ["노균병", "노균병유사", "정상", "흰가루병", "흰가루병유사"]

# 입력 이미지를 Numpy로 변환
X = []
files = []
for fname in sys.argv[1:]:
    img = cv2.imread(fname)
    if img is None:
        continue
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h, w, _ = img.shape
    if h > w:
        new_h, new_w = image_size, int(w * (image_size / h))
    else :
        new_h, new_w = int(h * (image_size / w)), image_size
    img = cv2.resize(img, (new_w, new_h))

    # 정사각형으로 패딩 추가
    pad_h = (image_size - new_h) // 2
    pad_w = (image_size - new_w) // 2
    img = cv2.copyMakeBorder(img, pad_h, image_size - new_h - pad_h,
                             pad_w, image_size - new_w - pad_w,
                             cv2.BORDER_CONSTANT, value = [0,0,0])
    X.append(img)
    files.append(fname)

X = np.array(X)
# CNN 모델 구축
model = kmelon.build_model(X.shape[1:])
model.load_weights('./koreanmelon/koreanmelon_model.weights.h5')

# 데이터 예측
html = ""
pre = model.predict(X)
for i, p in enumerate(pre):
   y = p.argmax()
   print("+입력:", files[i])
   print("|음식이름:", categories[y])
   html += """
       <h3>입력:{0}</h3>
       <div>
         <p><img src="..\{1}" width=300></p>
         <p>음식이름:{2}</p>
       </div>
   """.format(os.path.basename(files[i]),
       files[i],
       categories[y])

# 리포트를 HTML로 저장
html = "<html><body style='text-align:center;'>" + \
   "<style> p { margin:0; padding:0; } </style>" + \
   html + "</body></html>"


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
with open("./kfood/kfood_result_"+timestamp+".html", "w") as f:
   f.write(html)


print("Task Finished..!!")