####################################
# Card and deck creation functions #
####################################
POSSIBLE_VALUES = set([1,2,3]) # possible values for properties

## Card representation
class Card(object):
  def __init__(self, number, color, fill, shape):
    assert all(map(lambda e: (type(e) is int) and (e >= 0 and e <=3), [number, color, fill, shape])), "all properties must be ints between [0, 3]" 
    self.number = number
    self.color = color
    self.fill = fill
    self.shape = shape
  
  def __eq__(self, other):
    return (self.number == other.number and
            self.color == other.color and
            self.fill == other.fill and
            self.shape == other.shape)

  def __repr__(self):
    return "Card(%d%d%d%d)"%(self.number, self.color, self.fill, self.shape)

  def __hash__(self):
    return int("%d%d%d%d"%(self.number, self.color, self.fill, self.shape))

def create_card(s):
  """
  Creates a card from a string of containing 4 numerical characters.
  (USEFUL FOR TESTING)
  
  Input:
    s (str) - 4 character string representing a card.
  Output:
    dictionary representation of a card.
  """
  assert len(s) == 4, "input string must contain exactly 4 chars"
  return Card(*map(int, s))  

def create_deck(n=81):
  """
  Generates a deck of at MOST 81 cards by iterating through all possible combination
  of values for properties.
  Input:
    n (int) (OPTIONAL) -- number of cards generate
  Output:
    <list<dic>> -- list of cards <represented by dict>
  """
  deck = []
  for num in POSSIBLE_VALUES:
    for col in POSSIBLE_VALUES:
      for fil in POSSIBLE_VALUES:
	for shp in POSSIBLE_VALUES:
	  if len(deck) > n:
	    return deck
	  deck.append(Card(num,col,fil,shp))
  return deck

###############################
# Set validity check functions#
###############################

def check_property(property_fn, card_set):
  """
  Checks to see if a given property is the same across all cards or completely different across all cards.
  Input:
    * property_fn (fn: Card -> int ) -- function called to extract value from a Card object
    * card_set (<list<Card>>) -- set of 3 cards to check.
  Output:
    True if the given property is the same across all cards or completely different across all cards.
  """
  assert len(card_set) == 3, "card set must contain exactly 3 cards"
  values = map(property_fn, card_set)
  isSame = values[0] == values[1] == values[2]
  isDiff = (values[0] != values[1]) and (values[1] != values[2]) and (values[0] != values[2])
  return isSame or isDiff


def is_set_valid(card_set):
  """
  Checks to see whether or not a set of cards is valid.
  Input:
   * property (str) -- property to check
   * card_set (<list<Card>) -- set of 3 cards to check
  Output:
    True if cards are valid. Else, False.
  """
  assert len(card_set) == 3, "set of cards must have exactly 3 cards"
  return reduce(lambda b,p: check_property(p, card_set) and b, 
         [lambda c: c.number, lambda c: c.color, lambda c: c.fill, lambda c: c.shape], True)


#############
# solvers   #
#############
def brute_solver(deck):
  """
  Finds all valid sets of cards via brute force search (O(n^3)).
  Input:
    * deck <list<Card>> -- deck of cards.
  Output:
    * list<list<Card>> -- list of valid sets. Note that sets of cards are
      represented by list of dicts.
  """
  n = len(deck)
  good_sets = []
  for c1_ind in range(n):
    for c2_ind in range(c1_ind + 1, n):
      for c3_ind in range(c2_ind + 1, n):
        proposal = sorted((deck[c1_ind], deck[c2_ind], deck[c3_ind]))
        if is_set_valid(proposal):
          good_sets.append(proposal)
  return good_sets


def pair_solver(deck):
  """
  Finds all valid sets of cards by iterating through all pair of cards and determining
  what card(s) would be needed to create valid sets of cards.
  Input:
    * deck <list<Card>> -- deck of cards.
  Output:
    * list<list<Card>> -- list of valid sets. Note that sets of cards are
      represented by lis of dicts.
  """
  n = len(deck)
  good_sets = set()
  for c1_ind in range(n):
    for c2_ind in range(c1_ind + 1, n):
      card1 = deck[c1_ind]
      card2 = deck[c2_ind] 
      # find required card(s) that would complete card1 and card2 to form a valid set
      for req in required_cards(card1, card2):
        # ensure that the card exists in the deck
        if req in deck:
          # append proposed set to good_set
          proposal = frozenset(sorted((card1, card2, req)))
          good_sets.add(proposal)
  # convert set to proper form and return
  return map(list, good_sets)

def required_cards(card1, card2):
  """
  This is a helper function for pair_solver!
  Given a pair of cards, this function determines what cards(s)
  is required to make a valid set.
  Input:
    * card1 <Card> - a card
    * card2 <Card> - a card
  Output:
    * <Generator<Card>> that will yield card(s) required to make a valid set.
  """
  def required_value(property_fn):
    # helper function to determine the value needed for a given property of a third card
    value1 = property_fn(card1)
    value2 = property_fn(card2)
    if value1 == value2:
      return [value1]
    return (POSSIBLE_VALUES - set([value1, value2]))
  for num in required_value(lambda c: c.number):
    for col in required_value(lambda c: c.color):
      for fil in required_value(lambda c: c.fill):
        for shp in required_value(lambda c: c.shape):
          retCard = Card(num, col, fil, shp)
          assert is_set_valid([card1, card2, retCard])
          yield retCard
  
if __name__ == "__main__":
  import time, random

  n_cards = int(raw_input("input the number of cards that you'd like in a deck (max of 81): "))
  deck = create_deck()
  deck = random.sample(deck, n_cards)

  start = time.time()
  soln_brute = brute_solver(deck)
  end = time.time()
  print "solving with brute force took (%f secs) and found (%d solutions)"%(end-start, len(soln_brute))
  
  start = time.time()
  soln_pair = pair_solver(deck)
  end = time.time()
  print "solving with pair-solver took (%f secs) and found (%d solutions)"%(end-start, len(soln_pair))

  # helper function to ensure the solution contains no duplicate entries
  def unique_sets(soln):
    res = set()
    for s in soln:
      res.add(frozenset(s))
    return res

  print "difference between the results:", unique_sets(soln_brute) - unique_sets(soln_pair)
  
  
