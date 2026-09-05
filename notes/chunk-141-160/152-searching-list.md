# Video 152 — Collections Part-17: Searching Elements of List, `reverse()` & `reverseOrder()`

## Video info

## Session overview

This is Collections Part-17 — the second of three utility-method sessions on the Collections class (after sort, before additional utilities). Durga Sir covers searching, reversing, and the easy-to-confuse `reverse()` vs `reverseOrder()` distinction.

What this lecture covers:

- Recap: Collections as a utility class; last session = sort()
- Collections.binarySearch() — searching for an object in a List (ArrayList, LinkedList, etc.)
- Return type trap: int, not boolean
- Successful search → index; unsuccessful search → insertion point (negative value)
- Mandatory precondition: list must be sorted before calling binarySearch()
- Two overloads: default natural sorting vs customized Comparator sorting
- Six board conclusions (exam-critical)
- Live demo 1: natural-order sort + binary search (CollectionsSearchDemo)
- Live demo 2: comparator sort + binary search (CollectionsSearchDemo1)
- Unsorted-list trap demo (unpredictable results, no exception)
- Missing-comparator trap demo (unpredictable results when list was comparator-sorted)
- Arrays.binarySearch() — same rules in one sentence
- Mathematical result-range formulas for a list of n elements
- Collections.reverse(List) — reverse element order in-place
- Collections.reverseOrder(Comparator) — get a reversed Comparator (not the same as reverse())
Exam mantra: Sort first. Return type is int. Successful = non-negative index. Unsuccessful = negative insertion point. Comparator used at sort time must be passed again at search time. Know reverse() vs reverseOrder() cold.

## 00:04 — Recap: `Collections` utility class & last session

### What is `Collections`?

Collections is a utility class in java.util that defines several static utility methods for collection objects. You do not instantiate it.

### Last session recap

In the previous session (Video 151), Durga Sir covered:

- Collections.sort(List l) — sort according to default natural sorting order
- Collections.sort(List l, Comparator c) — sort according to customized sorting order
### This session's topic

Searching elements of List

Use case: "I have an ArrayList (or LinkedList). I want to search whether a particular target object is present in that list or not."

Internally, the search utility uses the binary search algorithm — the method name itself is binarySearch.

## 00:49 — Binary search algorithm: the mandatory sorted-list rule

### The golden rule (copy for exam)

If you want to apply the binary search algorithm, the list must be sorted first.

Workflow:

- First → sort the list (Collections.sort(...))
- Then → apply binary search (Collections.binarySearch(...))
This is the standard binary-search rule from data structures, and it applies exactly here.

### Why sorting matters (conceptual proof from the board)

Assume a sorted list: [A, K, M, J, a]. If you search for 'j' (not present), you can logically say: "'j' should be placed after the first `'A'` and before `'K'`" — that position is meaningful only because the list is sorted.

If the list is not sorted — e.g. original insertion order [J, A, M, K, a] — you cannot determine where 'j' should go. You cannot say it belongs after 'A' or before 'K' without a sort order.

Therefore: before calling `binarySearch()`, the list must be sorted.

### What happens if you skip sorting?

- No compile-time error
- No runtime exception
- You get unpredictable / unexpected results
Durga Sir demonstrates this live: even when 'J' is present in an unsorted list, binarySearch may return -5 instead of the correct index 0. Never trust output on an unsorted list.

## 01:51 — `Collections.binarySearch()`: method signature basics

### Access modifiers

```java
public static int binarySearch(List l, Object target)
```

- Public — callable from anywhere
- Static — call via class name: Collections.binarySearch(...)
- Return type: `int` — NOT `boolean`
### The return-type trap (star this)

Most students assume: "Can you search whether this object is available or not? → return type must be `boolean` (true/false)."

Wrong. The return type is `int`.

Board note: Successful search returns index. Unsuccessful search returns insertion point (as a negative value).

## 02:28 — Worked example: index vs insertion point (natural sort)

### Setup

