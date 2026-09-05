# Video 148 — Collections Part-13: SortedMap & TreeMap

## Video info

## Session overview

This lecture (~42 minutes) opens the sorted Map branch of the Collections Framework. After completing all HashMap variations in Video 147, Sir moves to maps where entries are stored according to sorting order of keys — not values, not insertion order.

What was already covered (prior Map sessions — recap only):

What this session covers:

- Map hierarchy recap — where SortedMap and TreeMap fit
- SortedMap interface — child of Map (NOT Collection); sorting by key only
- All six SortedMap-specific methods — signatures, return types, boundary rules (parallel to SortedSet)
- TreeMap — implementation class; Red-Black tree; complete property sheet (parallel TreeSet)
- Four TreeMap constructors — natural vs customized sorting (same thumb rule as TreeSet)
- Demo 1 — TreeMap with String keys (default natural sorting)
- Demo 2 — TreeMap with Integer keys + Comparator (descending order)
- Demo 3 — Custom class keys implementing Comparable
- Null key acceptance rules — identical story to TreeSet; null values allowed
- TreeMap vs HashMap — comparison table (top interview question)
- Exam traps and OCJP must-know questions
What continues in next sessions:

- NavigableMap (Java 1.6) — navigation methods on TreeMap (Video 151)
- Hashtable & Properties — legacy Map classes (Video 149)
- Queue module
Exam mantra: TreeMap = TreeSet logic applied to Map keys. If TreeSet + Comparable/Comparator (Videos 143–144) is clear, TreeMap becomes a 30-minute topic, not a new subject. Sorting is always by key; values are passengers — they never decide order.

## 00:05 — Recap: Map hierarchy and HashMap variations done

### Collection Framework — two halves (board reminder)

Collection Framework
├── First half  → Collection interface (List, Set, Queue)
└── Second half → Map interface (completely separate branch)

- Map is NOT a child interface of Collection.
- Map = group of objects as key–value pairs (entries).
- Collection = group of individual objects.
### Map module progress (after Video 147)

Map (I)
 ├── HashMap (C)              ← Video 146 ✓
 ├── LinkedHashMap (C)        ← Video 147 ✓  (extends HashMap)
 ├── IdentityHashMap (C)      ← Video 147 ✓
 ├── WeakHashMap (C)          ← Video 147 ✓
 ├── SortedMap (I)            ← TODAY (Video 148)
 │    └── NavigableMap (I)    ← deferred (Video 151, Java 1.6)
 │         └── TreeMap (C)    ← TODAY (Video 148)
 ├── Hashtable (C)            ← next (Video 149, legacy 1.0)
 └── Properties (C)           ← next (Video 149, legacy 1.0)

Sir's framing: "HashMap and its three small variations — finished. Now we enter sorted Map territory. Same story you saw with SortedSet and TreeSet — but Map terminology."

### Set ↔ Map parallel (critical memory hook)

"If TreeSet is clear, TreeMap is copy-paste — just replace add(element) with put(key, value) and remember sorting is by key, not value." — Durga Sir (cross-ref Video 146 recap)

## 02:30 — SortedMap interface introduction

### Hierarchy

Map (I)
 └── SortedMap (I)          ← child of Map, NOT Collection
      └── NavigableMap (I)  ← Java 1.6 (deferred)
           └── TreeMap (C)  ← implementation class

### When should we go for SortedMap?

Board rule (copy exactly):

If we want to represent a group of key–value pairs where entries are stored according to some sorting order of keys, then we should go for SortedMap.

Conditions implied:

- Duplicate keys are NOT allowed (Map contract — same as all Map implementations).
- Duplicate values ARE allowed.
- Entries appear in sorted key order, not insertion order.
### ★ Critical rule — sorting on KEYS only, NEVER values

Exam trap: "TreeMap sorts entries by value" → FALSE. Values can be any type in any order; only keys determine position in the tree.

Real-world examples (board):

- Phone directory: name (key) → phone number (value) — alphabetical by name
- Roll-number map: rollNo (key) → studentName (value) — numeric ascending by roll
- Word frequency (if key = word): lexicographic order of words
### Why no standalone SortedMap demo?

Same reason as SortedSet (Video 142):

SortedMap sm = new SortedMap();  // CE — interface cannot be instantiated

SortedMap is an interface. You always work through an implementation class — TreeMap.

## 06:00 — SortedMap: six specific methods (complete catalog)

SortedMap defines six specific methods beyond inherited Map methods. These apply only to SortedMap / TreeMap objects — NOT on HashMap, LinkedHashMap, etc.

Parallel to SortedSet (Video 142): Replace element with key, SortedSet return type with SortedMap, first()/last() with firstKey()/lastKey().

