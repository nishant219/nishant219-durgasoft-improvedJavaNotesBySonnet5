# Video 153 — Collections Part-18: `java.util.Arrays` Utility Class

## Video info

## Session overview

After `Collections` (Video 151–152: sort + binary search on List), this session introduces the second major utility class in the Collections Framework: `Arrays`.

Why `Arrays` exists: Collections give ready-made methods for common tasks (sort, search, etc.). With raw arrays, the programmer would normally write sorting/search logic manually. Most developers are unaware that `Arrays` fills that gap with predefined methods — the same philosophy as Collections.

Three utilities covered in this video:

- Sorting — sort elements of an array
- Searching — binary search in a sorted array
- Conversion — Arrays.asList() (array → list view)
Prerequisites from earlier videos:

- Default natural sorting order vs customized sorting via Comparator (Videos 144+)
- Collections.sort() and Collections.binarySearch() rules (Videos 151–152)
Exam mantra: Concept volume is small; documentation/traps volume is large. Master the three method groups, the primitive-vs-object restrictions, binary-search preconditions, and the three asList() conclusions — especially `UnsupportedOperationException` and `ArrayStoreException`.

## 00:05 — Introduction: Arrays vs Collections

### Collections advantage recap

For collections, ready-made method support exists for almost every requirement — the programmer uses those methods, not implements them.

For arrays, historically the programmer had to write code for:

- Searching an element
- Inserting/maintaining elements in sorted order
- Other array manipulations
`Arrays` class = utility class that defines several utility methods for arrays (primitive + object type).

### Board note (copy exactly)

`Arrays` class is a utility class to define several utility methods for arrays or array objects.

### Parallel with Collections

Both live in `java.util`.

## 03:06 — Utility 1: Sorting Elements of Array

### Board heading

Sorting elements of array

### How many `sort` methods?

Three overloaded sort methods:

### Board note (copy exactly)

`Arrays` class defines the following sort methods to sort elements of primitive and object type arrays.

Method prototypes (as written on board):

```java
public static void sort(primitive[] p);           // natural order
public static void sort(Object[] a);              // natural order
public static void sort(Object[] a, Comparator c); // customized order
```

### Natural sorting examples

### Critical exam rule — primitive vs object arrays

Board note (copy exactly):

We can sort primitive arrays only based on default natural sorting order.

Whereas we can sort object arrays either based on default natural sorting order OR based on customized sorting order.

Why no Comparator for primitives: Comparator interface defines compare(Object o1, Object o2). Customized sorting needs object arguments → applicable only to object type arrays.

## 09:12 — Demo 1: `ArraySortDemo` — All Three Sort Methods

### Imports

```java
import java.util.Arrays;
import java.util.Comparator;
```

Arrays is in `java.util` (same package as Comparator, Collections, List, etc.).

### Part A — Primitive array sort

int[] a = {10, 5, 20, 11, 6};

// Print before sort — use enhanced for-loop (NOT System.out.println(a))
for (int i1 : a) {
    System.out.println(i1);
}
// Output (one per line): 10, 5, 20, 11, 6

Arrays.sort(a);   // sort according to default natural sorting order

System.out.println("After sorting:");
for (int i1 : a) {
    System.out.println(i1);
}
// Output: 5, 6, 10, 11, 20

