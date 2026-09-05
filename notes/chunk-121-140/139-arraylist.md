# Video 139 — ArrayList & LinkedList (Collections Part-4)

## Video info

### 00:05 — Session recap: ArrayList basics from previous lecture

In the last session, Durga Sir covered:

- How to create an ArrayList
- A demo program for ArrayList
- Properties of ArrayList
This session continues with important conclusions related to ArrayList and concepts applicable to any collection class, then moves to the next level (LinkedList preview and demo).

### 00:29 — Why do we use Collections? (Container analogy)

Collection in Java is equivalent to container in C++.

Primary purpose of a collection / container:

- To hold objects (store data)
- To transfer objects from one location to another location
Real-world analogies Durga Sir uses:

Key takeaway: Collections are not only for local storage — a very common requirement is to hold data and transfer data across locations (including across a network).

### 01:57 — Serializable: mandatory for network transfer

To send a Java object across a network, that object must be Serializable.

Requirement: Transfer object across network
         ↓
Object must implement java.io.Serializable

Why this matters for collections:

- Usual requirement with collections = hold objects and transfer the whole collection
- To support this, every collection class by default implements `Serializable`
Quick exam drill — does each class implement Serializable?

Scenario walk-through:

- Person in Hyderabad sends a collection of Student objects over the network
- Person in London receives the collection object
- They perform operations on it
- If something goes wrong and the object gets disturbed, they need the original state back
Instead of requesting Hyderabad to resend, we can create a duplicate (clone) immediately after receiving and experiment on the clone.

### 03:31 — Cloneable: duplicate object for safe operations

To produce an exact duplicate (cloned) object, the object must implement `Cloneable`.

Requirement: Create exact duplicate / backup copy
         ↓
Object must implement java.lang.Cloneable

Advantage of cloning after network receive:

- Perform any operation on the duplicate without fear
- If something goes wrong → recover using the original clone
- Can compare updated state vs original state at any point
Rule: Every collection class already implements `Cloneable` (in addition to Serializable).

### 05:00 — Board summary: hold, transfer, Serializable, Cloneable

Usual purpose of collections:

To hold and transfer objects from one location to another location (container).

To provide support for this requirement:

Every collection class by default implements Serializable and Cloneable interfaces.

This rule applies to every collection — not only ArrayList.

### 06:54 — RandomAccess: only ArrayList and Vector

Among all collection classes, only two implement the `RandomAccess` interface:

- `ArrayList`
- `Vector`
What RandomAccess means (from interface documentation):

We can access any random element with the same speed.

Array-based intuition:

Because ArrayList and Vector implement RandomAccess, any index can be reached in O(1) time via direct array indexing.

Exam consequence:

If your frequent operation is retrieval (get element by index), `ArrayList` (or Vector) is the best choice.

Important: This ability is NOT available in every collection — only ArrayList and Vector.

### 10:48 — LinkedList does NOT implement RandomAccess

Observe the difference — LinkedList implements Serializable and Cloneable but not RandomAccess.

### 11:00 — RandomAccess interface details

Because it has no methods, it is a marker interface — it signals capability; the actual random-access behaviour is built into the ArrayList/Vector implementation internally.

### 13:13 — Exam-style `instanceof` question

```java
import java.util.ArrayList;
import java.util.LinkedList;
import java.io.Serializable;
import java.lang.Cloneable;
import java.util.RandomAccess;

public class CollectionInstanceOfDemo {
    public static void main(String[] args) {
        ArrayList<Object> l1 = new ArrayList<>();
        LinkedList<Object> l2 = new LinkedList<>();

        System.out.println(l1 instanceof Serializable);   // true  — ArrayList implements Serializable
        System.out.println(l2 instanceof Cloneable);        // true  — LinkedList implements Cloneable
        System.out.println(l1 instanceof RandomAccess);     // true  — ArrayList implements RandomAccess
        System.out.println(l2 instanceof RandomAccess);     // false — LinkedList does NOT implement RandomAccess
    }
}
```

Answer key:

Must remember for exam:

- ArrayList and Vector → implement RandomAccess
- LinkedList → does not implement RandomAccess
- Every collection class → implements Serializable and Cloneable
### 14:52 — When is ArrayList the BEST choice?

