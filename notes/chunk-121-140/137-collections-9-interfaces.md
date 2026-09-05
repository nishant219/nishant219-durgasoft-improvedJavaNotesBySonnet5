# Video 137 — Collections Part-2: 9 Key Interfaces

## Video info

## Session overview

Continuation of Collections Part-1 (Video 136). Part-1 covered: need for collections, difference between collections and arrays. This session introduces the nine key interfaces of the Java Collections Framework — the backbone for OCJP/SCJP and interview questions.

Mnemonic — 9 key interfaces:

- Collection
- List
- Set
- SortedSet
- NavigableSet
- Queue
- Map
- SortedMap
- NavigableMap
Framework split:

- First half (Collection side): interfaces 1–6 — represent a group of individual objects as a single entity.
- Second half (Map side): interfaces 7–9 — represent objects as key–value pairs.
- Map is not a child of Collection; both are separate roots within java.util collection framework.
### 00:04 — Recap & nine interfaces introduction

From the previous session:

- Why collections exist.
- Difference between collections (framework) and arrays.
Today's focus: nine key interfaces inside the collection framework. You must be able to name all nine from memory.

Sir's classroom mantra (repeat until automatic):

Nine key interfaces of collection framework.

### 00:37 — Listing all nine interfaces (board spell-out)

Spoken order on board: Collection → List → Set → SortedSet → NavigableSet → Queue → Map → SortedMap → NavigableMap.

### 02:27 — Interface 1: `Collection` (I)

#### When to use

If you want to represent a group of individual objects as a single entity, go for Collection.

Individual objects have no dependency on each other (unlike key–value pairs).

#### What it defines

Collection is an interface (not a class). It defines the most common methods applicable to any collection object:

- add(Object o) / add(E e)
- remove(Object o)
- isEmpty()
- size()
- contains(Object o)
- etc.
#### Root interface — with nuance

- In general, Collection is considered the root interface of the collection framework.
- Strictly speaking, the framework has two independent parts: Collection hierarchy and Map hierarchy — no inheritance link between them.
- In practice and in interviews, saying "Collection is the root interface" is accepted.
#### No direct concrete implementation

There is no concrete class that implements `Collection` directly.

Concrete classes implement child interfaces (List, Set, Queue, etc.), not Collection itself.

```java
import java.util.*;

// Collection is interface — cannot instantiate
// Collection c = new Collection(); // CE: Collection is abstract; cannot be instantiated

// Concrete classes implement child interfaces, not Collection directly
Collection<String> c1 = new ArrayList<>();   // via List
Collection<String> c2 = new HashSet<>();     // via Set
Collection<String> c3 = new LinkedList<>();  // via List

public class CollectionDemo {
    public static void main(String[] args) {
        Collection<String> c = new ArrayList<>();
        c.add("Durga");
        c.add("Java");
        System.out.println(c.size());    // prints 2
        System.out.println(c.isEmpty()); // prints false
        c.remove("Durga");
        System.out.println(c);           // prints [Java]
    }
}
```

#### Board conclusions — `Collection (I)`

- If we want to represent a group of individual objects as a single entity → go for Collection.
- Collection interface defines the most common methods applicable for any collection object.
- In general, Collection is considered as root interface of collection framework.
- There is no concrete class which implements `Collection` interface directly.
### 09:53 — Interview FAQ: `Collection` vs `Collections`

Most commonly asked entry-level / interview question.

Key insight: List never talks about sorting — it preserves insertion order. If you want to sort a List, use Collections.sort(list).

```java
import java.util.*;

public class CollectionVsCollectionsDemo {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>();
        list.add(30);
        list.add(10);
        list.add(20);

        // List preserves insertion order — no built-in sort
        System.out.println("Before sort: " + list); // prints Before sort: [30, 10, 20]

        Collections.sort(list);  // utility method in Collections CLASS
        System.out.println("After sort: " + list);  // prints After sort: [10, 20, 30]

        // Collections is utility class — cannot instantiate
        // Collections c = new Collections(); // CE: Collections() has private access
    }
}
```

#### Board notes — `Collections` (utility class)

- Collections is a utility class present in `java.util` package.
- Defines several utility methods for collection objects: sorting, searching, etc.
One-word interview answer: Collection = interface; Collections = class.

### 15:44 — Interface 2: `List` (I)

