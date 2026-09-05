# Video 161 — Concurrent Collections Part-8: ConcurrentHashMap vs synchronizedMap() vs Hashtable

## Video info

| Field | Value |
|-------|-------|
| Position | 161 of 203 |
| Title | CoreJavaWithOCJP/SCJP:ConcurrentCollectionsPart-8\|\|ConcurrentHashMap\|\|synchronizedMap()\|\|Hashtable |
| Instructor | Durga Sir (OCJP/SCJP) |
| Duration | 7m 55s |
| Video ID | 4Q2udLDhMC8 |
| Watch URL | https://www.youtube.com/watch?v=4Q2udLDhMC8 |
| Playlist | Core Java With OCJP/SCJP |
| Notes source | YouTube auto-captions (yt-dlp + node PO token) |

> **ASR decode notes:** concurrent Ash map / concurrent Dash map = **ConcurrentHashMap**; synchronizer map / synr Ranger M = **Collections.synchronizedMap()**; as table / has table / hash table = **Hashtable**; threat / threats = **thread(s)**; fail first / fail F = **fail-fast**; fail safe = **fail-safe**; inter room = **interview room**; updation / WR operation = **write/update operation**; null such a type of story = **null is not allowed**; Legacy = **legacy class (Java 1.0)**.

## Session overview

This is a **pure comparison / interview-prep session** (~8 min). Sir consolidates everything already taught about thread-safe maps into one definitive three-way answer:

> **What is the difference between ConcurrentHashMap, Collections.synchronizedMap(), and Hashtable?**

All three are **thread-safe**, but the **mechanism and behavior** differ completely. Sir warns this is one of the most frequently asked concurrent-collections interview questions — you must explain *how* thread safety is achieved, not just say "all are thread-safe."

**Prerequisites (prior videos in this block):**

| Video | Topic |
|-------|-------|
| 154 | Need for concurrent collections |
| 155 | Traditional vs concurrent collections — differences |
| 157 | ConcurrentHashMap internal details — segment/bucket locking |
| 158–159 | ConcurrentHashMap demo programs |
| 160 | HashMap vs ConcurrentHashMap comparison |

**What this session covers:**

1. Why this three-way question matters in the interview room
2. Master comparison table — ConcurrentHashMap vs synchronizedMap vs Hashtable
3. Locking model — bucket/segment lock vs total-map lock
4. Concurrent access — multiple threads vs single thread at a time
5. Read vs write locking behavior
6. ConcurrentModificationException during iteration
7. Fail-fast vs fail-safe iterators
8. Null key/value rules
9. Version history (1.0 / 1.2 / 1.5)
10. Bonus: synchronizedMap vs Hashtable — only one difference

