# Video 147 — Collections Part-12: LinkedHashMap, IdentityHashMap & WeakHashMap

## Video info

## Session overview

This lecture completes the three small variations of HashMap that Sir promised at the end of Video 146. All three are child/special-case implementations of HashMap — same API (methods + constructors), with one or two behavioral differences each.

What this session covers (~62 minutes):

- LinkedHashMap — insertion order preserved (parallel to LinkedHashSet)
- Prerequisite recap: `==` vs `equals()` — reference vs content comparison
- IdentityHashMap — uses == (not equals()) to detect duplicate keys
- Prerequisite recap: Garbage Collection + `finalize()`
- WeakHashMap — weak keys; GC can reclaim entries when no external references remain
Closing summary (Sir's words): IdentityHashMap, normal HashMap, LinkedHashMap — all are exactly the same with small small differences. Master the difference table; that is the entire exam story.

## 00:05 — Roadmap: Three HashMap variations

After HashMap and HashMap-vs-Hashtable (Video 146), Sir moves to small variations of HashMap:

Sir's framing: "These are exactly same as HashMap with small small differences."

## 00:30 — LinkedHashMap: The HashSet / LinkedHashSet analogy

### Parallel from Set hierarchy (critical memory hook)

Sir connects to prior HashSet session:

Same pattern applies to Map:

Exam mantra: If you know HashSet vs LinkedHashSet, you already know 80% of HashMap vs LinkedHashMap.

## 01:53 — LinkedHashMap: Core conclusions (copy to notes)

### Point 1: Inheritance

```java
// LinkedHashMap extends HashMap
class LinkedHashMap extends HashMap { ... }
```

LinkedHashMap is the child class of HashMap.

### Point 2: Same as HashMap except listed differences

It is exactly same as HashMap (including methods and constructors) except the following differences.

All HashMap methods work identically: put, get, remove, keySet, entrySet, null key rules, load factor, etc. Only ordering and internal linking differ.

### Point 3: The three differences (comparison table)

That's all — Sir explicitly says no other differences between HashMap and LinkedHashMap.

### How the hybrid structure works (conceptual)

Hash table (for O(1) lookup by hash code)
    +
Doubly-linked list (maintains insertion-order chain across buckets)

Bucket[0] → entry A ←→ entry C ←→ entry B ←→ ...
Bucket[1] → ...

- Hash table gives fast get/put by key hash.
- Linked list thread maintains the order in which entries were inserted.
- When you iterate or print Map.toString(), LinkedHashMap walks the linked list — hence insertion order in output.
## 07:18 — Demo 1: HashMap vs LinkedHashMap (insertion order)

Sir reuses the HashMap demo program from Video 146 notes. Only the map declaration changes.

### Program skeleton

```java
import java.util.*;

class LinkedHashMapDemo {
    public static void main(String[] args) {
        // Case 1: HashMap
        Map m = new HashMap();
        m.put("Chiranjeevi", 700);
        m.put("Balakrishna", 800);
        m.put("Venkatesh", 200);
        m.put("Nagarjuna", 500);
        System.out.println(m);

        // Case 2: Replace HashMap with LinkedHashMap — ONLY THIS LINE CHANGES
        // Map m = new LinkedHashMap();
        // ... same put() calls ...
        // System.out.println(m);
    }
}
```

### Insertion order (how keys were added)

- Chiranjeevi → 700
- Balakrishna → 800
- Venkatesh → 200
- Nagarjuna → 500
### Output comparison

HashMap output (NOT insertion order):

```java
{Nagarjuna=500, Venkatesh=200, Balakrishna=800, Chiranjeevi=700}
```

Order depends on hash codes of key strings — not the order you called put().

LinkedHashMap output (insertion order preserved):

```java
{Chiranjeevi=700, Balakrishna=800, Venkatesh=200, Nagarjuna=500}
```

Exactly the order keys were inserted.

### Board note (Sir dictates)

In the above HashMap program, if we replace HashMap with LinkedHashMap, then output is:

```java
{Chiranjeevi=700, Balakrishna=800, Venkatesh=200, Nagarjuna=500}
```

— insertion order is preserved.

### Key takeaways

## 10:41 — LinkedHashMap application area: Cache-based applications

Sir connects to LinkedHashSet from an earlier session:

LinkedHashSet and LinkedHashMap are commonly used for developing cache-based applications.

### Why cache needs this combination

Real-world pattern: When you need a map that behaves like a cache — unique keys, fast access, and you care about which entry came first — LinkedHashMap (or LinkedHashSet for key-only caches) is the standard choice.

## 12:22 — Transition to IdentityHashMap: `==` vs `equals()` recap

Before IdentityHashMap, Sir must clarify reference vs content comparison. This is compulsory knowledge.

### Difference table (board — copy exactly)

### Example (Sir's standard Integer demo)

Integer i1 = new Integer(10);   // or Integer.valueOf(10)
Integer i2 = new Integer(10);

System.out.println(i1 == i2);      // false  — different objects, different addresses
System.out.println(i1.equals(i2)); // true   — same content (both represent 10)

Diagram:

i1 ──→ [ Integer object @ addr1, value=10 ]
i2 ──→ [ Integer object @ addr2, value=10 ]

i1 == i2        → false  (different addresses)
i1.equals(i2)   → true   (same integer value)

Sir: If you are aware of this point, IdentityHashMap concept is very easy — because this concept only plays a very important role there.

## 17:47 — IdentityHashMap

### Class name rule

`IdentityHashMap` — single word, no space. Do not write "Identity Hash Map" in exam answers.

### Core conclusion

IdentityHashMap is exactly same as HashMap (including methods and constructors) except the following difference:

Everything else — hash table, null rules, methods — behaves like HashMap except how duplicate keys are decided.

### Important clarification: hash code vs equals

Sir explicitly corrects a common mistake:

- Hash code → used to identify bucket location (where to place the entry).
- `equals()` / `==` → used to decide whether a key is duplicate (whether to replace existing entry).
Hash code is going to be considered to place / identify the location.

In HashMap, JVM will use equals method to identify duplicate keys.

## 18:20 — Demo 2: HashMap duplicate-key behavior (equals-based)

### Program

```java
import java.util.*;

class IdentityHashMapDemo {
    public static void main(String[] args) {
        Map m = new HashMap();

        Integer i1 = new Integer(10);
        Integer i2 = new Integer(10);

        m.put(i1, "P");
        m.put(i2, "Kalyan");

        System.out.println(m);
    }
}
```

### Step-by-step analysis (HashMap)

- m.put(i1, "P") → map has one entry: 10=P (key is i1 object, prints as 10 via Integer.toString())
- m.put(i2, "Kalyan") → JVM checks: is i2 a duplicate key?
- i2.equals(i1) → true (both Integer 10)
- Duplicate key → replace value: "P" replaced by "Kalyan"
- Only ONE entry in map (not two)
Output:

```java
{10=Kalyan}
```

### Board theory beside code

i1 and i2 are duplicate keys because i1.equals(i2) returns true.

## 24:32 — Demo 2 continued: IdentityHashMap (== -based)

Replace only the map declaration:

Map m = new IdentityHashMap();  // instead of HashMap

Same i1, i2, same put calls.

### Step-by-step analysis (IdentityHashMap)

- m.put(i1, "P") → one entry
- m.put(i2, "Kalyan") → JVM checks: is i2 duplicate?
- i2 == i1 → false (different objects)
- NOT duplicate → second entry added
- TWO entries in map
Output:

```java
{10=P, 10=Kalyan}
```

(Both keys print as 10 because Integer.toString() shows value — but they are distinct key objects internally.)

### Board theory

If we replace HashMap with IdentityHashMap:

- i1 and i2 are NOT duplicate keys

- because i1 == i2 returns false

- Output: {10=P, 10=Kalyan} — both entries present

### When to use IdentityHashMap

Use when you need reference identity as the key contract — not logical equality:

- Interning / canonicalization maps
- Graph algorithms where object identity matters
- Avoiding equals() override side effects
- Not for normal business-key maps (use HashMap)
## 32:31 — Transition to WeakHashMap: Garbage Collection recap

Sir asks: "What is WeakHashMap?"

Student joke: "The hash map which is very weak."

Sir: Correct — after the demo you will accept the name.

### GC story (Sir's narrative — understand the analogy)

- Object with no references → eligible for GC.
- GC "comes" to destroy it.
- Before destruction, GC calls `finalize()` on the object (cleanup / last wish — close DB connection, network connection, etc.).
- After finalize() completes → object destroyed.
### Key GC facts for this lecture

## 37:47 — WeakHashMap demo setup: Temp class

Sir creates a helper class to prove whether GC destroyed the key object.

```java
class Temp {
    public String toString() {
        return "temp";
    }

    protected void finalize() {
        System.out.println("finalize method called");
    }
}
```

- `toString()` → map prints {temp=durga} style output.
- `finalize()` → if this prints, Temp object was destroyed by GC.
## 39:51 — Demo 3: HashMap vs WeakHashMap (GC dominance)

### Program structure

```java
import java.util.*;

class WeakHashMapDemo {
    public static void main(String[] args) throws Exception {
        Map m = new HashMap();          // Case 1 — change to WeakHashMap for Case 2

        Temp t = new Temp();
        m.put(t, "durga");
        System.out.println(m);          // 1st print

        t = null;                       // external reference gone
        System.gc();                    // suggest GC

        Thread.sleep(5000);             // wait — did GC destroy key?

        System.out.println(m);          // 2nd print
    }
}
```

### Memory picture after `m.put(t, "durga")`

Reference variable t ──→ Temp object ←── also referenced as KEY inside HashMap
Value in map: "durga"

Map entry: {temp=durga}

### After `t = null; System.gc();`

t = null  →  no external reference to Temp object
BUT Temp object still referenced as KEY inside HashMap

Sir's story: GC comes to destroy the key object. Key "cries." HashMap intervenes — "This object is associated with me — how can you destroy it?" HashMap is stronger than GC in this case. JVM tells GC: "HashMap dominates — don't go there again."

### Case 1: HashMap result

Conclusion: Temp object NOT eligible for GC because it is associated with HashMap (strong reference from map to key).

HashMap dominates Garbage Collector.

## 48:06 — Case 2: WeakHashMap — same program, one line change

Map m = new WeakHashMap();   // only change

Same flow: create Temp, put, print, t=null, System.gc(), sleep, print again.

### WeakHashMap behavior

- Keys are held by weak references internally.
- When no external strong references remain to the key object, GC can reclaim it.
- Sir's story: GC tells WeakHashMap "You are already weak — don't open your mouth." GC dominates WeakHashMap.
### Case 2: WeakHashMap result

Sequence observed on console:

```java
{temp=durga}
finalize method called
{}
```

When key object destroyed → entry removed from map → value "durga" also gone automatically.

Garbage Collector dominates WeakHashMap.

## 52:27 — WeakHashMap: Core conclusions (copy to notes)

WeakHashMap is exactly same as HashMap except the following difference:

### Board notes (Sir dictates for above example)

With HashMap:

In the above example, temp object not eligible for GC because it is associated with HashMap.

Output both times: {temp=durga}

With WeakHashMap (replace HashMap):

Then temp object eligible for GC.

Output: first {temp=durga}, then finalize method called, then {}

### Naming mnemonic (Sir-approved)

WeakHashMap = the HashMap which is very weak (compared to normal HashMap which is strong against GC).

## Master comparison: All four Map implementations

## Hierarchy diagram (board)

Map (I)
 └── HashMap (C)                    ← Java 1.2
      ├── LinkedHashMap (C)         ← 1.4, insertion order
      └── WeakHashMap (C)           ← 1.4, weak keys

Map (I)
 └── IdentityHashMap (C)            ← 1.4, == for keys (NOT a HashMap subclass)

Note: In the API, IdentityHashMap implements Map directly (does not extend HashMap), but Sir teaches it alongside HashMap as "same except one difference" — same exam treatment.

## OCJP / SCJP exam rapid-fire Q&A

- LinkedHashMap is child of which class? → HashMap.
- Main difference HashMap vs LinkedHashMap? → Insertion order preserved in LinkedHashMap; hybrid linked list + hash table.
- LinkedHashMap introduced in which version? → 1.4.
- HashMap uses which method to detect duplicate keys? → equals().
- IdentityHashMap uses which operator? → == (reference comparison).
- i1 and i2 both `new Integer(10)` — how many entries in HashMap after put both? → One (equals true).
- Same i1, i2 in IdentityHashMap? → Two (== false).
- LinkedHashSet + LinkedHashMap common use? → Cache-based applications.
- WeakHashMap — who dominates, map or GC? → GC dominates WeakHashMap.
- HashMap — key in map, external ref null — eligible for GC? → No; HashMap dominates GC.
- WeakHashMap — same scenario? → Yes, eligible; entry removed when key collected.
- Who calls finalize()? → Garbage Collector, just before destroying object.
## Complete demo programs (copy-paste ready)

### LinkedHashMapDemo.java

```java
import java.util.*;

class LinkedHashMapDemo {
    public static void main(String[] args) {
        Map m = new LinkedHashMap();
        m.put("Chiranjeevi", 700);
        m.put("Balakrishna", 800);
        m.put("Venkatesh", 200);
        m.put("Nagarjuna", 500);
        System.out.println(m);
        // {Chiranjeevi=700, Balakrishna=800, Venkatesh=200, Nagarjuna=500}
    }
}
```

### IdentityHashMapDemo.java

```java
import java.util.*;

class IdentityHashMapDemo {
    public static void main(String[] args) {
        Map m = new IdentityHashMap();

        Integer i1 = new Integer(10);
        Integer i2 = new Integer(10);

        m.put(i1, "P");
        m.put(i2, "Kalyan");

        System.out.println(m);
        // HashMap:      {10=Kalyan}
        // IdentityHashMap: {10=P, 10=Kalyan}
    }
}
```

### WeakHashMapDemo.java

```java
import java.util.*;

class Temp {
    public String toString() { return "temp"; }
    protected void finalize() {
        System.out.println("finalize method called");
    }
}

class WeakHashMapDemo {
    public static void main(String[] args) throws Exception {
        Map m = new WeakHashMap();

        Temp t = new Temp();
        m.put(t, "durga");
        System.out.println(m);

        t = null;
        System.gc();
        Thread.sleep(5000);

        System.out.println(m);
        // HashMap:     {temp=durga} then {temp=durga}
        // WeakHashMap: {temp=durga} then finalize... then {}
    }
}
```

## Common mistakes (exam traps)

## What's next (Video 148+)

Per Map module agenda from Video 146:

- SortedMap interface
- NavigableMap (Java 1.6)
- TreeMap (Comparable / Comparator — same rules as TreeSet)
- Hashtable (legacy, detailed)
- Properties class
## One-page revision sheet

LINKEDHASHMAP     = HashMap + insertion order + linked list chain (1.4)
IDENTITYHASHMAP   = HashMap but duplicate key = == not equals() (1.4)
WEAKHASHMAP       = HashMap but weak keys; GC wins over map (1.4)

HashMap:           equals() for dup keys | strong keys | GC loses
LinkedHashMap:     + insertion order preserved
IdentityHashMap:   == for dup keys
WeakHashMap:       weak keys | GC wins | entry vanishes when key collected

Cache apps → LinkedHashSet + LinkedHashMap
Integer i1,i2 both 10 → HashMap:1 entry | IdentityHashMap:2 entries
t=null; gc(); → HashMap still has entry | WeakHashMap → {}

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Collections Part-12 \ | \ | linked Hashmap |
| URL | https://www.youtube.com/watch?v=AVdD987trsc |  |  |
| Video ID | AVdD987trsc |  |  |
| Duration | 1h 01m 42s |  |  |
| Position | Video 147 of 203 in the Durga Sir OCJP/SCJP playlist |  |  |
| Source | YouTube auto-generated captions (yt-dlp) |  |  |
| Prerequisite | Video 146 (HashMap introduction, methods, HashMap vs Hashtable). Video 142 area (HashSet / LinkedHashSet) helps for the LinkedHashMap analogy. GC + finalize() from earlier Object-class sessions required for WeakHashMap. |  |  |

| # | Class | Java version | One-line difference from HashMap |
|---|---|---|---|
| 1 | LinkedHashMap | 1.4 | Preserves insertion order |
| 2 | IdentityHashMap | 1.4 | Uses `==` (not equals()) for duplicate-key detection |
| 3 | WeakHashMap | 1.4 | Weak keys — GC dominates over map when no external refs |

|  | HashSet | LinkedHashSet |
|---|---|---|
| Parent | Implements Set | Child class of HashSet |
| Underlying DS | Hash table | Linked list + hash table (hybrid) |
| Insertion order | Not preserved (based on hash code) | Preserved |

|  | HashMap | LinkedHashMap |
|---|---|---|
| Parent | Implements Map | Child class of HashMap |
| Underlying DS | Hash table | Linked list + hash table (hybrid) |
| Insertion order | Not preserved (based on hash code of keys) | Preserved |

| # | HashMap | LinkedHashMap |
|---|---|---|
| 1 | Underlying data structure is hash table | Underlying data structure is a combination of linked list + hash table (hybrid / mixed data structure) |
| 2 | Insertion order is not preserved; ordering based on hash code of keys | Insertion order is preserved |
| 3 | Introduced in Java 1.2 | Introduced in Java 1.4 |

| Question | HashMap | LinkedHashMap |
|---|---|---|
| Is insertion order preserved? | No | Yes (by default) |
| What determines iteration/print order? | Hash code of keys | Order of put() calls |
| Code change needed? | — | Replace new HashMap() with new LinkedHashMap() |

| Requirement | How LinkedHashMap satisfies it |
|---|---|
| Fast lookup by key | Hash table backing (like HashMap) |
| Duplicate keys not allowed | Map contract |
| Predictable iteration order | Insertion order preserved |
| LRU-style caches (advanced) | LinkedHashMap has access-order constructor (true flag) — Sir does not demo it here, but insertion-order is the foundation |

|  | == (double equal operator) | equals() method |
|---|---|---|
| Meant for | Reference comparison (address comparison) | Content comparison |
| Returns true when | Both references point to the same object | Object contents are logically equal (per class definition) |
| Default Object.equals() | Same as == unless overridden | — |

|  | HashMap | IdentityHashMap |
|---|---|---|
| Duplicate key detection | JVM uses `equals()` method → content comparison | JVM uses `==` (double equal operator) → reference comparison |
| Introduced in | 1.2 | 1.4 |

| Fact | Detail |
|---|---|
| Who calls finalize()? | Garbage Collector |
| When? | Just before destroying an object |
| Purpose? | Perform cleanup activities |
| Can you rely on it in production? | No (deprecated in Java 9+, removed in later JDKs — but exam still tests the concept) |

| Print | Output | finalize() called? |
|---|---|---|
| 1st System.out.println(m) | {temp=durga} | No |
| After t=null, gc(), sleep | {temp=durga} | No |

| Print | Output | finalize() called? |
|---|---|---|
| 1st print | {temp=durga} | No |
| After gc + sleep | `{}` (empty map) | Yes — finalize method called |

|  | HashMap | WeakHashMap |
|---|---|---|
| Key reference strength | Strong — map holds key strongly | Weak — keys are weakly referenced |
| Object with no external refs but key in map | NOT eligible for GC | Eligible for GC |
| Who dominates? | HashMap dominates GC | GC dominates WeakHashMap |
| Introduced in | 1.2 | 1.4 |

| Feature | HashMap | LinkedHashMap | IdentityHashMap | WeakHashMap |
|---|---|---|---|---|
| Parent / relation | Map impl | extends HashMap | Map impl (separate class) | extends HashMap |
| Underlying DS | Hash table | Linked list + hash table | Hash table (identity buckets) | Hash table + weak refs |
| Insertion order | No | Yes | No | No |
| Duplicate key test | equals() | equals() | `==` | equals() |
| GC vs map (key with no ext ref) | Map protects key | Map protects key | Map protects key | GC can collect key |
| Java version | 1.2 | 1.4 | 1.4 | 1.4 |
| Common use | General purpose | Caches, ordered maps | Identity-based keys | Caches, metadata maps, listeners |

| Mistake | Truth |
|---|---|
| "Hash code decides duplicate keys" | Hash code picks bucket; `equals()`/`==` decides duplicate |
| "IdentityHashMap extends HashMap" | Separate class; same behavioral teaching, not inheritance |
| "WeakHashMap values are weak" | Only keys are weak; Sir's demo focuses on key GC |
| "System.gc() guarantees immediate collection" | Only suggests GC; sleep() helps demo observe async behavior |
| "LinkedHashMap sorts keys" | Preserves insertion order, not natural/comparator sorting (that's TreeMap) |
| Writing "Identity Hash Map" as class name | Wrong — `IdentityHashMap` one word |
