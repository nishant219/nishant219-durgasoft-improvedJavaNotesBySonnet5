# Video 150 — Collections Part-15: Queue & PriorityQueue

## Video info

## Session overview

This lecture completes the Collection half of the Collections Framework by covering the last remaining child interface of Collection: Queue. After ~30 hours of List, Set, and Map, Sir states this is the final major piece on the "individual objects" side before utility classes and Java 1.6 enhancements.

What this session covers:

- Queue interface — child of Collection; FIFO principle; real-world analogies (ticket counter, printer queue, mail/SMS pipeline)
- Queue-specific methods: offer, poll, peek, element, remove — exact behavior when queue is empty (null vs exception)
- The three critical pairs: offer vs add, poll vs remove, peek vs element
- PriorityQueue — the only Queue implementation class required for OCJP/SCJP basic syllabus
- PriorityQueue complete property sheet: heap data structure, null rejection, Comparable/Comparator rules, NOT FIFO
- PriorityQueue constructors (same natural vs customized pattern as TreeSet)
- Demo 1: PriorityQueue with Integer — default natural ascending (smallest = highest priority)
- Demo 2: PriorityQueue with Integer + Comparator — descending / max-heap behavior
- Demo 3: PriorityQueue with String — alphabetical natural order
- Demo 4: PriorityQueue with StringBuffer → ClassCastException (non-Comparable, no Comparator)
- Iterator order vs poll() order — the #1 PriorityQueue exam trap
- Queue vs PriorityQueue vs Stack — LIFO vs FIFO vs priority
- OCJP/SCJP exam checklist
What continues in next session (Video 151):

- Java 1.6 enhancements: NavigableSet, NavigableMap
- Collections utility class sort() methods
Exam mantra: For basic OCJP/SCJP, know Queue interface methods and PriorityQueue only. BlockingQueue, LinkedBlockingQueue, etc. are advanced — not mandatory at basic level. PriorityQueue = heap, not FIFO; iterator ≠ poll order; null → NPE; non-Comparable without Comparator → ClassCastException.

## 00:04 — Recap: Map module complete; Queue is next

### Where we are in the Collections Framework

Sir opens by confirming the Map half is finished (HashMap through Properties in prior sessions). The Collection side still had one remaining child interface:

Collection (I)
 ├── List (I)           ✓ covered
 ├── Set (I)            ✓ covered
 │    └── SortedSet …   ✓ covered (TreeSet, Comparator)
 └── Queue (I)          ← TODAY
      └── PriorityQueue (C)   ← only impl required for basic exam

Board note from Video 149 closing:

"Next what we have to discuss — Queue. In Collections, one more remaining part — Queue. That part we will discuss."

### Queue version history

- Entire Queue concept introduced in Java 1.5
- Same release as generics, enums, autoboxing, java.util.concurrent package foundations
## 02:15 — Queue interface: child of Collection

### Hierarchy (board — copy exactly)

Collection (I)
 └── Queue (I)
      ├── PriorityQueue (C)        ← OCJP/SCJP basic level focus
      └── BlockingQueue (I)        ← advanced; NOT required for basic exam
           ├── PriorityBlockingQueue
           ├── LinkedBlockingQueue
           └── ArrayBlockingQueue, SynchronousQueue, DelayQueue, …

Sir's exam filter (confirmed in Video 151 recap):

- Queue concept — must know
- PriorityQueue — only implementation class needed at basic level
- BlockingQueue family — mentioned for awareness; advanced collections module
### Technical definition (Java API wording Sir uses)

Prior to processing — if you want to represent a group of individual objects, go for Queue.

Meaning:

- Objects wait in line before the actual work happens
- Before sending mail, before printing, before an officer processes your passport request
- Queue = holding area / waiting line
### FIFO principle — First In, First Out

Board definition:

Usually Queue follows FIFO (First In First Out) order.

FIFO rule: The element inserted first is removed first. Like a real-world queue — whoever stands first gets served first.

Sir's classroom analogies (repeat on board):

### Queue is NOT a standalone concept outside Collection

Because Queue extends Collection:

