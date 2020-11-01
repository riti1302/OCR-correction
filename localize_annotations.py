import cv2
import numpy as np
from matplotlib import pyplot as plt
import statistics
import imutils
import os


def cvt_BGR2RGB(img):
  return cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

def unsharp_mask(image, kernel_size=(5, 5), sigma=25.0, amount=1.0, threshold=1):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened


def connected_component(img, outPath):
	retval, labels, stats, _ = cv2.connectedComponentsWithStats(img)
	areas = []
	for i in range(1, len(stats)):
		area = int(stats[i,cv2.CC_STAT_HEIGHT] * stats[i,cv2.CC_STAT_WIDTH])
		if  area > 100 and area < 1000:
			areas.append(area)

	try:
		mode = statistics.mode(areas)
		print(mode)
	except Exception as e:
		print(e)
		return img, areas

	annotation = []
	for i in range(1, len(stats)):
		x,y,h,w = stats[i,cv2.CC_STAT_LEFT], stats[i,cv2.CC_STAT_TOP],stats[i,cv2.CC_STAT_HEIGHT],stats[i,cv2.CC_STAT_WIDTH]
		a = int(h * w)
		if a > 10*mode:
			#rec = cv2.rectangle(img, (x,y),(x+w,y+h),(255,0,0),2)
			annotation.append(img[y:y+h, x:x+w])
		else:
			cv2.rectangle(img, (x,y),(x+w,y+h),(0,0,0),-1)   # erase components that are not annotation
	for i in range(len(annotation)):
		cv2.imwrite(outPath+'/annotation_{}.jpg'.format(i),annotation[i])
	return img, areas

def get_contours(img):
	kernel = np.ones((3,3),np.uint8)
	closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	cnts = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	length = []
	new_img = cvt_BGR2RGB(img)
	for c in cnts:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.035* peri,True)
		#length.append(len(approx))
		if len(approx) >= 7 and len(approx) <= 9:
			cv2.drawContours(new_img, c, -1, (0, 255, 0), 3)
	plt.figure()
	plt.imshow(new_img)
	plt.show()
	#print(length)
	#show_hist(length)
	return img

def show_hist(values):
	Max = max(values)
	Min = min(values)
	bin = range(Min, Max, 10)
	#bin = range(Min, Max, 2)
	print(bin)
	a = np.array(values)
	plt.hist(a,bins = bin)
	plt.show()


# Change the input path
if __name__ == '__main__':
    inPath = 'Input/'
    outPath = 'Output/'
    if not os.path.exists(outPath):
        os.mkdir(outPath)

    for file in os.listdir(inPath):
        imgPath = os.path.join(inPath, file)
        img = cv2.imread(imgPath, 0)
        binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)[1]

        basename = os.path.splitext(file)[0]
        imgDir = os.path.join(outPath, basename)
        if not os.path.exists(imgDir):
        	os.mkdir(imgDir)

        result, pixels = connected_component(binary, imgDir)
        #result = get_contours(result)
        cv2.imwrite(imgDir+'/original.jpg', img)
        cv2.imwrite(imgDir+'/result.jpg', result)

        # to show histogram, set the value of show to True
        show = False
        if show:
        	show_hist(pixels)
