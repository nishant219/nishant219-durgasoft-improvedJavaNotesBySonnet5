# Video 138 — Collections Part-3: Collection Interface Methods, List & ArrayList

## Video info

## Session overview

Continuation of the Collections series (Part-1 = Video 136, Part-2 = Video 137). This session is the first deep dive into the `Collection` interface methods and then moves into `List` interface (index-based methods) and begins `ArrayList` (properties, constructors, growth formula, demo).

What this lecture covers:

- Recap of top interview FAQs from previous sessions
- When to use Collection and all generalized methods in Collection interface
- Important note: no concrete class implements `Collection` directly
- List interface — when to use, role of index, List-specific methods
- List implementation classes overview (ArrayList, LinkedList, Vector, Stack)
- ArrayList — underlying data structure, properties, three constructors, capacity growth formula
- Live demo program + generics warning (Java 1.5+)
What continues in next session (Video 139):

- General ArrayList conclusions (Serializable, Cloneable, RandomAccess)
- ArrayList performance characteristics
- LinkedList introduction
Scope note: The video title mentions "list & set". Set interface rules were covered in Video 137 (Part-2). This session focuses heavily on Collection methods + List + ArrayList; Set is referenced only in recap/interview context.

## 00:05 — Recap: must-know interview questions

Before starting new content, Durga Sir revisits questions you must answer confidently for internal exams and interviews:

These three differences are the minimum answerable level from prior lectures. Today's session adds the method-level detail behind the Collection and List interfaces.

## 01:06 — Interface 1 revisited: `Collection` (I)

### When should we go for Collection?

Rule (board conclusion): If you want to represent a group of individual objects as a single entity, then we should go for Collection.