- All 12 Collection methods inherited: add, remove, size, isEmpty, contains, iterator, etc.
- Queue adds queue-specific insertion/removal/inspection methods tuned for FIFO head/tail operations
- You can declare: Queue q = new PriorityQueue(); — interface reference, concrete implementation
```java
import java.util.*;

public class QueueHierarchyDemo {
    public static void main(String[] args) {
        // Queue is child of Collection — IS-A relationship
        Queue<String> q = new PriorityQueue<>();
        Collection<String> c = q;   // valid — Queue IS-A Collection

        q.offer("first");
        q.offer("second");
        System.out.println(c.size());     // 2 — inherited from Collection
        System.out.println(q.poll());     // first — Queue-specific removal
    }
}
```

## 08:40 — Queue interface methods (the five core operations)

Sir writes the Queue-specific methods on the board. These are the methods that define queue behavior at the head (front of the line).

### The five methods — two groups

### Method signatures and return types

```java
// Insertion
boolean offer(E e);          // Queue-specific — preferred for queues
boolean add(E e);            // Inherited from Collection

// Removal — returns removed element, or null / exception
E poll();                    // Queue-specific — returns null if empty
E remove();                  // Inherited — throws NoSuchElementException if empty

// Inspection — returns head element without removing
E peek();                    // Queue-specific — returns null if empty
E element();                 // Inherited — throws NoSuchElementException if empty
```

### Behavior when queue is EMPTY — exam-critical table

Sir's board wording (copy for exam):

poll() and peek() — if queue is empty → return `null`.

remove() and element() — if queue is empty → throw `NoSuchElementException`.

### Why two methods for the same operation?

Historical and API-design reason:

- add, remove, element come from Collection interface (Java 1.2) — fail-fast with exceptions
- offer, poll, peek added in Queue interface (Java 1.5) — graceful null return for empty queue
- For queue programming, Sir recommends mentally defaulting to `offer` / `poll` / `peek` trio
## 14:20 — offer vs add, poll vs remove, peek vs element

### Pair 1: `offer` vs `add` (insertion)

```java
import java.util.*;

public class OfferVsAddDemo {
    public static void main(String[] args) {
        Queue<String> q = new PriorityQueue<>();

        // Both work on unbounded PriorityQueue
        System.out.println(q.offer("A"));   // true
        System.out.println(q.add("B"));     // true — inherited Collection method

        System.out.println(q);              // heap internal order — NOT insertion order
    }
}
```

### Pair 2: `poll` vs `remove` (removal from head)

```java
import java.util.*;

public class PollVsRemoveDemo {
    public static void main(String[] args) {
        Queue<Integer> q = new PriorityQueue<>();
        q.offer(10);
        q.offer(20);

        System.out.println(q.poll());    // 10 — removes head (smallest for natural order)
        System.out.println(q.poll());    // 20 — removes head
        System.out.println(q.poll());    // null — empty, NO exception

        Queue<Integer> q2 = new PriorityQueue<>();
        // q2.remove();   // NoSuchElementException — queue is empty!
    }
}
```

### Pair 3: `peek` vs `element` (inspect head only)

```java
import java.util.*;

public class PeekVsElementDemo {
    public static void main(String[] args) {
        Queue<String> q = new PriorityQueue<>();
        q.offer("Durga");
        q.offer("Java");

        System.out.println(q.peek());     // Durga — still in queue
        System.out.println(q.size());     // 2 — peek did NOT remove
        System.out.println(q.element());  // Durga — same head, still in queue

        q.poll();
        q.poll();
        System.out.println(q.peek());     // null — empty
        // System.out.println(q.element()); // NoSuchElementException
    }
}
```

### Summary mnemonic (board)

Graceful (null):     offer  →  poll  →  peek
Strict (exception):  add    →  remove →  element

## 18:50 — FIFO demo with LinkedList as Queue

Before PriorityQueue, Sir demonstrates pure FIFO using LinkedList (implements Queue):

