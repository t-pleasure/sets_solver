import unittest
import time, random
from sets_solver import *

class SolverTest(unittest.TestCase):
  # tests to make sure validity functions work properly
  def test_set_validity(self):
    set1 = [create_card("1111"), create_card("2222"), create_card("3333")]
    set2 = [create_card("2222"), create_card("1111"), create_card("3233")]
    # set3 is the same as set2 except with a few cards swapped
    set3 = [create_card("1111"), create_card("2222"), create_card("3233")]
    # checks to make sure set1 has a valid number property
    self.assertTrue(check_property(lambda c: c.number, set1))  
    # checks to make sure set2 has an INVALID color property
    self.assertFalse(check_property(lambda c: c.color, set2))  
    # checks to make sure set3 has an INVALID color
    self.assertFalse(check_property(lambda c: c.color, set3))
    self.assertTrue(is_set_valid(set1))
    self.assertFalse(is_set_valid(set2))
    self.assertFalse(is_set_valid(set3))

  # tests the pair solver 
  def test_pair_solver(self):

    # helper method to convert soln to a hashable form
    def convert(soln):
      res = set()
      for s in soln:
        res.add(frozenset(s))
      return res
    # create deck
    deck = create_deck()

    # run the solver on multiple deck of cards (specified by N_ITERS)
    N_ITERS = 30
    for iteration in range(N_ITERS):
      # randomly create a deck by sampling from the original deck
      sample_deck = random.sample(deck, random.randint(3, 81))
      # solve using brute solver
      start = time.time()
      brute_soln = brute_solver(sample_deck)
      end = time.time()
      brute_time = end - start
      # solve using pair solver
      start = time.time()
      pair_soln = pair_solver(sample_deck)
      end = time.time()
      pair_time = end - start
      # convert solutions to a set<frozenset<str>> to allow for easy comparisons
      brute_soln = convert(brute_soln)
      pair_soln = convert(pair_soln)
      # ensure that solutions are equal
      self.assertEqual(len(brute_soln), len(pair_soln))
      self.assertEqual(brute_soln, pair_soln)
