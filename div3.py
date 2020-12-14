from Pyro4 import expose
from random import randint
import random
from math import sqrt

class Solver:
	def __init__(self, workers=None, input_file_name=None, output_file_name=None):
		self.input_file_name = input_file_name
		self.output_file_name = output_file_name
		self.workers = workers
		print("Inited")

	def solve(self):
		print("Job Started")
		print("Workers %d" % len(self.workers))

		n = 2500000
		a = [randint(2, 1000000000) for i in range(n)]


		result = []
		step = int(n / len(self.workers))
		for i in xrange(0, len(self.workers)):
			left_range = i * step
			right_range = n if i == len(self.workers) - 1 else i * step + step
			result.append(self.workers[i].getDiv3Numbers(a[left_range: right_range]))

		self.write_output(result)

	@staticmethod
	@expose
	def getDiv3Numbers(a):
		result = []
		for x in a:
			y = int(sqrt(x))
			if y * y == x and Solver.is_probably_prime(y) :
				result.append(x)
		return result

	@staticmethod
	@expose
	def is_probably_prime(n):
		k = 20
		if (n < 2 ):
			return False
		output = True
		for i in range(0, k):
			a = randint(1, n-1)
			if (pow(a, n-1, n) != 1):
				return False
		return output
	

	def read_input(self):
		f = open(self.input_file_name, 'r')
		lines = [int(line.rstrip('\n')) for line in f]
		f.close()
		return lines
	def write_output(self, output):
		f = open(self.output_file_name, 'w')
		
		for a in output:
 			for i in a.value:
 				f.write(str(i) + ' ')
		f.close()
		print("output done")
