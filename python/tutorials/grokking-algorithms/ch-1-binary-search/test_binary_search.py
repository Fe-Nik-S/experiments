
import unittest
import time

from binary_search import BinarySearch
from data import TestData, generate_data


class TestBinarySearch(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.arr = sorted(generate_data(1000, -2000, 2000))
        cls.expected_index = 867
        cls.expected_item = cls.arr[cls.expected_index]
        print("Initialized class...")

    def setUp(self):
        print("Start executing '{}'...".format(self._testMethodName))

    def test_iterative_bs_simple(self):
        arr = sorted(TestData.TO_SEARCH)
        item, expected_index = 45, 5

        index = BinarySearch.iterative_impl(arr, item)
        self.assertEqual(expected_index, index)

        item, expected_index = 105, -1
        index = BinarySearch.iterative_impl(arr, item)
        self.assertEqual(expected_index, index)

    def test_recursive_bs_simple(self):
        arr = sorted(TestData.TO_SEARCH)
        item, expected_index = 45, 5

        index = BinarySearch.recursive_impl(arr, item, 0, len(arr))
        self.assertEqual(expected_index, index)

        item, expected_index = 105, -1
        index = BinarySearch.recursive_impl(arr, item, 0, len(arr))
        self.assertEqual(expected_index, index)

    def test_binary_search_and_linear_search_execution_time(self):
        item, expected_index = self.expected_item, self.expected_index

        start_time = time.time()
        bs_iterative_founded_index = BinarySearch.iterative_impl(self.arr, item)
        bsi_time = time.time() - start_time

        start_time = time.time()
        bs_recursive_founded_index = BinarySearch.recursive_impl(self.arr, item, 0, len(self.arr))
        bsr_time = time.time() - start_time

        start_time = time.time()
        ls_founded_index = self.arr.index(item)
        bs_linear_time = time.time() - start_time

        self.assertEqual(expected_index, bs_iterative_founded_index)
        self.assertEqual(expected_index, bs_recursive_founded_index)
        self.assertEqual(expected_index, ls_founded_index)


if __name__ == '__main__':
    unittest.main()