#### Hierarchy

List is the child interface of `Collection`.

#### When to use

If you want to represent a group of individual objects as a single entity where:

- Duplicates are allowed, AND
- Insertion order must be preserved (objects saved in the same order they were added)
→ go for `List`.

#### Specific properties of List

#### Implementation classes

Hierarchy diagram (board):

Collection
    └── List
         ├── ArrayList
         ├── LinkedList
         ├── Vector      (1.0 — legacy)
         └── Stack       (1.0 — legacy, extends Vector)

#### Vector/Stack re-engineering (1.2)

- List interface introduced in Java 1.2.
- Vector and Stack existed since Java 1.0 — before List existed.
- In 1.2, Vector and Stack were re-engineered (modified/updated) to implement `List` interface.
- The List link did not exist in 1.0/1.1.
```java
import java.util.*;

public class ListDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("First");
        list.add("Second");
        list.add("First");  // duplicate allowed

        System.out.println(list);
        // prints [First, Second, First] — insertion order preserved

        List<String> vector = new Vector<>();  // legacy, now implements List
        vector.add("A");
        vector.add("B");
        System.out.println(vector); // prints [A, B]

        Stack<String> stack = new Stack<>();   // legacy
        stack.push("bottom");
        stack.push("top");
        System.out.println(stack.pop()); // prints top
    }
}
```

### 23:56 — Interface 3: `Set` (I)

#### Hierarchy

Set is the child interface of `Collection`.

#### When to use

If you want to represent a group of individual objects as a single entity where:

- Duplicates are NOT allowed, AND
- Insertion order is NOT required (not preserved)
→ go for `Set`.

#### Specific properties

#### Implementation classes

Hierarchy:

Collection
    └── Set
         ├── HashSet
         └── LinkedHashSet

```java
import java.util.*;

public class SetDemo {
    public static void main(String[] args) {
        Set<String> set = new HashSet<>();
        set.add("Durga");
        set.add("Java");
        set.add("Durga");  // duplicate — silently ignored

        System.out.println(set.size()); // prints 2
        System.out.println(set);        // order NOT guaranteed
        // prints something like [Java, Durga] — insertion order not preserved

        Set<String> linkedSet = new LinkedHashSet<>();
        linkedSet.add("C");
        linkedSet.add("A");
        linkedSet.add("B");
        System.out.println(linkedSet);
        // prints [C, A, B] — LinkedHashSet preserves insertion order (exception among Sets)
    }
}
```

Note: LinkedHashSet preserves insertion order — Sir focuses on plain Set/HashSet behavior in this lecture (insertion order not required for Set interface contract).

### 28:17 — Interface 4: `SortedSet` (I)

#### Hierarchy

SortedSet is the child interface of `Set`.

#### When to use

If you want to represent a group of individual objects as a single entity where:

- Duplicates are NOT allowed, AND
- All objects inserted according to some sorting order (not insertion order)
→ go for `SortedSet`.

The name itself indicates: this set is sorted according to some sorting order.

#### Implementation class

No concrete class in this lecture for SortedSet alone — implementation comes via NavigableSet → TreeSet (covered next).

### 31:21 — Interface 5: `NavigableSet` (I)

#### Hierarchy

NavigableSet is the child interface of `SortedSet`.

#### Purpose

Contains several methods for navigation purposes:

- lower(e), floor(e), ceiling(e), higher(e)
- pollFirst(), pollLast()
- descendingSet(), etc.
Navigable = can be used for navigation (find previous/next element).

#### Implementation class

Version history:

- TreeSet existed since 1.2 but was modified in 1.6 to implement NavigableSet (same pattern as Vector/Stack → List in 1.2).
Hierarchy:

Collection → Set → SortedSet → NavigableSet → TreeSet

All interfaces except TreeSet are interfaces only.

```java
import java.util.*;

public class NavigableSetDemo {
    public static void main(String[] args) {
        NavigableSet<Integer> set = new TreeSet<>();
        set.add(30);
        set.add(10);
        set.add(20);
        set.add(10); // duplicate ignored

        System.out.println(set);           // prints [10, 20, 30] — sorted order
        System.out.println(set.lower(20)); // prints 10
        System.out.println(set.higher(20));// prints 30
        System.out.println(set.ceiling(15));// prints 20
        System.out.println(set.floor(15)); // prints 10
    }
}
```

