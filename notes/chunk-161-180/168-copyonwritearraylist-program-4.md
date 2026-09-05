# Video 168 — Concurrent Collections Part-15: CopyOnWriteArrayList Program-4

## Video info

ASR decode notes: copy on writer list / copy and write list / copy on list / copy and grades = CopyOnWriteArrayList; co = CopyOnWriteArrayList (variable name in demo); operator = iterator; current modification exception = ConcurrentModificationException; normal list / normal error list = ArrayList.

## Session overview

This is Program-4 — the certification-critical demo explaining why the class is named CopyOnWriteArrayList and what happens when you modify the list after obtaining an iterator.

Prerequisites:

What this session covers:

- Conceptual walkthrough — list [A,B,C], open iterator, add D → new copy created, iterator still on old copy
- Certification importance — Kathy Sierra book has 3–4 questions on this exact point
- Full program — add ABC, get iterator, add D, iterate → output ABC only (not ABCD)
- Why iterator does not see D — clone-copy mechanism
- ArrayList replacement demo — same code throws CME instead
- Complete picture: CopyOnWrite behavior vs normal list behavior
What this session does NOT cover:

- Vector / synchronizedList comparison (→ Video 170)
- Performance implications of frequent writes (→ Video 163 summary)
## 00:19 — Why "CopyOnWriteArrayList"? The naming explained

### The central question

"Why the word CopyOnWriteArrayList? What is the reason?"

Answer: Every update operation will be performed on a separate cloned copy.

### Conceptual diagram (Sir's board walkthrough)

Initial state:

CopyOnWriteArrayList  →  internal array: [A, B, C]

Step 1 — Open iterator:

Iterator itr  →  points to snapshot: [A, B, C]
List object   →  still: [A, B, C]

Step 2 — Add D (update operation AFTER iterator obtained):

List object   →  NEW cloned copy: [A, B, C, D]   ← list now references this
Iterator itr  →  STILL points to OLD copy: [A, B, C]   ← unchanged

### Conclusion (exam-critical)

"After getting iterator, if you perform any update to the copy-on-write list, those updations are not available to the iterator."

Read via iterator after adding D → you get A, B, C — but NOT D.

### Why this matters for certification

Sir explicitly states:

"This is very important point for the certification exam — if you open Kathy Sierra's book, three to four questions are based on this small point only."

Memorize: Post-iterator updates are invisible to that iterator because they happen on a new clone.

## 02:43 — Full board program: Iterator snapshot demo

### Program structure

- Create CopyOnWriteArrayList
- Add A, B, C
- Obtain iterator before any further modification
- Add D after iterator obtained
- Iterate and print — expect ABC, not ABCD
```java
import java.util.*;
import java.util.concurrent.*;

public class Test {
    public static void main(String[] args) {
        CopyOnWriteArrayList<String> co = new CopyOnWriteArrayList<>();

        co.add("A");
        co.add("B");
        co.add("C");           // list = [A, B, C]

        Iterator<String> itr = co.iterator();   // snapshot taken: [A, B, C]

        co.add("D");           // NEW clone [A,B,C,D] — itr still on old [A,B,C]

        String s = "";
        while (itr.hasNext()) {
            s = s + itr.next();
        }
        System.out.println(s);  // output: ABC (NOT ABCD)
    }
}
```

### Step-by-step execution trace

### Expected output

ABC

NOT:

ABCD    ← WRONG answer on exam if you forget snapshot behavior

### Sir's board confirmation

"Compile is fine. But the answer by default we will get A B C only — but not A B C D. Clear."

## 04:16 — Certification exam traps and correct reasoning

### Common wrong answers on exam

### Correct exam logic chain

1. Iterator obtained        → snapshot frozen at [A,B,C]
2. co.add("D")              → write creates new clone [A,B,C,D]
3. Iterator not refreshed   → still reads old snapshot
4. Loop consumes A, B, C    → s = "ABC"
5. hasNext() false          → D never seen by this iterator

### Related rule from Video 163

## 04:22 — Student question: What if it were a normal ArrayList?

