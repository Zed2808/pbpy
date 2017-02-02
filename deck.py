from enum import Enum
from random import shuffle
from collections import defaultdict

class Suit(Enum):
	SPADES   = 0
	HEARTS   = 1
	DIAMONDS = 2
	CLUBS    = 3

def value_to_char(value):
	value_chars = {
		10 : 'T',
		11 : 'J',
		12 : 'Q',
		13 : 'K',
		14 : 'A'
	}
	value_chars = defaultdict(lambda: value, value_chars)
	return value_chars[value]

def suit_to_char(suit):
	suit_chars = {
		Suit.SPADES   : '\u2660',
		Suit.HEARTS   : '\u2661',
		Suit.DIAMONDS : '\u2662',
		Suit.CLUBS    : '\u2663'
	}
	return suit_chars[suit]

class Card:
	# Create ace of spades by default
	def __init__(self, suit=Suit.SPADES, value=14):
		self.suit = suit
		self.value = value

	def to_string(self):
		return '{}{}'.format(value_to_char(self.value), suit_to_char(self.suit))

class Deck:
	# Empty by default
	def __init__(self, filled=False):
		self.deck = []
		if filled:
			self.fill_deck()

	# Fill the deck like a standard deck of 52 cards
	def fill_deck(self):
		# For each suit...
		for suit in Suit:
			# Add every card of that suit, 2-14 (ace)
			for value in range(2, 15):
				self.deck.append(Card(suit, value))
		# Shuffle deck after filling
		shuffle(self.deck)

	# Draw card off the top of the deck
	def draw(self):
		return self.deck.pop(0)

	# Add card to deck
	def add_card(self, card):
		self.deck.append(card)

	# Remove card from deck
	def remove_card(self, index):
		del self.deck[index]

	# Return length of list
	def size(self):
		return len(self.deck)

	# Return string representation of the deck
	def to_string(self):
		output = ''
		for card in self.deck:
			output += card.to_string() + ' '
		return output
