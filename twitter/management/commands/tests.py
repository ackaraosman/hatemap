import unittest
from . import get_feature_vector, process_tweet


class TestProcessTweet(unittest.TestCase):
    def test_url(self):
        tweet = 'Franklin St.: I WAS THERE!! http://tinyurl.com/49955t3'
        expected = 'franklin st.: i was there!! URL'
        self.assertEqual(process_tweet(tweet), expected)

    def test_hashtag(self):
        tweet = 'Do you #jokes #quotes #music #photos or #news #articles'
        expected = 'do you jokes quotes music photos or news articles'
        self.assertEqual(process_tweet(tweet), expected)

    def test_username(self):
        tweet = 'Selam @1907fener nasılsın'
        expected = 'selam AT_USER nasılsın'
        self.assertEqual(process_tweet(tweet), expected)


class TestFeatureVector(unittest.TestCase):
    def test_simple_tweet(self):
        tweet = 'Ses kes amk!!! 3beş beşiktaş???'
        expected = ['ses', 'kes', 'amk', '3beş', 'beşiktaş']
        self.assertEqual(get_feature_vector(tweet), expected)


if __name__ == '__main__':
    unittest.main()
