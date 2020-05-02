from PIL import Image
import pytesseract
import cv2
import os
import argparse
import enchant
import re
import language_check
from main import complete_sentence
tool = language_check.LanguageTool('en-US')

args={}
args["image_dir"] = "image_dir"
args["preprocess"] = "thresh"

d = enchant.Dict("en_UK")

output_dir = 'output/'
for file in os.listdir(args["image_dir"]):
	image = cv2.imread(args["image_dir"]+'/'+file)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# check to see if we should apply thresholding to preprocess the
	# image
	if args["preprocess"] == "thresh":
		gray = cv2.threshold(gray, 0, 255,
			cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	# make a check to see if median blurring should be done to remove
	# noise
	elif args["preprocess"] == "blur":
		gray = cv2.medianBlur(gray, 3)

	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = output_dir+"{}.png".format(file.split('.')[0])
	cv2.imwrite(filename, gray)

	text = pytesseract.image_to_string(Image.open(filename))
	#print(text)
	#print(type(text))
	os.remove(filename)
	lines = text.split('\n')
	#print(lines)
	words = []

	text = re.sub("[^\w]", " ",  text).split()
	for word in  text:
		if d.check(word) or word.isdigit():
			pass
		else:
			words.append(word)
	#print(words)
	with open(output_dir + '{}.txt'.format(file.split('.')[0]), 'w+') as outfile:
		for line in lines:
			for word in words:
				if word in line:
					#xprint(word)
					line = line.replace(word, " ___ ")
			outfile.write(line.encode('utf-8')+'\n')
	with open(output_dir + '{} imputation.txt'.format(file.split('.')[0]), 'w+') as outfile:
		for line in lines:
			for word in words:
				if word in line:
					#xprint(word)
					#print(d.suggest(word))
					try:
						#s=d.suggest(word)[0]
						line = line.replace(word, lower(s))
					except:
						line = line.replace(word,word)
			outfile.write(line.encode('utf-8')+'\n')
	with open(output_dir + '{} result.txt'.format(file.split('.')[0]), "w") as outfile:
		with open(output_dir + '{} imputation.txt'.format(file.split('.')[0])) as infile:
			for text in infile:
				try:
					matches = tool.check(text)
					corrected_text = language_check.correct(text, matches)
					outfile.write(corrected_text)
				except Exception as e:
					#print(e)
					pass

"""
	text = re.split(r'\s', text)


	with open(output_dir + '{}.txt'.format(file.split('.')[0]), 'w+') as outfile:
		#print(text)
		for t in text:
		  a = re.sub("[^\w]", " ",  t).split()
		  if len(a):

		    if d.check(a[0]):
		        outfile.write(" "+t)
		    else:
		        outfile.write(" ---")


"""
