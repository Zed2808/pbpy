from deck import Suit, Card, Deck

class Gamestate:
	def __init__(self):
		self.num_players = 2
		self.hand_size = 6
		self.dealer = 0
		self.active_player = 1
		self.min_bid = 2
		self.bid = 0
		self.bidder = -1
		self.round = -1
		self.turn = 0
		self.taker = -1
		self.top_card = Card()
		self.trump = Suit.SPADES
		self.lead_suit = Suit.HEARTS
		self.deck = Deck(filled=True)
		self.middle = Deck()
		self.hands = []
		self.tricks = []
		self.scores = []
		self.score_limit = 11
		for player in range(self.num_players):
			self.hands.append(Deck())
			self.tricks.append(Deck())
			self.scores.append(0)

	# Increment active_player, loop if at end of player list
	def next_player(self):
		self.active_player += 1
		if self.active_player >= self.num_players:
			self.active_player = 0
		return self.active_player

	# Increment dealer, loop if necessary
	def next_dealer(self):
		self.dealer += 1
		if self.dealer >= self.num_players:
			self.dealer = 0
		return self.dealer
