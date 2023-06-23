import cv2
import numpy as np

ca_img = cv2.imread('unblurred/ca_test.png')
pa_img = cv2.imread('unblurred/pa_test.jpg')


def blur(img, state):
    # saves what a single blur run looks like
    single_run = cv2.GaussianBlur(img, (25, 25), 0)
    cv2.imwrite(f'{state}_1run.png', single_run)
    
    # saves what image looks like after blurring n times
    img_to_blur = cv2.imread(f'{state}_1run.png')
    for i in range(25): # 25 produces good results
        blurred = cv2.GaussianBlur(img_to_blur, (25, 25), 0)
        cv2.imwrite(f'{state}_output.png', blurred)
        img_to_blur = cv2.imread(f'{state}_output.png')


blur(ca_img, 'ca')
blur(pa_img, 'pa')