import unittest


class BasicTestCase(unittest.TestCase):
    def test_sanity(self):
        self.assertEqual(1 + 1, 2)


if __name__ == "__main__":
    unittest.main()
