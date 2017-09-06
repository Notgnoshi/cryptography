from crypto import BlumBlumShub as bbs
import gmpy2 as mp
import unittest


class BlumBlumShubTest(unittest.TestCase):
    def test_bbsn(self):
        # Taken from textbook, page 43.
        p = mp.mpz(24672462467892469787)
        q = mp.mpz(396736894567834589803)
        x0 = mp.mpz(873245647888478349013)

        expecteds = [8845298710478780097089917746010122863172,
                     7118894281131329522745962455498123822408,
                     3145174608888893164151380152060704518227,
                     4898007782307156233272233185574899430355,
                     3935457818935112922347093546189672310389,
                     675099511510097048901761303198740246040,
                     4289914828771740133546190658266515171326,
                     4431066711454378260890386385593817521668,
                     7336876124195046397414235333675005372436]
        for actual, expected in zip(bbs.bbsn(p, q, x0, 9), expecteds):
            self.assertEqual(actual, expected)