### Expected behavior with ArrayList

Sir asks students to guess:

"If it is the normal list, what will happen? After getting iterator, you are not allowed to modify. If you are trying to modify → immediately ConcurrentModificationException."

### ArrayList version (same structure)

```java
import java.util.*;

public class Test {
    public static void main(String[] args) {
        ArrayList<String> co = new ArrayList<>();   // ONLY CHANGE

        co.add("A");
        co.add("B");
        co.add("C");

        Iterator<String> itr = co.iterator();

        co.add("D");    // structural modification after iterator → CME

        String s = "";
        while (itr.hasNext()) {
            s = s + itr.next();
        }
        System.out.println(s);
    }
}
```

### Observed result (ArrayList)

Exception in thread "main" java.util.ConcurrentModificationException

- May not even reach System.out.println
- Fail-fast iterator detects modCount change at co.add("D") or on next itr.next()
### Three-way comparison for this exact program pattern

## 05:13 — Complete CopyOnWriteArrayList behavior summary (Programs 1–4)

### What Program-4 adds to the series

### The "CopyOnWrite" contract (exam-ready)

### Iterator refresh rule

To see post-iterator updates, you must obtain a new iterator after the modifications.

```java
Iterator<String> itr1 = co.iterator();
co.add("D");
Iterator<String> itr2 = co.iterator();   // new snapshot includes D
while (itr2.hasNext()) {
    System.out.print(itr2.next());       // ABCD
}
```

## Memory model visualization

Time ──────────────────────────────────────────────────────────►

co.add("A")  co.add("B")  co.add("C")  itr=iterator()  co.add("D")  itr.next()...
     │            │            │              │              │            │
     ▼            ▼            ▼              ▼              ▼            ▼
   [A]         [A,B]       [A,B,C]    snapshot=[A,B,C]  NEW [A,B,C,D]  reads A,B,C
                                              │              │
                                              └──── itr still here (old copy)

## OCJP / SCJP exam checklist

- [ ] Critical: After iterator obtained, updates to CopyOnWriteArrayList are NOT visible to that iterator
- [ ] Critical: Post-iterator add of D → iterate prints ABC, not ABCD
- [ ] Know why: every update creates separate cloned copy; iterator points to old copy
- [ ] Know Kathy Sierra book emphasizes this point (3–4 questions)
- [ ] ArrayList same code → ConcurrentModificationException (not ABC)
- [ ] CopyOnWriteArrayList same code → no CME, output ABC
- [ ] Distinguish Program-2 (concurrent threads) vs Program-4 (same thread, post-iterator add)
## Interview Q&A (rapid fire)

## Practice exam questions (with answers)

### Q1

```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("X");
list.add("Y");
Iterator<String> it = list.iterator();
list.add("Z");
System.out.println(it.next() + it.next());
```

Answer: XY (Z not visible to iterator)

### Q2

Same as Q1 but ArrayList instead of CopyOnWriteArrayList.

Answer: ConcurrentModificationException

### Q3

```java
CopyOnWriteArrayList<Integer> list = new CopyOnWriteArrayList<>(Arrays.asList(1, 2, 3));
Iterator<Integer> it = list.iterator();
list.add(4);
list.add(5);
int sum = 0;
while (it.hasNext()) sum += it.next();
System.out.println(sum);
```

Answer: 6 (1+2+3 — 4 and 5 not in snapshot)

## Related videos

## Summary (one paragraph)

Video 168 is Durga Sir's fourth and most certification-critical CopyOnWriteArrayList program. It explains the naming: every update operation performs on a separate cloned copy. The demo adds A, B, C to a CopyOnWriteArrayList, obtains an iterator, then adds D — but when iterating via that iterator, the output is ABC only, not ABCD, because the iterator still points to the old snapshot array while D lives on the new clone. Sir emphasizes this exact point appears in three to four Kathy Sierra certification questions. Replacing CopyOnWriteArrayList with ArrayList in the identical program yields ConcurrentModificationException instead, completing the contrast between fail-safe and fail-fast behavior. Together with Programs 2 and 3, this gives the full programmatic picture of CopyOnWriteArrayList iterator semantics.

