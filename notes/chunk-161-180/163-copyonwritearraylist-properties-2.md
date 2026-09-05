# Video 163 — Concurrent Collections Part-10: CopyOnWriteArrayList Properties Part-2

## Video info

| Field | Value |
|-------|-------|
| Position | 163 of 203 |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-10 \|\| CopyOnWriteArrayList Properties Part-2 |
| Instructor | Durga Sir (OCJP/SCJP) |
| Duration | 12m 09s |
| Video ID | WHOqKbjQGXI |
| Watch URL | https://www.youtube.com/watch?v=WHOqKbjQGXI |
| Playlist | Core Java With OCJP/SCJP |
| Notes source | YouTube auto-captions (yt-dlp + node PO token) |

> **ASR decode notes:** copy on WR / copy on VAR / copy on writ / copy onary list / copy on wrist = **CopyOnWriteArrayList**; ER list / normal gist / normalist / normal G list / normal are list / normal year list = **ArrayList**; threat / threats = **thread(s)**; fail F / fail first = **fail-fast**; current modification exception / copy concurrent modification = **ConcurrentModificationException**; hetrogeneous = **heterogeneous**; cable = **Serializable**; random XS = **RandomAccess**; unsupported operation Exception = **UnsupportedOperationException**.

## Session overview

Part-2 of CopyOnWriteArrayList properties. Sir covers **similarities with ArrayList** (most properties are identical) and **three critical differences** that matter for exams and interviews.

**Prerequisites:**

| Video | Topic |
|-------|-------|
| 162 | CopyOnWriteArrayList Part-1 — what it is, copy-on-write mechanism |

**What this session covers:**

1. Properties same as ArrayList: insertion order, heterogeneous objects, duplicates, null, Serializable/Cloneable/RandomAccess
2. Difference 1: Concurrent modification during iteration — no CME on COWAL
3. Difference 2: Fail-safe vs fail-fast iterator
4. Difference 3: Iterator remove — allowed on ArrayList, **UnsupportedOperationException** on COWAL
5. Full 6-point summary for interviews and certification exam

**What comes next (Video 164):**

- CopyOnWriteArrayList constructors and new methods (`addIfAbsent`, `addAllAbsent`)

---

## 00:26 — Similarities: CopyOnWriteArrayList vs ArrayList

Sir states upfront:

> "Except creating separate cloned copy for every update operation, all the remaining properties of ArrayList and CopyOnWriteArrayList are exactly the same."

### Property-by-property comparison (same behavior)

| # | Property | ArrayList | CopyOnWriteArrayList |
|---|----------|-----------|----------------------|
| 1 | **Insertion order preserved** | Yes | Yes |
| 2 | **Heterogeneous objects allowed** | Yes | Yes |
| 3 | **Duplicate objects allowed** | Yes | Yes |
| 4 | **Null insertion possible** | Yes | Yes |
| 5 | **Interfaces implemented** | Serializable, Cloneable, RandomAccess | Serializable, Cloneable, RandomAccess |

Sir walks through each on the board:

> "In normal ArrayList insertion order is preserved — same in CopyOnWriteArrayList."

> "Heterogeneous objects are allowed — no problem at all."

> "Duplicate objects are allowed — yes."

> "Null insertion is possible — yes, happily you can insert null."

> "ArrayList implements Serializable, Cloneable, RandomAccess — these three interfaces also implemented by CopyOnWriteArrayList."

```java
import java.util.ArrayList;
import java.util.concurrent.CopyOnWriteArrayList;

public class SimilarPropertiesDemo {
    public static void main(String[] args) {
        CopyOnWriteArrayList<Object> cow = new CopyOnWriteArrayList<>();

        // Insertion order preserved
        cow.add("String");
        cow.add(100);
        cow.add(true);
        System.out.println(cow);
        // prints [String, 100, true]

        // Heterogeneous objects — OK
        // Duplicates — OK
        cow.add("String");
        System.out.println(cow);
        // prints [String, 100, true, String]

        // Null insertion — OK
        cow.add(null);
        System.out.println(cow);
        // prints [String, 100, true, String, null]

        // Same behavior as ArrayList for all above properties
        ArrayList<Object> al = new ArrayList<>();
        al.add("String"); al.add(100); al.add(null);
        System.out.println(al);
        // prints [String, 100, null]
    }
}
```

