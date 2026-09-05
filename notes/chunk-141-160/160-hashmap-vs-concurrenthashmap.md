# Video 160 — Concurrent Collections Part-7: HashMap vs ConcurrentHashMap

## Video info

ASR decode (this lecture): Ash map / hash M / hmap = HashMap; concurrent Ash map / concat map / concat a Map / current hash map = ConcurrentHashMap; threat / threats = thread(s); thread safe = thread-safe; fail first = fail-fast; inter room / ENT room = interview room; normal collection / current collection = normal collection vs concurrent collection; updation = modification/update; Valu = value.

## Session overview

This is a pure comparison / interview-prep session. Sir does not write new demo code here — he consolidates everything already taught in Videos 157–159 into one definitive answer for the most common concurrent-collections interview question:

What is the difference between HashMap and ConcurrentHashMap?

Sir explicitly warns: Do not answer "ConcurrentHashMap is concurrent — that is the difference." That is naming, not functionality. You must explain how they differ in thread safety, performance, exceptions, null rules, iterators, and version.

Prerequisites (prior videos in this block):

What this lecture covers (~8 min):

- Six functional differences between HashMap and ConcurrentHashMap
- Fail-fast vs fail-safe iterators — conceptual model with diagram
- Full comparison table (board form)
- Interview one-liner summary
- Version history (1.2 vs 1.5)
What comes next (Sir's closing hint): HashMap vs ConcurrentHashMap vs Hashtable three-way comparison, and ConcurrentHashMap vs CopyOnWriteArrayList — deferred to upcoming sessions.

## 00:26 — The interview question

Sir opens with a direct statement:

"Now I will cover one very important question for the interview room: What is the difference between HashMap and ConcurrentHashMap?"

Context framing:

- We have already studied normal collections (HashMap, ArrayList, etc.) and concurrent collections (ConcurrentHashMap, CopyOnWriteArrayList, etc.).
- Our existing knowledge from the concurrent-collections module is more than enough to answer this question.
- The answer is very simple once you understand the prior lectures — this session is the revision and consolidation lecture.
Wrong answer (Sir rejects this immediately):

"Concurrent is the difference."

That tells the interviewer nothing about behavior. You must compare functionality.

## 01:00 — Difference 1: Thread safety

### HashMap — not thread-safe

```java
import java.util.HashMap;
import java.util.Map;

Map<Integer, String> map = new HashMap<>();
// Multiple threads can call put/get/remove simultaneously
// → NO synchronization → data inconsistency possible
```

Board conclusion: On a normal HashMap object, multiple threads are allowed to perform operations simultaneously. There may be a chance of data inconsistency problems. That is why normal HashMap is not thread-safe.

### ConcurrentHashMap — thread-safe

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;

ConcurrentMap<Integer, String> map = new ConcurrentHashMap<>();
// Multiple threads can operate safely
// Updates use segment/bucket-level locks (Video 157)
```

Board conclusion: Even when multiple threads operate on ConcurrentHashMap, they do so in a safe manner only. That is why ConcurrentHashMap is always thread-safe.

Interview one-liner: HashMap is not thread-safe; ConcurrentHashMap is thread-safe.

## 01:14 — Difference 2: ConcurrentModificationException (CME)

### What triggers CME on HashMap

While one thread is iterating over a HashMap (via keySet().iterator(), entrySet().iterator(), or enhanced for-loop), if another thread tries to modify the underlying map (add/remove entry), the iterator immediately fails by raising ConcurrentModificationException.

This is the classic multithreading pitfall demonstrated programmatically in Video 159.

### ConcurrentHashMap behavior

While one thread is iterating ConcurrentHashMap, other threads are allowed to modify the map object in a safe manner. ConcurrentHashMap never throws ConcurrentModificationException.

Sir extends this rule: Not only ConcurrentHashMap — any concurrent collection never throws ConcurrentModificationException.

Interview one-liner: HashMap → we will get ConcurrentModificationException. ConcurrentHashMap → we never get ConcurrentModificationException.

## 01:23 — Difference 3: Performance (relative)

### HashMap — high performance (no waiting)

Because HashMap is not synchronized, there is no lock contention:

- Even one lakh (100,000) threads can simultaneously operate on a HashMap object.
- No thread needs to wait for another thread to finish.
- Trade-off: speed comes at the cost of thread safety.
### ConcurrentHashMap — relatively lower performance (some waiting)

ConcurrentHashMap uses segment/bucket-level locking (covered in Video 157):

The 17th update thread must wait until one of the 16 segment locks is released. That waiting is why ConcurrentHashMap has relatively lower performance than HashMap.

Sir's exact wording:

"At a time how many threads are allowed to perform read operation? Any number of threads. But at a time how many threads are allowed to perform update operation? By default 16. If the 17th thread is coming, it has to wait. That's why relatively performance is low — because sometimes threads are required to wait."

Important nuance for interviews: ConcurrentHashMap is still much faster than Hashtable (which allows only one thread total for any operation). The "low performance" here is relative to HashMap, not absolute.

Interview one-liner: HashMap — relatively high performance (no waiting). ConcurrentHashMap — relatively low performance (threads sometimes wait for segment locks).

## 02:11 — Difference 4: Iterator behavior — fail-fast vs fail-safe

This is a separate topic Sir will cover in more depth later, but the basic idea is compulsory for the interview room.

### Fail-fast iterator (HashMap)

Definition (Sir's board wording):

If you modify the underlying collection while the iterator is active, the iterator immediately fails by raising ConcurrentModificationException. Such iterators are called fail-fast iterators. It fails very fast — hence "fail-fast."

Visual model:

Collection object
    │
    ├── Thread-1: Iterator iterating...
    │       while (it.hasNext()) { ... }
    │
    └── Thread-2: tries put/remove on same collection
            ↓
        Iterator FAILS IMMEDIATELY
            ↓
        ConcurrentModificationException

HashMap iterator = fail-fast because while one thread iterates, if any other thread modifies the map, the iterator fails very fast by raising CME.

### Fail-safe iterator (ConcurrentHashMap)

Definition (Sir's board wording):

While one thread is iterating in a safe way, remaining threads are allowed to modify the map object without raising ConcurrentModificationException. Such iterators are called fail-safe iterators.

Visual model:

ConcurrentHashMap object
    │
    ├── Thread-1: Iterator iterating...
    │       while (it.hasNext()) { ... }
    │
    └── Thread-2: put/remove on same map (safe manner)
            ↓
        Iterator does NOT fail
            ↓
        No ConcurrentModificationException

ConcurrentHashMap iterator = fail-safe because the iterator never fails and never raises CME, even when other threads modify the map concurrently.

### Critical caveat from Video 159 (Sir's programmatic proof)

While ConcurrentHashMap allows concurrent modification during iteration:

- No CME — confirmed by the demo program.
- No guarantee that concurrent updates are visible to the iterator — the update may or may not appear in the iteration depending on whether the iterator cursor has already passed that bucket/cell.
- After iteration completes, if you print the map (System.out.println(m)), the update will be visible.
Sir's conclusion from Video 159:

"While main thread is iterating, other thread is allowed to perform modification — but that update is not available to the iterator. There is no guarantee. At last when you print `m`, that update you can see."

Interview one-liner: Iterator of HashMap is fail-fast. Iterator of ConcurrentHashMap is fail-safe.

## 01:57 — Difference 5: Null key and null value

Sir's exact phrasing:

"Null is allowed for both key and value if it is normal HashMap. But ConcurrentHashMap — null, such a type of story not applicable — whether it is key or value."

This matches Hashtable as well (Video 157 noted: null not allowed in Hashtable or ConcurrentHashMap).

```java
// HashMap — OK
Map<String, String> hm = new HashMap<>();
hm.put(null, "value");   // allowed
hm.put("key", null);     // allowed

// ConcurrentHashMap — NullPointerException
ConcurrentMap<String, String> chm = new ConcurrentHashMap<>();
chm.put(null, "value");  // NullPointerException
chm.put("key", null);    // NullPointerException
```

Interview one-liner: HashMap allows null for both key and value. ConcurrentHashMap does not allow null for key or value.

## 07:04 — Difference 6: Java version introduced

Concurrent collections as a whole came in 1.5 along with the java.util.concurrent package, locks, thread pools, etc. (Videos 096–098 in the multithreading block).

Interview one-liner: HashMap — 1.2. ConcurrentHashMap — 1.5.

## 04:30 — Master comparison table (board form)

Sir puts all differences into one table for easy exam writing:

## 05:50 — Deep dive: CME scenario restated

Sir revisits the third row of the table with extra detail:

### HashMap scenario

Thread-1: iterating HashMap (keySet iterator)
Thread-2: tries to modify HashMap (put/remove)
    → ConcurrentModificationException

Why we get CME: HashMap's iterator maintains an internal modification count (modCount). When the map is structurally modified during iteration, the iterator detects the change and throws CME immediately. This is by design — fail-fast behavior protects against undefined iteration results.

### ConcurrentHashMap scenario

Thread-1: iterating ConcurrentHashMap
Thread-2: modifies ConcurrentHashMap (put/remove) in safe manner
    → NO ConcurrentModificationException
    → Iterator continues (fail-safe)
    → But update may not be visible to iterator (Video 159)

## 06:21 — Deep dive: fail-fast vs fail-safe restated

Sir emphasizes the word "fail-fast" is very important:

Exam tip: Fail-fast and fail-safe are iterator properties, not collection properties per se — but Sir maps them directly: HashMap iterator = fail-fast; ConcurrentHashMap iterator = fail-safe.

## Reference — Demo program from Video 159 (programmatic proof)

This program is not written live in Video 160, but Sir's entire CME/fail-safe discussion assumes you have seen it. Included here because every board example must be actual Java.

### Program A — ConcurrentHashMap: NO CME (fail-safe)

```java
import java.util.*;
import java.util.concurrent.*;

class MyThread extends Thread {
    static ConcurrentMap<Integer, String> m = new ConcurrentHashMap<>();

    public void run() {
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {}
        System.out.println("Child thread updating map");
        m.put(103, "C");
    }
}

public class Test {
    public static void main(String[] args) throws InterruptedException {
        MyThread.m.put(101, "A");
        MyThread.m.put(102, "B");

        MyThread t = new MyThread();
        t.start();

        Set<Integer> keys = MyThread.m.keySet();
        Iterator<Integer> it = keys.iterator();
        while (it.hasNext()) {
            Integer key = it.next();
            System.out.println("Main thread iterating map and current entry is "
                + key + " " + MyThread.m.get(key));
            Thread.sleep(2000);
        }
    }
}
```

Expected behavior:

- Main thread iterates keys 101, 102 (order not guaranteed).
- Child thread updates map with 103=C while main thread is iterating.
- No ConcurrentModificationException.
- Update 103=C may not appear during iteration but will appear if you print m after the loop.
Sample output (from Video 159):

Main thread iterating map and current entry is 102 B
Child thread updating map
Main thread iterating map and current entry is 101 A

Notice: child already added 103=C, but iterator did not show it — no guarantee of visibility to iterator.

### Program B — HashMap: CME thrown (fail-fast)

Same program, but replace ConcurrentHashMap with HashMap:

```java
import java.util.*;

class MyThread extends Thread {
    static Map<Integer, String> m = new HashMap<>();  // ONLY CHANGE

    public void run() {
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {}
        System.out.println("Child thread updating map");
        m.put(103, "C");
    }
}

public class Test {
    public static void main(String[] args) throws InterruptedException {
        MyThread.m.put(101, "A");
        MyThread.m.put(102, "B");

        MyThread t = new MyThread();
        t.start();

        Set<Integer> keys = MyThread.m.keySet();
        Iterator<Integer> it = keys.iterator();
        while (it.hasNext()) {
            Integer key = it.next();
            System.out.println("Main thread iterating map and current entry is "
                + key + " " + MyThread.m.get(key));
            Thread.sleep(2000);
        }
    }
}
```

Expected behavior:

- Main thread starts iterating.
- Child thread calls m.put(103, "C").
- Immediately: java.util.ConcurrentModificationException
This is the programmatic proof of the difference Sir summarizes in Video 160.

## Reference — ConcurrentHashMap locking recap (from Video 157)

Video 160 assumes you know why ConcurrentHashMap has the performance characteristics it does. Quick recap for completeness:

ConcurrentHashMap (default: 16 buckets, concurrency level 16)
┌────────┬────────┬────────┬─────┬────────┐
│Bucket 0│Bucket 1│Bucket 2│ ... │Bucket15│
│ Lock 0 │ Lock 1 │ Lock 2 │ ... │Lock 15 │
└────────┴────────┴────────┴─────┴────────┘

Read operation  → NO lock required → unlimited concurrent reads
Update operation → requires lock of THAT bucket/segment only
                 → default 16 simultaneous updates
                 → 17th update thread WAITS

Contrast with HashMap:

HashMap
┌──────────────────────────────────────┐
│         Single map object            │
│    NO locks — all threads free       │
│    → fast but NOT thread-safe        │
└──────────────────────────────────────┘

Contrast with Hashtable (for context — Video 157):

Hashtable
┌──────────────────────────────────────┐
│         Single map object            │
│    ONE lock for ENTIRE map           │
│    → only 1 thread at a time         │
│    → thread-safe but VERY slow       │
└──────────────────────────────────────┘

## 07:16 — Interview answer template

Sir's closing instruction:

"If any person is asking what is the difference between normal HashMap and ConcurrentHashMap, you should be in a position to tell ALL differences."

### Full answer (structured)

- Thread safety: HashMap is not thread-safe. ConcurrentHashMap is thread-safe.
- ConcurrentModificationException: HashMap throws CME when one thread iterates and another modifies. ConcurrentHashMap never throws CME.
- Performance: HashMap has relatively high performance (no waiting). ConcurrentHashMap has relatively lower performance (update threads may wait; default 16 concurrent updates).
- Iterator: HashMap iterator is fail-fast. ConcurrentHashMap iterator is fail-safe.
- Null: HashMap allows null key and null value. ConcurrentHashMap allows neither.
- Version: HashMap since 1.2. ConcurrentHashMap since 1.5 (concurrent collections package).
### Ultra-short answer (if interviewer wants "main difference")

HashMap is not thread-safe and throws ConcurrentModificationException during concurrent iteration+modification. ConcurrentHashMap is thread-safe, never throws CME, uses segment locking (16 default concurrent updates), does not allow null, and its iterator is fail-safe.

## Quick revision cards

## When to use which

Sir's statement from Video 159:

"Concurrent collections are best suitable for multithreaded scalable applications."

## Exam traps and clarifications

- "ConcurrentHashMap is slower" — true relative to HashMap, but much faster than Hashtable. Always clarify the comparison baseline.
- "Fail-safe means iterator sees all concurrent updates" — FALSE. Fail-safe means no CME. Visibility of concurrent updates to the iterator is not guaranteed (Video 159 demo proves this).
- "ConcurrentHashMap allows unlimited concurrent updates" — FALSE. Default is 16 simultaneous update operations (concurrency level). Reads are unlimited.
- "HashMap iterator is fail-safe" — FALSE. HashMap iterator is fail-fast.
- "We can use null in ConcurrentHashMap for value only" — FALSE. Null is not allowed for either key or value.
- "ConcurrentModificationException means two threads modified the map" — not necessarily. Even one thread modifying via non-iterator path while another thread (or same thread) iterates can trigger CME on fail-fast collections.
- "ConcurrentHashMap extends HashMap" — FALSE. ConcurrentHashMap implements ConcurrentMap (which extends Map). Separate class hierarchy.
## Class hierarchy (for reference)

Map (interface)                          ← java.util
 ├── HashMap (class)                     ← NOT thread-safe, 1.2
 ├── Hashtable (class)                  ← thread-safe, entire-map lock, 1.0 legacy
 └── ConcurrentMap (interface)         ← java.util.concurrent, 1.5
      └── ConcurrentHashMap (class)      ← thread-safe, segment locking, 1.5

## Summary table — one glance before exam

## Closing (07:40)

Sir ends with:

"That's all."

Next topics hinted at end of Video 159 (not covered in 160):

- HashMap vs ConcurrentHashMap vs Hashtable (three-way)
- ConcurrentHashMap vs CopyOnWriteArrayList (fail-safe mechanisms differ internally)
Video 160 is the definitive HashMap vs ConcurrentHashMap answer sheet. Memorize the master table and be able to explain fail-fast vs fail-safe with the iteration+modification scenario.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-7 \ | \ | HashMap & ConcurrentHashMap |
| URL | https://www.youtube.com/watch?v=c6u87_gMBDU |  |  |
| Duration | ~8 minutes 05 seconds |  |  |
| Position | 160 of 203 in the Durga Sir OCJP/SCJP playlist |  |  |
| Playlist | Core Java With OCJP/SCJP |  |  |
| Package | java.util (HashMap) vs java.util.concurrent (ConcurrentHashMap) |  |  |
| Source | YouTube auto-generated captions (ASR) |  |  |

| Video | Topic |
|---|---|
| 156 | ConcurrentMap interface — putIfAbsent, conditional remove, replace |
| 157 | ConcurrentHashMap internals — segment/bucket locking, concurrency level, constructors |
| 158 | ConcurrentHashMap Program-1 — demo of ConcurrentMap special methods |
| 159 | ConcurrentHashMap Program-2 — iteration + concurrent update demo; HashMap throws CME |

|  | HashMap | ConcurrentHashMap |
|---|---|---|
| Thread-safe? | NO | YES |
| Mechanism | No synchronization; multiple threads may operate on the same HashMap object simultaneously | Multiple threads can operate, but updates happen in a safe manner via segment/bucket-level locking |
| Risk | Data inconsistency problems are possible | Thread safety guaranteed by design |

|  | HashMap | ConcurrentHashMap |
|---|---|---|
| CME during iteration + modification? | YES — very common scenario | NO — never throws CME |
| Applies to | Normal (non-concurrent) collections generally | Any concurrent collection — none throw CME |

|  | HashMap | ConcurrentHashMap |
|---|---|---|
| Relative performance | High | Low (relatively) |
| Why | Threads are not required to wait to operate on HashMap | Threads are sometimes required to wait |

| Operation type | How many threads at a time? |
|---|---|
| Read (get, containsKey, etc.) | Any number — read operations do not require a lock |
| Update (put, remove, replace, etc.) | By default 16 — one update per segment/bucket lock |

|  | HashMap | ConcurrentHashMap |
|---|---|---|
| Iterator type | Fail-fast | Fail-safe |
| Modifies during iteration? | Other threads modifying → iterator fails immediately | Other threads modifying → iterator does not fail |
| Exception | ConcurrentModificationException | Never CME |

|  | HashMap | ConcurrentHashMap |
|---|---|---|
| Null key | Allowed (only once — duplicate null key not possible anyway) | NOT allowed → NullPointerException |
| Null value | Allowed (any number of entries can have null value) | NOT allowed → NullPointerException |

|  | HashMap | ConcurrentHashMap |
|---|---|---|
| Introduced in | Java 1.2 | Java 1.5 |
| Category | Part of original Collections Framework (Map module) | Part of java.util.concurrent package (concurrent collections) |

| # | Property | HashMap (normal) | ConcurrentHashMap (concurrent) |
|---|---|---|---|
| 1 | Thread safety | NOT thread-safe — multiple threads operate simultaneously → data inconsistency possible | Thread-safe — multiple threads operate in safe manner via segment/bucket locking |
| 2 | Relative performance | High — threads not required to wait; even 1 lakh threads can operate simultaneously | Low (relatively) — update threads may wait; default 16 concurrent updates; reads unlimited |
| 3 | ConcurrentModificationException | YES — while one thread iterates, other threads modifying → CME | NO — while one thread iterates, other threads can modify safely; never CME |
| 4 | Iterator type | Fail-fast — iterator fails immediately on concurrent modification | Fail-safe — iterator never fails; never raises CME |
| 5 | Null key / null value | Allowed for both key and value | NOT allowed for key or value |
| 6 | Version introduced | 1.2 | 1.5 |
| 7 | Package | java.util | java.util.concurrent |
| 8 | Locking model | No locking | Segment/bucket-level locking; default concurrency level = 16 |
| 9 | Read operations | No lock concept (no thread safety) | Any number of concurrent reads — no lock required |
| 10 | Update operations | Unlimited simultaneous (unsafe) | Default 16 simultaneous safe updates |

| Term | Behavior | Collection example |
|---|---|---|
| Fail-fast | While iterating, if anyone tries to modify → iterator fails very fast → CME | HashMap, ArrayList, HashSet, etc. (normal collections) |
| Fail-safe | While iterating, other threads can modify → iterator never fails → no CME | ConcurrentHashMap, CopyOnWriteArrayList, etc. (concurrent collections) |

| Question | Answer |
|---|---|
| Is HashMap thread-safe? | No |
| Is ConcurrentHashMap thread-safe? | Yes |
| CME on HashMap during iteration? | Yes |
| CME on ConcurrentHashMap? | Never |
| HashMap performance vs CHM? | HashMap higher (no lock wait) |
| Max concurrent updates on CHM (default)? | 16 |
| Max concurrent reads on CHM? | Unlimited |
| Null key in HashMap? | Allowed |
| Null key in ConcurrentHashMap? | Not allowed (NPE) |
| HashMap iterator? | Fail-fast |
| CHM iterator? | Fail-safe |
| HashMap introduced? | Java 1.2 |
| ConcurrentHashMap introduced? | Java 1.5 |
| CHM package? | java.util.concurrent |

| Scenario | Use |
|---|---|
| Single-threaded application | HashMap — simpler, faster, allows null |
| Multi-threaded app, all access synchronized externally | HashMap + external sync, or Collections.synchronizedMap() |
| Multi-threaded scalable app, frequent reads, concurrent updates | ConcurrentHashMap — best choice per Sir (Video 159) |
| Legacy code requiring thread-safe map, no concurrent package | Hashtable (or prefer ConcurrentHashMap in modern code) |
| Need null keys/values in shared map | HashMap with external synchronization (CHM forbids null) |

| # | HashMap | ConcurrentHashMap |
|---|---|---|
| 1 | Not thread-safe | Thread-safe |
| 2 | High performance (no wait) | Relatively low (update threads wait) |
| 3 | CME during iterate + modify | Never CME |
| 4 | Fail-fast iterator | Fail-safe iterator |
| 5 | Null key ✓, null value ✓ | Null key ✗, null value ✗ |
| 6 | Java 1.2 | Java 1.5 |
| 7 | java.util | java.util.concurrent |
| 8 | No locking | Segment lock; 16 default concurrent updates |
| 9 | Unlimited unsafe concurrent access | Unlimited safe reads + 16 safe updates |
