# Video 141 — Collections Part-6: Limitations of Enumeration, Iterator & ListIterator

## Video info

## Session overview

Continuation of the Three Cursors topic started in Video 140 (Enumeration demo). Video 141 completes the cursor hierarchy:

- Recap — Enumeration from last session (last example covered)
- Limitations of Enumeration — why Iterator was introduced (Java 1.2)
- Iterator — universal cursor; methods; live demo (filter even numbers + remove odds)
- Limitations of Iterator — why ListIterator was introduced
- ListIterator — bidirectional cursor; 9 methods; live demo (remove, add, replace)
- Most powerful cursor — ListIterator (with its own limitation)
- Comparison table — Enumeration vs Iterator vs ListIterator (5 properties)
- Internal implementation — anonymous inner class / inner class names via getClass().getName()
Prerequisite from Video 140: To retrieve objects one-by-one from a collection, we need a cursor. The first cursor is Enumeration (Java 1.0, legacy only).

## 00:07 — Recap: Enumeration from previous session

### Purpose of cursors

If you want to get objects one by one from a collection, you must use a cursor.

### Enumeration recap

Enumeration is the first cursor — but if a newer cursor (Iterator, ListIterator) exists, the old one must have problems/limitations. New concepts exist to overcome old limitations.

## 01:13 — Limitations of Enumeration

### Board heading (copy exactly)

Limitations of Enumeration

### Limitation 1 — Not a universal cursor (legacy classes only)

Enumeration concept came in Java 1.0. It is applicable only for legacy classes.

Board note:

We can apply enumeration concept only for legacy classes, and it is not a universal cursor.

You cannot apply Enumeration everywhere — only legacy classes (Vector, Hashtable, etc.) expose elements().

```java
import java.util.*;

public class EnumerationLegacyOnlyDemo {
    public static void main(String[] args) {
        // OK — Vector is legacy
        Vector<String> v = new Vector<>();
        v.add("A");
        Enumeration<String> e = v.elements();
        while (e.hasMoreElements()) {
            System.out.println(e.nextElement());
        }

        // ArrayList has NO elements() method — cannot use Enumeration
        ArrayList<String> list = new ArrayList<>();
        list.add("X");
        // list.elements();  // CE: method does not exist on ArrayList
    }
}
```

### Limitation 2 — Read-only; no remove capability

Classroom analogy (mango box):

Durga Sir gives a box of mangoes. You eat them one by one. When you pick the third mango and find it damaged, you have three options:

- Throw it out (remove from box) — recommended
- Put it back in the box
- Eat it anyway (waste nothing)
For collections, option 1 (remove bad object while iterating) is the right approach — but Enumeration cannot remove.

Enumeration has only 2 methods:

No `remove()` method.

Board note:

By using enumeration we can get only read access. We can't perform remove operation.

### Overcoming Enumeration limitations → Iterator

Board note:

To overcome above limitations, we should go for Iterator.

## 08:01 — Iterator (second cursor)

### First conclusion about Iterator

Board notes:

- We can apply iterator concept for any collection object, and hence it is a universal cursor.
- By using iterator we can perform both read and remove operations.
Iterator came in Java 1.2 — shorter method names than Enumeration.

### How to get Iterator object

Collection interface defines:

```java
public Iterator iterator();
```

Example:

Iterator it = c.iterator();

Where `c` = any Collection object (ArrayList, LinkedList, Vector, HashSet, etc.).

Board note:

We can create Iterator object by using iterator() method of Collection interface.

```java
public Iterator iterator();
```

### Iterator methods (3 methods)

Speciality vs Enumeration: Extra `remove()` capability.

Compare naming:

## 12:54 — Iterator demo: print even numbers, remove odd numbers

### Problem statement

Create ArrayList with integers 0 through 10 (11 objects). Print only even numbers, and remove odd numbers from the list while iterating.

### Step-by-step logic

