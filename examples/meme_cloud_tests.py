import unittest
import meme_cloud as mc

class simpleTestCase(unittest.TestCase):
    def setUp(self):
        self.response = """there is a fooo in the baar and behind the baar there are two fooos: fooo and fooo"""

    def tearDown(self):
        self.response = None

    def test_word_count(self):
        cloud = mc.MemeCloud()
        cloud.content = self.response
        cloud.count()
        self.assertEqual(3, cloud.wordCount['fooo'])
        self.assertEqual(2,cloud.wordCount['baar'])

    def test_sorted_word_count(self):
        cloud = mc.MemeCloud()
        cloud.content = self.response
        sorted_cloud = cloud.sort()
        self.assertEqual('fooo', sorted_cloud[0][0])
        self.assertEqual(3, sorted_cloud[0][1])
        self.assertEqual('there', sorted_cloud[1][0])

    # TODO: fix this test
    def test_show_cloud(self):
        cloud = mc.MemeCloud()
        cloud.content = self.response

        sorted_cloud = cloud.sort()
        cloud.show(sorted_cloud)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(simpleTestCase)

    unittest.TextTestRunner(verbosity=2).run(suite)
