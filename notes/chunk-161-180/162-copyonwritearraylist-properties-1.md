# Video 162 — Concurrent Collections Part-9: CopyOnWriteArrayList Properties Part-1

## Video info

| Field | Value |
|-------|-------|
| Position | 162 of 203 |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-9 \|\| CopyOnWriteArrayList Properties Part-1 |
| Instructor | Durga Sir (OCJP/SCJP) |
| Duration | 8m 44s |
| Video ID | plEY1GXYGrI |
| Watch URL | https://www.youtube.com/watch?v=plEY1GXYGrI |
| Playlist | Core Java With OCJP/SCJP |
| Notes source | YouTube auto-captions (yt-dlp + node PO token) |

> **ASR decode notes:** copy on write a list / copy on writer list / copy on var list / copy on vital list = **CopyOnWriteArrayList**; co a l / C A L = **CopyOnWriteArrayList (COWAL)**; entropies = **interfaces**; threats = **threads**; right operation / VAR operation / write operation = **write/update operation**; Le operations = **read operations**; clean copy / cloned copy = **cloned copy of the internal array**.

## Session overview

This lecture begins Durga Sir's **CopyOnWriteArrayList** module — the second major concurrent collection after ConcurrentHashMap. Part-1 covers **what it is** and **why it is named "CopyOnWrite"** — the core copy-on-write mechanism that provides thread safety.

**Prerequisites (prior videos):**

| Video | Topic |
|-------|-------|
| 154 | Need for concurrent collections |
| 155 | Traditional vs concurrent collections |
| 157–161 | ConcurrentHashMap series (completed) |

**What this session covers:**

1. CopyOnWriteArrayList — thread-safe version of List
2. Place in Java API hierarchy (Collection → List → CopyOnWriteArrayList)
3. Package: `java.util.concurrent`
4. Why the name "CopyOnWrite" — copy-on-write mechanism explained
5. Read operations on existing object; write operations on cloned copy
6. JVM automatically syncs the two versions
7. Performance trade-off — overhead of creating copies
8. When to use: many reads, few writes (best choice)
9. When NOT to use: many writes (worst choice)

**What continues in Part-2 (Video 163):**

- Similarities with ArrayList (insertion order, duplicates, null, interfaces)
- Differences: CME, fail-safe iterator, iterator remove restriction

---

## 00:28 — Transition from ConcurrentHashMap to CopyOnWriteArrayList

### Recap of prior concurrent collections work

Sir recaps what was already covered:

- What are concurrent collections?
- Why do we need concurrent collections?
- ConcurrentHashMap — differences from HashMap, Hashtable, synchronizedMap (Videos 157–161)

### Next concurrent collection

> "Now I have to talk about next concurrent collections. What is that? Next concurrent collection is **CopyOnWriteArrayList**."

The name itself indicates it is related to a **List**. It is:

- The **thread-safe version** of your list
- The **concurrent version** of your list

---

## 01:40 — Point 1: CopyOnWriteArrayList is the thread-safe version of List

### API hierarchy (board diagram)

```
java.util
  └── Collection (interface)
        └── List (interface)
              └── ArrayList (implementation — NOT thread-safe)

java.util.concurrent
  └── CopyOnWriteArrayList (implementation of List — thread-safe)
```

Sir's hierarchy on the board:

```
Collection (interface)          ← java.util package
    │
    └── List (interface)
            │
            └── CopyOnWriteArrayList (implementation class)
                                    ← java.util.concurrent package
```

**Key facts:**

| Fact | Detail |
|------|--------|
| Interface implemented | `List` (child of `Collection`) |
| Package | `java.util.concurrent` (NOT `java.util`) |
| Category | Concurrent collection |
| Purpose | Thread-safe version of list |

```java
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

public class COWALIntroDemo {
    public static void main(String[] args) {
        // Thread-safe list — concurrent collection
        List<String> list = new CopyOnWriteArrayList<>();
        list.add("A");
        list.add("B");
        System.out.println(list); // prints [A, B]
    }
}
```

**Interview one-liner:** CopyOnWriteArrayList is the thread-safe, concurrent version of List, in `java.util.concurrent`.