```java
import java.util.*;

public class FifoQueueDemo {
    public static void main(String[] args) {
        // LinkedList implements Queue — true FIFO
        Queue<String> ticketQueue = new LinkedList<>();

        ticketQueue.offer("Person-1");   // first in line
        ticketQueue.offer("Person-2");
        ticketQueue.offer("Person-3");

        // Serve in FIFO order
        System.out.println(ticketQueue.poll());   // Person-1
        System.out.println(ticketQueue.poll());   // Person-2
        System.out.println(ticketQueue.poll());   // Person-3
        System.out.println(ticketQueue.poll());   // null — queue empty
    }
}
```

Output:

Person-1
Person-2
Person-3
null

Sir's point: This is textbook FIFO. PriorityQueue breaks this rule — next section.

## 22:10 — PriorityQueue introduction

### Why PriorityQueue exists

Sometimes FIFO is wrong:

- Hospital emergency room — critical patient first, not whoever arrived first
- OS task scheduler — higher priority process runs first
- Event with VIP passes — VIP before general admission
Board conclusion:

Based on requirement, we can implement priority order → PriorityQueue.

### Only implementation class for basic OCJP/SCJP

Sir explicitly states (confirmed Video 151 recap):

- At basic exam level → PriorityQueue only
- Do not spend exam prep time on BlockingQueue implementations
- Know they exist in java.util.concurrent for advanced/thread-safe scenarios
### Class declaration

```java
public class PriorityQueue<E> extends AbstractQueue<E>
        implements Queue<E>, Serializable { ... }
```

- Package: java.util
- Introduced: Java 1.5
- Implements: Queue, Serializable
- Does NOT implement: RandomAccess, Cloneable
## 25:30 — PriorityQueue: complete property sheet (board conclusions)

Copy these exactly — same style as TreeSet property sheet (Video 143):

### Board wording (Sir's exact phrases)

"Underlying data structure — Heap."

"Null — such a type of story — not applicable for PriorityQueue. Otherwise we will get runtime exception saying NullPointerException."

"PriorityQueue is NOT following FIFO order. It follows priority order."

"For default natural sorting order — objects must be homogeneous and Comparable; otherwise ClassCastException."

### Priority / "smallest = highest priority" convention

Sir clarifies the default natural-order behavior for numbers:

- Default constructor → natural ascending order via Comparable
- For Integer: smallest number = highest priority (removed first by poll())
- Internally: min-heap — root is the smallest element
- Colloquial "priority 1 = most important" differs from Java's default numeric PQ — here minimum value exits first
Memory aid:

Natural order Integer PQ → min-heap → poll() always gives smallest remaining number.

### PriorityQueue vs TreeSet — duplicate handling trap

## 30:15 — PriorityQueue constructors

Same two-constructor emphasis as TreeSet (Video 143) — Sir: "We are going to use minimum 10 times these two words: default natural sorting order and customized sorting order."

### All constructors (OCJP-relevant)

### Constructor thumb rules (identical to TreeSet)

PriorityQueue q = new PriorityQueue();              // → default natural sorting order
PriorityQueue q = new PriorityQueue(new MyComp()); // → customized sorting order

Exam trap: Default initial capacity of PriorityQueue = 11 (same as Hashtable, NOT 16 like HashMap/HashSet).

## 33:40 — Demo 1: PriorityQueue with Integer — natural ascending (min-heap)

### Program

```java
import java.util.*;

public class PriorityQueueDemo1 {
    public static void main(String[] args) {
        PriorityQueue<Integer> pq = new PriorityQueue<>();  // default natural sorting

        pq.offer(30);
        pq.offer(10);
        pq.offer(20);
        pq.offer(5);

        System.out.println("Queue object: " + pq);
        // Internal heap — toString order is NOT guaranteed sorted

        System.out.println("poll(): " + pq.poll());   // 5  — smallest = highest priority
        System.out.println("poll(): " + pq.poll());   // 10
        System.out.println("poll(): " + pq.poll());   // 20
        System.out.println("poll(): " + pq.poll());   // 30
        System.out.println("poll(): " + pq.poll());   // null
    }
}
```

### Expected output (poll sequence)

Queue object: [5, 10, 20, 30]   // may vary — heap array layout; do NOT trust for iteration
poll(): 5
poll(): 10
poll(): 20
poll(): 30
poll(): null

### Step-by-step poll trace

