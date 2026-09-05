# Video 180 — Garbage Collection Part-3: Methods for Requesting JVM to Run GC

## Video info

## Session overview

Assumes objects are already eligible for GC (Video 179). This session explains:

- Eligible ≠ immediately destroyed — GC runs when JVM decides
- You can request JVM to run GC — but no guarantee
- Two ways to request: System.gc() and Runtime.getRuntime().gc()
- Runtime class — singleton, factory method, memory queries
- Live demo creating 10,000 Date objects + free memory before/after gc()
- Exam traps: static vs instance gc(), invalid call forms
- Convenient vs recommended — System.gc() vs Runtime.gc()
Prerequisite: Video 178 (GC intro), Video 179 (eligibility rules).

## 00:06 — Eligible for GC ≠ immediate destruction

### Key rule

Once we make an object eligible for GC:

- It is NOT destroyed immediately
- Destruction happens only when JVM runs GC
- When JVM runs GC — we don't know (varies JVM to JVM)
### Partial predictability

Some JVMs may favor morning, afternoon, or evening — not guaranteed, exam-wise treat timing as unpredictable.

## 01:51 — Analogy: house cleanup lady

Daily agreement: cleanup lady comes every morning at 7:00 AM.

During the day you throw waste papers into the dustbin:

- She does NOT come after every single paper
- She collects all at once when she arrives next scheduled time
If you need urgent cleanup (15 relatives coming for lunch at 10:00):

- You call and request her to come early
- She may come — depends on relationship, health, location
- Not always guaranteed — sometimes "next morning only"
Parallel:

## 05:32 — Requesting JVM to run garbage collector

We can request JVM programmatically:

"JVM, can you please run garbage collector? Huge number of objects eligible for GC."

## 09:04 — Theory block (board notes)

Once we made an object eligible for GC:

- It may not be destroyed immediately by garbage collector
- Whenever JVM runs a GC → then only objects destroyed
- When exactly JVM runs GC → can't expect — varied from JVM to JVM
Instead of waiting until JVM runs GC on its own:

- We can request JVM to run garbage collector programmatically
- Whether JVM accepts → no guarantee
- Most of the times → JVM accepts
## 09:46 — Two ways to request JVM to run GC

### Way 1 — `System` class

System.gc();

- System class contains static method gc()
- Purpose: requesting JVM to run garbage collector
- We are NOT calling garbage collector directly — we request JVM
### Way 2 — `Runtime` class

Runtime r = Runtime.getRuntime();
r.gc();

- Java application communicates with JVM via Runtime object
- Runtime class in java.lang package
- Singleton class — only one instance per JVM
- Cannot use new Runtime() — use factory method getRuntime()
## 17:09 — Runtime class architecture

Java Application  ----communicates via---->  Runtime object  ---->  JVM
                                                    |
                                            totalMemory()
                                            freeMemory()
                                            gc()

### Creating Runtime object

Runtime r = Runtime.getRuntime();   // factory method — NOT constructor

Singleton / single-ton class: We are allowed to create only one object; constructor is private; factory method returns the instance.

### Key Runtime methods (memory + GC)

## 28:19 — Live demo: `RuntimeDemo` with 10,000 Date objects

```java
import java.util.*;

public class RuntimeDemo {
    public static void main(String[] args) {
        Runtime r = Runtime.getRuntime();

        System.out.println("Total memory: " + r.totalMemory());
        System.out.println("Free memory:  " + r.freeMemory());

        for (int i = 1; i <= 10000; i++) {
            Date d = new Date();   // create object
            // d goes out of scope each iteration → eligible for GC
        }

        System.out.println("Free memory after 10000 objects: " + r.freeMemory());

        r.gc();   // request GC

        System.out.println("Free memory after gc(): " + r.freeMemory());
    }
}
```

### Conceptual numbers (board teaching example)

Assume total = 100 bytes, initial free = 60 bytes:

### Possible free-memory values after `r.gc()` (exam reasoning)

Nothing is impossible — behavior varies by JVM. Durga Sir's live run (JDK 1.6) showed free memory greater than initial after gc() because old useless objects were also collected.

### Actual execution output (from transcript, JDK 1.6)

Numbers vary system to system — understand trend, not exact digits.

## 43:12 — Exam trap: which calls are valid?

Question: Which is a valid way to request JVM to run garbage collector?

### Static vs instance distinction

Board note:

- GC method present in System class is a static method
- GC method present in Runtime class is an instance method
## 48:57 — Convenient vs recommended

### Why Runtime.gc() is recommended internally

System.gc() implementation (from JDK source — shown in class):

```java
public final class System {
    public static void gc() {
        Runtime.getRuntime().gc();
    }
}
```

System.gc() internally calls Runtime.getRuntime().gc() only.

So calling Runtime.getRuntime().gc() directly saves one method-call hop — fractionally better performance (nanosecond scale), but technically cleaner.

Most programmers know only System.gc() — both are valid requests.

## Complete reference program

```java
import java.util.*;

public class GCRequestDemo {

    public static void main(String[] args) {
        // Way 1 — convenient
        System.gc();

        // Way 2 — recommended for performance
        Runtime rt = Runtime.getRuntime();
        System.out.println("Total: " + rt.totalMemory());
        System.out.println("Free:  " + rt.freeMemory());

        for (int i = 0; i < 10000; i++) {
            new Date();
        }

        System.out.println("Free after allocation: " + rt.freeMemory());
        rt.gc();
        System.out.println("Free after gc(): " + rt.freeMemory());
    }
}
```

