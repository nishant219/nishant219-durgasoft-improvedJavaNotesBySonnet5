# Video 146 — Collections Part-11: Map Introduction, HashMap & HashMap vs Hashtable

## Video info

## Session overview

This session begins the Map module — the second half of the Collections Framework (first half = Collection; second half = Map). Sir states the full Map syllabus will take roughly 4–5 hours across multiple lectures.

What this lecture actually covers (~84 minutes):

- Recap: Comparable/Comparator is the most important Collections topic for interviews
- Full Map module agenda (roadmap for upcoming sessions)
- Introduction to Map — definition, keys/values, entries
- Map interface methods (put, putAll, get, remove, containsKey, containsValue, isEmpty, size, clear)
- Collection views of Map (keySet, values, entrySet)
- Map.Entry inner interface (getKey, getValue, setValue)
- HashMap — properties, four constructors, full demo program
- HashMap vs Hashtable — five differences (top interview question)
- How to get synchronized version of HashMap via Collections.synchronizedMap()
Scope note on LinkedHashMap: The video title and opening agenda list LinkedHashMap, but this session ends at HashMap vs Hashtable (~1:24:00). LinkedHashMap is not covered in this transcript — it is deferred to the next session along with IdentityHashMap, WeakHashMap, SortedMap, NavigableMap, and TreeMap.

## 00:04 — Recap: Comparable/Comparator is the crown jewel

Before starting Map, Sir reinforces:

- In the entire Collection Framework, the most worthy concept is Comparable vs Comparator.
- Interview favourites:
- What is the difference between Comparable and Comparator?
- How to implement customized sorting using Comparator?
- TreeSet was covered; TreeMap (coming later) uses the same Comparable/Comparator terminology — copy-paste logic.
- Set-related terminology was completed in the previous session.
Exam mantra: If Comparable/Comparator is clear, TreeMap learning becomes very simple.

## 00:55 — Full Map module agenda (roadmap)

Sir writes the complete Map syllabus on the board. This is the master checklist for the next several videos:

Version summary (board):

- Map concept → 1.2
- LinkedHashMap, IdentityHashMap, WeakHashMap → 1.4
- NavigableMap → 1.6
- Dictionary, Hashtable, Properties → 1.0 legacy classes
Sir explicitly says: Dictionary is abstract — we won't discuss it because abstract classes are not used directly.

## 05:33 — Introduction to Map

### Point 1: Map is NOT a child of Collection

This is the first and most important conclusion:

Collection Framework
├── First half  → Collection interface (List, Set, Queue)
└── Second half → Map interface (completely separate branch)

- Map is NOT a child interface of Collection.
- Map is nowhere related to Collection.
- Collection = group of individual objects.
- Map = group of objects as key–value pairs.
Underline on board: Map is not child interface of Collection.

### Point 2: When should we go for Map?

Rule (board): If we want to represent a group of objects as key–value pairs, then we should go for Map.

Real-world examples Sir gives:

- Web form parameters are stored internally in Map style.
- Servlet attributes are stored internally in Map style.
- Wherever name–value pair or key–value pair exists → highly recommended to use Map.
### Point 3: Visual model — keys, values, entries

Map
┌─────────────────────────────────────┐
│  Key (101)  →  Value (Durga)        │  ← Entry 1
│  Key (102)  →  Value (Ravi)         │  ← Entry 2
│  Key (103)  →  Value (Shiva)        │  ← Entry 3
│  Key (104)  →  Value (some name)    │  ← Entry 4
└─────────────────────────────────────┘

Board conclusions (copy exactly):

- Both keys and values are objects only (even if you store numbers, they are Integer objects via autoboxing).
- Duplicate keys are NOT allowed. (Roll number can never duplicate.)
- Duplicate values ARE allowed. (Two students can have the same name.)
- Each key–value pair is called one Entry — this is a technical term, not oral English. An interface named Entry exists for this reason.
- Map is considered as a collection of Entry objects.
## 13:41 — Map has its own methods (NOT Collection methods)

Because Map concept is different from Collection:

Why Collection methods don't apply:

- Collection: group of individual objects → add(singleObject).
- Map: group of key–value pairs → must add key and value simultaneously → put(key, value).
Map contains its own specific methods. Collection methods cannot be applied to Map because concepts are different.

## 15:41 — Map interface methods (detailed)

### Method 1: `Object put(Object key, Object value)`

Purpose: To add one key–value pair to the map.

The twist — return type is `Object`:

Sir emphasizes: return type is NOT void, NOT boolean — it is Object. Why?

Scenario walkthrough (board example):

