# Video 155 — Concurrent Collections Part-2: Diff Between Traditional & Concurrent Collections

## Video info

ASR decode notes: threats = threads; multi Ed = multi-threaded; lcks = lakhs; concurrent H / concurrent Ash map = ConcurrentHashMap; copy on WR / copy on VAR = CopyOnWrite; interent = interview.

## Session overview

This is a short bridge lecture (~7 minutes) between Part-1 (need for concurrent collections) and the deep-dive series on individual concurrent classes (Videos 156–159+).

Prerequisite from previous session (Part-1 recap): Sir already explained why concurrent collections exist — three major problems with traditional (normal) collections. Video 155 does not re-derive those problems in full; it assumes you remember them and immediately maps each problem to how concurrent collections solve it.

What this session covers:

- Quick recap — three problems of traditional collections
- Problem 1 → Thread safety: traditional = mostly not thread-safe; concurrent = always thread-safe
- Problem 2 → Performance: legacy thread-safe classes (Vector, Hashtable) lock the entire collection; concurrent collections use segment/bucket-level locking → relatively higher performance
- Problem 3 → ConcurrentModificationException: traditional iterators fail when another thread modifies during iteration; concurrent collections allow safe concurrent modification and never throw CME
- Scalable multi-threaded applications — when to choose concurrent collections (lakhs of threads)
- Interview-style summary — "Explain differences between normal and concurrent collections"
- Roadmap — three most important concurrent collection classes to study next:
- ConcurrentHashMap
- CopyOnWriteArrayList
- CopyOnWriteArraySet
What this session does NOT cover (deferred):

- Internal locking mechanism details (segment locking) → next videos
- Why the name CopyOnWrite instead of ConcurrentList → explained when covering CopyOnWriteArrayList
- ConcurrentMap interface methods → Video 156
- Programs and HashMap vs ConcurrentHashMap table → Videos 157–160
## 00:19 — Recap: Why concurrent collections? (from Part-1)

### Board context

Sir opens by referencing the previous video where the need for concurrent collections was established.

### Three major problems with traditional collections

### Sir's conclusion from Part-1

To overcome these problems, we should go for concurrent collections.

Video 155 now answers: "Okay — for each problem, exactly how do concurrent collections differ from traditional ones?"

## 00:55 — Problem 1: Thread safety

### Traditional collections

Board question: What is the first problem with traditional collection objects?

Answer (classroom): Most of the traditional collections are not thread-safe.

Examples (from prior collections lectures in this course):

Key exam point: "Most" — not "all". Legacy classes Vector and Hashtable are synchronized, but they suffer from Problem 2 (performance).

### Concurrent collections

Board statement (copy exactly):

Every concurrent collection is always thread-safe.

Sir's wording:

- If you consider every concurrent collection → it is always thread-safe
- First problem is by default resolved — all concurrent collections are always thread-safe
### Difference #1 (summary row)

## 01:38 — Problem 2: Performance of thread-safe collections

### Traditional thread-safe approach — total lock

Even though some thread-safe collections exist (Vector, Hashtable):

Board note:

Performance-wise not up to the mark — because for any operation, the total collection object will be locked by only one thread.

Mechanism:

- Entire collection gets one lock (synchronized methods on the whole object)
- Thread A doing vector.add() holds lock → Thread B cannot do anything on that Vector until A releases
- Under heavy multi-threaded load → threads wait → performance is low
### Concurrent collections — different locking mechanism

Board note:

Performance-wise, relatively performance is high (compared to traditional thread-safe collections).

Why:

- Instead of locking the total collection, concurrent collections use a different locking mechanism
- A thread gets a lock on a particular block or particular segment — not the whole structure
- This is called:
- Segment locking, or
- Bucket-level locking
Sir explicitly defers detail:

In the next videos I will explain in detail — not required to worry now.

