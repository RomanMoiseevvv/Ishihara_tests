import cv2
import numpy as np
from random import randint
import os

SOURCE_PATCH = "test5"
RESULT_PATH = "noise test5"

def add_noise(name,k=10):
	'''
	Add noise in each pixel of name.png.
	256/k - ratio of dispersion.
	'''
	range_ = int(512/k)
	img = cv2.imread(os.path.join(SOURCE_PATCH ,  name + ".png"))

	for i in range(len(img)):
		for j , x in enumerate(img[i]):
			rand = [ int (randint(0,range_) - range_ / 2)  for i in range(3)]
			for k in range(3):
				sum_ = x[k] + rand[k] 
				if sum_ <= 0:
					rand[k] = 0
				elif 0 < sum_ < 255:
					rand[k] = sum_
				else:
					rand[k] = 255 
			img[i][j] =  rand
	cv2.imwrite(os.path.join(RESULT_PATH , name+".png"),img)
	print ( name+".png" + " generated")

def main():
	if not os.path.isdir(RESULT_PATH):
		os.mkdir(RESULT_PATH)
	files = os.listdir(SOURCE_PATCH)
	count = 0
	for filename in files:
		name,ext = os.path.splitext(filename)
		if ext == ".png":
			add_noise(name)
			count += 1
			print("not more than " + str(len(files) - count) + " files left" )
	print("Generate test success")

if __name__ == '__main__':
	main()