**Board conclusion:** For collection behavior (order, duplicates, null, interfaces), CopyOnWriteArrayList = ArrayList. The **only** behavioral difference comes from the concurrent copy-on-write mechanism.

---

## 02:22 — Difference 1: Concurrent modification during iteration

### Normal ArrayList behavior (fail-fast)

While one thread is performing **iteration**, if any other thread tries to **modify** the underlying list object → immediately **`ConcurrentModificationException`**.

This was covered in earlier concurrent collections videos (Video 154 — Reason 3 for needing concurrent collections).

### CopyOnWriteArrayList behavior (no CME)

While one thread is performing **iteration**, other threads **are allowed** to perform **update operations** — no problem at all. We **won't get** `ConcurrentModificationException`.

**Why?** Because update operation is performed on a **separate cloned copy** — there is no effect on the existing array that the iterating thread is reading.

Sir's exact words:

> "While one thread performing iteration, the other threads can perform update operation — there is no problem at all. We won't get any concurrent modification exception. That is the need of concurrent collections."

```java
import java.util.ArrayList;
import java.util.concurrent.CopyOnWriteArrayList;

public class CMEComparisonDemo {
    public static void main(String[] args) throws InterruptedException {
        CopyOnWriteArrayList<String> cow = new CopyOnWriteArrayList<>();
        cow.add("A"); cow.add("B"); cow.add("C");

        Thread iteratorThread = new Thread(() -> {
            for (String s : cow) {
                System.out.println("COWAL reading: " + s);
                try { Thread.sleep(50); } catch (InterruptedException e) {}
            }
        });

        Thread modifierThread = new Thread(() -> {
            cow.add("D"); // update on clone — no effect on iterator's snapshot
            System.out.println("COWAL modified — no CME");
        });

        iteratorThread.start();
        modifierThread.start();
        iteratorThread.join();
        modifierThread.join();
        // prints: COWAL reading: A, B, C (iterator may not see D — snapshot)
        //         COWAL modified — no CME
        // No ConcurrentModificationException

        // ArrayList — same scenario throws CME
        ArrayList<String> al = new ArrayList<>();
        al.add("A"); al.add("B");

        Thread it2 = new Thread(() -> {
            for (String s : al) {
                System.out.println("AL reading: " + s);
                try { Thread.sleep(50); } catch (InterruptedException e) {}
            }
        });
        Thread mod2 = new Thread(() -> al.add("C"));
        it2.start(); mod2.start();
        it2.join(); mod2.join();
        // CE: ConcurrentModificationException at runtime
    }
}
```

| | ArrayList | CopyOnWriteArrayList |
|---|-----------|----------------------|
| Iterate + concurrent modify | **CME** | **No CME** |
| Other threads during iteration | Not allowed to modify | Allowed to modify |
| Reason | In-place modification detected by iterator | Modification on separate clone |

**Interview one-liner:** ArrayList → iterate + modify → CME. CopyOnWriteArrayList → iterate + modify → no CME (update on clone).

---

## 05:03 — Difference 2: Iterator type — fail-fast vs fail-safe

| | ArrayList | CopyOnWriteArrayList |
|---|-----------|----------------------|
| **Iterator type** | **Fail-fast** | **Fail-safe** |
| **On concurrent modification** | Iterator fails immediately → CME | Iterator never fails → no CME |
| **Definition** | "Fails very fast" when underlying collection modified during iteration | "Never fails" — works on snapshot |

