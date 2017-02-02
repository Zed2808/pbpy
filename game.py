from gamestate import Gamestate
from pb import PB

class Game:
	def __init__(self):
		self.gs = Gamestate()
		self.pb = PB()

	def play(self):
		print('Player {} is the dealer.'.format(self.gs.dealer + 1))

		# Deal players' hands
		for player in range(self.gs.num_players):
			for card in range(self.gs.hand_size):
				self.gs.hands[player].add_card(self.gs.deck.draw())

		# Print player's hand
		print('Your hand:\n{}'.format(self.gs.hands[0].to_string()))

		# Do bidding round, return highest bidder
		self.bidding_round()
		self.gs.active_player = self.gs.bidder

		# Print highest bidder and their bid
		print('Player {} won the bidding round with a bid of {}.'.format(self.gs.bidder + 1, self.gs.bid))

		# Play out a hand
		for player in range(self.gs.num_players):
			self.gs.active_player = self.do_round()

	# Returns player that wins the bidding round
	def bidding_round(self):
		print('Player {} bids first.'.format(self.gs.active_player + 1))

		bid = 0

		# Bid until back to the dealer
		while self.gs.active_player != self.gs.dealer:
			# Human
			if self.gs.active_player == 0:
				print('Current bid is {}.'.format(bid))
				# Loop until valid bid
				while True:
					# Get bid from the player
					bid = input('Your bid (0 to pass): ')
					# If bid too small/large, get new bid
					if bid < self.gs.min_bid or bid > 4 and bid != 0:
						print('Bid must be between {} and 4.'.format(self.gs.min_bid))
					# Valid bid
					else:
						# Player does not pass
						if bid != 0:
							self.gs.bid = bid
							self.gs.min_bid = bid + 1
							self.gs.bidder = self.gs.active_player
						break
			# Bot
			else:
				# Get bid from bot
				bid = self.pb.bid(self.gs)
				# Bot passes
				if bid == 0:
					print('Player {} passes the bid.'.format(self.gs.active_player + 1))
				else:
					self.gs.bid = bid
					self.gs.min_bid = bid + 1
					self.gs.bidder = self.gs.active_player
					print('Player {} bid {}.'.format(self.gs.active_player + 1, bid))

			self.gs.next_player()

		# No bids, dealer's bid is forced
		if self.gs.bid < 2:
			print('Player {} is forced to bid {}.'.format(self.gs.active_player + 1, self.gs.min_bid))
			self.gs.bid = self.gs.min_bid
			self.gs.bidder = self.gs.active_player

			return self.gs.bidder

		# Give dealer chance to match or pass
		# Human
		if self.gs.active_player == 0:
			print('As the dealer, you may match Player {}\'s bid of {} or pass.'.format(self.gs.active_player + 1, self.gs.bid))
			# Loop until valid input (match/pass)
			while True:
				bid = input('Match bid or pass (0): ')
				# Invalid bid
				if bid != 0 and bid != self.gs.bid:
					print('Bid must be {} or pass (0).'.format(self.gs.bid))
				else:
					break
		# Bot
		else:
			bid = self.pb.bid(gs)

		# Dealer passes
		if bid == 0:
			print('Player {} passes.'.format(self.gs.active_player + 1))
		# Dealer matches
		else:
			print('Player {} matches Player {}\'s bet of {}.'.format(self.gs.active_player + 1, self.gs.bidder + 1, self.gs.bid))
			self.gs.bidder = self.gs.active_player
