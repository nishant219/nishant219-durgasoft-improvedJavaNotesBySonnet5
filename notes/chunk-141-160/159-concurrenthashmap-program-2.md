# Video 159 — Concurrent Collections Part-6: ConcurrentHashMap Program-2

## Video info

### ASR decode corrections (auto-caption garble → intended term)

## Session overview

This lecture is the second demo program for ConcurrentHashMap. Video 158 (Program-1) demonstrated the three ConcurrentMap-specific methods. This session proves two critical runtime behaviors programmatically:

- While one thread is iterating a `ConcurrentHashMap`, other threads ARE allowed to modify the map safely — no ConcurrentModificationException.
- That concurrent modification is NOT guaranteed to be visible to the active iterator — but it will appear when you print the map after iteration completes.
What this lecture covers (~12 minutes):

- Why ConcurrentHashMap is the best choice when a huge number of threads operate on a shared map
- Program-2 — main thread iterates; child thread modifies concurrently
- Live execution — proof that ConcurrentHashMap never throws ConcurrentModificationException during concurrent iteration + modification
- Control experiment — replace ConcurrentHashMap with HashMap → immediate ConcurrentModificationException
- Iterator visibility rule — no guarantee that mid-iteration updates appear in the iterator; forward-only cursor explanation
- Teaser — next session: HashMap vs ConcurrentHashMap vs Hashtable differences
Scope note: This is a hands-on continuation of Video 157's theoretical property "ConcurrentHashMap never throws ConcurrentModificationException." Program-1 (158) covered API methods; Program-2 (this video) covers fail-safe concurrent iteration.

## 00:20 — Why ConcurrentHashMap matters (recap before the demo)

Sir restates the main objective of ConcurrentHashMap:

### When is ConcurrentHashMap the **best choice**?

If a huge number of threads are present in your application, ConcurrentHashMap is the best choice.

The specific behavior this demo proves:

Thread-1 (main)  → iterating ConcurrentHashMap (via keySet + Iterator)
Thread-2 (child) → modifying ConcurrentHashMap (put/remove) at the same time
                   ↓
                   ALLOWED — in a safe manner
                   ↓
                   ConcurrentHashMap NEVER throws ConcurrentModificationException

Sir's programmatic intention for this session:

"My intention is I have to show how is it possible for the other thread to perform modification while the first thread is iterating data."

This is not theory anymore — he will compile and run it.

## 01:37 — Program-2: Full source code (ConcurrentHashMap version)

### Imports and class structure

```java
import java.util.*;
import java.util.concurrent.*;

class MyThread extends Thread {

    static ConcurrentHashMap m = new ConcurrentHashMap();
    // static map — accessible from both main() and run()
    // Sir confirms: static vs non-static — no problem for this demo

    public void run() {
        try {
            Thread.sleep(1000);   // child thread sleeping some time
        } catch (InterruptedException e) {}
        System.out.println("Child thread updating map");
        m.put(103, "C");          // child thread updating map while main iterates
    }

    public static void main(String[] args) throws Exception {

        // ── Phase 1: only MAIN thread exists ──
        m.put(101, "A");
        m.put(102, "B");

        // ── Phase 2: start child thread → now TWO threads ──
        MyThread t = new MyThread();
        t.start();

        // ── MAIN thread: iterate map keys ──
        Set s = m.keySet();           // get only keys of the map
        Iterator itr = s.iterator();  // open iterator on keySet
        while (itr.hasNext()) {
            Object key = itr.next();
            System.out.println("Main thread iterating map and current entry is "
                + key + " " + m.get(key));
            Thread.sleep(3000);       // slow down so child can update mid-iteration
        }

        // ── After iteration: print full map ──
        System.out.println(m);
    }
}
```

### Thread timeline (step-by-step)

Sir walks through how many threads exist at each line — this is a recurring multithreading teaching pattern:

Sir's prerequisite warning (02:46):

"If you are able to understand this terminology, compulsory first you have to complete multithreading clearly and then come to these examples. I don't know multithreading — then these classes are not at all helpful for you. Remember that."

## 03:13 — What main thread does vs what child thread does

### Main thread responsibilities

- Add initial entries: 101→A, 102→B
- Start child thread
- Get keySet() — only keys (not values, not entries)
- Open Iterator on the key set
- Iterate — for each key, print key and corresponding value via m.get(key)
- After loop, print entire map m
### Child thread responsibilities (`run()`)

