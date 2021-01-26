import yaml
import const

class Solver:
	'''

		Second price sealed-bid auction is considered a classical problem in economics
		and it is one of the way ebay ads work these days. This problem is a very good example
		of applied Nash Equilibrium as the highest bidder price is not consider dominant 
		over all the others.

	'''

	def __init__(self, buyers: dict, reserved_price: int, solver_mode: str):
		self.solver_mode = solver_mode
		self.reserved_price = reserved_price
		self.buyers = buyers

		self.winner = None
		self.winning_price = None

		# Global mode memory
		self.memory = []


	def solve(self):
		if self.buyers != {}:

			# Check if there are any buyers to solve

			if self.solver_mode == const.STATE_MODE:
				self.state_solver()
				return self.winner, self.winning_price
			elif self.solver_mode == const.GLOBAL_MODE:
				self.global_solver()
				return self.winner, self.winning_price
			else:
				return const.NOT_SUPPORTED_SOLVER_MODE
		else:
			return self.winner, self.winning_price

	def state_solver(self):
		# Moving from state to state
		#
		# This is considered a dynamic programming approach as in this model
		# we use past information is a so called 'time series of states'
		#

		number_of_states = max(list(map(lambda e: len(self.buyers[e]['bids']), self.buyers)))
		
		post_winner = None
		post_winning_price = None

		current_winner = None
		current_winning_price = None

		for state_idx in range(number_of_states):
			state_bids = [(self.buyers[buyer_idx]['name'], self.buyers[buyer_idx]['bids'][state_idx])
							for buyer_idx in self.buyers 
							if len(self.buyers[buyer_idx]['bids']) > state_idx]

			sorted_bids = sorted(state_bids, key = lambda entry: entry[1], reverse = True)

			print(sorted_bids)

			# Compute current potential winner based only on this state info

			if sorted_bids[0][1] >= self.reserved_price:
				current_winner = sorted_bids[0]
				if sorted_bids[1][1] >= self.reserved_price:
					current_winning_price = sorted_bids[1]
				else:
					current_winning_price = sorted_bids[0]

			if post_winner is None and post_winning_price is None:
				post_winner = current_winner
				post_winning_price = current_winning_price

			# Evaluate based on past state info if the winner keeps his place
			# according to this type of system rules

			(c_name, p_price) = current_winner
			(p_name, c_price) = post_winner

			if p_name == c_name:

				# We have to pick the highest bid from the ones that the winner don't own
				# otherwise his bid

				(pp_name, pp_price) = post_winning_price
				(cc_name, cc_price) = current_winning_price

				if cc_name == c_name:
					current_winning_price = post_winning_price
				else:
					if cc_name == pp_name:

						# Take the lower one
						if pp_price < cc_price:
							current_winning_price = post_winning_price
					else:

						# Take the highest one
						if pp_price > cc_price:
							current_winning_price = post_winning_price

			else:
				# Take max from them
				if p_price > c_price:
					current_winner = post_winner

				(_, pp_price) = post_winning_price
				(_, cc_price) = current_winning_price

				if pp_price > cc_price:
					current_winning_price = post_winning_price


			post_winning_price = current_winning_price
			post_winner = current_winner

		(_, self.winning_price) = current_winning_price
		(self.winner, _) = current_winner

	def global_solver(self):
		# Create a databse with pairs of  < buyer name, max bid >
		# 
		# This solution is based of the fact that in this type of problems
		# we know all the information at the end and basically we can compute
		# the winner and he's winning price using 'all game' knowledge.
		#


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
			self.winner = top_name
			if self.memory[1][1] >= self.reserved_price:
				self.winning_price = self.memory[1][1]
			else:
				self.winning_price = top_bid