End of Video 168 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |
|---|---|---|
| Position | 168 of 203 |  |
| Title | Core Java With OCJP/SCJP: Concurrent Collections Part-15 \ | CopyOnWriteArrayList Program-4 |
| Instructor | Durga Sir (OCJP/SCJP) |  |
| Duration | 5m 43s |  |
| Video ID | xD9t3fHLjRQ |  |
| Watch URL | https://www.youtube.com/watch?v=xD9t3fHLjRQ |  |
| Playlist | Core Java With OCJP/SCJP |  |
| Notes source | YouTube auto-captions (yt-dlp + node PO token) |  |

| Video | Topic |
|---|---|
| 163 | Why "CopyOnWrite" — every update on separate cloned copy |
| 166 | Program-2 — no CME when iterate + modify concurrently |
| 167 | Program-3 — iterator cannot remove (UnsupportedOperationException) |

| Step | Code | Internal state |
|---|---|---|
| 1 | co.add("A") | array = [A] |
| 2 | co.add("B") | array = [A, B] |
| 3 | co.add("C") | array = [A, B, C] |
| 4 | itr = co.iterator() | itr → snapshot [A, B, C] |
| 5 | co.add("D") | new clone [A,B,C,D]; itr still → [A,B,C] |
| 6 | itr.next() × 3 | reads A, B, C from snapshot |
| 7 | System.out.println(s) | prints ABC |

| Wrong thinking | Why wrong |
|---|---|
| "D was added before iteration finished, so ABCD" | Iterator holds snapshot from step 4 — D added on new copy |
| "ConcurrentModificationException" | CopyOnWriteArrayList is fail-safe — no CME |
| "Only AB printed" | All three snapshot elements are still readable |

| Iterator type | List | Post-creation modification visible? | CME? |
|---|---|---|---|
| Fail-fast | ArrayList | N/A — throws before you can read | Yes |
| Fail-safe | CopyOnWriteArrayList | No — snapshot isolation | No |

| List type | After co.add("D") post-iterator | Final output |
|---|---|---|
| CopyOnWriteArrayList | No exception | ABC |
| ArrayList | ConcurrentModificationException | No clean output |
| Vector | ConcurrentModificationException | No clean output |

| Program | Video | Proves |
|---|---|---|
| Program-1 | 165 | addIfAbsent, addAllAbsent basic operations |
| Program-2 | 166 | Concurrent iterate + modify → no CME |
| Program-3 | 167 | Iterator remove() → UnsupportedOperationException |
| Program-4 | 168 | Post-iterator add invisible to iterator → ABC not ABCD |

| Operation | Effect on list | Effect on existing iterator |
|---|---|---|
| add() before iterator | New element in list | Iterator sees it (if created after add) |
| add() after iterator | New cloned copy with element | Iterator sees old snapshot only |
| remove() after iterator | New cloned copy without element | Iterator sees old snapshot only |
| set() after iterator | New cloned copy with change | Iterator sees old snapshot only |

| Question | Answer |
|---|---|
| Why named CopyOnWriteArrayList? | Every write/update creates a separate cloned copy of the underlying array |
| Added D after getting iterator — what does iterator return? | A, B, C only — not D |
| Why doesn't iterator see D? | Iterator holds reference to snapshot array before D was added |
| Does adding D after iterator cause CME? | No — fail-safe iterator on CopyOnWriteArrayList |
| Same code with ArrayList? | ConcurrentModificationException |
| How to make iterator see D? | Create a new iterator after adding D |
| Is this point exam-important? | Yes — Sir says 3–4 Kathy Sierra questions on this |

| Video | Topic |
|---|---|
| 163 | Theory — copy-on-write mechanism, fail-safe iterator |
| 166 | Program-2 — multi-thread iterate + modify, no CME |
| 167 | Program-3 — iterator remove unsupported |
| 168 | Program-4 — post-iterator update invisible (this video) |
| 170 | CopyOnWriteArrayList vs synchronizedList vs Vector table |
