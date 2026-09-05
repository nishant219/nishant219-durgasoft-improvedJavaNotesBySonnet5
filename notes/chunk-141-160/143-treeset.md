# Video 143 — Collections Part-8: TreeSet

## Video info

## Session overview

This lecture is the first major session on TreeSet — the concrete implementation class for SortedSet. Durga Sir states he will spend roughly 3–4 hours across multiple videos on TreeSet alone, so clarity here is critical for OCJP/SCJP exams and interviews.

What was already covered (prior sessions):

- Set interface
- SortedSet interface (no demo program possible — it is an interface, not a class)
- NavigableSet — deferred to a separate Java 1.6 enhancements heading (covered later)
What this session covers:

- TreeSet introduction and all core properties/conclusions
- Four TreeSet constructors (with emphasis on first two)
- Demo 1 — default natural sorting with String objects
- Heterogeneous objects → ClassCastException
- Null acceptance — complete rules + Java 1.6 vs 1.7 version difference
- Demo 2 — StringBuffer objects → ClassCastException (non-Comparable)
- Default natural sorting order requirements: homogeneous + Comparable
- `Comparable` interface — package, method, compareTo() semantics
- Demo 3 — compareTo() behavior with live output
- Internal TreeSet insertion mechanism — how JVM calls compareTo() while building the balanced tree
- Comparable vs Comparator — the most important thumb rule for the collection framework
What continues in next session:

- Comparator interface (explicit customized sorting)
- More TreeSet demo programs
## 00:06 — Recap: SortedSet → TreeSet

### Why no SortedSet demo?

SortedSet is an interface. You cannot write:

SortedSet s = new SortedSet(); // CE — interface cannot be instantiated

Interfaces define contracts; concrete classes provide implementation. Therefore there is no standalone "SortedSet demo program" — you always work through an implementation class.

### Hierarchy reminder

Set (I)
 └── SortedSet (I)          ← covered previously, no demo
      └── NavigableSet (I)  ← Java 1.6, covered later
           └── TreeSet (C)  ← TODAY'S FOCUS

Implementation class for SortedSet = TreeSet

Durga Sir explicitly defers NavigableSet to a separate Java 1.6 version enhancements section. Today's focus is entirely on TreeSet.

## 01:19 — TreeSet: Core Properties & Conclusions

Take special care — these points are exam staples and form the foundation for TreeMap (same terminology applies).

### Property 1: Underlying data structure

