
import logging
from data import TestData


class BinarySearch:
    @staticmethod
    def iterative_impl(arr, element):
        left = 0
        right = len(arr) - 1
        while left <= right:
            mid_index = int((left + right)/2)
            item_by_index = arr[mid_index]
            if item_by_index == element:
                return mid_index

            if item_by_index > element:
                right = mid_index - 1
            else:
                left = mid_index + 1
        return -1

    @staticmethod
    def recursive_impl(arr, element, left_idx, right_idx):
        if right_idx >= left_idx:
            mid_idx = int((left_idx + right_idx) / 2)
            item_by_index = arr[mid_idx]
            if item_by_index == element:
                return mid_idx

            if item_by_index > element:
                return BinarySearch.recursive_impl(arr, element, left_idx, mid_idx - 1)

            return BinarySearch.recursive_impl(arr, element, mid_idx + 1, right_idx)

        return -1


def main():

    arr = sorted(TestData.TO_SEARCH)

    logging.info("Start executing, iterative implementation..")
    for element in [5, -10, 34]:
        founded_index = BinarySearch.iterative_impl(arr, element)
        logging.info("Element '{}' founded in index {} ...".format(element, founded_index))

    logging.info("Start executing, recursive implementation..")
    for element in [5, -10, 34]:
        founded_index = BinarySearch.recursive_impl(arr, element, 0, len(arr))
        logging.info("Element '{}' founded in index {} ...".format(element, founded_index))

    logging.info("End executing...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
