# Video 170 — Concurrent Collections Part-17: CopyOnWriteArrayList, synchronizedList(), Vector

## Video info

ASR decode notes: copy/write list / copy n te list / copy not write list / copy not make list = CopyOnWriteArrayList; current modification exception / cant modification exception / concat modification exception = ConcurrentModificationException; single list = synchronizedList; no redo operation = no remove operation (via iterator); copy on make = CopyOnWriteArrayList.

## Session overview

This is the summary comparison lecture for three thread-safe List implementations. Sir answers the interview question: "CopyOnWriteArrayList, synchronizedList, and Vector are all thread-safe — where is the difference?"

Prerequisites (full CopyOnWriteArrayList module):

What this session covers:

- All three are thread-safe — but different mechanisms
- How each achieves thread safety (clone-copy vs whole-object lock)
- Concurrent access model — multiple threads vs one-at-a-time
- Iterate + modify behavior — CME vs no CME
- Iterator capabilities — read-only vs read+remove
- Fail-safe vs fail-fast iterators
- Master comparison table (documentation-ready diagram)
What this session does NOT cover:

- ConcurrentHashMap comparisons (Videos 157–160)
- Performance benchmarks or micro-profiling
- CopyOnWriteArraySet (same copy-on-write semantics)
## 00:18 — Opening: Three thread-safe lists, three different models

### The interview question

"CopyOnWriteArrayList is thread-safe. synchronizedList is thread-safe. Vector is also thread-safe. All three are thread-safe — but where is the difference?"

### High-level answer preview

All three are thread-safe. The mechanism and behavior differ completely.

## 00:58 — Point 1: How thread safety is achieved

### CopyOnWriteArrayList — copy-on-write mechanism

Thread-1 calls add("X")  →  clone current array  →  add X to clone  →  replace reference
Thread-2 calls add("Y")  →  clone (possibly updated) array  →  add Y  →  replace reference
Thread-3 iterating       →  reads from its snapshot  →  unaffected by Thread-1/2 writes

- No lock on whole list for reads
- Writes are expensive (array copy) but reads are fast and lock-free
- Existing iterators and readers continue on old snapshot
### synchronizedList and Vector — mutual exclusion (lock)

Thread-1 acquires lock  →  performs operation  →  releases lock
Thread-2 waits...
Thread-3 waits...
Thread-1 done           →  Thread-2 acquires lock  →  ...

Vector:

```java
public class Vector<E> extends AbstractList<E> {
    public synchronized boolean add(E e) { ... }
    public synchronized E get(int index) { ... }
    // every public method synchronized
}
```

synchronizedList (via Collections.synchronizedList):

List<String> syncList = Collections.synchronizedList(new ArrayList<>());
// wrapper delegates to backing list with synchronized block on each method

- At a time, only ONE thread allowed to operate
- All threads operate one by one — automatic serialization
- Total collection object locked during each operation
### Thread safety mechanism comparison

## 02:00 — Point 2: Concurrent access — how many threads at a time?

### CopyOnWriteArrayList

"At a time, multiple threads are allowed to operate on CopyOnWriteArrayList."

- Multiple threads can read simultaneously (each on snapshot)
- Multiple threads can write (each creates own clone — with coordination internally)
- Multiple threads can read while others write — no blocking for readers
### synchronizedList and Vector

"At a time, only one thread is allowed to operate."

