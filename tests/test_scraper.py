import unittest

from app.cleaner import clean_books


class TestCleaner(unittest.TestCase):

    def test_price_cleaning(self):

        sample = [
            {
                "title": "Python Book",
                "price": "£51.77",
                "rating": "Three",
                "availability": "In stock",
                "url": "sample_url"
            }
        ]

        cleaned = clean_books(sample)

        self.assertEqual(cleaned[0]["price"], "51.77")


if __name__ == "__main__":
    unittest.main()