Sir's definitions (from prior lectures, repeated here):

**Fail-fast:** While iterating, if anyone modifies the underlying collection → iterator fails very fast → `ConcurrentModificationException`.

**Fail-safe:** Iterator never fails and never raises CME — even when other threads modify the collection concurrently.

```
ArrayList (fail-fast)                CopyOnWriteArrayList (fail-safe)
─────────────────────                ─────────────────────────────────
Iterator on live array               Iterator on snapshot (array copy at creation)
Concurrent modify detected           Concurrent modify on separate clone
→ CME immediately                    → Iterator unaffected
```

**Interview one-liner:** ArrayList iterator = fail-fast. CopyOnWriteArrayList iterator = fail-safe.

---

## 05:40 — Difference 3: Iterator remove operation — CRITICAL exam point

Sir marks this as **very very important** — may appear on the certification exam.

### Scenario (board walkthrough)

```java
Iterator it = list.iterator();
while (it.hasNext()) {
    Integer i = (Integer) it.next();
    if (i % 2 == 0) {
        it.remove(); // remove even numbers
    }
}
```

### ArrayList — remove via iterator is ALLOWED

Iterator of normal ArrayList **can perform remove operation** — no problem at all. The iterator's `remove()` modifies the underlying list in a controlled way (fail-fast checks modCount).

### CopyOnWriteArrayList — remove via iterator is NOT ALLOWED

Iterator of CopyOnWriteArrayList **cannot perform remove operation**.

**Why?** Remove is a write operation. If remove were performed on a separate cloned copy, at sync time there could be **inconsistency**. That is why the designers disabled iterator remove on COWAL.

> "Remove operation should be performed on separate clone copy or not — if remove operation performing on separate clone copy, at later point of time sync maybe inconsistency at sync level. That's why CopyOnWriteArrayList iterator can't perform remove operation."

**By mistake if you try:**

```java
RuntimeException: UnsupportedOperationException
```

Sir's exact words:

> "By mistake if you are trying to perform remove operation, then we will get runtime exception saying UnsupportedOperationException."

```java
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

public class IteratorRemoveDemo {
    public static void main(String[] args) {
        // ArrayList — iterator.remove() ALLOWED
        ArrayList<Integer> al = new ArrayList<>();
        al.add(1); al.add(2); al.add(3); al.add(4);

        Iterator<Integer> it1 = al.iterator();
        while (it1.hasNext()) {
            Integer i = it1.next();
            if (i % 2 == 0) {
                it1.remove(); // OK — removes from underlying ArrayList
            }
        }
        System.out.println(al); // prints [1, 3]

        // CopyOnWriteArrayList — iterator.remove() NOT ALLOWED
        CopyOnWriteArrayList<Integer> cow = new CopyOnWriteArrayList<>();
        cow.add(1); cow.add(2); cow.add(3); cow.add(4);

        Iterator<Integer> it2 = cow.iterator();
        while (it2.hasNext()) {
            Integer i = it2.next();
            if (i % 2 == 0) {
                // it2.remove(); // CE: UnsupportedOperationException at runtime
            }
        }
        // Use cow.remove(Integer.valueOf(2)) instead — that goes through copy-on-write path
        cow.remove(Integer.valueOf(2));
        System.out.println(cow); // prints [1, 3, 4]
    }
}
```

| Operation | ArrayList iterator | COWAL iterator |
|-----------|-------------------|----------------|
| `next()` (read) | Allowed | Allowed |
| `remove()` | **Allowed** | **UnsupportedOperationException** |
| Alternative for COWAL | N/A | Use `list.remove(object)` directly |

**Exam trap:** This is explicitly flagged by Sir as a certification exam point. Memorize: COWAL iterator = read only, no remove.

---

## 08:39 — Full 6-point summary (interview + exam)

Sir asks a student to summarize — this is the **complete answer** for "Tell me about CopyOnWriteArrayList":

