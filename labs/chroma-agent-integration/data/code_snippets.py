CODE_SNIPPETS_DATA = [
    {
        "id": "code_snippet_1",
        "document": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
""",
        "metadata": {
            "title": "Recursive Factorial Function",
            "language": "python",
            "description": "Calculates the factorial of a non-negative integer recursively."
        }
    },
    {
        "id": "code_snippet_2",
        "document": """
def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        print(a, end=" ")
        a, b = b, a + b
""",
        "metadata": {
            "title": "Fibonacci Sequence Generator",
            "language": "python",
            "description": "Generates the Fibonacci sequence up to n terms."
        }
    },
    {
        "id": "code_snippet_3",
        "document": """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
        "metadata": {
            "title": "Binary Search Algorithm",
            "language": "python",
            "description": "Implements binary search for a sorted list."
        }
    },
    {
        "id": "code_snippet_4",
        "document": """
import os

def list_files_in_directory(path):
    files = []
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            files.append(entry)
    return files
""",
        "metadata": {
            "title": "List Files in Directory",
            "language": "python",
            "description": "Lists all files (excluding subdirectories) in a given directory path."
        }
    },
    {
        "id": "code_snippet_5",
        "document": """
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
""",
        "metadata": {
            "title": "Quicksort Algorithm",
            "language": "python",
            "description": "Implements the Quicksort sorting algorithm."
        }
    }
]
