# Video 157 — Concurrent Collections Part-4: ConcurrentHashMap Details

## Video info

## Session overview

This lecture is the internal-details session for ConcurrentHashMap. Video 156 covered the ConcurrentMap interface and its three special methods (putIfAbsent, conditional remove, replace). This session answers the most important interview question in the concurrent-collections module:

HashMap vs Hashtable vs ConcurrentHashMap — all three exist; what is the difference, especially with respect to thread safety and performance?

What this lecture covers (~19 minutes):

- Recap — ConcurrentHashMap implements ConcurrentMap; ConcurrentMap is child interface of Map
- Three-way comparison — HashMap (not thread-safe) vs Hashtable (thread-safe, slow) vs ConcurrentHashMap (thread-safe, fast)
- Internal locking mechanism — why Hashtable is slow and how ConcurrentHashMap fixes it
- Segment locking / bucket-level locking — the core performance idea
- Concurrency level — new term; default 16; relationship to number of buckets
- Scenarios when concurrency level ≠ initial capacity (8 vs 16, 32 vs 16)
- Theoretical properties of ConcurrentHashMap (null rules, iteration, CME)
- Five constructors and three default parameters (initial capacity, fill ratio, concurrency level)
Scope note: This session is theory + constructors only. Demo programs are deferred to Videos 158 and 159.

## 00:20 — Recap: where ConcurrentHashMap sits in the hierarchy

Map (interface)
 └── ConcurrentMap (child interface of Map)
      └── ConcurrentHashMap (implementation class)

Already covered (Video 156):

- All concurrent collections live in java.util.concurrent package.
- ConcurrentMap is the child interface of Map.
- ConcurrentHashMap is the implementation class of ConcurrentMap.
- ConcurrentMap defines three special methods in addition to all regular Map methods: putIfAbsent, conditional remove, replace.
This session's focus: Not the three special methods again — now the internal working, locking, and properties of ConcurrentHashMap.

## 00:44 — ConcurrentHashMap: thread-safe AND concurrent

Sir states two labels that apply to ConcurrentHashMap:

Interview setup question (Sir asks the class):

HashMap is there. Hashtable is there. ConcurrentHashMap is there. What is the difference?

You must understand all three before you can explain why ConcurrentHashMap exists.

## 01:11 — Level 1: HashMap — NOT thread-safe

### Behavior

On a normal HashMap object, multiple threads are allowed to operate simultaneously.

### Problem

Because there is no synchronization, there may be a chance of data inconsistency problems.

### Conclusion (board)

Normal HashMap is NOT thread-safe. Thread safety is NOT there with normal HashMap.

If your requirement is thread safety, HashMap alone is not enough — you need Hashtable or ConcurrentHashMap (or Collections.synchronizedMap()).

## 02:04 — Level 2: Hashtable — thread-safe but performance problem

### Behavior

Hashtable IS thread-safe.

But the mechanism is brutal:

At a time, only ONE thread is allowed to operate on the Hashtable object.

This applies to every operation — including read operations.

### Locking model (Hashtable)

Thread-1 trying to operate
    ↓
While Thread-1 is operating, if any other thread comes
    ↓
Other thread MUST WAIT until Thread-1 completes its operation
    ↓
At a time on the Hashtable object: only ONE thread allowed

Sir's wording: "Total map object lock" — the entire map is locked for any operation (read or write).

### Why this causes performance problems

- Requirement met: thread safety ✓
- Cost: waiting time of remaining threads increases
- Result: performance problem in multi-threaded scalable applications
Board conclusion:

We get thread safety because at a time only one thread is allowed to operate — but it increases wait time of remaining threads and creates performance problems.

## 03:32 — Level 3: ConcurrentHashMap — thread-safe WITH improved performance

To overcome Hashtable's performance issues in multi-thread scalable applications, we should go for ConcurrentHashMap.

Both Hashtable and ConcurrentHashMap are thread-safe. The difference is how thread safety is achieved and what that costs in performance.

Key interview question:

How is locking different in ConcurrentHashMap when compared with Hashtable?

This is the entire rest of the lecture.

## 03:49 — Internal structure: 16 buckets by default

### Default initial capacity

Both normal HashMap and ConcurrentHashMap have default initial capacity of 16.

That means 16 buckets internally:

Bucket index:  0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
               └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
               Total: 16 buckets (indices 0 to 15)

Sir draws buckets numbered 0 through 15 on the board.

## 04:31 — The revolutionary locking rule: reads vs writes

This is the single most important internal detail of ConcurrentHashMap.

### Read operations — NO lock required

To perform read operation, thread won't require lock.

- Any number of threads are allowed to perform read operations simultaneously.
- Multiple threads can read at the same time with zero waiting (for the lock itself).
### Write / update operations — lock required, but NOT whole-map lock

To perform write operation or update operation, thread compulsorily requires lock.

But critically:

### Side-by-side comparison (board)

HASHTABLE:
  Thread wants read  → requires total map object lock
  Thread wants write → requires total map object lock
  → Only 1 thread at a time for ANYTHING

CONCURRENTHASHMAP:
  Thread wants read  → NO lock required (unlimited concurrent reads)
  Thread wants write → requires lock of THAT BUCKET/SEGMENT only
  → Many threads can operate simultaneously on different buckets

## 05:15 — Bucket-level locking explained

### Concept

The total ConcurrentHashMap is divided into multiple parts. Each part is nothing but a bucket.

Instead of total map object lock, we use bucket-level lock.

For every part (bucket), internally a separate lock will be maintained.

### Default scenario (16 buckets, 16 locks)

Assume 16 buckets → 16 locks available.

Bucket 0 [lock₀]   Bucket 1 [lock₁]   ...   Bucket 15 [lock₁₅]

Scenario: Thread-1 is performing an update operation in Bucket 3.

- Bucket 3 is locked by Thread-1.
- All remaining threads are allowed to perform update operations simultaneously in the remaining 15 buckets.
### How many simultaneous updates?

At a time, 16 update operations can be performed simultaneously (by default), because there are 16 buckets with 16 separate locks.

Plus: any number of read operations can happen concurrently on top of that.

### Performance impact

With this different locking mechanism, relatively performance is going to be improved.

Sir also introduces the formal term: segment locking.

## 06:56 — Segment locking and concurrency level

### Segment locking

Sir says: instead of saying "bucket-level locking" every time, use segment locking.

Meaning:

Total hash map will be divided into a specific number of parts.

That number is called concurrency level.

### Concurrency level — NEW TERM (exam + interview)

Board definition:

Concurrency level = 16 means total map will be divided into 16 segments/buckets, and for each segment a separate lock will be maintained.

If a thread wants to perform any update operation in that segment, it requires the lock of that particular segment — not the total map object lock.

### Relationship between buckets and concurrency level

Most of the times, number of buckets and concurrency level both are same.

That's why we can describe it as: for every bucket, one lock (in the default case).

## 08:00 — Performance summary: Hashtable vs ConcurrentHashMap

At a time:

- Read operations on ConcurrentHashMap: any number of threads
- Update operations simultaneously: 16 threads (default concurrency level)
Wait time of threads will be reduced → overall performance of the system will be improved.

## 08:47 — When concurrency level ≠ initial capacity

Sir emphasizes: most of the time both numbers are the same, but need not be same.

### Case 1: Both equal (default) — bucket-level locking

Initial capacity = 16  →  16 buckets
Concurrency level = 16  →  16 locks
Result: For every bucket, one lock  ✓  (bucket-level locking)

### Case 2: Concurrency level = 8, initial capacity = 16

Initial capacity = 16  →  16 buckets
Concurrency level = 8   →  8 locks
Result: For every TWO buckets, ONE lock will be maintained

Lock-0 covers buckets 0,1
Lock-1 covers buckets 2,3
Lock-2 covers buckets 4,5
...
Lock-7 covers buckets 14,15

In two buckets (sharing one lock), at a time only one thread is allowed to perform update operation in that pair.

Maximum simultaneous updates = 8 (not 16).

### Case 3: Concurrency level = 32, initial capacity = 16

Initial capacity = 16  →  16 buckets
Concurrency level = 32  →  32 locks
Result: TWO locks per bucket (first half + second half of each bucket)

Sir's board explanation: in every bucket, two locks will be maintained — one for the first half, one for the second half.

### General rule

Based on concurrency level and number of buckets, the arrangement will be adjusted.

## 10:37 — Internal mechanism recap (Sir's final summary before properties)

