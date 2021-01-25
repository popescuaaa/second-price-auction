import yaml
import const

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
		if self.solver_mode == const.STATE_MODE:
			self.state_solver()
			return self.winner, self.winning_price
		elif self.solver_mode == const.GLOBAL_MODE:
			self.global_solver()
			return self.winner, self.winning_price
		else:
			return const.NOT_SUPPORTED_SOLVER_MODE

	def state_solver(self):
		number_of_states = max(list(map(lambda e: len(self.buyers[e]['bids']), self.buyers)))
		
		post_winner = None
		post_winning_score = None

		current_winner = None
		current_winning_score = None

		for state_idx in range(number_of_states):
			state_bids = [(self.buyers[buyer_idx]['name'], self.buyers[buyer_idx]['bids'][state_idx])
							for buyer_idx in self.buyers 
							if len(self.buyers[buyer_idx]['bids']) > state_idx]

			sorted_bids = sorted(state_bids, key = lambda entry: entry[1], reverse = True)

			print(sorted_bids)

			if sorted_bids[0][1] >= self.reserved_price:
				current_winner = sorted_bids[0][0]
				if sorted_bids[1][1] >= self.reserved_price:
					current_winning_score = sorted_bids[1][1]
				else:
					current_winning_score = sorted_bids[0][1]

			print('Current state: {} {}'.format(current_winner, current_winning_score))
			print('Old state: {} {}'.format(post_winner, post_winning_score))

		
			# Decide based on previous state information
			if state_idx != 0:
				if post_winning_score > current_winning_score and post_winner != current_winner:
					current_winner = post_winner
					current_winning_score = post_winning_score

			post_winning_score = current_winning_score
			post_winner = current_winner

		self.winning_price = current_winning_score
		self.winner = current_winner

	def global_solver(self):
		for buyer_idx in self.buyers:
			name = self.buyers[buyer_idx]['name']
			bids = self.buyers[buyer_idx]['bids']

			if bids:
				max_bid = max(bids)
			else:
				max_bid = const.DEFAULT_BID

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
    				int(tests['cases'][1]['reserved_price']), 
    				tests['cases'][1]['solver'])
    result = solver.solve()
    print(result)



















