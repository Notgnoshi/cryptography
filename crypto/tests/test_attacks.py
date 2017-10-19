from crypto.attacks import *
from crypto.classical import *
from crypto.math import coprimes
import unittest

# A rather well behaved excerpt from Bram Stoker's Dracula.

well_behaved_message = """Who more gladly than we throughout the Four Nations received the 'bloody sword,' or at its warlike call flocked quicker to the standard of the King? When was redeemed that great shame of my nation, the shame of Cassova, when the flags of the Wallach and the Magyar went down beneath the Crescent? Who was it but one of my own race who as Voivode crossed the Danube and beat the Turk on his own ground? This was a Dracula indeed! Woe was it that his own unworthy brother, when he had fallen, sold his people to the Turk and brought the shame of slavery on them! Was it not this Dracula, indeed, who inspired that other of his race who in a later age again and again brought his forces over the great river into Turkey-land; who, when he was beaten back, came again, and again, and again, though he had to come alone from the bloody field where his troops were being slaughtered, since he knew that he alone could ultimately triumph! They said that he thought only of himself."""
well_behaved_plaintext = """whomoregladlythanwethroughoutthefournationsreceivedthebloodyswordoratitswarlikecallflockedquickertothestandardofthekingwhenwasredeemedthatgreatshameofmynationtheshameofcassovawhentheflagsofthewallachandthemagyarwentdownbeneaththecrescentwhowasitbutoneofmyownracewhoasvoivodecrossedthedanubeandbeattheturkonhisowngroundthiswasadraculaindeedwoewasitthathisownunworthybrotherwhenhehadfallensoldhispeopletotheturkandbroughttheshameofslaveryonthemwasitnotthisdraculaindeedwhoinspiredthatotherofhisracewhoinalaterageagainandagainbroughthisforcesoverthegreatriverintoturkeylandwhowhenhewasbeatenbackcameagainandagainandagainthoughhehadtocomealonefromthebloodyfieldwherehistroopswerebeingslaughteredsinceheknewthathealonecouldultimatelytriumphtheysaidthathethoughtonlyofhimself"""
# Encrypted with AffineCipher(9, 18)
affine_well_behaved_ciphertext = """idowopcunstnahdsfichdpoqudoqhhdcloqpfshmofypckcmzcthdcbnootayioptopshmhyispnmecksnnlnokectgqmkecphohdcyhsftsptolhdcemfuidcfisypctccwcthdshupcshydswcolwafshmofhdcydswcolksyyozsidcfhdclnsuyolhdcisnnskdsfthdcwsuaspicfhtoifbcfcshdhdckpcykcfhidoisymhbqhofcolwaoifpskcidosyzomzotckpoyycthdctsfqbcsftbcshhdchqpeofdmyoifupoqfthdmyisystpskqnsmftcctiocisymhhdshdmyoifqfiophdabpohdcpidcfdcdstlsnncfyontdmyxcoxnchohdchqpesftbpoqudhhdcydswcolynszcpaofhdcwisymhfohhdmytpskqnsmftcctidomfyxmpcthdshohdcpoldmypskcidomfsnshcpsucsusmfsftsusmfbpoqudhdmylopkcyozcphdcupcshpmzcpmfhohqpecansftidoidcfdcisybcshcfbskekswcsusmfsftsusmfsftsusmfhdoquddcdsthokowcsnofclpowhdcbnootalmcntidcpcdmyhpooxyicpcbcmfuynsqudhcpctymfkcdcefcihdshdcsnofckoqntqnhmwshcnahpmqwxdhdcaysmthdshdchdoqudhofnaoldmwycnl"""


class AffineAttackTest(unittest.TestCase):
    def test_affine_naive(self):
        attack = AffineAttack(affine_well_behaved_ciphertext)
        decrypted = attack.naive_frequency_attack()
        self.assertSequenceEqual(decrypted, well_behaved_plaintext)

    def test_all_keys_naive(self):
        # Does a naive attack work on all combinations of a and b for this plaintext?
        for a in coprimes(26):
            for b in range(26):
                cipher = AffineCipher(a, b)
                ciphertext = cipher.encrypt(well_behaved_plaintext)
                attack = AffineAttack(ciphertext)
                decrypted = attack.naive_frequency_attack()
                self.assertSequenceEqual(decrypted, well_behaved_plaintext)


class VigenereAttackTest(unittest.TestCase):
    def test_vigenere(self):
        pass