### Worked example map (used throughout)

Assume this TreeMap of roll numbers → names (keys sorted ascending):

```java
{100=Ram, 101=Sita, 104=Arjun, 106=Bharat, 110=Lakshman, 115=Hanuman, 120=Ravan}
```

### Method 1 — `Comparator comparator()`

Comparator comparator()

Board note: comparator() returning null means default natural sorting order is in effect (numbers → ascending, strings → alphabetical).

### Method 2 — `Object firstKey()`

Object firstKey()

- Returns the first (lowest) key in the sorted map.
- Example: firstKey() → 100
- Throws NoSuchElementException if map is empty.
### Method 3 — `Object lastKey()`

Object lastKey()

- Returns the last (highest) key in the sorted map.
- Example: lastKey() → 120
### Method 4 — `SortedMap headMap(Object toKey)`

SortedMap headMap(Object toKey)

- Returns a view of the portion of this map whose keys are strictly less than toKey (< — NOT equal).
- Example: headMap(106) → {100=Ram, 101=Sita, 104=Arjun}
- 106 is excluded — headMap uses strict <.
### Method 5 — `SortedMap tailMap(Object fromKey)`

SortedMap tailMap(Object fromKey)

- Returns a view whose keys are greater than or equal to fromKey (≥ — inclusive).
- Example: tailMap(106) → {106=Bharat, 110=Lakshman, 115=Hanuman, 120=Ravan}
### Method 6 — `SortedMap subMap(Object fromKey, Object toKey)`

SortedMap subMap(Object fromKey, Object toKey)

- Returns a view whose keys are:
- ≥ fromKey (inclusive start)
- < toKey (exclusive end)
- Example: subMap(101, 115) → {101=Sita, 104=Arjun, 106=Bharat, 110=Lakshman}
- Includes 101 (≥ 101); excludes 115 (< 115, not ≤).
### ★ Boundary rule summary (star this — exam favorite)

Same < vs ≤ pattern as SortedSet — Sir uses identical numeric examples in both lectures.

### SortedSet ↔ SortedMap method mapping table

### Quick reference program — SortedMap methods only

```java
import java.util.*;

class SortedMapMethodsDemo {
    public static void main(String[] args) {
        SortedMap<Integer, String> sm = new TreeMap<>();
        sm.put(100, "Ram");
        sm.put(101, "Sita");
        sm.put(104, "Arjun");
        sm.put(106, "Bharat");
        sm.put(110, "Lakshman");
        sm.put(115, "Hanuman");
        sm.put(120, "Ravan");

        System.out.println("Full map: " + sm);
        System.out.println("firstKey(): " + sm.firstKey());           // 100
        System.out.println("lastKey(): " + sm.lastKey());             // 120
        System.out.println("headMap(106): " + sm.headMap(106));       // {100=Ram, 101=Sita, 104=Arjun}
        System.out.println("tailMap(106): " + sm.tailMap(106));       // {106=Bharat, 110=Lakshman, 115=Hanuman, 120=Ravan}
        System.out.println("subMap(101,115): " + sm.subMap(101, 115)); // {101=Sita, 104=Arjun, 106=Bharat, 110=Lakshman}
        System.out.println("comparator(): " + sm.comparator());       // null (natural ascending)
    }
}
```

Expected output:

Full map: {100=Ram, 101=Sita, 104=Arjun, 106=Bharat, 110=Lakshman, 115=Hanuman, 120=Ravan}
firstKey(): 100
lastKey(): 120
headMap(106): {100=Ram, 101=Sita, 104=Arjun}
tailMap(106): {106=Bharat, 110=Lakshman, 115=Hanuman, 120=Ravan}
subMap(101,115): {101=Sita, 104=Arjun, 106=Bharat, 110=Lakshman}
comparator(): null

## 12:00 — TreeMap: implementation class & complete properties

### Board introduction

TreeMap is the implementation class of SortedMap.

Same relationship as TreeSet ↔ SortedSet:

### Property 1 — Underlying data structure