ArrayList l = new ArrayList();
l.add("J");
l.add("A");
l.add("M");
l.add("K");
l.add("a");
System.out.println(l);           // [J, A, M, K, a]  — insertion order preserved
Collections.sort(l);             // sort by natural order
System.out.println(l);           // [A, K, M, J, a]

### After sorting — index map

Insertion points (negative, for elements not in list — where you could insert):

### Search 1 — successful: `"J"` (capital J, present)

Collections.binarySearch(l, "J");   // returns 3

'J' is at index 3 → successful search → returns 3.

### Search 2 — unsuccessful: `"j"` (lowercase j, not present)

Collections.binarySearch(l, "J");   // 3  — successful (capital J exists)
Collections.binarySearch(l, "j");   // -2 — unsuccessful (lowercase j absent)

In sorted order [A, K, M, J, a], lowercase 'j' would be placed after `'A'` and before `'K'` — that slot corresponds to insertion point −2.

### Why insertion points are negative

If unsuccessful search returned a positive number like 1, students might confuse it with a successful search at index 1. Negative values eliminate that ambiguity.

### What is "insertion point"?

Insertion point = the location in the sorted list where you can place (insert) the target element while preserving sort order.

- It does not mean you must call add() — it tells you where the element would belong.
- For 'j': after 'A', before 'K' → insertion point −2.
## 08:24 — Two `binarySearch` overloads

The Collections class defines two binary search methods:

### Method 1 — list sorted by default natural sorting order

```java
public static int binarySearch(List l, Object target)
```

Use when: the list was sorted with Collections.sort(l) (no comparator) — i.e. default natural sorting order.

### Method 2 — list sorted by customized sorting order

```java
public static int binarySearch(List l, Object target, Comparator c)
```

Use when: the list was sorted with Collections.sort(l, comparator) — i.e. customized sorting order via Comparator.

### Critical matching rule

At search time, you must pass the same Comparator that was used at sort time. Otherwise → unpredictable results (no exception).

## 12:53 — Six board conclusions (exam-critical — memorize all six)

Durga Sir writes six conclusions on the board. Copy all six:

### Conclusion 1 — Algorithm used internally

The above search methods internally will use binary search algorithm.

Binary search is the standard searching algorithm for sorted collections.

### Conclusion 2 — Successful search

Successful search returns index (non-negative integer: 0, 1, 2, …).

### Conclusion 3 — Unsuccessful search

Unsuccessful search returns insertion point (negative integer: −1, −2, −3, …).

### Conclusion 4 — Definition of insertion point

Insertion point is the location where we can place the target element in the sorted list.

### Conclusion 5 — List must be sorted

Before calling binarySearch() method, compulsory the list should be sorted. Otherwise we will get unpredictable results (no compile-time or runtime error).

### Conclusion 6 — Comparator must match at search time

If the list is sorted according to Comparator, then at the time of search operation also we must pass the same Comparator object. Otherwise we will get unpredictable results.

## 18:34 — Example 1: `CollectionsSearchDemo` (default natural sorting)

### Full program

```java
import java.util.*;

public class CollectionsSearchDemo {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        l.add("J");
        l.add("A");
        l.add("M");
        l.add("K");
        l.add("a");

        System.out.println("Before sorting: " + l);
        // Output: [J, A, M, K, a]

        Collections.sort(l);
        System.out.println("After sorting:  " + l);
        // Output: [A, K, M, J, a]

        System.out.println(Collections.binarySearch(l, "J"));
        // Successful search → 3

        System.out.println(Collections.binarySearch(l, "j"));
        // Unsuccessful search → -2
    }
}
```

### Board diagram (draw beside the code)

After sort: A  K  M  J  a

### Compile & run output

Before sorting: [J, A, M, K, a]
After sorting:  [A, K, M, J, a]
3
-2

### Trap demo: search without sorting

Comment out Collections.sort(l) and call binarySearch anyway:

```java
// Collections.sort(l);   // commented out — list stays [J, A, M, K, a]
System.out.println(Collections.binarySearch(l, "J"));   // unpredictable: -5
System.out.println(Collections.binarySearch(l, "j"));   // unpredictable: -1
```