Hashtable:

- Total map object will be locked for any operation (read or write).
ConcurrentHashMap:

- Segment lock concept available at bucket level or segment level.
- Instead of total map object lock → partial lock only.
- Read operation: no lock.
- Update operation: segment lock / bucket-level lock required.
- Default: 16 simultaneous update operations (concurrency level = 16).
Thread safety ✓ + improved performance ✓

## 12:06 — Theoretical properties / conclusions about ConcurrentHashMap

Sir now lists board points — copy these exactly for exams.

### Property 1: Underlying data structure

Underlying data structure is hash table (same as HashMap and Hashtable).

Java's ConcurrentHashMap is implemented based on hash table data structure.

### Property 2: Concurrent reads + thread-safe updates

ConcurrentHashMap allows concurrent read operations and thread-safe update operations.

- Any number of read operations can be performed concurrently.
- Multiple update operations can be performed in a safe way (up to concurrency level simultaneously).
### Property 3: Lock rules (repeated for exam)

### Property 4: Map divided into smaller portions

Concurrent update achieved by internally dividing map into smaller portions, which is defined by concurrency level.

- How many parts to divide? → concurrency level
- How many locks to maintain? → concurrency level
- Default concurrency level = 16
- By default → 16 locks maintained
### Property 5: Default simultaneous operations

ConcurrentHashMap allows any number of read operations but 16 update operations at a time by default (because concurrency level = 16).

### Property 6: Null not allowed

Null is NOT allowed for both key and value.

Same rule as Hashtable. You cannot use null for the key; you cannot use null for the value.

ConcurrentHashMap m = new ConcurrentHashMap();
m.put(null, "value");   // RuntimeException — null key not allowed
m.put("key", null);     // RuntimeException — null value not allowed

Contrast: HashMap allows one null key and multiple null values.

### Property 7: Iteration + concurrent updates — no CME

While one thread is iterating, another thread can perform update operation in the map simultaneously.

ConcurrentHashMap never throws `ConcurrentModificationException`.

Sir extends this:

Not only ConcurrentHashMap — any concurrent collection never throws ConcurrentModificationException.

This is a major difference from regular HashMap / ArrayList where fail-fast iterators throw CME if structurally modified during iteration.

### Property 8: How thread safety + performance achieved (one-line exam answer)

- Thread safety: bucket-level / segment-level lock for updates
- Performance improved: read operation lock not required; update operation uses lock of particular part (not total map object lock), defined by concurrency level
One word you must know: concurrency level

## 16:00 — Constructors: how to create ConcurrentHashMap

Sir says: before programs (next videos), let's see how to create ConcurrentHashMap and what constructors exist.

### Pattern (same as HashMap)

Like normal HashMap / HashSet — four constructors with capacity/fill-ratio variants — plus one extra parameter: concurrency level.

Total constructors: 5

Three parameters to remember:

### Constructor 1: No-arg (all defaults)

```java
ConcurrentHashMap m = new ConcurrentHashMap();
```

Creates an empty ConcurrentHashMap with:

- Default initial capacity = 16
- Default fill ratio = 0.75
- Default concurrency level = 16
### Constructor 2: Custom initial capacity

```java
ConcurrentHashMap m = new ConcurrentHashMap(int initialCapacity);
```

If default capacity 16 is not enough, customize your own capacity. Fill ratio and concurrency level still use defaults (0.75 and 16).

### Constructor 3: Custom initial capacity + fill ratio

```java
ConcurrentHashMap m = new ConcurrentHashMap(int initialCapacity, float loadFactor);
```

Customize both initial capacity and fill ratio (load factor). Concurrency level still defaults to 16.

### Constructor 4: Custom initial capacity + fill ratio + concurrency level

```java
ConcurrentHashMap m = new ConcurrentHashMap(int initialCapacity, float loadFactor, int concurrencyLevel);
```

Full customization. If you don't want default concurrency level 16, you can set 8, 30, 32, etc. based on requirement:

- How many locks do you require?
- How many parts do you want to divide your ConcurrentHashMap into?
That number = concurrency level.

### Constructor 5: From another Map (inter-conversion)

```java
ConcurrentHashMap m = new ConcurrentHashMap(Map map);
```

