# Video 142 — Collections Part-7: Set Interface, HashSet, LinkedHashSet & SortedSet

## Video info

Title: Core Java With OCJP/SCJP: Collections Part-7 || Setinterface||ShortedSet

URL: https://www.youtube.com/watch?v=AooYaSeVuZo

Duration: 1h 20m 55s

Position: Video 142 of 203 in the Durga Sir OCJP/SCJP playlist

Prerequisite: Previous sessions covered the Collections Framework overview, Collection interface methods, the full List module (ArrayList, LinkedList, Vector, Stack), and cursors (Enumeration, Iterator, ListIterator). This lecture begins the second major module of Collections — Set.

## Session overview

This is Collections Part-7 — the first deep session on the Set side of the framework. Durga Sir positions Set as the second module after List.

What this lecture covers:

- Brief recap of List module and cursors
- Set hierarchy diagram — HashSet, LinkedHashSet, SortedSet, NavigableSet, TreeSet (with Java version numbers)
- When to use Set interface
- Critical exam point: Set interface defines no new methods — only inherited Collection methods
- HashSet — properties, duplicate behavior, four constructors, fill ratio / load factor, live demo
- LinkedHashSet — difference from HashSet, comparison table, cache-based application use case
- SortedSet interface — when to use, six specific methods (first, last, headSet, tailSet, subSet, comparator), default natural sorting order, worked numeric example
What continues in the next session:

- NavigableSet interface and TreeSet implementation class (mentioned in hierarchy but not fully covered here)
- Comparator / customized sorting (Sir mentions ~3 hours of content planned for that topic)
Exam mantra: Know exactly when to pick Set vs List vs SortedSet. Know HashSet properties cold. Know the four HashSet constructors and fill ratio. Know HashSet vs LinkedHashSet in one table. Know all six SortedSet-specific methods and their boundary conditions (especially < vs <=).

## 00:05 — Recap: List module completed

Before starting Set, Durga Sir quickly revisits what was already covered in the List module:

Transition statement: List module is done. The next terminology / second module in Collections is Set.

## 01:03 — Set module: hierarchy diagram

Durga Sir draws the Set branch under Collection:

Collection
    └── Set
            ├── HashSet
            ├── LinkedHashSet
            ├── SortedSet          (interface)
            │       └── NavigableSet   (interface)
            └── TreeSet            (implementation class of NavigableSet)

### Java version introduction (board note — no deep explanation required)

Sir's instruction: Just remember the version numbers on the board — no lengthy explanation needed for the exam.

## 03:30 — When should we go for `Set`?

### Rule (board conclusion)

If you want to represent a group of individual objects as a single entity where:

- Duplicates are NOT allowed
- Insertion order is NOT preserved
…then we should go for Set.

### Mental model

Classroom phrasing: "Sir, I don't want order. I am not interested in order. But duplicates are not allowed — then we should go for Set."

### Interface relationship

- Set is a child interface of `Collection`
- All Collection interface methods can be applied on Set implemented objects
## 06:00 — `Set` interface: NO new methods (critical exam trap)

Durga Sir deliberately teases the class:

"Set itself contains how many methods? Almost around 58 methods… are you ready for 58 methods?"

Then immediately clarifies the real answer:

### Board note (star this)

`Set` interface doesn't contain any new method.

We have to use only `Collection` interface methods on Set objects.

Why the "58 methods" joke? Sir was testing whether students were paying attention. The correct exam answer: Set adds zero methods beyond Collection.

Implication: No separate section is needed to "discuss Set interface methods" — jump directly to implementation classes starting with HashSet.

## 08:17 — `HashSet`: introduction and properties

HashSet is the first implementation class of Set.

### Property 1 — Underlying data structure

Hash table (hashing-based data structure).

Every object has a hash code (from Object class in java.lang — covered in earlier lectures). Objects are inserted based on hash code, not insertion sequence.

### Property 2 — Duplicates not allowed

Because it is a Set, duplicate objects are not allowed.

### Property 3 — Insertion order not preserved

Objects are inserted based on hash code of the objects. Therefore you cannot predict output order unless you know the hash codes.

### Property 4 — Null insertion

- Null insertion is possible — no problem
- But only once (because duplicates are not allowed; two nulls would be duplicates)
### Property 5 — Heterogeneous objects allowed

Yes. Heterogeneous objects are allowed in HashSet.

Cross-reference (from prior session): Except TreeSet and TreeMap, everywhere else heterogeneous objects are allowed. TreeSet/TreeMap require comparison/sorting → same type needed.

### Property 6 — Implemented interfaces

HashSet implements:

