import cv2
import numpy as np
import os 

DIR_NAME = "fonts"
BORDER = 1.5
def gen_norm(name):
	'''
	Search contour, cut out the shape 
	and insert into the center of the new picture.
	
	Border is the ratio of the length of square edge
	of obtained image to the larger side of the cut-out digit.
	'''
	
	img = cv2.imread(os.path.join(DIR_NAME,name+'.png'))
	hsv = cv2.cvtColor( img, cv2.COLOR_BGR2HSV )
	thresh = cv2.inRange( hsv, 0, 255,0 )
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[1:]

	try:
		x0 = ( min(contours[0][i][0][0] for i in range(contours[0].shape[0])), min(contours[0][i][0][1] for i in range(contours[0].shape[0])) )
		x1 = ( max(contours[0][i][0][0] for i in range(contours[0].shape[0])), max(contours[0][i][0][1] for i in range(contours[0].shape[0])) )
	except IndexError:
		print("Error to norm ",name)
		return

	# gen new picture
	weight = height = int ( max ( x1[0] - x0[0] , x1[1] - x0[1] )  * BORDER )

	new_img = np.zeros((weight,height,3), np.uint8)
	cv2.rectangle(new_img,(0,0),(weight,height),(255,255,255),-1)

	dx = int ( weight / 2 - (x1[1] - x0[1]) / 2 )
	dy = int ( height / 2 - (x1[0] - x0[0]) / 2 )
	new_img[dx:x1[1]-x0[1] + dx, dy :x1[0] - x0[0]  + dy ] = img[x0[1]:x1[1], x0[0]:x1[0]]


	cv2.imwrite(os.path.join(DIR_NAME,name+'.png'),new_img)

def main():
	files = os.listdir(DIR_NAME)
	for filename in files:
		name,ext = os.path.splitext(filename)
		if ext == ".png":
			gen_norm(name)

	print("Normalize all pic in current dir")
if __name__ == '__main__':
	main()