**What comes next (Sir's closing hint):**

- CopyOnWriteArrayList series (Videos 162–165+)
- HashMap vs ConcurrentHashMap vs Hashtable (already partially covered here)

---

## 00:19 — The interview question: All three are thread-safe — so where is the difference?

### Sir opens with a student question

> "Sir, there may be a chance of asking: What is the difference between ConcurrentHashMap, Hashtable, and synchronizedMap?"

### Why this question is important

All three are thread-safe:

| Class / API | Thread-safe? |
|-----------|--------------|
| `ConcurrentHashMap` | Yes |
| `Hashtable` | Yes |
| `Collections.synchronizedMap(map)` | Yes |

But **how** thread safety is achieved and **what behavior** you get are completely different. The interviewer wants **functional differences**, not naming.

### Sir's framing

> "ConcurrentHashMap performance is high — you know the reason: at a time multiple threads are allowed to operate simultaneously on ConcurrentHashMap. ConcurrentHashMap never throws ConcurrentModificationException. But Hashtable and synchronizedMap — through them we will get ConcurrentModificationException."

**Wrong answer:** "All three are thread-safe — no difference."

**Right answer:** Compare locking granularity, concurrent access, CME, iterators, null rules, and version.

---

## 01:23 — Master comparison table (board form)

Sir draws a three-column table on the board. This is the **central deliverable** of the lecture.

### Difference 1 — Thread safety mechanism (locking model)

| | ConcurrentHashMap | synchronizedMap / Hashtable |
|---|-------------------|----------------------------|
| **How thread safety is achieved** | Thread safety **without locking the total map object** | Thread safety **by locking the total map object** |
| **Lock granularity** | **Bucket-level lock** (sometimes called **segment lock**) | **Entire map object lock** — one lock for the whole map |
| **Thread waiting** | Thread needs lock on **one bucket/segment only**, not the whole map | Thread must acquire lock on **entire map** before any operation |

```java
import java.util.*;
import java.util.concurrent.*;

public class LockingModelDemo {
    public static void main(String[] args) {
        // ConcurrentHashMap — bucket/segment-level locking internally
        ConcurrentMap<Integer, String> chm = new ConcurrentHashMap<>();
        // Multiple threads can operate on DIFFERENT buckets simultaneously

        // synchronizedMap — total map object lock
        Map<Integer, String> syncMap =
            Collections.synchronizedMap(new HashMap<>());
        // Every operation locks the ENTIRE map wrapper

        // Hashtable — total map object lock (legacy)
        Hashtable<Integer, String> ht = new Hashtable<>();
        // Every operation locks the ENTIRE Hashtable object
    }
}
```

**Board conclusion:**

- **ConcurrentHashMap:** Thread requires only **bucket-level lock** (or segment lock), **not** total map object lock.
- **synchronizedMap / Hashtable:** Thread **compulsorily** requires **total map object lock**.

**Interview one-liner:** ConcurrentHashMap → bucket/segment lock. synchronizedMap & Hashtable → total map object lock.

---

## 02:38 — Difference 2 — How many threads can operate simultaneously?

| | ConcurrentHashMap | synchronizedMap / Hashtable |
|---|-------------------|----------------------------|
| **Concurrent threads** | **Multiple threads** allowed to operate on the map simultaneously (in a safe manner) | **Only one thread** allowed at a time — even for **read operations** |
| **Read + read** | Multiple reads can happen concurrently (no lock for reads in CHM) | Second read must wait for first operation to finish |
| **Read + write** | Reads proceed without lock; writes use bucket lock | Any operation blocks all others |

```java
import java.util.*;
import java.util.concurrent.*;

public class ConcurrentAccessDemo {
    public static void main(String[] args) throws InterruptedException {
        ConcurrentHashMap<String, Integer> chm = new ConcurrentHashMap<>();
        chm.put("A", 1);

        // Thread-1: read
        Thread t1 = new Thread(() -> System.out.println(chm.get("A")));
        // Thread-2: read — allowed simultaneously on CHM
        Thread t2 = new Thread(() -> System.out.println(chm.get("A")));
        // Thread-3: write — allowed on different bucket
        Thread t3 = new Thread(() -> chm.put("B", 2));

        t1.start(); t2.start(); t3.start();
        t1.join(); t2.join(); t3.join();
        // prints: 1, 1 (order may vary) — no blocking between concurrent reads/writes on CHM

        Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
        syncMap.put("A", 1);
        // On synchronizedMap: at a time ONLY ONE thread can perform ANY operation
        // Even two read threads cannot run truly in parallel
    }
}
```

**Board conclusion:**

- **ConcurrentHashMap:** Multiple threads allowed — no problem at all.
- **synchronizedMap / Hashtable:** At a time **only one** thread is allowed to perform **any** operation on the map object — **even read operation**.

**Interview one-liner:** CHM → multiple threads simultaneously. synchronizedMap/Hashtable → one thread at a time.

---

## 03:16 — Difference 3 — Read operations: with or without lock?

| | ConcurrentHashMap | synchronizedMap / Hashtable |
|---|-------------------|----------------------------|
| **Read operation (get, containsKey, etc.)** | Can be performed **without lock** | **Total map object lock must be required** |
| **Write operation (put, remove, etc.)** | Performed with **bucket-level lock** | **Total map object lock must be required** |

Sir's exact wording:

> "Read operation can be performed without lock. But write operation can be performed with bucket-level lock."

And for the other two:

> "Any operation — whether it is read operation or write operation — compulsory total map object lock must be required."

```java
import java.util.*;
import java.util.concurrent.*;

public class ReadWriteLockDemo {
    public static void main(String[] args) {
        ConcurrentHashMap<Integer, String> chm = new ConcurrentHashMap<>();
        chm.put(1, "One");

        // READ — no lock required internally (any number of concurrent reads)
        String v = chm.get(1); // prints One

        // WRITE — bucket-level lock internally
        chm.put(2, "Two");

        Map<Integer, String> syncMap = Collections.synchronizedMap(new HashMap<>());
        syncMap.put(1, "One");
        // BOTH read and write acquire synchronized(syncMap) — total object lock
        synchronized (syncMap) { // recommended idiom for iteration too
            String sv = syncMap.get(1);
        }
    }
}
```

**Interview one-liner:** CHM reads → no lock. CHM writes → bucket lock. synchronizedMap/Hashtable → every read AND write → total map lock.

---

## 04:05 — Difference 4 — ConcurrentModificationException during iteration

| | ConcurrentHashMap | synchronizedMap / Hashtable |
|---|-------------------|----------------------------|
| **While one thread iterates, can other threads modify?** | **Yes** — allowed to modify map in safe manner | **No** — other threads must not modify |
| **ConcurrentModificationException** | **Never** throws CME | **Will get** CME if modified during iteration |

Sir's board wording:

> "While one thread iterating map object, the other threads are allowed to modify map in safe manner and we won't get any concurrent modification exception."

vs

> "While one thread iterating map object, the other threads are not allowed to modify map otherwise we will get concurrent modification exception."

```java
import java.util.*;
import java.util.concurrent.*;

public class CMEDuringIterationDemo {
    public static void main(String[] args) throws InterruptedException {
        ConcurrentHashMap<Integer, String> chm = new ConcurrentHashMap<>();
        chm.put(1, "A"); chm.put(2, "B");

        Thread iteratorThread = new Thread(() -> {
            for (Integer key : chm.keySet()) {
                System.out.println(key + " -> " + chm.get(key));
            }
        });

        Thread modifierThread = new Thread(() -> chm.put(3, "C"));

        iteratorThread.start();
        modifierThread.start();
        iteratorThread.join();
        modifierThread.join();
        // No ConcurrentModificationException on CHM

        Map<Integer, String> syncMap = Collections.synchronizedMap(new HashMap<>());
        syncMap.put(1, "A"); syncMap.put(2, "B");

        Thread it2 = new Thread(() -> {
            synchronized (syncMap) {
                for (Integer key : syncMap.keySet()) {
                    // If another thread modifies WITHOUT external sync → CME
                    System.out.println(key);
                }
            }
        });
        // CE: Demonstrating CME requires unsynchronized concurrent modify during iteration
    }
}
```

**Interview one-liner:** CHM → iterate + modify concurrently → no CME. synchronizedMap/Hashtable → modify during iteration → CME.

---

## 04:54 — Difference 5 — Iterator type: fail-safe vs fail-fast

| | ConcurrentHashMap | synchronizedMap / Hashtable |
|---|-------------------|----------------------------|
| **Iterator type** | **Fail-safe** | **Fail-fast** |
| **Behavior** | Iterator **never fails**; never raises CME | While iterator iterating, if any modification → iterator **fails immediately** with CME |
| **Why** | Concurrent collections designed for safe concurrent access | Wrappers/legacy classes use fail-fast iterators from underlying collection |

**Fail-fast definition (Sir):**

> "While iterator iterating, if you are performing any modification, immediately iterator fails by raising ConcurrentModificationException. That's why iterator is fail-fast."

**Fail-safe definition (Sir):**

> "My iterator never fails and my iterator never raises ConcurrentModificationException. That's why it is fail-safe."

```
ConcurrentHashMap                    synchronizedMap / Hashtable
─────────────────                    ─────────────────────────────
Thread-1: iterating...               Thread-1: iterating...
Thread-2: put/remove (safe)          Thread-2: put/remove
        ↓                                    ↓
Iterator does NOT fail                 Iterator FAILS immediately
No CME                                 ConcurrentModificationException
(fail-safe)                            (fail-fast)
```

**Interview one-liner:** CHM iterator = fail-safe. synchronizedMap & Hashtable iterator = fail-fast.

---

## 05:25 — Difference 6 — Null key and null value

| | ConcurrentHashMap | synchronizedMap | Hashtable |
|---|-------------------|-----------------|-----------|
| **Null key** | **NOT allowed** → NullPointerException | **Allowed** (inherited from HashMap) | **NOT allowed** |
| **Null value** | **NOT allowed** → NullPointerException | **Allowed** (inherited from HashMap) | **NOT allowed** |

Sir's wording:

> "Null is not allowed for both key and values — such a type of story not applicable for ConcurrentHashMap."

> "Null is allowed for both key and values if it is synchronizedMap — because we will get from HashMap related terminology."

> "Null is not allowed — even in Hashtable also."

```java
import java.util.*;
import java.util.concurrent.*;

public class NullRulesDemo {
    public static void main(String[] args) {
        // ConcurrentHashMap — null NOT allowed
        ConcurrentHashMap<String, String> chm = new ConcurrentHashMap<>();
        // chm.put(null, "value");   // CE: NullPointerException
        // chm.put("key", null);     // CE: NullPointerException

        // synchronizedMap (wrapping HashMap) — null allowed
        Map<String, String> syncMap = Collections.synchronizedMap(new HashMap<>());
        syncMap.put(null, "value");  // OK
        syncMap.put("key", null);    // OK

        // Hashtable — null NOT allowed
        Hashtable<String, String> ht = new Hashtable<>();
        // ht.put(null, "value");    // CE: NullPointerException
        // ht.put("key", null);      // CE: NullPointerException
    }
}
```

**Interview one-liner:** CHM → no null key/value. synchronizedMap → null allowed (HashMap behavior). Hashtable → no null key/value.

---

## 05:57 — Difference 7 — Version introduced

| | ConcurrentHashMap | synchronizedMap | Hashtable |
|---|-------------------|-----------------|-----------|
| **Java version** | **1.5** | **1.2** | **1.0** |
| **Category** | Concurrent collection (`java.util.concurrent`) | Collections utility wrapper (`java.util.Collections`) | **Legacy class** (original Java API) |
| **Package** | `java.util.concurrent` | `java.util` | `java.util` |

Sir's exact words:

> "ConcurrentHashMap came in 1.5 version. synchronizedMap concept came in 1.2. Hashtable concept came in 1.0 — it is the legacy class."

---

## 06:25 — Bonus: synchronizedMap vs Hashtable — only ONE difference

Sir groups synchronizedMap and Hashtable into **one category** because almost all properties are identical:

```
Category 1: synchronizedMap + Hashtable  (total map lock, fail-fast, CME, one thread at a time)
Category 2: ConcurrentHashMap            (bucket lock, fail-safe, no CME, multiple threads)
```

**The ONLY difference between synchronizedMap and Hashtable:**

| Property | synchronizedMap | Hashtable |
|----------|-----------------|-----------|
| Null key / null value | **Allowed** | **NOT allowed** |
| Everything else | Same | Same |

Sir's exact words:

> "In synchronizedMap null is allowed for both key and values. But in Hashtable null is not allowed for both key and values. Except this difference, all the remaining properties are always the same."

```java
import java.util.*;

public class SyncMapVsHashtableDemo {
    public static void main(String[] args) {
        Map<String, String> syncMap = Collections.synchronizedMap(new HashMap<>());
        syncMap.put(null, "nullKeyOK");     // OK — only difference from Hashtable
        syncMap.put("k", null);             // OK

        Hashtable<String, String> ht = new Hashtable<>();
        // ht.put(null, "x");  // CE: NullPointerException
        // ht.put("k", null);  // CE: NullPointerException

        // All other behavior identical:
        // - total map object lock
        // - one thread at a time
        // - fail-fast iterator
        // - CME if modified during iteration
    }
}
```

---

## 07:02 — Interview answer template

### Full three-way comparison (one glance)

| # | Property | ConcurrentHashMap | synchronizedMap | Hashtable |
|---|----------|-------------------|-----------------|-----------|
| 1 | Thread-safe | Yes | Yes | Yes |
| 2 | Locking model | Bucket/segment level | Total map object | Total map object |
| 3 | Threads at a time | Multiple (safe) | Only one | Only one |
| 4 | Read without lock | Yes | No — total lock | No — total lock |
| 5 | Write lock | Bucket-level | Total map | Total map |
| 6 | CME during iteration | Never | Yes | Yes |
| 7 | Iterator | Fail-safe | Fail-fast | Fail-fast |
| 8 | Null key | Not allowed | Allowed | Not allowed |
| 9 | Null value | Not allowed | Allowed | Not allowed |
| 10 | Performance | Highest (among thread-safe maps) | Lowest (total lock) | Lowest (total lock) |
| 11 | Version | Java 1.5 | Java 1.2 | Java 1.0 (legacy) |
| 12 | Package | `java.util.concurrent` | `java.util` | `java.util` |

### Interview one-liner (Sir's closing)

> "All three are thread-safe. ConcurrentHashMap gives thread safety via bucket-level locking — multiple threads can operate simultaneously, reads need no lock, never throws CME, fail-safe iterator, no null. synchronizedMap and Hashtable lock the entire map — one thread at a time, every operation needs total lock, CME on concurrent modification, fail-fast iterator. Between synchronizedMap and Hashtable, the only difference is null: allowed in synchronizedMap, not in Hashtable."

### Related interview questions (Sir's hints at end)

| Question | Where answered |
|----------|----------------|
| HashMap vs ConcurrentHashMap | Video 160 |
| ConcurrentHashMap vs synchronizedMap vs Hashtable | **This video (161)** |
| HashMap vs ConcurrentHashMap vs Hashtable | Combine Videos 160 + 161 |

---

## Quick revision cards

| Question | Answer |
|----------|--------|
| Are all three thread-safe? | Yes |
| Which allows multiple concurrent threads? | ConcurrentHashMap only |
| Which locks entire map? | synchronizedMap, Hashtable |
| CHM read needs lock? | No |
| CHM write needs lock? | Bucket-level |
| CME on CHM? | Never |
| CME on synchronizedMap/Hashtable? | Yes (if modified during iteration) |
| CHM iterator type? | Fail-safe |
| synchronizedMap/Hashtable iterator? | Fail-fast |
| Null in CHM? | Not allowed |
| Null in synchronizedMap? | Allowed |
| Null in Hashtable? | Not allowed |
| CHM version? | 1.5 |
| synchronizedMap version? | 1.2 |
| Hashtable version? | 1.0 (legacy) |
| Only diff between syncMap & Hashtable? | Null allowed in syncMap, not in Hashtable |

---

## Exam traps

1. **Trap:** "All three are thread-safe, so they behave the same." → **Wrong.** Locking granularity and CME behavior differ completely.
2. **Trap:** "Hashtable allows null like HashMap." → **Wrong.** Hashtable rejects null keys and values.
3. **Trap:** "synchronizedMap is in java.util.concurrent." → **Wrong.** It is `Collections.synchronizedMap()` in `java.util`.
4. **Trap:** "ConcurrentHashMap allows null for values only." → **Wrong.** Neither null key nor null value is allowed.
5. **Trap:** "Multiple threads can read synchronizedMap concurrently." → **Wrong.** Only one thread at a time for ANY operation.

---

## When to use which (practical guide)

| Scenario | Recommended |
|----------|-------------|
| High-concurrency multi-threaded app, frequent reads + updates | **ConcurrentHashMap** |
| Legacy code using Hashtable API | Migrate to **ConcurrentHashMap** (modern) |
| Need thread-safe HashMap with null keys/values | **Collections.synchronizedMap(new HashMap<>())** |
| Single-threaded app | Plain **HashMap** (no thread-safe wrapper needed) |
| Exam: "best performance among thread-safe maps" | **ConcurrentHashMap** |