Best choice when: frequent operation = retrieval (get by index)

Examples:

- "What is the 1st element?"
- "What is the 10th element?"
- "What is the 11th element?"
All answered instantly because of RandomAccess / array backing.

### 15:26 — When is ArrayList the WORST choice? (Insertion in middle)

Worst choice when: frequent operation = insertion in the middle (not insertion at last — that is fine)

Example scenario:

- ArrayList with 1 crore (10 million) elements: [A, B, C, D, ...]
- Requirement: insert M at index 1 (second position)
```java
import java.util.ArrayList;

public class ArrayListMiddleInsertDemo {
    public static void main(String[] args) {
        ArrayList<String> list = new ArrayList<>();
        // Imagine list already has 1 crore elements: A, B, C, D, ...

        list.add(1, "M");  // insert M at index 1
        // Result: A, M, B, C, D, ...
    }
}
```

What happens internally:

- Index 1 already has B
- To place M at index 1, `B` must shift to index 2
- `C` shifts to index 3, `D` shifts to index 4, … and so on
- 1 crore shift operations required just to insert one element!
Durga Sir's humorous remark: "Maybe after 6 months it will tell successfully inserted."

Conclusion: Insertion in the middle of a large ArrayList is extremely costly — not recommended.

### 17:18 — ArrayList worst for deletion in middle too

Removal at index 1:

```java
import java.util.ArrayList;

public class ArrayListMiddleRemoveDemo {
    public static void main(String[] args) {
        ArrayList<String> list = new ArrayList<>();
        // Imagine 1 crore elements: A, B, C, D, ...

        list.remove(1);  // remove element at index 1 (B)
        // Result: A, C, D, ... (gap closed by shifting)
    }
}
```

What happens internally:

- Element at index 1 (B) is removed → cell becomes vacant
- C moves to index 1, D moves to index 2, … 1 crore shifts
Board conclusions:

### 19:56 — If middle insert/delete is frequent → use LinkedList

When frequent operation = insertion or deletion in the middle:

- `ArrayList` = worst choice
- `LinkedList` = highly recommended (best choice)
(Detailed LinkedList explanation follows later in this lecture.)

### 20:46 — ArrayList vs Vector: interview favourite

Very common interview question: "What is the difference between ArrayList and Vector?"

Durga Sir says: attend 10 interviews → in 6 to 8 you will get this question.

#### Comparison table

#### Thread safety detail

ArrayList:

- Multiple threads (T1, T2, T3, …) can operate simultaneously
- Not thread-safe — data corruption possible
- Advantage: no waiting → better performance
Vector:

- T1 operates → then T2 → then T3 (one at a time)
- Thread-safe
- Disadvantage: waiting increases → performance problems
#### Version / legacy

### 29:40 — Modern interview twist: synchronized ArrayList

Old question: difference between ArrayList and Vector.

New question (these days): "I want to use ArrayList only, but I need thread safety — how do I get a synchronized version of an ArrayList object?"

Answer: Use `Collections.synchronizedList()` from the `Collections` utility class.

#### Method signature (from board)

```java
public static <T> List<T> synchronizedList(List<T> list)
```

#### Example

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class SynchronizedArrayListDemo {
    public static void main(String[] args) {
        ArrayList<String> l = new ArrayList<>();  // non-synchronized (default)
        List<String> l1 = Collections.synchronizedList(l);  // synchronized wrapper

        // l  → non-synchronized, not thread-safe, high performance
        // l1 → synchronized, thread-safe, lower performance
    }
}
```

Board notes:

By default, ArrayList is non-synchronized.

But we can get synchronized version of ArrayList object by using `synchronizedList()` method of `Collections` class.

### 35:33 — Synchronized Set and Map (same pattern)

Similarly, Collections class provides:

```java
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class SynchronizedCollectionDemo {
    public static void main(String[] args) {
        Set<String> syncSet = Collections.synchronizedSet(new HashSet<>());
        Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
        // Use syncSet and syncMap for thread-safe operations
    }
}
```

### 38:37 — LinkedList: best for middle insertion/deletion (memory structure)

When frequent operation = insertion/deletion in the middle → LinkedList is the best choice.

#### Why ArrayList is slow for middle ops

- Elements stored in consecutive memory locations (array)
- Insert/remove in middle → shift nearly all elements
#### LinkedList memory structure

- Elements (nodes) stored in non-consecutive memory locations
- Example addresses (Durga Sir's board): one node at C, next at K, next at Abids, next at KPHB, next at Uppal Nag — scattered across memory
- Each node stores:
- Data
- Next node address (singly linked) OR Previous + Next addresses (doubly linked)
Java's `LinkedList` uses: Doubly linked list (double linked list) as underlying data structure.

#### Insertion in middle — only pointer changes

To insert M at index 1:

```java
import java.util.LinkedList;

