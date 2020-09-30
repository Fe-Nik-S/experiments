
import logging


TO_SEARCH = [100, 5, 10, 3434, 34, -5, 8, 102, 45]


def binary_search(arr, element):
    arr = sorted(arr)
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


def main():
    logging.info("Start executing...")

    for element in [5, -10, 34]:
        founded_index = binary_search(TO_SEARCH, element)
        logging.info("Element '{}' founded in index {} ...".format(element, founded_index))

    logging.info("End executing...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