- Individual objects have no dependency on each other (unlike Map's key–value dependency).
- Example mental model: five separate objects (obj1, obj2, obj3, obj4, obj5) grouped together as one collection object.
### What does Collection interface define?

Rule: Collection interface defines the most common methods which are applicable for any collection object.

Whether the concrete object is:

- ArrayList
- LinkedList
- Stack
- TreeSet
- HashSet
…the common operations (add, remove, size, etc.) are declared once in Collection interface. Every child interface/class inherits or implements these generalized methods.

### There is NO concrete class for Collection

Important exam note: There is no concrete class which implements Collection interface directly.

Concrete classes always implement child interfaces (List, Set, Queue), never Collection itself.

```java
import java.util.*;

// CE: Collection is abstract; cannot be instantiated
// Collection c = new Collection();

// Valid — concrete classes implement child interfaces
Collection<String> c1 = new ArrayList<>();   // via List
Collection<String> c2 = new HashSet<>();     // via Set
Collection<String> c3 = new LinkedList<>();  // via List
```

Board note to copy:

- There is no concrete class which implements Collection interface directly.
- That is why we do not discuss any "Collection class" — only the Collection interface.
## 01:44 — All methods in `Collection` interface (generalized methods)

Durga Sir stresses: You must have crystal-clear clarity on every method below. These are the generalized methods present inside Collection interface, applicable to any collection object (ArrayList, HashSet, Vector, etc.).

### Category 1: Adding elements

Classroom analogy for `addAll`:

- "I don't want to add one student — I want to add these 10 students (a whole batch) to my main collection."
- A group of objects is itself a Collection → pass it to addAll.
```java
import java.util.*;

public class CollectionAddDemo {
    public static void main(String[] args) {
        Collection<String> main = new ArrayList<>();
        main.add("Durga");           // add single object

        Collection<String> batch = new ArrayList<>();
        batch.add("Ravi");
        batch.add("Shiva");
        batch.add("Radha");

        main.addAll(batch);          // add entire group
        System.out.println(main);
        // prints [Durga, Ravi, Shiva, Radha]
    }
}
```

### Category 2: Removing elements (four remove-related methods)

Durga Sir's classroom analogies (memorize these):

```java
import java.util.*;

public class CollectionRemoveDemo {
    public static void main(String[] args) {
        Collection<String> classRoom = new ArrayList<>(
            Arrays.asList("Morning-A", "Morning-B", "Evening-A", "Evening-B", "New-1", "New-2")
        );

        Collection<String> eveningBatch = Arrays.asList("Evening-A", "Evening-B");
        classRoom.removeAll(eveningBatch);
        System.out.println("After removeAll evening: " + classRoom);
        // prints After removeAll evening: [Morning-A, Morning-B, New-1, New-2]

        Collection<String> newMembers = Arrays.asList("New-1", "New-2");
        classRoom.retainAll(newMembers);
        System.out.println("After retainAll newMembers: " + classRoom);
        // prints After retainAll newMembers: [New-1, New-2]

        classRoom.clear();
        System.out.println("After clear, size: " + classRoom.size());
        // prints After clear, size: 0
    }
}
```

Exam point: There are four removal-related methods: remove, removeAll, clear, retainAll. Normal remove removes one object; retainAll is also for removal but keeps only the specified group.

### Category 3: Checking / querying

```java
import java.util.*;

public class CollectionQueryDemo {
    public static void main(String[] args) {
        Collection<String> c = new ArrayList<>(Arrays.asList("A", "B", "C"));

        System.out.println(c.contains("B"));      // true
        System.out.println(c.contains("Z"));      // false
        System.out.println(c.isEmpty());            // false
        System.out.println(c.size());               // 3

        Collection<String> sub = Arrays.asList("A", "B");
        System.out.println(c.containsAll(sub));   // true
    }
}
```

### Category 4: Conversion and traversal

Why `toArray()`?

- After all insertions/deletions are done, converting to array makes operations more efficient.
- Array operations are faster than collection operations in some scenarios.
Why `iterator()`?

- Collection = group of objects. To access objects one by one, a cursor is required.
- `Iterator` is the universal cursor applicable for any collection object.
```java
import java.util.*;

public class CollectionIteratorDemo {
    public static void main(String[] args) {
        Collection<String> c = new ArrayList<>(Arrays.asList("Durga", "Java", "OCJP"));

        // Universal cursor — works on ANY collection
        Iterator<String> it = c.iterator();
        while (it.hasNext()) {
            System.out.println(it.next());
        }
        // prints Durga
        // prints Java
        // prints OCJP

        Object[] arr = c.toArray();
        System.out.println(arr.length); // 3
    }
}
```

### Complete Collection interface method summary (12 core methods)

Can we call these on LinkedList? On TreeSet? → Yes. Because Collection is the root (parent) of List/Set/Queue hierarchies. Any concrete collection object can use all 12 methods happily.

## 17:01 — Interface 2: `List` (I) — deep dive

### Hierarchy reminder

Collection (parent)
    └── List (child)
         ├── ArrayList
         ├── LinkedList
         ├── Vector   (legacy, 1.0)
         └── Stack    (legacy, extends Vector)

Rule: Collection is parent, List is child. All 12 Collection methods are automatically available on List. But List adds extra index-based methods on top.

### When should we go for List?

Rule (board conclusion): If we want to represent a group of individual objects as a single entity where:

1. Duplicates are allowed, AND

2. Insertion order must be preserved

→ then we should go for List.

### How insertion order is preserved in List — INDEX is the key

Consider a List with index positions 0, 1, 2, 3, 4, 5…

Point 1 — Insertion order preserved via index:

- First inserted element → 0th index
- Second inserted element → 1st index
- Third inserted element → 2nd index
- Insertion order is preserved with respect to index.
Point 2 — Duplicates allowed; differentiated by index:

- Two "A" objects can coexist at index 0 and index 15.
- We can differentiate duplicate objects by using index.
- Therefore: Index plays a very important role in List.
Board conclusion (copy exactly):

- We can preserve insertion order via index.

- We can differentiate duplicate objects by using index.

- Index will play a very important role in List.

### List-specific methods (all index-related)

Every List-specific method talks about index. Collection's add(Object) always appends at end; List adds index-aware variants.

No ready-made method for 2nd or 3rd occurrence — only first and last. For other occurrences, write explicit loop logic.

#### `add(int index, E e)` — shift behavior

```java
import java.util.*;

public class ListAddAtIndexDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>(Arrays.asList("A", "B", "C", "D", "E"));
        // indexes:                        0    1    2    3    4

        list.add(3, "X");  // insert X at index 3
        // Before: A B C D E
        // D was at index 3 → shifts to index 4
        // Result: A B C X D E

        System.out.println(list);
        // prints [A, B, C, X, D, E]
    }
}
```

#### `remove(int index)` vs `remove(Object o)`

```java
import java.util.*;

public class ListRemoveIndexDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>(Arrays.asList("A", "B", "C", "D"));

        String removed = list.remove(2);  // remove by INDEX
        System.out.println("Removed: " + removed);  // Removed: C
        System.out.println(list);                    // [A, B, D]

        list.remove("A");  // remove by OBJECT (from Collection)
        System.out.println(list);                    // [B, D]
    }
}
```

#### `get`, `set`, `indexOf`, `lastIndexOf`

```java
import java.util.*;

public class ListIndexMethodsDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("A");  // index 0
        list.add("B");  // index 1
        list.add("A");  // index 2 — duplicate
        list.add("C");  // index 3

        System.out.println(list.get(2));        // A (element at index 2)
        list.set(2, "Z");                        // replace index 2
        System.out.println(list);                // [A, B, Z, C]

        System.out.println(list.indexOf("A"));     // 0 (first occurrence)
        System.out.println(list.lastIndexOf("A")); // 0 (only one A left after set)
    }
}
```

### List-specific cursor: `ListIterator`

```java
import java.util.*;

public class ListIteratorDemo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>(Arrays.asList("A", "B", "C"));

        ListIterator<String> lit = list.listIterator();
        while (lit.hasNext()) {
            System.out.println(lit.next());
        }
        // prints A, B, C
    }
}
```

### Board summary — List interface defines

List interface defines methods to:

- add(int index, E e) — add at specified index
- addAll(int index, Collection c) — add group from specified index
- remove(int index) — remove by index
- get(int index) — retrieve by index
- set(int index, E e) — replace at index
- indexOf(Object o) — first occurrence index
- lastIndexOf(Object o) — last occurrence index
- listIterator() — List-specific cursor
All 8 List-specific methods + 12 Collection methods = available on every List implementation class (ArrayList, LinkedList, Vector, Stack).

## 33:47 — List implementation classes (overview)

Hierarchy diagram (board):

Collection
    └── List
         ├── ArrayList
         ├── LinkedList
         ├── Vector
         └── Stack (extends Vector)

This session begins deep coverage of ArrayList. LinkedList, Vector, Stack details continue in upcoming lectures.

## 35:27 — `ArrayList` class — properties (point by point)

### Point 1: Underlying data structure

The underlying data structure for ArrayList is resizable array (growable array).

ArrayList is implemented using the resizable array concept in Java. Internally it maintains an Object array that grows when full.

### Point 2: Duplicates allowed

ArrayList is under List → List allows duplicates → duplicates are allowed in ArrayList.

### Point 3: Insertion order preserved

Objects appear in the same order they were added. Insertion order is preserved (via index, as explained above).

### Point 4: Heterogeneous objects — allowed (with framework-wide exception)

ArrayList allows heterogeneous objects (different types in same list).

Framework-wide rule (very important for exam):

- In the entire Collection Framework, only two areas do NOT allow heterogeneous objects:
- TreeSet
- TreeMap
- Why? TreeSet/TreeMap insert objects according to sorting order → comparison is required → objects must be same type (Comparable or Comparator).
- In all other collections (including ArrayList), if comparison is not required, objects can be different types — no problem.
```java
import java.util.*;

public class ArrayListHeterogeneousDemo {
    public static void main(String[] args) {
        ArrayList list = new ArrayList();  // raw type for demo
        list.add("Durga");    // String
        list.add(10);         // Integer (autoboxing)
        list.add(null);       // null also OK
        System.out.println(list);
        // prints [Durga, 10, null]
    }
}
```

### Point 5: Null insertion — possible

Null insertion is possible in ArrayList.

list.add(null) — no problem. Multiple nulls also allowed (duplicates allowed).

### ArrayList properties — board checklist

## 42:17 — ArrayList constructors (three constructors)

Almost every collection class follows this three-constructor pattern. Know all three for ArrayList.

### Constructor 1: `ArrayList()` — default empty list

```java
ArrayList list = new ArrayList();
```

- Creates an empty ArrayList object.
- Default initial capacity = 10.
- You can add up to 10 elements before internal resize happens.
### What happens when 11th element is added? (Growth mechanism)

When ArrayList reaches max capacity (e.g., 10 elements filled) and you try to insert the 11th object:

- A new, bigger ArrayList (internal array) object is created
- All existing elements are copied to the new array
- Reference variable is reassigned to the new object
- Old array object becomes eligible for garbage collection
This copy-on-grow pattern is why specifying initial capacity matters for performance.

### Growth formula (OCJP exam favourite)

newCapacity = (currentCapacity * 3 / 2) + 1

Worked example:

Note: Integer division applies — 25 * 3 / 2 = 75 / 2 = 37 (not 37.5).

NOT simply doubling (10 → 20). The formula is specifically `currentCapacity × 3/2 + 1`.

### Constructor 2: `ArrayList(int initialCapacity)` — specify capacity upfront

```java
ArrayList list = new ArrayList(1000);
```

- Creates empty ArrayList with specified initial capacity (e.g., 1000).
- Avoids repeated create-copy-grow cycles if you know approximate size upfront.
- Performance tip: If you know you'll store ~1000 elements, create with capacity 1000 at the beginning instead of default 10 → 16 → 25 → 38 → …
### Constructor 3: `ArrayList(Collection c)` — equivalent ArrayList from any collection

```java
ArrayList list = new ArrayList(linkedListObject);
ArrayList list = new ArrayList(vectorObject);
ArrayList list = new ArrayList(hashSetObject);
```

- Creates an equivalent ArrayList containing all elements from the given collection.
- Works with any collection object (LinkedList, Vector, Stack, HashSet, etc.).
- Used for inter-conversion between collection types.
```java
import java.util.*;

public class ArrayListConstructorsDemo {
    public static void main(String[] args) {
        // Constructor 1: default capacity 10
        ArrayList<String> a1 = new ArrayList<>();
        System.out.println("a1 size: " + a1.size()); // 0

        // Constructor 2: specified capacity
        ArrayList<String> a2 = new ArrayList<>(1000);

        // Constructor 3: from another collection
        LinkedList<String> ll = new LinkedList<>();
        ll.add("A");
        ll.add("B");
        ArrayList<String> a3 = new ArrayList<>(ll);
        System.out.println(a3); // [A, B]
    }
}
```

### Three constructors summary table

## 53:43 — ArrayList demo program (board example)

```java
import java.util.*;

public class ArrayListDemo {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();

        l.add(10);       // Integer (autoboxing)
        l.add("Durga");  // String — heterogeneous OK
        l.add(10);       // duplicate OK
        l.add(null);     // null OK

        System.out.println(l);
        // prints [10, Durga, 10, null]
        // Collection toString: square brackets [ ]

        l.remove(2);     // remove element at INDEX 2 (second 10)
        // After remove: [10, Durga, null]

        l.add(2, "Software");  // insert at index 2
        // D shifts: [10, Durga, Software, null]

        l.add("M");      // add at end (no index specified)
        // [10, Durga, Software, null, M]

        System.out.println(l);
    }
}
```

### Properties demonstrated in demo

### Collection vs Map — toString format difference

## 58:19 — Generics warning (Java 1.5+)

When compiling with raw types (no generics):

Note: ArrayListDemo.java uses unchecked or unsafe operations.
Recompile with -Xlint:unchecked for details.

Why the warning?

- From Java 1.5, Generics concept introduced.
- Highly recommended to use collections with generics for type safety.
- Raw type ArrayList l = new ArrayList() allows any object → compiler warns about unchecked operations.
Correct generic syntax:

```java
ArrayList<String> l = new ArrayList<String>();
// or (Java 7+ diamond)
ArrayList<String> l = new ArrayList<>();
```

- With generics → no warning.
- Without generics → warning at compile time (still compiles and runs).
Generics deep-dive is a separate topic. For now: use generic syntax to avoid warnings and ensure type safety.

## Quick revision — exam checklist

### Collection interface

- [ ] When to use: group of individual objects as single entity
- [ ] Defines 12 generalized methods (add, addAll, remove, removeAll, clear, retainAll, contains, containsAll, isEmpty, size, toArray, iterator)
- [ ] No concrete class implements Collection directly
- [ ] retainAll = keep specified group, remove everything else
- [ ] Iterator = universal cursor for any collection
### Collection vs Collections (interview)

- [ ] Collection = interface; Collections = utility class
- [ ] Collections.sort(list) for sorting a List
### List interface

- [ ] When to use: duplicates allowed + insertion order preserved
- [ ] Index preserves insertion order and differentiates duplicates
- [ ] 8 List-specific methods (all index-related)
- [ ] set(index, obj) — NOT replace
- [ ] indexOf = first occurrence; lastIndexOf = last occurrence
- [ ] ListIterator = List-specific cursor via listIterator()
### List vs Set (interview)

- [ ] List: duplicates YES, insertion order YES
- [ ] Set: duplicates NO, insertion order NOT required
### ArrayList

- [ ] Underlying DS: resizable/growable array
- [ ] Duplicates allowed, insertion order preserved
- [ ] Heterogeneous objects allowed
- [ ] Null insertion possible
- [ ] Default initial capacity: 10
- [ ] Growth formula: newCapacity = (currentCapacity × 3/2) + 1
- [ ] 3 constructors: (), (int capacity), (Collection c)
- [ ] Constructor 3 used for inter-conversion between collection types
- [ ] Only TreeSet and TreeMap disallow heterogeneous objects (framework-wide)
### Generics

- [ ] Raw types → unchecked warning
- [ ] Use ArrayList<Type> for type safety (Java 1.5+)
## Homework / self-test

- Write all 12 Collection interface methods from memory with one-line purpose each.
- Explain retainAll vs removeAll using Durga Sir's classroom analogy.
- Calculate new ArrayList capacity after filling: 10 → ? → ? → ? (first four growth steps).
- Write a program that creates ArrayList from a HashSet using constructor 3 and prints elements.
- Demonstrate add(index, element) shift behavior with at least 5 elements.
- Convert raw-type demo to generic ArrayList<String> and confirm warning disappears.
```java
import java.util.*;

public class SelfTest138 {
    public static void main(String[] args) {
        // Growth trace: 10 -> 16 -> 25 -> 38
        ArrayList<Integer> list = new ArrayList<>(10);
        for (int i = 1; i <= 26; i++) {
            list.add(i);
        }
        System.out.println("Size after 26 adds: " + list.size());
        // prints Size after 26 adds: 26

        // Inter-conversion: HashSet -> ArrayList
        HashSet<String> set = new HashSet<>(Arrays.asList("C", "A", "B"));
        ArrayList<String> fromSet = new ArrayList<>(set);
        System.out.println("From HashSet: " + fromSet);
        // order not guaranteed for HashSet source

        // List index methods
        List<String> names = new ArrayList<>(Arrays.asList("A", "B", "A", "C"));
        System.out.println("First A at: " + names.indexOf("A"));      // 0
        System.out.println("Last A at: " + names.lastIndexOf("A"));  // 2
        names.set(1, "Z");
        System.out.println("After set: " + names);                   // [A, Z, A, C]
    }
}
```

## Session scope & next lecture preview

Completed in Video 138:

- Full Collection interface method catalog with analogies
- List interface index-based methods
- ArrayList properties, 3 constructors, growth formula
- Demo program + generics warning
Continues in Video 139:

- General collection conclusions (Serializable, Cloneable, RandomAccess)
- ArrayList performance (best for retrieval, worst for middle insertion/deletion)
- ArrayList vs Vector comparison
- Synchronized collection wrappers
- LinkedList introduction
## Reference tables

### Collection interface — complete method reference

### List interface — additional methods beyond Collection

### ArrayList capacity growth worked examples

### Heterogeneous objects — framework rule

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 138 of 203 |  |  |
| Playlist | Core Java With OCJP/SCJP |  |  |
| Title | Collections Part-3 \ | collection & collections \ | list & set |
| Instructor | Durga Sir |  |  |
| Duration | 1h 00m 55s |  |  |
| Video ID | foi7_Zjbz5c |  |  |
| URL | https://www.youtube.com/watch?v=foi7_Zjbz5c |  |  |
| Notes source | Local Whisper STT |  |  |

| # | Question | One-line answer |
|---|---|---|
| 1 | What is the difference between Collection and Collections? | Collection = interface; Collections = utility class with static helper methods (sort, reverse, etc.) |
| 2 | What is the difference between List and Set? | List → duplicates allowed + insertion order preserved; Set → duplicates NOT allowed + insertion order NOT required |
| 3 | What is the difference between Collection and Map? | Collection = group of individual objects; Map = group of key–value pairs — completely separate hierarchies |

| Requirement (plain English) | Method | Signature |
|---|---|---|
| Add one object to the collection | add | boolean add(Object o) / boolean add(E e) |
| Add a group of objects (another collection) | addAll | boolean addAll(Collection c) |

| Requirement | Method | What happens |
|---|---|---|
| Remove one particular object | remove(Object o) | That object removed from collection |
| Remove a group of objects | removeAll(Collection c) | All objects present in c are removed from main collection |
| Remove ALL objects (empty the collection) | clear() | Every object removed; size becomes 0 |
| Retain only a specified group; remove everything else | retainAll(Collection c) | Keep objects in c; all remaining objects removed |

| Method | Classroom story |
|---|---|
| remove("Ravi") | "If any person named Ravi is in class, please go out." |
| removeAll(eveningBatch) | "All evening SCJP batch people, please go out." |
| clear() | "Class completed for today — everyone please go out." After clear(), classroom is empty (size = 0). |
| retainAll(newMembers) | "Only the new members who came for Collections topic — accept these, all remaining please go out." |

| Requirement | Method | Return |
|---|---|---|
| Check if one particular object is present | contains(Object o) | boolean |
| Check if all objects of another collection are present | containsAll(Collection c) | boolean |
| Check if collection is empty | isEmpty() | boolean |
| Get number of objects | size() | int |

| Requirement | Method | Return type |
|---|---|---|
| Convert collection to array (for faster operations) | toArray() | Object[] |
| Get objects one by one (universal cursor) | iterator() | Iterator |

| # | Method | Purpose |
|---|---|---|
| 1 | add(E e) | Add single element |
| 2 | addAll(Collection c) | Add all elements from another collection |
| 3 | remove(Object o) | Remove single element |
| 4 | removeAll(Collection c) | Remove all elements found in c |
| 5 | clear() | Remove all elements |
| 6 | retainAll(Collection c) | Keep only elements in c; remove rest |
| 7 | contains(Object o) | Check single element presence |
| 8 | containsAll(Collection c) | Check all elements of c are present |
| 9 | isEmpty() | Check if size == 0 |
| 10 | size() | Return number of elements |
| 11 | toArray() | Convert to Object array |
| 12 | iterator() | Return Iterator for one-by-one access |

| Insertion order | Element | Index |
|---|---|---|
| 1st inserted | A | 0 |
| 2nd inserted | B | 1 |
| 3rd inserted | C | 2 |
| … | … | … |
| 16th inserted | A (duplicate) | 15 |

| Requirement | Method | Notes |
|---|---|---|
| Add at default (end/next available cell) | add(E e) | Inherited from Collection; appends at end |
| Add at specified index | add(int index, E e) | Existing element at that index shifts right |
| Add group starting at index | addAll(int index, Collection c) | Insert all elements of c starting from index |
| Remove by index (not just by object) | remove(int index) | Returns removed element; shifts left |
| Get object at index | get(int index) | Returns element at specified index |
| Replace object at index | set(int index, E e) | Not replace — method name is `set` |
| Find first occurrence index of object | indexOf(Object o) | Returns first occurrence index |
| Find last occurrence index of object | lastIndexOf(Object o) | Returns last occurrence index |

| Cursor | Applicable for | Method to obtain |
|---|---|---|
| Iterator | Any Collection | iterator() |
| ListIterator | List only | listIterator() |

| # | Class | Underlying DS | Version | Notes |
|---|---|---|---|---|
| 1 | ArrayList | Resizable / growable array | 1.2 | Most commonly used List |
| 2 | LinkedList | Doubly linked list | 1.2 | Covered in detail later |
| 3 | Vector | Resizable array (like ArrayList) | 1.0 (legacy) | Re-engineered in 1.2 to implement List |
| 4 | Stack | Extends Vector | 1.0 (legacy) | LIFO stack; extends Vector |

| # | Property | ArrayList behavior |
|---|---|---|
| 1 | Underlying data structure | Resizable (growable) array |
| 2 | Duplicates | Allowed |
| 3 | Insertion order | Preserved |
| 4 | Heterogeneous objects | Allowed |
| 5 | Null insertion | Possible |

| Event | Current capacity | Calculation | New capacity |
|---|---|---|---|
| Initial create | — | default | 10 |
| 11th element added | 10 | (10 × 3/2) + 1 = 15 + 1 | 16 |
| 17th element added | 16 | (16 × 3/2) + 1 = 24 + 1 | 25 |
| 26th element added | 25 | (25 × 3/2) + 1 = 37 + 1 | 38 |

| # | Constructor | Creates |
|---|---|---|
| 1 | ArrayList() | Empty ArrayList, default initial capacity 10 |
| 2 | ArrayList(int initialCapacity) | Empty ArrayList with specified initial capacity |
| 3 | ArrayList(Collection c) | Equivalent ArrayList from any collection object |

| Property | Evidence in demo |
|---|---|
| Insertion order preserved | Elements appear in add order |
| Duplicates allowed | Two 10 values coexist |
| Null insertion possible | null added successfully |
| Heterogeneous objects | Integer + String in same list |
| Index-based remove | remove(2) removes by index |
| Index-based add | add(2, "Software") shifts existing elements |

| Type | toString output style | Example |
|---|---|---|
| Collection | Square brackets [ ] | [10, Durga, null] |
| Map | Curly braces { } with key=value | {1=Durga, 2=Ravi, 3=Shiva} |

| Method | Returns | Description |
|---|---|---|
| boolean add(E e) | boolean | Adds single element |
| boolean addAll(Collection<? extends E> c) | boolean | Adds all elements from c |
| boolean remove(Object o) | boolean | Removes single element |
| boolean removeAll(Collection<?> c) | boolean | Removes all elements in c from this collection |
| void clear() | void | Removes all elements |
| boolean retainAll(Collection<?> c) | boolean | Retains only elements in c |
| boolean contains(Object o) | boolean | Checks if element present |
| boolean containsAll(Collection<?> c) | boolean | Checks if all of c present |
| boolean isEmpty() | boolean | true if size == 0 |
| int size() | int | Number of elements |
| Object[] toArray() | Object[] | Converts to array |
| Iterator<E> iterator() | Iterator | Returns iterator cursor |

| Method | Returns | Description |
|---|---|---|
| void add(int index, E e) | void | Insert at index; shifts right |
| boolean addAll(int index, Collection<? extends E> c) | boolean | Insert all from c at index |
| E remove(int index) | E | Remove and return element at index |
| E get(int index) | E | Return element at index |
| E set(int index, E e) | E | Replace element at index |
| int indexOf(Object o) | int | First occurrence index (-1 if absent) |
| int lastIndexOf(Object o) | int | Last occurrence index (-1 if absent) |
| ListIterator<E> listIterator() | ListIterator | List-specific bidirectional cursor |

| Step | Current capacity | Elements stored | Action on next add |
|---|---|---|---|
| Create | 10 | 0 | — |
| Fill to 10 | 10 | 10 | At capacity |
| Add 11th | 10 → 16 | 11 | New array created, copy, reassign |
| Fill to 16 | 16 | 16 | At capacity |
| Add 17th | 16 → 25 | 17 | Grow again |
| Fill to 25 | 25 | 25 | At capacity |
| Add 26th | 25 → 38 | 26 | Grow again |

| Collection / Map | Heterogeneous objects allowed? | Reason |
|---|---|---|
| ArrayList | Yes | No comparison needed |
| LinkedList | Yes | No comparison needed |
| HashSet | Yes | No comparison needed |
| HashMap | Yes | No comparison needed |
| TreeSet | No | Sorting requires comparison → same type |
| TreeMap | No | Sorting by key requires comparison → same type |