Map m = new HashMap();

m.put(101, "Durga");   // key 101 not present → adds entry → returns null
m.put(102, "Shiva");   // key 102 not present → adds entry → returns null
m.put(101, "Ravi");    // key 101 ALREADY present → REPLACES old value → returns OLD value "Durga"

Rules for `put()`:

Board wording:

- If the key is already present → old value will be replaced with new value.
- Returns old value (so you know what got replaced).
Contrast with Set:

- In HashSet, add() with duplicate element → returns false, element NOT added.
- In Map, duplicate key → old value replaced, new value stored, old value returned.
Example to print old value:

System.out.println(m.put("Chiranjeevi", 1000));
// If "Chiranjeevi" key existed with value 700 → prints 700 (old value)

### Method 2: `void putAll(Map m)`

Purpose: To add a group of key–value pairs to the map.

- A group of key–value pairs = another Map (small map).
- Pass the small map → all its entries are added to the big map.
Map bigMap = new HashMap();
Map smallMap = new HashMap();
smallMap.put("A", 1);
smallMap.put("B", 2);

bigMap.putAll(smallMap);  // both entries added to bigMap

### Method 3: `Object get(Object key)`

Purpose: Returns the value associated with the specified key.

- If key exists → returns corresponding value.
- If key does NOT exist → returns null.
Analogy: Like getting a servlet parameter — you know parameter name (key), you want parameter value.

### Method 4: `Object remove(Object key)`

Purpose: Removes the entry associated with the specified key.

- You specify only the key.
- The entire entry (key + value together) is removed.
- There is no concept of "key removed but value remains" — without key, value cannot exist in Map.
### Method 5: `boolean containsKey(Object key)`

Purpose: Check whether a particular key is available in the map.

### Method 6: `boolean containsValue(Object value)`

Purpose: Check whether a particular value is available in the map.

### Method 7: `boolean isEmpty()`

Purpose: Check whether the map is empty.

### Method 8: `int size()`

Purpose: Returns the number of key–value pairs (entries) in the map.

### Method 9: `void clear()`

Purpose: Removes all key–value pairs from the map.

### Map methods summary table

## 27:47 — Collection views of Map (three special methods)

Given a map with entries:

Map: { 101→Durga, 102→Shiva, 103→Ravi, 104→some name }

### Method 1: `Set keySet()`

Requirement: "I want only keys."

- Return type: Set (not Map, not Collection).
- Why Set? Because duplicate keys are not allowed in Map → keys are unique → Set is appropriate.
Set s = m.keySet();
// Output style: [103, 102, 101, 104]  (square brackets — Set/Collection style)

### Method 2: `Collection values()`

Requirement: "I want only values."

- Return type: Collection (generic word — not Set).
- Why Collection? Duplicate values allowed; order not important.
Collection c = m.values();
// Output style: [500, 200, 800, 1000]  (square brackets)

### Method 3: `Set entrySet()`

Requirement: "Give me set of Entry objects."

- Each key–value pair = one Entry object.
- Return type: Set of Entry objects.
Set s1 = m.entrySet();
// Output style: [103=Ravi, 102=Shiva, 101=Durga, 104=...]
// Each element is one Entry object printed as key=value

### Why called "Collection Views of Map"

These three methods are applied on Map object, but return types use Collection terminology (Set, Collection):

Board term: These three methods are called Collection Views of Map — we are viewing the map in the form of collections (keys only, values only, or entries only).

## 31:43 — Map.Entry inner interface

### Entry concept (reinforcement)

- Map = group of key–value pairs.
- Each key–value pair = one Entry.
- Map = collection of Entry objects.
### Critical question: Is Entry always part of Map?

Answer: Yes. Without an existing Map object, there is no chance of an Entry object existing.

Therefore: Entry is an inner interface of Map interface.

interface Map {
    interface Entry {
        Object getKey();
        Object getValue();
        Object setValue(Object value);
    }
    // ... other Map methods
}

### Entry interface methods (only three)

Board points:

- Entry-specific methods — apply only on Entry object, not on Map directly.
- setValue() replaces current value with new value and returns old value (same pattern as put()).
### Iterating entries — full demo pattern