Provide any Map object → creates an equivalent ConcurrentHashMap with the same entries.

This type of constructor exists in all Map implementations — inter-conversion between one map type and another.

## Constructors summary table

## Master comparison: HashMap vs Hashtable vs ConcurrentHashMap

## Locking mechanism diagram (exam-ready)

┌─────────────────────────────────────────────────────────────────┐
│                    HASHTABLE (total map lock)                      │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  ONE LOCK on entire map                                    │  │
│  │  Read  → needs lock → 1 thread at a time                   │  │
│  │  Write → needs lock → 1 thread at a time                   │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              CONCURRENTHASHMAP (segment/bucket locks)            │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐     ┌────┐ ┌────┐                  │
│  │ B0 │ │ B1 │ │ B2 │ │ B3 │ ... │B14 │ │B15 │  (16 buckets)   │
│  │ L0 │ │ L1 │ │ L2 │ │ L3 │     │L14 │ │L15 │  (16 locks)     │
│  └────┘ └────┘ └────┘ └────┘     └────┘ └────┘                  │
│  Read anywhere  → NO lock needed (unlimited threads)            │
│  Write in B3    → only L3 locked; B0-B2, B4-B15 still free      │
│  Max simultaneous writes (default) = 16                          │
└─────────────────────────────────────────────────────────────────┘

## Interview questions & model answers

### Q1: What is the difference between HashMap, Hashtable, and ConcurrentHashMap?

Answer: HashMap is not thread-safe — multiple threads can operate simultaneously but data inconsistency may occur. Hashtable is thread-safe by locking the entire map object — only one thread at a time even for reads, causing performance problems. ConcurrentHashMap is thread-safe with segment/bucket-level locking — reads need no lock; writes lock only the relevant segment. Default concurrency level 16 allows 16 simultaneous updates plus unlimited concurrent reads.

### Q2: Why is ConcurrentHashMap faster than Hashtable?

Answer: Hashtable requires total map object lock for every operation including reads — only one thread at a time. ConcurrentHashMap uses segment locking — reads require no lock at all; updates lock only the specific bucket/segment. So many threads can read and write (in different segments) simultaneously.

### Q3: What is concurrency level?

Answer: Concurrency level defines how many parts the ConcurrentHashMap is internally divided into and how many locks are maintained. Default is 16. It determines the maximum number of simultaneous update operations (when concurrency level equals number of buckets). It can be customized via the 4-parameter constructor.

### Q4: Does ConcurrentHashMap allow null keys or null values?

Answer: No. Null is not allowed for both keys and values — same as Hashtable, unlike HashMap.

### Q5: Will ConcurrentHashMap throw ConcurrentModificationException during iteration?

Answer: No. While one thread iterates, another thread can update the map simultaneously. In fact, no concurrent collection throws ConcurrentModificationException.

### Q6: What are the default values for ConcurrentHashMap constructor?

Answer: Initial capacity = 16, fill ratio (load factor) = 0.75, concurrency level = 16.

### Q7: What is segment locking / bucket-level locking?

Answer: Instead of locking the entire map, ConcurrentHashMap divides the map into segments (buckets) and maintains a separate lock per segment. A thread performing an update only locks its target segment, leaving other segments available for other threads.

## Exam one-liners (copy to revision sheet)

- ConcurrentHashMap → implementation class of ConcurrentMap → child interface of Map.
- Thread-safe and concurrent collection.
- Underlying data structure: hash table.
- Read operation → no lock; any number of concurrent reads.
- Update operation → segment/bucket lock required (NOT total map object lock).
- Concurrency level (default 16) = number of internal parts = number of locks (usually).
- Default: 16 simultaneous update operations + unlimited reads.
- Null not allowed for key or value.
- Never throws `ConcurrentModificationException` (true for all concurrent collections).
- Default constructor: capacity 16, load factor 0.75, concurrency level 16.
- 5 constructors total; 4 like HashMap + concurrency level parameter + Map-copy constructor.
- Hashtable = total map lock (1 thread); ConcurrentHashMap = segment lock (16 updates + unlimited reads by default).
## Connection to adjacent videos

## Sir's closing (18:58)

Clear for all of you? That's all for this session.

Next session: programs demonstrating ConcurrentHashMap in code.

