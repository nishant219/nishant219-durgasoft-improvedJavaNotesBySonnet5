# Video 085 — yield() and join()

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-5 || yield() || join()

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 85 of 203 |
| Series | Multi Threading · Part 5 |
| Topic | yield(), join() |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 49m 27s |
| Video ID | AZuwWOURi2Y |
| Watch | https://www.youtube.com/watch?v=AZuwWOURi2Y |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is **Multi Threading Part 5**, continuing Part 4's theme of *temporarily*
pausing a running thread (not killing it). Three `Thread` methods do that:

| # | Method | Covered here? |
|---|---|---|
| 1 | `yield()` | Yes — first half of the session |
| 2 | `join()` | Yes — second half of the session |
| 3 | `sleep()` | Already covered in an earlier session; only used for contrast |

Comparisons among `yield()`, `join()`, and `sleep()` are flagged repeatedly as
**high-frequency OCJP and interview questions** — knowing the differences, not
just each method in isolation, is the actual exam skill.

---

## 00:09 — How can we prevent thread execution?

Sir's framing: a running thread is like a person mid-task — you want to say
*"can you please pause?"*, not *"stop permanently."* Three methods give you
that temporary pause:

```java
// Three ways to temporarily prevent thread execution:
Thread.yield();     // 1
thread.join();       // 2 — called on another Thread reference
Thread.sleep(ms);    // 3 — already familiar
```

`sleep()` is the easy one — already covered. This session is about `yield()`
and `join()`.

---

## 03:18 — The public telephone booth (why `yield()` exists)

