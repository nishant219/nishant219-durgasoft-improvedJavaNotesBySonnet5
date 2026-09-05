# Video 140 — ArrayList vs LinkedList, Vector, Stack & Enumeration (Cursors Part 1)

## Video info

## Lecture roadmap (full session)

- ArrayList vs LinkedList — similarities, performance-based differences, internal memory structure
- Vector — properties, constructors, growth formula, legacy method names, capacity demo
- Stack — child of Vector, LIFO, stack-specific methods, index vs offset, demo
- Three Cursors of Java (intro) — purpose of cursors; Enumeration in depth with demo
- (Iterator and ListIterator deferred to next session)
## 00:04 — Session context & prior knowledge recap

Durga Sir opens by recalling that in earlier sessions the two main implementation classes of `List` were covered:

- `ArrayList` — first implementation class
- `LinkedList` — second implementation class
Before diving into ArrayList vs LinkedList, he briefly revisits related interview topics already covered:

Exam trap: If asked "What is the difference between ArrayList and LinkedList?", do not answer with similarities like "both allow duplicates" or "both preserve insertion order" — those are similarities, not differences.

## 01:03 — ArrayList vs LinkedList: similarities first

Both belong to the same category — both are under `List`.

### Shared properties (similarities)

Because so many properties match, the real differentiator is usage / performance behavior, not basic List contract rules.

## 02:25 — Performance-based differences (the board table)

### Point 1 — Best choice

### Point 2 — Worst choice

### Decision rule (interview answer)

Based on your requirement, choose ArrayList or LinkedList according to your most frequently performed operation:

- Retrieval-heavy → ArrayList (highly recommended)

- Update-heavy (insert/delete in the middle) → LinkedList (highly recommended)

## 07:22 — Internal memory structure (root cause of performance difference)

### Third comparison point — memory layout

Why the differences exist: entirely because of internal data structure.

- ArrayList → array-based → consecutive memory → fast random access, costly middle insert/delete
- LinkedList → double linked list → non-consecutive nodes → fast middle insert/delete, slow random access
## ArrayList vs LinkedList — master comparison table

## 10:24 — Transition: next List implementation — Vector

After ArrayList vs LinkedList, the next `List` implementation class is `Vector`.

## 10:42 — Vector: properties (point-by-point board notes)

### 1. Underlying data structure

- Resizable array or growable array (same family as ArrayList)
### 2. Insertion order

- Preserved
### 3. Duplicate objects

- Allowed (because it is under List)
### 4. Heterogeneous objects

- Allowed
### 5. Null insertion

- Possible — can happily insert null; no problem
### 6. Implemented interfaces

Vector implements:

- `Serializable`
- `Cloneable`
- `RandomAccess`
### 7. Synchronization / thread safety (THE key difference from ArrayList)

- Every method present in Vector is `synchronized`
- Therefore the Vector object is thread-safe
Summary: Except the synchronization point, almost all remaining properties are exactly the same as ArrayList.

## 14:59 — Vector constructors (4 constructors)

ArrayList has 3 constructors; LinkedList has 2 constructors (no capacity concept). Vector has 4 constructors because capacity terminology applies (array-based, consecutive memory).

### Constructor 1 — no-arg (default capacity 10)

```java
import java.util.Vector;

class VectorConstructorDemo1 {
    public static void main(String[] args) {
        Vector v = new Vector();
        // Creates empty Vector with default initial capacity = 10
        System.out.println("Default initial capacity: " + v.capacity()); // 10
    }
}
```

Behavior when full: After inserting 10 elements, inserting the 11th element triggers:

- Vector reaches max capacity
- A new (bigger) Vector internal array is created
- All existing elements are copied
- 11th element is inserted
Growth formula (Vector):

newCapacity = currentCapacity * 2

Examples: 10 → 20 → 40 → 80 → …

Important: ArrayList uses newCapacity = currentCapacity * 3/2 + 1. Do not assume the same formula everywhere — data structure implementation may differ. Vector simply doubles capacity.

### Constructor 2 — specified initial capacity

