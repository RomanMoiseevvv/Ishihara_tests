import cv2
import numpy as np
import os

SOURCE_PATCH = "noise test5"
RESULT_PATH = "filtred_noise 5"

def filter(name):
	''' 
	Select number from name.png test card.
	Create b/w picture of it.
	'''
	rgb = cv2.imread(os.path.join(SOURCE_PATCH,name+'.png'))
	lab = cv2.cvtColor(rgb, cv2.COLOR_BGR2Lab)

	average_a = np.array( list(x[1]  for i in range(len(lab)) for x in lab[i] )) .mean()
	average_b = 0
	
	a = cv2.split(lab)[1]
	if average_a < 130: # MANY GREEN OR BLUE, IN A CONTRAST 
		rgb = cv2.threshold(a,132,255,cv2.THRESH_BINARY)[1]
		state = 1
	else:
		average_b = np.array( list(x[2]  for i in range(len(lab)) for x in lab[i] )) .mean()
		if  average_b < 135: # LITTLE RED => RED CHANNEL DARK, IN A CONTRAST
			state = 2
			rgb = cv2.threshold(a,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]#
		else:
			state = 3 # МНОГО КРАСНОГО => MANY RED => RED CHANNEL LIGHT, IN RED CONTRAST
			rgb = cv2.threshold(cv2.split(rgb)[2],227,255,cv2.THRESH_BINARY)[1] 
			rgb = cv2.bitwise_not(rgb)
	
	kernel_opening = np.ones((2,2),np.uint8) 
	kernel_closing = np.ones((12, 12),np.uint8)

	opening = cv2.morphologyEx(rgb, cv2.MORPH_OPEN, kernel_opening)
	closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_closing)

	dst = cv2.medianBlur(closing,5)

	cv2.imwrite( os.path.join(RESULT_PATH ,  name +".png"),dst )
	print(name+".png filtered")


def main():
	if not os.path.isdir(RESULT_PATH):
		os.mkdir(RESULT_PATH)
	files = os.listdir(SOURCE_PATCH)
	
	for filename in files:
		name,ext = os.path.splitext(filename)
		if ext == ".png":
			filter(name)

if __name__ == '__main__':
	main()