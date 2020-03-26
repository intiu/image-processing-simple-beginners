import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('lena.jpg')

blur = cv2.blur(img,(5,5))

plt.subplot(121),plt.imshow(img),plt.title('ảnh gốc')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(blur),plt.title('ảnh lọc trung bình')
plt.xticks([]), plt.yticks([])
plt.show()
