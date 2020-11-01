import cv2
import PyDIP as dip
for i in range(5):
	img = cv2.imread("crop"+str(i)+".jpg",0)
	cv2.imshow("Orig", img)
	lines = dip.PathOpening(img, length=270, mode={'constrained'})
	lines.Show()
	cv2.waitKey()