### 35:17 — Interview FAQ: `List` vs `Set`

Very important interview question — know at least two differences.

Explanation for Set's non-insertion-order:

- In Set, objects are stored based on hash code (HashSet) or sorting order (TreeSet).
- You cannot expect objects to remain in the order you added them (except LinkedHashSet special case).
```java
import java.util.*;

public class ListVsSetDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("Durga");
        list.add("Ravi");
        list.add("Durga"); // duplicate OK
        System.out.println("List: " + list);
        // prints List: [Durga, Ravi, Durga]

        Set<String> set = new HashSet<>();
        set.add("Durga");
        set.add("Ravi");
        set.add("Durga"); // duplicate ignored
        System.out.println("Set: " + set);
        // prints Set: [Ravi, Durga] or [Durga, Ravi] — order not guaranteed
    }
}
```

### 38:02 — Interface 6: `Queue` (I)

#### Hierarchy

Queue is the child interface of `Collection`.

#### Real-world meaning

Queue = standing in line (passport office, temple, ticket counter) — FIFO (First In First Out).

#### Technical definition (Java API wording)

Prior to processing — if you want to represent a group of individual objects, go for Queue.

- Prior to processing = before the actual work happens (before sending mail, before offering service).
#### FIFO default behavior

- Usually Queue follows FIFO (First In First Out).
- But based on requirement, you can implement priority order → PriorityQueue.
#### Examples from lecture

- Mail sending application: Store all mail IDs in a queue before sending; first added mail sent first.
- Bulk SMS: 10 lakh mobile numbers stored in queue; message delivered in insertion order.
- Passport query queue: Stand in queue before officer processes your request.
#### Implementation classes

Version: Entire Queue concept introduced in Java 1.5.

Hierarchy (board):

Collection
    └── Queue
         ├── PriorityQueue
         └── BlockingQueue
              ├── PriorityBlockingQueue
              └── LinkedBlockingQueue

```java
import java.util.*;

public class QueueDemo {
    public static void main(String[] args) {
        // FIFO queue — mail sending scenario
        Queue<String> mailQueue = new LinkedList<>();
        mailQueue.offer("durga@gmail.com");
        mailQueue.offer("student@gmail.com");
        mailQueue.offer("java@gmail.com");

        System.out.println(mailQueue.poll()); // prints durga@gmail.com — first in, first out
        System.out.println(mailQueue.poll()); // prints student@gmail.com
        System.out.println(mailQueue.poll()); // prints java@gmail.com

        // PriorityQueue — not necessarily FIFO
        Queue<Integer> pq = new PriorityQueue<>();
        pq.offer(30);
        pq.offer(10);
        pq.offer(20);
        System.out.println(pq.poll()); // prints 10 — natural ordering (min-heap)
    }
}
```

#### Board notes — `Queue (I)`

- Child interface of Collection.
- Prior to processing → go for Queue.
- Usually follows FIFO order.
- Based on requirement, can implement priority order (PriorityQueue).
- Example: before sending mail, store all mail IDs; deliver in same order added.
### 53:21 — Collection vs Map: the great divide

Six interfaces covered so far (Collection side):

Collection, List, Set, SortedSet, NavigableSet, Queue

All six are for representing a group of individual objects — objects with no dependency on each other.

When objects are related as key–value pairs → cannot use Collection interfaces → must use Map.

Examples:

- Student roll number → name (roll number is unique key)
- Attribute name → attribute value (Servlet request attributes, parameters)
- Parameter name → parameter value
#### Board note (critical)

All the above interfaces (Collection, List, Set, SortedSet, NavigableSet, Queue) are meant for representing a group of individual objects.

If you want to represent a group of objects as key–value pairs → go for Map.

### 57:21 — Interface 7: `Map` (I)

#### NOT a child of Collection

- Map is NOT the child interface of Collection.
- Collection framework = two halves of a movie: first half Collection, second half Map.
- Map is still part of collection framework (same java.util package ecosystem) but separate hierarchy.
#### When to use

If you want to represent a group of objects as key–value pairs → go for Map.

#### Key rules

Recommended key choice: Use the unique identifier as key (e.g., roll number as key, name as value — not the reverse, because duplicate names exist).

#### Example (board)