```java
import java.util.Vector;

class VectorConstructorDemo2 {
    public static void main(String[] args) {
        // If you know you need ~1000 objects upfront, avoid repeated resize:
        // 10 → 20 → 40 → 80 → 160 → ... is wasteful
        Vector v = new Vector(1000);
        // Creates empty Vector with specified initial capacity = 1000
        System.out.println("Initial capacity: " + v.capacity()); // 1000
    }
}
```

Use case: When you know approximate final size at the beginning, create one large Vector upfront instead of many incremental resizes.

### Constructor 3 — initial capacity + incremental capacity (Vector-only flexibility)

```java
import java.util.Vector;

class VectorConstructorDemo3 {
    public static void main(String[] args) {
        // initialCapacity=1000, incrementalCapacity=5
        // When full, grow by 5 each time instead of doubling to 2000
        Vector v = new Vector(1000, 5);
        System.out.println("Start: " + v.capacity()); // 1000

        for (int i = 1; i <= 1000; i++) {
            v.addElement(i);
        }
        System.out.println("After 1000 elements: " + v.capacity()); // still 1000

        v.addElement(1001); // 11th beyond 1000 → capacity becomes 1005
        System.out.println("After 1001st element: " + v.capacity()); // 1005

        for (int i = 1002; i <= 1005; i++) {
            v.addElement(i);
        }
        System.out.println("After 1005 elements: " + v.capacity()); // 1005

        v.addElement(1006);
        System.out.println("After 1006th element: " + v.capacity()); // 1010
    }
}
```

Why this exists: If you create Vector(1000) and add 1001 elements, default doubling gives capacity 2000 — but you may only need 3–4 more slots. Incremental capacity lets you specify how much to grow (e.g. +5 each time).

ArrayList has NO such constructor. ArrayList always follows newCapacity = currentCapacity * 3/2 + 1 with no way to specify incremental growth.

### Constructor 4 — from Collection (inter-conversion)

```java
import java.util.ArrayList;
import java.util.Collection;
import java.util.Vector;

class VectorConstructorDemo4 {
    public static void main(String[] args) {
        Collection c = new ArrayList();
        c.add("A");
        c.add("B");

        Vector v = new Vector(c);
        // Creates equivalent Vector for the given Collection
        System.out.println(v); // [A, B]
    }
}
```

Purpose: Inter-conversion between collection objects — create a Vector equivalent of any given Collection.

## Vector constructors summary table

## 26:12 — Vector-specific (legacy) methods

Vector came in Java 1.0 (1995) — legacy / old generation. Collection framework (List, ArrayList, etc.) came in Java 1.2 (~2000).

Analogy Durga Sir uses: Old generation people had lengthy names; newer generation prefers short names (add vs addElement).

### Method name mapping: Collection/List vs Vector

Notation used on board:

- C = Collection method
- L = List method
- V = Vector-specific (legacy) method
#### Category 1 — To add objects

#### Category 2 — To remove objects

#### Category 3 — To get objects

#### Category 4 — Other miscellaneous Vector methods

Size vs Capacity:

- `size()` → how many elements are actually present
- `capacity()` → maximum objects the internal array can hold before next resize
## 38:23 — Why `capacity()` exists in Vector but not ArrayList

Question: Capacity method is in Vector — why not in ArrayList?

Answer:

- Java is a high-level language; as Java programmers we generally do not worry about memory-level details — resizing happens automatically.
- If you want memory-level control, use C, not Java.
- Vector is old generation (1.0) — some low-level facilities like capacity() were kept.
- Modern Collection framework (1.2+) deliberately did not expose capacity to Java programmers — not required for typical application code.
## 40:06 — Vector capacity demo programs (board + IDE output)

### Demo A — Default capacity: 10 → stays 10 → becomes 20 after 11th add