### Key observations

- Insertion order was 30, 10, 20, 5 — poll order completely different
- NOT FIFO — 30 was inserted first but removed last
- System.out.println(pq) before polling may look sorted — coincidence for small integer demo; iterator still does not guarantee sorted traversal
## 38:05 — Demo 2: PriorityQueue with Integer + Comparator — descending (max-heap)

Same pattern as TreeSet descending demo (Video 144):

```java
import java.util.*;

public class PriorityQueueDemo2 {
    public static void main(String[] args) {
        PriorityQueue<Integer> pq = new PriorityQueue<>(new MyComparator());

        pq.offer(10);
        pq.offer(0);
        pq.offer(15);
        pq.offer(5);
        pq.offer(20);
        pq.offer(20);   // duplicate — BOTH kept (unlike TreeSet)

        System.out.println("poll order:");
        while (pq.peek() != null) {
            System.out.println(pq.poll());
        }
    }
}

class MyComparator implements Comparator {
    public int compare(Object o1, Object o2) {
        Integer I1 = (Integer) o1;
        Integer I2 = (Integer) o2;

        if (I1 < I2)
            return +1;      // smaller → lower priority → comes out later
        else if (I1 > I2)
            return -1;      // bigger → higher priority → comes out first
        else
            return 0;
    }
}
```

### Expected output (poll order — descending)

poll order:
20
20
15
10
5
0

### Which method does JVM call?

Same TreeSet rule (Video 144):

### Descending compare logic table

## 42:15 — Demo 3: PriorityQueue with String — natural alphabetical order

```java
import java.util.*;

public class PriorityQueueDemo3 {
    public static void main(String[] args) {
        PriorityQueue<String> pq = new PriorityQueue<>();  // default natural sorting

        pq.offer("Z");
        pq.offer("A");
        pq.offer("M");
        pq.offer("B");

        System.out.println("Insertion done: Z, A, M, B");
        System.out.println("Poll order (alphabetical = priority order):");

        while (pq.peek() != null) {
            System.out.println(pq.poll());
        }
    }
}
```

### Expected output

Insertion done: Z, A, M, B
Poll order (alphabetical = priority order):
A
B
M
Z

### Analysis

- Constructor: no-arg → default natural sorting order
- Element type: String — implements Comparable
- Natural order for String = lexicographic (Unicode) alphabetical
- A has highest priority (comes out first) because it is "smallest" in natural String order
- Same Unicode rule as TreeSet (Video 143): lowercase 'a' (97) comes after uppercase 'Z' (90)
### Heterogeneous trap (same as TreeSet)

PriorityQueue pq = new PriorityQueue();
pq.offer("A");
pq.offer(new Integer(10));   // ClassCastException — heterogeneous

## 45:30 — Demo 4: StringBuffer → ClassCastException

Identical lesson to TreeSet Demo 2 (Video 143) — StringBuffer does NOT implement Comparable:

```java
import java.util.*;

public class PriorityQueueDemo4 {
    public static void main(String[] args) {
        PriorityQueue pq = new PriorityQueue();  // default natural sorting — needs Comparable

        pq.offer(new StringBuffer("A"));
        pq.offer(new StringBuffer("Z"));
        // RuntimeException: ClassCastException
        // StringBuffer cannot be cast to Comparable
    }
}
```

### Why ClassCastException?

- Default constructor → JVM uses natural sorting → calls compareTo()
- compareTo() exists only on Comparable types
- StringBuffer does NOT implement Comparable
- JVM tries to treat elements as Comparable internally → ClassCastException
### Fix — pass Comparator (customized sorting)

```java
import java.util.*;

public class PriorityQueueDemo4Fixed {
    public static void main(String[] args) {
        PriorityQueue<StringBuffer> pq =
            new PriorityQueue<>(new StringBufferComparator());

        pq.offer(new StringBuffer("Z"));
        pq.offer(new StringBuffer("A"));

        while (pq.peek() != null) {
            System.out.println(pq.poll());   // A, then Z — by length or custom logic
        }
    }
}

class StringBufferComparator implements Comparator<StringBuffer> {
    public int compare(StringBuffer sb1, StringBuffer sb2) {
        return sb1.toString().compareTo(sb2.toString());
    }
}
```