Even though 'J' exists at index 0 in the unsorted list, binary search returns −5 — completely wrong. Proves Conclusion 5.

## 28:37 — Example 2: `CollectionsSearchDemo1` (Comparator / descending sort)

### Comparator for descending order

```java
class MyComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Integer I1 = (Integer) obj1;
        Integer I2 = (Integer) obj2;
        return I2.compareTo(I1);   // descending order
    }
}
```

I2.compareTo(I1) = reverse of default natural (ascending) order = descending.

### Full program

```java
import java.util.*;

class MyComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Integer I1 = (Integer) obj1;
        Integer I2 = (Integer) obj2;
        return I2.compareTo(I1);
    }
}

public class CollectionsSearchDemo1 {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        l.add(15);
        l.add(0);
        l.add(20);
        l.add(10);
        l.add(5);

        System.out.println("Before sorting: " + l);
        // [15, 0, 20, 10, 5]

        Collections.sort(l, new MyComparator());
        System.out.println("After sorting:  " + l);
        // [20, 15, 10, 5, 0]  — descending (customized)

        System.out.println(Collections.binarySearch(l, 10, new MyComparator()));
        // Successful → 2

        System.out.println(Collections.binarySearch(l, 13, new MyComparator()));
        // Unsuccessful → -3

        System.out.println(Collections.binarySearch(l, 17));
        // NO comparator passed → UNPREDICTABLE (e.g. -6)

        // Correct call for 17:
        // Collections.binarySearch(l, 17, new MyComparator());  → -2
    }
}
```

### Trace: before and after sort

### Index / insertion-point map (after descending sort)

### Search results explained

### Live run output (from the video)

Before sorting: [15, 0, 20, 10, 5]
After sorting:  [20, 15, 10, 5, 0]
2
-3
-6

Expected for 17 with Comparator: −2. Without Comparator: −6 (wrong) — proves Conclusion 6.

### Board summary for Example 2

Before sorting:  15  0  20  10  5
After sorting:   20  15  10  5   0

binarySearch(l, 10, new MyComparator())  →  2
binarySearch(l, 13, new MyComparator())  → -3
binarySearch(l, 17)                        → unpredictable (must pass Comparator)

## 41:54 — `Arrays.binarySearch()` — same rules

Even in the `Arrays` class, binary search exists (Arrays.binarySearch(...)).

Durga Sir's one-line rule for the exam:

All rules of `Arrays` class `binarySearch()` method are exactly the same as `Collections` class `binarySearch()` method.

He will not re-explain — if you master this session, Arrays.binarySearch is free marks.

Same rules apply:

- Array must be sorted first
- Return type is int
- Successful → index; unsuccessful → insertion point
- Two overloads: natural order vs Comparator
- Comparator at search must match Comparator at sort
## 42:27 — Result ranges for a list of n elements (exam math)

Durga Sir derives formulas — may be asked directly in the exam.

### Example: list of 3 elements

List (sorted): [A, K, J] (3 elements, indices 0–2)

Note: write unsuccessful range as −4 to −1 (not −1 to −4) because −4 < −1.

Searching for 'a' (not present) after 'J' → insertion point −4 (after last element).

### General formulas — list of **n** elements

### Board note (copy exactly)

For the list of n elements, in the case of binarySearch() method:

1. Successful search result range: 0 to n − 1

2. Unsuccessful search result range: −(n + 1) to −1

3. Total result range: −(n + 1) to (n − 1)

### Worked check (n = 3)

- Successful: 0 to 2 ✓
- Unsuccessful: −(3+1) to −1 = −4 to −1 ✓
- Total: −4 to 2 ✓
## 49:44 — `Collections.reverse(List l)` — reversing elements of a List

### Third utility in this block

After sorting and searching, the third topic: reversing elements of a List.

### Method signature

```java
public static void reverse(List l)
```

- Public static void
- Reverses the order of elements in the given list in-place
- Returns nothing (void) — the original list object is modified
### Board theory

Collections class defines the following reverse method to reverse elements of List.

### Example program

