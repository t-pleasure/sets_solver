####################################
# Card and deck creation functions #
####################################
POSSIBLE_VALUES = set([1,2,3]) # possible values for properties
NUMBER_INDX = 0
COLOR_INDX = 1
FILL_INDX = 2
SHAPE_INDX = 3

def create_card(s):
  """
  Creates a card from a string of containing 4 numerical characters.
  Please see NUMBER_INDX, COLOR_INDX, FILL_INDX, SHAPE_INDX for reference.
  
  Input:
    s (str) - 4 character string representing a card.
  Output:
    dictionary representation of a card.
  """
  assert len(s) == 4, "input string must contain exactly 4 chars"
  return {"number": int(s[0]),
          "color": int(s[1]),
          "fill": int(s[2]),
          "shape": int(s[3])}

def card_to_str(card):
  """
  Helper function to convert a card back into its string representation
  Input:
    card -- dictionary representaiton of a card.
  Output:
    String representation of a card
  """
  return "%d%d%d%d"%(card["number"], card["color"], card["fill"], card["shape"])

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
	  property_str = "%d%d%d%d"%(num,col,fil,shp)
	  deck.append(create_card(property_str))
  return deck

###############################
# Set validity check functions#
###############################

def check_property(property, card_set):
  """
  Checks to see if a given property is the same across all cards or completely different across all cards.
  Input:
    * property (str) -- property to check
    * card_set (<list<dict>>) -- set of 3 cards to check.
  Output:
    True if the given property is the same across all cards or completely different across all cards.
  """
  assert len(card_set) == 3, "card set must contain exactly 3 cards"
  isSame = ((card_set[0][property] == card_set[1][property]) and (card_set[1][property] == card_set[2][property]) and (card_set[0][property] == card_set[2][property]))
  isDiff = (card_set[0][property] != card_set[1][property] and card_set[1][property] != card_set[2][property] and card_set[0][property] != card_set[2][property])
  return isSame or isDiff


def is_set_valid(card_set):
  """
  Checks to see whether or not a set of cards is valid.
  Input:
   * property (str) -- property to check
   * card_set (<list<dict>>) -- set of 3 cards to check
  Output:
    True if cards are valid. Else, False.
  """
  assert len(card_set) == 3, "set of cards must have exactly 3 cards"
  return reduce(lambda b,p: check_property(p, card_set) and b, 
         ["number", "color", "fill", "shape"], True)


#############
# solvers   #
#############
def brute_solver(deck):
  """
  Finds all valid sets of cards via brute force search (O(n^3)).
  Input:
    * deck <list<dict>> -- deck of cards.
  Output:
    * list<list<dict>> -- list of valid sets. Note that sets of cards are
      represented by list of dicts.
  """
  n = len(deck)
  good_sets = []
  for c1_ind in range(n):
    for c2_ind in range(c1_ind + 1, n):
      for c3_ind in range(c2_ind + 1, n):
        proposal = [deck[c1_ind], deck[c2_ind], deck[c3_ind]]
        if is_set_valid(proposal):
          good_sets.append(proposal)
  return good_sets


def pair_solver(deck):
  """
  Finds all valid sets of cards by iterating through all pair of cards and determining
  what card(s) would be needed to create valid sets of cards.
  Input:
    * deck <list<dict>> -- deck of cards.
  Output:
    * list<list<dict>> -- list of valid sets. Note that sets of cards are
      represented by list of dicts.
  """
  n = len(deck)
  # convert cards to str representation for efficiency in lookup
  deck =[card_to_str(card) for card in deck]
  good_sets = set()
  for c1_ind in range(n - 1):
    for c2_ind in range(c1_ind + 1, n):
      card1 = deck[c1_ind]
      card2 = deck[c2_ind] 
      # find required card(s) that would complete card1 and card2 to form a valid set
      for req in required_cards(card1, card2):
        # ensure that the card exists in the deck
        if req in deck:
          # append proposed set to good_set
          proposal = frozenset((card1, card2, req))
          good_sets.add(proposal)
  # convert set to proper form and return
  return map(lambda s: map(create_card, s), good_sets)

def required_cards(card1, card2):
  """
  This is a helper function for pair_solver!
  Given a pair of cards, this function determines what cards(s)
  is required to make a valid set.
  Input:
    * card1 <dict> - a card
    * card2 <dict> - a card
  Output:
    * <Generator<dict>> that will yield card(s) required to make a valid set.
  """
  def required_property(p):
    if card1[p] == card2[p]:
      return [card1[p]]
    return (set(["1","2","3"]) - set([card1[p], card2[p]]))
  for num in required_property(NUMBER_INDX):
    for col in required_property(COLOR_INDX):
      for fil in required_property(FILL_INDX):
        for shp in required_property(SHAPE_INDX):
          yield "%s%s%s%s"%(num, col, fil, shp)
  
if __name__ == "__main__":
  import time, random

  n_cards = int(raw_input("input the number of cards that you'd like in a deck (max of 81): "))
  deck = create_deck()
  deck = random.sample(deck, n_cards)

  start = time.time()
  soln_brute = brute_solver(deck)
  end = time.time()
  print "solving with brute force took:", end-start
  
  start = time.time()
  soln_pair = pair_solver(deck)
  end = time.time()
  print "solving with pair-solver took:", end-start
  