- Serializable
- Cloneable
But NOT RandomAccess — there is no index-based random access.

### Property 7 — Best choice for search operations

Wherever hashing is involved, hashing-related data structures are the best suitable choice for search operations.

"Search algorithm number one up to today is nothing but hashing only."

Rule: If your frequent operation is search, better to go for HashSet.

### Complete HashSet property summary (copy for exam)

## 15:14 — Duplicate insertion behavior in HashSet (exam favorite)

### Example (board)

```java
import java.util.*;

public class HashSetDuplicateDemo {
    public static void main(String[] args) {
        HashSet h = new HashSet();
        System.out.println(h.add("A"));   // true  — first insertion, not duplicate
        System.out.println(h.add("A"));   // false — duplicate, NOT inserted
    }
}
```

### Rules

- add() method return type is `boolean`
- If you try to insert a duplicate object:
- No compile-time error
- No runtime exception
- add() simply returns `false`
- By default HashSet won't allow duplicates
### Board note (star this)

In HashSet, duplicates are not allowed. If we are trying to insert duplicates, we won't get any compile-time or runtime errors — `add()` method simply returns `false`.

## 19:42 — HashSet constructors (four constructors)

Durga Sir emphasizes: Several hashing-related data structures share the same constructor pattern:

- HashSet
- LinkedHashSet
- HashMap
- LinkedHashMap
- WeakHashMap
- IdentityHashMap
Learn HashSet constructors carefully — the same constructors apply to all hashing-based collection classes. Sir will not repeat full explanations for each later class.

### Constructor 1 — Default (no-arg)

```java
HashSet h = new HashSet();
```

- Creates an empty HashSet object
- Default initial capacity: 16
- Default fill ratio (load factor): 0.75
### Constructor 2 — Specified initial capacity

```java
HashSet h = new HashSet(int initialCapacity);
// Example: capacity 1000
HashSet h = new HashSet(1000);
```

- Creates an empty HashSet with specified initial capacity
- Default fill ratio still `0.75`
### Constructor 3 — Initial capacity + fill ratio

```java
HashSet h = new HashSet(int initialCapacity, float fillRatio);
// Example: resize after 90% full instead of default 75%
HashSet h = new HashSet(100, 0.9f);
```

- Customizes both initial capacity and fill ratio
- Default behavior resizes at 75%; with 0.9f, a new (bigger) HashSet internal table is created after 90% is filled
### Constructor 4 — Collection inter-conversion

```java
HashSet h = new HashSet(Collection c);
// Example: create HashSet from a Vector
Vector v = new Vector();
HashSet h = new HashSet(v);
```

- Creates an equivalent HashSet for the given collection
- Meant for inter-conversion between collection objects
- This constructor pattern exists in every collection class
### Constructor summary table

## 22:41 — Fill ratio / Load factor (interview favorite)

### What is fill ratio?

Also called load factor.

Definition (board): After filling how much ratio, a new HashSet object (internal rehash / resize) will be created — that ratio is called fill ratio or load factor.

Alternative wording: After loading how much factor, a new HashSet object is going to be created.

### Comparison with ArrayList

Why 75% and not 100%? Hash table performance degrades as buckets fill up. Resizing early (at 75%) keeps search/insert performance good. Sir's analogy: "I don't want to wait until completing 100%. After filling 75% ratio only, please create a bigger HashSet object."

### Example

- Fill ratio = 0.75 means: after filling 75% of capacity, automatically a new (larger) HashSet internal structure will be created
- Fill ratio = 0.9 means: resize happens after 90% full
### Board note

Fill ratio (or load factor): After filling how much ratio, a new HashSet object will be created.

Example: Fill ratio 0.75 means after filling 75% ratio, a new HashSet object will be created automatically.

Interview question: "What is the default fill ratio of HashSet?" → 0.75

## 36:50 — HashSet live demo program

### Program (board — `HashSetDemo`)

```java
import java.util.*;

public class HashSetDemo {
    public static void main(String[] args) {
        HashSet h = new HashSet();
        h.add("B");
        h.add("C");
        h.add("D");
        h.add("J");
        h.add(null);
        h.add(10);          // Integer — heterogeneous allowed

        System.out.println(h.add("J"));   // false — J already present
        System.out.println(h);            // unpredictable order
    }
}
```

### Expected output (from live run)

false
[null, D, B, C, 10, J]

(Actual order may vary by JVM/hash codes — Sir got this order in class.)

### Observations from the demo

Important exam point: In HashSet output questions, if hash codes are unknown, say "insertion order not preserved — exact order depends on hash codes." Do NOT assume insertion order.

## 42:38 — `LinkedHashSet`

