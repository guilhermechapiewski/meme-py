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
        sortedCloud = cloud.sort()
        self.assertEqual('fooo', sortedCloud[0][0])
        self.assertEqual(3, sortedCloud[0][1])
        self.assertEqual('there', sortedCloud[1][0])

    # TODO: fix this test
    def test_show_cloud(self):
        cloud = mc.MemeCloud()
        cloud.content = self.response

        sortedCloud = cloud.sort()
        cloud.showCloud(sortedCloud)

if __name__ == '__main__':
#    unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(simpleTestCase)

    unittest.TextTestRunner(verbosity=2).run(suite)