```java
import java.util.Vector;

class VectorDemo1 {
    public static void main(String[] args) {
        Vector v = new Vector();

        System.out.println("Initial capacity: " + v.capacity()); // 10

        for (int i = 1; i <= 10; i++) {
            v.addElement(i); // legacy method; autoboxing: int → Integer
        }
        System.out.println("After 10 elements, capacity: " + v.capacity()); // 10

        v.addElement(11); // triggers resize: newCapacity = 10 * 2 = 20
        System.out.println("After 11th element, capacity: " + v.capacity()); // 20

        System.out.println("Elements: " + v);
        // [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    }
}
```

Expected output:

Initial capacity: 10
After 10 elements, capacity: 10
After 11th element, capacity: 20
Elements: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

Autoboxing note: addElement(i) where i is int — primitive is auto-boxed to Integer object internally.

### Demo B — Custom initial capacity 24 (no resize until full)

```java
import java.util.Vector;

class VectorDemo2 {
    public static void main(String[] args) {
        Vector v = new Vector(24);
        System.out.println("Initial capacity: " + v.capacity()); // 24

        for (int i = 1; i <= 10; i++) {
            v.addElement(i);
        }
        System.out.println("After 10 elements: " + v.capacity()); // 24

        v.addElement(11);
        System.out.println("After 11 elements: " + v.capacity()); // 24 (still space)

        for (int i = 12; i <= 24; i++) {
            v.addElement(i);
        }
        System.out.println("After 24 elements: " + v.capacity()); // 24

        v.addElement(25);
        System.out.println("After 25th element: " + v.capacity()); // 48 (doubled)
    }
}
```

### Demo C — Initial capacity 10, incremental capacity 5

```java
import java.util.Vector;

class VectorDemo3 {
    public static void main(String[] args) {
        Vector v = new Vector(10, 5);
        System.out.println("Initial: " + v.capacity()); // 10

        for (int i = 1; i <= 10; i++) {
            v.addElement(i);
        }
        System.out.println("After 10 elements: " + v.capacity()); // 10

        v.addElement(11);
        System.out.println("After 11th element: " + v.capacity()); // 15 (not 20!)

        for (int i = 12; i <= 15; i++) {
            v.addElement(i);
        }
        System.out.println("After 15 elements: " + v.capacity()); // 15

        v.addElement(16);
        System.out.println("After 16th element: " + v.capacity()); // 20
    }
}
```

## Growth formula comparison: ArrayList vs Vector

## 46:36 — Stack: child class of Vector

Next implementation: `Stack`.

### Stack properties

```java
import java.util.Stack;

class StackConstructorDemo {
    public static void main(String[] args) {
        Stack s = new Stack(); // only constructor
    }
}
```

Default capacity: Mostly 10 (inherited from Vector) — verify with s.capacity().

## 48:21 — Stack-specific methods (5 methods)

Whenever we say "stack", two methods immediately come to mind: push and pop. Stack has 5 dedicated methods:

## 50:50 — Index vs Offset (critical Stack concept)

Assume stack with elements pushed in order: A, B, C (bottom → top).

TOP
         C   ← last pushed
         B
         A   ← first pushed
        BOTTOM

### Index (Vector/List style — bottom-up, zero-based)

### Offset (Stack search style — top-down, 1-based distance from top)

`search(Object o)` returns offset, NOT index.

- s.search("A") → 3 (A is 3rd element from top)
- s.search("Z") → -1 (not found)
## 55:14 — Stack demo program (board + compile/run output)

```java
import java.util.Stack;

class StackDemo {
    public static void main(String[] args) {
        Stack s = new Stack();

        s.push("A");
        s.push("B");
        s.push("C");

        // Printing Stack directly → insertion order preserved in toString
        System.out.println(s);           // [A, B, C]

        // search() returns OFFSET from top, not index
        System.out.println(s.search("A")); // 3
        System.out.println(s.search("Z")); // -1

        // If we POP elements → LIFO removal order: C, B, A
        System.out.println("Pop: " + s.pop()); // C
        System.out.println("Pop: " + s.pop()); // B
        System.out.println("Pop: " + s.pop()); // A
    }
}
```

Key clarification from class:

- `System.out.println(s)` prints insertion order [A, B, C] because Stack extends Vector/List — insertion order is preserved in display.
- Removal order (via pop()) follows LIFO: C → B → A.
- `search("A")` → 3 (offset from top)
- `search("Z")` → -1 (not present)
Compile & run (as shown in video):

