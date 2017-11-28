import better_exceptions
import unittest
from parameterized import parameterized


class TestAdd(unittest.TestCase):

    @parameterized.expand([
        ("01",1, 1, 2),
        ("02",2, 2, 5),
        ("03",3, 3, 6),
    ])
    def test_add(self, name, a, b, c):
        try:
            self.assertEqual(a + b, c)
        except:
            print 'faild'


if __name__ == '__main__':
    unittest.main(verbosity=2)