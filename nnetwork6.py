import numpy as np
import scipy.special
from keras.datasets import mnist
from math import *

TRAIN_COUNT = 100
TEST_COUNT = 10
EPOCH = 1

class Neural_network:
	"""docstring for Neural_network"""
	def __init__(self, layers_shape, speed= 0.1, alpha=1 ):
		# Learning speed
		self.speed = speed

		self.alpha = alpha

		self.shape = layers_shape

		self.activation_function = lambda x: 1 / ( 1 + exp( -2 * alpha * x ))
		# Tensor of output all neurons
		self.output = np.ndarray(shape= (len(layers_shape) , ) , dtype= list)
		# Init weight
		weights_list = list()
		for i in range(len(layers_shape)-1):
			weights_list.append( np.random.normal(0.0, pow(layers_shape[i], -0.5), (layers_shape[i], layers_shape[i+1])))
		self.weights_list = np.array(weights_list)

	def sign(self,input):
		return [ self.activation_function(x) for x in input ]
	
	def predict(self,input, i= 0):
		y = self.sign( np.dot(input,self.weights_list[i]) )
		if len(self.weights_list) == i + 1 :
			return y
		return self.predict(y,i+1)

	def get_output(self,input, i= 1):
		'''
		Return output matrix
		'''
		y = self.sign( np.dot(input,self.weights_list[i-1]) )
		self.output[i] = y 
		if i == 1:
			self.output[0] = input
		if len(self.output) == i + 1:
			return self.output
		return self.get_output(y,i+1)

	def lern(self,input,label):
		output = self.get_output(input) 
		delta =  output[1:]
		# DESCENT
		# LAST LAYER
		delta[-1] = -2 * self.alpha * output[-1] * np.array( 1.0 - x for x in output[-1] ) *( label - output[-1])
		# HIDEN LAYERS
		# REVERSE, BEGIN FROM SECOND FROM END
		for i in range( len(output) - 2 , 0, -1) : # CHOOSE LAYER
			#delta[i-1] = 2 * self.alpha * output[i] ( 1 - output[i] ) * sum ( delta[i][k] * self.weights_list[i][j] )
			for j, x in enumerate(output[i]): # CHOOSE NEURON
				delta[i-1][j] = 2 * self.alpha * x * ( 1 - x ) * sum ( delta[i][k] * self.weights_list[i][j][k] for k in range( len( delta[i] ) ) ) 
		# UPDATE WEIGHTS
		for layer in range(len(self.weights_list)): # CHOOSE LAYER
			self.weights_list[layer] -= self.speed * np.dot(delta[layer],output[layer].T) 
			



def main():
	(x_train, y_train), (x_test, y_test) = mnist.load_data()
	nn = Neural_network([784,200,10])
	for e in range(EPOCH):
		print("Epoch ", e)
		for i, digit in enumerate(x_train[:TRAIN_COUNT]): 
			inputs = digit.ravel()
			# scale the inputs
			inputs = (np.asfarray(inputs) / 255.0 * 0.99) + 0.01
		    # create the target output values (all 0.01, except the desired label which is 0.99)
			targets = np.zeros(10) + 0.01
			# all_values[0] is the target label for this record
			targets[y_train[i]] = 0.99
			nn.lern(inputs,targets)
			print(nn.predict(inputs) - targets)
			print(TRAIN_COUNT - i)
	
	for i, digit in enumerate(x_test[:TEST_COUNT]):
		inputs = digit.ravel()
		# scale the inputs
		inputs = (np.asfarray(inputs) / 255.0 * 0.99) + 0.01
	    # create the target output values (all 0.01, except the desired label which is 0.99)
		targets = np.zeros(10) + 0.01
		# all_values[0] is the target label for this record
		targets[y_test[i]] = 0.99
		print( targets ,"\n",  nn.predict(inputs),'\n')
		print( targets -  nn.predict(inputs))
	
	'''
	nn = Neural_network([3,10,1])
	for i in range(10000):
		nn.lern([1,0,1],[0.99])
	print(nn.predict([1,0,1]))
	'''
if __name__ == '__main__':
	main()


		