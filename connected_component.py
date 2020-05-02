import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
import statistics

img = cv2.imread('25.jpg', 0)
#img = cv2.GaussianBlur(img,(5,5),0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
img = cv2.bitwise_not(img)
retval, labels, stats, _ = cv2.connectedComponentsWithStats(img)
pixels = []
sum = 0
for i in range(1, len(stats)):
	sum += stats[i,cv2.CC_STAT_AREA]
	if stats[i,cv2.CC_STAT_AREA] > 100 and stats[i,cv2.CC_STAT_AREA] < 1000:
		pixels.append(stats[i,cv2.CC_STAT_AREA])

mode = statistics.mode(pixels)
print(mode)
area = []
annotation = []
for i in range(1, len(stats)):
	x,y,h,w,a = stats[i,cv2.CC_STAT_LEFT], stats[i,cv2.CC_STAT_TOP],stats[i,cv2.CC_STAT_HEIGHT],stats[i,cv2.CC_STAT_WIDTH],stats[i,cv2.CC_STAT_AREA]

	if a > 5*mode:
		rec = cv2.rectangle(img, (x,y),(x+w,y+h),(255,0,0),2)
		annotation.append(img[y:y+h, x:x+w])
	else:
		rec = cv2.rectangle(img, (x,y),(x+w,y+h),(0,0,255),-1)
	area.append(a)
for i in range(len(annotation)):
	cv2.imwrite("crop{}.jpg".format(i),annotation[i])

cv2.imwrite("result.jpg", img)

#print(pixels)
max = max(pixels)
min = min(pixels)
bin = range(min, max, 10)
print(bin)
a = np.array(pixels)
plt.hist(a,bins = bin)
plt.show()

##################################################
"""
ts = time.time()
num = labels.max()
pixels = []

N = 50
for i in range(1, num+1):
    pts =  np.where(labels == i)
    if len(pts[0]) < N:
        labels[pts] = 0
    if len(pts[0]) > N and len(pts[0]) < 10000:
        pixels.append(len(pts[0]))
#pixels.pop(0)
print(pixels)
max = max(pixels)
min = min(pixels)
bin = range(min, max, 20)
print(bin)
a = np.array(pixels)
plt.hist(a,bins = bin)
plt.show()
print("Time passed: {:.3f} ms".format(1000*(time.time()-ts)))
# Time passed: 4.607 ms

##################################################

# Map component labels to hue val
label_hue = np.uint8(179*labels/np.max(labels))
blank_ch = 255*np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

# cvt to BGR for display
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

# set bg label to black
labeled_img[label_hue==0] = 0

#cv2.imshow('labeled.png', labeled_img)
cv2.imwrite("labeled.png", labeled_img)
#cv2.waitKey(0)
"""