```java
import java.util.*;

public class CollectionsReverseDemo {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        l.add(15);
        l.add(0);
        l.add(20);
        l.add(10);
        l.add(5);

        System.out.println("Before reverse: " + l);
        // [15, 0, 20, 10, 5]

        Collections.reverse(l);
        System.out.println("After reverse:  " + l);
        // [5, 10, 20, 0, 15]
    }
}
```

### Critical clarification (common mistake)

`reverse()` reverses the ORDER of elements — NOT the elements themselves.

- 15 stays the integer 15 — it does not become 51
- Only the position changes: first element becomes last, last becomes first
- Order reversal ≠ element reversal (digit reversal)
## 54:23 — `reverse()` vs `reverseOrder()` — do NOT confuse

### Two different methods — most common confusion point

### `Collections.reverseOrder(Comparator c)`

Comparator c1 = Collections.reverseOrder(c);

- Input: a Comparator c (e.g. ascending order)
- Output: a new Comparator c1 that produces the opposite order (e.g. descending)
- Return type: `Comparator`
### Analogy from the board

We can use reverseOrder() method to get a reversed Comparator.

### When to use `reverseOrder()`

- You already have a Comparator for ascending order
- You need a Comparator for descending order
- Instead of writing a new Comparator class, call Collections.reverseOrder(existingComparator)
### Example

Comparator ascending = /* some ascending comparator */;
Comparator descending = Collections.reverseOrder(ascending);
// c  → ascending
// c1 → descending

### Board summary (copy for exam)

Don't get confused — exam may ask: "What is the difference between `reverse()` and `reverseOrder()`?"

## 59:11 — Session wrap-up: three utilities covered

This lecture completes three Collections class utilities:

## Quick reference tables

### `binarySearch` decision tree

Is the list sorted?
├── NO  → unpredictable results (sort first!)
└── YES → How was it sorted?
          ├── Collections.sort(l)           → binarySearch(l, target)
          └── Collections.sort(l, comp)     → binarySearch(l, target, comp)
                                              (SAME comp required)

### Return value interpretation

### Java API encoding (official — beyond board notation)

Standard Java encodes insertion point as:

return -(insertionPoint) - 1

Durga Sir teaches insertion points directly as −1, −2, −3, … on the board. For the OCJP/SCJP exam, follow Sir's board conclusions and worked examples.

### `reverse` vs `reverseOrder` at a glance

| | reverse(List) | reverseOrder(Comparator) |

|--|----------------|---------------------------|

| Argument | List | Comparator |

| Return type | void | Comparator |

| Effect | Reverses list element order in-place | Returns opposite-order Comparator |

| Modifies original? | Yes (the List) | No (returns new Comparator) |

## Exam traps checklist

- Return type is `int`, not boolean
- List must be sorted before search — no exception thrown if unsorted
- Same Comparator at sort and search when using customized order
- Unsuccessful search returns negative insertion point, not -1 only (range: −(n+1) to −1)
- reverse() = flip list order; `reverseOrder()` = flip Comparator logic — completely different
- Arrays.binarySearch follows identical rules to Collections.binarySearch
- Successful index range: 0 to n−1; total range: −(n+1) to n−1
## Programs to practice (from the video)

## What's next

- Additional Collections utility methods in upcoming sessions
- Arrays.binarySearch() — same rules, no separate lecture needed if this session is clear
- reverseOrder() will be used when combining sorting with descending/custom comparators

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Collections Part-17 \ | \ | searching elements of list |
| URL | https://www.youtube.com/watch?v=bQkR6N8OUks |  |  |
| Duration | 59m 35s |  |  |
| Position | Video 152 of 203 in the Durga Sir OCJP/SCJP playlist |  |  |
| Prerequisite | Video 151 covered Collections.sort() — sorting elements of a List using default natural sorting order and customized sorting via Comparator. Earlier sessions covered the Comparator interface, compare() return-value contract, and the full Collections Framework hierarchy. |  |  |

