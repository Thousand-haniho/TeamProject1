from PIL import Image, ImageEnhance, ImageOps
import os
import glob
import numpy as np
from collections import defaultdict
import random
from sklearn.model_selection import train_test_split

root_dir = "./download/참외데이터/Training/01.원천데이터"

categories = ["normal", "nogunbyeong", "hyngalubyeong"]
nb_classes = len(categories)

image_w, image_h = 64, 64

X = []
Y = []

def add_sample(cat_idx, filepath, is_train):
    global X, Y
    img = Image.open(filepath).convert("RGB").resize((image_w, image_h))
    data = np.asarray(img)
    X.append(data)

    # One-hot encoding
    label = [0] * nb_classes
    label[cat_idx] = 1
    Y.append(label)

    if not is_train:
        return

    for _ in range(2):
        aug_img = img.copy()

        angle = random.uniform(-30, 30)
        aug_img = aug_img.rotate(angle)

        if random.random() < 0.5:
            aug_img = ImageOps.mirror(aug_img)

        aug_img = ImageEnhance.Brightness(aug_img).enhance(random.uniform(0.8, 1.2))
        aug_img = ImageEnhance.Color(aug_img).enhance(random.uniform(0.8, 1.2))
        aug_img = ImageEnhance.Contrast(aug_img).enhance(random.uniform(0.9, 1.3))

        aug_img = aug_img.resize((image_w, image_h))
        X.append(np.asarray(aug_img))
        Y.append(label)


allfiles = []
print("이미지 수집 시작...")
for idx, cat in enumerate(categories):
    image_dir = os.path.join(root_dir, cat)
    files = glob.glob(os.path.join(image_dir, "*.jpg"))
    if len(files) == 0:
        print(f"[WARNING] {image_dir}에 이미지가 없습니다!")
    else:
        print(f"[INFO] {cat} 클래스에 {len(files)}개 이미지 발견")
    for f in files:
        allfiles.append((idx, f))

print(f"총 수집된 이미지 개수: {len(allfiles)}")

files_by_class = defaultdict(list)
for cls_idx, filepath in allfiles:
    files_by_class[cls_idx].append(filepath)

if len(files_by_class) == 0:
    raise Exception("모든 클래스에 이미지가 없습니다. 경로와 폴더명을 확인하세요.")

for cls_idx in range(nb_classes):
    print(f"클래스 {categories[cls_idx]} 이미지 수: {len(files_by_class[cls_idx])}")

max_count = max(len(filelist) for filelist in files_by_class.values())
print(f"최대 클래스 이미지 수: {max_count}")

balanced_files = []
for cls_idx, filelist in files_by_class.items():
    current_list = filelist.copy()
    if len(current_list) < max_count:
        needed = max_count - len(current_list)
        sampled = random.choices(filelist, k=needed)
        current_list.extend(sampled)
    balanced_files.extend([(cls_idx, f) for f in current_list])

print(f"균형 맞춘 후 총 샘플 수: {len(balanced_files)}")

train_files, test_files = train_test_split(
    balanced_files, test_size=0.3,
    stratify=[x[0] for x in balanced_files],
    random_state=42)

print(f"훈련 샘플 수: {len(train_files)}")
print(f"테스트 샘플 수: {len(test_files)}")

X, Y = [], []
for cat_idx, fpath in train_files:
    add_sample(cat_idx, fpath, is_train=True)
x_train = np.array(X, dtype=np.uint8)
y_train = np.array(Y, dtype=np.float32)
print(f"증강 포함 훈련 데이터셋 크기: {x_train.shape}, {y_train.shape}")

X, Y = [], []
for cat_idx, fpath in test_files:
    add_sample(cat_idx, fpath, is_train=False)
x_test = np.array(X, dtype=np.uint8)
y_test = np.array(Y, dtype=np.float32)
print(f"테스트 데이터셋 크기: {x_test.shape}, {y_test.shape}")

os.makedirs("./saveFiles", exist_ok=True)
np.savez("./saveFiles/lemon_aug_balanced.npz",
         x_train=x_train, y_train=y_train,
         x_test=x_test, y_test=y_test)

print("데이터 저장 완료!")