- Sleep briefly (gives main thread time to begin iteration)
- Update map: m.put(103, "C")
- Print "Child thread updating map"
### The core question Sir asks

"Child thread is updating map while main thread is iterating — is it allowed or not allowed?"

Answer for ConcurrentHashMap: ALLOWED.

In ConcurrentHashMap, while one thread is iterating, the remaining threads are allowed to perform any modification to the underlying map object in a safe manner.

And:

`ConcurrentHashMap` never throws `ConcurrentModificationException`.

## 04:31 — Live execution: ConcurrentHashMap output

Sir compiles and runs:

javac MyThread.java
java MyThread

### Observed console output (from the lecture)

Child thread updating map
Main thread iterating map and current entry is 102 B
Main thread iterating map and current entry is 101 A
{101=A, 102=B, 103=C}

(Exact key order in iteration may vary — HashMap/ConcurrentHashMap ordering is hash-code based, not insertion order.)

### What the output proves

Sir's conclusion:

"ConcurrentHashMap never throws ConcurrentModificationException — programmatic proof. While main thread is iterating, child thread is trying to update map — no problem, it itself is acceptable. Proper output — we are not going to get ConcurrentModificationException."

## 06:13 — Control experiment: replace ConcurrentHashMap with HashMap

Sir asks the natural follow-up:

"Suppose if I replace ConcurrentHashMap with normal HashMap — while one thread is iterating, is the remaining thread allowed to modify the underlying map object?"

Answer: NO.

### The one-line change

```java
// BEFORE (safe):
static ConcurrentHashMap m = new ConcurrentHashMap();

// AFTER (unsafe — demo only):
static HashMap m = new HashMap();
// import java.util.HashMap;  (already covered by java.util.*)
```

Everything else stays identical — same two threads, same iteration, same child put(103, "C").

### HashMap output

Main thread iterating map and current entry is ...
Child thread updating map
Exception in thread "main" java.util.ConcurrentModificationException
    at java.util.HashMap$HashIterator.next(HashMap.java:...)
    ...

Immediately when the child thread updates the map, the main thread's iterator detects structural modification and throws `ConcurrentModificationException`.

### Side-by-side comparison (exam table)

Sir's board conclusion:

"If I took normal HashMap — I got ConcurrentModificationException. If I took ConcurrentHashMap — we don't get ConcurrentModificationException. That is the advantage of concurrent collection. Concurrent collections are best suitable for multithreaded scalable applications."

### Why HashMap fails (quick internal recap)

Normal HashMap iterators are fail-fast:

- Iterator tracks an `expectedModCount`
- Any structural change (put, remove) increments `modCount`
- On next(), if modCount != expectedModCount → `ConcurrentModificationException`
ConcurrentHashMap iterators are weakly consistent — they do not use this fail-fast check, so concurrent modification during iteration is permitted.

## 07:55 — Critical second property: iterator visibility (no guarantee)

After proving CME behavior, Sir highlights a second point many students miss:

While main thread is iterating the map, child thread updated the map — correct. But is that update available to the iterator?

Answer: There is NO guarantee.

### The rule (copy to exam notes)

While one thread is iterating over a ConcurrentHashMap, if another thread performs any modification, that updation is NOT guaranteed to be available to the iterator.

This is different from "modification is not allowed." Modification is allowed — it just may not appear in the iterator's view.

### Why — forward-only cursor (Sir's bucket-by-bucket explanation)

Sir explains using internal iteration model:

ConcurrentHashMap internal buckets:

  Bucket-0   Bucket-1   Bucket-2   ...
     ↓
  Iterator cursor moves forward (one direction only — "next")
     ↓
  If update happens BEFORE cursor reaches that bucket/cell
      → iterator MAY see the new entry
  If update happens AFTER cursor already passed that position
      → iterator will NOT see the new entry

Key phrases from Sir:

- Iterator is a forward-direction cursor only (hasNext / next — no going back)
- Iteration proceeds bucket by bucket
- Timing of child thread's put() relative to cursor position determines visibility
- No guarantee either way — do not rely on seeing concurrent updates in an active iterator
### Evidence from the demo output

Sir's walkthrough:

*"Main thread iterating — current entry is 102 B and 101 A. Child already updated — but that updation you are not able to see [in the iterator]. After iterator, if you print m — that updation by default you can see."*

## 10:28 — Contrast with CopyOnWriteArrayList (forward reference)

Sir briefly contrasts with other concurrent collections:

For the remaining concurrent collections (he names CopyOnWriteArrayList), that updation will never be available to the iterator — he will explain Copy-On-Write there.

CopyOnWriteArrayList is covered in later videos (166 area). For now, remember: ConcurrentHashMap allows concurrent writes during iteration, but don't expect the iterator to reflect them.

## 10:40 — Final conclusion (Sir repeats three times)

Sir explicitly asks students to repeat this conclusion:

### The three-part rule for ConcurrentHashMap iteration

- While the main thread is iterating, the other thread is allowed to perform any modification to the map.
- That update is NOT available to the iterator — there is no guarantee.
- After iteration completes, if you print the map (System.out.println(m)), that update you CAN see.
┌─────────────────────────────────────────────────────────────┐
│  ConcurrentHashMap + Iterator during concurrent modification │
├─────────────────────────────────────────────────────────────┤
│  ✓ Modification allowed                                     │
│  ✓ No ConcurrentModificationException                       │
│  ✗ No guarantee iterator sees the update                    │
│  ✓ Map itself contains the update after iteration ends      │
└─────────────────────────────────────────────────────────────┘

## 11:27 — Next session preview

Sir closes with a teaser for Video 160:

Next: HashMap vs ConcurrentHashMap vs Hashtable — what are the differences and so on.

That session consolidates the three-way comparison started theoretically in Video 157 and proven programmatically in Videos 158–159.

## Complete comparison: HashMap vs ConcurrentHashMap (iteration scenario)

## Exam traps and interview questions

### Q1: Can I modify a ConcurrentHashMap while iterating it?

Yes. Other threads (or even the same thread in some cases) can modify the map while one thread holds an iterator. It is safe and will not throw ConcurrentModificationException.

### Q2: Will the iterator always show entries added during iteration?

No. There is no guarantee. The iterator reflects a weakly consistent view; entries added after the cursor passes may not appear.

### Q3: How do I see updates made during iteration?

Don't use the iterator for that. After iteration completes, read the map directly (m.get(key), m.containsKey(), System.out.println(m)).

### Q4: What happens if I use HashMap instead?

ConcurrentModificationException as soon as a structural modification occurs during iteration.

### Q5: Is this the same as CopyOnWriteArrayList behavior?

No. CopyOnWriteArrayList iterators operate on a snapshot — concurrent updates are never visible to the iterator. ConcurrentHashMap iterators are weakly consistent — updates might be visible depending on timing, but never guaranteed.

### Q6: Does ConcurrentHashMap allow null keys or values?

No — neither null keys nor null values (covered in Video 157). The demo uses non-null keys and values.

## Program variants summary (single file, three experiments)

Sir runs the same program skeleton three ways:

## Relationship to prior videos in this sub-series

## Key takeaways (one-page revision)

- ConcurrentHashMap objective: thread safety + performance for many threads.
- Unique iteration property: one thread may iterate while others modify — safely, without CME.
- HashMap fails this scenario — fail-fast iterator throws ConcurrentModificationException.
- Iterator visibility: concurrent updates are not guaranteed to appear in the iterator (forward-only cursor, bucket-by-bucket traversal).
- Map state after iteration: updates are in the map — print m or call get() after the loop.
- Not the same as CopyOnWriteArrayList — different iterator consistency model (deferred to later lecture).
- Prerequisite: multithreading (Thread, start(), run(), main vs child thread) must be clear first.
## Video metadata footer

End of Video 159 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Position | 159 of 203 |  |  |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-6 \ | \ | ConcurrentHashMap Program-2 |
| YouTube URL | https://www.youtube.com/watch?v=4XfL2wJYLsU |  |  |
| Video ID | 4XfL2wJYLsU |  |  |
| Duration | 11m 56s |  |  |
| Instructor | Durga Sir (OCJP/SCJP) |  |  |
| Module | Concurrent Collections (Part 6 of 7 in this sub-series) |  |  |
| Caption source | YouTube auto-generated (yt-dlp + node PO token) |  |  |
| Prerequisite | Video 157 (ConcurrentHashMap theory — locking, concurrency level, properties). Video 158 (Program-1 — putIfAbsent, conditional remove, replace). Multithreading fundamentals are mandatory — Sir explicitly warns: without clear multithreading knowledge, these concurrent collection demos will not help. |  |  |