public class LinkedListMiddleInsertDemo {
    public static void main(String[] args) {
        LinkedList<String> list = new LinkedList<>();
        // Existing: A -> B -> C -> D -> ...

        list.add(1, "M");  // insert M at index 1
        // Result: A -> M -> B -> C -> D -> ...
    }
}
```

Internal steps (conceptual):

- Create a new node with data M
- Reassign left pointer and right pointer of adjacent nodes
- No shift operations — just 2 or 4 pointer changes
Insertion in the middle = matter of 2 or 4 pointer changes only.

#### Deletion in middle — also easy

```java
import java.util.LinkedList;

public class LinkedListMiddleRemoveDemo {
    public static void main(String[] args) {
        LinkedList<String> list = new LinkedList<>();
        // Existing: A -> B -> C -> D -> ...

        list.remove(2);  // remove 3rd element (C)
        // Just remove pointers; orphaned node eligible for GC
    }
}
```

Steps: Remove pointers connecting the node → re-link previous to next → removed node becomes eligible for garbage collection.

### 42:53 — Every strength has a weakness (LinkedList trade-off)

Durga Sir's philosophy note: if a data structure is strong in one area, it is weak in another.

### 45:28 — LinkedList WORST choice for retrieval

If frequent operation = retrieval → LinkedList is the worst choice.

Why?

To get the 1st element: direct — ~1 second.

To get the 2nd element:

- Ask 1st node for address of 2nd node
- Go to that address → read data
- Takes ~2 seconds
To get the 3rd element: traverse 1 → 2 → 3 → ~3 seconds.

To get the 10th element: ~10 seconds (or "after 10 years" as Sir jokes for very large lists).

No direct communication with arbitrary index — must traverse from head (or tail) via next/previous pointers.

### 47:24 — LinkedList properties (preview for next LinkedList lecture)

Durga Sir boards these properties (full LinkedList lecture continues next):

### 51:23 — LinkedList constructors (only TWO — no capacity)

Why no capacity constructor?

- Capacity concept applies when objects stored in consecutive memory (arrays)
- LinkedList nodes are scattered — capacity terminology not applicable
ArrayList has 3 constructors (no-arg, initial capacity, collection conversion).

LinkedList has only 2 constructors:

#### Constructor 1 — no-arg: empty LinkedList

LinkedList<String> l = new LinkedList<>();
// Creates an empty LinkedList object

#### Constructor 2 — collection conversion

```java
import java.util.Arrays;
import java.util.Collection;
import java.util.LinkedList;

public class LinkedListConstructorsDemo {
    public static void main(String[] args) {
        // Constructor 1: empty LinkedList
        LinkedList<String> l = new LinkedList<>();

        // Constructor 2: equivalent LinkedList from existing collection
        Collection<String> c = Arrays.asList("A", "B", "C");
        LinkedList<String> l2 = new LinkedList<>(c);
        // Creates equivalent LinkedList for the given collection
    }
}
```

### 57:16 — LinkedList class-specific methods (Stack & Queue support)

LinkedList is commonly used to implement Stack and Queue data structures.

Six specific methods defined in LinkedList class:

These methods can be applied only on LinkedList objects — not on other List implementations.

Board note:

Usually we can use LinkedList to develop stacks and queues.

To provide support, LinkedList class defines the following specific methods.

(Durga Sir also mentions CM data structures lab — linked-list-based stack/queue programs are common and worth keeping in "slips" for lab exams.)

### 01:01:41 — LinkedList demo program (full board example)

Durga Sir converts the discussion into a demo program:

```java
import java.util.LinkedList;

