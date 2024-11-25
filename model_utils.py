import subprocess
import os
import cv2
import numpy as np

def get_feature_coordinates(model, image):
    """
    모델을 통해 이미지에서 머리, 피부, 눈 좌표를 반환.
    추후 모델을 추가할 때 이 함수를 구현합니다.
    """
    # 더미 좌표 반환 (모델이 구현되면 이 부분 수정)
    hair_coords = (10, 10, 50, 50)
    skin_coords = (60, 60, 50, 50)
    eye_coords = (120, 120, 30, 30)
    return hair_coords, skin_coords, eye_coords


def process_image_with_test_py(image_path):
    """
    입력된 이미지 디렉토리를 test.py를 통해 처리합니다.
    
    Parameters:
        img_path (str): 입력 이미지 경로.
        save_path (str): 처리된 결과를 저장할 경로.
    """
    try:
        # test.py 실행 명령어
        command = f"python /content/personalcolor_model/face-parsing.PyTorch/test.py --image_path \"{image_path}\""
        
        # subprocess를 사용해 외부 명령 실행
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        # 출력 확인
        print("test.py 실행 결과:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("test.py 실행 중 오류 발생!")
        print(e.stderr)    


# 함수: 특정 레이블의 평균 RGB 계산
def calculate_average_rgb(label, mask, image):
    # 특정 레이블의 픽셀만 선택
    region_mask = (mask == label)
    region_pixels = image[region_mask]
    if len(region_pixels) > 0:
        # 평균 RGB 계산
        return region_pixels.mean(axis=0)
    else:
        return np.array([0, 0, 0])  # 해당 레이블이 없는 경우 (검정색 반환)
        