---

## 02:15 — Point 2: Why the name "CopyOnWrite"?

### The central question

> "Immediately you may ask: Why the word CopyOnWriteArrayList?"

### How thread safety is achieved — copy-on-write mechanism

Sir draws on the board:

```
CopyOnWriteArrayList object (existing)
        │
        ├── Thread T1 ──→ READ operation  ──→ operates on EXISTING object
        ├── Thread T2 ──→ READ operation  ──→ operates on EXISTING object
        ├── Thread T3 ──→ WRITE operation ──→ operates on CLONED COPY
        └── Thread Tn ──→ WRITE/UPDATE    ──→ operates on CLONED COPY
```

### Step-by-step mechanism

1. **Read operation:** Performed on the **existing object** — no effect, no copy needed. Any number of read threads can access the current array simultaneously.

2. **Write/update operation:** For **every write operation**, a **separate cloned copy** of the internal array is created. The update is performed on that clone — **not** on the array that readers are currently using.

3. **Synchronization:** At a later point, the JVM **automatically syncs** the two versions internally. Readers continue on the old snapshot until the swap happens.

Sir's exact words:

> "For every write operation, a separate cloned copy will be created. On that cloned copy, update operation will be performed — so that there is no effect for the threads which are performing read operation on that object."

> "Later point of time, these two objects will be synced by the JVM automatically internally."

```java
import java.util.concurrent.CopyOnWriteArrayList;

public class CopyOnWriteMechanismDemo {
    public static void main(String[] args) throws InterruptedException {
        CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
        list.add("Original");

        // READ thread — operates on existing internal array (no copy)
        Thread reader = new Thread(() -> {
            for (String s : list) {
                System.out.println("Reading: " + s);
            }
        });

        // WRITE thread — creates cloned copy, writes on clone, JVM swaps later
        Thread writer = new Thread(() -> {
            list.add("AddedByWriter");
            System.out.println("Write complete on clone");
        });

        reader.start();
        writer.start();
        reader.join();
        writer.join();

        System.out.println(list); // prints [Original, AddedByWriter]
    }
}
```

### Visual model (board)

```
Time ──────────────────────────────────────────────────────────►

Internal array:  [A, B, C]          ← readers see this
                      │
                 write(put D)
                      │
                 clone created: [A, B, C]  (copy)
                      │
                 modify clone:   [A, B, C, D]
                      │
                 JVM swap ──►   [A, B, C, D]  ← new "existing" for future reads
```

**Why thread safety?** Readers never see a partially modified array. Writers never interfere with active readers because they work on a separate copy.

**Interview one-liner:** CopyOnWrite = for every write, clone the array, write on clone, JVM swaps atomically. Reads use existing snapshot — no lock, no interference.

---

## 04:49 — Thread safety summary

Sir consolidates the two points students must remember by end of Part-1:

### Point 1 — What is CopyOnWriteArrayList?

> "CopyOnWriteArrayList is a thread-safe version of your list object. It is a concurrent collection."

### Point 2 — How thread safety is achieved (why "CopyOnWrite")?

> "For every write operation, a separate cloned copy will be created. On that cloned copy, update operation will be performed. Later, these two objects will be synced by the JVM automatically internally."

### Sir's interview answer template

> "Sir, I have one list object. If any thread tries to modify, that modification is done on a separate cloned copy — so for the threads which are accessing the existing ArrayList object, there is no effect at all. That is how we get thread safety."

---

## 07:01 — Performance trade-off: When to use CopyOnWriteArrayList

### The performance problem

Sir raises the obvious question:

> "For every update operation, a separate copy is going to be created. Suppose I am performing thousand update operations — how many copies are required? 1,000 copies — which is a big performance overhead."

### Decision rule (board)

| Scenario | Recommendation |
|----------|----------------|
| **More reads, fewer writes** | CopyOnWriteArrayList is **recommended** / **best choice** |
| **More writes, fewer reads** | CopyOnWriteArrayList is the **worst choice** — performance overhead |

Sir's exact words:

> "If more number of read operations are there, less number of write operations are there, then CopyOnWriteArrayList is recommended to use."