| Heard in captions | Correct term |
|---|---|
| concatMap / concat currentMap / current hash map | ConcurrentHashMap |
| concatModificationException / currentModificationException | ConcurrentModificationException |
| concat collection / current collection | concurrent collection |
| java cand star / ut daar | `import java.util.concurrent.*` (and java.util.* for Set/Iterator) |
| legion | let us |
| old thread / l thread | child thread |
| ao of m | `System.out.println(m)` / map's toString() |
| 10 a / 10 b | 101→A, 102→B (numeric keys garbled in captions) |
| th c / child thread dead 103 c | child thread added 103→C |

| Goal | How ConcurrentHashMap delivers |
|---|---|
| Improve performance | Segment/bucket-level locking (Video 157) — not total-map lock like Hashtable |
| Achieve thread safety | Safe concurrent reads and writes without data corruption |

| Step | Code | Threads active | Who executes |
|---|---|---|---|
| 1 | m.put(101, "A"); m.put(102, "B"); | 1 — main only | Main thread adds two entries |
| 2 | t.start(); | 2 — main + child | Child begins run() asynchronously |
| 3 | keySet() → iterator() → while loop | 2 | Main iterates; child may be sleeping or updating |
| 4 | Child wakes, m.put(103, "C") | 2 | Modification while main is in the loop |
| 5 | Loop ends, System.out.println(m) | 1 or 2 | Final map state printed |

| Observation | Meaning |
|---|---|
| Program did not crash | No ConcurrentModificationException |
| Child printed "Child thread updating map" during main's loop | Concurrent modification happened |
| Iterator showed only 102→B and 101→A | Two original entries |
| 103→C NOT shown during iteration | Child's update not visible to iterator |
| Final System.out.println(m) shows 103→C | Update IS in the map after iteration |

| Scenario | Map type | Child modifies while main iterates? | Exception? |
|---|---|---|---|
| Demo 2a | ConcurrentHashMap | Yes — allowed safely | Never throws CME |
| Demo 2b | HashMap | No — not allowed | Immediately throws ConcurrentModificationException |

| Fact | Confirms |
|---|---|
| Child added 103→C during iteration | Modification succeeded |
| Iterator loop printed only 102 and 101 | 103→C not visible to iterator |
| Final System.out.println(m) included 103→C | Update is in the map; just not in iterator snapshot |

| Collection | Concurrent modification during iteration | Update visible to active iterator? |
|---|---|---|
| ConcurrentHashMap | Allowed; no CME | No guarantee (may or may not appear) |
| CopyOnWriteArrayList | Allowed; no CME | Never available to iterator (snapshot iterator) |

| # | Property | HashMap | ConcurrentHashMap |
|---|---|---|---|
| 1 | Thread-safe? | No | Yes |
| 2 | Multiple threads iterate + modify simultaneously? | No (CME on modify) | Yes |
| 3 | Throws ConcurrentModificationException during concurrent mod? | Yes | No |
| 4 | Concurrent update visible to active iterator? | N/A (throws first) | No guarantee |
| 5 | Concurrent update visible in map after iteration? | N/A | Yes |
| 6 | Iterator type | Fail-fast | Weakly consistent |
| 7 | Best for multi-threaded scalable apps? | No | Yes |

| Experiment | Map declaration | Result |
|---|---|---|
| 2a — Default (this video's main demo) | new ConcurrentHashMap() | Runs cleanly; child adds 103→C; iterator misses it; final print shows it |
| 2b — Control (HashMap) | new HashMap() | ConcurrentModificationException when child updates |
| 2c — After iteration check | ConcurrentHashMap + System.out.println(m) at end | Proves update persisted even though iterator didn't show it |

| Video | Topic | Connection to 159 |
|---|---|---|
| 156 | ConcurrentMap interface intro | Defines the interface ConcurrentHashMap implements |
| 157 | ConcurrentHashMap theory | Stated "never throws CME" — 159 proves it |
| 158 | Program-1: putIfAbsent, remove(key,val), replace | API methods demo |
| 159 | Program-2: iterate + concurrent modify | Runtime behavior demo (this video) |
| 160 | HashMap vs ConcurrentHashMap vs Hashtable | Three-way comparison (next) |

| Field | Value |
|---|---|
| Chunk | 141–160 |
| Output file | 159-concurrenthashmap-program-2 |
| Playlist position | 159 / 203 |
| Previous | Video 158 — ConcurrentHashMap Program-1 |
| Next | Video 160 — HashMap & ConcurrentHashMap comparison |
