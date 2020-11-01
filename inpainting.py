import cv2
import numpy as np



def remove_noise(img):

	img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	img = cv2.dilate(img,cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)),iterations = 1)
	copy = img.copy()
	copy = cv2.cvtColor(copy,cv2.COLOR_GRAY2RGB)
	refCnts, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	mask = np.zeros(img.shape[:2], dtype=img.dtype)
	noise = []
	
	for c in refCnts:
		area = cv2.contourArea(c)
		if area < 80:
			#print(area)
			noise.append(c)
			cv2.drawContours(mask, [c], 0, (255), -1)
	mask= cv2.bitwise_not(mask)
	result = cv2.bitwise_and(img,img, mask= mask)
	return result

for i in range(47):
	img = cv2.imread("localized/t"+str(i+1)+".jpg",0)
	mask = cv2.imread("masks/mask"+str(i+1)+".png",0)
	dst = cv2.inpaint(img, mask, inpaintRadius=2, flags=cv2.INPAINT_NS)
	cv2.imwrite("inpaint/res"+str(i+1)+"a.png", remove_noise(dst))

	dst1 = cv2.inpaint(img, mask, inpaintRadius=8, flags=cv2.INPAINT_NS)
	cv2.imwrite("inpaint/res"+str(i+1)+"b.png",remove_noise(dst1))

	dst2 = cv2.inpaint(img, mask, inpaintRadius=2, flags=cv2.INPAINT_TELEA)
	cv2.imwrite("inpaint/res"+str(i+1)+"c.png",remove_noise(dst2))

	dst3 = cv2.inpaint(img, mask, inpaintRadius=8, flags=cv2.INPAINT_TELEA)
	cv2.imwrite("inpaint/res"+str(i+1)+"d.png",remove_noise(dst3))
