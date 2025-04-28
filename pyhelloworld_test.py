import unittest

import pyhelloworld


class TestHelloWorld(unittest.TestCase):
    def test_helloworld(self):
        result = pyhelloworld.create()
        self.assertEqual("Hello world", result.id)
        self.assertEqual(3, result.duration.seconds)

if __name__ == "__main__":
    unittest.main()
