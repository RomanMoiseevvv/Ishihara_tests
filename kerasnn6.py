from keras.utils import to_categorical
from keras import models
from keras import layers
import numpy as np
import os
import cv2

TEST_PATH = "data"
DATASET_PATH = TEST_PATH +"_dataset" + ".npz"
TRAIN_COUNT = 800
	
def create_dataset():
	'''
	Generate BORDER in file DATASET_PATH.npz element "dataset"
	'''
	images = list()
	labels = list()
	files = os.listdir(TEST_PATH)
	for filename in files:
		name,ext = os.path.splitext(filename)
		if ext == ".png":
			img = cv2.imread(os.path.join(TEST_PATH,name+'.png'))
			img = np.compress([True],cv2.resize(img, (28, 28)).reshape(784,3), axis=1 )
			images.append( img )
			labels.append( int(name[0]) )
	np.savez(DATASET_PATH,dataset= np.array( [images, labels] ) )
	
def get_dataset(path= DATASET_PATH):
	'''
	Generate BORDER from file DATASET_PATH.npz
	'''
	data = np.load(path, allow_pickle = True)['dataset']
	return ( np.stack(data[0],axis=0) , np.stack(data[1],axis=0) )


def create_network():
	images,labels = get_dataset()
	train_images, test_images = images[:TRAIN_COUNT], images[TRAIN_COUNT:]
	train_labels, test_labels = labels[:TRAIN_COUNT], labels[TRAIN_COUNT:]
	
	#model = VGG16(weights='imagenet', include_top=False)

	network = models.Sequential()
	#network.add(model)
	network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
	network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
	network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
	network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
	network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
	network.add(layers.Dense(10, activation='softmax'))

	network.compile(optimizer='rmsprop',
	loss='categorical_crossentropy',
	metrics=['accuracy'])


	train_images = train_images.reshape((TRAIN_COUNT, 28 * 28))
	train_images = train_images.astype('float32') / 255
	test_images = test_images.reshape((len(images) - TRAIN_COUNT, 28 * 28))
	test_images = test_images.astype('float32') / 255

	train_labels = to_categorical(train_labels)
	test_labels = to_categorical(test_labels)

	network.fit(train_images, train_labels, epochs=25, batch_size=128)

	test_acc = network.evaluate(test_images, test_labels)[1]
	print("Accuracy: ", test_acc)

def main():
	#create_dataset()
	create_network()

if __name__ == '__main__':
	main()