javac StackDemo.java
java StackDemo

Output:

[A, B, C]
3
-1
Pop: C
Pop: B
Pop: A

## Stack index vs offset diagram (board)

Stack (bottom → top):  A, B, C

Index (0-based from bottom):     A=0,  B=1,  C=2
Offset (1-based from top):       C=1,  B=2,  A=3

## 61:08 — End of Vector & Stack; intro to Three Cursors

Topics covered: Vector and Stack terminology complete.

Next subtopic: The Three Cursors of Java

## 61:58 — What is a Cursor? (mango box analogy)

Analogy: Someone gives you a box of mangoes. You don't eat all mangoes simultaneously by opening the box and putting your head in. Humans eat one by one — first mango, then second, then third…

- Box = Collection
- Mangoes inside = Objects
- To get objects one by one from the collection → use Cursor concept
### Cursor definition (board)

If you want to get objects one by one from the collection, then we should go for Cursor concept.

### Three types of cursors in Java

(This video covers Enumeration in detail; Iterator & ListIterator come next.)

## 66:12 — Enumeration: need demonstrated with example

### Problem without cursor

```java
import java.util.Vector;

class WithoutCursorDemo {
    public static void main(String[] args) {
        Vector v = new Vector();
        for (int i = 0; i <= 10; i++) {
            v.addElement(i);
        }
        System.out.println(v);
        // Prints ALL: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
}
```

Requirement: Print only even numbers — must examine each object one-by-one, check if even, print if yes, skip if odd. Cannot achieve selective processing by just printing the whole Vector.

## 68:20 — Enumeration: creating and using

### Get Enumeration from Vector

Enumeration e = v.elements(); // Vector-specific method

### Traversal loop

```java
while (e.hasMoreElements()) {
    Integer i = (Integer) e.nextElement(); // return type is Object → cast needed
    if (i % 2 == 0) {
        System.out.println(i);
    }
}
```

Logic walkthrough:

## 71:34 — Enumeration properties (board)

### Where to use Enumeration

We can use Enumeration to get objects one by one from legacy collection objects.

Legacy collections = old generation classes like Vector, Hashtable, etc. (Java 1.0 era).

### How to create Enumeration object

We can create Enumeration object by using `elements()` method of Vector class.

```java
public Enumeration elements();  // defined in Vector class
```

Example:

Enumeration e = v.elements();

## 74:10 — Enumeration interface methods (only 2 methods)

Enumeration is a limited cursor — contains only two methods:

```java
public boolean hasMoreElements();
public Object nextElement();
```

Usage pattern:

- Check hasMoreElements() → more elements available?
- If yes → call nextElement() to retrieve next object
- Repeat until no more elements
## 75:21 — Complete Enumeration demo program

```java
import java.util.Enumeration;
import java.util.Vector;

class VectorEnumerationDemo {
    public static void main(String[] args) {
        Vector v = new Vector();

        // Add 0 through 10 → 11 objects
        for (int i = 0; i <= 10; i++) {
            v.addElement(i);
        }

        // Print entire vector (all elements)
        System.out.println("Full Vector: " + v);
        // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        // Create Enumeration cursor
        Enumeration e = v.elements();

        System.out.print("Even numbers only: ");
        while (e.hasMoreElements()) {
            Integer num = (Integer) e.nextElement(); // Object → Integer cast
            if (num % 2 == 0) {
                System.out.print(num + " ");
            }
        }
        System.out.println();
        // Even numbers only: 0 2 4 6 8 10
    }
}
```

Compile & run:

javac VectorEnumerationDemo.java
java VectorEnumerationDemo

Expected output:

Full Vector: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Even numbers only: 0 2 4 6 8 10

Important distinction:

- System.out.println(v) → all values at once
- Enumeration loop → one-by-one processing with custom logic (filter evens)
## OCJP / SCJP exam checklist — Video 140

### Must know differences