Board conclusion (same as TreeSet):

If objects are not Comparable and we are not passing Comparator → ClassCastException.

## 48:10 — Null insertion demo → NullPointerException

```java
import java.util.*;

public class PriorityQueueNullDemo {
    public static void main(String[] args) {
        PriorityQueue<String> pq = new PriorityQueue<>();
        pq.offer("A");
        // pq.offer(null);   // NullPointerException — null NOT allowed
    }
}
```

Unlike HashMap (null key once) or TreeSet (null once if alone), PriorityQueue never accepts null — heap cannot compare null priority.

## 49:25 — Iterator order vs poll order (CRITICAL exam trap)

Sir emphasizes this repeatedly — the #1 PriorityQueue trick question:

### The rule

### Demo — iterator vs poll

```java
import java.util.*;

public class PriorityQueueIteratorVsPollDemo {
    public static void main(String[] args) {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.offer(30);
        pq.offer(10);
        pq.offer(20);
        pq.offer(5);

        System.out.print("Iterator order:  ");
        for (Integer i : pq) {
            System.out.print(i + " ");
        }
        // Might print: 5 10 30 20  (heap array layout — NOT sorted, NOT insertion order)

        System.out.println();
        System.out.print("Poll order:      ");
        while (pq.peek() != null) {
            System.out.print(pq.poll() + " ");
        }
        // Guaranteed: 5 10 20 30  (ascending = priority order)
    }
}
```

### Sample output

Iterator order:  5 10 30 20
Poll order:      5 10 20 30

### Board conclusion (must copy)

Iterator of PriorityQueue does not guarantee any particular order.

Only poll() sequence reflects priority order.

If exam asks "output of iterating PriorityQueue" vs "output of repeated poll()" → different answers.

### Why this happens (memory level)

- PriorityQueue stores elements in internal array representing a heap
- Heap property: parent ≤ children (min-heap) — but array is NOT fully sorted
- Iterator walks the array index 0 → n-1 — heap layout order
- poll() always extracts root (index 0), then re-heaps — true priority sequence
## 52:40 — Queue vs PriorityQueue vs Stack

### Three-way comparison table

### Visual diagram (board)

FIFO Queue (LinkedList):     PriorityQueue (min-heap):     Stack (LIFO):

  IN → [A][B][C] → OUT          poll→ 5 (smallest)           push ↓
       ↑       ↑               [5,10,20,30]                  [C] ← top
    tail     head               (NOT FIFO)                    [B]
                                                              [A]
  A out first                   5 out first                   pop → C out first

### Sir's one-liner summary

Queue = who came first gets served first.

PriorityQueue = who has highest priority gets served first — not necessarily who came first.

Stack = who came last gets served first.

## 54:50 — Session wrap-up

### Collection module status after this video

### Next topic (Video 151)

Per session closing and Video 151 opening:

- Java 1.6 version enhancements: NavigableSet, NavigableMap
- Then Collections utility class (sort(), etc.)
## Queue interface methods — complete reference table

## PriorityQueue vs TreeSet — comparison (sorting cousins)

Both use Comparable/Comparator and reject heterogeneous natural-order mixes — but different contracts:

## OCJP / SCJP exam rapid-fire Q&A

## OCJP/SCJP exam checklist

### Must know definitions

- [ ] Queue is child interface of Collection
- [ ] Use Queue for prior to processing scenarios
- [ ] FIFO = First In First Out (general Queue concept)
- [ ] PriorityQueue = only basic-exam Queue implementation class
- [ ] PriorityQueue underlying DS = heap
- [ ] PriorityQueue is NOT FIFO
### Must know method behavior

- [ ] offer / poll / peek → null-safe on empty queue
- [ ] add / remove / element → exception on empty queue (or full for add)
- [ ] poll() removes; peek() does not
- [ ] Natural order Integer PQ → smallest polled first
### Must know constructor rules

- [ ] No-arg / capacity-only → default natural sorting order (Comparable required)
- [ ] Comparator arg → customized sorting order
- [ ] Default initial capacity = 11
### Must know exception traps

