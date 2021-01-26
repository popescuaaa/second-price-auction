import unittest
import yaml
from solver import *

class SolverTest(unittest.TestCase):
	
	def setUp(self):
		with open('assets/cases.yaml') as f:
			testcases = yaml.load(f, Loader=yaml.FullLoader)
		# Prepare the setup
		self.testcases = testcases['cases']

	def test_solver_all_cases(self):
		for idx in self.testcases:
			current_case = self.testcases[idx]
			if 'buyers' in current_case:
				solver = Solver(current_case['buyers'], int(current_case['reserved_price']), current_case['solver'])
			else:
				solver = Solver({}, int(current_case['reserved_price']), current_case['solver'])

			result = solver.solve()
			
			(winner, winning_price) = result

			# Resolve string problems from yaml file
			if current_case['result']['name'] == 'None':
				current_case['result']['name'] = None

			if current_case['result']['price'] == 'None':
				current_case['result']['price'] = None
			else:
				current_case['result']['price'] = int(current_case['result']['price'])

			self.assertEqual(winner, current_case['result']['name'], 
							'Incorrect winner for: ~ {} ~'.format(current_case['name']))

			self.assertEqual(winning_price, current_case['result']['price'], 
							'Incorrect winning price for: ~ {} ~'.format(current_case['name']))


if __name__ == '__main__':
	unittest.main()
