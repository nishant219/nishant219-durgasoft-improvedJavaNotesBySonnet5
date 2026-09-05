# Video 091 — Inter-Thread Communication Part-2

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-11 || Inter Thread Communication Part-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 91 of 203 |
| Series | Multi Threading · Part 11 |
| Topic | Inter Thread Communication Part-2 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 24m 46s |
| Video ID | 2z218xjvw1M |
| Watch | https://www.youtube.com/watch?v=2z218xjvw1M |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Part 1 spent close to ninety minutes on five conclusions about `wait`,
`notify`, and `notifyAll`. Part 2 turns that theory into a working program: a
sum-of-1-to-100 demo where main thread must wait on a child thread's result,
why `sleep` and `join` are the wrong tools for "expecting an update," the
correct `wait`/`notify` program, the missed-notify forever-wait trap, timed
wait as the fix, a producer–consumer sketch, and the difference between
`notify` and `notifyAll` — closing on a lock-ownership exam trap.

---

### 00:06 — Recap of Part-1's five conclusions

1. Two threads communicate using `wait`, `notify`, `notifyAll`.
2. Those methods are declared in **`Object`**, not `Thread`.
3. Call them only from a **synchronized** area, or get a runtime
   **`IllegalMonitorStateException`**.
4. A thread that calls **`wait`** releases that object's lock **immediately**
   and enters the waiting state.
5. A thread that calls **`notify`** releases the lock too, but **may not
   immediately**. Of the classical thread methods, `wait`/`notify`/`notifyAll`
   are the only ones that release a lock at all — the waiter must free it so
   the updater can get in, and the notifier must eventually free it so the
   waiter can continue.

Next: turn the whole discussion into a runnable example.

### 02:08 — Board problem: child sums 1…100; main prints `total`

Two threads: main (exists by default) and one child, `ThreadB`. The child
updates an instance field `total` — the sum of the first 100 naturals,
\(100 \times 101 / 2 = 5050\). Main prints `b.total`.

```java
class ThreadB extends Thread {
    int total = 0;

    public void run() {
        for (int i = 1; i <= 100; i++) {
            total = total + i;
        }
        // after the loop, total should be 5050
    }
}

class ThreadA {
    public static void main(String[] args) {
        ThreadB b = new ThreadB();
        b.start();
        // two threads now: main + child
        System.out.println(b.total);
    }
}
```

The child (`run`) is responsible for **updating** `total`; main is
responsible for **printing** `b.total` — main is "expecting the update."

### 06:36 — Without wait: output is not guaranteed

Run it as written and there is **no guarantee** which value prints:

| Who gets the CPU first | Typical result |
|---|---|
| Main prints before child updates | `0` |
| Child finishes the loop, then main prints | `5050` |
| Main prints while the loop is mid-way | some intermediate value (demo runs showed `4851`, `1653`, …) |

Any value from `0` to `5050` is possible — a classic data race. The
**requirement**: always print `5050`, never `0` and never a partial sum.

### 10:46 — Attempt 1: `Thread.sleep` so main waits for the update

Idea: after `b.start()`, have main sleep long enough for the child to finish,
then print.

```java
class ThreadA {
    public static void main(String[] args) throws InterruptedException {
        ThreadB b = new ThreadB();
        b.start();
        Thread.sleep(10000); // 10 seconds
        System.out.println(b.total);   // prints 5050, almost always, for this tiny loop
    }
}
```

Classroom pushback: "what if the child doesn't finish in 10 seconds?" Sir's
answer is to not underestimate the machine — a modern CPU executes millions
of operations per nanosecond, and a 100-iteration loop finishes trivially. He
walks the sleep duration down — **10 s → 1 s → 100 ms → 10 ms → 1 ms → even
0 ms + 1 ns** — and the answer stays `5050` every time for this loop. The
point is pedagogical (how absurdly little time this loop actually needs), not
a timing guarantee for real workloads.

### 16:04 — Why sleep is not recommended for "expecting an update"

Even though sleep "works" here, for three reasons:

1. **Performance** — if the update is ready in far less than 10 s, main still
   sleeps out the rest of that time for nothing; the system runs slower than
   it needs to.
2. **Correctness** — if the calculation is large and does **not** finish
   within the chosen sleep window, main wakes early and prints an
   intermediate or wrong value again.
