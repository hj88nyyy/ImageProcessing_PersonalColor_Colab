import numpy as np

def extract_feature_area(image, start_x, start_y, width, height):
    section = image[start_y:start_y + height, start_x:start_x + width]
    avg_color_per_row = np.average(section, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return avg_color
