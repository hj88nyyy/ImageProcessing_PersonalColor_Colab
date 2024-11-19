from PIL import Image
import numpy as np
from extract_features import extract_feature_area
from model_utils import get_feature_coordinates
from personal_color_diagnosis import bgr_to_hsv, determine_clear_dull

# 이미지 로드
def load_image(image_path):
    try:
        image = Image.open(image_path).convert('RGB')
        return np.array(image)
    except FileNotFoundError:
        print("Image not found.")
        return None

def main(image_path):
    image = load_image(image_path)
    if image is None:
        return

    # 모델로 좌표 가져오기
    model = None  # 모델 로드 코드 추가 필요
    hair_coords, skin_coords, eye_coords = get_feature_coordinates(model, image)

    # 각 영역의 평균 색상 추출
    hair_color = extract_feature_area(image, *hair_coords)
    skin_color = extract_feature_area(image, *skin_coords)
    eye_color = extract_feature_area(image, *eye_coords)

    # HSV 변환 및 분석
    hair_hsv = bgr_to_hsv(hair_color)
    skin_hsv = bgr_to_hsv(skin_color)
    eye_hsv = bgr_to_hsv(eye_color)

    hair_clear_dull = determine_clear_dull(image[hair_coords[1]:hair_coords[1] + hair_coords[3], hair_coords[0]:hair_coords[0] + hair_coords[2]])
    skin_clear_dull = determine_clear_dull(image[skin_coords[1]:skin_coords[1] + skin_coords[3], skin_coords[0]:skin_coords[0] + skin_coords[2]])
    eye_clear_dull = determine_clear_dull(image[eye_coords[1]:eye_coords[1] + eye_coords[3], eye_coords[0]:eye_coords[0] + eye_coords[2]])

    print("Hair HSV & Clear/Dull:", hair_hsv, hair_clear_dull)
    print("Skin HSV & Clear/Dull:", skin_hsv, skin_clear_dull)
    print("Eye HSV & Clear/Dull:", eye_hsv, eye_clear_dull)

if __name__ == "__main__":
    image_path = 'C:/Users/KimTY/personalcolor_model/images/iu.jpg'
    main(image_path)
