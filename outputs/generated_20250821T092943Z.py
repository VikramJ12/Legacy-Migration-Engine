class BubbleSort:
    def __init__(self, arr):
        """
        Initialize the BubbleSort object with an array.
        
        Args:
        arr (list): The array to be sorted.
        """
        self.arr = arr

    def sort(self):
        """
        Sort the array using the bubble sort algorithm.
        """
        n = len(self.arr)
        i = 0
        while i < n - 1:
            swapped = False
            j = 0
            while j < n - i - 1:
                if self.arr[j] > self.arr[j + 1]:
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
                    swapped = True
                j += 1
            if not swapped:
                break
            i += 1

    def print_array(self):
        """
        Print the sorted array.
        """
        print(self.arr)


# Example usage:
arr = [64, 34, 25, 12, 22, 11, 90]
bubble_sort = BubbleSort(arr)
bubble_sort.sort()
bubble_sort.print_array()