(Later videos cover ConcurrentHashMap's segment/bucket model — default 16 segments, etc.)

### Difference #2 (summary row)

### Illustrative analogy (for notes)

Think of a library:

- Vector/Hashtable model: Only one person allowed inside the entire library at a time — even if they only want one shelf
- Concurrent collection model: Different people can use different sections/rooms simultaneously — less waiting
## 02:53 — Problem 3: ConcurrentModificationException

### Traditional collections — strict iteration rule

Scenario:

- Thread-1 is iterating over a collection (via Iterator / enhanced for-loop)
- Thread-2 tries to modify the underlying collection (add / remove / structural change)
Result:

- ConcurrentModificationException at runtime
- This is the biggest headache with traditional collections in multi-threaded code
Why (conceptual — from Iterator fail-fast design):

- Iterator tracks modCount (modification count) of the collection
- If collection is structurally modified outside Iterator's own remove(), Iterator detects mismatch → throws CME
- Design intent: fail-fast — detect concurrent unsynchronized modification early
```java
import java.util.*;

public class TraditionalCME_Demo {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("A");
        list.add("B");
        list.add("C");

        Iterator<String> it = list.iterator();
        System.out.println(it.next()); // "A"

        // Structural modification NOT via iterator.remove()
        list.add("D");  // modCount changed

        System.out.println(it.next()); // ConcurrentModificationException
    }
}
```

### Concurrent collections — safe concurrent modification

Board statement (copy exactly):

While one thread is iterating the collection, the remaining threads are allowed to modify the underlying collection in a safe manner.

And:

Concurrent collections never throw ConcurrentModificationException.

**Difference #3 (summary row):

Important nuance (for exam depth):

- "Never CME" applies to concurrent collection implementations designed for this (e.g. ConcurrentHashMap, CopyOnWriteArrayList)
- Fail-fast vs fail-safe iterators (covered in Video 160): HashMap iterator = fail-fast; ConcurrentHashMap iterator = fail-safe
## 03:48 — Master comparison: Traditional vs Concurrent

### Sir's synthesis

Whatever problems are there in traditional collections, we can overcome by using concurrent collections.

### Full comparison table (exam-ready)

## 03:56 — Scalable multi-threaded applications

### When traditional collections fail

Sir's scenario:

In my application lakhs of threads I'm going to use — thousands of threads — in such areas traditional collections are not going to work. Compulsory we should go for concurrent collections.

Board conclusion:

Concurrent collections are best suitable for scalable multi-threaded applications.

### Decision guide

Interview one-liner:

Normal collections for normal apps; concurrent collections when the app is multi-threaded and scalable (many threads operating on shared data structures).

## 04:14 — Interview question: Explain the differences

### Question format

Sir frames this as a likely interview / exam room question:

Normal collection vs concurrent collection — can you please explain the differences?

He says students should already be in a position to answer after this lecture.

### Model answer (structured — 3 problems → 3 solutions)

1. Thread safety

- Traditional: most collection classes (ArrayList, HashMap, HashSet, …) are not thread-safe
- Concurrent: every concurrent collection class is always thread-safe
2. Performance

- Traditional thread-safe: Vector, Hashtable synchronize the entire object → one thread at a time → low performance
- Concurrent: use segment locking / bucket-level locking → multiple threads can proceed on different parts → relatively high performance
3. ConcurrentModificationException

- Traditional: while one thread iterates, others cannot safely modify → CME
- Concurrent: other threads can modify safely during iteration → no CME
Closing line:

Concurrent collections are the right choice for scalable multi-threaded applications where traditional collections fail.

## 04:25 — Roadmap: Important concurrent collection classes

### Sir's next target

Total — what are various concurrent collections? What are various important concurrent collection classes?

He narrows the syllabus to three classes for the first level of study:

Sir on board: "These three things we are going to discuss in detail."

### Interview warm-up question

What are various concurrent collections you are aware of? Can you please explain?

Immediate answer Sir expects:

- ConcurrentHashMap
- CopyOnWriteArrayList
- CopyOnWriteArraySet
(Full `java.util.concurrent` package has more — `BlockingQueue`, `ConcurrentLinkedQueue`, `ConcurrentSkipListMap`, etc. — but Sir prioritizes these three for OCJP/SCJP depth in this module.)

## 05:12 — ConcurrentHashMap (preview)

### Spelling / naming

Sir drills the name for interviews:

ConcurrentHashMap — can you spell out? Concurrent Hash Map

### Role in the hierarchy

- Implements ConcurrentMap interface (Video 156)
- Thread-safe alternative to HashMap
- Detailed internals, methods, and programs → Videos 157–159
### Quick contrast (expanded from Video 160 — forward reference)

When you later study HashMap vs ConcurrentHashMap, the differences trace directly back to today's three problems:

## 05:18 — CopyOnWriteArrayList (preview)

### Name

CopyOnWriteArrayList — Copy On Write Array List

### Why not "ConcurrentList"?

Student question Sir anticipates:

Why instead of concurrent list did they use the word CopyOnWrite?

Answer (deferred):

There is a big reason — the total behavior of this list is copy-on-write property only. What is that? We will discuss in detail.

Conceptual preview (for study notes):

- Copy-on-write (COW): On every mutating operation (add, set, remove), the underlying array is copied, modified, and swapped
- Iterators operate on a snapshot → no CME, safe for concurrent reads
- Trade-off: Writes are expensive; best when reads >> writes (e.g. listener lists, configuration caches)
```java
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.Iterator;

public class CopyOnWritePreview {
    public static void main(String[] args) {
        CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
        list.add("A");
        list.add("B");

        Iterator<String> it = list.iterator();
        System.out.println(it.next()); // "A"

        list.add("C"); // creates new backing array — iterator still sees old snapshot

        System.out.println(it.next()); // "B" — no CME
        // Iterator will NOT see "C" — it holds the snapshot from creation time
    }
}
```

## 05:53 — CopyOnWriteArraySet (preview)

### Name

CopyOnWriteArraySet — third concurrent collection

### Relationship to CopyOnWriteArrayList

- CopyOnWriteArraySet is backed internally by a CopyOnWriteArrayList
- Set semantics (no duplicates) + copy-on-write thread safety
- Same COW trade-offs apply
```java
import java.util.concurrent.CopyOnWriteArraySet;

CopyOnWriteArraySet<String> set = new CopyOnWriteArraySet<>();
set.add("X");
set.add("X"); // duplicate ignored
// Thread-safe, iteration never throws CME
```

## 06:07 — Session wrap-up checklist

Sir closes by confirming students should understand:

Final board list:

- ConcurrentHashMap
- CopyOnWriteArrayList
- CopyOnWriteArraySet
"These three classes we have to discuss in detail — with respect to programs."

## Deep dive supplements (exam enrichment)

### A. How to make traditional collections thread-safe (without concurrent classes)

From earlier collections lectures — for completeness:

```java
List<String> syncList = Collections.synchronizedList(new ArrayList<>());
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
Set<String> syncSet = Collections.synchronizedSet(new HashSet<>());
```

Sir's implicit point: These wrappers still lock the whole structure (like Vector) and still have CME risk if you iterate without manual synchronization → concurrent collections are the better scalable choice.

### B. Segment locking — mental model for ConcurrentHashMap

(Preview only — detailed in later videos)

ConcurrentHashMap internal view (conceptual):

[ Segment 0 ] [ Segment 1 ] ... [ Segment 15 ]   ← default 16 segments

Thread-1 updates key hashing to segment 3  → locks only segment 3
Thread-2 updates key hashing to segment 7  → locks only segment 7
→ Both can proceed concurrently (unlike Vector's single global lock)

### C. Fail-fast vs fail-safe (iterator behavior)

### D. Other concurrent collections (awareness — not Sir's focus in 155)

For OCJP/SCJP in this playlist, Sir prioritizes ConcurrentHashMap and CopyOnWrite variants first.

## OCJP / SCJP exam checklist

- [ ] List three problems of traditional collections
- [ ] State: concurrent collections are always thread-safe
- [ ] Explain why Vector/Hashtable are slow ( whole-object lock )
- [ ] Name segment locking / bucket-level locking as concurrent collection advantage
- [ ] Explain ConcurrentModificationException and why concurrent collections avoid it
- [ ] Know when to use concurrent collections (scalable multi-threaded apps)
- [ ] Name three key classes: ConcurrentHashMap, CopyOnWriteArrayList, CopyOnWriteArraySet
- [ ] Spell ConcurrentHashMap correctly in interviews
- [ ] Know concurrent collections package: java.util.concurrent, version 1.5
## Interview Q&A (rapid fire)

## Summary (one paragraph)

Video 155 is the comparison bridge in Durga Sir's Concurrent Collections module. After Part-1 established three problems with traditional collections — (1) most are not thread-safe, (2) legacy thread-safe classes like Vector and Hashtable lock the entire object and perform poorly, and (3) ConcurrentModificationException when iterating while other threads modify — this session shows how concurrent collections resolve all three: they are always thread-safe, use segment/bucket-level locking for better performance, and never throw CME because concurrent modification during iteration is handled safely. Concurrent collections are therefore best suited for scalable multi-threaded applications with many threads. Sir then previews the three classes to study in depth: ConcurrentHashMap, CopyOnWriteArrayList, and CopyOnWriteArraySet, with programs and internals starting in Video 156.

## What's next

End of Video 155 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 155 of 203 |  |  |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-2 \ | \ | Diff B/W Traditional & Concurrent Collections |
| URL | https://www.youtube.com/watch?v=ev8zxzRdsFQ |  |  |
| Duration | 7m 08s |  |  |
| Source | YouTube auto-captions (yt-dlp + node PO token) |  |  |
| Instructor | Durga Sir (OCJP/SCJP) |  |  |
| Package | java.util.concurrent (introduced in Java 1.5) |  |  |

| # | Problem | One-line summary |
|---|---|---|
| 1 | Not thread-safe | Most traditional collection classes are not thread-safe |
| 2 | Poor performance of legacy thread-safe classes | Even where thread safety exists (Vector, Hashtable), performance is not up to the mark |
| 3 | ConcurrentModificationException (CME) | The biggest headache — modifying a collection while another thread (or operation) is iterating causes runtime failure |

| Class | Thread-safe? |
|---|---|
| ArrayList | No |
| LinkedList | No |
| HashSet | No |
| HashMap | No |
| TreeSet / TreeMap | No |
| Vector | Yes (legacy) |
| Hashtable | Yes (legacy) |
| Stack | Yes (extends Vector) |
| Properties | Yes (extends Hashtable) |

| Aspect | Traditional collections | Concurrent collections |
|---|---|---|
| Thread safety | Most are not thread-safe | Every concurrent collection is always thread-safe |

| Aspect | Traditional thread-safe (Vector, Hashtable) | Concurrent collections |
|---|---|---|
| Lock scope | Entire collection locked for any operation | Segment / bucket level locking |
| Performance | Relatively low | Relatively high |
| Reason | One thread blocks all others on that object | Multiple threads can work on different segments concurrently |

| Aspect | Traditional collections | Concurrent collections |
|---|---|---|
| Iterate + modify (other threads) | Other threads not allowed to modify safely → CME | Other threads allowed to modify in safe manner |
| CME | Very common headache | Never get CME |

| # | Property | Traditional / Normal collections | Concurrent collections |
|---|---|---|---|
| 1 | Thread safety | Most are not thread-safe | Always thread-safe |
| 2 | Performance (thread-safe case) | Vector/Hashtable: lock whole object → slow | Segment/bucket locking → relatively high performance |
| 3 | ConcurrentModificationException | Common when iterate + modify | Never throws CME |
| 4 | Best use case | Single-threaded or low concurrency | Scalable multi-threaded applications |
| 5 | Java version | Core collections from 1.0 / 1.2 | java.util.concurrent from 1.5 |

| Situation | Recommendation |
|---|---|
| Single-threaded CLI / simple program | ArrayList, HashMap — fine |
| Few threads + external synchronization | May use Collections.synchronizedList() — but performance hit |
| High concurrency, many reader/writer threads | Concurrent collections (ConcurrentHashMap, CopyOnWriteArrayList, etc.) |
| Legacy code on Vector/Hashtable | Consider migrating to concurrent alternatives for scale |

| # | Class | Package |
|---|---|---|
| 1 | ConcurrentHashMap | java.util.concurrent |
| 2 | CopyOnWriteArrayList | java.util.concurrent |
| 3 | CopyOnWriteArraySet | java.util.concurrent |

| Property | HashMap | ConcurrentHashMap |
|---|---|---|
| Thread-safe | No | Yes |
| CME during iteration | Yes (fail-fast iterator) | No (fail-safe iterator) |
| Performance under many threads | High for single-thread; unsafe for shared access | Threads may wait on segment locks (default 16 updaters) — trade safety for some wait |
| null key/value | Allowed (one null key, many null values) | Not allowed |
| Since | 1.2 | 1.5 |

| Topic | Status after Video 155 |
|---|---|
| What is a traditional collection | ✓ (prior course) |
| What problems exist with traditional collections | ✓ (3 problems) |
| Why not suitable for scalable multi-threaded apps | ✓ |
| How concurrent collections overcome each problem | ✓ (this video) |
| Why concurrent collections suit multi-threaded scalable apps | ✓ |
| Three important concurrent collection classes | ✓ — CHM, COWAL, COWAS |
| Detailed programs & internals | → Videos 156+ |

| Iterator type | Behavior on concurrent modification | Example |
|---|---|---|
| Fail-fast | Immediately throws CME | HashMap, ArrayList, HashSet iterators |
| Fail-safe | Works on snapshot / weakly consistent view; no CME | ConcurrentHashMap, CopyOnWriteArrayList iterators |

| Class | Purpose |
|---|---|
| ConcurrentLinkedQueue | Non-blocking thread-safe queue |
| LinkedBlockingQueue | Blocking queue (producer-consumer) |
| ArrayBlockingQueue | Bounded blocking queue |
| ConcurrentSkipListMap / ConcurrentSkipListSet | Sorted concurrent map/set |
| BlockingDeque implementations | Work stealing, thread pools |

| Question | Answer |
|---|---|
| Difference between normal and concurrent collections? | Thread safety, performance (locking granularity), CME behavior — see master table |
| Are all traditional collections thread-safe? | No — most are not; only legacy ones like Vector/Hashtable |
| Are all concurrent collections thread-safe? | Yes — always |
| Why is Vector slow in multi-threading? | Synchronizes entire collection for every operation |
| What locking do concurrent collections use? | Segment / bucket-level locking (not whole collection) |
| What is CME? | Runtime exception when collection structurally modified during iteration (outside iterator's remove) |
| Do concurrent collections throw CME? | No — never |
| When must you use concurrent collections? | Scalable multi-threaded applications (many threads, shared data) |
| Name three concurrent collection classes | ConcurrentHashMap, CopyOnWriteArrayList, CopyOnWriteArraySet |
| Why CopyOnWrite instead of ConcurrentList? | Behavior is copy-on-write — explained in detail in CopyOnWriteArrayList lecture |

| Video | Topic |
|---|---|
| 156 | Concurrent Collections Part-3 — ConcurrentMap methods |
| 157 | Part-4 — ConcurrentHashMap details |
| 158 | Part-5 — ConcurrentHashMap Program-1 |
| 159 | Part-6 — ConcurrentHashMap Program-2 |
| 160 | Part-7 — HashMap vs ConcurrentHashMap (full comparison table + fail-fast/fail-safe) |