- [ ] ArrayList vs LinkedList — performance (not duplicates/order)
- [ ] ArrayList implements RandomAccess; underlying resizable array
- [ ] LinkedList — doubly linked list; best for middle insert/delete
- [ ] Vector vs ArrayList — synchronized / thread-safe is the key difference
- [ ] Vector growth: double capacity; ArrayList: 3/2 + 1
- [ ] Vector has incremental capacity constructor; ArrayList does not
- [ ] Vector legacy methods: addElement, removeElement, elementAt, etc.
- [ ] Stack extends Vector; LIFO; methods: push, pop, peek, empty, search
- [ ] Stack search() returns offset from top (1-based), not index; -1 if absent
- [ ] Three cursors: Enumeration, Iterator, ListIterator
- [ ] Enumeration: legacy only; 2 methods; created via Vector.elements()
### Constructor counts (List implementations)

## Quick reference — method equivalence table

## Session ends at 1:17:22

Enumeration example completed and verified in IDE. Iterator and ListIterator differences will be covered in the next session (Video 141+).

End of Video 140 study notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Playlist | Core Java With OCJP/SCJP |  |  |
| Position | 140 of 203 |  |  |
| Title | Collections Part-5 \ | \ | Difference between Array list & linked list |
| Instructor | Durga Sir |  |  |
| Duration | 1h 18m 37s |  |  |
| Video ID | VmZrSCMkYoY |  |  |
| Watch | https://www.youtube.com/watch?v=VmZrSCMkYoY |  |  |
| Notes source | YouTube auto-captions |  |  |

| Comparison | Key difference |
|---|---|
| List vs Set | List allows duplicates & preserves insertion order; Set does not allow duplicates & does not preserve insertion order |
| ArrayList vs Vector | Vector is synchronized (thread-safe); ArrayList is not synchronized (not thread-safe). Vector has relatively lower performance; ArrayList has higher performance |
| Collection vs Collections | Already covered in prior sessions |

| Property | ArrayList | LinkedList |
|---|---|---|
| Duplicates allowed | Yes | Yes |
| Insertion order preserved | Yes | Yes |
| Heterogeneous objects allowed | Yes | Yes |
| Null insertion possible | Yes | Yes |
| Parent interface | List | List |

| Class | Best choice when… | Reason |
|---|---|---|
| ArrayList | Frequent operation is retrieval (random access / get) | Implements `RandomAccess` marker interface → direct index-based access is fast |
| LinkedList | Frequent operation is insertion or deletion in the middle | No shifting of all trailing elements; only pointer rewiring in the doubly-linked structure |

| Class | Worst choice when… | Reason |
|---|---|---|
| ArrayList | Frequent insertion/deletion in the middle | Internally several shift operations are performed — elements after the insertion/deletion point must move |
| LinkedList | Frequent retrieval operation | Must traverse from head (or known node); no random access to arbitrary index in O(1) |

|  | ArrayList | LinkedList |
|---|---|---|
| Internal implementation | Resizable / growable array | Doubly linked list |
| Memory layout | Elements stored in consecutive memory locations | Elements NOT stored in consecutive memory locations |
| Retrieval | Easy — e.g. 10th element: go directly to index 9 | Difficult — must traverse node by node |
| Insert/delete in middle | Costly — shift operations | Cheaper — pointer updates only |

| # | Aspect | ArrayList | LinkedList |
|---|---|---|---|
| 1 | Best choice | Retrieval operation | Insertion/deletion in the middle |
| 2 | Worst choice | Insertion/deletion in the middle (shift ops) | Retrieval operation |
| 3 | Underlying DS | Resizable / growable array | Doubly linked list |
| 4 | Memory | Consecutive memory locations | Non-consecutive (linked nodes) |
| 5 | Retrieval speed | Easy / fast | Difficult / slow |
| 6 | Middle insert/delete | Slow (shifts) | Relatively fast |
| 7 | RandomAccess interface | Yes | No |
| 8 | Duplicates | Allowed | Allowed |
| 9 | Insertion order | Preserved | Preserved |
| 10 | Null elements | Allowed | Allowed |
| 11 | Heterogeneous objects | Allowed | Allowed |