- [ ] null → NullPointerException
- [ ] Non-Comparable without Comparator → ClassCastException
- [ ] Heterogeneous mix with natural constructor → ClassCastException
- [ ] Empty queue + remove() / element() → NoSuchElementException
### Likely trap questions

- Insert 30, 10, 20 into PriorityQueue — what does first poll() return? → 10 (not 30)
- Iterator vs poll order on same PriorityQueue → different
- poll() on empty queue — exception or null? → null
- remove() on empty queue — exception or null? → NoSuchElementException
- StringBuffer in default PriorityQueue → ClassCastException
- Is PriorityQueue thread-safe? → No
- PriorityQueue vs TreeSet on duplicate insert → PQ allows, TreeSet rejects
- Default capacity: PriorityQueue vs HashMap → 11 vs 16
## Cross-references (playlist)

## Board diagrams to reproduce

### Diagram 1: Collection hierarchy — Queue branch

Collection (I)
 ├── List (I)
 ├── Set (I)
 │    └── SortedSet (I) → TreeSet
 └── Queue (I)  ← prior to processing, usually FIFO
      └── PriorityQueue (C)  ← heap, priority order, NOT FIFO

### Diagram 2: Queue method pairs

INSERT           REMOVE           INSPECT
Graceful: offer(e)  →   poll()      →    peek()
          ↓ null if empty              ↓ null if empty

Strict:   add(e)    →   remove()    →    element()
          ↓ exception if full        ↓ NoSuchElementException if empty

### Diagram 3: Min-heap after inserting 30, 10, 20, 5

5          ← root = smallest = first poll()
       / \
     10   30
    /
   20

poll() sequence: 5 → 10 → 20 → 30
iterator walk:   may NOT match this visual left-to-right

### Diagram 4: FIFO vs Priority vs LIFO

FIFO (Queue):     enter A, B, C  →  exit A, B, C
Priority (PQ):    enter 30,10,20 →  exit 10, 20, 30 (natural Integer)
LIFO (Stack):     push A, B, C   →  pop C, B, A

## Metadata

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Collections Part-15 \ | \ | queue |
| URL | https://www.youtube.com/watch?v=JOoq94-UQ-A |  |  |
| Video ID | JOoq94-UQ-A |  |  |
| Duration | 57m 26s |  |  |
| Position | Video 150 of 203 in the Durga Sir OCJP/SCJP playlist |  |  |
| Source | Synthesized from adjacent lectures + standard syllabus (captions unavailable; Whisper blocked) |  |  |
| Prerequisite | Videos 137 (Queue intro in 9-interfaces), 143–144 (TreeSet / Comparable / Comparator), 149 (Hashtable — session ends with "next topic is Queue") |  |  |
| Output | 150-queue-priorityqueue.doc |  |  |

| Real-world scenario | Queue behavior |
|---|---|
| Ticket counter at cinema | First person in line gets ticket first |
| Temple / passport office queue | First devotee/applicant served first |
| Printer job queue | First document sent to printer prints first |
| Mail sending application | First mail ID added is sent first |
| Bulk SMS (10 lakh numbers) | Messages delivered in order they were queued |

| Purpose | Returns null when empty | Throws exception when empty |
|---|---|---|
| Insert at tail | offer(e) | add(e) (inherited from Collection) |
| Remove from head | poll() | remove() (inherited from Collection) |
| Inspect head (no remove) | peek() | element() |

| Method | Queue empty — result | Exception? |
|---|---|---|
| offer(e) | Inserts element; returns true | Never throws for full queue in unbounded PriorityQueue |
| add(e) | Inserts element; returns true | IllegalStateException if capacity-restricted queue is full |
| poll() | Returns `null` | No exception |
| remove() | — | `NoSuchElementException` |
| peek() | Returns `null` | No exception |
| element() | — | `NoSuchElementException` |

|  | offer(e) | add(e) |
|---|---|---|
| Origin | Queue interface (1.5) | Collection interface (1.2) |
| Return | boolean — false if cannot insert (bounded queue full) | boolean — but throws on failure |
| On full bounded queue | Returns false | Throws IllegalStateException |
| PriorityQueue (unbounded) | Always succeeds; returns true | Always succeeds; returns true |
| Exam default | Preferred queue idiom | Works, but exception on full |

