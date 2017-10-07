from crypto.utilities import preprocessor
import unittest


class PreprocessorTest(unittest.TestCase):
    def test_frankenstein(self):
        text = """From Italy they visited Germany and France.  I, their eldest child, was
        born at Naples, and as an infant accompanied them in their rambles.  I
        remained for several years their only child.  Much as they were
        attached to each other, they seemed to draw inexhaustible stores of
        affection from a very mine of love to bestow them upon me.  My mother's
        tender caresses and my father's smile of benevolent pleasure while
        regarding me are my first recollections."""

        # Breaking this onto multiple lines breaks the test. Sorry pep8.
        expected = """fromitalytheyvisitedgermanyandfranceitheireldestchildwasbornatnaplesandasaninfantaccompaniedthemintheirramblesiremainedforseveralyearstheironlychildmuchastheywereattachedtoeachothertheyseemedtodrawinexhaustiblestoresofaffectionfromaverymineoflovetobestowthemuponmemymotherstendercaressesandmyfatherssmileofbenevolentpleasurewhileregardingmearemyfirstrecollections"""

        self.assertSequenceEqual(''.join(preprocessor(text)), expected)

    def test_unicode(self):
        text = 'ÈÆÖÉEAEOE'
        expected = 'eaeoe'
        self.assertSequenceEqual(''.join(preprocessor(text)), expected)

        text = 'ÈÆÖÉEAEOE'
        expected = 'èæöéeaeoe'
        self.assertSequenceEqual(''.join(preprocessor(text, ascii=False)), expected)