- ArrayList l = new ArrayList();
- Add 0, 1, 2, … 10 via loop
- System.out.println(l); → [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
- Get iterator: Iterator it = l.iterator();
- while (it.hasNext())
- Integer I = (Integer) it.next(); — cast because we added int (auto-boxed)
- If even (I % 2 == 0) → print
- Else → it.remove() — odd numbers removed from list
- After loop, System.out.println(l); → [0, 2, 4, 6, 8, 10] only
Key point: This remove while iterating is not possible with Enumeration.

### Full demo program

```java
import java.util.*;

public class IteratorDemo {
    public static void main(String[] args) {
        ArrayList<Integer> l = new ArrayList<>();

        for (int i = 0; i <= 10; i++) {
            l.add(i);
        }

        System.out.println("Before iteration: " + l);
        // Before iteration: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        Iterator<Integer> it = l.iterator();

        while (it.hasNext()) {
            Integer I = it.next();

            if (I % 2 == 0) {
                System.out.println(I);   // prints 0, 2, 4, 6, 8, 10
            } else {
                it.remove();             // odd numbers removed from underlying list
            }
        }

        System.out.println("After iteration: " + l);
        // After iteration: [0, 2, 4, 6, 8, 10]
    }
}
```

### Expected output

Before iteration: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
0
2
4
6
8
10
After iteration: [0, 2, 4, 6, 8, 10]

Odd numbers are permanently removed from the list because of it.remove().

## 24:33 — Limitations of Iterator

Even Iterator has limitations (same pattern: old cursor → problems → new cursor).

### Board heading

Limitations of Iterator

### Limitation 1 — Single-direction cursor (forward only)

Both Enumeration and Iterator can move only in forward direction.

List:  [ A ] [ B ] [ C ] [ D ]
              ↑ cursor
              → next → next → next   (only forward)

You can ask "what is the next element?" but not "what is the previous element?" even though previous elements exist in the list.

Board note:

By using enumeration and iterator we can always move only towards forward direction, and we can't move towards backward direction. These are single direction cursors (only forward), but not bidirectional cursors.

### Limitation 2 — No add or replace; only read + remove

By using Iterator we can perform only:

- Read operation
- Remove operation
We cannot:

- Add new objects while iterating
- Replace existing object with a new object
Board note:

By using iterator we can perform only read and remove operations. We can't perform replacement and addition of new objects.

### Overcoming Iterator limitations → ListIterator

Board note:

To overcome above limitations, we should go for ListIterator.

## 30:33 — ListIterator (third cursor — most powerful)

### First conclusion — Bidirectional cursor

Board notes:

- By using ListIterator we can move either to the forward direction or to the backward direction, and hence it is a bidirectional cursor.
- We can perform replacement and addition of new objects, in addition to read and remove operations.
### How to get ListIterator object

List interface defines:

```java
public ListIterator listIterator();
```

Example:

ListIterator ltr = l.listIterator();

Where `l` = any List object (ArrayList, LinkedList, Vector, etc.) — must be a List, not any Collection.

Board note:

We can create ListIterator object by using listIterator() method of List interface.

```java
public ListIterator listIterator();
```

### ListIterator extends Iterator

Important relationship:

ListIterator is the child interface of Iterator.

Therefore all 3 Iterator methods are by default available in ListIterator:

- hasNext()
- next()
- remove()
Plus 6 additional methods → total 9 methods.

### ListIterator — all 9 methods

Board heading: ListIterator defines the following nine methods.

#### Group A — Forward movement (3 methods)

#### Group B — Backward movement (3 methods)

#### Group C — Extra operations (3 methods)

Summary structure:

- 3 methods → forward movement
- 3 methods → backward movement
- 3 methods → extra operations (remove, add, replace)
ListIterator is the most powerful cursor because it is bidirectional and supports addition, replacement, remove, forward movement, and backward movement.

## 45:57 — ListIterator demo: remove, add, replace on LinkedList

### Setup

```java
LinkedList<String> l = new LinkedList<>();
l.add("Balakrishna");
l.add("Venkatesh");
l.add("Chiranjeevi");
```

System.out.println(l); → [Balakrishna, Venkatesh, Chiranjeevi] (insertion order preserved)

### Walk-through operations

```java
ListIterator<String> ltr = l.listIterator();

while (ltr.hasNext()) {
    String s = ltr.next();

    if (s.equals("Venkatesh")) {
        ltr.remove();                    // remove Venkatesh
        ltr.add("Venkatesh2");           // add immediately after current position
    }

    if (s.equals("Chiranjeevi")) {
        ltr.set("Charan");               // replace Chiranjeevi with Charan
    }
}
```

### State after each operation

### Full demo program

```java
import java.util.*;

public class ListIteratorDemo {
    public static void main(String[] args) {
        LinkedList<String> l = new LinkedList<>();
        l.add("Balakrishna");
        l.add("Venkatesh");
        l.add("Chiranjeevi");

        System.out.println("Initial: " + l);
        // Initial: [Balakrishna, Venkatesh, Chiranjeevi]

        ListIterator<String> ltr = l.listIterator();

        while (ltr.hasNext()) {
            String s = ltr.next();
            System.out.println("Current: " + s);

            if (s.equals("Venkatesh")) {
                ltr.remove();
                ltr.add("Venkatesh2");
            }

            if (s.equals("Chiranjeevi")) {
                ltr.set("Charan");
            }
        }

        System.out.println("Final: " + l);
        // Final: [Balakrishna, Venkatesh2, Charan]
    }
}
```

### Expected output

Initial: [Balakrishna, Venkatesh, Chiranjeevi]
Current: Balakrishna
Current: Venkatesh
Current: Chiranjeevi
Final: [Balakrishna, Venkatesh2, Charan]

Operations demonstrated:

## 53:31 — Most powerful cursor + its limitation

### Board conclusion

The most powerful cursor is ListIterator.

But its limitation:

It is applicable only for List objects — not a universal cursor.

## 55:07 — Comparison table of three cursors

### Board heading

Comparison table of three cursors

### Quick exam memory chart

Enumeration  → legacy only  → read only           → 2 methods → Vector.elements()
Iterator     → universal     → read + remove       → 3 methods → Collection.iterator()
ListIterator → List only     → read+remove+add+set → 9 methods → List.listIterator()

## 1:05:08 — Internal implementation of cursors (important loophole)

### Student doubt

Enumeration, Iterator, and ListIterator are interfaces. We cannot create objects for interfaces directly. So how do we get "enumeration object", "iterator object", "list iterator object"?

### Answer

We are NOT creating objects for the interface. We are getting objects of implementation classes that implement these interfaces internally.

Vector v = new Vector();

Enumeration e = v.elements();       // implementation class object, not interface object
Iterator i = v.iterator();          // implementation class object
ListIterator ltr = v.listIterator(); // implementation class object

### Discover implementation class name

Use `getClass().getName()`:

```java
System.out.println(e.getClass().getName());
System.out.println(i.getClass().getName());
System.out.println(ltr.getClass().getName());
```

### Full demo program

```java
import java.util.*;

public class CursorImplementationDemo {
    public static void main(String[] args) {
        Vector v = new Vector();
        v.add("A");
        v.add("B");

        Enumeration e = v.elements();
        Iterator i = v.iterator();
        ListIterator ltr = v.listIterator();

        System.out.println("Enumeration impl: " + e.getClass().getName());
        System.out.println("Iterator impl:    " + i.getClass().getName());
        System.out.println("ListIterator impl:" + ltr.getClass().getName());
    }
}
```

### Expected output (Vector)

Enumeration impl: java.util.Vector$1
Iterator impl:    java.util.Vector$Itr
ListIterator impl:java.util.Vector$ListItr

### Meaning of class names

Dollar symbol rule:

- Format: OuterClass$InnerClassName
- If number after $ (e.g. $1) → anonymous inner class (no name)
Board note:

Internal implementation of cursors — inside Vector class, inner classes are present which implement these interfaces. We are getting implementation class objects, not interface objects.

## Hierarchy diagram (conceptual)

Cursor (concept)
                         |
        +----------------+----------------+
        |                |                |
   Enumeration        Iterator       ListIterator
   (Java 1.0)        (Java 1.2)      (Java 1.2)
   legacy only       universal        List only
   read only         read+remove      read+remove+add+set
   forward only      forward only     forward + backward
        |                |                |
        |                +--------> child interface
        |                                 |
   Vector.elements()              List.listIterator()
   2 methods                       9 methods (3+3+3)

## Exam checklist (must memorize)

- [ ] Three cursors: Enumeration, Iterator, ListIterator
- [ ] Enumeration limitations: legacy only + read only
- [ ] Iterator overcomes: universal + remove
- [ ] Iterator limitations: forward only + no add/replace
- [ ] ListIterator overcomes: bidirectional + add/replace/set
- [ ] ListIterator limitation: List objects only
- [ ] Most powerful cursor = ListIterator
- [ ] Universal cursor = Iterator
- [ ] Enumeration methods: hasMoreElements(), nextElement()
- [ ] Iterator methods: hasNext(), next(), remove()
- [ ] ListIterator: 9 methods (3 forward + 3 backward + 3 extra)
- [ ] iterator() from Collection interface; listIterator() from List interface
- [ ] Cursor objects are implementation class objects — use getClass().getName() to find them
- [ ] Vector inner classes: $1 (anonymous Enumeration), $Itr, $ListItr
## Common exam traps

- "Can we use Enumeration on ArrayList?" → No. Only legacy classes.
- "Can Iterator move backward?" → No. Forward only. Use ListIterator for backward.
- "Can Iterator add elements while iterating?" → No. Use ListIterator.add().
- "Is ListIterator universal?" → No. List objects only — but it is the most powerful.
- "How many methods in ListIterator?" → 9 (not 3 — it inherits 3 from Iterator + 6 own).
- "What does set() do in ListIterator?" → Replaces current element (replacement operation).
- "What does add() do in ListIterator?" → Adds permanently to list immediately after current position.
## Summary (one paragraph)

Video 141 completes Java's three collection cursors. Enumeration (1.0) works only on legacy classes and supports read-only forward traversal. Iterator (1.2) is the universal cursor for any collection, adding remove() while still moving forward only. ListIterator (1.2), a child of Iterator, is the most powerful cursor — bidirectional with add/replace/remove — but restricted to List implementations. A five-property comparison table covers applicability, legacy status, movement direction, allowed operations, and how to obtain each cursor. Internally, concrete collection classes (e.g. Vector) use inner/anonymous inner classes to implement these interfaces; getClass().getName() reveals names like Vector$1, Vector$Itr, and Vector$ListItr.

## What's next

Video 142 continues the Collections series (next topic per playlist index).

End of Video 141 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 141 of 203 |  |  |
| Title | Core Java With OCJP/SCJP: Collections Part-6 \ | \ | limitations of enumerations |
| URL | https://www.youtube.com/watch?v=E2uSAGD3-UY |  |  |
| Duration | 1h 15m 07s |  |  |
| Source | YouTube auto-captions (yt-dlp + node PO token) |  |  |
| Instructor | Durga Sir (OCJP/SCJP) |  |  |

| Step | Code / concept |
|---|---|
| Get Enumeration | Enumeration e = v.elements(); |
| Check more elements | e.hasMoreElements() |
| Get next element | e.nextElement() |

| Collection | Can get Enumeration? |
|---|---|
| Vector | Yes |
| Stack | Yes |
| ArrayList | No |
| LinkedList | No |
| Any modern List | No |

| Method | Purpose |
|---|---|
| boolean hasMoreElements() | Are more elements available? |
| Object nextElement() | Return next element |

| Point | Enumeration | Iterator |
|---|---|---|
| Applicability | Legacy classes only | Any collection object |
| Cursor type | Not universal | Universal cursor |
| Operations | Read only | Read + Remove |

| # | Method signature | Purpose |
|---|---|---|
| 1 | public boolean hasNext() | Is next element available? |
| 2 | public Object next() | Return next element |
| 3 | public void remove() | Remove current element from underlying collection |

| Enumeration (1.0) | Iterator (1.2) |
|---|---|
| hasMoreElements() | hasNext() |
| nextElement() | next() |
| (none) | remove() |

| Problem with Iterator | ListIterator solution |
|---|---|
| Forward only | Can move forward OR backward |
| Read + remove only | Read, remove, add, replace |

| Method | Purpose |
|---|---|
| public boolean hasNext() | Is next element there? |
| public Object next() | Return next element |
| public int nextIndex() | Index of next element (List-specific) |

| Method | Purpose |
|---|---|
| public boolean hasPrevious() | Is previous element there? |
| public Object previous() | Return previous element |
| public int previousIndex() | Index of previous element |

| Method | Purpose |
|---|---|
| public void remove() | Remove current element |
| public void add(Object o) | Add new object immediately after current position (permanent add to list) |
| public void set(Object o) | Replace current element with new object |

| After step | List content |
|---|---|
| Initial | [Balakrishna, Venkatesh, Chiranjeevi] |
| After remove() on Venkatesh | [Balakrishna, Chiranjeevi] |
| After add("Venkatesh2") | [Balakrishna, Venkatesh2, Chiranjeevi] |
| After set("Charan") on Chiranjeevi | [Balakrishna, Venkatesh2, Charan] |

| Operation | Method | Meaning |
|---|---|---|
| Read | next() | Get current element |
| Remove | remove() | Remove Venkatesh |
| Add | add("Venkatesh2") | Insert new element after cursor |
| Replace | set("Charan") | Replace Chiranjeevi with Charan |

| Cursor | Scope |
|---|---|
| Enumeration | Legacy classes only |
| Iterator | Any collection (universal) |
| ListIterator | List objects only (most powerful but restricted) |

| Property | Enumeration | Iterator | ListIterator |
|---|---|---|---|
| Where we can apply | Only for legacy classes | For any collection object | Only for List objects |
| Is it Legacy? | Yes (Java 1.0) | No (Java 1.2) | No (Java 1.2) |
| Movement | Single direction (only forward) | Single direction (only forward) | Bidirectional |
| Allowed operations | Read only | Read + Remove | Read + Remove + Replace + Add |
| How to get | elements() method of Vector class | iterator() method of Collection interface | listIterator() method of List interface |
| Number of methods | 2 | 3 | 9 |
| Method names | hasMoreElements(), nextElement() | hasNext(), next(), remove() | 9 methods (3 forward + 3 backward + 3 extra) |

| Output | Meaning |
|---|---|
| java.util.Vector$1 | Anonymous inner class inside Vector implementing Enumeration ($1 = numbered anonymous class) |
| java.util.Vector$Itr | Named inner class Itr inside Vector implementing Iterator |
| java.util.Vector$ListItr | Named inner class ListItr inside Vector implementing ListIterator |