|  | poll() | remove() |
|---|---|---|
| Empty queue | Returns `null` | Throws `NoSuchElementException` |
| Non-empty | Removes and returns head | Removes and returns head |
| Sir's recommendation | Use this for queues | Risky if emptiness not guaranteed |

|  | peek() | element() |
|---|---|---|
| Empty queue | Returns `null` | Throws `NoSuchElementException` |
| Non-empty | Returns head; does not remove | Returns head; does not remove |
| Use case | Safe check before poll | Fail-fast if queue must not be empty |

| # | Property | PriorityQueue value |
|---|---|---|
| 1 | Underlying data structure | Heap (binary heap — min-heap for natural ascending order) |
| 2 | Duplicate objects | Allowed (unlike Set — Queue is NOT a Set) |
| 3 | Insertion order | NOT preserved |
| 4 | Removal order (poll) | Priority order — highest priority element first; NOT FIFO |
| 5 | Heterogeneous objects | NOT allowed (with default natural-order constructor) |
| 6 | Null insertion | NOT allowed → NullPointerException |
| 7 | Natural sorting requirement | Elements must be homogeneous and Comparable (default constructor) |
| 8 | Non-Comparable elements | Allowed only if Comparator passed to constructor |
| 9 | Implements Serializable | Yes |
| 10 | Implements RandomAccess | No |
| 11 | Thread-safe | No |
| 12 | Best choice when | Prior to processing with priority (not strict arrival order) |

| Collection | compare / compareTo returns 0 | Result |
|---|---|---|
| TreeSet | Duplicate | Second element NOT inserted |
| PriorityQueue | "Equal" priority | Both elements kept — duplicates allowed |

| # | Signature | Sorting order | Notes |
|---|---|---|---|
| 1 | new PriorityQueue() | Default natural sorting | Empty queue; default initial capacity 11 |
| 2 | new PriorityQueue(int initialCapacity) | Default natural sorting | User-specified capacity; still grows dynamically |
| 3 | new PriorityQueue(Comparator c) | Customized sorting | Comparator defines priority |
| 4 | new PriorityQueue(int initialCapacity, Comparator c) | Customized sorting | Capacity + Comparator |
| 5 | new PriorityQueue(Collection c) | Natural order of elements | Builds heap from collection's elements |
| 6 | new PriorityQueue(PriorityQueue c) | Same order as source | Copy constructor |
| 7 | new PriorityQueue(SortedSet c) | Same order as sorted set | Since Java 1.8 |

| Step | poll() returns | Remaining in PQ | Reason |
|---|---|---|---|
| Initial | — | {30, 10, 20, 5} | Insertion order irrelevant |
| 1 | 5 | {10, 20, 30} | 5 is smallest → highest priority |
| 2 | 10 | {20, 30} | Next smallest |
| 3 | 20 | {30} | Next smallest |
| 4 | 30 | {} | Last element |
| 5 | null | {} | Empty queue |

| Constructor | Comparison method invoked |
|---|---|
| new PriorityQueue() | compareTo() — natural order |
| new PriorityQueue(new MyComparator()) | compare() — customized order |

| Condition | Return | Meaning in descending PQ |
|---|---|---|
| I1 < I2 | +1 (positive) | Smaller element has lower priority |
| I1 > I2 | -1 (negative) | Bigger element has higher priority |
| I1 == I2 | 0 | Equal priority — duplicate kept |

| Operation | Order guarantee |
|---|---|
| poll(), peek(), remove(), element() | Priority order (head = highest priority) |
| iterator(), enhanced for-loop, forEach | NO order guarantee — not sorted, not insertion order, not poll order |
| System.out.println(pq) | Uses internal array toString() — unreliable for predicting iteration order |