Key (roll no)  →  Value (name)
1              →  Durga
2              →  Ravi
3              →  Shiva

Servlet/server examples using Map internally:

- parameter name → parameter value
- attribute name → attribute value
- Request attributes, session attributes
#### Implementation classes

Hashtable spelling trap:

- Correct: Hashtable (lowercase t)
- Wrong: HashTable → compile error — no such class
Dictionary hierarchy:

Dictionary (Abstract Class) — legacy, 1.0
    └── Hashtable
         └── Properties

#### Board conclusions — `Map (I)`

- Map is NOT child interface of Collection.
- If key–value pairs → go for Map.
- Both key and value are objects only.
- Duplicate keys not allowed; duplicate values can be duplicated.
```java
import java.util.*;

public class MapDemo {
    public static void main(String[] args) {
        Map<Integer, String> students = new HashMap<>();
        students.put(1, "Durga");
        students.put(2, "Ravi");
        students.put(3, "Shiva");
        students.put(2, "Ravi2"); // same key — replaces previous value

        System.out.println(students.get(1)); // prints Durga
        System.out.println(students);        // prints {1=Durga, 2=Ravi2, 3=Shiva}

        // Duplicate key not allowed — second put replaces
        students.put(1, "DurgaUpdated");
        System.out.println(students.get(1)); // prints DurgaUpdated

        // Duplicate values allowed
        Map<String, String> phoneBook = new HashMap<>();
        phoneBook.put("Durga", "9848022338");
        phoneBook.put("Ravi", "9848022338"); // same value, different keys — OK
        System.out.println(phoneBook); // prints {Durga=9848022338, Ravi=9848022338}

        // Map is NOT a Collection
        // Collection c = new HashMap(); // CE: HashMap cannot be converted to Collection
    }
}
import java.util.*;

public class HashtableSpellingDemo {
    public static void main(String[] args) {
        // Correct spelling — lowercase 't'
        Hashtable<String, String> ht = new Hashtable<>();
        ht.put("key", "value");
        System.out.println(ht); // prints {key=value}

        Properties props = new Properties();
        props.setProperty("user", "durga");
        System.out.println(props.getProperty("user")); // prints durga
    }
}

// class BadSpelling {
//     HashTable<String, String> ht = new HashTable<>(); // CE: cannot find symbol — HashTable
// }
```

### 1:07:36 — Interface 8: `SortedMap` (I)

#### Hierarchy

SortedMap is the child interface of `Map`.

#### When to use

If you want to represent a group of key–value pairs where entries are stored according to some sorting order of keys → go for SortedMap.

#### Critical rule — sorting on keys ONLY

Sorting should be based on key, but NOT based on value.

Value never participates in sorting.

#### Implementation

Comes via NavigableMap → TreeMap (next section).

### 1:10:50 — Interface 9: `NavigableMap` (I)

#### Hierarchy

NavigableMap is the child interface of `SortedMap`.

#### Purpose

Defines several methods for navigation purposes (analogous to NavigableSet).

#### Implementation class

Version history:

Hierarchy:

Map → SortedMap → NavigableMap → TreeMap

```java
import java.util.*;

public class NavigableMapDemo {
    public static void main(String[] args) {
        NavigableMap<Integer, String> map = new TreeMap<>();
        map.put(3, "Shiva");
        map.put(1, "Durga");
        map.put(2, "Ravi");

        System.out.println(map);              // prints {1=Durga, 2=Ravi, 3=Shiva} — sorted by KEY
        System.out.println(map.lowerKey(2));  // prints 1
        System.out.println(map.higherKey(2)); // prints 3
        System.out.println(map.firstEntry()); // prints 1=Durga
        System.out.println(map.lastEntry());  // prints 3=Shiva
    }
}
```

### 1:13:14 — All nine interfaces complete

Summary hierarchy (full framework):

COLLECTION SIDE (individual objects):
Collection (I)
├── List (I) → ArrayList, LinkedList, Vector*, Stack*
├── Set (I) → HashSet, LinkedHashSet
│    └── SortedSet (I)
│         └── NavigableSet (I) → TreeSet
└── Queue (I) → PriorityQueue, BlockingQueue → ...

MAP SIDE (key-value pairs):
Map (I) → HashMap, LinkedHashMap, WeakHashMap, IdentityHashMap, Hashtable*, Properties*
    └── SortedMap (I)
         └── NavigableMap (I) → TreeMap

