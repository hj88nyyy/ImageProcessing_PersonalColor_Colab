import subprocess
import os
import cv2
import numpy as np

# 입력 받은 이미지 test.py를 통해 처리리
def process_image_with_test_py(image_path):
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


# 특정 레이블의 평균 RGB 계산
def calculate_average_rgb(label, mask, image):
    # 특정 레이블의 픽셀만 선택
    region_mask = (mask == label)
    region_pixels = image[region_mask]
    if len(region_pixels) > 0:
        # 평균 RGB 계산
        return region_pixels.mean(axis=0)
    else:
        return np.array([0, 0, 0])  # 해당 레이블이 없는 경우 (검정색 반환)
        