- Thread-2 must wait until Thread-1 completes
- Even two read-only threads cannot run concurrently — whole object locked
- Performance bottleneck under high concurrency (Sir's Video 154 Reason 2)
### Concurrency model table

## 02:34 — Point 3: Iterate + modify — ConcurrentModificationException

### CopyOnWriteArrayList

"While one thread is iterating the list, the other thread is also allowed to modify — no problem."

- Modification happens on separate cloned copy
- No `ConcurrentModificationException`
- Iterator is fail-safe
```java
// Video 166 pattern — works with CopyOnWriteArrayList
Iterator itr = cowList.iterator();     // main thread
// child thread: cowList.add("D");     // NO CME
while (itr.hasNext()) { itr.next(); }
```

### synchronizedList and Vector

"While one thread is iterating synchronizedList/Vector, if another thread tries to modify → immediately `ConcurrentModificationException`."

- Even though list methods are synchronized, iterator is NOT fail-safe
- Iterator created without holding lock throughout iteration
- Another thread modifies between hasNext() and next() → CME
List syncList = Collections.synchronizedList(new ArrayList<>());
// Thread-1: Iterator it = syncList.iterator(); while(it.hasNext()) ...
// Thread-2: syncList.add("X");  → ConcurrentModificationException

Manual fix for synchronizedList (verbose — why concurrent collections preferred):

```java
synchronized (syncList) {
    for (String s : syncList) {
        System.out.println(s);
    }
}
```

### Iterate + modify comparison

## 03:46 — Point 4: Iterator operations — read vs remove

### CopyOnWriteArrayList iterator

"Iterator can perform only read operation — NOT remove operation."

- By mistake if you call itr.remove() → `UnsupportedOperationException`
- Remove would require modifying snapshot copy — would break consistency model
- Covered programmatically in Video 167
```java
CopyOnWriteArrayList<String> cow = new CopyOnWriteArrayList<>(Arrays.asList("A", "B", "C"));
Iterator<String> itr = cow.iterator();
while (itr.hasNext()) {
    String s = itr.next();
    if (s.equals("B")) {
        itr.remove();   // UnsupportedOperationException
    }
}
```

### synchronizedList and Vector iterators

"Iterator can perform both read and remove operation — no problem."

- itr.remove() is supported — removes current element via iterator
- Standard fail-fast iterator with structural remove coordination
- Same as ArrayList iterator behavior (but list itself is synchronized)
```java
Vector<String> v = new Vector<>(Arrays.asList("A", "B", "C", "D"));
Iterator<String> itr = v.iterator();
while (itr.hasNext()) {
    Integer i = Integer.valueOf(itr.next());  // if Integer elements
    if (i % 2 == 0) {
        itr.remove();   // OK on Vector — no UnsupportedOperationException
    }
}
```

### Iterator capability table

## 04:02 — Point 5: Legacy vs modern thread-safe list

### Vector — legacy (Java 1.0)

- Predates Collections Framework (Java 1.2)
- All methods synchronized — coarse-grained locking
- Still thread-safe but not recommended for new code
- Superseded by ArrayList + Collections.synchronizedList or CopyOnWriteArrayList
### synchronizedList — wrapper pattern (Java 1.2)

List<String> list1 = Collections.synchronizedList(new ArrayList<>());
List<String> list2 = Collections.synchronizedList(new LinkedList<>());
// Works with ANY List implementation

- Thread-safe wrapper around any List
- Same one-thread-at-a-time limitation as Vector
- Same CME risk during unsynchronized iteration
### CopyOnWriteArrayList — concurrent collection (Java 1.5)

```java
CopyOnWriteArrayList<String> cow = new CopyOnWriteArrayList<>();
```

- Designed for concurrent access from ground up
- Best when: many reads, few writes
- Worst when: many writes (copy cost per write)
## 04:24 — Master comparison table (Sir's documentation diagram)

### Complete five-point comparison

### When to use which (decision guide)

## Code examples: Same scenario, three implementations

### Scenario: Main iterates, child thread adds "D"

CopyOnWriteArrayList — succeeds:

```java
import java.util.*;
import java.util.concurrent.*;

class Demo {
    static CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();

    static class AddThread extends Thread {
        public void run() { list.add("D"); }
    }

    public static void main(String[] args) throws Exception {
        list.addAll(Arrays.asList("A", "B", "C"));
        new AddThread().start();
        for (String s : list) {
            System.out.println(s);
        }
    }
}
// Output: A, B, C (possibly D) — NO exception
```

Vector — ConcurrentModificationException:

```java
import java.util.*;

class Demo {
    static Vector<String> list = new Vector<>();

    static class AddThread extends Thread {
        public void run() { list.add("D"); }
    }

    public static void main(String[] args) throws Exception {
        list.addAll(Arrays.asList("A", "B", "C"));
        new AddThread().start();
        Iterator<String> itr = list.iterator();
        while (itr.hasNext()) {
            System.out.println(itr.next());  // CME when child adds D
        }
    }
}
```

synchronizedList — ConcurrentModificationException:

```java
import java.util.*;

class Demo {
    static List<String> list = Collections.synchronizedList(new ArrayList<>());

    static class AddThread extends Thread {
        public void run() { list.add("D"); }
    }

    public static void main(String[] args) throws Exception {
        list.addAll(Arrays.asList("A", "B", "C"));
        new AddThread().start();
        Iterator<String> itr = list.iterator();
        while (itr.hasNext()) {
            System.out.println(itr.next());  // CME
        }
    }
}
```

## Fail-fast vs fail-safe summary

## OCJP / SCJP exam checklist

- [ ] All three (CopyOnWriteArrayList, synchronizedList, Vector) are thread-safe
- [ ] Know different mechanisms: clone-copy vs synchronized/lock
- [ ] CopyOnWriteArrayList: multiple threads can operate; others: one at a time
- [ ] CopyOnWriteArrayList: iterate + modify → no CME; others → CME
- [ ] CopyOnWriteArrayList iterator: read only, remove → UnsupportedOperationException
- [ ] Vector/synchronizedList iterator: read + remove supported
- [ ] CopyOnWriteArrayList: fail-safe; Vector/synchronizedList: fail-fast
- [ ] Know Collections.synchronizedList(new ArrayList<>()) factory method
- [ ] Vector is legacy — prefer concurrent collections for new code
- [ ] CopyOnWriteArrayList best for read-heavy, write-light workloads
## Interview Q&A (rapid fire)

## Connection to Video 154 three reasons

Conclusion: CopyOnWriteArrayList addresses all three reasons from Video 154. Vector and synchronizedList only address Reason 1 (thread safety) but retain Reasons 2 and 3 problems.

## Related videos

## Summary (one paragraph)

Video 170 is Durga Sir's capstone comparison of three thread-safe List options: CopyOnWriteArrayList, Collections.synchronizedList(), and Vector. All three provide thread safety, but through fundamentally different mechanisms. CopyOnWriteArrayList achieves safety by performing every update on a separate cloned copy, allowing multiple threads to operate concurrently with fail-safe iterators that never throw ConcurrentModificationException — but iterator remove is unsupported. Vector and synchronizedList achieve safety by allowing only one thread at a time on the entire list object via synchronization, which creates performance bottlenecks and fail-fast iterators that throw ConcurrentModificationException if one thread iterates while another modifies. Sir presents a five-row comparison table covering mechanism, concurrent access, iterate+modify behavior, iterator type, and remove support — the documentation-ready answer for OCJP interviews and certification exams asking "all are thread-safe, where is the difference?"

End of Video 170 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |
|---|---|---|
| Position | 170 of 203 |  |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-17 \ | CopyOnWriteArrayList, synchronizedList(), Vector |
| Instructor | Durga Sir (OCJP/SCJP) |  |
| Duration | 8m 13s |  |
| Video ID | 6FXfRR6gzEU |  |
| Watch URL | https://www.youtube.com/watch?v=6FXfRR6gzEU |  |
| Duration | 8m 13s |  |
| Playlist | Core Java With OCJP/SCJP |  |
| Notes source | YouTube auto-captions (yt-dlp + node PO token) |  |

| Video | Topic |
|---|---|
| 154 | Need for concurrent collections — CME, performance, thread safety |
| 163–168 | CopyOnWriteArrayList theory and four programs |
| 169 | (Intermediate program/topic in series) |

| Implementation | Thread safety via |
|---|---|
| CopyOnWriteArrayList | Every update on separate cloned copy |
| synchronizedList | List accessed by only one thread at a time (lock) |
| Vector | Same as synchronizedList — one thread at a time (synchronized methods) |

|  | CopyOnWriteArrayList | synchronizedList | Vector |
|---|---|---|---|
| Mechanism | Clone-on-write | Synchronized wrapper | Synchronized methods |
| Lock scope | Per write (copy array) | Entire list per operation | Entire vector per operation |
| Read during write | Yes (different snapshots) | No (blocked) | No (blocked) |
| Package | java.util.concurrent | java.util (wrapper) | java.util (legacy) |
| Since | Java 1.5 | Java 1.2 | Java 1.0 |

|  | CopyOnWriteArrayList | synchronizedList | Vector |
|---|---|---|---|
| Threads operating simultaneously | Multiple | One only | One only |
| Read + read concurrent | Yes | No | No |
| Read + write concurrent | Yes (snapshot isolation) | No | No |
| Write + write concurrent | Serialized internally | One at a time | One at a time |

| Scenario | CopyOnWriteArrayList | synchronizedList | Vector |
|---|---|---|---|
| Thread-1 iterates, Thread-2 adds | No CME | CME | CME |
| Iterator type | Fail-safe | Fail-fast | Fail-fast |
| Safe iteration pattern | No special sync needed | Must sync on list during iteration | Must sync on vector during iteration |

| Iterator operation | CopyOnWriteArrayList | synchronizedList | Vector |
|---|---|---|---|
| next() (read) | Yes | Yes | Yes |
| remove() | UnsupportedOperationException | Yes | Yes |
| Fail-safe / fail-fast | Fail-safe | Fail-fast | Fail-fast |

| # | Feature | CopyOnWriteArrayList | synchronizedList | Vector |
|---|---|---|---|---|
| 1 | How thread safety achieved | Every update on separate cloned copy | List locked — one thread at a time | All methods synchronized — one thread at a time |
| 2 | Threads operating at a time | Multiple threads allowed | Only one thread | Only one thread |
| 3 | Iterate + modify (another thread) | Other thread CAN modify — no CME | Other thread modifies → CME | Other thread modifies → CME |
| 4 | Iterator type | Fail-safe | Fail-fast | Fail-fast |
| 5 | Iterator remove() | Not allowed → UnsupportedOperationException | Allowed | Allowed |

| Use case | Recommended |
|---|---|
| Read-heavy, write-rare, many concurrent readers | CopyOnWriteArrayList |
| Legacy code already using Vector | Migrate to CopyOnWriteArrayList or synchronizedList |
| Need iterator remove during iteration | Vector or synchronizedList (NOT CopyOnWriteArrayList) |
| Frequent writes, many threads | NOT CopyOnWriteArrayList — copy cost too high; consider other structures |
| Simple thread-safe list, low concurrency | Collections.synchronizedList |
| Certification exam default for concurrent read + write | CopyOnWriteArrayList |

| Term | Behavior | Implementations |
|---|---|---|
| Fail-fast | Iterator detects concurrent modification → throws CME immediately | ArrayList, HashMap, HashSet, Vector, synchronizedList iterators |
| Fail-safe | Iterator works on snapshot/copy → no CME, may not see latest data | CopyOnWriteArrayList, ConcurrentHashMap, ConcurrentLinkedQueue |

| Question | Answer |
|---|---|
| COW vs Vector — both thread-safe, difference? | COW: clone on write, multiple concurrent readers; Vector: synchronized, one thread at a time |
| Why is Vector slow under load? | Every operation locks entire vector — even reads block each other |
| synchronizedList vs Vector? | Same locking model; synchronizedList wraps any List, Vector is concrete resizable array |
| Which allows iterate + concurrent modify without CME? | CopyOnWriteArrayList only |
| Which iterator supports remove()? | Vector and synchronizedList — NOT CopyOnWriteArrayList |
| What exception on COW iterator.remove()? | UnsupportedOperationException |
| When to choose CopyOnWriteArrayList? | Many reads, few writes, need concurrent iteration safety |
| Fail-safe implementations in this lecture? | CopyOnWriteArrayList |
| Fail-fast in this lecture? | Vector, synchronizedList (iterators) |

| Video 154 reason | CopyOnWriteArrayList | synchronizedList / Vector |
|---|---|---|
| Reason 1: Not thread-safe | Solves — thread-safe | Solves — thread-safe |
| Reason 2: Poor performance (whole lock) | Solves — no read lock | Same problem — whole object lock |
| Reason 3: CME on iterate+modify | Solves — fail-safe | Same problem — fail-fast iterator |

| Video | Topic |
|---|---|
| 154 | Three reasons for concurrent collections |
| 163–168 | CopyOnWriteArrayList deep dive |
| 170 | Three-way comparison table (this video) |
| 160 | HashMap vs ConcurrentHashMap (parallel map comparison) |