* = legacy (1.0)

### 1:13:20 — Grand summary & "Collection King" interview story

Sir summarizes the decision tree an OCJP student (Ravi) wrote on paper in a CTS interview:

Interview lesson: Know the framework deeply — write the hierarchy confidently, don't just claim "Collection King" without substance.

```java
import java.util.*;

/**
 * Decision-tree demo matching Sir's interview white-paper summary.
 */
public class NineInterfacesSummaryDemo {
    public static void main(String[] args) {
        // LIST — duplicates + insertion order
        List<String> list = new ArrayList<>();
        list.add("A"); list.add("B"); list.add("A");
        System.out.println("List: " + list); // prints List: [A, B, A]

        // SET — no duplicates
        Set<String> set = new HashSet<>();
        set.add("A"); set.add("B"); set.add("A");
        System.out.println("Set: " + set); // prints Set: [A, B] (order varies)

        // SORTED SET — TreeSet via NavigableSet
        NavigableSet<Integer> sortedSet = new TreeSet<>();
        sortedSet.add(3); sortedSet.add(1); sortedSet.add(2);
        System.out.println("SortedSet: " + sortedSet); // prints SortedSet: [1, 2, 3]

        // QUEUE — prior to processing
        Queue<String> queue = new LinkedList<>();
        queue.offer("mail1"); queue.offer("mail2");
        System.out.println("Queue poll: " + queue.poll()); // prints Queue poll: mail1

        // MAP — key-value
        Map<Integer, String> map = new HashMap<>();
        map.put(1, "Durga"); map.put(2, "Ravi");
        System.out.println("Map: " + map); // prints Map: {1=Durga, 2=Ravi}

        // SORTED MAP — TreeMap via NavigableMap
        NavigableMap<Integer, String> sortedMap = new TreeMap<>();
        sortedMap.put(2, "Ravi"); sortedMap.put(1, "Durga");
        System.out.println("SortedMap: " + sortedMap); // prints SortedMap: {1=Durga, 2=Ravi}
    }
}
```

### 1:21:07 — Legacy classes in collection framework

Legacy = coming from old generation (Java 1.0).

Six legacy characters present in collection framework.

Re-engineering notes:

- Vector, Stack → re-engineered in 1.2 to implement List
- TreeSet → re-engineered in 1.6 to implement NavigableSet
- TreeMap → re-engineered in 1.6 to implement NavigableMap
### 1:22:11 — Preview topics (next sessions)

Sir briefly previews upcoming collection topics:

#### Sorting — Comparable vs Comparator

Used with SortedSet, SortedMap, TreeSet, TreeMap, and Collections.sort().

#### Cursors — traversing collections one-by-one

If you want to get objects one by one from a collection → Cursor concept:

#### Utility classes in collection framework

### 1:25:00 — Complete version matrix (board diagram)

### 1:31:24 — Session closing

- All nine key interfaces covered at overview level.
- Next session: each interface and implementation class in more detail (methods, programs, OCJP traps).
- Memorize: nine key interfaces, Collection vs Collections, List vs Set, Collection vs Map, legacy classes, version numbers.
## Quick reference tables

### Nine interfaces at a glance

### Collection vs Collections vs Map

### List vs Set (interview)

### Implementation class cheat sheet

## OCJP / interview checklist

- [ ] Name all 9 key interfaces from memory
- [ ] Explain Collection vs Collections in one sentence each
- [ ] Explain List vs Set (duplicates + insertion order)
- [ ] State when to use Queue ("prior to processing")
- [ ] State why Map is NOT child of Collection
- [ ] Map rules: duplicate keys, duplicate values, both are Objects
- [ ] SortedMap sorts by key only, not value
- [ ] List all 6 legacy members (Vector, Stack, Dictionary, Hashtable, Properties, Enumeration)
- [ ] Know 1.0 vs 1.2 re-engineering (Vector/Stack → List; TreeSet/TreeMap → Navigable*)
- [ ] Know version: Queue = 1.5, Navigable* = 1.6, LinkedHash* = 1.4
- [ ] Spell Hashtable correctly (lowercase t)
## Homework / self-test

