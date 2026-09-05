# Video 166 — Concurrent Collections Part-13: CopyOnWriteArrayList Program-2

## Video info

ASR decode notes: copy-on-write a relay system / copy under a very Lister / puppy on Voyager Lister / copy on the returnees / nominee register / normally releases = ArrayList; concurrent a modification exception / current modification exception = ConcurrentModificationException; predator a ping / interpret trying to modify = iterator trying to modify; religious object = ArrayList object; smidge example = small example; change occurred = child thread; mr. Gilardi adapts = child thread updates; productive released = child thread; update oppression = update operation.

## Session overview

This is Program-2 in Durga Sir's CopyOnWriteArrayList demo series — the programmatic proof that CopyOnWriteArrayList does NOT throw `ConcurrentModificationException` when one thread iterates while another thread performs update operations.

Prerequisites (earlier videos in this module):

What this session covers:

- Learning objective — demonstrate no CME with CopyOnWriteArrayList under concurrent iterate + modify
- Full board program — MyThread extends Thread with static CopyOnWriteArrayList
- Thread timeline — main iterates, child updates via run()
- Live compile/run — output shows all elements printed, no exception
- Controlled experiment — replace CopyOnWriteArrayList with ArrayList → same code throws CME
- Side-by-side comparison — the only variable is the list implementation
What this session does NOT cover (deferred):

- Iterator snapshot behavior after update (→ Video 168, Program-4)
- Comparison with Vector / synchronizedList (→ Video 170)
- addIfAbsent / addAllAbsent details (→ Videos 164–165)
## 00:21 — Program goal: No ConcurrentModificationException with CopyOnWriteArrayList

### Core rule (from Video 163 theory — now proven in code)

In the case of CopyOnWriteArrayList:

- While one thread is iterating, the other thread is allowed to perform update operations (add, remove, set)
- There is no chance of ConcurrentModificationException
- This is the speciality of CopyOnWriteArrayList — the main reason we use concurrent collections instead of normal ArrayList in multi-threaded read-heavy scenarios
### Contrast with normal ArrayList (fail-fast)

In the case of normal ArrayList:

- While one thread is iterating, the other thread is NOT allowed to modify the underlying list object
- By mistake, if another thread tries to modify → immediate `ConcurrentModificationException`
- Iterator of ArrayList is fail-fast
### Sir's framing for this program

"This is a small example — observe very carefully what I am doing."

Target: Programmatically prove the theoretical point from Video 163 with a live demo, then flip one line (list type) to show ArrayList fails the same scenario.

## 00:76 — Program design: MyThread with static CopyOnWriteArrayList

### Design decisions (board walkthrough)

### Why static? (same explanation as Video 154)

Sir uses static so the list is shared across threads without passing references. Both main thread and child thread operate on the identical CopyOnWriteArrayList instance.

### Thread responsibilities after `t.start()`

### Critical overlap (what would cause CME on ArrayList)

Main thread:   Iterator itr = l.iterator();
               while (itr.hasNext()) { print itr.next(); }   // iterating

Child thread:  l.add("D");                                   // structural modify

On ArrayList → ConcurrentModificationException when modCount changes during iteration.

On CopyOnWriteArrayList → no exception — update happens on a separate cloned copy; iterator's snapshot is unaffected.

## 00:76 — Full board program (CopyOnWriteArrayList version)

```java
import java.util.*;
import java.util.concurrent.*;

class MyThread extends Thread {

    // Shared static CopyOnWriteArrayList — both threads use same object
    static CopyOnWriteArrayList l = new CopyOnWriteArrayList();

    public void run() {
        l.add("D");    // child thread: update operation
    }

    public static void main(String[] args) {
        l.add("A");
        l.add("B");
        l.add("C");    // list = [A, B, C]

        MyThread t = new MyThread();
        t.start();     // now 2 threads: main + child

        Iterator itr = l.iterator();
        while (itr.hasNext()) {
            System.out.println(
                "Main thread iterating list and current object is: " + itr.next());
        }
    }
}
```

### Step-by-step execution trace

