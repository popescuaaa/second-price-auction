from solver import *

if __name__ == '__main__':
	with open('assets/cases.yaml') as f:
		testcases = yaml.load(f, Loader=yaml.FullLoader)

	# Prepare the setup
	testcases = testcases['cases']

	# Choose test
	target = testcases[2] # from 1 to 6 -> see assets/cases.yaml for details

	# Create a solver instance
	solver = Solver(target['buyers'], target['reserved_price'], target['solver'])

	# Call solver
	r = solver.solve() # winner name, winning price

	print('For current configuration: {}, the solution is: {} {} and the expected solution is: {} {}'.format(target['name'], r[0], r[1], 
																											 target['result']['name'], 
																											 target['result']['price']))