| # | Syntax | Creates |
|---|---|---|
| 1 | new Vector() | Empty Vector, default initial capacity 10 |
| 2 | new Vector(int initialCapacity) | Empty Vector with specified initial capacity |
| 3 | new Vector(int initialCapacity, int incrementalCapacity) | Empty Vector; grows by incrementalCapacity instead of doubling |
| 4 | new Vector(Collection c) | Equivalent Vector copy of given Collection |

| Collection / List | Vector equivalent |
|---|---|
| add(Object o) (C/L) | addElement(Object o) (V) |
| add(int index, Object o) (L) | insertElementAt(Object o, int index) (V) |
| addAll(Collection c) (C) | addAll(Collection c) |
| addAll(int index, Collection c) (L) | addAll(int index, Collection c) |

| Collection / List | Vector equivalent |
|---|---|
| remove(Object o) (C) | removeElement(Object o) (V) |
| remove(int index) (L) | removeElementAt(int index) (V) |
| clear() (C/L) | removeAllElements() (V) |

| List | Vector equivalent |
|---|---|
| get(int index) (L) | elementAt(int index) (V) |
| — | firstElement() (V) |
| — | lastElement() (V) |

| Method | Purpose |
|---|---|
| size() | Number of elements currently stored |
| capacity() | Total slots the internal array can hold (may be > size) |
| elements() | Returns `Enumeration` object to traverse elements one-by-one |

| Class | When full | New capacity formula |
|---|---|---|
| ArrayList | Resizes automatically | currentCapacity * 3/2 + 1 |
| Vector (default) | Resizes automatically | currentCapacity * 2 |
| Vector (custom incremental) | Resizes by increment | currentCapacity + incrementalCapacity |

| Property | Detail |
|---|---|
| Inheritance | Child class of `Vector` |
| All Vector properties | Inherited (resizable array, synchronized methods, etc.) |
| Special purpose | Specially designed class for LIFO — Last In First Out order |
| Constructors | Only one — default no-arg constructor |

| Method | Signature | Purpose |
|---|---|---|
| push | Object push(Object o) | Insert (push) object onto top of stack |
| pop | Object pop() | Remove and return top of stack |
| peek | Object peek() | Return top of stack without removal |
| empty | boolean empty() | Returns true if stack is empty |
| search | int search(Object o) | Returns offset from top if element found; otherwise -1 |

| Element | Index |
|---|---|
| A | 0 |
| B | 1 |
| C | 2 |

| Element | Offset |
|---|---|
| C (top) | 1 |
| B | 2 |
| A | 3 |

| # | Cursor |
|---|---|
| 1 | Enumeration |
| 2 | Iterator |
| 3 | ListIterator |

| Step | nextElement | Even? | Action |
|---|---|---|---|
| 1 | 0 | Yes | Print 0 |
| 2 | 1 | No | Skip |
| 3 | 2 | Yes | Print 2 |
| … | … | … | … |
| Final output |  |  | 0 2 4 6 8 10 |

| Method | Return type | Purpose |
|---|---|---|
| hasMoreElements() | boolean | Returns whether more elements exist |
| nextElement() | Object | Returns the next element |

| Class | # Constructors | Capacity support |
|---|---|---|
| ArrayList | 3 | Yes (no incremental) |
| LinkedList | 2 | No |
| Vector | 4 | Yes (+ incremental) |
| Stack | 1 | Inherited from Vector |

| Operation | ArrayList / List | Vector (legacy) |
|---|---|---|
| Add | add(o) | addElement(o) |
| Add at index | add(index, o) | insertElementAt(o, index) |
| Remove by object | remove(o) | removeElement(o) |
| Remove by index | remove(index) | removeElementAt(index) |
| Clear all | clear() | removeAllElements() |
| Get by index | get(index) | elementAt(index) |
| First element | — | firstElement() |
| Last element | — | lastElement() |
| Size | size() | size() |
| Capacity | N/A | capacity() |
| Cursor | Iterator | elements() → Enumeration |
