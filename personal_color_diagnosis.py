import numpy as np

def bgr_to_hsv(bgr_color):
    b, g, r = bgr_color / 255.0
    c_max = max(r, g, b)
    c_min = min(r, g, b)
    delta = c_max - c_min

    if delta == 0:
        hue = 0
    elif c_max == r:
        hue = ((g - b) / delta) % 6
    elif c_max == g:
        hue = ((b - r) / delta) + 2
    elif c_max == b:
        hue = ((r - g) / delta) + 4
    hue *= 60

    lightness = (c_max + c_min) / 2 * 255
    saturation = 0 if lightness == 0 else (delta / (1 - abs(2 * lightness / 255 - 1))) * 255

    return np.array([hue, saturation, lightness], dtype=np.uint8)

def determine_clear_dull(image_section):
    gray_image = np.mean(image_section, axis=2)
    gray_mean = np.mean(gray_image)
    return 'C' if gray_mean > 128 else 'D'