## Important clarifications

### We do NOT "call" garbage collector

Correct phrasing: request JVM to run garbage collector.

Programmer → JVM → (maybe) GC runs.

### gc() vs finalize()

## OCJP exam traps (Video 180)

- Eligible object destroyed only when GC runs, not immediately
- GC timing unpredictable — varies JVM to JVM
- System.gc() — static; Runtime.gc() — instance on singleton
- Runtime.getRuntime() — only legal way to get Runtime reference
- new Runtime() — invalid (singleton)
- Runtime.gc() — invalid (non-static call on class)
- Request ≠ guarantee — JVM may ignore
- System.gc() delegates to Runtime.getRuntime().gc() internally
- Recommended: direct Runtime call; Convenient: System.gc()
- Free memory after gc() can exceed pre-allocation free memory (other garbage collected too)
## Summary

Video 180 bridges eligibility (Video 179) and actual reclamation. Objects eligible for GC wait until a GC cycle — like trash in a bin until scheduled pickup. Programmers may request early collection via `System.gc()` (static, convenient) or `Runtime.getRuntime().gc()` (instance on singleton Runtime, performance-recommended). JVM usually honors the request but is never obligated. The Runtime API also exposes `totalMemory()` and `freeMemory()` for heap inspection. The demo with 10,000 short-lived Date objects shows free memory dropping after allocation and typically rising after gc(). Exam focus: valid vs invalid call syntax and static/instance distinction.

## What's next

Finalization — finalize() method and object lifecycle before destruction (fourth GC subtopic).

End of Video 180 notes.

## Tables (placement lost -- re-place these in context)

| Field | Value |  |  |
|---|---|---|---|
| Title | Core Java With OCJP/SCJP: Garbage collection Part-3 \ | \ | The methods for requesting jvm to run GC |
| URL | https://www.youtube.com/watch?v=ECQlT9qwakA |  |  |
| Video ID | ECQlT9qwakA |  |  |
| Duration | 56m 05s |  |  |
| Position | 180 of 203 |  |  |
| Source | YouTube auto-captions (yt-dlp + node PO token) |  |  |
| Instructor | Durga Sir (OCJP/SCJP) |  |  |

| Condition | Likely GC trigger |
|---|---|
| Program running with low memory | JVM more likely to run GC |
| Exact time/schedule | Unknown — differs per JVM implementation |

| House | Java |
|---|---|
| Waste paper in bin | Object eligible for GC |
| Scheduled 7 AM cleanup | JVM's automatic GC cycle |
| Phone request for early visit | System.gc() / Runtime.gc() |
| "Maybe tomorrow" response | JVM may ignore request |

| Aspect | Detail |
|---|---|
| Request possible? | Yes |
| JVM must accept? | No guarantee |
| Practical success rate | ~99% — "most of the times JVM accepts" |

| Method | Returns | Meaning |
|---|---|---|
| totalMemory() | long | Number of bytes of total heap memory (heap size) |
| freeMemory() | long | Number of bytes of free memory currently in heap |
| gc() | void | Request JVM to run garbage collector |

| Stage | Free memory | Reason |
|---|---|---|
| Start | 60 | Baseline |
| After 10,000 Date objects | 40 | 20 bytes consumed for object creation |
| After r.gc() (if GC runs) | 60 or higher | Eligible objects destroyed |

| Value | Scenario |
|---|---|
| 30 | GC did not run; JVM used ~10 bytes internally to run program |
| 40 | GC did not run; no extra JVM overhead |
| 50 | GC ran but destroyed only some eligible objects |
| 60 | GC destroyed all 10,000 objects — back to initial free |
| 80 | GC also destroyed pre-existing useless objects in heap |

| Print statement | Approximate value |
|---|---|
| Total memory | 5173… bytes |
| Initial free memory | 4945… bytes |
| After 10,000 objects | 4714… bytes |
| After r.gc() | 5059352… bytes (greater than initial) |

| Code | Valid? | Reason |
|---|---|---|
| System.gc(); | Yes | Static gc() on System |
| Runtime.gc(); | No | gc() is instance method, not static |
| new Runtime().gc(); | No | Runtime is singleton — cannot new |
| Runtime.getRuntime().gc(); | Yes | Correct factory + instance call |

| Class | gc() method type | Call style |
|---|---|---|
| System | static | System.gc() |
| Runtime | instance | runtimeObject.gc() |

| Criterion | Winner | Explanation |
|---|---|---|
| Convenient to use | System.gc() | One call; no Runtime object needed |
| Highly recommended (performance) | Runtime.getRuntime().gc() | Avoids extra indirection |

|  | System.gc() | Runtime.getRuntime().gc() |
|---|---|---|
| Convenience | Better | Need Runtime reference first |
| Performance | One extra hop | Direct — recommended |
| Functionality | Same request to JVM | Same request to JVM |

|  | gc() | finalize() |
|---|---|---|
| Who defines | System / Runtime | Object class |
| Purpose | Request GC cycle | Last-chance cleanup before destruction |
| Covered in | This video | Finalization session |
