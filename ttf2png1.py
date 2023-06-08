import sys
import os
import subprocess
import random
from fontTools.ttLib import TTFont

RESULT_PATH = "fonts"
FONT_COUNT = 30
BAD_FONTS = (b'cst',b'rsfs',b'lklug',b'esint',b'ani',b'cmex',b'msam',b'EagleLake')

def gen_pics(TTF_PATH,FONT_SIZE = "500"):
	'''
	Generate png picture of digits with fonts from TTF_PATH.
	'''
	TTF_NAME = os.path.splitext(os.path.basename(TTF_PATH))[0]

	for i in range(10):
	    name = str(i)
	    output_png = os.path.join( RESULT_PATH ,name + "_" + TTF_NAME + ".png")
	    subprocess.call(["convert-im6.q16", "-font", TTF_PATH, "-pointsize", FONT_SIZE, "-background", "#FFFFFF", "label:" + str(i)  , output_png])

def main():
	# Read all fonts
	process = subprocess.Popen(['convert', '-list','font' ], stdout=subprocess.PIPE)
	out = process.communicate()[0]
	# Choose good fonts
	out = [x.decode("utf-8") for x in out.split() \
		   if x.find(b'ttf') != -1 and all( map( lambda type: x.find(type) == -1 , BAD_FONTS ) ) ]
	# Choise random fonts
	ttfs = random.sample(out,FONT_COUNT)
	print("Generate:")
	for x in ttfs:
		print(x)	
	'''
	ttfs = ["/home/dupeljan/.local/share/fonts/GamjaFlower-Regular.ttf",\
			"/usr/share/fonts/truetype/tlwg/Kinnari.ttf",\
			"/usr/share/fonts/truetype/tlwg/Laksaman-Italic.ttf",\
			"/home/dupeljan/.local/share/fonts/Lora-Bold.ttf",\
			"/usr/share/fonts/truetype/malayalam/Uroob.ttf"]
	'''
	if not os.path.isdir(RESULT_PATH):
		os.mkdir(RESULT_PATH)
	
	for ttf in ttfs:
		gen_pics(ttf)
	print("Generate digits successfuly")
		

if __name__ == '__main__':
	main()
