
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('Word_Local134.png',0)
kernel = np.ones((3,3),np.uint8)
erode = cv2.erode(img,kernel,iterations = 1)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,5))
blackhat = cv2.morphologyEx(erode, cv2.MORPH_TOPHAT, kernel)



cv2.imshow('blackhat', blackhat)
cv2.imshow('erode', erode)
cv2.waitKey(0)
'''

img = cv2.imread('Word_Local134.png',0)
size = np.size(img)
skel = np.zeros(img.shape,np.uint8)

ret,img = cv2.threshold(img,127,255,0)
element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
done = False

while( not done):
    eroded = cv2.erode(img,element)
    temp = cv2.dilate(eroded,element)
    temp = cv2.subtract(img,temp)
    skel = cv2.bitwise_or(skel,temp)
    img = eroded.copy()

    zeros = size - cv2.countNonZero(img)
    if zeros==size:
        done = True

kernel = np.ones((1,1),np.uint8)
tophat = cv2.morphologyEx(skel, cv2.MORPH_TOPHAT, kernel)

f, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(10, 3))

ax0.imshow(img, cmap='gray')
ax0.set_title('Input')

ax1.imshow(skel, cmap='gray')
ax1.set_title('Skeletonize')

ax2.imshow(tophat, cmap='gray')
ax2.set_title('Tophat')

plt.savefig('/tmp/char_out.png')
plt.show()
'''