```java
import java.util.*;

public class HashMapEntryDemo {
    public static void main(String[] args) {
        Map m = new HashMap();
        m.put("Chiranjeevi", 700);
        m.put("Balayya", 800);
        m.put("Venkatesh", 200);
        m.put("Nagarjuna", 500);

        Set entrySet = m.entrySet();
        Iterator it = entrySet.iterator();

        while (it.hasNext()) {
            Map.Entry me = (Map.Entry) it.next();  // inner interface → Map.Entry

            System.out.println(me.getKey() + " ====== " + me.getValue());

            // Conditional update via entry
            if (me.getKey().equals("Nagarjuna")) {
                me.setValue(10000);  // changes value in the actual map
            }
        }

        System.out.println(m);  // Nagarjuna=10000 reflected here
    }
}
```

Important syntax note:

- Entry is inner interface → use Map.Entry (outer.inner pattern).
- Cast iterator's next element: (Map.Entry) it.next().
Timing trap Sir warns about:

- If you print map before calling setValue() inside the loop, you still see old value (500).
- Change happens during iteration; final System.out.println(m) shows updated value (10000).
## 39:16 — HashMap: first implementation class of Map

### HashMap properties (board — memorize all)

Board exact wording for null rules:

- Null is allowed for key — (only once).
- Null is allowed for values — (any number of times).
### HashMap constructors (same pattern as HashSet — four constructors)

Sir notes: HashSet constructors = HashMap constructors = LinkedHashMap constructors (same four patterns).

Constructor 1 board wording:

Creates an empty HashMap object with the default initial capacity 16 and default load factor 0.75.

Note: Map is NOT Collection → constructor 4 is HashMap(Map m), not HashMap(Collection c).

## 50:46 — HashMap demo program (HashMapDemo)

### Full program from the lecture

```java
import java.util.*;

public class HashMapDemo {
    public static void main(String[] args) {
        HashMap m = new HashMap();

        m.put("Chiranjeevi", 700);
        m.put("Balayya", 800);
        m.put("Venkatesh", 200);
        m.put("Nagarjuna", 500);

        System.out.println(m);
        // HashMap → NOT insertion order
        // Output: {Nagarjuna=500, Venkatesh=200, Balayya=800, Chiranjeevi=700}
        // Curly braces { } — Map toString style

        System.out.println(m.put("Chiranjeevi", 1000));
        // Key "Chiranjeevi" already exists → returns old value 700

        Set s = m.keySet();
        System.out.println(s);
        // [Nagarjuna, Venkatesh, Balayya, Chiranjeevi] — square brackets (Set)

        Collection c = m.values();
        System.out.println(c);
        // [500, 200, 800, 1000] — square brackets (Collection)

        Set s1 = m.entrySet();
        System.out.println(s1);
        // [Nagarjuna=500, Venkatesh=200, Balayya=800, Chiranjeevi=1000]

        // Iterate entries and modify
        Iterator it = s1.iterator();
        while (it.hasNext()) {
            Map.Entry me = (Map.Entry) it.next();
            System.out.println(me.getKey() + " ====== " + me.getValue());

            if (me.getKey().equals("Nagarjuna")) {
                me.setValue(10000);
            }
        }

        System.out.println(m);
        // Nagarjuna value now 10000
    }
}
```

### Output style rules (exam favourite)

### HashMap insertion order

- Cannot guarantee insertion order in output.
- Order depends on hash code of keys — we don't know hash codes, so cannot predict exact order.
- Do NOT call HashMap output "insertion order."
## 1:09:26 — HashMap vs Hashtable (TOP INTERVIEW QUESTION)

Sir calls this: "Minimum one crore times asked question in the interview room."

Analogy: Same differences as ArrayList vs Vector.

### Five differences (board — left: HashMap, right: Hashtable)

### Detailed explanation per point

Point 1 — Synchronization:

- HashMap methods = non-synchronized.
- Hashtable methods = synchronized (method-level locking).
Point 2 — Thread safety:

- HashMap: multiple threads can operate on same HashMap object simultaneously → not thread-safe.
- Hashtable: at a time only one thread allowed → thread-safe.
Point 3 — Performance:

- HashMap: no waiting → higher performance.
- Hashtable: threads wait for lock → lower performance.
Point 4 — Null (VERY IMPORTANT — many students miss this):

HashMap:   null key ✓ (once)    null value ✓ (any number of times)
Hashtable: null key ✗           null value ✗
           → NullPointerException if you try

Point 5 — Version / Legacy:

- HashMap → Java 1.2, part of new Collections Framework, not legacy.
- Hashtable → Java 1.0, legacy class (like Vector, Stack).
## 1:19:47 — How to get synchronized version of HashMap

By default HashMap is non-synchronized, but we can obtain a synchronized wrapper:

HashMap m = new HashMap();                        // non-synchronized
Map m1 = Collections.synchronizedMap(m);          // synchronized version