- JVM starts — only main thread exists.
- Main adds "A", "B", "C" → underlying array = [A, B, C].
- Main creates MyThread t and calls t.start() → JVM spawns child thread.
- Both threads now compete for CPU:
- Main thread: obtains Iterator, enters while (itr.hasNext()) loop.
- Child thread: runs l.add("D") — CopyOnWriteArrayList creates a new cloned copy with [A, B, C, D]; original snapshot used by iterator is unchanged.
- Main continues itr.next() for each element in its snapshot — prints A, B, C (and possibly D depending on timing — Sir's demo prints without exception).
- No `ConcurrentModificationException` — program completes normally.
### Why CopyOnWriteArrayList avoids CME (internal mechanism)

### Expected console output (CopyOnWriteArrayList)

Main thread iterating list and current object is: A
Main thread iterating list and current object is: B
Main thread iterating list and current object is: C

Note: Whether "D" appears in output depends on thread scheduling. The guaranteed outcome is no exception. Sir's demo emphasizes absence of CME, not necessarily seeing D during iteration (that behavior is covered in Video 168 — iterator sees snapshot, not post-iterator updates).

## 03:28 — Compile and run (CopyOnWriteArrayList version)

### Commands (as on Sir's board)

javac MyThread.java
java MyThread

### Imports required

```java
import java.util.*;              // Iterator
import java.util.concurrent.*;   // CopyOnWriteArrayList
```

### Observed result

- Code compiles fine (javac succeeds)
- Runtime: main thread prints "Main thread iterating list and current object is: " followed by each element
- No `ConcurrentModificationException` at the end
- Child thread successfully performed update operation while main thread was iterating
### Sir's conclusion from live run

"When main thread is iterating, child thread is able to perform update operation — advantage yes, that is the speciality of CopyOnWriteArrayList."

Key takeaway: Many threads can perform update operations while another thread iterates — no CME. This is impossible with normal ArrayList without external synchronization.

## 05:09 — Controlled experiment: Replace CopyOnWriteArrayList with ArrayList

### The one-line change

Sir repeats the exact same program but replaces:

```java
static CopyOnWriteArrayList l = new CopyOnWriteArrayList();
```

with:

```java
static ArrayList l = new ArrayList();
```

Everything else stays identical — same run(), same main(), same iteration loop.

### Full ArrayList version (for comparison)

```java
import java.util.*;

class MyThread extends Thread {

    static ArrayList l = new ArrayList();   // ONLY CHANGE

    public void run() {
        l.add("D");
    }

    public static void main(String[] args) {
        l.add("A");
        l.add("B");
        l.add("C");

        MyThread t = new MyThread();
        t.start();

        Iterator itr = l.iterator();
        while (itr.hasNext()) {
            System.out.println(
                "Main thread iterating list and current object is: " + itr.next());
        }
    }
}
```

### Observed result (ArrayList version)

Main thread iterating list and current object is: A
Exception in thread "main" java.util.ConcurrentModificationException
    at java.util.ArrayList$Itr.checkForComodification(ArrayList.java:...)
    at java.util.ArrayList$Itr.next(ArrayList.java:...)
    at MyThread.main(MyThread.java:...)

- Program may print "A" (or more elements) before exception
- As soon as child thread's l.add("D") changes modCount while main's iterator is active → fail-fast detection → CME
### Side-by-side comparison table

## 06:19 — Session recap: Programmatic proof of CME difference

### Sir's closing summary

"I hope you people are clear — with respect to the program, what is the difference between normal ArrayList and CopyOnWriteArrayList with respect to ConcurrentModificationException?"

Answer structure:

- Normal ArrayList: While one thread is iterating, if another thread tries to modify → `ConcurrentModificationException`
- CopyOnWriteArrayList: While one thread is iterating, other threads can perform update operations → no CME
### Connection to Video 154 demo

Video 154 used the same `MyThread` pattern with ArrayList to introduce CME. Video 166 reuses that pattern with CopyOnWriteArrayList to show the concurrent collection solution.

## Master comparison: Iterate + Modify scenario

## OCJP / SCJP exam checklist

- [ ] Know that CopyOnWriteArrayList allows concurrent iteration + modification without CME
- [ ] Know that ArrayList iterator is fail-fast → CME on concurrent structural modification
- [ ] Know CopyOnWriteArrayList iterator is fail-safe → no CME
- [ ] Understand update-on-clone-copy is why CME does not occur
- [ ] Recognize the MyThread demo pattern from certification questions
- [ ] Know package: java.util.concurrent.CopyOnWriteArrayList
- [ ] Distinguish: CME (ArrayList) vs no CME (CopyOnWriteArrayList) with same code structure
## Interview Q&A (rapid fire)

## Related videos in CopyOnWriteArrayList series

## Summary (one paragraph)

Video 166 is Durga Sir's second CopyOnWriteArrayList program — a live, side-by-side proof of the fail-safe iterator behavior taught in Video 163. Using the familiar MyThread extends Thread pattern with a static shared list, main thread adds A/B/C, starts a child thread, and iterates with an Iterator while the child calls l.add("D"). With CopyOnWriteArrayList, the program runs to completion with no ConcurrentModificationException because updates happen on a separate cloned copy and the iterator reads from its original snapshot. Sir then replaces only the list type with ArrayList — identical code — and immediately gets ConcurrentModificationException, demonstrating fail-fast behavior. This programmatic comparison is the certification-ready answer to "what is the difference between ArrayList and CopyOnWriteArrayList regarding concurrent modification during iteration?"

End of Video 166 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |
|---|---|---|
| Position | 166 of 203 |  |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-13 \ | CopyOnWriteArrayList Program-2 |
| Instructor | Durga Sir (OCJP/SCJP) |  |
| Duration | 7m 07s |  |
| Video ID | Puk_oT7_VNU |  |
| Watch URL | https://www.youtube.com/watch?v=Puk_oT7_VNU |  |
| Playlist | Core Java With OCJP/SCJP |  |
| Notes source | YouTube auto-captions (yt-dlp + node PO token) |  |

| Video | Topic |
|---|---|
| 154 | Need of concurrent collections — Reason 3 is CME |
| 163 | CopyOnWriteArrayList properties Part-2 — fail-safe iterator, no CME during concurrent update |
| 164 | CopyOnWriteArrayList constructors & methods |
| 165 | CopyOnWriteArrayList Program-1 — addIfAbsent, addAllAbsent |

| Element | Choice | Why |
|---|---|---|
| Class name | MyThread | Same pattern as Video 154 CME demo — students already know this structure |
| Extends | Thread | Child thread runs run() method |
| Shared list | static CopyOnWriteArrayList l | Static → both main thread and child thread access the same list object |
| Child run() | l.add("D") | Child thread performs update operation while main may be iterating |
| Main main() | Add A,B,C → start child → iterate with Iterator | Main thread responsible for iteration |

| Thread | Responsibility |
|---|---|
| Main thread | Continue in main() — obtain Iterator, loop with hasNext() / next(), print each element |
| Child thread | Execute run() — call l.add("D") to update the list |

| Step | What happens |
|---|---|
| Iterator created | Iterator holds reference to current array snapshot at creation time |
| Another thread calls add("D") | New array copy created with D added; iterator still points to old snapshot |
| itr.next() called | Reads from snapshot — no modCount check that throws CME |
| Iterator type | Fail-safe — never throws CME due to concurrent modification |

| Aspect | CopyOnWriteArrayList | ArrayList |
|---|---|---|
| One thread iterates, other modifies | Allowed — no exception | Not allowed — CME |
| Iterator type | Fail-safe | Fail-fast |
| Update mechanism | Separate cloned copy | In-place modify + modCount change |
| Thread safety | Built-in (concurrent collection) | Not thread-safe |
| Same program structure | Works | Throws CME |

| Video | List type | Outcome |
|---|---|---|
| 154 | ArrayList | CME — proves the problem |
| 166 | CopyOnWriteArrayList | No CME — proves the solution |
| 166 (part 2) | ArrayList again | CME — controlled comparison |

| # | List implementation | Thread-1 (main) | Thread-2 (child) | Result |
|---|---|---|---|---|
| 1 | ArrayList | Iterate with Iterator | l.add("D") | ConcurrentModificationException |
| 2 | CopyOnWriteArrayList | Iterate with Iterator | l.add("D") | No exception — program completes |
| 3 | Vector | Iterate with Iterator | l.add("D") | ConcurrentModificationException (→ Video 170) |
| 4 | Collections.synchronizedList(ArrayList) | Iterate (unsynchronized) | l.add("D") | ConcurrentModificationException (→ Video 170) |

| Question | Answer |
|---|---|
| What happens if one thread iterates CopyOnWriteArrayList while another adds? | No ConcurrentModificationException — update on cloned copy |
| What happens with ArrayList in the same scenario? | ConcurrentModificationException — fail-fast iterator |
| Why no CME on CopyOnWriteArrayList? | Iterator works on snapshot; updates create new copy |
| Is CopyOnWriteArrayList iterator fail-fast or fail-safe? | Fail-safe |
| Best use case for CopyOnWriteArrayList? | Read-heavy, write-light multi-threaded scenarios |
| Can multiple threads update CopyOnWriteArrayList simultaneously? | Yes — each update on separate clone (with performance cost) |

| Video | Topic |
|---|---|
| 163 | CopyOnWriteArrayList properties Part-2 (theory) |
| 164 | Constructors & methods |
| 165 | Program-1 — addIfAbsent, addAllAbsent |
| 166 | Program-2 — no CME demo (this video) |
| 167 | Program-3 (iterator remove → UnsupportedOperationException) |
| 168 | Program-4 — iterator snapshot after post-iterator add |
| 170 | Comparison: CopyOnWriteArrayList vs synchronizedList vs Vector |
