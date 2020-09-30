
import logging


TO_SORT = [100, 5, 10, 3434, 34, -5, 8, 102, 45]


def selection_sort(arr):
    def find_smallest(arr):
        smallest_idx = 0
        smallest_val = arr[smallest_idx]
        for idx in range(1, len(arr)):
            if arr[idx] < smallest_val:
                smallest_val = arr[idx]
                smallest_idx = idx
        return smallest_idx

    sorted_arr = []
    for idx in range(len(arr)):
        smallest_idx = find_smallest(arr)
        sorted_arr.append(arr.pop(smallest_idx))
    return sorted_arr


def main():
    logging.info("Start executing...")

    print("Array: {}".format(TO_SORT))
    sorted_arr = selection_sort(TO_SORT)
    print("Sorted array: {}".format(sorted_arr))

    logging.info("End executing...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