### Point 1 — What is it?

> "CopyOnWriteArrayList is a concurrent collection. It is the thread-safe version of your list object."

### Point 2 — Why "CopyOnWrite"?

> "For every write operation, a separate cloned copy will be created. There is no effect on existing list object or any existing threads."

### Point 3 — Performance consideration

> "For every write operation, separate cloned copy will be created — there may be performance issues if more number of write operations. CopyOnWriteArrayList is the best choice if more reads, less writes."

### Point 4 — Same as ArrayList

> "Insertion order preserved, duplicate objects allowed, heterogeneous objects allowed, null insertion possible, Serializable/Cloneable/RandomAccess — all same as ArrayList."

### Point 5 — Concurrent modification (CME)

> "Normal ArrayList: while one thread iterating, other threads not allowed to modify → CME. CopyOnWriteArrayList: other threads can modify → no CME (modification on separate clone)."

### Point 6 — Iterator behavior

> "Normal ArrayList iterator = fail-fast. CopyOnWriteArrayList iterator = fail-safe. Normal iterator can perform read + remove. COWAL iterator can perform only read — remove throws UnsupportedOperationException."

---

## Master comparison table — ArrayList vs CopyOnWriteArrayList

| # | Property | ArrayList | CopyOnWriteArrayList |
|---|----------|-----------|----------------------|
| 1 | Thread-safe | No | Yes |
| 2 | Package | `java.util` | `java.util.concurrent` |
| 3 | Insertion order | Preserved | Preserved |
| 4 | Heterogeneous objects | Allowed | Allowed |
| 5 | Duplicates | Allowed | Allowed |
| 6 | Null insertion | Allowed | Allowed |
| 7 | Serializable, Cloneable, RandomAccess | Yes | Yes |
| 8 | Write mechanism | In-place | Clone + write on copy |
| 9 | CME during iteration + modify | Yes | Never |
| 10 | Iterator type | Fail-fast | Fail-safe |
| 11 | Iterator remove() | Allowed | UnsupportedOperationException |
| 12 | Best use case | General purpose | Read-heavy concurrent |
| 13 | Worst use case | Multi-threaded without sync | Write-heavy |

---

## Quick revision cards

| Question | Answer |
|----------|--------|
| COWAL preserves insertion order? | Yes |
| Duplicates allowed in COWAL? | Yes |
| Null allowed in COWAL? | Yes |
| COWAL implements RandomAccess? | Yes |
| CME on COWAL during iterate+modify? | Never |
| ArrayList iterator type? | Fail-fast |
| COWAL iterator type? | Fail-safe |
| COWAL iterator remove()? | UnsupportedOperationException |
| COWAL iterator read (next)? | Allowed |
| Why no CME on COWAL? | Write on separate clone |
| Why no iterator remove on COWAL? | Sync inconsistency risk |

---

## Exam traps

1. **Trap:** "CopyOnWriteArrayList does not allow null." → **Wrong.** Null insertion is allowed (same as ArrayList).
2. **Trap:** "CopyOnWriteArrayList iterator supports remove()." → **Wrong.** Throws `UnsupportedOperationException`.
3. **Trap:** "CopyOnWriteArrayList throws CME like ArrayList." → **Wrong.** Never throws CME.
4. **Trap:** "CopyOnWriteArrayList does not preserve insertion order." → **Wrong.** Order is preserved.
5. **Trap:** "Fail-safe means iterator sees live updates." → **Partially wrong.** Iterator works on snapshot at creation time; may not see concurrent adds until new iterator created.

---

## Certification exam focus (Sir's explicit warning)

Sir states at **08:30**:

> "Make sure maybe a chance to ask in our certification exam also this point."

**The exam point:** Iterator of CopyOnWriteArrayList **cannot** perform `remove()` → `UnsupportedOperationException`.

Memorize this alongside: COWAL iterator = fail-safe, read-only via iterator API.