> "If more number of write operations are there, CopyOnWriteArrayList is the worst choice because there may be a chance of performance overhead."

```java
import java.util.concurrent.CopyOnWriteArrayList;

public class WhenToUseCOWALDemo {
    public static void main(String[] args) {
        // GOOD use case: event listener list, configuration cache
        // Many threads READ the list constantly; writes are rare
        CopyOnWriteArrayList<String> listeners = new CopyOnWriteArrayList<>();
        listeners.add("Listener1");
        listeners.add("Listener2");
        // 1000 threads reading → fast, no copies created
        // 1 thread occasionally adding listener → one copy, acceptable

        // BAD use case: frequently updated shared work queue
        // CopyOnWriteArrayList queue = new CopyOnWriteArrayList<>();
        // 1000 add/remove operations → 1000 array clones → huge overhead
        // Use ConcurrentLinkedQueue or blocking queue instead
    }
}
```

### Real-world examples where COWAL shines

| Use case | Why COWAL fits |
|----------|----------------|
| **Event listener lists** (Swing, servlet context listeners) | Listeners added/removed rarely; iterated frequently |
| **Configuration/settings snapshots** | Config read by many threads; updated occasionally |
| **Observer pattern** | Observers notified (read) constantly; registration changes are rare |
| **Read-heavy caches** | Cache hit = read; cache invalidation = rare write |

### Real-world examples where COWAL is wrong

| Use case | Why COWAL fails |
|----------|-----------------|
| **Work queues** with frequent add/remove | Every add = full array clone |
| **Logging buffers** with constant appends | Write-heavy → constant cloning |
| **Real-time data feeds** with streaming updates | Write ratio too high |

---

## 07:45 — Part-1 summary (two points to remember)

Sir closes Part-1 with exactly two takeaways:

| # | Point |
|---|-------|
| 1 | **CopyOnWriteArrayList** = thread-safe version of List; concurrent collection in `java.util.concurrent` |
| 2 | **Copy-on-write mechanism** = every write creates a cloned copy; reads use existing object; JVM syncs automatically |
| 3 | **Best when:** many reads, few writes |
| 4 | **Worst when:** many writes (performance overhead from cloning) |

**What comes in Part-2 (Video 163):** Similarities with ArrayList + concurrent-specific differences (CME, fail-safe, iterator remove).

---

## Quick revision cards

| Question | Answer |
|----------|--------|
| What is CopyOnWriteArrayList? | Thread-safe concurrent version of List |
| Package? | `java.util.concurrent` |
| Interface? | Implements `List` |
| Why "CopyOnWrite"? | Every write → clone array → write on clone → JVM swap |
| Read operation? | On existing object — no copy |
| Write operation? | On separate cloned copy |
| Who syncs the versions? | JVM automatically |
| Best use case? | Many reads, few writes |
| Worst use case? | Many writes |
| 1000 writes = ? copies | 1000 cloned copies (overhead) |

---

## Exam traps

1. **Trap:** "CopyOnWriteArrayList is in java.util." → **Wrong.** It is in `java.util.concurrent`.
2. **Trap:** "CopyOnWriteArrayList uses locking like Vector." → **Wrong.** It uses copy-on-write — no explicit lock on reads.
3. **Trap:** "CopyOnWriteArrayList is good for write-heavy workloads." → **Wrong.** Worst choice for write-heavy; best for read-heavy.
4. **Trap:** "Reads also create a copy." → **Wrong.** Only writes create a copy; reads operate on existing snapshot.
5. **Trap:** "CopyOnWriteArrayList implements a new interface." → **Wrong.** It implements existing `List` interface.

---

## Comparison preview (expanded in Video 163)

| Property | ArrayList | CopyOnWriteArrayList |
|----------|-----------|----------------------|
| Thread-safe | No | Yes |
| Package | `java.util` | `java.util.concurrent` |
| Write mechanism | In-place modify | Clone + write on copy |
| Read during write | Unsafe / CME | Safe — reads on old snapshot |
| Best for | General single-threaded use | Read-heavy concurrent use |
