import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('lena.jpg')

median = cv2.medianBlur(img,1)

plt.subplot(121),plt.imshow(img),plt.title('ảnh gốc')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(median),plt.title('ảnh lọc trung vị')
plt.xticks([]), plt.yticks([])
plt.show()