| Feature | Queue (FIFO impl e.g. LinkedList) | PriorityQueue | Stack (legacy Vector-based) |
|---|---|---|---|
| Principle | FIFO — First In First Out | Priority order — highest priority first | LIFO — Last In First Out |
| Insert | offer() at tail | offer() — position by priority | push() at top |
| Remove | poll() from head | poll() — highest priority element | pop() from top |
| Inspect | peek() at head | peek() at highest priority | peek() at top |
| Underlying DS | Linked list (for LinkedList) | Binary heap | Dynamic array (Vector) |
| Implementation | LinkedList, ArrayDeque | PriorityQueue | Stack (legacy, extends Vector) |
| OCJP basic focus | Concept only | YES — main impl | Already covered (List module) |
| Ordering | Arrival / insertion order | Comparable / Comparator | Reverse arrival order |

| Collection branch | Status |
|---|---|
| List (ArrayList, LinkedList, Vector, Stack, CopyOnWriteArrayList) | ✓ |
| Set (HashSet, LinkedHashSet, TreeSet) | ✓ |
| Queue (PriorityQueue) | ✓ (this session) |
| Map (HashMap … Properties) | ✓ (prior sessions) |

| Method | Type | Empty queue behavior | Removes element? |
|---|---|---|---|
| offer(e) | Insert | N/A — inserts | No |
| add(e) | Insert | N/A — inserts (throws if bounded full) | No |
| poll() | Remove/retrieve | Returns null | Yes |
| remove() | Remove/retrieve | NoSuchElementException | Yes |
| peek() | Inspect | Returns null | No |
| element() | Inspect | NoSuchElementException | No |

| Property | TreeSet | PriorityQueue |
|---|---|---|
| Interface | SortedSet / Set | Queue |
| Underlying DS | Red-Black Tree | Binary Heap |
| Duplicates | Not allowed | Allowed |
| Null | Once (with caveats) | Never |
| Iteration order | Sorted order | No guarantee |
| Removal order | Sorted (via iterator) | Priority (poll()) |
| FIFO? | No | No |

| # | Question | Answer |
|---|---|---|
| 1 | Queue is child of which interface? | Collection |
| 2 | Default ordering principle for general Queue? | FIFO |
| 3 | Does PriorityQueue follow FIFO? | No — priority order |
| 4 | Only Queue impl required for basic exam? | PriorityQueue |
| 5 | Underlying DS of PriorityQueue? | Heap |
| 6 | poll() on empty queue? | Returns `null` |
| 7 | remove() on empty queue? | `NoSuchElementException` |
| 8 | peek() on empty queue? | Returns `null` |
| 9 | element() on empty queue? | `NoSuchElementException` |
| 10 | Null allowed in PriorityQueue? | No → NullPointerException |
| 11 | Default Integer PriorityQueue — first poll()? | Smallest number (min-heap) |
| 12 | StringBuffer in default PriorityQueue? | `ClassCastException` |
| 13 | Iterator order same as poll order? | No — iterator unordered |
| 14 | Default initial capacity of PriorityQueue? | 11 |
| 15 | Duplicates in PriorityQueue? | Allowed |
| 16 | Duplicates in TreeSet? | Not allowed |
| 17 | Stack ordering principle? | LIFO |
| 18 | Queue introduced in which Java version? | 1.5 |
| 19 | No-arg PriorityQueue constructor sorting? | Default natural sorting order |
| 20 | Comparator constructor sorting? | Customized sorting order |

| Topic | Video | Notes file |
|---|---|---|
| 9 Collection interfaces incl. Queue intro | 137 | 137-collections-9-interfaces.doc |
| TreeSet properties & Comparable | 143 | 143-treeset.doc |
| Comparator interface deep dive | 144 | 144-comparator.doc |
| Hashtable — ends pointing to Queue | 149 | 149-hashtable.doc |
| Queue & PriorityQueue | 150 | 150-queue-priorityqueue.doc |
| NavigableSet recap confirms PQ done | 151 | 151-navigableset.doc |

| Field | Value |
|---|---|
| Video | 150 of 203 |
| Series | Durga Sir Core Java OCJP/SCJP |
| Topic | Collections Part-15 — Queue & PriorityQueue |
| Source | Synthesized from adjacent lectures + standard syllabus (captions unavailable; Whisper blocked) |
| Output | 150-queue-priorityqueue.doc |
