from flask import Flask, request, render_template, redirect, url_for
from PIL import Image

from flask_ngrok import run_with_ngrok  # ngrok 사용
from flask import Flask
from pyngrok import ngrok


import numpy as np
import os
import cv2
from werkzeug.utils import secure_filename
from model_utils import process_image_with_test_py, calculate_average_rgb
from personal_color_diagnosis import bgr_to_hsv, determine_clear_dull, diagnose_color_properties, determine_seasonal_type

app = Flask(__name__)

# ngrok 터널 열기
ngrok.set_auth_token("2pFgWcURJwDrBRwIF8WwIIOCtKd_2Cq8qGY7Wm4TfNcB3ghrG")
public_url = ngrok.connect(5000)
print(" * ngrok 터널 URL:", public_url)

# 업로드 폴더 설정
UPLOAD_FOLDER = '/content/personalcolor_model/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_image(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        return np.array(image)
    except FileNotFoundError:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', result="No file part")

        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', result="No selected file")

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return redirect(url_for('result', filename=filename))

    return render_template('index.html')

@app.route('/result/<filename>', methods=['GET'])
def result(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image = load_image(file_path)

    if image is None:
        return render_template('result.html', result="Error loading image")

    
    process_image_with_test_py(file_path)

    filename_trim = os.path.splitext(filename)[0]  # 확장자 제거
    segmentation_mask = cv2.imread(f"/content/personalcolor_model/face-parsing.PyTorch/res/test_res/{filename_trim}.png", cv2.IMREAD_GRAYSCALE)
    original_image = cv2.imread(f"/content/personalcolor_model/face-parsing.PyTorch/res/test_res/{filename_trim}.jpg")

    # 레이블 정의
    labels = {
        "skin": 1,
        "hair": 10,
        "left_eye": 4,
        "right_eye": 5
    }

    # 결과 저장
    average_rgbs = {}

    for region_name, label in labels.items():
        average_rgb = calculate_average_rgb(label, segmentation_mask, original_image)
        average_rgbs[region_name] = average_rgb

    skin_color = average_rgbs["skin"]
    hair_color = average_rgbs["hair"]

    if np.all(average_rgbs["left_eye"] == 0):
        eye_color = average_rgbs["right_eye"]
    elif np.all(average_rgbs["right_eye"] == 0):
        eye_color = average_rgbs["left_eye"]
    else:
        eye_color = (average_rgbs["right_eye"] + average_rgbs["left_eye"]) / 2

    
        
    """


    # 모델을 통해 좌표를 가져오는 부분
    model = None  # 모델이 추가되면 이 부분 수정
    hair_coords, skin_coords, eye_coords = get_feature_coordinates(model, image)

    # 각 영역의 평균 색상 추출 및 분석
    hair_color = extract_feature_area(image, *hair_coords)
    skin_color = extract_feature_area(image, *skin_coords)
    eye_color = extract_feature_area(image, *eye_coords)

    """

    # HSV 변환 및 분석
    hair_hsv = bgr_to_hsv(hair_color).astype(float)
    skin_hsv = bgr_to_hsv(skin_color).astype(float)
    eye_hsv = bgr_to_hsv(eye_color).astype(float)

    # 청·탁 속성 추가
    hair_clear_dull = determine_clear_dull(hair_color)
    skin_clear_dull = determine_clear_dull(skin_color)
    eye_clear_dull = determine_clear_dull(eye_color)

    # 종합 평균 퍼스널 컬러 타입 계산
    avg_hue = (hair_hsv[0] + skin_hsv[0] + eye_hsv[0]) / 3
    avg_lightness = (hair_hsv[2] + skin_hsv[2] + eye_hsv[2]) / 3
    avg_saturation = (hair_hsv[1] + skin_hsv[1] + eye_hsv[1]) / 3
    avg_clear_dull = 'C' if ((255 if hair_clear_dull == 'C' else 0) +
                             (255 if skin_clear_dull == 'C' else 0) +
                             (255 if eye_clear_dull == 'C' else 0)) > 384 else 'D'

    type_code = diagnose_color_properties(avg_hue, avg_lightness, avg_clear_dull, avg_saturation)
    overall_type = determine_seasonal_type(type_code)


    # 결과 반환
    results = {
        "Hair Type": determine_seasonal_type(diagnose_color_properties(hair_hsv[0], hair_hsv[2], hair_clear_dull, hair_hsv[1])),
        "Skin Type": determine_seasonal_type(diagnose_color_properties(skin_hsv[0], skin_hsv[2], skin_clear_dull, skin_hsv[1])),
        "Eye Type": determine_seasonal_type(diagnose_color_properties(eye_hsv[0], eye_hsv[2], eye_clear_dull, eye_hsv[1])),
        "Overall Type": overall_type
    }

    return render_template('result.html', filename=filename, results=results)

if __name__ == '__main__':
    app.run()
