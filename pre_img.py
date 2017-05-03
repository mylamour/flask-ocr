#!/usr/bin/env python 
#coding:utf-8
import pytesseract
import urllib
import cv2
#from StringIO import StringIO
import numpy as np
from PIL import Image

def process_image(url=None,path=None):
#	image = _get_image(url)
	if url != None:
		image = url_to_image(url)
	elif path != None:
		image = cv2.imread(path)
	else:
		return "Wrong Wrong Wrong, What are you doing ??? "

	gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
	ret2,th2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	dst = cv2.fastNlMeansDenoising(th2,10,10,7)
	cv2.imwrite('./uploads/tmp.jpg',dst)
	cao = Image.open('./uploads/tmp.jpg')
	print ("Recongizeing...")
	rec_string =  pytesseract.image_to_string(cao,lang='chi_sim')
	print ("the result is {}".format(rec_string))
	return rec_string

#def _get_image(url):
#	return Image.open(StringIO(requests.get(url).content))

def url_to_image(url):
	resp = urllib.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	return image

#a = process_image("https://www.realpython.com/images/blog_images/ocr/ocr.jpg")

#a = process_image("http://www.tp-link.com.cn/content/images/detail/R50kit/1.jpg")
#print a