- m → original, non-synchronized, not thread-safe.
- m1 → synchronized, thread-safe wrapper around m.
Board wording:

By default HashMap is non-synchronized, but we can get synchronized version of HashMap by using synchronizedMap method of Collections class.

Same pattern as:

- Collections.synchronizedList() for ArrayList
- Collections.synchronizedSet() for HashSet
- Collections.synchronizedMap() for HashMap
## LinkedHashMap — deferred (not in this video)

The title mentions LinkedHashMap and the opening agenda lists it as topic #3, but this session ends before LinkedHashMap is taught. Expected in the next lecture:

- LinkedHashMap = HashMap + insertion order preserved
- Same constructors as HashMap
- Child class of HashMap (1.4)
Do not confuse with this session's content — everything above is what was actually covered on the board and in the demo.

## Board summary — copy for revision

### Map introduction (5 points)

- Map is not child interface of Collection.
- Use Map to represent group of objects as key–value pairs.
- Both keys and values are objects.
- Duplicate keys not allowed; duplicate values allowed.
- Each key–value pair = one Entry; Map = collection of Entry objects.
### Map interface methods (9 + 3 views)

Core methods: put, putAll, get, remove, containsKey, containsValue, isEmpty, size, clear

Collection views: keySet() → Set, values() → Collection, entrySet() → Set

### Entry interface (inner of Map)

- getKey(), getValue(), setValue(Object)
- Apply only on Entry objects obtained via entrySet() iterator
### HashMap (11 properties)

Hash table | No insertion order | Hash code of keys | No duplicate keys | Duplicate values OK | Heterogeneous OK | Null key once | Null values any times | Serializable + Cloneable | Not RandomAccess | Best for search

### HashMap vs Hashtable (5 differences)

Non-sync vs Sync | Not thread-safe vs Thread-safe | High perf vs Low perf | Null allowed vs Null NPE | 1.2 non-legacy vs 1.0 legacy

### Synchronized HashMap

Collections.synchronizedMap(hashMapObject)

## Quick reference — method return types

## Interview questions from this session

- Is Map a child interface of Collection? No — explain why.
- When should we go for Map? Key–value pair representation.
- What is an Entry? One key–value pair; Map.Entry inner interface.
- What does put() return when key already exists? Old value. When key is new? null.
- What are Collection Views of Map? keySet(), values(), entrySet().
- What methods does Entry interface define? getKey(), getValue(), setValue().
- What is the underlying data structure of HashMap? Hash table.
- Is insertion order preserved in HashMap? No — based on hash code of keys.
- Null rules for HashMap? Null key once; null values unlimited.
- HashMap vs Hashtable — five differences? Sync, thread-safe, performance, null, legacy.
- How to get synchronized HashMap? Collections.synchronizedMap(m).
- How many constructors in HashMap? Four — same pattern as HashSet.
- Default initial capacity and load factor? 16 and 0.75.
## What's next (Video 147+)

Per the agenda written at session start:

- LinkedHashMap
- IdentityHashMap
- WeakHashMap
- SortedMap interface
- NavigableMap (1.6)
- TreeMap (Comparable/Comparator applies here)
- Hashtable (legacy — detailed)
- Properties class

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Collections Part-11 \ | \ | Map \ | \ | Hashmap \ | \ | linked Hashmap |
| URL | https://www.youtube.com/watch?v=pSGvbJ7GJ68 |  |  |  |  |  |  |
| Video ID | pSGvbJ7GJ68 |  |  |  |  |  |  |
| Duration | 1h 24m 06s |  |  |  |  |  |  |
| Position | Video 146 of 203 in the Durga Sir OCJP/SCJP playlist |  |  |  |  |  |  |
| Source | YouTube auto-generated captions (yt-dlp) |  |  |  |  |  |  |
| Prerequisite | Video 145 (Set terminology + Comparable/Comparator postmortem). TreeMap later reuses Comparable/Comparator — must be crystal clear before TreeMap. |  |  |  |  |  |  |

| # | Topic | Java version | Notes |
|---|---|---|---|
| 1 | Map (introduction) | 1.2 | Interface — not part of Collection |
| 2 | HashMap | 1.2 | First implementation class |
| 3 | LinkedHashMap | 1.4 | Preserves insertion order |
| 4 | IdentityHashMap | 1.4 | Uses == not equals() |
| 5 | WeakHashMap | 1.4 | Weak references for keys |
| 6 | SortedMap | 1.2 | Interface for sorted maps |
| 7 | NavigableMap | 1.6 | Enhanced navigation methods |
| 8 | TreeMap | 1.2 | SortedMap implementation (Comparable/Comparator) |
| 9 | Dictionary | 1.0 | Abstract legacy class — skip |
| 10 | Hashtable | 1.0 | Legacy synchronized map |
| 11 | Properties | 1.0 | Hashtable child for config files |