| Situation | Return value | Meaning |
|---|---|---|
| Successful search — target found | Non-negative index (0, 1, 2, …) | The index where the element exists in the list |
| Unsuccessful search — target not found | Negative insertion point (−1, −2, −3, …) | The encoded position where the target could be inserted to maintain sorted order |

| Index | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Element | A | K | M | J | a |

| Position | Before index 0 | Before index 1 | Before index 2 | Before index 3 | Before index 4 | After index 4 |
|---|---|---|---|---|---|---|
| Insertion point | −1 | −2 | −3 | −4 | −5 | −6 |

| How list was sorted | Which binarySearch to call |
|---|---|
| Collections.sort(l) | Collections.binarySearch(l, target) |
| Collections.sort(l, c) | Collections.binarySearch(l, target, c) — same Comparator `c` |

| Label | Values |
|---|---|
| Index | 0, 1, 2, 3, 4 |
| Insertion point | −1, −2, −3, −4, −5, −6 |

| Stage | List contents |
|---|---|
| Before sort (insertion order) | 15, 0, 20, 10, 5 |
| After sort(l, new MyComparator()) (descending) | 20, 15, 10, 5, 0 |

| Index | 0 | 1 | 2 | 3 | 4 |  |
|---|---|---|---|---|---|---|
| Element | 20 | 15 | 10 | 5 | 0 |  |
| Insertion point | −1 | −2 | −3 | −4 | −5 | −6 |

| Call | Result | Explanation |
|---|---|---|
| binarySearch(l, 10, new MyComparator()) | 2 | 10 present at index 2 — successful |
| binarySearch(l, 13, new MyComparator()) | −3 | 13 absent; in descending order, 13 goes after 15 (before 10) → insertion point −3 |
| binarySearch(l, 17) — no Comparator | −6 (wrong) | List sorted by Comparator but search uses natural order → unpredictable |
| binarySearch(l, 17, new MyComparator()) | −2 | 17 goes after 20 in descending order → insertion point −2 — predictable |

| Category | Range |
|---|---|
| Successful search result range | 0 to 2 (indices 0, 1, or 2) |
| Unsuccessful search result range | −4 to −1 (−4 is smallest, −1 is largest among negatives) |
| Total result range (success or failure) | −4 to 2 |

| Category | Formula | Example (n = 5) |
|---|---|---|
| Successful search result range | 0 to (n − 1) | 0 to 4 |
| Unsuccessful search result range | −(n + 1) to −1 | −6 to −1 |
| Total result range | −(n + 1) to (n − 1) | −6 to 4 |

| Before | After Collections.reverse(l) |
|---|---|
| 15, 0, 20, 10, 5 | 5, 10, 20, 0, 15 |

| Method | Purpose |
|---|---|
| Collections.reverse(List l) | Reverse the order of elements in an existing List (in-place) |
| Collections.reverseOrder(Comparator c) | Get a reversed Comparator object (returns Comparator) |

| Comparator passed in (c) | Comparator returned (c1) |
|---|---|
| Ascending order | Descending order |
| Alphabetical order | Reverse alphabetical order |

| Method | Use |
|---|---|
| `reverse(List l)` | Reverse order of elements of a List |
| `reverseOrder(Comparator c)` | Get a reversed Comparator |

| # | Utility | Method(s) |
|---|---|---|
| 1 | Sorting (previous session) | Collections.sort(l), Collections.sort(l, c) |
| 2 | Searching (this session) | Collections.binarySearch(l, target), Collections.binarySearch(l, target, c) |
| 3 | Reversing (this session) | Collections.reverse(l), Collections.reverseOrder(c) |

| Return value | Meaning | Example |
|---|---|---|
| >= 0 | Successful — element found at this index | 3 → element at index 3 |
| < 0 | Unsuccessful — insertion point encoded as negative | -2 → would insert before index 1 |

| Class | File purpose |
|---|---|
| CollectionsSearchDemo | Natural sort + binary search; unsorted trap |
| CollectionsSearchDemo1 | Comparator (descending) sort + binary search; missing-comparator trap |
| CollectionsReverseDemo | Collections.reverse() in-place order flip |