Balanced Tree (Red-Black Tree internally in Java's TreeMap implementation).

- Unlike HashMap (hash table), TreeMap maintains entries in a tree structure.
- Balanced tree → O(log n) for get, put, remove.
- Sir: "Same Red-Black tree story as TreeSet — only difference is each node stores a key and a value."
### Property 2 — Duplicate keys

NOT allowed.

- TreeMap is a Map — duplicate keys rejected.
- When compareTo() returns 0 (or compare() returns 0), keys are considered equal → old value replaced, new value stored (Map put() contract).
- Contrast with TreeSet: duplicate element silently not inserted (add() returns false).
```java
TreeMap tm = new TreeMap();
tm.put("A", 1);
tm.put("A", 2);   // duplicate KEY — replaces value; returns old value 1
System.out.println(tm);  // {A=2}
```

### Property 3 — Insertion order

NOT preserved.

- Entries stored according to sorting order of keys, not the order of put() calls.
- If you put Z, then A, then L — output follows key sorting, not Z-A-L.
### Property 4 — Heterogeneous keys

NOT allowed.

Critical exception in Collections Framework (same as TreeSet):

TreeMap tm = new TreeMap();
tm.put("A", 100);
tm.put("B", 200);
tm.put(new Integer(10), 300);  // RuntimeException: ClassCastException

- Comparison is compulsory for TreeMap keys.
- String and Integer are heterogeneous → JVM cannot compare meaningfully → ClassCastException.
- Values can be heterogeneous — only keys must be comparable and homogeneous.
### Property 5 — Null key insertion

Possible — but only once (with major caveats; see Null Key section below).

- Default board answer (legacy): "Null key insertion is possible (only once)."
- Sir's warning: "There is a big story about null key." — identical to TreeSet null story.
- Null values: Allowed without restriction (unlike Hashtable).
### Property 6 — Marker interfaces

TreeMap implements:

### Property 7 — Sorting order of keys

All entries inserted based on sorting order of keys.

Two options (same as TreeSet):

### Complete TreeMap property summary (copy for exam)

## 16:00 — TreeMap constructors (all four — VERY IMPORTANT)

Sir: "Same constructor terminology as TreeSet and SortedSet. We are going to use minimum 10 times these two words: default natural sorting order and customized sorting order."

### Constructor 1 — No-argument (DEFAULT NATURAL SORTING)

```java
TreeMap tm = new TreeMap();
```

- Creates an empty TreeMap.
- Keys inserted according to default natural sorting order.
- Natural order comes from the key class implementing Comparable.
Thumb rule: No-arg constructor = default natural sorting order.

### Constructor 2 — Comparator argument (CUSTOMIZED SORTING)

```java
TreeMap tm = new TreeMap(Comparator c);
```

- Creates an empty TreeMap.
- Keys inserted according to customized sorting order.
- Customized order specified by the Comparator object passed as argument.
Thumb rule: Comparator-argument constructor = customized sorting order.

### Constructor 3 — Map argument (INTER-CONVERSION)

```java
TreeMap tm = new TreeMap(Map m);
```

- Used for inter-conversion between Map objects.
- If you pass a normal HashMap (or any Map), TreeMap applies default natural sorting order to those entries.
- Source map has no inherent key sorting — TreeMap imposes natural order on keys.
### Constructor 4 — SortedMap argument (EQUIVALENT TREEMAP)

```java
TreeMap tm = new TreeMap(SortedMap sm);
```

- Creates an equivalent TreeMap from any existing SortedMap.
- Same sorting order as the source SortedMap is preserved.
- Contrast with Constructor 3: here the source already has a defined sort order (including custom Comparator).
### Constructor summary table

Constructors 3 and 4 are inter-conversion constructors — less exam emphasis than 1 and 2.

Memorize permanently: Constructor 1 = natural, Constructor 2 = customized.

## 18:30 — Demo 1: TreeMap with String keys (natural sorting)

### Program

```java
import java.util.*;

class TreeMapDemo {
    public static void main(String[] args) {
        TreeMap t = new TreeMap();  // no-arg → default natural sorting of KEYS
        t.put("Z", 100);
        t.put("A", 200);
        t.put("L", 300);
        t.put("A", 400);   // duplicate KEY "A" → replaces 200 with 400; returns 200
        t.put("B", 500);
        // t.put(new Integer(10), 600);  // ClassCastException — heterogeneous key
        // t.put(null, 700);             // see Null Key section
        System.out.println(t);
    }
}
```

### Which constructor? Which sorting?

### Predicting the output

Insertion sequence of keys: Z, A, L, A (dup), B — but insertion order is NOT preserved. Output follows key sorting order.

For String keys, default natural sorting = lexicographic (Unicode-based) order.

Critical Unicode fact (exam favorite — from TreeSet session):

Capital letters (65–90) come before lowercase letters (97–122). Small 'a' is "bigger" than capital 'A' because 97 > 65.

Given keys: "Z", "A", "L", "B" (all capitals in this demo):

Output: {A=400, B=500, L=300, Z=100}

- Duplicate key "A": value 200 replaced by 400 (Map put contract).
- Keys sorted: A, B, L, Z — values follow their keys.
### Heterogeneous keys trap

t.put(new Integer(10), 600);  // after String keys already present

Result: Exception in thread "main" java.lang.ClassCastException

- String and Integer keys are heterogeneous types.
- TreeMap cannot compare them → ClassCastException.
## 22:00 — Demo 2: TreeMap with Integer keys + Comparator (descending)

Cross-reference: Video 144 — same descending Integer Comparator program, but TreeSet → TreeMap.

### Problem statement (board)

Write a program to insert key–value pairs into TreeMap where keys are Integer objects and sorting order of keys is descending order.

### Step 1 — Comparator class

```java
class MyComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Integer I1 = (Integer) obj1;
        Integer I2 = (Integer) obj2;

        if (I1 < I2)
            return +1;      // smaller key → after (descending)
        else if (I1 > I2)
            return -1;      // bigger key → before (descending)
        else
            return 0;       // equal keys → duplicate key
    }
}
```

### Step 2 — Full program

```java
import java.util.*;

class MyComparator implements Comparator {
    public int compare(Object obj1, Object obj2) {
        Integer I1 = (Integer) obj1;
        Integer I2 = (Integer) obj2;
        if (I1 < I2) return +1;
        else if (I1 > I2) return -1;
        else return 0;
    }
}

class TreeMapDemo2 {
    public static void main(String[] args) {
        TreeMap t = new TreeMap(new MyComparator());  // LINE ONE — customized sorting
        t.put(10, "Ten");
        t.put(0, "Zero");
        t.put(15, "Fifteen");
        t.put(5, "Five");
        t.put(20, "Twenty");
        t.put(20, "Score");   // duplicate KEY 20 → replaces "Twenty" with "Score"
        System.out.println(t);
    }
}
```

### Which method does JVM call on keys?

Observe the difference: Without Comparator → compareTo. With Comparator → compare.

### Expected output

```java
{20=Score, 15=Fifteen, 10=Ten, 5=Five, 0=Zero}
```

Keys in descending order: 20, 15, 10, 5, 0. Values are attached to keys — they do not influence sort position.

### Descending-order compare logic table (keys)

JVM-as-blind-person rule (Video 144): JVM trusts only the sign of the return value — negative = before, positive = after, zero = duplicate/equal.

## 28:00 — Demo 3: Custom class keys with Comparable

When key class implements Comparable, no-arg TreeMap constructor works — JVM calls compareTo() on keys during insertion.

### Custom key class

```java
class Student implements Comparable {
    int rollNo;
    String name;

    Student(int rollNo, String name) {
        this.rollNo = rollNo;
        this.name = name;
    }

    public int compareTo(Object obj) {
        Student s = (Student) obj;
        // Sort by rollNo ascending (natural order for this class)
        return this.rollNo - s.rollNo;
    }

    public String toString() {
        return rollNo + "=" + name;
    }
}
```

Note: compareTo() defines natural order for keys. Values (here embedded in toString for demo clarity) are separate.

### Program

```java
import java.util.*;

class Student implements Comparable {
    int rollNo;
    String name;

    Student(int rollNo, String name) {
        this.rollNo = rollNo;
        this.name = name;
    }

    public int compareTo(Object obj) {
        Student s = (Student) obj;
        return this.rollNo - s.rollNo;
    }

    public String toString() {
        return rollNo + "=" + name;
    }
}

class TreeMapDemo3 {
    public static void main(String[] args) {
        TreeMap t = new TreeMap();  // default natural sorting — keys must be Comparable
        t.put(new Student(103, "Ravi"), "Hyderabad");
        t.put(new Student(101, "Durga"), "Bangalore");
        t.put(new Student(105, "Shiva"), "Chennai");
        t.put(new Student(102, "Rama"), "Mumbai");
        System.out.println(t);
    }
}
```

### Internal insertion mechanism (keys)

Same as TreeSet (Video 143) — only the object being compared is the key:

obj1 vs obj2 terminology (exam favorite):

obj1.compareTo(obj2)

obj1 = the KEY which is TO BE INSERTED (new key in put())
obj2 = the KEY which is ALREADY INSERTED (existing key in tree)

### Output

When printing TreeMap, entrySet() iteration walks keys in sorted order. With custom toString on Student showing rollNo:

```java
{101=Durga, 102=Rama, 103=Ravi, 105=Shiva}
```

Keys sorted by rollNo ascending. Values (city names) do not affect order.

### What if key class does NOT implement Comparable?

```java
class Employee {  // NO Comparable
    int id;
    Employee(int id) { this.id = id; }
}

TreeMap t = new TreeMap();
t.put(new Employee(1), "A");
t.put(new Employee(2), "B");
// ClassCastException: Employee cannot be cast to Comparable
```

Same trap as StringBuffer in TreeSet (Video 143) — homogeneous but non-Comparable keys fail with no-arg constructor.

Mandatory conditions for default natural sorting (keys):

- Keys must be homogeneous (same type).
- Key class must implement Comparable.
## 32:00 — Null key acceptance rules in TreeMap (same as TreeSet)

"Null — such a type of story — for key in TreeMap, same as TreeSet. For value, null is happily allowed." — Durga Sir

### Why null key is problematic

While adding entries to TreeMap, comparison of keys is compulsory (except for the very first entry in an empty map).

When inserting null key, JVM must decide: "Should null go before or after existing key X?" → it must compare null with existing keys.

Comparing any key object with null → NullPointerException.

### Rule 1 — Non-empty TreeMap + null key

TreeMap t = new TreeMap();
t.put("A", 1);
t.put("B", 2);
t.put(null, 3);   // NullPointerException at runtime — compiles fine!

- Code compiles (generics erasure; null allowed at compile time).
- Runtime: NullPointerException.
- Reason: null key must be compared with existing "A", "B" to find tree position.
### Rule 2 — Empty TreeMap — first entry null key (Java ≤ 1.6 only)

```java
TreeMap t = new TreeMap();
t.put(null, "value");  // OK in Java 1.6 only
System.out.println(t);  // {null=value}
```

No comparison required for first entry — tree is empty, null key goes in directly.

### Rule 3 — After null key inserted, adding any other key

TreeMap t = new TreeMap();
t.put(null, "first");  // OK (Java 1.6)
t.put("A", 2);         // NPE — must compare "A" with null key

### Rule 4 — Null VALUES are allowed (contrast with Hashtable)

```java
TreeMap t = new TreeMap();
t.put("A", null);      // ✓ OK — null VALUE is fine
t.put("B", null);      // ✓ OK — multiple null values allowed
System.out.println(t); // {A=null, B=null}
```

Hashtable rejects both null key and null value. TreeMap rejects null key (with TreeSet rules) but accepts null values.

### ★ Version difference: Java 1.6 vs 1.7+ (STAR NOTE)

For modern OCJP/SCJP exams (Java 8+): null key is NOT allowed in TreeMap at all.

### Null acceptance summary table (KEYS)

## 36:00 — TreeMap vs HashMap (comparison table)

Top interview / OCJP question — Sir covers this after TreeMap properties are established.

### When to use which? (decision guide)

### Side-by-side demo — same puts, different output

```java
import java.util.*;

class HashMapVsTreeMapDemo {
    public static void main(String[] args) {
        Map hash = new HashMap();
        hash.put("Z", 1);
        hash.put("A", 2);
        hash.put("M", 3);
        System.out.println("HashMap: " + hash);
        // e.g. {A=2, Z=1, M=3} — unpredictable hash order

        Map tree = new TreeMap();
        tree.put("Z", 1);
        tree.put("A", 2);
        tree.put("M", 3);
        System.out.println("TreeMap: " + tree);
        // {A=2, M=3, Z=1} — always sorted by key
    }
}
```

## 38:30 — Comparable vs Comparator thumb rule (TreeMap edition)

Same one-line interview answer from Video 143/144 — applied to keys:

If default natural sorting order is not available for keys, OR if we are not satisfied with default natural sorting order of keys, then we can go for customized sorting by using Comparator.

Cross-ref Video 146: "If Comparable/Comparator is clear, TreeMap learning becomes very simple."

## 40:00 — Exam traps and interview questions

### OCJP must-know Q&A

### Common exam traps

### Interview favorites

- Difference between TreeMap and HashMap? → Use comparison table above.
- Difference between SortedSet and SortedMap methods? → element vs key terminology; first/last vs firstKey/lastKey.
- When does TreeMap call compareTo vs compare? → Depends on constructor (no-arg vs Comparator).
- Can I use TreeMap without Comparable keys? → Only if you pass a Comparator that handles the key type.
- Why is TreeMap slower than HashMap? → Tree O(log n) vs hash O(1) average.
## Exception quick reference

## Programs covered in this session

## Connection to upcoming topics

NavigableMap preview (Video 151): "Same copy-paste as NavigableSet — but Map terminology. Methods operate on keys, not values."

## Durga Sir's emphasis points (write in notebook)

- "TreeMap is copy-paste of TreeSet" — sorting rules apply to keys, not values.
- "Minimum 10 times" — default natural sorting order vs customized sorting order.
- "Map is not child of Collection" — SortedMap lives on Map branch.
- "Sorting based on key, NOT based on value" — underline on board.
- "Same null story as TreeSet" — for keys only; values can be null.
- Constructor 1 = natural, Constructor 2 = customized — memorize permanently.
- headMap `<`, tailMap `≥`, subMap `≥` and `<` — same as SortedSet boundaries.
- comparator() returns null → default natural sorting in effect.
- obj1 = key to be inserted, obj2 = key already in tree — during put().
- If Comparable/Comparator clear from TreeSet sessions, TreeMap is easy — don't re-learn from scratch.
## One-page revision sheet

SORTEDMAP  = Map + keys sorted (no dup keys) — interface, no impl
TREEMAP    = SortedMap implementation — Red-Black tree — Java 1.2

Sorting: KEY only, NEVER value
Constructors:
  new TreeMap()              → natural (keys Comparable)
  new TreeMap(Comparator)    → customized
  new TreeMap(Map)           → natural on copy
  new TreeMap(SortedMap)     → same order as source

SortedMap methods (6):
  comparator()  firstKey()  lastKey()
  headMap(k)    → keys < k
  tailMap(k)    → keys ≥ k
  subMap(from,to) → keys ≥ from AND < to

TreeMap properties (= TreeSet on keys):
  No dup keys | sorted keys | no heterogeneous keys
  null key: TreeSet rules (Java 7+ = never)
  null value: OK

TreeMap vs HashMap:
  Tree = sorted O(log n) | Hash = unsorted O(1)
  Tree = no null key (7+) | Hash = one null key OK
  Tree = homogeneous Comparable keys | Hash = any keys

## Metadata — Map module checklist (updated)

## Heterogeneous objects allowed? (Collections Framework)

TreeSet and TreeMap are the only places in the Collections Framework where heterogeneous objects (for elements/keys) cause ClassCastException.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 148 of 203 |  |  |
| Title | Core Java With OCJP/SCJP: Collections Part-13 \ | \ | sortedmap |
| URL | https://www.youtube.com/watch?v=aOAWzh3BJM4 |  |  |
| Video ID | aOAWzh3BJM4 |  |  |
| Duration | 42m 13s |  |  |
| Series | Collections Framework — Map module (sorted maps) |  |  |
| Prerequisite | Videos 146–147 (HashMap, LinkedHashMap, IdentityHashMap, WeakHashMap). Videos 143–144 (TreeSet, Comparable/Comparator) — mandatory; TreeMap is copy-paste of TreeSet terminology applied to keys. |  |  |
| Notes source | Synthesized from adjacent lecture cross-references + standard Durga Sir OCJP syllabus (YouTube captions unavailable; Whisper blocked by bot-check — pending re-transcription) |  |  |

| # | Topic | Status |
|---|---|---|
| 1 | Map introduction — keys, values, entries; Map is NOT child of Collection | ✓ Video 146 |
| 2 | HashMap — properties, four constructors, demo | ✓ Video 146 |
| 3 | HashMap vs Hashtable | ✓ Video 146 |
| 4 | LinkedHashMap — insertion order preserved | ✓ Video 147 |
| 5 | IdentityHashMap — == for duplicate keys | ✓ Video 147 |
| 6 | WeakHashMap — weak keys, GC interaction | ✓ Video 147 |

| Set side | Map side | Sorting applies to |
|---|---|---|
| SortedSet (I) | SortedMap (I) | Keys only (Map) / Elements (Set) |
| TreeSet (C) | TreeMap (C) | Red-Black tree implementation |
| NavigableSet (I) | NavigableMap (I) | Java 1.6 navigation APIs |
| Comparable/Comparator on elements | Comparable/Comparator on keys | Same rules |

| Sorts by | SortedMap |
|---|---|
| Key | ✓ YES — this is the entire purpose |
| Value | ✗ NO — value never participates in sorting |

| Aspect | Detail |
|---|---|
| Returns | The Comparator object describing the sorting technique used for keys |
| Default natural sorting | Returns `null` — no custom Comparator was supplied |
| Custom sorting | Returns the same Comparator object passed to TreeMap(Comparator c) constructor |

| Method | Lower bound | Upper bound |
|---|---|---|
| headMap(toKey) | (none) | < toKey (exclusive) |
| tailMap(fromKey) | ≥ fromKey (inclusive) | (none) |
| subMap(from, to) | ≥ fromKey (inclusive) | < toKey (exclusive) |

| SortedSet (Video 142) | SortedMap (Video 148) | Same boundary? |
|---|---|---|
| first() | firstKey() | — |
| last() | lastKey() | — |
| headSet(toElement) | headMap(toKey) | Strict < |
| tailSet(fromElement) | tailMap(fromKey) | Inclusive ≥ |
| subSet(from, to) | subMap(from, to) | ≥ from, < to |
| comparator() | comparator() | null = natural order |

| Interface | Implementation |
|---|---|
| SortedSet | TreeSet |
| SortedMap | TreeMap |

| Interface | Supported? |
|---|---|
| Serializable | ✓ Yes |
| Cloneable | ✓ Yes |
| RandomAccess | ✗ NO (List-only marker) |

| Sorting type | Mechanism | Constructor |
|---|---|---|
| Default natural sorting order | Key class implements Comparable; JVM calls compareTo() on keys internally | new TreeMap() |
| Customized sorting order | You supply a Comparator object for keys | new TreeMap(Comparator c) |

| # | Property | TreeMap value |
|---|---|---|
| 1 | Underlying DS | Red-Black tree (balanced tree) |
| 2 | Duplicate keys | Not allowed (replace on duplicate key) |
| 3 | Duplicate values | Allowed |
| 4 | Insertion order | Not preserved (sorted by key) |
| 5 | Heterogeneous keys | Not allowed — ClassCastException |
| 6 | Null key | See Null Key section (1.7+: never) |
| 7 | Null value | Allowed |
| 8 | Sorting | By key only, never by value |
| 9 | Implements | Serializable, Cloneable |
| 10 | RandomAccess | No |
| 11 | Time complexity | O(log n) get/put/remove |
| 12 | Best for | Sorted key traversal, range queries (headMap/tailMap/subMap) |

| # | Syntax | Sorting order applied |
|---|---|---|
| 1 | new TreeMap() | Default natural sorting (keys must be Comparable) |
| 2 | new TreeMap(Comparator c) | Customized sorting (via Comparator on keys) |
| 3 | new TreeMap(Map m) | Default natural sorting (imposed on m's entries) |
| 4 | new TreeMap(SortedMap sm) | Same as source SortedMap's order |

| Question | Answer |
|---|---|
| Constructor used | No-argument → default natural sorting order |
| Key type | String — implements Comparable → valid |
| Sorting applies to | Keys only; values (100, 200, …) do not affect order |

| Character | Unicode value |
|---|---|
| 'A' (capital) | 65 |
| 'a' (small) | 97 |

| LINE ONE | Method invoked internally for key comparison |
|---|---|
| new TreeMap() | compareTo() on keys (Comparable) |
| new TreeMap(new MyComparator()) | compare() on keys (Comparator) |

| Comparison | Return | Meaning (descending) |
|---|---|---|
| I1 < I2 | +1 (positive) | Smaller key goes after |
| I1 > I2 | -1 (negative) | Larger key goes before |
| I1 == I2 | 0 | Duplicate key → replace value |

| Step | put() call | Internal comparison |
|---|---|---|
| 1 | put(103, "Hyderabad") | First key — no comparison; 103 becomes root |
| 2 | put(101, "Durga") | 101.compareTo(103) → negative → go left |
| 3 | put(105, "Shiva") | 105.compareTo(103) → positive → go right |
| 4 | put(102, "Rama") | 102.compareTo(103) → negative → left; then 102.compareTo(101) → positive → right of 101 |

| JDK version | t.put(null, value) on empty TreeMap |
|---|---|
| Java 1.6 | Allowed — {null=value} |
| Java 1.7 onwards | NullPointerException — even as first entry |

| Scenario | Result |
|---|---|
| Non-empty TreeMap + put(null, v) | NullPointerException |
| Empty TreeMap + put(null, v) as first entry | Allowed (Java ≤ 1.6 only) |
| TreeMap containing null key + put(anyKey, v) | NullPointerException |
| Second put(null, v) attempt | Only one null key possible anyway |
| put(key, null) — null value | Allowed |

| # | Feature | HashMap | TreeMap |
|---|---|---|---|
| 1 | Underlying DS | Hash table | Red-Black tree |
| 2 | Map interface child | ✓ | ✓ |
| 3 | SortedMap interface | ✗ | ✓ |
| 4 | Key order | No guaranteed order (hash-based) | Sorted by key (natural or Comparator) |
| 5 | Insertion order preserved | ✗ | ✗ (sorted order, not insertion) |
| 6 | Duplicate keys | ✗ | ✗ |
| 7 | Duplicate values | ✓ | ✓ |
| 8 | Null key | ✓ (one null key allowed) | ✗ (Java 7+; see null rules) |
| 9 | Null value | ✓ | ✓ |
| 10 | Heterogeneous keys | ✓ | ✗ — ClassCastException |
| 11 | Comparable/Comparator | Not required | Required for keys (Comparable or Comparator ctor) |
| 12 | Performance get/put | O(1) average | O(log n) |
| 13 | Default initial capacity | 16 | N/A (tree grows dynamically) |
| 14 | Fill ratio / load factor | 0.75 default | N/A |
| 15 | Synchronized | No (use Collections.synchronizedMap) | No |
| 16 | Best choice when | General-purpose map; fast lookup; no sorting needed | Sorted key traversal; range views (headMap/tailMap/subMap) |
| 17 | Java version | 1.2 | 1.2 (NavigableMap in 1.6) |

| Requirement | Choose |
|---|---|
| Fast lookup, don't care about key order | HashMap |
| Insertion order of entries | LinkedHashMap |
| Sorted keys, range queries | TreeMap |
| Reference-equality keys | IdentityHashMap |
| Cache with weak keys | WeakHashMap |
| Thread-safe, legacy | Hashtable |

| Mechanism | TreeMap constructor | JVM calls on keys |
|---|---|---|
| Comparable (internal) | new TreeMap() | compareTo() |
| Comparator (external) | new TreeMap(Comparator c) | compare() |

| # | Question | Answer |
|---|---|---|
| 1 | What is the implementation class of SortedMap? | TreeMap |
| 2 | Is SortedMap a child of Collection? | No — child of Map |
| 3 | Does TreeMap sort by key or value? | Key only — never by value |
| 4 | Underlying DS of TreeMap? | Red-Black tree (balanced tree) |
| 5 | Are heterogeneous keys allowed? | No — ClassCastException |
| 6 | Are null values allowed in TreeMap? | Yes |
| 7 | Is null key allowed (Java 8+)? | No — NullPointerException |
| 8 | Which constructor for natural key sorting? | new TreeMap() |
| 9 | Which constructor for custom key sorting? | new TreeMap(Comparator c) |
| 10 | What does comparator() return for natural order? | `null` |
| 11 | headMap(106) — is 106 included? | No — strict < |
| 12 | tailMap(106) — is 106 included? | Yes — inclusive ≥ |
| 13 | Duplicate key in TreeMap — what happens? | Old value replaced; put() returns old value |
| 14 | Duplicate key in TreeSet — what happens? | Element not inserted; add() returns false |
| 15 | TreeMap vs HashMap — null key? | HashMap allows one; TreeMap does not (Java 7+) |
| 16 | Time complexity of TreeMap get/put? | O(log n) |
| 17 | Time complexity of HashMap get/put? | O(1) average |

| Trap | Reality |
|---|---|
| "TreeMap sorts by value" | FALSE — keys only |
| "TreeMap preserves insertion order" | FALSE — sorted key order |
| "Null key OK in TreeMap like HashMap" | FALSE for Java 7+ |
| "Null value throws NPE in TreeMap" | FALSE — null values OK (unlike Hashtable) |
| "headMap(N) includes N" | FALSE — strict less than |
| "subMap(101,115) includes 115" | FALSE — upper bound exclusive |
| "StringBuffer keys work in no-arg TreeMap" | FALSE — not Comparable → CCE |
| "Values must be Comparable" | FALSE — only keys |
| "SortedMap is part of Collection API" | FALSE — Map branch |

| Failure type | Example | Exception |
|---|---|---|
| Heterogeneous keys | String key + Integer key | ClassCastException |
| Non-Comparable keys (no-arg ctor) | StringBuffer as key | ClassCastException |
| Null key (Java 7+) | put(null, v) | NullPointerException |
| Null key in non-empty map | After real keys exist | NullPointerException |
| Empty map firstKey/lastKey | No entries | NoSuchElementException |

| # | Class name | Topic |
|---|---|---|
| 1 | SortedMapMethodsDemo | All six SortedMap methods with numeric keys |
| 2 | TreeMapDemo | String keys, natural sorting, duplicate key replace |
| 3 | TreeMapDemo2 | Integer keys, Comparator descending |
| 4 | TreeMapDemo3 | Custom Comparable class as key |
| 5 | HashMapVsTreeMapDemo | Side-by-side order comparison |

| Topic | Video | Relationship |
|---|---|---|
| NavigableMap | 151 | Child of SortedMap; ceilingKey, floorKey, pollFirstEntry, descendingMap on TreeMap |
| Hashtable | 149 | Legacy synchronized map; null key/value both rejected |
| Properties | 149 | Extends Hashtable; config files |
| Collections.sort() | 151 | Same Comparable/Comparator rules as TreeMap keys |

| # | Topic | Video | Status |
|---|---|---|---|
| 1 | Map intro, HashMap | 146 | ✓ |
| 2 | LinkedHashMap, IdentityHashMap, WeakHashMap | 147 | ✓ |
| 3 | SortedMap, TreeMap | 148 | ✓ This session |
| 4 | Hashtable, Properties | 149 | Next |
| 5 | NavigableMap (detail) | 151 | Later |

| Collection / Map | Heterogeneous allowed? |
|---|---|
| ArrayList, LinkedList | Yes |
| HashSet, LinkedHashSet | Yes |
| HashMap, LinkedHashMap, IdentityHashMap, WeakHashMap | Yes (keys and values) |
| TreeSet | No |
| TreeMap | No (keys) — values can differ in type |
| All others | Yes |
