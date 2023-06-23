import cv2
import numpy as np

img = cv2.imread('ca_test.png')

test = cv2.GaussianBlur(img, (11, 11), 0)

cv2.imwrite("output.png", test)