3. **You don't know when the update will be ready** — a fixed sleep duration
   is a guess, not a guarantee.

So: when expecting an update, calling `sleep` for a fixed time is **not
recommended**.

### 17:17 — Attempt 2: `b.join()` instead of sleep

```java
class ThreadA {
    public static void main(String[] args) throws InterruptedException {
        ThreadB b = new ThreadB();
        b.start();
        b.join();                    // main waits until the child dies
        System.out.println(b.total); // prints 5050
    }
}
```

`join()` does give `5050` here — main waits until the child **completes**
`run()`, then prints.

### 18:32 — Why join is also not recommended for "expecting an update"

`total` is ready **right after the `for` loop**. If `run()` still had another
1 crore (10 million) lines of unrelated work after that loop, `join()` would
make main wait for **all of it too** — the update was ready mid-`run()`, and
waiting until the child actually dies is pure wasted time.

The rule Sir drills:

- Expecting an update → **sleep**: not recommended.
- Expecting an update → **join**: not recommended.
- Expecting an update → **`wait`/`notify`**: **highly recommended.**

Every method has its own purpose; swapping one in for another doesn't
automatically fit the job.

### 20:15 — Correct approach sketched (still missing synchronization)

Main (expecting the update) calls `wait()` and enters waiting immediately;
the child finishes the sum, then calls `notify()`, and main resumes and
prints `total` — without waiting a single extra nanosecond after the update
is ready, and without waiting through any leftover unrelated work.

```java
class ThreadB extends Thread {
    int total = 0;

    public void run() {
        for (int i = 1; i <= 100; i++) {
            total = total + i;
        }
        // update ready -> notify the waiting main thread
        this.notify(); // WRONG place still — see next section
    }
}

class ThreadA {
    public static void main(String[] args) throws InterruptedException {
        ThreadB b = new ThreadB();
        b.start();
        b.wait(); // main expects the update — WRONG place still
        System.out.println(b.total);
    }
}
```

### 21:53 — Without `synchronized`: `IllegalMonitorStateException` (twice)

Part 1's rule: `wait`/`notify`/`notifyAll` only from a synchronized area.
Neither `wait()` nor `notify()` above is inside one — this **compiles fine**
but throws at **runtime**:

```java
class ThreadB extends Thread {
    int total = 0;

    public void run() {
        for (int i = 1; i <= 100; i++) {
            total = total + i;
        }
        this.notify();
        // Runtime: IllegalMonitorStateException, in the child thread
    }
}

class ThreadA {
    public static void main(String[] args) throws InterruptedException {
        ThreadB b = new ThreadB();
        b.start();
        b.wait();
        // Runtime: IllegalMonitorStateException, in main
        System.out.println(b.total);
    }
}
```

Running it throws **two** separate `IllegalMonitorStateException`s — one
from `wait()` in main, one from `notify()` in the child. Verified:

```text
$ java NoSync
java.lang.IllegalMonitorStateException: current thread is not owner
java.lang.IllegalMonitorStateException: current thread is not owner
```

### 23:38 — Full correct program with synchronized (the most valuable demo)

Main must hold the lock of `b` before calling `b.wait()`. The child
synchronizes on `this` — the same `b` object — before calling `notify()`.

```java
class ThreadB extends Thread {
    int total = 0;

    public void run() {
        synchronized (this) {
            System.out.println("Child thread starts calculation");
            for (int i = 1; i <= 100; i++) {
                total = total + i;
            }
            System.out.println("Child thread giving notification");
            this.notify();
        }
    }
}

class ThreadA {
    public static void main(String[] args) throws InterruptedException {
        ThreadB b = new ThreadB();
        b.start();
        synchronized (b) {
            System.out.println("Main thread calling wait method");
            b.wait();
            System.out.println("Main thread got notification");
            System.out.println(b.total);
        }
    }
}
```

**Usual sequence** (most of the time, main gets the lock of `b` first):

```text
Main thread calling wait method
Child thread starts calculation
Child thread giving notification
Main thread got notification
5050
```

Numbered the way Sir asks students to number it on the board: ① main calls
wait → ② child calculates → ③ child notifies → ④ main gets notification →
⑤ main prints `total`.

