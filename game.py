from collections import defaultdict
from gamestate import Gamestate
from pb import PB
from deck import Deck

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

		# Set round from -1 (bidding round) to 0
		self.gs.round = 0

		# Play out a hand
		for player in range(self.gs.hand_size):
			self.gs.active_player = self.do_round()
			self.gs.round += 1

		# Print each player's tricks after the hand
		for player in range(self.gs.num_players):
			print('Player {} took {}'.format(player + 1, self.gs.tricks[player].to_string()))

		# Score each player's hand and increment their score accordingly
		self.score_hands()

		# Print score
		print('\nSCORE')
		for player in range(self.gs.num_players):
			print('Player {} has {} points.'.format(player + 1, self.gs.scores[player]))

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

	# Play a round and return the winning player
	def do_round(self):
		print('Player {} is leading out.'.format(self.gs.active_player + 1))

		# Give each player a turn to play their card
		for turn in range(self.gs.num_players):
			self.gs.turn = turn

			# Force player to play their last card
			if self.gs.round == self.gs.hand_size - 1:
				choice = 1
			else:
				# Human
				if self.gs.active_player == 0:
					# Print player's hand
					print('Your hand:\n{}'.format(self.gs.hands[self.gs.active_player].to_string()))
					# Print selection numbers under hand
					for i in range(self.gs.hands[self.gs.active_player].size()):
						print('{}. '.format(i + 1), end='')

					# Let player choose a card
					# Loop until valid choice
					while True:
						choice = int(input('\nChoose a card to play (1-{}): '.format(self.gs.hand_size - self.gs.round)))
						# Choice out of bounds
						if choice < 1 or choice > self.gs.hands[self.gs.active_player].size():
							print('Invalid choice.')
						else:
							break
				# Bot
				else:
					choice = self.pb.play_card(self.gs)

			# Get played card from hand
			played_card = self.gs.hands[self.gs.active_player].deck[choice - 1]

			# Print played card
			print ('Player {} plays {}.'.format(self.gs.active_player + 1, played_card.to_string()))

			# If leading the round
			if self.gs.turn == 0:
				self.gs.lead_suit = played_card.suit
				self.gs.taker = self.gs.active_player
				self.gs.top_card = played_card

				# Set trump if first round
				if self.gs.round == 0:
					self.gs.trump = played_card.suit
					print('Trump is now {}.'.format(self.gs.trump.name))
			# Check if new card beats previous top
			else:
				# Current top card is trump
				if self.gs.top_card.suit == self.gs.trump:
					# Played card is also trump
					if played_card.suit == self.gs.trump:
						# Played card beats value of top card
						if played_card.value > self.gs.top_card.value:
							self.gs.top_card = played_card
							self.gs.taker = self.gs.active_player
				# Current top card is not trump (must be lead suit)
				else:
					# Played card is trump
					if played_card.suit == self.gs.trump:
						self.gs.top_card = played_card
						self.gs.taker = self.gs.active_player
					# Played card is lead suit
					elif played_card.suit == self.gs.lead_suit:
						# Played card beats value of top card
						if played_card.value > self.gs.top_card.value:
							self.gs.top_card = played_card
							self.gs.taker = self.gs.active_player

			# Move card from hand to the middle pile
			self.gs.middle.add_card(played_card)
			self.gs.hands[self.gs.active_player].remove_card(choice - 1)

			# Move on to next player
			self.gs.next_player()

		print('Player {} takes the trick.'.format(self.gs.taker + 1))

		# Take trick
		for card in range(self.gs.num_players):
			self.gs.tricks[self.gs.taker].add_card(self.gs.middle.deck[card])

		# Clear middle
		self.gs.middle = Deck()

		# Return winner of the round
		return self.gs.taker

	# Score each player's hand and increment points according
	def score_hands(self):
		high_trump = 0
		low_trump = 14
		jack_taker = -1
		game_taker = -1
		round_scores = []
		pips = []

		# Pip values for each card
		pip_values = {
			10 : 10,
			11 : 1,
			12 : 2,
			13 : 3,
			14 : 4
		}
		pip_values = defaultdict(lambda: 0, pip_values)

		# For each stack of tricks
		for player in range(self.gs.num_players):
			# Append 0 to round_score and pips for each player

			round_scores.append(0)
			pips.append(0)
			# For each card in the stack
			for card in range(self.gs.tricks[player].size()):
				current_card = self.gs.tricks[player].deck[card]
				# If card is trump
				if current_card.suit == self.gs.trump:
					# Card is higher than current high trump
					if current_card.value > high_trump:
						high_trump = current_card.value
						high_taker = player

					# Card is lower than current low trump
					if current_card.value < low_trump:
						low_trump = current_card.value
						low_taker = player

					# Card is jack
					if current_card.value == 11:
						jack_taker = player

					# Add pips
					pips[player] += pip_values[current_card.value]

		# Find game point taker
		max_pips = 0
		for player in range(self.gs.num_players):
			if pips[player] > max_pips:
				game_taker = player
				max_pips = pips[player]

		# Add up round scores
		round_scores[high_taker] += 1
		round_scores[low_taker] += 1
		round_scores[game_taker] += 1
		if jack_taker > -1:
			round_scores[jack_taker] += 1

		# Bidder does not make their bid
		if round_scores[self.gs.bidder] < self.gs.bid:
			# Lose points equal to bid and set round score to 0
			# (bidder gets nothing when points are added)
			self.gs.scores[self.gs.bidder] -= self.gs.bid
			round_scores[self.gs.bidder] = 0

		# Increment game scores
		for player in range(self.gs.num_players):
			self.gs.scores[player] += round_scores[player]

		# Print who got what points
		print('Player {} took high.'.format(high_taker + 1))
		print('Player {} took low.'.format(low_taker + 1))
		if jack_taker > -1:
			print('Player {} took jack.'.format(jack_taker + 1))
		print('Player {} took game.'.format(game_taker + 1))
