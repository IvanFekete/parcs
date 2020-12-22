from Pyro4 import expose
from random import randint
import random
import string
from math import sqrt

popcount = lambda x: 0 if x == 0 else x % 2 + popcount(x // 2)

class Solver:
	def __init__(self, workers=None, input_file_name=None, output_file_name=None):
		self.input_file_name = input_file_name
		self.output_file_name = output_file_name
		self.workers = workers
		print("Inited")

	def solve(self):
		print("Job Started")
		print("Workers %d" % len(self.workers))

		a = self.read_input()
		n = len(a)

		masks = (1 << n)

		step = int(masks / len(self.workers))
		result = []
		for i in xrange(0, len(self.workers)):
			left_range = i * step
			right_range = masks if i == len(self.workers) - 1 else i * step + step
			result.append(self.workers[i].getMaximalCliqueSize(n, a, left_range, right_range))

		self.write_output(max([x.value for x in result]))

	@staticmethod
	@expose
	def getMaximalCliqueSize(n, a, left_range, right_range):
		result = 0


		for mask in range(left_range, right_range):
			ok = True
			for i in range(n):
				if (mask >> i) % 2 == 1:
					for j in range(n):
						if j != i and (mask >> j) % 2 == 1 and not a[i][j]:
							ok = False
							break
					if not ok: break
			if ok:
				result = max(result, popcount(mask))


		return result


	def read_input(self):
		f = open(self.input_file_name, 'r')
		lines = [line.rstrip('\n') for line in f]
		n = int(lines[0])
		a = [[False for _ in range(n)] for __ in range(n)]
		for line in lines[1:]:
			u, v = map(int, line.split())
			a[u][v] = a[v][u] = True

		f.close()
		return a

	def write_output(self, output):
		f = open(self.output_file_name, 'w')
		f.write(str(output))
		f.close()
		print("output done")
