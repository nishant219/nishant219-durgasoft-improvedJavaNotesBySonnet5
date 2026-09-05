# Video 151 — Collections Part-16: NavigableSet, NavigableMap & Collections.sort()

## Video info

## Session overview

This lecture completes the Java 1.6 Collection Framework enhancements block and begins the `Collections` utility class sorting APIs. Although the video title says NavigableSet, Sir covers three major topics in one session (~70 minutes):

- NavigableSet — why it exists, all navigation methods, full TreeSet demo
- NavigableMap — parallel hierarchy and methods on TreeMap, full demo
- `Collections` class `sort()` methods — default natural sorting + customized sorting with Comparator, two demo programs
Prior session recap (00:04):

- Queue concept completed
- PriorityQueue is the only Queue implementation class required for OCJP/SCJP basic syllabus
- Advanced queue types may appear in advanced collections; not mandatory for exam
What this session covers:

- Java 1.6 version enhancements in Collections Framework — NavigableSet + NavigableMap
- Motivation: gaps in SortedSet navigation (flight-timing airport example)
- NavigableSet hierarchy, theory, and all method signatures with precise return semantics
- floor / lower / ceiling / higher — mathematical floor/ceiling analogy
- pollFirst, pollLast, descendingSet
- Demo 1: NavigableSetDemo with generic TreeSet<Integer>
- NavigableMap — child of SortedMap, implementation = TreeMap
- NavigableMap methods (*Key, poll*Entry, descendingMap) — copy-paste of Set terminology
- Demo 2: NavigableMapDemo with TreeMap<String,String>
- Collections utility class purpose — fills gaps that normal collections cannot
- Two sort() overloads — natural vs customized sorting
- Rules for natural sort: homogeneous + Comparable, no null
- Demo 3: CollectionsSortDemo — natural alphabetical sort on ArrayList
- Demo 4: CollectionsSortDemo2 — reverse alphabetical via Comparator
What continues in next sessions:

- More Collections utility methods (search, reverse, synchronized wrappers, etc.)
- Searching elements of List (Video 152 per playlist index)
Exam mantra: NavigableSet/NavigableMap methods are navigation helpers on already-sorted data. Know the strict vs inclusive boundary difference (lower vs floor, higher vs ceiling). For Collections.sort(List), adding heterogeneous elements is fine — calling sort is what throws ClassCastException.

## 00:04 — Recap: Queue & PriorityQueue done

For SCJP/OCJP basic collections syllabus:

- Queue concept — covered
- PriorityQueue — only implementation class needed at this level
- No other queue types required for exam at basic level
Sir moves to Java 1.6 version enhancements.

## 00:30 — Java 1.6 enhancements in Collections Framework

### Board heading (copy exactly)

As a part of 1.6 version, the following two concepts were introduced in Collection Framework:

1. NavigableSet

2. NavigableMap

Version history reminder (board):

Same pattern as earlier 1.2 → 1.6 upgrades (e.g., Vector/Stack retrofitted to implement List in 1.2).

## 03:02 — Why NavigableSet? The Shamshabad airport example

### Hierarchy placement

Collection (I)
 └── Set (I)
      └── SortedSet (I)        ← 6 methods already covered
           └── NavigableSet (I) ← NEW in 1.6 — fills navigation gaps
                └── TreeSet (C) ← implementation class

### Real-world scenario: flight timings

Sir uses Shamshabad International Airport (Hyderabad) flight departure times stored in a sorted structure:

Question: Is this a SortedSet? Yes — times are unique and naturally sorted.

### What SortedSet CAN answer (6 methods — already covered)

Sir: "Beautiful methods — happily we can use these directly. Where? In SortedSet."

### The GAP SortedSet CANNOT fill

Critical exam questions SortedSet cannot answer:

Sir walks the hierarchy upward:

- Ask SortedSet → "No method with me, boss"
- Ask Set → "Sorry, I can't provide"
- Ask Collection → "Sorry, I can't provide"
Conclusion: Navigation support for before/after boundary queries on a single element was missing. To fill these gaps → NavigableSet introduced in Java 1.6.