End of Video 157 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 157 of 203 |  |  |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-4 \ | \ | ConcurrentHashMap Details |
| YouTube URL | https://www.youtube.com/watch?v=IUo1Ym-Uj_I |  |  |
| Duration | 19m 14s |  |  |
| Instructor | Durga Sir (OCJP/SCJP) |  |  |
| Module | Concurrent Collections (Part 4 of 7 in this sub-series) |  |  |
| Caption source | YouTube auto-generated (yt-dlp + node PO token) |  |  |

| Label | Meaning |
|---|---|
| Thread-safe collection | Multiple threads can use it without data corruption |
| Concurrent collection | Multiple threads can operate simultaneously with good performance |

| Collection | Lock scope for update |
|---|---|
| Hashtable | Total map object lock — entire map locked |
| ConcurrentHashMap | Bucket-level lock (or segment lock) — only the relevant part locked |

| Term | Definition |
|---|---|
| Concurrency level | The number of parts the map is divided into internally; equals the number of locks maintained |
| Default value | 16 |

| Aspect | Hashtable | ConcurrentHashMap |
|---|---|---|
| Lock for any operation | Total map object lock | Segment/bucket lock for updates only |
| Read operations | Requires total map lock (1 thread) | No lock — unlimited concurrent reads |
| Update operations | 1 at a time (whole map) | Up to concurrency level simultaneous updates (default 16) |
| Performance | Not up to the mark | Too good (Sir's words) |
| Thread safety | Yes | Yes |

| Condition | Locking style |
|---|---|
| concurrency level == number of buckets | Bucket-level locking (1 lock per bucket) |
| concurrency level ≠ number of buckets | Locks distributed based on concurrency level and bucket count |

| Operation | Lock required? | Which lock? |
|---|---|---|
| Read | No | — |
| Update (put, remove, replace, etc.) | Yes, compulsory | Lock of particular part only — segment lock or bucket-level lock — NOT total map object lock |

| Parameter | Default value | Also known as |
|---|---|---|
| Initial capacity | 16 | — |
| Fill ratio | 0.75 | Load factor |
| Concurrency level | 16 | Number of segments/locks |

| # | Signature | Defaults used |
|---|---|---|
| 1 | ConcurrentHashMap() | capacity=16, loadFactor=0.75, concurrencyLevel=16 |
| 2 | ConcurrentHashMap(int initialCapacity) | loadFactor=0.75, concurrencyLevel=16 |
| 3 | ConcurrentHashMap(int initialCapacity, float loadFactor) | concurrencyLevel=16 |
| 4 | ConcurrentHashMap(int initialCapacity, float loadFactor, int concurrencyLevel) | all custom |
| 5 | ConcurrentHashMap(Map m) | copies from given map |

| Feature | HashMap | Hashtable | ConcurrentHashMap |
|---|---|---|---|
| Introduced | 1.2 | 1.0 (legacy) | 1.5 (java.util.concurrent) |
| Thread-safe? | No | Yes | Yes |
| Null key | Allowed (one) | Not allowed | Not allowed |
| Null value | Allowed | Not allowed | Not allowed |
| Lock scope | None | Entire map for every operation | Segment/bucket for updates only |
| Read concurrency | Unsynchronized (unsafe) | 1 thread (locked) | Unlimited (no lock) |
| Write concurrency | Unsynchronized (unsafe) | 1 thread (locked) | Up to concurrency level (default 16) |
| Performance (multi-thread) | Fast but unsafe | Slow (total lock) | Fast + safe |
| Underlying DS | Hash table | Hash table | Hash table |
| Default capacity | 16 | 11 | 16 |
| Default load factor | 0.75 | 0.75 | 0.75 |
| Concurrency level | N/A | N/A | 16 (default) |
| Fail-fast / CME on iteration | Yes (CME possible) | Yes (CME possible) | Never throws CME |
| Implements | Map | Map (legacy) | ConcurrentMap |

| Video | Topic |
|---|---|
| 156 | ConcurrentMap interface — putIfAbsent, conditional remove, replace |
| 157 (this) | ConcurrentHashMap internal details, locking, properties, constructors |
| 158 | ConcurrentHashMap Program-1 (demo) |
| 159 | ConcurrentHashMap Program-2 (demo) |
| 160 | HashMap & ConcurrentHashMap comparison program |
