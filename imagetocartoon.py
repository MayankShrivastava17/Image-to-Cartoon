import cv2
import numpy as np

from google.colab.patches import cv2_imshow
from google.colab import files

def read_file(filename):
  img = cv2.imread(filename)
  cv2_imshow(img)
  return img

uploaded = files.upload()
filename = next(iter(uploaded))
img = read_file(filename)

def edge_mask(img, line_size, blur_value):
  grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  grey_blur = cv2.medianBlur(grey, blur_value)
  edges = cv2.adaptiveThreshold(grey_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
  return edges

line_size = 7
blur_value = 7

edges = edge_mask(img, line_size, blur_value)
cv2_imshow(edges)

def color_quantization(img, k):
  data = np.float32(img).reshape((-1, 3))
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
  ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
  center = np.uint8(center)
  result = center[label.flatten()]
  result = result.reshape(img.shape)
  return result

total_color = 9
img = color_quantization(img, total_color)

cv2_imshow(img)

blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200, sigmaSpace=200)
cv2_imshow(blurred)

cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

cv2_imshow(cartoon)