### Purpose of NavigableSet (board — must copy)

NavigableSet defines several methods for navigation purposes.

"Before" and "after" = navigation. NavigableSet adds precise boundary-navigation APIs on top of SortedSet.

## 09:03 — NavigableSet answers the gap: floor, lower, ceiling, higher

### Mapping questions to methods

### Flight example answers

- Before 10:00, last flight → lower(10:00) → 09:20
- At or before 10:00, last flight → floor(10:00) → if 10:00 existed it would be 10:00; here 09:20 is highest ≤ 10:00 among {…, 09:20, 10:25, …}
- Strictly after 10:00, first flight → higher(10:00) → 10:25
- At or after 10:00, first flight → ceiling(10:00) → 10:25 (or 10:00 if present)
### floor vs lower — THE critical distinction

Mathematics analogy (Sir's board):

- Floor function and Ceiling function from mathematics
- floor(x) = greatest integer ≤ x
- ceiling(x) = smallest integer ≥ x
- Same intuition applies to NavigableSet elements in sorting order
Memory trick:

- Floor = you can stand on the floor (inclusive ≤)
- Lower = strictly below the floor (exclusive <)
- Ceiling = you can touch the ceiling (inclusive ≥)
- Higher = strictly above the ceiling (exclusive >)
## 11:08 — NavigableSet theory (board)

### Definition

NavigableSet is the child interface of SortedSet.

It defines several methods for navigation purposes.

### Complete hierarchy diagram

Collection (I)
 └── Set (I)
      └── SortedSet (I)
           └── NavigableSet (I)   ← Java 1.6
                └── TreeSet (C)

Important: NavigableSet methods are available on TreeSet objects (and any NavigableSet reference). TreeSet is the implementation class.

## 12:46 — NavigableSet method catalog (complete)

Sir writes all methods on board. These are the methods you must know for OCJP/SCJP:

### Navigation methods (4)

### Mutation + navigation methods (2)

### View method (1)

Note: NavigableSet also inherits all SortedSet methods (first, last, headSet, tailSet, subSet, comparator) plus additional overloads with inclusive flags in the full API — Sir focuses on the core navigation methods above for this lecture.

### Return-value pattern summary

## 21:02 — Demo 1: NavigableSetDemo (TreeSet<Integer>)

### Why TreeSet?

NavigableSet is an interface. Methods are applied on TreeSet object because TreeSet is the implementation class of NavigableSet.

### Generic vs non-generic TreeSet

TreeSet t = new TreeSet();              // non-generic — can add any type
TreeSet<Integer> t = new TreeSet<>();   // generic — only Integer objects

Sir uses generic version in demo for type safety. Generics covered separately — here just observe the syntax.

### Program

```java
import java.util.*;

class NavigableSetDemo {
    public static void main(String[] args) {
        TreeSet<Integer> t = new TreeSet<>();
        t.add(1000);
        t.add(2000);
        t.add(3000);
        t.add(4000);
        t.add(5000);

        System.out.println("Set: " + t);
        // Output: [1000, 2000, 3000, 4000, 5000]

        System.out.println("ceiling(2000): " + t.ceiling(2000));
        // Either 2000 or after 2000 → lowest element ≥ 2000 → 2000

        System.out.println("higher(2000): " + t.higher(2000));
        // Strictly after 2000 → lowest element > 2000 → 3000

        System.out.println("floor(3000): " + t.floor(3000));
        // Either 3000 or before 3000 → highest element ≤ 3000 → 3000

        System.out.println("lower(3000): " + t.lower(3000));
        // Strictly before 3000 → highest element < 3000 → 2000

        System.out.println("pollFirst(): " + t.pollFirst());
        // Remove and return first element → 1000

        System.out.println("pollLast(): " + t.pollLast());
        // Remove and return last element → 5000

        System.out.println("descendingSet: " + t.descendingSet());
        // Reverse order view → [4000, 3000, 2000]

        System.out.println("Original set: " + t);
        // After pollFirst/pollLast → [2000, 3000, 4000]
    }
}
```

### Sorting order used

- Constructor: no-arg → default natural sorting order
- No Comparator passed
- For Integer: natural order = ascending numeric order
### Step-by-step output trace

### Compiled output (Sir's run)

[1000, 2000, 3000, 4000, 5000]
2000
3000
3000
2000
1000
5000
[4000, 3000, 2000]
[2000, 3000, 4000]

Key observation: pollFirst() and pollLast() mutate the original set. descendingSet() returns a view in reverse order but the underlying set after polling is [2000, 3000, 4000].

## 28:58 — NavigableMap (second half of 1.6 enhancements)

Sir: "NavigableMap is very easy — same copy-paste, but instead of Set terminology use Map terminology."

### Hierarchy

Map (I)
 └── SortedMap (I)
      └── NavigableMap (I)   ← Java 1.6
           └── TreeMap (C)

### Theory (board)

NavigableMap is the child interface of SortedMap.

It defines several methods for navigation purposes.

## 33:21 — NavigableMap methods (parallel to NavigableSet)

Because Map stores key-value pairs, methods operate on keys (not values):

Sir: "Same description — copy paste. No extra explanation required."

### Why pollFirstEntry not pollFirstKey?

"Because only key you can't remove — entry (key + value together) must be removed."

## 35:52 — Demo 2: NavigableMapDemo (TreeMap<String,String>)

### Program

```java
import java.util.*;

class NavigableMapDemo {
    public static void main(String[] args) {
        TreeMap<String, String> t = new TreeMap<>();
        t.put("B", "banana");
        t.put("C", "cat");
        t.put("A", "apple");
        t.put("D", "dog");
        t.put("G", "gun");

        System.out.println("Map: " + t);
        // Keys sorted alphabetically (default natural order for String)

        System.out.println("ceilingKey(C): " + t.ceilingKey("C"));
        // Lowest key ≥ C → C itself (already present)

        System.out.println("higherKey(E): " + t.higherKey("E"));
        // Lowest key > E → G (E not present; next key after E)

        System.out.println("floorKey(E): " + t.floorKey("E"));
        // Highest key ≤ E → D

        System.out.println("lowerKey(E): " + t.lowerKey("E"));
        // Highest key < E → D

        System.out.println("pollFirstEntry(): " + t.pollFirstEntry());
        // Remove and return first entry → A=apple

        System.out.println("pollLastEntry(): " + t.pollLastEntry());
        // Remove and return last entry → G=gun

        System.out.println("descendingMap: " + t.descendingMap());
        // Reverse key order → {D=dog, C=cat, B=banana}

        System.out.println("Original map: " + t);
        // Remaining → {B=banana, C=cat, D=dog}
    }
}
```

### Sorting order

- No Comparator → default natural sorting order of keys
- Keys are String → alphabetical order
- Insertion order of put() calls does NOT matter
### Map after initial puts (sorted by key)

```java
{A=apple, B=banana, C=cat, D=dog, G=gun}
```

### Method-by-method trace

Note on `higherKey("E")`: Sir emphasizes E need not exist as a key — method searches for the navigation boundary relative to the given argument.

## 44:40 — Collections utility class introduction

NavigableSet and NavigableMap complete the 1.6 enhancement topic. Sir now introduces utility classes.

### Two utility classes in Collections Framework (roadmap)

- `Collections` ← today's focus (sort methods)
- `Arrays` ← next sessions
### Collection vs Collections (recap — very important exam question)

### Purpose of Collections class

Collections class defines several utility methods for collection objects

— such as sorting, searching, synchronization, reverse, etc.

Previously covered from Collections class:

- synchronizedList()
- synchronizedMap()
- synchronizedSet()
### Why Collections.sort() exists — the List gap

Problem: "I want to use ArrayList only, but I want all elements in sorting order. How?"

Answer: Collections.sort(list) — fills the gap that List implementations cannot provide natively.

Sir's principle:

Wherever normal collection interfaces have gaps, Collections class utility methods fill those gaps.

## 48:39 — Sorting elements of List: two sort() methods

### Board heading

Sorting elements of List

Collections class defines two sort methods:

Same pattern as TreeSet constructors:

- No Comparator → natural sorting
- With Comparator → customized sorting
## 49:31 — Method 1: sort(List l) — natural sorting

### Signature

```java
public static void sort(List l)
```

- Return type: void — sorts in place inside the existing list (no new list returned)
- Effect: Whatever elements present in the list will be sorted according to default natural sorting order
### Default natural sorting order

### MANDATORY rules (exam — copy all three)

Rule 1: List must contain homogeneous and Comparable objects.

Rule 2: List must NOT contain null.

Rule 3: Sorting happens in the existing list itself — mutates original list order.

Sir repeats TreeSet rule: "Homogeneous and Comparable — we covered this already in TreeSet."

### Board note (exact wording)

In this case, list should compulsorily contain homogeneous and comparable objects;

otherwise we will get runtime exception saying ClassCastException.

List should not contain null;

otherwise we will get NullPointerException.

## 51:35 — Method 2: sort(List l, Comparator c) — customized sorting

### Signature

```java
public static void sort(List l, Comparator c)
```

- Sorts the list according to customized sorting order defined by the Comparator object
- Comparator's compare() method decides element order
- Same compare() return contract as compareTo(): negative = before, positive = after, zero = duplicate
## 52:55 — Board summary: two sort methods

Collections class defines the following two sort methods:

1. public static void sort(List l)
   → to sort based on default natural sorting order
   → list must contain homogeneous & comparable objects; no null

2. public static void sort(List l, Comparator c)
   → to sort based on customized sorting order

## 56:37 — Demo 3: CollectionsSortDemo — natural sorting

### Program

```java
import java.util.*;

class CollectionsSortDemo {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        l.add("J");
        l.add("A");
        l.add("K");
        l.add("N");

        System.out.println("Before sorting: " + l);
        // [J, A, K, N] — insertion order preserved

        Collections.sort(l);

        System.out.println("After sorting: " + l);
        // [A, K, N, J] — alphabetical natural order
    }
}
```

### Output

Before sorting: [J, A, K, N]
After sorting: [A, K, N, J]

### Analysis

- Before: insertion order J, A, K, N
- After: alphabetical A, K, N, J
- Method used: Collections.sort(l) — default natural sorting (no Comparator)
- Strings implement Comparable → valid for natural sort
### Heterogeneous list trap (Sir's warning)

ArrayList l = new ArrayList();
l.add("A");
l.add(new Integer(10));   // adding heterogeneous — NO problem here

Collections.sort(l);        // ClassCastException HERE — at sort call

Critical exam point:

- Adding heterogeneous objects to list → allowed
- Calling Collections.sort() on heterogeneous list → `ClassCastException`
Similarly:

l.add(null);
Collections.sort(l);   // NullPointerException

Adding null may succeed; sorting triggers NPE.

## 1:03:23 — Demo 4: CollectionsSortDemo2 — customized (reverse) sorting

### Program

```java
import java.util.*;

class CollectionsSortDemo2 {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        l.add("J");
        l.add("A");
        l.add("K");
        l.add("L");

        System.out.println("Before sorting: " + l);
        // [J, A, K, L]

        Collections.sort(l, new MyComparator());

        System.out.println("After sorting: " + l);
        // [J, L, K, A] — reverse alphabetical
    }
}

class MyComparator implements Comparator {
    public int compare(Object o1, Object o2) {
        String s1 = (String) o1;
        String s2 = (String) o2;
        return s2.compareTo(s1);   // reverse of natural alphabetical order
    }
}
```

### Comparator logic

```java
return s2.compareTo(s1);
```

- Normal alphabetical: s1.compareTo(s2)
- Reverse: s2.compareTo(s1) — swaps operand order → reverse of alphabetical
### Output

Before sorting: [J, A, K, L]
After sorting: [J, L, K, A]

### Trace (reverse alphabetical)

Starting set: {J, A, K, L}

Reverse alpha order: J > L > K > A → [J, L, K, A]

Sir confirms by running CollectionsSortDemo2.java live.

## NavigableSet vs SortedSet — quick comparison

## NavigableMap vs SortedMap — quick comparison

## Collections.sort() — decision flowchart

Need to sort a List?
│
├── Want default order (Comparable)?
│   └── Collections.sort(list)
│       ├── Objects homogeneous? ──No──→ ClassCastException
│       ├── Objects Comparable? ──No──→ ClassCastException
│       └── Contains null? ──Yes──→ NullPointerException
│
└── Want custom order?
    └── Collections.sort(list, comparator)
        └── Uses Comparator.compare() — your logic decides order

## OCJP/SCJP exam checklist

### Must know definitions

- [ ] NavigableSet is child of SortedSet; TreeSet implements it (since 1.6)
- [ ] NavigableMap is child of SortedMap; TreeMap implements it (since 1.6)
- [ ] Purpose: navigation methods on sorted data
- [ ] Collections is utility class; Collection is interface
### Must know method semantics

- [ ] floor / ceiling = inclusive boundary (≤ / ≥)
- [ ] lower / higher = exclusive boundary (< / >)
- [ ] floor/lower return highest among candidates
- [ ] ceiling/higher return lowest among candidates
- [ ] pollFirst/pollLast remove and return
- [ ] descendingSet() / descendingMap() = reverse-order view
### Must know sort rules

- [ ] Collections.sort(list) = natural order; needs homogeneous Comparable elements
- [ ] Collections.sort(list, c) = customized order via Comparator
- [ ] Heterogeneous add OK; heterogeneous sort → ClassCastException
- [ ] null in list + sort → NullPointerException
- [ ] sort() returns void — modifies list in place
### Likely trap questions

- Difference between lower(10) and floor(10) when 10 exists in set
- higherKey("E") when E is not a key in TreeMap
- After pollFirst() + pollLast(), what does original set contain?
- Collections.sort() on ArrayList containing Integer and String
- Collection vs Collections (interface vs utility class)
## Cross-references (playlist)

## Session closing summary

Sir completes three deliverables in this video:

- NavigableSet — theory + TreeSet demo; fills SortedSet navigation gaps using floor/lower/ceiling/higher and poll/descending views
- NavigableMap — parallel API on TreeMap keys/entries; same logic with Map terminology
- Collections.sort() — two overloads for sorting List elements (natural vs customized), with ClassCastException and NullPointerException rules
Final board point on sorting:

Demo program to sort elements of list according to default natural sorting order → Collections.sort(l)

Demo program to sort elements of list according to customized sorting order → Collections.sort(l, new MyComparator())

That's all for sorting elements of List in this session.

## Metadata

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 151 of 203 |  |  |
| Title | Core Java With OCJP/SCJP: Collections Part-16 \ | \ | Navigableset |
| YouTube ID | Tk-vLd0zjN0 |  |  |
| URL | https://www.youtube.com/watch?v=Tk-vLd0zjN0 |  |  |
| Duration | 1h 09m 43s |  |  |
| Source | YouTube auto-captions |  |  |
| Output | 151-navigableset.doc |  |  |

| Concept | Introduced in | Parent interface | Implementation class |
|---|---|---|---|
| NavigableSet | Java 1.6 | SortedSet | TreeSet |
| NavigableMap | Java 1.6 | SortedMap | TreeMap |

| Interface / Class | Version |
|---|---|
| Collection | 1.2 |
| Set | 1.2 |
| SortedSet | 1.2 |
| TreeSet | 1.2 (modified in 1.6 to implement NavigableSet) |
| Map | 1.2 |
| SortedMap | 1.2 |
| TreeMap | 1.2 (modified in 1.6 to implement NavigableMap) |
| NavigableSet | 1.6 |
| NavigableMap | 1.6 |

| Time | Notes |
|---|---|
| 00:30 | First flight (late night / early morning) |
| 01:45 |  |
| 02:30 |  |
| 03:45 |  |
| 04:20 |  |
| 05:30 |  |
| 06:45 |  |
| 07:30 |  |
| 09:20 |  |
| 10:25 |  |
| 12:30 |  |
| 14:25 |  |
| 15:30 |  |
| 18:20 |  |
| 20:20 |  |
| 23:25 |  |
| 23:59 | Last flight |

| Requirement | Method | Answer (example) |
|---|---|---|
| First flight | first() | 00:30 |
| Last flight | last() | 23:59 |
| All flights before 10:00 | headSet(10:00) | flights < 10:00 |
| All flights after 10:00 | tailSet(10:00) | flights ≥ 10:00 |
| Flights from 07:00 to 12:00 | subSet(07:00, 12:00) | range view |

| Question | SortedSet answer |
|---|---|
| Before 10:00, what is the last flight? (single element, not a view) | ❌ No direct method — hands up |
| After 10:00, what is the first flight? (single element) | ❌ No direct method |
| Before or at 10:00, what is the last flight? | ❌ No direct method |
| At or after 10:00, what is the first flight? | ❌ No direct method |

| Question | NavigableSet method | Boundary type |
|---|---|---|
| Last flight strictly before 10:00 | lower(10:00) | < e (exclusive) |
| Last flight at or before 10:00 | floor(10:00) | ≤ e (inclusive) |
| First flight strictly after 10:00 | higher(10:00) | > e (exclusive) |
| First flight at or after 10:00 | ceiling(10:00) | ≥ e (inclusive) |

| Method | Meaning | Includes element e itself? | Returns |
|---|---|---|---|
| floor(e) | Either e or before e — what is the last/highest? | Yes (≤ e) | Highest element ≤ e |
| lower(e) | Strictly before e — what is the last/highest? | No (< e) | Highest element < e |
| ceiling(e) | Either e or after e — what is the first/lowest? | Yes (≥ e) | Lowest element ≥ e |
| higher(e) | Strictly after e — what is the first/lowest? | No (> e) | Lowest element > e |

| Method | Returns | Precise description |
|---|---|---|
| E floor(E e) | E or null | Highest element which is ≤ e |
| E lower(E e) | E or null | Highest element which is < e |
| E ceiling(E e) | E or null | Lowest element which is ≥ e |
| E higher(E e) | E or null | Lowest element which is > e |

| Method | Returns | Description |
|---|---|---|
| E pollFirst() | E or null | Remove and return first (lowest) element |
| E pollLast() | E or null | Remove and return last (highest) element |

| Method | Returns | Description |
|---|---|---|
| NavigableSet<E> descendingSet() | NavigableSet | Returns NavigableSet in reverse order (descending view) |

| Pair | "Highest" or "Lowest"? | Boundary |
|---|---|---|
| floor / lower | Highest among candidates | ≤ e vs < e |
| ceiling / higher | Lowest among candidates | ≥ e vs > e |

| Statement | Result | Reasoning |
|---|---|---|
| t after adds | [1000, 2000, 3000, 4000, 5000] | Natural ascending sort |
| ceiling(2000) | 2000 | Lowest element ≥ 2000; 2000 exists |
| higher(2000) | 3000 | Lowest element > 2000 |
| floor(3000) | 3000 | Highest element ≤ 3000; 3000 exists |
| lower(3000) | 2000 | Highest element < 3000 |
| pollFirst() | 1000 | Removes 1000 from set |
| pollLast() | 5000 | Removes 5000 from set |
| descendingSet() | [4000, 3000, 2000] | Reverse-order view of remaining |
| t (final) | [2000, 3000, 4000] | Original set minus polled ends |

| Interface | Version | Implementation |
|---|---|---|
| Map | 1.2 | — |
| SortedMap | 1.2 | TreeMap |
| NavigableMap | 1.6 | TreeMap |

| NavigableSet method | NavigableMap equivalent | Notes |
|---|---|---|
| floor(e) | floorKey(K key) | Highest key ≤ given key |
| lower(e) | lowerKey(K key) | Highest key < given key |
| ceiling(e) | ceilingKey(K key) | Lowest key ≥ given key |
| higher(e) | higherKey(K key) | Lowest key > given key |
| pollFirst() | pollFirstEntry() | Remove and return first entry (key-value pair) |
| pollLast() | pollLastEntry() | Remove and return last entry |
| descendingSet() | descendingMap() | Map in reverse key order |

| Call | Result | Explanation |
|---|---|---|
| ceilingKey("C") | "C" | Lowest key ≥ C; C exists in map |
| higherKey("E") | "G" | E not a key; lowest key strictly greater than E is G |
| floorKey("E") | "D" | Highest key ≤ E (E absent, so highest below/at boundary) |
| lowerKey("E") | "D" | Highest key strictly less than E |
| pollFirstEntry() | A=apple | First entry removed |
| pollLastEntry() | G=gun | Last entry removed |
| descendingMap() | {D=dog, C=cat, B=banana} | Descending key view |
| t (final) | {B=banana, C=cat, D=dog} | Ascending key order remaining |

| Term | Type | Purpose |
|---|---|---|
| Collection | Interface | Root interface for group of individual objects |
| Collections | Utility class | Defines several utility methods for Collection objects |

| Collection type | Built-in sorting? |
|---|---|
| Set → TreeSet | ✅ Yes — TreeSet always sorted |
| Queue → PriorityQueue | ✅ Yes — heap priority order |
| List → ArrayList, LinkedList, Vector, Stack | ❌ No — only insertion order |

| # | Method | Sorting type |
|---|---|---|
| 1 | sort(List l) | Default natural sorting order |
| 2 | sort(List l, Comparator c) | Customized sorting order |

| Element type | Natural order |
|---|---|
| Numbers (Integer, etc.) | Ascending order |
| String objects | Alphabetical order |

| Violation | Exception |
|---|---|
| Heterogeneous objects (String + Integer) | ClassCastException |
| Non-Comparable objects (StringBuffer in TreeSet-style scenario) | ClassCastException |

| Violation | Exception |
|---|---|
| null present when sort compares | NullPointerException |

| Capability | SortedSet | NavigableSet |
|---|---|---|
| First / last element | first(), last() | Inherited |
| Range views | headSet, tailSet, subSet | Inherited + inclusive overloads in full API |
| Single-element before boundary | ❌ | lower(), floor() |
| Single-element after boundary | ❌ | higher(), ceiling() |
| Poll (remove + return) ends | ❌ | pollFirst(), pollLast() |
| Reverse view | ❌ | descendingSet() |
| Since | 1.2 | 1.6 |

| Capability | SortedMap | NavigableMap |
|---|---|---|
| Range views on keys | headMap, tailMap, subMap | Inherited |
| Key navigation | ❌ | floorKey, lowerKey, ceilingKey, higherKey |
| Poll entries | ❌ | pollFirstEntry, pollLastEntry |
| Reverse view | ❌ | descendingMap() |
| Since | 1.2 | 1.6 |

| Topic | Video | Notes file |
|---|---|---|
| SortedSet six methods (first, last, headSet, tailSet, subSet) | 142 | 142-set-sortedset.doc |
| TreeSet properties & Comparable | 143 | 143-treeset.doc |
| Comparator interface deep dive | 144 | 144-comparator.doc |
| Queue & PriorityQueue | 150 | (prior session) |
| Searching elements of List | 152 | next session |
| Arrays utility class | 153 | upcoming |

| Field | Value |
|---|---|
| Video | 151 of 203 |
| Series | Durga Sir Core Java OCJP/SCJP |
| Topic | Collections Part-16 — NavigableSet, NavigableMap, Collections.sort() |
| Source | YouTube auto-captions |
| Output | 151-navigableset.doc |