public class LinkedListDemo {
    public static void main(String[] args) {
        LinkedList<Object> l = new LinkedList<>();

        l.add("D");           // [D]
        l.add(30);            // [D, 30]           — heterogeneous allowed
        l.add(null);          // [D, 30, null]     — null insertion allowed
        l.add("D");           // [D, 30, null, D]  — duplicates allowed

        // Content so far: D, 30, null, D
        // Insertion order preserved

        l.set(0, "Software"); // replace index 0: D → Software
        // [Software, 30, null, D]

        l.addFirst("CCC");    // add at beginning
        // [CCC, Software, 30, null, D]

        l.removeLast();       // remove last element (D)
        // [CCC, Software, 30, null]

        System.out.println(l);
        // prints [CCC, Software, 30, null]
    }
}
```

#### Step-by-step trace

Properties demonstrated in this demo:

- Insertion order preserved
- Duplicates allowed (D added twice)
- Null insertion possible
- Heterogeneous objects allowed (String + Integer)
- set(index, element) for replacement
- addFirst() adds at beginning (LinkedList-specific)
- removeLast() removes last element (LinkedList-specific)
Expected output:

[CCC, Software, 30, null]

## Quick revision — exam checklist

### Every collection class

- Implements `Serializable` ✓
- Implements `Cloneable` ✓
### RandomAccess (marker interface, `java.util`, no methods)

- Only ArrayList and Vector implement it
- LinkedList does NOT
### When to use which

### ArrayList vs Vector

### Get synchronized ArrayList

```java
List<String> sync = Collections.synchronizedList(new ArrayList<>());
```

Also available: Collections.synchronizedSet(), Collections.synchronizedMap().

### LinkedList

- Underlying structure: doubly linked list
- Constructors: 2 (no capacity constructor)
- Specific methods: addFirst, addLast, getFirst, getLast, removeFirst, removeLast
- Used for Stack and Queue implementations
## Session scope note

This lecture title says ArrayList Part-4, but the session also covers:

- Collection-wide rules (Serializable, Cloneable, RandomAccess)
- ArrayList performance characteristics and vs Vector
- Synchronized collection wrappers
- LinkedList introduction, properties, constructors, specific methods, and demo
Full dedicated LinkedList deep-dive continues in the next session (Video 140 — difference between ArrayList and LinkedList).

## Tables (placement lost -- re-place these in context)

| Field | Value |
|---|---|
| Playlist | Core Java With OCJP/SCJP |
| Position | 139 of 203 |
| Series | Core Java With OCJP/SCJP |
| Topic | Collections Part-4 — ArrayList (continued), ArrayList vs Vector, synchronized collections, LinkedList intro |
| Instructor | Durga Sir |
| Duration | 1h 06m 59s (4019 s) |
| Video ID | LFri78r3zUQ |
| Watch URL | https://www.youtube.com/watch?v=LFri78r3zUQ |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | YouTube auto-captions |

| Scenario | Container needed? |
|---|---|
| Transport goods from Hyderabad to Bangalore | Yes — physical container |
| Transfer 10,000 litres of petrol/diesel | Yes — tank/container |
| Hold several Student objects in memory | Yes — collection object |
| Send a collection object from Hyderabad to London over a network | Yes — the collection itself is the container being transferred |

| Class | Implements Serializable? |
|---|---|
| ArrayList | Yes |
| LinkedList | Yes |
| HashSet | Yes |
| TreeSet | Yes |
| Any collection class | Yes (by default) |

| Interface | Purpose | All collection classes? |
|---|---|---|
| Serializable | Network transfer / persistence | Yes |
| Cloneable | Exact duplicate copy | Yes |

| Operation | ArrayList time (conceptual) |
|---|---|
| Get 1st element | ~1 second (instant) |
| Get 10th element | ~1 second (same speed) |
| Get 1,00,000th element | ~1 second (same speed) |

| Class | Serializable | Cloneable | RandomAccess |
|---|---|---|---|
| ArrayList | Yes | Yes | Yes |
| Vector | Yes | Yes | Yes |
| LinkedList | Yes | Yes | No |

| Property | Value |
|---|---|
| Package | java.util |
| Methods | None (zero methods) |
| Type | Marker interface |
| Who provides ability? | JVM / internal implementation of ArrayList and Vector |

| Expression | Result | Reason |
|---|---|---|
| l1 instanceof Serializable | true | ArrayList implements Serializable |
| l2 instanceof Cloneable | true | LinkedList implements Cloneable |
| l1 instanceof RandomAccess | true | ArrayList implements RandomAccess |
| l2 instanceof RandomAccess | false | LinkedList does not implement RandomAccess |

| Frequent operation | ArrayList |
|---|---|
| Retrieval | Best choice (implements RandomAccess) |
| Insertion in the middle | Worst choice (massive shift operations) |
| Deletion in the middle | Worst choice (massive shift operations) |
| Insertion at last | No problem |
| Deletion at last | No problem |

| # | ArrayList | Vector |
|---|---|---|
| 1 | Every method is non-synchronized | Most methods are synchronized |
| 2 | Multiple threads allowed to operate simultaneously on same object → not thread-safe | Only one thread at a time → thread-safe |
| 3 | Threads don't wait → relatively high performance | Threads must wait → relatively low performance |
| 4 | Introduced in Java 1.2 | Introduced in Java 1.0 |
| 5 | Non-legacy class | Legacy class |

| Class | JDK Version | Legacy? |
|---|---|---|
| ArrayList | 1.2 | No (Collections Framework) |
| Vector | 1.0 | Yes (pre-Collections Framework) |

| Method | Signature | Purpose |
|---|---|---|
| synchronizedList | public static <T> List<T> synchronizedList(List<T> list) | Thread-safe List wrapper |
| synchronizedSet | public static <T> Set<T> synchronizedSet(Set<T> s) | Thread-safe Set wrapper |
| synchronizedMap | public static <K,V> Map<K,V> synchronizedMap(Map<K,V> m) | Thread-safe Map wrapper |

| Data structure | Strong at | Weak at |
|---|---|---|
| ArrayList | Retrieval (random access) | Middle insert/delete |
| LinkedList | Middle insert/delete | Retrieval |

| Frequent operation | Best | Worst |
|---|---|---|
| Retrieval | ArrayList | LinkedList |
| Insert/delete in middle | LinkedList | ArrayList |

| # | Property | Value |
|---|---|---|
| 1 | Underlying data structure | Doubly linked list |
| 2 | Insertion order preserved? | Yes (List property) |
| 3 | Duplicate objects allowed? | Yes |
| 4 | Heterogeneous objects allowed? | Yes (except TreeSet and TreeMap — covered earlier) |
| 5 | Null insertion possible? | Yes |
| 6 | Implements Serializable & Cloneable? | Yes |
| 7 | Implements RandomAccess? | No |
| 8 | Best choice when | Insertion/deletion in the middle |
| 9 | Worst choice when | Retrieval operation |

| Data structure | Principle | LinkedList role |
|---|---|---|
| Stack | LIFO — Last In First Out | addLast, removeLast, getLast |
| Queue | FIFO — First In First Out | addLast, removeFirst, getFirst |

| Method | Description |
|---|---|
| void addFirst(E e) | Add element at the beginning |
| void addLast(E e) | Add element at the end |
| E getFirst() | Retrieve (peek) first element |
| E getLast() | Retrieve (peek) last element |
| E removeFirst() | Remove and return first element |
| E removeLast() | Remove and return last element |

| Step | Code | List content after |
|---|---|---|
| 1 | new LinkedList<>() | [] |
| 2 | l.add("D") | [D] |
| 3 | l.add(30) | [D, 30] |
| 4 | l.add(null) | [D, 30, null] |
| 5 | l.add("D") | [D, 30, null, D] |
| 6 | l.set(0, "Software") | [Software, 30, null, D] |
| 7 | l.addFirst("CCC") | [CCC, Software, 30, null, D] |
| 8 | l.removeLast() | [CCC, Software, 30, null] |
| 9 | System.out.println(l) | `[CCC, Software, 30, null]` |

| Frequent operation | Best choice | Worst choice |
|---|---|---|
| Retrieval (get by index) | ArrayList | LinkedList |
| Insertion/deletion in middle | LinkedList | ArrayList |

|  | ArrayList | Vector |
|---|---|---|
| Synchronized? | No | Yes |
| Thread-safe? | No | Yes |
| Performance | Higher | Lower |
| JDK | 1.2 | 1.0 |
| Legacy? | No | Yes |
