import os
import json

# 이미지와 JSON이 저장된 폴더 경로 설정
image_folder = './download/참외데이터/Training/01.원천데이터/normal'  # 이미지가 저장된 폴더
json_folder = './download/참외데이터/Training/02.라벨링데이터/TL_정상'  # JSON이 저장된 폴더

# 모든 JSON 파일 처리
for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        json_path = os.path.join(json_folder, filename)

        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"[오류] JSON 파싱 실패: {filename}, {e}")
                continue

        # 'image' → 'date_section'이 '야간'인 경우 삭제
        if 'image' in data and data['image'].get('day_section') == '야간':
            # 이미지 파일 이름 추정: JSON 파일명과 동일한 이름 (확장자만 다르게)
            base_name = os.path.splitext(filename)[0]
            possible_extensions = ['.jpg', '.png', '.jpeg']

            # 이미지 삭제 시도
            for ext in possible_extensions:
                image_path = os.path.join(image_folder, base_name + ext)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f"[삭제됨] 이미지: {image_path}")
                    break  # 하나만 삭제하면 됨

            # JSON 파일도 삭제
            os.remove(json_path)
            print(f"[삭제됨] JSON: {json_path}")