Printing arrays: You cannot use System.out.println(a) for meaningful element output (prints something like [I@hashcode). Use enhanced for-each loop to print each element.

Compile & run: javac ArraySortDemo.java → java ArraySortDemo

### Part B — Object array sort (natural order)

String[] s = {"a", "j", "b"};

System.out.println("Object array before sorting:");
for (String x : s) System.out.println(x);
// a, j, b

Arrays.sort(s);   // default natural sorting → alphabetical for String

System.out.println("Object array after sorting:");
for (String x : s) System.out.println(x);
// a, b, j

### Part C — Object array sort (customized / reverse alphabetical)

```java
Arrays.sort(s, new MyComparator());

// MyComparator — reverse of natural alphabetical order
class MyComparator implements Comparator<String> {
    public int compare(String s1, String s2) {
        return s2.compareTo(s1);   // reverse: s2 vs s1 instead of s1 vs s2
    }
}
```

Interpretation: return s2.compareTo(s1) reverses the default String order → reverse alphabetical.

### Sort demo summary table

## 21:29 — Utility 2: Searching Elements of Array (Binary Search)

### Board heading

Searching elements of array

### How many `binarySearch` methods?

Three — mirroring the three sort overloads:

### Board note (copy exactly)

`Arrays` class defines the following binary search methods.

Method prototypes:

```java
public static int binarySearch(primitive[] p, primitive target);
public static int binarySearch(Object[] a, Object target);
public static int binarySearch(Object[] a, Object target, Comparator c);
```

### Which search method when?

Primitive arrays: Only one search method needed (only natural sorting exists for primitives).

## 26:58 — Rules: Same as `Collections.binarySearch()`

### Board note (copy exactly)

All rules of `Arrays` class binary search methods are exactly same as `Collections` class binary search methods.

From Video 152 (Collections.binarySearch on List):

### Index vs insertion point (classroom diagram)

For sorted array with indices 0, 1, 2, 3, 4:

Return value formula (unsuccessful):

return = -(insertionPoint) - 1

Example: insertion point = 5 → return = -(5) - 1 = -6?

Wait: if insertion point is 5, return is -6. Transcript uses insertion point 5 → return -5 for target 14 in [5,6,10,11,20]:

- 14 belongs between 11 (index 3) and 20 (index 4)
- Insertion point = 4 (would insert at index 4, pushing 20 right)
- Return = -(4) - 1 = -5 ✓
## 28:10 — Demo 2: `ArraySearchDemo`

### Part A — Primitive `int[]` search

int[] a = {10, 5, 20, 11, 6};
Arrays.sort(a);   // → {5, 6, 10, 11, 20}

// Index map after sort:
// index:  0  1   2   3   4
// value:  5  6  10  11  20

System.out.println(Arrays.binarySearch(a, 6));   // 1  (found at index 1)
System.out.println(Arrays.binarySearch(a, 14));  // -5 (14 would insert at index 4)

### Part B — String array (natural sort)

String[] s = {"a", "j", "b"};
Arrays.sort(s);   // → {"a", "b", "j"}

// index:  0   1   2
// value:  a   b   j

System.out.println(Arrays.binarySearch(s, "j"));  // 2
System.out.println(Arrays.binarySearch(s, "s"));  // -3 (classroom trace: s after b, before j)

Also demonstrated in class:

System.out.println(Arrays.binarySearch(s, "z"));  // 2 — "z" at index 2? 
// Sir states z available at second index in one trace — verify: after sort a,b,j → z not present, would be index 3 → -4
// Follow classroom output: j search → 2; capital S search → -3 in natural-order section

(Take the exact numeric outputs from Sir's executed program as exam reference: `1, -5` for int; `2, -3` for String natural order.)

### Part C — String array (Comparator / reverse sort)

Arrays.sort(s, new MyComparator());   // → {"j", "b", "a"}

// index:  0   1   2
// value:  j   b   a

System.out.println(Arrays.binarySearch(s, "j", new MyComparator()));  // 0
System.out.println(Arrays.binarySearch(s, "S", new MyComparator()));  // -2
System.out.println(Arrays.binarySearch(s, "n"));  // UNPREDICTABLE — no Comparator passed!

### Exam trap — Comparator mismatch

If the array is sorted according to a Comparator, at search time you must pass the same Comparator object. If you omit it, the result is unpredictable (not a clean exception — wrong/garbage index).

### Static import note

In the demo code, Sir sometimes writes Arrays.binarySearch(...) and sometimes just binarySearch(...) after:

```java
import static java.util.Arrays.*;
```

With static import, static members can be called without class name.

### Search demo program output (executed)

1
-5
2
-3
0
-2
(unpredictable for last case)

## 44:48 — Utility 3: Conversion — Array to List (`Arrays.asList()`)

### Board heading

Conversion of array to list

### Collection → array (recap — opposite direction)

Naming matters: Collection uses `toArray()` (actual conversion). Array uses `asList()` — the word "as" is intentional.

### Method signature

```java
public static List asList(Object... a)
// equivalently: public static <T> List<T> asList(T... a)
```

- public static method
- Return type: `List`
- Method name: `asList`
- Argument: object array (varargs)
### Why `asList` and NOT `toList`?

Board note (copy exactly):

Strictly speaking, this method won't create an independent list object. For the existing array we are getting list view.

Database analogy (Durga Sir):

- One table → many views possible
- One array → you get a List view of that same array
- NOT a separate copy / new List object
String[] s = {"a", "j", "b"};
List l = Arrays.asList(s);

// Underlying object = SAME array
// l is just a List-flavoured window into s

## 52:07 — Three Conclusions of `Arrays.asList()` (MUST KNOW FOR EXAM)

### Conclusion 1 — List view, not independent list

`Arrays.asList()` does NOT create a new List object. It returns a list VIEW of the existing array.

### Conclusion 2 — Changes reflect both ways (shared backing store)

Board notes:

By using array reference, if we perform any change, automatically that change will be reflected to the list.

Similarly, by using list reference, if we perform any change, automatically that change will be reflected to the array.

Both references point to the same underlying array object.

Example:

String[] s = {"a", "j", "b"};
List l = Arrays.asList(s);

s[0] = "k";                    // change via array reference
System.out.println(l);         // [k, j, b] — list reflects change

l.set(1, "l");                 // change via list reference (replacement OK)
for (String s1 : s) System.out.println(s1);  // k, l, b — array reflects change

### Conclusion 3 — Size-varying operations → `UnsupportedOperationException`

Contradiction (by design):

By using list reference, we can't perform any operation which varies the size. Otherwise we get `RuntimeException: UnsupportedOperationException`.

Why: Internally the object is still an array (fixed size). Array property dominates even though you hold a List reference.

```java
// l.add("d");      // UnsupportedOperationException
// l.remove(2);     // UnsupportedOperationException
l.set(1, "n");      // OK — replacement, no size change
```

### Conclusion 4 — Heterogeneous replacement → `ArrayStoreException`

Second contradiction:

By using list reference, we are not allowed to replace with heterogeneous objects. Otherwise `ArrayStoreException` (runtime exception).

Example — String array view:

String[] s = {"a", "b", "c"};
List l = Arrays.asList(s);

// l.set(1, new Integer(10));   // ArrayStoreException
// Internally: String[] — cannot store Integer at index 1

Memory aid: Array Store → ArrayStoreException (wrong type for array component type).

## 65:54 — Demo 3: `ArrayAsListDemo` (Full Program)

```java
import java.util.*;

public class ArrayAsListDemo {
    public static void main(String[] args) {
        String[] s = {"a", "b", "c"};
        List l = Arrays.asList(s);

        System.out.println(l);       // [a, b, c]

        // --- Conclusion 2: array change reflects to list ---
        s[0] = "k";
        System.out.println(l);       // [k, b, c]

        // --- Conclusion 2: list change reflects to array ---
        l.set(1, "l");
        for (String s1 : s)
            System.out.println(s1);  // k, l, c

        // --- Conclusion 3: size-varying ops ---
        // l.add("d");               // UnsupportedOperationException
        // l.remove(2);              // UnsupportedOperationException

        // --- Conclusion 4: heterogeneous set ---
        // l.set(1, new Integer(10)); // ArrayStoreException
    }
}
```

### Expected trace

## Master comparison tables

### `Arrays.sort()` overloads

### `Arrays.binarySearch()` overloads

### Binary search return values

### `Arrays.asList()` — operation validity

### `Collections` vs `Arrays` (this playlist)

## OCJP / SCJP exam traps checklist

- `Arrays` is in `java.util`, not java.lang.
- Primitive arrays: only sort(arr) — no Comparator overload.
- Must sort before binarySearch — same rule as Collections.
- Successful search → non-negative index; failed → negative encoded insertion point.
- Comparator used at sort MUST be passed at search — else unpredictable (favorite trick question).
- `asList` ≠ new ArrayList — it's a fixed-size list view backed by the array.
- `add`/`remove` on asList view → `UnsupportedOperationException` (not ArrayIndexOutOfBoundsException).
- `set` with wrong element type → `ArrayStoreException` (not ClassCastException at set time for arrays).
- Changes via array ref OR list ref are visible both ways — shared mutability.
- Do not confuse: Collection.toArray() (creates array from collection) vs Arrays.asList() (view, not copy).
## Session closing

- This video completes the two utility classes of the Collections Framework block: `Collections` + `Arrays`.
- Sorting and searching on arrays mirror List operations but use `Arrays` static methods.
- The `asList()` section is the highest-value exam content — three conclusions (view, bidirectional mutation, two exception types).
- Sir's closing: "Concept is very less but documentation is more" — write the method signatures, trace one sort/search example, and memorize the asList() exception matrix.
End of Video 153 study notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |
|---|---|---|
| Position | 153 of 203 |  |
| Playlist | Core Java With OCJP/SCJP |  |
| Title | Collections Part-18 \ | Arrays |
| Instructor | Durga Sir |  |
| Duration | 1h 10m 35s |  |
| Video ID | 2kn8rgNJf3U |  |
| URL | https://www.youtube.com/watch?v=2kn8rgNJf3U |  |
| Notes source | YouTube auto-captions |  |

| Utility class | Package | Defines utility methods for |
|---|---|---|
| Collections | java.util | Collection objects (List, Set, Map wrappers, etc.) |
| Arrays | java.util | Array objects (primitive arrays + object arrays) |

| Class | Role |
|---|---|
| Collections | Utility methods for collection objects |
| Arrays | Utility methods for array objects |

| # | Method signature (conceptual) | Applies to | Sorting order |
|---|---|---|---|
| 1 | public static void sort(primitive[] p) | Any primitive array (int[], char[], byte[], …) | Default natural sorting order only |
| 2 | public static void sort(Object[] a) | Any object array (String[], Student[], …) | Default natural sorting order |
| 3 | public static void sort(Object[] a, Comparator c) | Object arrays only | Customized sorting order via Comparator |

| Array type | Default natural sorting order |
|---|---|
| int[] | Ascending numeric order |
| char[] | Alphabetical order |
| String[] | Lexicographical (dictionary) order via compareTo() |

| Array kind | sort(arr) | sort(arr, comparator) |
|---|---|---|
| Primitive (int[], char[], …) | ✅ Yes — natural only | ❌ Not available — Comparator.compare() takes objects, not primitives |
| Object (String[], custom types, …) | ✅ Yes — natural | ✅ Yes — customized |

| Stage | int[] a content |
|---|---|
| Before sorting | 10, 5, 20, 11, 6 |
| After Arrays.sort(a) | 5, 6, 10, 11, 20 (ascending) |

| Stage | String[] s |
|---|---|
| Before | a, j, b |
| After natural sort | a, b, j |

| Stage | String[] s |
|---|---|
| Original | a, j, b |
| After reverse Comparator sort | j, b, a |

| Method used | Input | Output |
|---|---|---|
| Arrays.sort(a) | {10,5,20,11,6} | {5,6,10,11,20} |
| Arrays.sort(s) | {"a","j","b"} | {"a","b","j"} |
| Arrays.sort(s, new MyComparator()) | {"a","j","b"} | {"j","b","a"} |

| # | Method signature (conceptual) | When to use |
|---|---|---|
| 1 | public static int binarySearch(primitive[] p, primitive target) | Search in sorted primitive array |
| 2 | public static int binarySearch(Object[] a, Object target) | Array sorted by natural order |
| 3 | public static int binarySearch(Object[] a, Object target, Comparator c) | Array sorted by customized order (same Comparator) |

| How array was sorted | Search method to call |
|---|---|
| Primitive array (always natural) | binarySearch(primitive[], primitive target) |
| Object array — natural sort (Arrays.sort(a)) | binarySearch(Object[], Object target) |
| Object array — Comparator sort (Arrays.sort(a, c)) | binarySearch(Object[], Object target, Comparator c) — same Comparator object |

| Rule | Meaning |
|---|---|
| 1. Sort first | Before calling binarySearch, the array must be sorted (using the same ordering you will search with) |
| 2. Successful search | Returns index (0-based) where element is found |
| 3. Unsuccessful search | Returns insertion point encoded as `-(insertionPoint) - 1` |
| 4. Comparator consistency | If sorted with Comparator, search must pass the same Comparator; otherwise → unpredictable result |
| 5. Algorithm | Internally uses binary search algorithm — requires sorted data |

| Concept | Values |
|---|---|
| Index | 0, 1, 2, 3, 4 |
| Insertion point | 0, 1, 2, 3, 4, 5 (one more slot — where element would go) |

| Call | Target | Found? | Return | Explanation |
|---|---|---|---|---|
| binarySearch(a, 6) | 6 | Yes | 1 | 6 is at index 1 |
| binarySearch(a, 14) | 14 | No | -5 | 14 fits after 11; insertion point 4 → -(4)-1 = -5 |

| Call | Return | Explanation |
|---|---|---|
| binarySearch(s, "j") | 2 | "j" at index 2 |
| binarySearch(s, "s") | -3 | "s" not present; insertion point 2 per Sir's trace |

| Call | Comparator passed? | Return | Explanation |
|---|---|---|---|
| binarySearch(s, "j", new MyComparator()) | ✅ Same as sort | 0 | "j" at index 0 in reverse-sorted array |
| binarySearch(s, "S", new MyComparator()) | ✅ Same | -2 | "S" would come after "J" in reverse order |
| binarySearch(s, "n") | ❌ Missing | Unpredictable | Array sorted with Comparator but search uses natural order |

| Direction | API | Method |
|---|---|---|
| Collection → Array | Collection.toArray() | Creates equivalent object array |
| Array → List | Arrays.asList() | Not toList() |

| DB concept | Array equivalent |
|---|---|
| Table (physical storage) | Array (underlying real object) |
| View (logical presentation of same data) | List reference from asList() |

| Operation via | Code | Effect on other view |
|---|---|---|
| Array ref | s[0] = "k" | List shows [k, j, b] |
| List ref | l.set(1, "l") | Array becomes k, l, b |

| Feature | Array | Collection/List |
|---|---|---|
| Size | Fixed | Growable |
| Underlying object in asList() | Array dominates | List API exposed but backed by fixed array |

| Operation | Changes size? | Valid on asList() view? |
|---|---|---|
| l.add("m") | ✅ Yes (increase) | ❌ UnsupportedOperationException |
| l.remove(1) | ✅ Yes (decrease) | ❌ UnsupportedOperationException |
| l.set(1, "n") | ❌ No (replacement only) | ✅ Valid — size unchanged |

| Feature | Array | List (general) |
|---|---|---|
| Element types | Homogeneous (declared component type) | Heterogeneous (can hold different object types) |

| Operation | Exception |
|---|---|
| l.set(1, new Integer(10)) on String[] view | `ArrayStoreException` |
| l.add(...) / l.remove(...) | `UnsupportedOperationException` |

| Step | Code | Output / result |
|---|---|---|
| Initial | Arrays.asList(s) | [a, b, c] |
| Array change | s[0] = "k" | l → [k, b, c] |
| List change | l.set(1, "l") | array → k, l, c |
| Add attempt | l.add("d") | UnsupportedOperationException |
| Remove attempt | l.remove(2) | UnsupportedOperationException |
| Heterogeneous set | l.set(1, new Integer(10)) | ArrayStoreException |

| Method | Array type | Sort order |
|---|---|---|
| sort(primitive[]) | Primitive | Natural only |
| sort(Object[]) | Object | Natural (Comparable) |
| sort(Object[], Comparator) | Object | Customized |

| Method | Precondition | Comparator at search? |
|---|---|---|
| binarySearch(primitive[], target) | Primitive array sorted (natural) | N/A |
| binarySearch(Object[], target) | Sorted by natural order | No |
| binarySearch(Object[], target, Comparator) | Sorted with same Comparator | Yes — mandatory |

| Outcome | Return type meaning | Example |
|---|---|---|
| Element found | Index ≥ 0 | 6 in {5,6,10,11,20} → 1 |
| Element not found | -(insertionPoint) - 1 | 14 → insertion point 4 → -5 |
| Wrong Comparator / unsorted | Unpredictable | Search without Comparator after Comparator-sort |

| Operation | Size change? | Type check? | Result |
|---|---|---|---|
| get / set (same type) | No | Compatible type | ✅ OK |
| set(index, wrongType) | No | Incompatible | ❌ ArrayStoreException |
| add | Yes | — | ❌ UnsupportedOperationException |
| remove | Yes | — | ❌ UnsupportedOperationException |

| Topic | Collections | Arrays |
|---|---|---|
| Target | List (and other collections) | Arrays |
| Sort | Collections.sort(list) / with Comparator | Arrays.sort(array) / with Comparator |
| Search | Collections.binarySearch(list, key) | Arrays.binarySearch(array, key) |
| To array | collection.toArray() | — |
| To list | — | Arrays.asList(array) → view |
| Search rules | Sort first; index vs insertion point | Identical rules |
