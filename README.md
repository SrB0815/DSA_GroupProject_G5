Data Structures and Algorithms
Binary Search
Let’s take an example:
A = [1, 3, 7, 8, 10, 11, 12, 15, 19, 21, 22, 23, 29, 31, 37]
This list can be visualized as a binary tree (though we don't actually build one):

b0) Let T, R be the tree and its root respectively

         15 (R)
    ____/  \____
   /            \
__8__           _23__
/ \ /
3 11 21 31 / \ / \ / \ /
1 7 10 12 19 22 29 37

Let’s search for e = 27:

b1) Compare e to R: e > 15
→ Move to right subtree. R becomes 23.

b2) Compare e to R: e > 23
→ Move to right subtree. R becomes 31.

b3) Compare e to R: e < 31
→ Move to left subtree. R becomes 29.

b4) Compare e to R: e ≠ 29
→ No subtree remains. Element not found.

Exponential Search
Exponential search is used on sorted arrays.
It begins by checking arr[0], then arr[1], arr[2], arr[4], arr[8]... until the range is found. Then it uses binary search in that sub-range.

Let’s take the same array:
A = [1, 3, 7, 8, 10, 11, 12, 15, 19, 21, 22, 23, 29, 31, 37]
We search for e = 27.

e > arr[0], arr[1], arr[2], ..., arr[8] = 19
→ Keep going:
Check arr[16] → out of bounds
→ Use binary search from index 8 to 14

Binary search proceeds as before. Result: not found.

Quick Sort
Let’s take an array:
A = [12, 8, 19, 3, 7, 1]

Choose the last element as pivot → 1

Step 1: Rearranged: [1, 8, 19, 3, 7, 12]
Left of pivot < 1 → none
Right of pivot > 1 → rest
Now, recursively sort left and right subarrays.

This continues recursively:

Final Sorted Array: [1, 3, 7, 8, 12, 19]

Merge Sort
Let’s take an array:
A = [12, 8, 19, 3, 7, 1]

Step 1: Split
[12, 8, 19] and [3, 7, 1]
Then again → [12], [8], [19] and [3], [7], [1]

Step 2: Merge and sort each part:
[8, 12, 19] and [1, 3, 7]

Step 3: Merge the two sorted parts:
→ [1, 3, 7, 8, 12, 19]