### Name breakdown

Linked + HashSet = LinkedHashSet

Common interview question: "What is the difference between HashSet and LinkedHashSet?"

Do NOT answer: "The difference is linked."

DO answer: Explain the purpose of "linked" — insertion order preservation.

### When to use LinkedHashSet

Requirement mix:

- Set property: Duplicates NOT allowed ✓
- List property: Insertion order MUST be preserved ✓
"List and Set mixed properties — duplicates not allowed but insertion order must be preserved."

Then use LinkedHashSet.

### How it works internally

The linked list maintains insertion order; the hash table provides fast lookup.

### Class relationship

- LinkedHashSet is a child class of HashSet
- It is exactly the same as HashSet (same methods, same constructors) except the differences listed below
### HashSet vs LinkedHashSet comparison table

### Demo: same program, replace HashSet with LinkedHashSet

```java
import java.util.*;

public class LinkedHashSetDemo {
    public static void main(String[] args) {
        LinkedHashSet h = new LinkedHashSet();
        h.add("B");
        h.add("C");
        h.add("D");
        h.add("J");
        h.add(null);
        h.add(10);

        System.out.println(h.add("J"));   // false
        System.out.println(h);            // insertion order preserved
    }
}
```

Output:

false
[B, C, D, J, null, 10]

Key difference from HashSet demo: Output follows insertion order — B, C, D, J, null, 10.

### Board note

In the above HashSet program, if we replace HashSet with LinkedHashSet, the output is:

false then [B, C, D, J, null, 10] — insertion order preserved.

Spelling note: LinkedHashSet is one class name — do not put a space in the middle.

## 52:59 — LinkedHashSet and cache-based applications

Durga Sir connects LinkedHashSet to cache memory concepts (useful for system-design-style interview answers).

### Primary vs secondary memory (quick recap)

Problem: If every operation hits secondary memory, overall system performance drops because secondary memory is slow.

### Cache memory solution

Place cache memory in the middle:

- Frequently/repeatedly required data or code is stored in cache
- Before hitting secondary memory, check cache first
- Cache is faster than disk → overall performance improves
- Cache is costly memory
### Cache properties that match LinkedHashSet

Conclusion: LinkedHashSet is commonly used to develop cache-based applications.

### Board note

In general, we can use LinkedHashSet to develop cache-based applications where duplicates are not allowed and insertion order is preserved.

(How to build cache applications in detail is out of scope for this course — just remember the use case.)

## 59:07 — `SortedSet` interface

### Interface relationship

- SortedSet is a child interface of `Set`
- Set is child of Collection
Collection → Set → SortedSet → NavigableSet → TreeSet (impl)

### When should we go for SortedSet?

If you want to represent a group of individual objects:

- According to some sorting order
- Without duplicates
…then we should go for SortedSet.

### Real-world examples (board)

The name itself indicates: objects are inserted in sorted order.

### Mathematics analogy: normal Set vs SortedSet

Consider three sets from discrete mathematics:

```java
{1, 2, 3}    {3, 2, 1}    {2, 1, 3}
```

In normal Set theory, all three are equal — order of elements does not matter.

But in SortedSet, elements are always in sorted order, e.g. {1, 2, 3}.

This is why SortedSet defines specific methods that are NOT applicable to normal Set / HashSet / LinkedHashSet.

## 1:04:54 — SortedSet: six specific methods

SortedSet interface defines six specific methods. These apply only to SortedSet-related objects — NOT on HashSet or LinkedHashSet.

### Worked example set (used throughout explanation)

Assume this SortedSet of integers:

```java
{100, 101, 104, 106, 110, 115, 120}
```

### Method 1 — `first()`

Object first()

- Returns the first element of the sorted set
- Example: first() → 100
### Method 2 — `last()`

Object last()

- Returns the last element of the sorted set
- Example: last() → 120
### Method 3 — `headSet(Object toElement)`

SortedSet headSet(Object toElement)

- Returns a SortedSet whose elements are less than toElement (strictly less than — NO equal)
- Example: headSet(106) → {100, 101, 104}
- NOT {100, 101, 104, 106} — 106 itself is excluded
### Method 4 — `tailSet(Object fromElement)`

SortedSet tailSet(Object fromElement)

- Returns a SortedSet whose elements are greater than OR equal to fromElement (inclusive)
- Example: tailSet(106) → {106, 110, 115, 120}
### Method 5 — `subSet(Object fromElement, Object toElement)`

SortedSet subSet(Object fromElement, Object toElement)

