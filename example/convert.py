import cv2
import os

def convert(name):
	#name = '4_Chilanka-Regular0'
	rgb = cv2.imread(name + '.png')

	lab = cv2.cvtColor(rgb, cv2.COLOR_BGR2Lab)


	l,a,b = cv2.split(lab)


	cv2.imwrite("L "+name+".png",l)
	cv2.imwrite("A "+name+".png",a)
	cv2.imwrite("B "+name+".png",b)

	b,g,r = cv2.split(rgb)

	cv2.imwrite("Red "+name+".png",r)
	cv2.imwrite("Green "+name+".png",g)
	cv2.imwrite("Blue "+name+".png",b)

def main():
	files = os.listdir()
	for filename in files:
		name,ext = os.path.splitext(filename)
		if ext == '.png':
			convert(name)

if __name__ == '__main__':
	main()