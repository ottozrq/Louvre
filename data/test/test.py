import unittest
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import miner
import artwork


class TestMiner(unittest.TestCase):

    def test_louvre_miner(self):
        url = "https://art.rmngp.fr/en/library/artworks?locations=mus%C3%A9e%20du%20Louvre&ajax=1&page=0"
        miner.louvre_miner(url)
        artworks = artwork.Artwork.objects
        self.assertEqual(len(artworks), 20)

    def test_clear_db(self):
        miner.clear_database()
        artworks = artwork.Artwork.objects
        self.assertEqual(len(artworks), 0)

    def test_google_search(self):
        title = 'La mort de Cléopâtre'
        self.assertIsNotNone(miner.description_miner(title))
        self.assertEqual(len(miner.training_img_miner(title)), 100)


if __name__ == '__main__':
    unittest.main()