Balanced Tree (Red-Black Tree internally in Java's TreeSet implementation).

Unlike HashSet (hash table) or ArrayList (dynamic array/resizable array), TreeSet maintains elements in a tree structure that stays balanced for efficient insertion, deletion, and lookup — O(log n) operations.

### Property 2: Duplicate objects

NOT allowed.

TreeSet is a Set implementation. Duplicate insertion is rejected. When compareTo() returns 0 (objects are equal by sorting order), the duplicate is silently not inserted.

### Property 3: Insertion order

NOT preserved.

Elements are inserted according to sorting order, not the order in which you call add(). If you add "Z", then "A", then "L", the internal/storage order follows alphabetical sorting — not Z-A-L.

### Property 4: Heterogeneous objects

NOT allowed.

This is a critical exception in the Collections Framework:

Reason: Comparison is compulsory in TreeSet. To compare two objects, they must be of the same type. If you mix String and Integer, the JVM cannot perform a meaningful comparison → `ClassCastException`.

TreeSet t = new TreeSet();
t.add("A");
t.add("B");
t.add(new Integer(10)); // RuntimeException: ClassCastException

### Property 5: Null insertion

Possible — but only once (with major caveats; see Null Acceptance section below).

Default board answer: "Null insertion is possible (only once)."

But Durga Sir immediately warns: "There is a big story about null." Full rules are covered separately because null behavior differs by TreeSet state (empty vs non-empty) and by Java version.

### Property 6: Marker interfaces

TreeSet implements:

- `Serializable` — yes
- `Cloneable` — yes
- `RandomAccess` — NO
Same pattern as other collection classes (except RandomAccess, which is only for List implementations like ArrayList).

### Property 7: Sorting order

All objects are inserted based on some sorting order.

Two options exist:

## 06:52 — TreeSet Constructors (All Four)

Very important — same constructor terminology repeats for TreeMap and SortedMap. Master these here.

### Constructor 1: No-argument (DEFAULT NATURAL SORTING)

```java
TreeSet t = new TreeSet();
```

- Creates an empty TreeSet
- Elements inserted according to default natural sorting order
- Natural order comes from the element class implementing Comparable interface
Thumb rule: No-arg constructor = default natural sorting order.

### Constructor 2: Comparator argument (CUSTOMIZED SORTING)

```java
TreeSet t = new TreeSet(Comparator c);
```

- Creates an empty TreeSet
- Elements inserted according to customized sorting order
- Customized order is specified by the `Comparator` object passed as argument
Thumb rule: Comparator-argument constructor = customized sorting order.

Durga Sir: "We are going to use minimum 10 times these two words."

### Constructor 3: Collection argument (INTER-CONVERSION)

```java
TreeSet t = new TreeSet(Collection c);
```

- Used for inter-conversion between collection objects
- If you pass a normal ArrayList (or any Collection), TreeSet applies default natural sorting order to those elements
- The source collection has no inherent sorting — TreeSet imposes natural order
### Constructor 4: SortedSet argument (EQUIVALENT TREESET)

```java
TreeSet t = new TreeSet(SortedSet s);
```

- Creates an equivalent TreeSet from any existing SortedSet
- Same sorting order as the source SortedSet is preserved
- Contrast with Constructor 3: here the source already has a defined sort order
### Constructor summary table

Constructors 3 and 4 are "normal" inter-conversion constructors — less exam emphasis than 1 and 2.

## 14:04 — Demo 1: TreeSetDemo (String Natural Sorting)

### Program

```java
import java.util.*;

class TreeSetDemo {
    public static void main(String[] args) {
        TreeSet t = new TreeSet();  // no-arg → default natural sorting
        t.add("A");
        t.add("A");   // duplicate — ignored
        t.add("B");
        t.add("Z");
        t.add("L");
        // t.add(new Integer(10));  // ClassCastException — heterogeneous
        // t.add(null);             // see Null Acceptance section
        System.out.println(t);
    }
}
```

### Which constructor? Which sorting?

- Constructor used: No-argument → default natural sorting order
- Object type: `String` — implements Comparable → valid
### Predicting the output

Insertion sequence: A, A, B, Z, L — but insertion order is NOT preserved. Output follows sorting order.

For String, default natural sorting is lexicographic (Unicode-based) order.

Critical Unicode fact (exam favorite):

Small `'a'` is "bigger" than capital `'A'` because 97 > 65.

Given input: "A", "A" (dup), "B", "Z", "L" — all capitals except none here, but if small 'a' were added:

Capital letters (65–90) come before lowercase letters (97–122)

Output: [A, B, L, Z]

(Duplicate "A" is not inserted twice. If "a" (lowercase) were also added, it would appear after "Z".)

### Heterogeneous objects in Demo 1

t.add(new Integer(10));  // after String objects already present

Result: Exception in thread "main" java.lang.ClassCastException

- String and Integer are heterogeneous types
- TreeSet cannot compare them → ClassCastException
- This line is kept as a commented line in the board example
## 13:13 — Null Acceptance in TreeSet (Complete Rules)

"There is a big story about null." — one of the most tested TreeSet topics.

### Why null is problematic in TreeSet

While adding objects to TreeSet, comparison is compulsory (except for the very first element in an empty set).

When inserting null, the JVM must decide: "Should null go before or after existing element X?" → it must compare null with existing elements.

Comparing any object with `null` → `NullPointerException`.

### Rule 1: Non-empty TreeSet + null insertion

If TreeSet already contains elements (non-empty),
and you try to insert null → NullPointerException

Example:

TreeSet t = new TreeSet();
t.add("A");
t.add("B");
t.add("C");
t.add(null);  // NPE at runtime — compiles fine!

- Code compiles fine (generics erasure; null is allowed at compile time)
- At runtime: NullPointerException
- Reason: null must be compared with existing "A", "B", "C" to find its position in the tree
### Rule 2: Empty TreeSet — first element null

If TreeSet is empty,
inserting null as the FIRST element → ACCEPTABLE (Java 1.6 only — see version note)

Example (Java 1.6):

TreeSet t = new TreeSet();
t.add(null);  // OK in Java 1.6 — no comparison needed for first element
System.out.println(t);  // prints [null]

No comparison required for the first element — tree is empty, null goes in directly.

### Rule 3: After null is inserted, adding any other element

If TreeSet contains null as first element,
and you try to insert ANY other element → NullPointerException

Example:

TreeSet t = new TreeSet();
t.add(null);     // OK (Java 1.6)
t.add("A");      // NPE — must compare "A" with null

When adding "A", JVM calls "A".compareTo(null) or compares null with existing element → NullPointerException.

### Null acceptance summary (board notes)

### ★ Version difference: Java 1.6 vs 1.7+ (STAR NOTE — exam critical)

Durga Sir demonstrates the same program on two JDK versions:

Java 1.6:

TreeSet t = new TreeSet();
t.add(null);
// Output: [null]  ← WORKS

Java 1.7 onwards:

TreeSet t = new TreeSet();
t.add(null);
// NullPointerException  ← FAILS even as first element

Board note with star (★):

Until Java 1.6: Null is allowed at the first element to an empty TreeSet.

From Java 1.7 onwards: Null is NOT allowed even as the first element.

"Null such type of story not applicable for TreeSet from 1.7 version onwards."

For modern OCJP/SCJP exams (Java 8+), the answer is: null is NOT allowed in TreeSet at all.

## 31:08 — Demo 2: TreeSetDemo1 (StringBuffer — Non-Comparable)

### Program

```java
import java.util.*;

class TreeSetDemo1 {
    public static void main(String[] args) {
        TreeSet t = new TreeSet();  // default natural sorting
        t.add(new StringBuffer("A"));
        t.add(new StringBuffer("Z"));
        t.add(new StringBuffer("L"));
        t.add(new StringBuffer("B"));
        System.out.println(t);
    }
}
```

### Student trap question

Durga Sir asks: "What output — `[A, Z, L, B]`, `[A, B, L, Z]`, or `[Z, L, B, A]`?"

Many students guess `[A, B, L, Z]` (alphabetical) because they assume StringBuffer behaves like String.

Wrong. The program throws `ClassCastException` at runtime.

### Why ClassCastException?

- Objects are homogeneous (all StringBuffer) — no heterogeneous problem
- Constructor is no-arg → default natural sorting order
- For default natural sorting: objects must be homogeneous AND Comparable
`StringBuffer` does NOT implement `Comparable`.

### Proof via `javap`

String class:

```java
public final class java.lang.String
    extends java.lang.Object
    implements java.io.Serializable, Comparable<String>, ...
```

→ String implements Comparable ✓

StringBuffer class:

```java
public final class java.lang.StringBuffer
    extends AbstractStringBuilder
    implements java.io.Serializable, CharSequence
```

→ No Comparable ✗

### Exception message

Exception in thread "main" java.lang.ClassCastException:
    java.lang.StringBuffer cannot be cast to java.lang.Comparable

The JVM internally tries to cast StringBuffer to Comparable to call compareTo() — fails.

### Default natural sorting order — mandatory conditions

If we are depending on default natural sorting order, compulsory the objects should be:

1. Homogeneous (same type)

2. Comparable (class implements Comparable interface)

If either condition fails → ClassCastException.

### When is an object "Comparable"?

An object is said to be Comparable if and only if the corresponding class implements `Comparable` interface.

Classes that already implement Comparable:

- String class
- All wrapper classes (Byte, Short, Integer, Long, Float, Double, Character, Boolean)
Classes that do NOT implement Comparable (example):

- StringBuffer class
## 45:35 — Comparable Interface (Theory)

### Package and structure

### compareTo() method — complete syntax

```java
public int compareTo(Object obj);   // legacy/raw
// modern:
public int compareTo(T obj);
```

### Why return type is `int`, NOT `boolean`

When comparing two objects (obj1 vs obj2), three outcomes are possible:

Boolean can only represent two states. Three states require `int`:

- Negative → one category (before)
- Positive → another category (after)
- Zero → third category (equal/duplicate)
### compareTo() return value semantics

obj1.compareTo(obj2)

Important: The magnitude of the negative/positive value does NOT matter — only the sign matters. -25 and -1 both mean "before".

### compareTo() with null

"A".compareTo(null);  // NullPointerException

Comparing any element with null always throws NullPointerException. This connects directly to TreeSet null acceptance rules.

## 53:12 — Demo 3: Tester.java (compareTo Behavior)

### Program

```java
class Tester {
    public static void main(String[] args) {
        System.out.println("A".compareTo("Z"));      // negative
        System.out.println("Z".compareTo("K"));      // positive
        System.out.println("A".compareTo("A"));      // zero
        System.out.println("A".compareTo(null));     // NullPointerException
    }
}
```

### Expected output

-25          ← negative (A comes before Z)
1            ← positive (Z comes after K)
0            ← zero (A equals A)
Exception in thread "main" java.lang.NullPointerException

### Reasoning for each line

Note: Don't focus on -25 vs -1 — focus on minus sign = before.

## 58:55 — Internal TreeSet Insertion Mechanism (compareTo in Action)

"What is the relation between compareTo method and TreeSet?" — the most valuable internal concept.

### Demo program

```java
import java.util.*;

class TreeSetInternalDemo {
    public static void main(String[] args) {
        TreeSet t = new TreeSet();  // default natural sorting
        t.add("K");   // first element — no comparison
        t.add("Z");
        t.add("A");
        t.add("A");   // duplicate
        System.out.println(t);  // [A, K, Z]
    }
}
```

### Step-by-step internal insertion

#### Step 1: `t.add("K")` — first element

- TreeSet is empty
- No comparison required for first element
- "K" becomes the root of the balanced tree
Tree:  K (root)

#### Step 2: `t.add("Z")` — second element

- Comparison required
- JVM internally calls: `"Z".compareTo("K")`
obj1 vs obj2 identification (CRITICAL — exam favorite):

- "Z".compareTo("K") → Z comes after K → returns positive
- JVM decides: Z goes to the right of K (right = greater)
Tree:  K
         \
          Z

#### Step 3: `t.add("A")` — third element

- JVM calls: `"A".compareTo("K")` (compare with root first)
- A comes before K → returns negative
- JVM places A to the left of K
Tree:    K
       /   \
      A     Z

#### Step 4: `t.add("A")` — duplicate attempt

- JVM calls: `"A".compareTo("K")` → negative → go left
- At left, "A" already exists
- JVM calls: `"A".compareTo("A")` → returns zero
- Zero = duplicate → do NOT insert
Final tree: A ← K → Z

Output: [A, K, Z]

### Internal mechanism — board conclusion

If we are depending on default natural sorting order, then while adding objects into the TreeSet, JVM will call `compareTo()` method internally.

Therefore:

- Objects must be Comparable (otherwise JVM cannot call compareTo())
- Objects must be homogeneous (otherwise comparison is meaningless)
### obj1 vs obj2 — memorize this

obj1.compareTo(obj2)

obj1 = the object which is TO BE INSERTED (new element being added)
obj2 = the object which is ALREADY INSERTED (existing element in tree)

Durga Sir emphasizes: "The most valuable terminology you people should be aware clearly."

### Tree navigation logic

When going left/right and another node exists, compare again with that node (may require multiple comparisons per insertion).

## 1:11:13 — Comparable vs Comparator (Thumb Rule)

### When default natural sorting is not enough

Two scenarios require Comparator (covered in next session):

- Default natural sorting order not already available
- Example: StringBuffer — no Comparable implementation
- You must supply external sorting logic via Comparator
- Not satisfied with default natural sorting order
- Example: Strings sort alphabetically A→Z, but you want reverse alphabetical Z→A
- Default order exists but you want customized order
### The one-line interview answer (HIGHLIGHT THIS)

Board note:

If default natural sorting order is not available, OR if we are not satisfied with default natural sorting order, then we can go for customized sorting by using `Comparator`.

### How they relate to TreeSet constructors

- Comparable — everything happens internally (class implements it, JVM calls compareTo())
- Comparator — what we have to do explicitly (pass object, define compare() method) — next session
## Complete TreeSet Properties — Quick Reference Card

## Exception Quick Reference

## Classes Implementing Comparable (Exam List)

## Interview / OCJP Must-Know Questions

- What is the underlying data structure of TreeSet?
→ Balanced Tree (Red-Black Tree)

- What is the implementation class for SortedSet?
→ TreeSet

- Are heterogeneous objects allowed in TreeSet?
→ No — ClassCastException (TreeSet and TreeMap are the only exceptions in Collections Framework)

- What are the two mandatory conditions for default natural sorting in TreeSet?
→ Objects must be homogeneous AND Comparable

- When is an object said to be Comparable?
→ If its class implements Comparable interface

- What is the return type of compareTo()? Why not boolean?
→ int — because three outcomes (before, after, equal) need three states

- compareTo() returns negative / positive / zero — what does each mean?
→ Negative = obj1 before obj2; Positive = obj1 after obj2; Zero = equal (duplicate)

- In obj1.compareTo(obj2) during TreeSet insertion, which is obj1?
→ The object being inserted (new element)

- Null in TreeSet — Java 1.6 vs 1.7?
→ 1.6: null allowed as first element only; 1.7+: null never allowed

- Difference between Comparable and Comparator?
→ Comparable = default natural sorting; Comparator = customized sorting

- Which TreeSet constructor for natural sorting? For custom sorting?
→ No-arg = natural; TreeSet(Comparator) = customized

- Why StringBuffer fails in TreeSet with no-arg constructor?
→ StringBuffer doesn't implement Comparable; JVM cannot call compareTo()

## Programs Covered in This Session

## Connection to Upcoming Topics

## Durga Sir's Emphasis Points (Write in Notebook)

- "Take a bit special care" — TreeSet conclusions are foundation for TreeMap
- "Minimum 10 times these two words" — Comparable vs Comparator
- "Most valuable terminology" — obj1 = to be inserted, obj2 = already inserted
- "Star note" — Java 1.6 vs 1.7 null behavior in TreeSet
- "3 to 4 hours only on TreeSet" — this is a deep topic; don't rush
- Constructor 1 = natural, Constructor 2 = customized — memorize permanently
- StringBuffer looks like String but is NOT Comparable — classic exam trap
- compareTo sign matters, not magnitude (-25 same as -1 for ordering purposes)
- Duplicates silently rejected when compareTo returns 0
- Comparable = internal/automatic; Comparator = external/explicit (next class)

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 143 of 203 |  |  |
| Title | Core Java With OCJP/SCJP: Collections Part-8 \ | \ | TreeSet |
| URL | https://www.youtube.com/watch?v=sLW7GufoSXM |  |  |
| Duration | 1h 16m 30s |  |  |
| Source | YouTube auto-captions (yt-dlp) |  |  |
| Series | Collections Framework (Part-8) |  |  |

| Collection | Heterogeneous objects allowed? |
|---|---|
| ArrayList | Yes |
| LinkedList | Yes |
| HashSet | Yes |
| LinkedHashSet | Yes |
| TreeSet | No |
| TreeMap | No (keys must be comparable) |
| All others | Yes |

| Sorting type | Mechanism | Constructor |
|---|---|---|
| Default natural sorting order | Objects must implement Comparable; JVM calls compareTo() internally | No-arg constructor |
| Customized sorting order | You supply a Comparator object | TreeSet(Comparator c) constructor |

| Concept | Purpose |
|---|---|
| `Comparable` | Default natural sorting order (built into the class) |
| `Comparator` | Customized / our own sorting order (external, passed at construction) |

| # | Syntax | Sorting order applied |
|---|---|---|
| 1 | new TreeSet() | Default natural sorting |
| 2 | new TreeSet(Comparator c) | Customized sorting (via Comparator) |
| 3 | new TreeSet(Collection c) | Default natural sorting |
| 4 | new TreeSet(SortedSet s) | Same as source SortedSet |

| Character | Unicode value |
|---|---|
| 'A' (capital A) | 65 |
| 'a' (small a) | 97 |

| Scenario | Result |
|---|---|
| Non-empty TreeSet + add(null) | NullPointerException |
| Empty TreeSet + add(null) as first element | Allowed (Java ≤ 1.6) |
| TreeSet containing null + add(anything else) | NullPointerException |
| Second add(null) attempt | Duplicate null — only one null possible anyway |

| Failure type | Example | Exception |
|---|---|---|
| Heterogeneous | String + Integer | ClassCastException |
| Non-Comparable | StringBuffer only | ClassCastException |

| Detail | Value |
|---|---|
| Interface | Comparable |
| Package | java.lang |
| Methods | Only one method: compareTo() |
| Type | Generic since Java 5: Comparable<T> |

| Outcome | Meaning |
|---|---|
| obj1 comes before obj2 | Negative return |
| obj1 comes after obj2 | Positive return |
| obj1 and obj2 are equal | Zero return |

| Return value | Meaning | TreeSet action |
|---|---|---|
| Negative (e.g., -1, -25, -1000) | obj1 has to come before obj2 | Place obj1 to the left (smaller) |
| Positive (e.g., +1, +25, +1000) | obj1 has to come after obj2 | Place obj1 to the right (greater) |
| Zero (0) | obj1 and obj2 are equal | Duplicate — do NOT insert |

| Expression | Alphabetical reasoning | Return |
|---|---|---|
| "A".compareTo("Z") | A comes before Z | Negative (-25) |
| "Z".compareTo("K") | Z comes after K | Positive (+1) |
| "A".compareTo("A") | Both equal | Zero (0) |
| "A".compareTo(null) | Cannot compare with null | NullPointerException |

| Variable | Meaning |
|---|---|
| obj1 | The object being inserted (new element) = "Z" |
| obj2 | The object already in the tree (existing element) = "K" |

| compareTo result | Tree direction | Meaning |
|---|---|---|
| Negative | Go left | New element is smaller |
| Positive | Go right | New element is greater |
| Zero | Stop — duplicate | Do not insert |

| Interface | Purpose |
|---|---|
| `Comparable` | Meant for default natural sorting order |
| `Comparator` | Meant for customized sorting order |

| Goal | Constructor | Interface involved |
|---|---|---|
| Natural order | new TreeSet() | Comparable (internal, automatic) |
| Custom order | new TreeSet(Comparator c) | Comparator (external, explicit) |

| Property | TreeSet |
|---|---|
| Underlying DS | Balanced Tree |
| Duplicates | Not allowed |
| Insertion order | Not preserved |
| Heterogeneous objects | Not allowed (ClassCastException) |
| Null insertion | Not allowed (Java 7+); complex rules in Java 6 |
| Serializable | Yes |
| Cloneable | Yes |
| RandomAccess | No |
| Sorting | Default natural OR customized (Comparator) |
| Interface implemented | NavigableSet → SortedSet → Set |

| Scenario | Exception |
|---|---|
| Heterogeneous objects (e.g., String + Integer) | ClassCastException |
| Non-Comparable objects with no-arg constructor (e.g., StringBuffer) | ClassCastException (cannot cast to Comparable) |
| Null in non-empty TreeSet | NullPointerException |
| Any element after null is in TreeSet (Java 6) | NullPointerException |
| Null as first element (Java 7+) | NullPointerException |
| "A".compareTo(null) | NullPointerException |
| Duplicate insert (compareTo returns 0) | Silently ignored (no exception) |

| Class | Implements Comparable? |
|---|---|
| java.lang.String | Yes |
| java.lang.Byte | Yes |
| java.lang.Short | Yes |
| java.lang.Integer | Yes |
| java.lang.Long | Yes |
| java.lang.Float | Yes |
| java.lang.Double | Yes |
| java.lang.Character | Yes |
| java.lang.Boolean | Yes |
| java.lang.StringBuffer | No |
| java.lang.StringBuilder | No |

| # | Class name | Purpose | Key output/exception |
|---|---|---|---|
| 1 | TreeSetDemo | String natural sorting, heterogeneous demo, null demo | [A, B, L, Z] |
| 2 | TreeSetDemo1 | StringBuffer non-Comparable | ClassCastException |
| 3 | Tester | compareTo() return values | -25, 1, 0, NPE |
| 4 | TreeSet internal demo | K, Z, A, A insertion | [A, K, Z] |

| Topic | Status |
|---|---|
| TreeSet properties & constructors | ✅ This session |
| Null acceptance rules | ✅ This session |
| Comparable & compareTo() | ✅ This session |
| Internal insertion mechanism | ✅ This session |
| Comparable vs Comparator thumb rule | ✅ Introduced |
| Comparator interface & compare() | ⏳ Next session |
| NavigableSet (Java 1.6) | ⏳ Later session |
| TreeMap | ⏳ Future (same constructor terminology) |
| More TreeSet demo programs (5–6 total planned) | ⏳ Continuing |
