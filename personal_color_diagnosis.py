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

def determine_clear_dull(rgb_avg):
    """
    청·탁 속성 판단.
    """
    gray_mean = np.mean(rgb_avg)
    return 'C' if gray_mean > 128 else 'D'

def diagnose_color_properties(hue, lightness, clear_dull, saturation):
    """
    4가지 속성으로 진단하고 8자리 코드를 생성.
    """
    hue_category = 'Warm' if hue >= 0 and hue <= 60 else 'Cool'
    lightness_level = 'H' if lightness >= 215 else ('M' if 145 <= lightness < 215 else 'L')
    clear_dull_level = 'C' if clear_dull == 'C' else 'D'
    saturation_level = 'H' if saturation >= 170 else ('M' if 85 <= saturation < 170 else 'L')
    type_code = f"{hue_category}/{lightness_level}/{clear_dull_level}/{saturation_level}"
    return type_code

def determine_seasonal_type(type_code):
    """
    20유형 매트릭스에서 type_code에 따라 최종 유형을 반환.
    """
    type_map = {
        'Warm/H/C/L': 'Light Spring',
        'Warm/M/C/L': 'Soft Spring',
        'Warm/H/C/H': 'Bright Spring',       
        'Warm/M/C/H': 'Vivid Spring',
        'Warm/M/C/M': 'Warm Spring',
        'Warm/H/C/M': 'Warm Spring',
        'Cool/H/D/L': 'Light Summer',
        'Cool/H/D/M': 'Soft Summer',
        'Cool/M/D/M': 'Soft Summer',
        'Cool/M/D/L': 'Soft Summer',
        'Cool/H/C/H': 'Bright Summer',       
        'Cool/L/D/M': 'Muted Summer',
        'Cool/L/D/L': 'Muted Summer',
        'Cool/H/D/H': 'Cool Summer',
        'Cool/M/D/H': 'Cool Summer',
        'Cool/L/D/H': 'Cool Summer',
        'Warm/H/D/H': 'Soft Autumn',
        'Warm/H/D/M': 'Soft Autumn',
        'Warm/H/D/L': 'Soft Autumn',     
        'Warm/M/D/L': 'Muted Autumn',
        'Warm/L/C/H': 'Deep Autumn',
        'Warm/L/C/M': 'Deep Autumn',
        'Warm/L/C/L': 'Deep Autumn',
        'Warm/L/D/L': 'Dark Autumn',
        'Warm/L/D/M': 'Dark Autumn',
        'Warm/L/D/H': 'Dark Autumn',
        'Warm/M/D/M': 'Warm Autumn',
        'Warm/M/D/H': 'Warm Autumn',
        'Cool/H/C/L': 'Light Winter',
        'Cool/H/C/M': 'Clear Winter',
        'Cool/M/C/H': 'Vivid Winter',
        'Cool/L/C/H': 'Vivid Winter',
        'Cool/L/C/M': 'Deep Winter',
        'Cool/L/C/L': 'Deep Winter',
        'Cool/M/C/M': 'Cool Winter',
        'Cool/M/C/L': 'Cool Winter'
    }
    return type_map.get(type_code, 'Intermediate')