- Returns a SortedSet whose elements are:
- ≥ fromElement (inclusive start)
- < toElement (exclusive end)
- Example: subSet(101, 115) → {101, 104, 106, 110}
- Includes 101 (≥ 101)
- Excludes 115 (< 115, not ≤)
Boundary rule (star this):

### Method 6 — `comparator()`

Comparator comparator()

- Returns the Comparator object that describes the underlying sorting technique
- Tells you: ascending? descending? custom sort?
- If using default natural sorting order → returns `null`
- No special/custom comparator was supplied
Comparator is a big topic (~3 hours planned in future sessions). For now: know the method signature and that null means default natural order.

### Complete SortedSet method table

### Method count summary (exam)

You CANNOT call `first()`, `last()`, `headSet()`, etc. on a HashSet or LinkedHashSet.

## 1:16:51 — Default natural sorting order

When no custom Comparator is provided, SortedSet uses default natural sorting order.

### Board note (star this — Sir says he'll use this 100+ times)

Default natural sorting order:

- For numbers → ascending order

- For string objects → alphabetical order

When comparator() returns null, it means default natural sorting is in effect.

Customized sorting order (Comparator, Comparable) — covered in upcoming sessions.

## 1:18:37 — SortedSet methods worked example (quick reference)

Using sorted set: {100, 101, 104, 106, 110, 115, 120}

```java
// Assume SortedSet<Integer> s contains the above elements

s.first();              // 100
s.last();               // 120
s.headSet(106);         // {100, 101, 104}
s.tailSet(106);         // {106, 110, 115, 120}
s.subSet(101, 115);     // {101, 104, 106, 110}
s.comparator();         // null (default natural ascending order for integers)
```

## Quick revision — entire Set branch at a glance

### When to use which?

### Hierarchy with method counts

Collection (12 methods)
    └── Set (0 new methods)
            ├── HashSet
            ├── LinkedHashSet (child of HashSet)
            ├── SortedSet (6 new methods)
            │       └── NavigableSet (more methods — next session)
            └── TreeSet (implementation)

### HashSet vs LinkedHashSet vs SortedSet

## Important board notes to copy verbatim

- Set interface doesn't contain any new method — use only Collection methods.
- In HashSet, duplicates are not allowed. Trying to insert duplicates → no error → add() returns false.
- HashSet default initial capacity = 16, default fill ratio = 0.75.
- Fill ratio: after filling that ratio, a new HashSet internal structure is created (default: 75%).
- HashSet underlying DS = hash table. LinkedHashSet = linked list + hash table.
- LinkedHashSet preserves insertion order; HashSet does not.
- LinkedHashSet → cache-based applications (no duplicates + insertion order).
- SortedSet → sorting order without duplicates.
- SortedSet methods: `first`, `last`, `headSet` (<), `tailSet` (≥), `subSet` (≥ and <), `comparator`.
- Default natural sorting: numbers = ascending, strings = alphabetical.
- `comparator()` returns `null` when default natural sorting is used.
## Metadata

## Tables (placement lost -- re-place these in context)

| Topic | What was covered |
|---|---|
| List interface | Child interface of Collection; index-based access |
| Implementation classes | ArrayList, LinkedList, Vector, Stack |
| Cursors | Enumeration, Iterator, ListIterator — when to use each, comparison between them |

| Type | Introduced in |
|---|---|
| Collection, Set, HashSet | Java 1.2 |
| SortedSet | Java 1.2 |
| LinkedHashSet | Java 1.4 |
| NavigableSet | Java 1.6 |
| TreeSet | Java 1.2 (as SortedSet impl; NavigableSet features added later) |

| Requirement | List behavior | Set behavior |
|---|---|---|
| Duplicates | Allowed | Not allowed |
| Insertion order | Preserved | Not preserved |
| Index-based access | Yes | No |

| Interface | New methods defined? | Total usable methods (conceptually) |
|---|---|---|
| Collection | 12 generalized methods (covered in earlier session) | 12 |
| Set | 0 new methods | Same 12 from Collection |
| SortedSet | 6 specific methods (covered later in this video) | 12 + 6 = 18 |

| # | Property | Value |
|---|---|---|
| 1 | Underlying data structure | Hash table |
| 2 | Duplicates | Not allowed |
| 3 | Insertion order | Not preserved (based on hash code) |
| 4 | Null insertion | Possible, but only once |
| 5 | Heterogeneous objects | Allowed |
| 6 | Implements | Serializable, Cloneable |
| 7 | RandomAccess | No |
| 8 | Best for | Frequent search operations |