- Draw the full hierarchy diagram from memory (Collection side + Map side).
- For each interface, write when to use in one line.
- Without looking, fill the version matrix.
- Write a program using all nine interface types as variable declarations with appropriate concrete classes.
- Explain to a friend why HashTable fails to compile but Hashtable works.
```java
import java.util.*;

public class SelfTestNineInterfaces {
    public static void main(String[] args) {
        Collection<String> c = new ArrayList<>();
        List<String> list = new ArrayList<>();
        Set<String> set = new HashSet<>();
        SortedSet<String> ss = new TreeSet<>();
        NavigableSet<String> ns = new TreeSet<>();
        Queue<String> q = new PriorityQueue<>();
        Map<Integer, String> m = new HashMap<>();
        SortedMap<Integer, String> sm = new TreeMap<>();
        NavigableMap<Integer, String> nm = new TreeMap<>();

        c.add("test"); list.add("test"); set.add("test");
        ss.add("test"); ns.add("test"); q.offer("test");
        m.put(1, "test"); sm.put(1, "test"); nm.put(1, "test");

        System.out.println("All 9 interface types demonstrated OK");
        // prints All 9 interface types demonstrated OK
    }
}
```

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | Video 137 of 203 |  |  |
| Playlist | Core Java With OCJP/SCJP |  |  |
| Title | Collections Part-2 \ | \ | 9 Key Interfaces |
| Instructor | Durga Sir |  |  |
| Duration | 1h 31m 50s |  |  |
| Video ID | n8RRsB2dP7k |  |  |
| URL | https://www.youtube.com/watch?v=n8RRsB2dP7k |  |  |
| Notes source | YouTube auto-captions |  |  |

| # | Interface | Package |
|---|---|---|
| 1 | Collection | java.util |
| 2 | List | java.util |
| 3 | Set | java.util |
| 4 | SortedSet | java.util |
| 5 | NavigableSet | java.util |
| 6 | Queue | java.util |
| 7 | Map | java.util |
| 8 | SortedMap | java.util |
| 9 | NavigableMap | java.util |

|  | Collection | Collections |
|---|---|---|
| Type | Interface | Utility class |
| Package | java.util | java.util |
| Purpose | Represent group of individual objects as single entity | Define utility/static methods for collection objects |
| Examples | add, remove, size, isEmpty | sort, reverse, shuffle, binarySearch, synchronizedList |

| Property | List behavior |
|---|---|
| Duplicates | Allowed |
| Insertion order | Must be preserved |
| Sorting order | Not guaranteed (List ≠ sorted) |

| Class | Java version | Notes |
|---|---|---|
| ArrayList | 1.2 | Resizable array |
| LinkedList | 1.2 | Doubly-linked list |
| Vector | 1.0 | Legacy class |
| Stack | 1.0 | Legacy class (extends Vector) |

| Property | Set behavior |
|---|---|
| Duplicates | Not allowed |
| Insertion order | Not preserved (objects stored based on hash code or sorting — unpredictable insertion order) |

| Class | Java version |
|---|---|
| HashSet | 1.2 |
| LinkedHashSet | 1.4 (newly added) |

| Class | Java version | Notes |
|---|---|---|
| TreeSet | 1.2 | Only implementation class of NavigableSet |

| Interface/Class | Version |
|---|---|
| Collection, Set, SortedSet, TreeSet | 1.2 |
| NavigableSet | 1.6 (new concept) |

| Feature | List | Set |
|---|---|---|
| Duplicates | Allowed | Not allowed |
| Insertion order | Preserved | Not preserved |

| Class | Notes |
|---|---|
| PriorityQueue | Priority-based ordering |
| BlockingQueue | Blocking operations (interface) |
| ↳ PriorityBlockingQueue | Child of BlockingQueue |
| ↳ LinkedBlockingQueue | Child of BlockingQueue |
| SynchronousQueue, DelayQueue, etc. | Mentioned briefly |

| Rule | Detail |
|---|---|
| Key type | Every key is an Object |
| Value type | Every value is an Object |
| Duplicate keys | NOT allowed |
| Duplicate values | Allowed |

| Class | Version | Notes |
|---|---|---|
| HashMap | 1.2 | General purpose |
| LinkedHashMap | 1.4 | Preserves insertion order of keys |
| WeakHashMap | 1.2 | Weak references for keys |
| IdentityHashMap | 1.4 | == instead of equals() |
| Hashtable | 1.0 | Legacy — note lowercase 't' |
| Properties | 1.0 | Legacy — child of Hashtable |

