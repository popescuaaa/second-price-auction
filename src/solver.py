import yaml
from const import STATE_MODE, GLOBAL_MODE, NOT_SUPPORTED_SOLVER_MODE, DEFAULT_BID

class Solver:
	def __init__(self, buyers: dict, reserved_price: int, solver_mode: str):
		self.solver_mode = solver_mode
		self.reserved_price = reserved_price
		self.buyers = buyers

		self.winner = None
		self.winning_price = None

		# Global mode memory
		self.memory = []


	def solve(self):
		if self.solver_mode == STATE_MODE:
			self.state_solver()
			return self.winner, self.winning_price
		elif self.solver_mode == GLOBAL_MODE:
			self.global_solver()
			return self.winner, self.winning_price
		else:
			return NOT_SUPPORTED_SOLVER_MODE

	def state_solver(self):
		return 'hello'

	def global_solver(self):
		'''
			This is a static algorithm example, in which we can speculate 
			the a posteriori information about all the auction steps and 
			we can choose the winner based on his bid.
		'''
		for buyer_idx in self.buyers:
			name = self.buyers[buyer_idx]['name']
			bids = self.buyers[buyer_idx]['bids']

			if bids:
				max_bid = max(bids)
			else:
				max_bid = DEFAULT_BID

			self.memory.append((name, max_bid))

		self.memory = sorted(self.memory, key = lambda entry: entry[1], reverse = True)

		top_name, top_bid = self.memory[0][0], self.memory[0][1]

		if top_bid >= self.reserved_price:
			self.winner = (top_name, top_bid)	
			if self.memory[1][1] >= self.reserved_price:
				self.winning_price = self.memory[1][1]
			else:
				self.winning_price = top_bid


if __name__ == '__main__':
	# System configuration
    with open('assets/cases.yaml') as f:
        tests = yaml.load(f, Loader=yaml.FullLoader)

    solver = Solver(tests['cases'][1]['buyers'], 
    				tests['cases'][1]['reserved_price'], 
    				tests['cases'][1]['solver'])
    result = solver.solve()
    print(result)



















