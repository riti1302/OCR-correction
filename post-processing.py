import cv2 as cv
import numpy as np


def false_pos(img):
	img = cv.blur(img,(5,5))
	cv.imshow("this is it",img)
	cv.waitKey()
	h,w = img.shape
	for i in range(w-1):
		count = 0
		for j in range(h-1):
			if img[j][i] <=127 and img[j+1][i] >=127:
				count+=1
			if count>=2:
				return False
	return True

for i in range(5):
	img = cv.imread("crop"+str(i)+".jpg",0)
	orig = img.copy()
	# Structuring element
	kernel = cv.getStructuringElement(cv.MORPH_RECT,(8,8))
	opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)

	dilatation_size = 8
	dilatation_type = cv.MORPH_RECT
	element = cv.getStructuringElement(dilatation_type, (2*dilatation_size + 1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
	dilated = cv.dilate(opening, element)

	contours = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
	for cnt in contours:
		(x,y,w,h) = cv.boundingRect(cnt)
		startx = max(x-12,0)
		starty = max(y-6,0)
		endx = min(x+w+12, orig.shape[1])
		endy = min(y+h+6, orig.shape[0])
		if not false_pos(orig[starty:endy, startx:endx]):
			orig = cv.rectangle(orig, (startx,starty), (endx,endy), (255, 0, 0) , 1)
	cv.imwrite('Word_Localised'+str(i)+".png", orig)