| # | Signature | Creates | Default capacity | Default fill ratio |
|---|---|---|---|---|
| 1 | new HashSet() | Empty HashSet | 16 | 0.75 |
| 2 | new HashSet(int initialCapacity) | Empty HashSet | user-specified | 0.75 |
| 3 | new HashSet(int initialCapacity, float fillRatio) | Empty HashSet | user-specified | user-specified |
| 4 | new HashSet(Collection c) | Equivalent HashSet from c | depends on c | 0.75 |

| Structure | Default initial capacity | When does it grow? |
|---|---|---|
| ArrayList | 10 | After 100% full — when inserting 11th element into capacity-10 list |
| HashSet | 16 | After 75% full (default fill ratio 0.75) — do NOT wait until 100% |

| Observation | Explanation |
|---|---|
| h.add("J") prints false | Duplicate insertion — returns false, no exception |
| Output is NOT insertion order | Insertion was B, C, D, J, null, 10 — output is null, D, B, C, 10, J |
| Heterogeneous objects present | String objects + Integer(10) + null — all allowed |
| Null is present | Null insertion allowed (once) |
| Cannot predict order without hash codes | HashSet inserts based on hash code; unless you compute hash codes, you cannot guarantee print order |

| Class | Underlying data structure |
|---|---|
| HashSet | Hash table only |
| LinkedHashSet | Linked list + Hash table (hybrid) |

| Point | HashSet | LinkedHashSet |
|---|---|---|
| Underlying data structure | Hash table | Linked list + Hash table (combination) |
| Insertion order | Not preserved | Preserved |
| Duplicates | Not allowed | Not allowed |
| Null insertion | Once | Once |
| Heterogeneous objects | Allowed | Allowed |
| Introduced in | Java 1.2 | Java 1.4 |

| Memory | Example | Speed | Storage |
|---|---|---|---|
| Primary | RAM | High speed | Temporary |
| Secondary | Hard disk | Slower | Permanent |

| Cache requirement | LinkedHashSet satisfies? |
|---|---|
| Duplicates not allowed | ✓ Yes |
| Insertion order preserved | ✓ Yes — "in which order we saved, in the same order only" |

| Scenario | Sorting requirement |
|---|---|
| Student objects | By roll number, or alphabetical order of names |
| Employee objects | Ascending order of employee IDs |
| Integer objects | Ascending order |
| String objects | Alphabetical order |

| Concept | Normal Set | SortedSet |
|---|---|---|
| {1,2,3} vs {3,2,1} | Equal | Different representation |
| Can ask "first element"? | No — meaningless | Yes — first() returns 1 |
| Can ask "last element"? | No | Yes — last() returns 3 |

| Method | Lower bound | Upper bound |
|---|---|---|
| headSet(x) | (none) | < x (exclusive) |
| tailSet(x) | ≥ x (inclusive) | (none) |
| subSet(a, b) | ≥ a (inclusive) | < b (exclusive) |

| Method | Return type | Description |
|---|---|---|
| first() | Object | First element of sorted set |
| last() | Object | Last element of sorted set |
| headSet(Object obj) | SortedSet | Elements less than obj |
| tailSet(Object obj) | SortedSet | Elements ≥ obj (inclusive) |
| subSet(Object obj1, Object obj2) | SortedSet | Elements ≥ obj1 and < obj2 |
| comparator() | Comparator | Underlying sort; null if default natural order |

| Interface | New methods | Applicable on |
|---|---|---|
| Collection | 12 generalized | All collections |
| Set | 0 | HashSet, LinkedHashSet, TreeSet, etc. |
| SortedSet | 6 specific | SortedSet / TreeSet objects only |

| Element type | Default natural sorting order |
|---|---|
| Numbers (Integer, etc.) | Ascending order |
| String objects | Alphabetical order |

| Need | Use |
|---|---|
| No duplicates, no order needed, fast search | HashSet |
| No duplicates, insertion order needed | LinkedHashSet |
| No duplicates, sorted order needed | SortedSet / TreeSet |
| Cache (no duplicates + insertion order) | LinkedHashSet |

| Feature | HashSet | LinkedHashSet | SortedSet |
|---|---|---|---|
| Duplicates | No | No | No |
| Order | Hash-code based (unpredictable) | Insertion order | Sorting order |
| Null allowed | Once | Once | Depends on implementation (TreeSet: generally no null) |
| New interface methods | — | — | 6 specific |
| Best for | Search | Cache / ordered unique set | Sorted unique set |

| Field | Value |
|---|---|
| Video | 142 of 203 |
| Series | Durga Sir Core Java OCJP/SCJP |
| Topic | Collections Part-7 — Set, HashSet, LinkedHashSet, SortedSet |
| Source | YouTube auto-captions |
| Output | 142-set-sortedset.doc |