This single `b.wait()` call is not wrapped in a loop, and that is fine here —
there is exactly one condition, one `notify()`, and one waiter. The
producer–consumer version later in this same lecture needs a loop instead
(see 51:23), because there the condition ("is the queue empty?") can still be
false by the time the woken thread actually gets the lock back.

> ❗ **Correction — waiting and notifying on `b` itself is a documented
> anti-pattern, because `b` is also a `Thread`.**
> This demo works, but only because nothing else in the program calls
> `b.join()` concurrently. `Thread.join()` is implemented with exactly the
> same mechanism this lecture teaches — `synchronized (this) { wait(...); }`
> — and the JVM calls `this.notifyAll()` on a thread object the moment it
> terminates. `Thread`'s own javadoc (`@implNote` on `join(long, int)`, still
> true in the current JDK) says so explicitly:
> ```text
> For platform threads, the implementation uses a loop of this.wait
> calls conditioned on this.isAlive. As a thread terminates the
> this.notifyAll method is invoked. It is recommended that applications
> not use wait, notify, or notifyAll on Thread instances.
> ```
> Mixing your own `wait`/`notify` protocol with `join()`'s internal one on
> the same object risks a stray notification waking the wrong waiter, or
> vice versa. This has been true since Java's earliest days — it is not a
> version change. The fix costs nothing: use a private, ordinary `Object`
> (or the `ThreadB` instance's own separate lock field) as the monitor,
> and reserve `join()` for anyone who genuinely wants "wait until this
> thread dies."

### 33:22 — Lesson restated

If a thread is **expecting an update**, it should call `wait`. If a thread
**performs the update**, it should call `notify` right after. The waiting
thread then continues with the updated value.

| Approach when main expects `total` | Verdict |
|---|---|
| Print immediately after `start()` | Race: `0` / `5050` / some middle value |
| `Thread.sleep(fixed)` | Works only by luck of timing — not recommended |
| `b.join()` | Waits until the child dies, possibly over-waiting — not recommended |
| `synchronized(b) { b.wait(); }` + child's `synchronized(this) { notify(); }` | **Recommended** |

> ⚠️ **Modern Java — for exactly this "child computes one value, parent needs
> it" shape, nobody hand-writes `wait`/`notify` any more.**
> `java.util.concurrent` shipped in **Java 5** with a purpose-built type for
> this: submit a `Callable` to an `ExecutorService` and call `Future.get()` —
> it blocks until the result exists, with no `synchronized`, `wait`, or
> `notify` written by hand:
> ```java
> ExecutorService pool = Executors.newSingleThreadExecutor();
> Future<Integer> f = pool.submit(() -> {
>     int total = 0;
>     for (int i = 1; i <= 100; i++) total += i;
>     return total;
> });
> System.out.println(f.get()); // blocks until ready, then prints 5050
> pool.shutdown();
> ```
> `CompletableFuture.supplyAsync(...)` (Java 8) does the same with chaining.
> `StructuredTaskScope` (previewed since Java 21, its API still evolving —
> verified still behind `--enable-preview` on a current JDK 26) goes further,
> scoping the child thread's lifetime to the block that forked it. None of
> this makes the `wait`/`notify` mechanics obsolete to know — OCJP asks about
> them directly, they're what these higher-level types are built on, and
> legacy code is full of hand-rolled versions of exactly this pattern.

### 36:14 — Doubt: what if the child gets the chance first?

There is **no guarantee** main always gets the lock first after `b.start()`.
Sir simulates the bad ordering by making **main sleep** first, so the child
runs to completion — including its `notify()` — before main ever calls
`wait()`:

```java
class ThreadB extends Thread {
    int total = 0;

    public void run() {
        synchronized (this) {
            System.out.println("Child thread starts calculation");
            for (int i = 1; i <= 100; i++) {
                total = total + i;
            }
            System.out.println("Child thread giving notification");
            this.notify(); // nobody is waiting yet!
        }
    }
}

class ThreadA {
    public static void main(String[] args) throws InterruptedException {
        ThreadB b = new ThreadB();
        b.start();
        Thread.sleep(10000); // lazy main — child finishes + notifies while main sleeps
        synchronized (b) {
            System.out.println("Main thread calling wait method");
            b.wait(); // waits forever — the notification already happened
            System.out.println("Main thread got notification");
            System.out.println(b.total);
        }
    }
}
```

What happens: main sleeps 10 s; the child runs, calculates, notifies (to no
one), and dies; main wakes, acquires the lock, calls `wait()` — and now
**no one is left to notify it**. Main waits forever.

Sir's analogies for this, condensed: a friend who "slept 10 seconds" while
the notifier already finished is left waiting for years; a student standing
in the same spot telling his parents "I'll get a job in 2–3 months," still
saying it after years have passed. The moral in both: don't sleep through the
window in which your notification arrives — this is why "main first" is the
common case, but never a guarantee, and the reverse order is a real,
demonstrable trap.

### 48:23 — Fix for the missed-notify trap: `wait(long)` with a time period

Same parents-analogy logic: after years without a job, come home instead of
waiting forever. If there is **no guarantee** someone will notify, don't wait
forever — wait **at most** a time period, then continue regardless.

```java
class ThreadA {
    public static void main(String[] args) throws InterruptedException {
        ThreadB b = new ThreadB();
        b.start();
        Thread.sleep(10000); // still simulates a late main
        synchronized (b) {
            System.out.println("Main thread calling wait method");
            b.wait(10000); // wait at most 10 s, then continue even without a notify
            System.out.println("Main thread got notification (or timed out)");
            System.out.println(b.total);
            // with timed wait, main can continue either way;
            // total may already be 5050 because the child finished earlier
        }
    }
}
```

| Situation | Prefer |
|---|---|
| Update is compulsory; someone is guaranteed to notify | `wait()` — no args; don't wait a single extra ns after the notify |
| No guarantee a notifier exists | `wait(ms)` / `wait(ms, ns)` — continue after the timeout |

### 51:23 — Producer–consumer problem (the standard ITC example)

The "standard problem" for inter-thread communication: **producer–consumer**,
sharing one common object — a queue, like a morning post-box.

- **Producer** thread produces items **into** the queue.
- **Consumer** thread consumes items **from** the queue.
- Only one of them accesses the queue at a time, so both work inside
  `synchronized (queue)`.
- **Who expects the update?** The consumer — it calls `wait()` when the queue
  is empty.
- **Who performs the update?** The producer — it calls `notify()` after
  adding an item.

```java
// Board pseudo-structure — basic idea only, not a full buffer implementation
class ProducerThread {
    Object queue; // common object shared with the consumer

    public void produce() {
        synchronized (queue) {
            // produce an item into the queue
            queue.notify(); // after performing the update
        }
    }
}

class ConsumerThread {
    Object queue;
    boolean queueIsEmpty; // stands in for "the queue has no items"

    public void consume() throws InterruptedException {
        synchronized (queue) {
            if (queueIsEmpty) {
                queue.wait(); // expecting the update
            } else {
                // consume an item from the queue
            }
        }
    }
}
```

Flow, repeated on the board: consumer finds the queue empty → `wait()` →
waiting state; producer produces an item → producer calls `notify()` → the
waiting consumer gets the notification and continues with the new item.

> ❗ **Correction — the empty-check must be a `while` loop, not an `if`.**
> Sir's board pseudocode checks the condition once and calls `wait()` inside
> an `if`. That is unsafe even in Java 6/7: `Object.wait()`'s own contract
> permits a **spurious wakeup** — returning with no notification at all — and
> with more than one consumer, several can wake for a single item and race to
> consume it. Production code always re-checks the condition in a loop:
> ```java
> synchronized (queue) {
>     while (queueIsEmpty()) {
>         queue.wait();
>     }
>     // safe to consume now — condition re-verified after waking
> }
> ```
> This is the loop Part 1 of this series (Video 090) flagged in advance as
> "the full producer/consumer program later in this series uses exactly this
> `while` form" — this is that program.

> ⚠️ **Modern Java — this exact hand-rolled queue is what `BlockingQueue`
> replaces.**
> `java.util.concurrent.BlockingQueue` (Java 5, e.g. `ArrayBlockingQueue`,
> `LinkedBlockingQueue`) gives you `put()` that blocks the producer when full
> and `take()` that blocks the consumer when empty — no `synchronized`,
> `wait`, or `notify` written by hand, and no `if`-vs-`while` mistake to make:
> ```java
> BlockingQueue<Item> queue = new LinkedBlockingQueue<>();
> // producer:  queue.put(item);
> // consumer:  Item item = queue.take();   // blocks until available
> ```
> The board version is still worth building by hand once — it's the exact
> mechanism `BlockingQueue` is built on, and it's what OCJP and most
> interviewers ask about first.

### 1:02:30 — When to use timed vs. untimed wait (summary)

- Update is compulsory and a notifier is guaranteed → prefer **`wait()`**
  without a timeout.
- No guarantee a notifier exists → prefer **`wait` with a time period**.

That closes the "how threads communicate with `wait`/`notify`/`notifyAll`"
half of the lecture, full example plus the producer–consumer idea.

### 1:03:46 — Difference between `notify` and `notifyAll`

Top-level answer, acceptable as a first pass:

| Method | Effect on waiters of that object |
|---|---|
| `notify()` | Notifies exactly **one** waiting thread |
| `notifyAll()` | Notifies **all** waiting threads of that object |

Sir insists on the deeper, loophole-aware version below — this is where SCJP
actually tests it.

### 1:04:49 — `notify` in detail (multiple waiters)

If **10** threads are all waiting on the same object and someone calls
`notify()` once:

- **Only one** waiting thread is notified.
- The other nine stay waiting for a **further** notification.
- **Which** of the 10 gets notified? You **can't expect** a particular one —
  it depends on the **JVM's thread scheduler**. `notify()` only means
  "someone waiting for this object's update, here is a notification" — never
  "this notification is for thread T2 specifically."

```java
/*
notify():
- Gives notification to only ONE waiting thread.
- If multiple threads are waiting on the same object,
  only one is notified; the rest wait for a further notification.
- Which thread is chosen is unspecified — depends on the JVM.
*/
class DemoNotify {
    public synchronized void wakeOne() {
        notify(); // one waiter only
    }
}
```

### 1:09:40 — `notifyAll` in detail, and the "particular object" twist

Simple line: use `notifyAll()` to notify multiple waiting threads. The twist:
not "every waiting thread in the JVM" — only **every waiting thread of that
particular object**.

Board scenario: 100 threads are waiting in total — 60 called `o1.wait()`, 40
called `o2.wait()`. Someone calls `o1.notifyAll()`. Only the **60** waiting on
`o1` are notified, never the 40 on `o2`.

```java
class NotifyAllScope {
    public static void main(String[] args) throws InterruptedException {
        final Object o1 = new Object();
        final Object o2 = new Object();

        // imagine 60 threads doing: synchronized (o1) { o1.wait(); }
        // imagine 40 threads doing: synchronized (o2) { o2.wait(); }

        synchronized (o1) {
            o1.notifyAll();
            // notifies the 60 waiting on o1 only — not the 40 on o2
        }
    }
}
```

Sir's Hyderabad bus-travels analogy, condensed: a travel office has people
waiting for different buses — Vijayawada, Kakinada, and so on. When the
Vijayawada bus arrives, staff call only the Vijayawada passengers, never
everyone in the office. Notification is per **particular bus** — per
particular object.

> ⚠️ **Modern Java — a single lock with multiple `Condition`s replaces
> juggling several monitor objects for this.**
> `java.util.concurrent.locks.Lock` and `Condition` (both Java 5) let one
> `ReentrantLock` hand out several independent wait-sets — the same split
> this scenario models with two separate objects (`o1`, `o2`), but on a
> single lock, with clearer names than "the 60 on `o1`, the 40 on `o2`":
> ```java
> Lock lock = new ReentrantLock();
> Condition vijayawadaBus = lock.newCondition();
> Condition kakinadaBus   = lock.newCondition();
> // vijayawadaBus.signalAll() wakes only its own waiters — same idea, one lock
> ```
> The intrinsic-lock version taught here (multiple raw `Object`s) is still
> exactly how OCJP frames it and still works today; `Condition` is simply the
> more explicit modern equivalent when a codebase already uses `Lock`.

### 1:13:45 — Even after `notifyAll`, execution is still one-by-one

After `o1.notifyAll()`, all 60 leave "waiting for notification" and head
toward getting the lock — like 60 people running for one bus door. But the
object has **only one lock**: all 60 may be notified, but they still enter
and execute **one at a time**, because each needs the lock and only one lock
exists.

```java
/*
notifyAll():
- Notification for ALL waiting threads of THAT particular object.
- Even though many threads are notified, further execution still
  happens one by one, because each requires the lock and only one
  lock exists.
*/
class DemoNotifyAll {
    public synchronized void wakeAll() {
        notifyAll();
        // all waiters on 'this' are notified;
        // they still re-enter synchronized one at a time
    }
}
```

### 1:17:38 — Exam loophole: lock ownership must match the wait target

SCJP-style trap, using two arbitrary objects (`Stack` here is just a
convenient stand-in — the rule applies to any object):

```java
import java.util.Stack;

class LockOwnershipDemo {
    public static void main(String[] args) throws InterruptedException {
        Stack s1 = new Stack();
        Stack s2 = new Stack();

        // INVALID — owner of s1's lock, but wait() called on s2
        synchronized (s1) {
            s2.wait();
            // Runtime: IllegalMonitorStateException
            // you hold the lock of s1; wait() here needs the lock of s2
        }

        // VALID — owner of s1's lock, wait() on s1
        synchronized (s1) {
            s1.wait(); // OK
        }

        // same rule for notify / notifyAll
        synchronized (s1) {
            s1.notify(); // OK
            // s2.notify(); // would also be IllegalMonitorStateException
        }
    }
}
```

Verified — the mismatched call throws exactly as described:

```text
mismatch: java.lang.IllegalMonitorStateException: current thread is not owner
```

**Rule:** if you call `wait`/`notify`/`notifyAll` on `s1`, the calling thread
must hold the lock of `s1` — not of some other object `s2`. Mismatch means
`IllegalMonitorStateException`.

### 1:22:08 — Closing emphasis

Sir has students repeat it once more: calling `wait` on `s1` requires holding
the lock of `s1`, never `s2`; the same ownership rule governs `notify` and
`notifyAll`. Session closes here, having covered: the racy sum demo; sleep vs.
join vs. wait/notify; the full synchronized wait/notify sequence; the
missed-notify forever-wait trap plus timed wait; the producer–consumer
sketch; `notify` vs. `notifyAll` (one vs. all-of-object, then one-by-one for
the lock); and the wrong-object wait exam trap.

---

## Exam and interview points

1. **Expecting an update → `wait`/`notify`, never `sleep` or `join`.**
   `sleep` guesses a fixed duration (wrong if too short or wasteful if too
   long); `join` over-waits for anything left in `run()` after the value is
   actually ready.
2. **`wait`/`notify`/`notifyAll` require the calling thread to already own
   the target object's lock** — call on the wrong object, or from outside a
   synchronized area entirely, and it's `IllegalMonitorStateException` at
   runtime, not a compile error.
3. **A missed notification means forever-wait.** If the notifier runs (and
   calls `notify()`) before anyone is waiting, that notification is gone —
   there is no queued-up signal to collect later. The fix for "no guarantee a
   notifier exists" is `wait(ms)`, not an unbounded `wait()`.
4. **`notify()` wakes exactly one waiter of that object; which one is
   unspecified** (JVM/scheduler-dependent). **`notifyAll()`** wakes every
   waiter **of that same object only** — never waiters of a different object
   — and even then they still acquire the single lock one at a time.
5. **Never wait/notify on a `Thread` instance.** `Thread.join()` uses
   `wait`/`notifyAll` on `this` internally; the JDK's own javadoc recommends
   against mixing your own protocol into the same object. Use a plain,
   private `Object` as the monitor instead.
6. **Always re-check the wait condition in a `while` loop, not an `if`** —
   `wait()` can return via a spurious wakeup with no notification at all, and
   `notifyAll()` can wake several competitors for a single update.
7. **Modern context worth citing past OCJP:** `java.util.concurrent` (Java 5)
   supplies `Future`/`ExecutorService` for "wait on one child's result,"
   `BlockingQueue` for hand-rolled producer/consumer, and `Lock`/`Condition`
   for multiple wait-sets on one lock — the mechanics taught here are what
   all three are built from.

---

**Next:** Video 092 — Deadlock and Starvation