Sir's analogy is set around 1998–2000, before mobile phones: his village had
BSNL landlines only, and the nearest public telephone booth — run by a man
named **Sheshadri** — was 4–5 km away. One day a neighbour asked Sir to relay
an urgent message to the neighbour's brother, a doctor. Sir made the trip, but
the booth's phone was occupied by a "long-batting" caller endlessly repeating
four Telugu filler words (*"Avuna, Inka, Cheppu, Cheppali"* — "Really? More?
Tell. Should I tell?"). After a **four-hour wait**, Sir got his call — five to
ten seconds, message already stale — and felt "complete irritation." That, Sir
says, is exactly how a waiting thread feels.

```java
// Processor = the one telephone booth (one CPU core, one thread at a time)
// Long-batting caller = thread holding the CPU for a long run() call
// Waiting person (Sir) = thread T2 waiting for the CPU
// T2 needs 1 nanosecond of CPU; T1 holds it for "10 hours" — not recommended
```

**Processor rule: first-come-first-served (FCFS).** The JVM gives the
processor to whichever thread arrived first (`T1`). `T2` arriving a second
later must wait for `T1` to finish completely — even if `T2` needs only a
nanosecond.

**The fix Sir proposes to Sheshadri:** for known long-batting customers, check
every 10–15 minutes whether anyone is waiting; if so, pause and let them use
the phone briefly, then resume if no one (or only lower-priority callers) is
still waiting. **That algorithm is `Thread.yield()`.**

### 17:41 — `yield()` defined (formal)

```java
// yield() causes the CURRENT executing thread to PAUSE temporarily
// and give a chance to REMAINING WAITING threads of SAME PRIORITY.
//
// If NO waiting thread exists           → same thread continues.
// If ALL waiting threads are LOWER priority → same thread continues.
```

**Key phrase (memorise for exams):**

> **`yield()` causes the current executing thread to pass its execution to
> give the chance for remaining waiting threads of same priority.**

**Who needs `yield()`?** Threads that need a long time in `run()` — "long
batsmen" — should call it periodically in the middle of their work.

> ⚠️ **Modern Java — the "same priority" model does not apply to virtual threads.**
> A virtual thread's priority is fixed: `getPriority()` always returns
> `Thread.NORM_PRIORITY` (5), and `setPriority()` is silently a no-op —
> verified against the JDK's own source (`Thread.setPriority`, since Java 21):
> ```java
> public final void setPriority(int newPriority) {
>     if (newPriority > MAX_PRIORITY || newPriority < MIN_PRIORITY) {
>         throw new IllegalArgumentException();
>     }
>     if (!isVirtual()) {
>         priority(newPriority);      // platform threads only
>     }
> }
> ```
> Virtual threads are multiplexed cooperatively over a small pool of *carrier*
> platform threads (JEP 444, Java 21), not scheduled by OS/JVM priority at
> all. `Thread.yield()` still works on a virtual thread, but it means
> "unmount from my carrier and let another virtual thread run" — the
> priority-based mental model Sir is building here is specific to **platform
> threads**, which is everything this lecture (and the 6/7-era JVM) deals with.

### 22:09 — Four conclusions about `yield()`

```java
// 1. yield() passes the current thread's turn to waiting threads of the
//    SAME priority.
// 2. No waiting thread, or all waiters are lower priority → same thread
//    continues.
// 3. Multiple same-priority waiters → which one runs next is decided by the
//    scheduler. No guarantee.
// 4. When the yielded thread itself runs again is also up to the scheduler —
//    "at the mercy of the thread scheduler."
```

Scenario Sir walks through: `TX` (priority 7) is running; `T1`–`T4` (also
priority 7) are waiting. `TX` calls `Thread.yield()`. One of `T1`–`T4` gets a
turn — which one, nobody can predict — and `TX` itself re-joins the pool of
runnable threads with no guarantee of running next, even ahead of `T1`–`T4`.

### 31:15 — Complete prototype of `yield()`

```java
public static native void yield();
```

| Modifier | Meaning |
|---|---|
| `public` | Accessible everywhere |
| `static` | Called as `Thread.yield()` — no object needed |
| `native` | Not implemented in Java — implemented in the JVM/OS native layer |
| `void` | Returns nothing |
| No arguments | — |
| No checked exceptions | Unlike `sleep()` and `join()` |

> ⚠️ **Modern Java — `yield()` is no longer literally `native`.**
> Since virtual threads arrived (previewed in Java 19–20, finalised in Java 21
> via JEP 444), `Thread.yield()` is a small Java method that only *delegates*
> to native code for platform threads. Verified against JDK 26 (`javap -p
> java.lang.Thread`):
> ```java
> public static void yield();               // no longer 'native' itself
> private static native void yield0();       // the native part moved here
> ```
> The source shows why:
> ```java
> public static void yield() {
>     if (currentThread() instanceof VirtualThread vthread) {
>         vthread.tryYield();
>     } else {
>         yield0();
>     }
> }
> ```
> The OCJP-era prototype (`public static native void yield()`) is still the
> right answer for a pre-Java-19 JVM and for platform threads specifically —
> just not the literal signature you'll see if you inspect `Thread.class` on
> a current JDK.

### 32:28 — `yield()`'s impact on the thread lifecycle

Recap from the thread life-cycle lecture:

```java
// new MyThread()      → NEW / BORN state
// t.start()           → READY / RUNNABLE state
// scheduler picks CPU → RUNNING state (run() executing)
// run() completes     → TERMINATED / DEAD state
```

New transition added by `yield()`:

```java
// RUNNING thread calls Thread.yield()
//   → goes back to READY / RUNNABLE state (NOT waiting/blocked, NOT terminated)
//   → purpose: pass the CPU to same-priority waiting threads
```

| Method | From RUNNING goes to |
|---|---|
| `yield()` | READY / RUNNABLE |
| `sleep()` | WAITING / TIMED_WAITING |
| `join()` | WAITING (blocked for joining) |

Only a **running** thread can meaningfully call `Thread.yield()`.

> ❗ **Correction — there is no separate "READY" state in the actual API.**
> `java.lang.Thread.State` (introduced in Java 5) has exactly six values:
> `NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED` — confirmed by
> printing `Thread.State.values()` on a current JDK. "Running" and "ready to
> run" are **both** `RUNNABLE`; there is no JVM-visible distinction between
> them. So calling `yield()` typically does **not** change what
> `Thread.getState()` reports — it stays `RUNNABLE` before and after, even
> though the thread really did give up the processor underneath. Sir's
> RUNNING → READY diagram is the right *conceptual* OS-scheduling picture
> (and matches how the exam textbooks draw it); just don't expect
> `getState()` to expose that extra state.

### 37:42 — Demo: `ThreadYieldDemo`

```java
class MyThread extends Thread {
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println("child thread");
            Thread.yield();  // line 1 — child always yields
        }
    }
}

class ThreadYieldDemo {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        for (int i = 0; i < 10; i++) {
            System.out.println("main thread");
        }
    }
}
```

After `t.start()` there are **two** threads: main and child.

**With `Thread.yield()` active (line 1):** the child keeps giving up the CPU
to same-priority waiters. Since main has the same default priority (5), main
gets more turns and is likely to finish first.

**With line 1 commented out:** both threads run "simultaneously" (interleaved
by the scheduler). Which one finishes first is unpredictable — no guarantee
either way.

**Priority variations Sir walks through:**

```java
// Same priority (default 5/5): yield() in child → main gets more chances.
// Main has HIGHER priority: main wins with or without the child's yield()
//   — the child has no same-priority waiter to yield to anyway.
// Child has LOWER priority: main gets the CPU regardless of yield().
```

### 47:27 — Live execution

Sir compiles and runs it: with the child yielding, `main thread` lines appear
noticeably more often, and main tends to finish first — though the child can
still slip in turns whenever the scheduler chooses to hand it one.

### 49:33 — Platform support limitation

```java
// yield() hints at PREEMPTIVE scheduling: temporarily take the processor
// from the current thread and give it to another.
//
// Some OS/processor combinations support only NON-PREEMPTIVE scheduling:
// once a thread has the CPU, it runs until run() completes (or it blocks
// itself via sleep/join/etc).
//
// yield() is native and needs OS/processor cooperation — there is no
// guarantee it does anything on every platform.
```

Non-preemptive: `T1` runs to completion, then `T2`. Preemptive: `T1` can be
interrupted mid-run so `T2` gets a turn. `yield()`'s hint only means something
under preemptive scheduling.

> ⚠️ **Modern Java — this caveat is now mostly historical, but the underlying warning stands.**
> Cooperative (non-preemptive) multitasking OSes were a real concern in the
> Windows 3.x/9x and classic Mac OS era; essentially every OS a JDK targets
> today (Linux, Windows NT-family, macOS) schedules preemptively, so
> `yield()` reaching an OS that ignores it outright is now rare. What
> **hasn't** changed is Java's own advice about relying on it — the current
> `Thread.yield()` javadoc (verified against JDK 26 source) says plainly:
> *"It is rarely appropriate to use this method... The scheduler is free to
> ignore this hint."* Sir's "no guarantee" lesson is, if anything, more
> official today than it was in 2010.

### 51:42 — The one line to memorise

> **`yield()` causes the current executing thread to pass its execution to
> give the chance for remaining waiting threads of same priority.**

---

## 52:06 — join(): waiting for another thread to finish

Sir's framing: `join()` is conceptually simple, but students confuse it with
`yield()`. The purpose, and the "who calls whom" direction, are what matter.

### 52:48 — Analogy: two roommates in Miyapur

Two roommates came to Miyapur for evening classes — one for an Advanced Java
class that runs long, the other for Sir's SCJP class, which ends on time. When
the SCJP student finishes and calls his roommate, the roommate says his class
is "in full swing, don't know when it'll stop," and offers him the choice to
wait or go home alone. The best-friend answer: *"I'll wait until your class
completes — even until 2 AM, no problem."*

```java
// Friend B (finished class) = thread T1
// Friend A (still in class)  = thread T2
// B waits until A completes  → T1 calls T2.join()
```

### 55:37 — Formal definition, and who calls whom

```java
// If a thread wants to WAIT until some OTHER thread completes,
// use join().
//
// T1 wants to wait for T2 → T1 calls T2.join()   (not the other way round)
// The WAITING thread calls join() ON the TARGET thread object.
```

**The confusion Sir calls out repeatedly:** it is tempting to think the thread
being waited for calls something on the waiter. It is the reverse:

```java
Thread t1 = new MyThread();
Thread t2 = new AnotherThread();
t1.start();
t2.start();

// T1 wants to wait for T2 to finish:
t2.join();   // called BY the waiting thread ON the target Thread object

// After t2.join():
//   → the calling thread enters WAITING
//   → T2 is unaware — it just keeps running
//   → once T2 finishes, the caller becomes runnable again
```

### 62:48 — Chaining waits: the marriage-planning example

Three sequential wedding tasks, each depending on the one before it: fixing
the venue (`T1`), printing the cards (`T2`, needs the venue finalised), and
distributing the cards (`T3`, needs the cards printed). Card printing must
wait on venue fixing, and distribution must wait on printing — a chain of
`join()` calls:

```java
class VenueFixingThread extends Thread {
    public void run() { /* fix venue */ }
}

class CardPrintingThread extends Thread {
    Thread venueThread;
    CardPrintingThread(Thread venueThread) { this.venueThread = venueThread; }
    public void run() {
        try {
            venueThread.join();  // T2 waits for T1
            // print wedding cards
        } catch (InterruptedException e) { }
    }
}

class CardDistributionThread extends Thread {
    Thread printingThread;
    CardDistributionThread(Thread printingThread) { this.printingThread = printingThread; }
    public void run() {
        try {
            printingThread.join();  // T3 waits for T2
            // distribute wedding cards
        } catch (InterruptedException e) { }
    }
}
```

```java
// Venue fixing (T1)
//   ↓ T2 waits via t1.join()
// Wedding card printing (T2)
//   ↓ T3 waits via t2.join()
// Wedding card distribution (T3)
```

> ⚠️ **Modern Java — hand-chaining `join()` calls like this has a supervised alternative.**
> `java.util.concurrent.StructuredTaskScope` (first previewed in Java 21 via
> JEP 453, and still a preview API as of Java 25/26 — confirmed by compiling
> against it on a current JDK, which still requires `--enable-preview`) lets
> you fork a group of related tasks under one scope and call a single
> `scope.join()` that waits for the whole group together, propagating
> cancellation and failure as a unit instead of leaving each `join()` to fail
> independently. For a strict A-then-B-then-C pipeline like this one, plain
> sequential `join()` calls (what Sir teaches here) are still the simplest
> correct tool — structured concurrency earns its keep once you're forking
> *multiple* subtasks per stage and need them to succeed or fail together.

### 70:45 — Three (now four) overloaded prototypes

All are **`public final`** (cannot be overridden), all are **instance
methods** (called on a `Thread` object, not statically), and all
**`throws InterruptedException`** (checked).

```java
public final void join()                       throws InterruptedException  // wait forever
public final void join(long millis)             throws InterruptedException  // wait up to millis
public final void join(long millis, int nanos)  throws InterruptedException  // wait up to millis+nanos
```

Sir's phone-call framing for each: *"I'll wait until your class ends, no time
limit"* (no-arg); *"I'll wait exactly one hour, then I'm leaving"*
(`millis`); *"I'll wait 1h 23m 43s exactly, no more"* (`millis, nanos`).

**Why is `nanos` an `int` but `millis` a `long`?** Nanoseconds only ever need
to express a sub-millisecond remainder — `0` to `999,999` — which fits
comfortably in an `int`. `millis` can represent hours or days of waiting, so
it needs `long`'s range. Sir's analogy: writing ₹2,500 on a cheque as "2500,"
not "2499" rolled over from 999 — once a smaller unit would overflow, the
larger unit absorbs the carry. Concretely: `join(0, 999_999)` is the largest
legal nanosecond fraction before it would have to become `join(1, 0)`.

> ⚠️ **Modern Java — a fourth `join()` overload was added in Java 19.**
> ```java
> public final boolean join(Duration duration) throws InterruptedException
> ```
> Confirmed against the JDK 26 source (`@since 19`). It takes a
> `java.time.Duration` instead of separate `millis`/`nanos` longs, and
> **returns `boolean`** — `true` if the thread had already terminated by the
> time the wait ended, `false` otherwise — so you no longer need a follow-up
> `isAlive()` check after a timed join. The three overloads Sir teaches are
> still there and still correct; this is an additive, more ergonomic sibling.

### 77:04 — `InterruptedException`

Sir continues the roommate story: while the friend is waiting outside the
classroom, someone else (in the story, a passer-by) invites him for tea and
he abandons the wait early — that abandonment is what `InterruptedException`
models. Every `join()` overload declares it, checked, so it must be handled or
declared:

```java
// Option 1: try-catch
try {
    t.join();
} catch (InterruptedException e) {
    // handle
}

// Option 2: declare it
public static void main(String[] args) throws InterruptedException {
    t.join();
}

// Without either:
// error: unreported exception InterruptedException;
// must be caught or declared to be thrown
```

### 83:53 — Impact on the thread lifecycle

```java
// RUNNING → WAITING (blocked for joining) when t2.join() is called
//
// Three ways OUT of that waiting state:
//   1. T2 completes
//   2. the timeout expires (timed overloads only)
//   3. the waiting thread is interrupted
//
// After leaving WAITING → READY/RUNNABLE, not directly back to RUNNING —
// the scheduler still has to allocate the processor again.
```

> ❗ **Correction — a timed `join()` reports a different state than a plain one.**
> Verified on a current JDK: a thread blocked in the no-arg `t2.join()`
> reports `Thread.State.WAITING`, but a thread blocked in `t2.join(2000)` or
> `t2.join(millis, nanos)` reports **`TIMED_WAITING`** — a distinct enum
> value that has existed since `Thread.State` was introduced in Java 5, not
> a recent change. "Blocked for joining" is accurate informally for both, but
> if an exam or interview question asks for the exact `Thread.State`, the
> timed overloads are `TIMED_WAITING`, not `WAITING`.

### 91:38 — Demo: `ThreadJoinDemo` (Case 1)

> **Case 1: main thread waits for the child thread to finish.**

```java
class MyThread extends Thread {
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println("Sita thread");
            try {
                Thread.sleep(2000);  // 2 seconds after each print
            } catch (InterruptedException e) { }
        }
    }
}

class ThreadJoinDemo {
    public static void main(String[] args) throws InterruptedException {
        MyThread t = new MyThread();
        t.start();          // 2 threads: main + child
        t.join();           // line 1 — main waits for the child to finish
        for (int i = 0; i < 10; i++) {
            System.out.println("Rama thread");
        }
    }
}
```

The child ("Sita") loops 10 times, sleeping 2 seconds after each print — a
minimum of 20 seconds. `t.join()` on line 1 (executed by main, "Rama") blocks
main in `WAITING` for the entire ~20+ seconds; only once the child terminates
does main print its own 10 lines. Expected output: `Sita thread` × 10 (with
~2-second gaps), then `Rama thread` × 10.

### 97:02 — Timed `join()`: the "modern Rama" variant

Old Rama waits forever; "modern Rama" sets a 10-second deadline instead:

```java
class ThreadJoinDemoTimed {
    public static void main(String[] args) throws InterruptedException {
        MyThread t = new MyThread();
        t.start();
        t.join(10000);  // wait at most 10 seconds, not the ~20+ the child needs
        for (int i = 0; i < 10; i++) {
            System.out.println("Rama thread");
        }
    }
}
```

| Call | Behaviour |
|---|---|
| `t.join()` | Wait until the child dies — no deadline |
| `t.join(10000)` | Wait at most 10 seconds, then continue regardless |

Since the child needs ~20 seconds minimum, main's 10-second deadline expires
first: some `Sita thread` lines print, then `Rama thread` lines start
interleaving or continuing before the child is done.

### 104:57 — Case 1, wrapped up

**Line 1 (`t.join()`) commented out:** main and child run interleaved with no
guaranteed order — either could finish first, and Sir is explicit that "we
can't expect" a fixed sequence.

**Line 1 kept:** main blocks until the child fully completes, so the output
is deterministic — `Sita thread` × 10, then `Rama thread` × 10. Sir runs this
live: `main` requires `throws InterruptedException` (or a try/catch) to
compile at all, and the observed run matches the predicted order exactly:

```java
// Sita thread   (× 10, ~2 sec apart)
// Rama thread   (× 10)
```

### 106:01 — `join()` vs `yield()` vs `sleep()`, side by side

| | `yield()` | `join()` | `sleep()` |
|---|---|---|---|
| Declared as | `static` | instance, `final` | `static` |
| Effect | Current thread pauses | Current thread waits for a **specific** target thread | Current thread pauses for a **fixed time** |
| Who it yields to | Same-priority waiters | No one in particular — just waits for the target | No one — pure timer |
| Resulting state | `RUNNABLE` (no visible change) | `WAITING` (no-arg) / `TIMED_WAITING` (timed) | `TIMED_WAITING` |
| Checked exception | None | `InterruptedException` | `InterruptedException` |
| Native? | Yes, historically (see the modern-Java note above) | No — implemented in Java | Yes |
| Reliability | A hint; scheduler may ignore it | A hard block until the target finishes, the timeout expires, or an interrupt arrives | A hard block for at least the given time |

### 109:06 — Case 2 — next session

Sir ends with *"Case 2 — come later."* Case 2 (the reverse scenario, or a
child thread waiting on the main thread) is not covered in this video —
Sir picks it up in the next session.

---

## Quick reference cards

### `yield()` cheat sheet

```java
Thread.yield();
// public static void yield();   — dispatches to native yield0() for a
//                                  platform thread, or VirtualThread.tryYield()
// RUNNABLE the whole time (no distinct "ready" state in Thread.State)
// Passes the turn to same-priority waiting PLATFORM threads
// No effect if there's no equal-or-lower-priority waiter worth yielding to
// Re-entry timing: entirely scheduler-dependent
// A hint the scheduler is free to ignore (per its own javadoc)
```

### `join()` cheat sheet

```java
t2.join();                    // wait forever for t2      → WAITING
t2.join(5000);                 // wait max 5 seconds        → TIMED_WAITING
t2.join(5000, 500_000);        // 5 sec + 500,000 ns max    → TIMED_WAITING
t2.join(Duration.ofSeconds(5)); // Java 19+, returns boolean → TIMED_WAITING

// Waiting thread calls join() ON the target thread object.
// Exits WAITING/TIMED_WAITING when: target completes, timeout expires,
// or the waiter is interrupted.
// throws InterruptedException — must handle or declare.
```

---

## Exam and interview points

1. **Three ways to temporarily pause a thread:** `yield()`, `join()`,
   `sleep()` — and the exam cares about the *differences* between them, not
   just each one alone.
2. **`yield()`'s exact wording:** "causes the current executing thread to
   pass its execution to give the chance for remaining waiting threads of
   same priority." No waiters, or all lower priority → the same thread just
   continues.
3. **`yield()` gives no guarantees** — which same-priority waiter runs next,
   and when the yielding thread runs again, are both entirely up to the
   thread scheduler. Its own javadoc calls it "rarely appropriate to use."
4. **`yield()`'s complete prototype (OCJP-era answer):**
   `public static native void yield()` — no arguments, no checked exceptions.
   On a modern JDK the `native` part has moved to a private `yield0()`
   helper, but the OCJP answer above is still what to write on the exam.
5. **`join()`'s purpose:** if thread `T1` wants to wait until thread `T2`
   finishes, `T1` calls `T2.join()` — the **waiting** thread calls `join()`
   on the **target**, never the other way round.
6. **Three classic overloads, all `public final`, all instance methods, all
   `throws InterruptedException`:** `join()`, `join(long millis)`,
   `join(long millis, int nanos)`. A fourth, `join(Duration)` returning
   `boolean`, was added in Java 19.
7. **`nanos` is `int`, `millis` is `long`** — nanos only ever needs `0` to
   `999,999`; millis can represent hours or days.
8. **Lifecycle impact:** `yield()` takes RUNNING back to READY/RUNNABLE.
   `join()` takes RUNNING to WAITING (no-arg) or TIMED_WAITING (timed) —
   two different `Thread.State` values, both present since Java 5.
9. **`join()` is implemented in Java**, not native — unlike `yield()` and
   `sleep()`.
10. **Priority-based `yield()` semantics are a platform-thread concept.**
    Virtual threads (Java 21) always report `NORM_PRIORITY` and ignore
    `setPriority()`, so "pass to same-priority waiters" has nothing to act on
    there.
11. **For a strict A→B→C dependency chain**, sequential `join()` calls (as in
    the marriage-planning example) are still the right tool. Reach for
    `StructuredTaskScope` (preview since Java 21) only when you're forking
    *multiple* subtasks per stage that must succeed or fail as a group.

---

**Next:** Video 086 — join(), sleep(), and thread interruption
