from gamestate import Gamestate

class Game:
	def __init__(self):
		self.gs = Gamestate()
		# self.pb = PB()

	def play(self):
		print('Player {} is the dealer.'.format(self.gs.dealer+1))

		# Deal players' hands
		for player in range(self.gs.num_players):
			for card in range(self.gs.hand_size):
				self.gs.hands[player].add_card(self.gs.deck.draw())

		# Print player's hand
		print('Your hand:\n{}'.format(self.gs.hands[0].to_string()))

		# Do bidding round, return highest bidder
		self.gs.active_player = self.bidding_round()

		# Print highest bidder and their bid
		print('Player {} won the bidding round with a bid of {}.'.format(self.gs.bidder, self.gs.bid))