| Class | Version |
|---|---|
| TreeMap | 1.2 |

| Interface/Class | Version |
|---|---|
| Map, SortedMap, TreeMap | 1.2 |
| NavigableMap | 1.6 |

| Requirement | Interface | Implementation classes |
|---|---|---|
| Group of individual objects | Collection | (via child interfaces) |
| Duplicates + insertion order | List | ArrayList, LinkedList, Vector, Stack |
| No duplicates, no insertion order | Set | HashSet, LinkedHashSet |
| No duplicates + sorting order | SortedSet | (via NavigableSet) |
| + navigation support | NavigableSet | TreeSet |
| Prior to processing (FIFO) | Queue | PriorityQueue, BlockingQueue, ... |
| Key–value pairs | Map | HashMap, LinkedHashMap, WeakHashMap, IdentityHashMap |
| Key–value + sorted keys | SortedMap | (via NavigableMap) |
| + navigation support | NavigableMap | TreeMap |
| Legacy map | — | Hashtable, Properties (Dictionary hierarchy) |

| Legacy member | Type | Version |
|---|---|---|
| Vector | Class | 1.0 |
| Stack | Class | 1.0 |
| Dictionary | Abstract class | 1.0 |
| Hashtable | Class | 1.0 |
| Properties | Class | 1.0 |
| Enumeration | Interface | 1.0 |

| Need | Interface |
|---|---|
| Default natural sorting order | Comparable |
| Customized sorting order | Comparator |

| # | Cursor | Notes |
|---|---|---|
| 1 | Enumeration | Legacy (1.0) — only for legacy collections |
| 2 | Iterator | Universal (1.2+) |
| 3 | ListIterator | List-only, bidirectional (1.2+) |

| # | Class | Package |
|---|---|---|
| 1 | Collections | java.util |
| 2 | Arrays | java.util |

| Interface / Class | Version |
|---|---|
| Collection, List, Set, SortedSet, Map, SortedMap | 1.2 |
| ArrayList, LinkedList, HashSet, HashMap, TreeSet, TreeMap, WeakHashMap | 1.2 |
| LinkedHashSet, LinkedHashMap, IdentityHashMap | 1.4 |
| Queue, PriorityQueue, BlockingQueue, ... | 1.5 |
| NavigableSet, NavigableMap | 1.6 |
| Vector, Stack, Dictionary, Hashtable, Properties, Enumeration | 1.0 (legacy) |

| # | Interface | Parent | Represents | Key rule |
|---|---|---|---|---|
| 1 | Collection | — (root, collection side) | Individual objects | Common methods |
| 2 | List | Collection | Individual objects | Duplicates ✓, insertion order ✓ |
| 3 | Set | Collection | Individual objects | Duplicates ✗, insertion order ✗ |
| 4 | SortedSet | Set | Individual objects | + sorted insertion |
| 5 | NavigableSet | SortedSet | Individual objects | + navigation methods |
| 6 | Queue | Collection | Individual objects | Prior to processing, usually FIFO |
| 7 | Map | — (root, map side) | Key–value pairs | Duplicate keys ✗ |
| 8 | SortedMap | Map | Key–value pairs | Sorted by key only |
| 9 | NavigableMap | SortedMap | Key–value pairs | + navigation methods |

|  | Collection | Collections | Map |
|---|---|---|---|
| Kind | Interface | Utility class | Interface |
| Data model | Individual objects | N/A (helper) | Key–value pairs |
| Child of Collection? | Root (collection side) | No | No |
| Instantiate? | Via subtypes | No (private ctor) | Via subtypes |

|  | List | Set |
|---|---|---|
| Duplicates | Allowed | Not allowed |
| Insertion order | Preserved | Not preserved |

| Interface | Implementation classes |
|---|---|
| List | ArrayList, LinkedList, Vector, Stack |
| Set | HashSet, LinkedHashSet |
| NavigableSet | TreeSet |
| Queue | PriorityQueue, BlockingQueue, PriorityBlockingQueue, LinkedBlockingQueue |
| Map | HashMap, LinkedHashMap, WeakHashMap, IdentityHashMap, Hashtable, Properties |
| NavigableMap | TreeMap |
