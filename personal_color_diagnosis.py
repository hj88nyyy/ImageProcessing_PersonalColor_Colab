import numpy as np

def bgr_to_hsv(bgr_color):
    """
    수동으로 BGR 색상을 HSV로 변환.
    """
    b, g, r = bgr_color / 255.0
    c_max = max(r, g, b)
    c_min = min(r, g, b)
    delta = c_max - c_min

    # Hue 계산
    if delta == 0:
        hue = 0
    elif c_max == r:
        hue = ((g - b) / delta) % 6
    elif c_max == g:
        hue = ((b - r) / delta) + 2
    elif c_max == b:
        hue = ((r - g) / delta) + 4
    hue *= 60

    # Lightness 계산
    lightness = (c_max + c_min) / 2 * 255

    # Saturation 계산
    saturation = 0 if lightness == 0 else (delta / (1 - abs(2 * lightness / 255 - 1))) * 255

    return np.array([hue, saturation, lightness], dtype=np.uint8)

def determine_clear_dull(image_section):
    """
    청·탁 속성 판단.
    """
    gray_image = np.mean(image_section, axis=2)
    gray_mean = np.mean(gray_image)
    return 'C' if gray_mean > 128 else 'D'

def diagnose_color_properties(hue, lightness, clear_dull, saturation):
    """
    4가지 속성으로 진단하고 8자리 코드를 생성.
    """
    hue_category = 'Warm' if hue >= 0 and hue <= 60 else 'Cool'
    lightness_level = 'H' if lightness >= 215 else ('M' if 145 <= lightness < 215 else 'L')
    clear_dull_level = 'C' if clear_dull == 'C' else 'D'
    saturation_level = 'H' if saturation >= 5 else ('M' if 2.65 <= saturation < 5 else 'L')
    type_code = f"{hue_category}/{lightness_level}/{clear_dull_level}/{saturation_level}"
    return type_code

def determine_seasonal_type(type_code):
    """
    20유형 매트릭스에서 type_code에 따라 최종 유형을 반환.
    """
    type_map = {
        'Warm/H/C/H': 'Bright Spring',
        'Warm/H/D/M': 'Light Spring',
        'Warm/M/C/H': 'Warm Spring',
        'Warm/M/D/L': 'Soft Spring',
        'Warm/L/C/H': 'Vivid Spring',
        'Cool/H/C/H': 'Bright Summer',
        'Cool/H/D/L': 'Light Summer',
        'Cool/M/C/H': 'Cool Summer',
        'Cool/M/D/M': 'Soft Summer',
        'Cool/L/C/H': 'Muted Summer',
        'Warm/H/C/M': 'Warm Autumn',
        'Warm/H/D/L': 'Light Autumn',
        'Warm/M/C/H': 'Deep Autumn',
        'Warm/M/D/M': 'Soft Autumn',
        'Warm/L/C/H': 'Dark Autumn',
        'Cool/H/C/H': 'Bright Winter',
        'Cool/H/D/L': 'Light Winter',
        'Cool/M/C/H': 'Cool Winter',
        'Cool/M/D/M': 'Soft Winter',
        'Cool/L/C/H': 'Deep Winter',
    }
    return type_map.get(type_code, 'Intermediate')