| Key | Value |
|---|---|
| Roll number | Name |
| Mobile number | Address |
| IP address | Domain name |
| Attribute name | Attribute value |
| Parameter name | Parameter value |
| HTTP form parameter name | Parameter value |

| Collection thinking | Map thinking |
|---|---|
| Add one object | Add one key + value together |
| add(Object o) — one argument | put(Object key, Object value) — two arguments |
| Add group of objects | Add group of key–value pairs |
| addAll(Collection c) | putAll(Map m) |

| Situation | What happens | Return value |
|---|---|---|
| Key is new (not in map) | Entry added | null |
| Key already exists | Old value replaced with new value | Old value (the replaced one) |

| Method | Return type | Purpose |
|---|---|---|
| put(Object key, Object value) | Object | Add one entry; returns old value if key existed, else null |
| putAll(Map m) | void | Add all entries from another map |
| get(Object key) | Object | Get value for key; null if absent |
| remove(Object key) | Object | Remove entry by key |
| containsKey(Object key) | boolean | Is key present? |
| containsValue(Object value) | boolean | Is value present? |
| isEmpty() | boolean | Is map empty? |
| size() | int | Number of entries |
| clear() | void | Remove all entries |

| Method | Return type | What you get |
|---|---|---|
| keySet() | Set | Only keys |
| values() | Collection | Only values |
| entrySet() | Set | Set of Entry objects |

| Method | Return type | Purpose |
|---|---|---|
| getKey() | Object | Returns the key of this entry |
| getValue() | Object | Returns the value of this entry |
| setValue(Object value) | Object | Replaces value; returns old value |

| # | Property | Detail |
|---|---|---|
| 1 | Underlying data structure | Hash table |
| 2 | Insertion order | NOT preserved (hashing-based) |
| 3 | Based on | Hash code of keys (NOT values) |
| 4 | Duplicate keys | NOT allowed |
| 5 | Duplicate values | Allowed |
| 6 | Heterogeneous objects | Allowed for both key and value |
| 7 | Null key | Allowed — only once (duplicate keys not allowed) |
| 8 | Null values | Allowed — any number of times |
| 9 | Interfaces implemented | Serializable and Cloneable |
| 10 | RandomAccess | NOT RandomAccess |
| 11 | Best choice when | Frequent operation is search (hashing = fast lookup) |

| # | Constructor | Creates |
|---|---|---|
| 1 | HashMap() | Empty HashMap, default initial capacity 16, default load factor 0.75 |
| 2 | HashMap(int initialCapacity) | Empty HashMap with specified initial capacity; default load factor 0.75 |
| 3 | HashMap(int initialCapacity, float loadFactor) | Empty HashMap with specified capacity AND load factor |
| 4 | HashMap(Map m) | Equivalent HashMap from any existing Map object (inter-map conversion; NOT Collection conversion) |

| Object type | toString() style | Example |
|---|---|---|
| Collection / Set / List | Square brackets [ ] | [A, B, C] |
| Map | Curly braces { } with key=value | {1=Durga, 2=Ravi} |

| # | HashMap | Hashtable |
|---|---|---|
| 1 | Every method is non-synchronized | Every method is synchronized |
| 2 | Multiple threads allowed simultaneously → NOT thread-safe | Only one thread at a time → thread-safe |
| 3 | Threads not required to wait → relatively high performance | Threads must wait → relatively low performance |
| 4 | Null allowed for both key and value (key: once; value: any number of times) | Null NOT allowed for key or value → NullPointerException |
| 5 | Introduced in 1.2 — NOT legacy | Introduced in 1.0 — legacy class |

| Call | Return type | Notes |
|---|---|---|
| m.put(k, v) | Object | Old value or null |
| m.putAll(map) | void | — |
| m.get(k) | Object | Value or null |
| m.remove(k) | Object | Removed value or null |
| m.containsKey(k) | boolean | — |
| m.containsValue(v) | boolean | — |
| m.isEmpty() | boolean | — |
| m.size() | int | Entry count |
| m.clear() | void | — |
| m.keySet() | Set | Collection view |
| m.values() | Collection | Collection view |
| m.entrySet() | Set | Collection view |
| entry.getKey() | Object | Entry method |
| entry.getValue() | Object | Entry method |
| entry.setValue(v) | Object | Old value returned |
