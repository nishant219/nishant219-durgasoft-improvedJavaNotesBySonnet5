# Video 090 — Inter-Thread Communication Part-1

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-10 || Inter Thread Communication Part-1

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 90 of 203 |
| Series | Multi Threading · Part 10 |
| Topic | Inter Thread Communication Part-1 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 18m 26s |
| Video ID | Ev0mltHfYh0 |
| Watch | https://www.youtube.com/watch?v=Ev0mltHfYh0 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Part 9 finished synchronized methods, object-level and class-level locks, and
the synchronized block. Part 10 opens the next topic: **inter-thread
communication** — how two threads, both needing the same shared object,
coordinate with each other instead of guessing. Sir flags it up front as a
*thinking* topic like synchronization itself, not a "list of ways to do X"
topic, and says most students carry real gaps here going into interviews.

This part is theory, terminology, and the method signatures for `wait`,
`notify`, and `notifyAll` — plus the twist they add to the thread life cycle.
The full producer/consumer-style program that actually uses all three
together is built in later sessions.

---

## 00:06 — Topic intro: inter-thread communication

> How two threads can communicate with each other is nothing but inter-thread
> communication.

The question worth asking first is *why* two threads would ever need to talk
to each other at all — Sir answers it with a story before naming a single API
method.

## 01:40 — The post-box story (why polling is bad)

Sir's story: a call around 6 p.m. says a letter has been posted and should
arrive by the next morning. Rather than wait for a call back, he walks out to
check his personal post-box every 15–45 minutes, all night into the next
afternoon — until, around 1:45 p.m., the letter shows up. Its entire content:
*"leaving for our native place, don't call or message until I'm back."* A full
night's anxiety, spent on something one phone call could have settled.

The mapping to threads:

| Role | Behavior |
|---|---|
| Person expecting the letter | Keeps polling the post-box himself — wastes his own time every 15–45 minutes |
| Postman | Eventually performs the one update that mattered |

**Polling in code is the same waste.** A thread that repeatedly checks "is the
condition true yet?" in a loop burns CPU time for no benefit. The fix in the
story: leave a note on the box — *"eagerly waiting; please notify me when you
update"* — then go to sleep. The postman updates the box and notifies; total
contact with the box drops to two events (leave the note, come back once
notified) instead of dozens of pointless checks.

| Role | Thread | Action |
|---|---|---|
| Person expecting the letter (T1) | expects the update | calls `wait()` on the post-box object → enters the **waiting** state |
| Postman (T2) | performs the update | calls `notify()` on the same object → the waiting T1 resumes with the updated post-box |

**The advantage, stated plainly:** when threads can communicate directly,
neither one wastes system time on unnecessary waiting or polling.

## 12:00 — The core rule (board)

```java
/*
Two threads can communicate with each other
by using the wait, notify, and notifyAll methods.

The thread that is expecting an update
is responsible for calling wait()
  -> it immediately enters the waiting state.

The thread that performs the update,
after performing it,
is responsible for calling notify()
  -> the waiting thread then receives that notification
     and continues its execution with the updated data.
*/
```

## 17:19 — Why `wait`/`notify`/`notifyAll` live in `Object`, not `Thread`

**SCJP-favorite fact:** these three methods are declared in `java.lang.Object`,
never in `Thread`.

Two wrong reasons students give, and why they're wrong:

- *"Maybe `Thread` didn't have enough room for them."* Space was never the
  constraint — a class can declare as many methods as it needs.
- *"They're in `Object` so that `Thread` inherits them too."* If that were the
  design principle, every method of every class could be pushed up to `Object`
  by the same logic. It proves too much to be the real reason.

**The actual reason** is about the *target*, not the caller:

- `start()` and `join()` are called **on a `Thread` object** — nothing else
  ever needs them, so they belong in `Thread`.
- `wait()`, `notify()`, and `notifyAll()` are called **on whatever object is
  being waited on** — a post-box, a `Stack`, a `Queue`, a custom `Order`
  object, literally anything. A method that must be callable on *every* Java
  object can only live in `Object`, the common superclass of all of them.

```java
/*
wait, notify, and notifyAll are present in the Object class,
not in the Thread class,
because a thread can call these methods on any Java object —
not only on a Thread object.
*/
```

```java
class Contrast {
    public static void main(String[] args) throws InterruptedException {
        // Illustrative contrast
        Thread t = new Thread();
        t.start();   // only ever called on a Thread -> lives in Thread
        t.join();    // only ever called on a Thread -> lives in Thread

        Object postBox = new Object();
        // any object can be a wait/notify target -> lives in Object
        synchronized (postBox) {
            postBox.notify();   // after the update — see full wait() demo above
        }
    }
}
```

## 28:15 — Must own the lock: wait/notify only from a synchronized area

To call `wait`, `notify`, or `notifyAll` on an object, the calling thread must
be the **owner** of that object's lock — which means it must currently be
inside a `synchronized` method or block **for that object**.

Sir's analogy: you can put a note on *your own* post-box; putting a note on
your *neighbor's* post-box gets you into trouble. Calling these methods
outside a synchronized area throws a runtime exception —
`IllegalMonitorStateException` (the "monitor" here is the lock itself).

```java
/*
To call wait, notify, or notifyAll on any object,
the calling thread must be the owner of that object's lock,
i.e. it must be inside a synchronized area for that object.

Calling these methods outside a synchronized area
throws IllegalMonitorStateException at runtime.
*/
```

```java
class Bad {
    public void m1() {
        try {
            wait();   // not inside a synchronized area
        } catch (InterruptedException e) {
        }
    }
}

class Good {
    public synchronized void m1() {
        try {
            wait();   // OK — this thread owns Good's own object lock
        } catch (InterruptedException e) {
        }
    }
}
```

Verified: calling `new Bad().m1()` throws at the `wait()` line —

```text
Exception in thread "main" java.lang.IllegalMonitorStateException: current thread is not owner
	at java.base/java.lang.Object.wait(Object.java:...)
	at Bad.m1(Bad.java:4)
```

**Three conclusions so far:**

1. Threads communicate via `wait`, `notify`, and `notifyAll`.
2. Those methods are declared in `Object`, not `Thread`.
3. They can only be called from a synchronized area, or you get
   `IllegalMonitorStateException`.

## 35:26 — Effect of `wait`: releases the lock immediately, and only that lock

If a thread calls `wait()` on an object, two things happen, and Sir stresses
both words:

1. It **immediately** releases the lock **of that particular object**.
2. It then enters the **waiting** state.

If the thread holds ten different locks and calls `wait()` on one object, it
releases **only that one** lock — the other nine stay held. The release has
to be immediate: otherwise the updating thread (the postman) could never
acquire the lock it needs to perform the update and call `notify()`.

```java
/*
If a thread calls wait() on any object,
it immediately releases the lock of that particular object
and enters the waiting state.
*/
```

## 39:05 — Effect of `notify`: releases the lock, but maybe not immediately

Sir tells two versions of a postman's routine: one who delivers the letter
and only then shouts "post!" (update, then notify last); another who shouts
"post!" first and then still spends time finding and handing over the letter
(notify, then more work). Both patterns are common, which is exactly the
point: after calling `notify()`, the calling thread may keep doing work
*while still holding the lock* — the lock isn't released until it actually
leaves the synchronized method or block.

```java
/*
If a thread calls notify() on any object,
it releases the lock of that object,
but not necessarily immediately.
*/
```

**Except for `wait`, `notify`, and `notifyAll`, no other thread method
releases an object's lock:**

| Method | Releases the lock? |
|---|---|
| `yield()` | No |
| `join()` | No |
| `sleep()` | No |
| `wait()` | Yes — immediately, and only that object's lock |
| `notify()` | Yes — eventually, when the synchronized area is left |
| `notifyAll()` | Yes — eventually, when the synchronized area is left |

> ❗ **Correction — "`notify()` releases the lock" is slightly the wrong verb.**
> `notify()` itself releases nothing. Its `Object` javadoc says only: it marks
> one waiting thread as eligible to compete for the lock once it becomes
> free. The lock is released the normal way — when the notifying thread
> exits the `synchronized` method/block (or calls `wait()` itself). The
> practical outcome Sir describes is exactly right (the notified thread
> cannot proceed until the notifier lets go of the lock, and that can happen
> well after the `notify()` call returns); it's just `notify()`'s *caller*
> that eventually releases the lock, not the `notify()` call. Verified below:
> ```text
> waiter: eagerly waiting...
> postman: updating post-box...
> postman: still holding the lock, doing more work
> waiter: got the notification, continuing   <- only after postman's block ends
> ```

> ❗ **Correction — a woken thread must re-check its condition, not just
> "continue with the updated items."**
> `wait()` can return without ever being notified — the JVM is explicitly
> permitted to produce a *spurious wakeup* (documented in `Object.wait`'s
> javadoc), and with `notifyAll()` several threads wake up to compete for one
> update. Production code always calls `wait()` inside a loop that re-checks
> the condition:
> ```java
> synchronized (postBox) {
>     while (!updated) {     // not "if" — a loop
>         postBox.wait();
>     }
>     // safe to use the update now
> }
> ```
> The full producer/consumer program later in this series uses exactly this
> `while` form — keep it in mind as the reason the loop is there, not an
> arbitrary style choice.

## 51:38 — SCJP-style "which statement is valid?" checklist

Sir frames the material as a set of true/false options, the way SCJP would:

1. `wait()` enters waiting **without releasing any lock** → **INVALID**
2. `wait()` releases the object's lock, **but maybe not immediately** →
   **INVALID** (`wait` releases immediately; that phrasing describes
   `notify`)
3. `wait()` releases **all locks** held by the thread, then waits →
   **INVALID** (only that one object's lock)
4. `wait()` **immediately** releases the lock of **that particular object**
   and enters waiting → **VALID**
5. `notify()` **immediately** releases the lock of that object → **INVALID**
   ("immediately" is wrong for `notify`)
6. `notify()` releases the object's lock, **but maybe not immediately** →
   **VALID**

Correct answers: **4 and 6**.

**Five conclusions to cross-check against the board notes:**

1. Threads communicate via `wait` / `notify` / `notifyAll`.
2. Present in `Object`, not `Thread`.
3. Callable only from a synchronized area, else `IllegalMonitorStateException`.
4. `wait()` → immediately releases that object's lock → enters waiting.
5. `notify()` → releases that object's lock, but maybe not immediately;
   except these three methods, no other method releases a lock.

## 58:39 — Method signatures, in `Object`

```java
public final void wait() throws InterruptedException;
// wait forever until notified or interrupted

public final native void wait(long timeoutMillis) throws InterruptedException;
// wait at most timeoutMillis; resume even without a notify once time is up

public final void wait(long timeoutMillis, int nanos) throws InterruptedException;
// wait timeoutMillis (+ finer-grained timing, see correction below)

public final native void notify();

public final native void notifyAll();
```

Sir's notes on the signatures:

- `wait` is **overloaded** — three forms.
- Of the three, only `wait(long)` is `native`; `wait()` and
  `wait(long, int)` are plain Java methods that delegate to it. `notify` and
  `notifyAll` are both `native`.
- **Every `wait` method throws `InterruptedException`** — a checked
  exception — so calling `wait()` compulsorily requires a `try`/`catch` or a
  `throws` clause, or it's a compile-time error.
- `notify` and `notifyAll` throw nothing — they never put the calling thread
  into a waiting state, so there's nothing to be interrupted out of.

```java
/*
Every wait method throws InterruptedException,
a checked exception.
Whenever we use a wait method,
we must handle InterruptedException,
either with try-catch or with throws,
otherwise it is a compile-time error.
*/
```

```java
class Demo {
    public synchronized void expectUpdate() {
        // wait();   // CE if left unhandled: unreported exception InterruptedException
        try {
            wait();
        } catch (InterruptedException e) {
        }
    }
}
```

> ❗ **Correction — `wait(ms, ns)`'s nanoseconds aren't a finer clock.**
> The JDK never actually sleeps for extra nanoseconds. Its implementation
> (verified in `Object.java`) only checks whether `nanos > 0`, and if so adds
> **one whole millisecond** to `timeoutMillis` before delegating to
> `wait(long)` — the `nanos` value itself is otherwise discarded:
> ```java
> if (nanos > 0 && timeoutMillis < Long.MAX_VALUE) {
>     timeoutMillis++;
> }
> ```
> So `wait(1000, 1)` and `wait(1000, 999999)` behave identically — both wait
> up to 1001 ms. This has always been true, not a version change; "stricter
> timing" oversells what the second parameter actually buys you.

> ⚠️ **Modern Java — which `wait` overload is `native` has changed.**
> As of this recording (and up through Java 17), `wait(long)` was the one
> `native` overload, exactly as taught. Since **Java 19** (JDK-8284161, part
> of building virtual threads for **JEP 444**, finalized in **Java 21**), all
> three public `wait` overloads are plain Java methods; the actual native
> call moved to a `private` method, `wait0(long)`. Verified against a current
> JDK's `Object` class:
> ```text
> public final void wait() throws InterruptedException;
> public final void wait(long) throws InterruptedException;
> private final native void wait0(long) throws InterruptedException;
> public final void wait(long, int) throws InterruptedException;
> ```
> The extra Java-level wrapper exists so a virtual thread can unmount from
> its OS carrier thread around the native wait call. `notify()`/`notifyAll()`
> are still `native`, unchanged. The exam-era answer ("one `wait` overload is
> native") is no longer literally true of `Object`'s public API — say
> "`wait`'s native call lives in a private `wait0` since Java 19" if asked
> today.

> ⚠️ **Modern Java — `synchronized` + `wait`/`notify` used to pin virtual
> threads; Java 24 fixed it.**
> From virtual threads' introduction in **Java 21** through **Java 23**, a
> virtual thread executing inside a `synchronized` block (exactly this
> lecture's post-box pattern) could not unmount from its carrier OS thread —
> it stayed **pinned** for the whole block, including while blocked in
> `wait()`. Heavy use of `synchronized`/`wait`/`notify` under virtual threads
> could starve the small carrier-thread pool. **JEP 491 (delivered in Java
> 24)** removed this limitation: the monitor is now associated with the
> virtual thread itself rather than its carrier, so a virtual thread blocking
> in a `synchronized` region — including in `wait()` — no longer pins.
> Nothing here changes what Sir teaches about the mechanics of `wait`/
> `notify`; it only means the classic advice "avoid `synchronized` with
> virtual threads" is now obsolete on Java 24+.

> ⚠️ **Modern Java — hand-rolled `wait`/`notify` is rarely how this gets
> written today.**
> Everything in this lecture predates `java.util.concurrent` only in
> teaching order, not in the calendar — `java.util.concurrent` shipped in
> **Java 5**. Sir's own post-box (one producer, one waiting consumer,
> "notify me when you update it") is precisely what a
> `java.util.concurrent.BlockingQueue` gives you for free, without writing
> `wait`/`notify`/`synchronized` by hand: `put()` blocks the producer if full,
> `take()` blocks the consumer until an item exists, and both use `wait`/
> `notify`-equivalent signaling internally. For a one-shot "did the update
> happen yet" signal, `CountDownLatch` is the built-in analogue. This lecture
> is still worth learning in full — it's the mechanism those classes are
> built on, it's what OCJP asks about, and legacy code is full of exactly
> this pattern — but production code reaches for the higher-level type first.

## 1:06:38 — Impact on the thread life cycle

The familiar path, redrawn:

1. `new MyThread()` → **New / Born**
2. `t.start()` → **Ready / Runnable**
3. Thread scheduler allocates the processor → **Running**
4. `run()` completes → **Dead**

**New transition:** a running thread calls `wait()` — as `obj.wait()`,
`obj.wait(1000)`, or `obj.wait(1000, 100)` — and moves to **Waiting**,
immediately releasing that object's lock.

A waiting thread leaves the waiting state on any of:

- a **notification**,
- its **time expiring** (the timed overloads only), or
- being **interrupted**.

**The exam trap:** after leaving waiting, does the thread go straight to
Running? Straight to Ready/Runnable? Most students answer Ready/Runnable —
Sir says that skips a step.

Leaving `wait()` needs **two** things to actually resume execution:
notification (or timeout, or interrupt) **and** the object's lock again.
Notification by itself isn't enough if the notifier is still holding the
lock (Section 39:05 — `notify()` may not release immediately). So: a
notified thread first moves to *another* waiting state — waiting to
**reacquire the lock** — and only once it gets that lock does it become
Ready/Runnable.

```java
/*
Life cycle, wait path:

New/Born --t.start()--> Ready/Runnable
Ready/Runnable --scheduler allocates CPU--> Running
Running --run() completes--> Dead

Running --obj.wait() / wait(ms) / wait(ms,ns)--> Waiting
Waiting --notified, OR time expires, OR interrupted--> waiting for the lock
waiting for the lock --lock acquired--> Ready/Runnable --scheduler--> Running
*/
```

> ❗ **Correction — this "waiting for the lock" state already has a name:
> `Thread.State.BLOCKED`.**
> `java.lang.Thread.State` (an enum that has existed since **Java 5**, so it
> predates this recording too) already distinguishes exactly the states this
> lecture is describing informally:
>
> | `Thread.State` | Matches |
> |---|---|
> | `NEW` | "New / Born" |
> | `RUNNABLE` | "Ready/Runnable" and "Running" — Java doesn't distinguish these two |
> | `WAITING` | a thread inside `obj.wait()` with no timeout |
> | `TIMED_WAITING` | a thread inside `obj.wait(ms)` / `wait(ms, ns)` / `sleep(ms)` |
> | `BLOCKED` | exactly the "waiting to get the lock again" step Sir adds here |
> | `TERMINATED` | "Dead" |
>
> So "there's a second waiting state after notification, for the lock" isn't
> a special case invented for `wait`/`notify` — it's the same `BLOCKED` state
> a thread enters any time it's waiting to enter *any* synchronized region,
> including one it's never called `wait()` in. `Thread.getState()` returns
> this enum directly, which is a fast way to confirm the transition in a
> debugger instead of reasoning about it from a diagram.

## 1:18:09 — Close of Part-1

Theoretical foundations only: why `wait`/`notify`/`notifyAll` live in
`Object`, the synchronized-area requirement, the asymmetry between `wait`'s
immediate lock release and `notify`'s deferred one, the method signatures,
and the waiting → waiting-for-the-lock life-cycle twist. Practical
producer/consumer-style programs that actually run these together continue
in Part 2.

---

## Exam and interview points

1. **`wait`, `notify`, and `notifyAll` are declared in `Object`, not
   `Thread`** — because they must be callable on any Java object, not only on
   a `Thread`. A classic SCJP fact question.
2. **All three require the calling thread to already own the object's
   lock** — i.e. be inside a `synchronized` method or block for that object —
   or every one of them throws `IllegalMonitorStateException` at runtime.
3. **`wait()` releases the lock of that one object immediately** and enters
   the waiting state; it does not touch any other locks the thread holds.
4. **`notify()`/`notifyAll()` release the lock eventually, not
   immediately** — the notifying thread may keep running (and holding the
   lock) until it actually leaves the synchronized region. Strictly, the
   release comes from leaving the block, not from the `notify()` call itself.
5. **Every `wait` overload throws checked `InterruptedException`**;
   `notify`/`notifyAll` throw nothing.
6. **A notified thread does not go straight back to Running.** It first
   competes to reacquire the lock (`Thread.State.BLOCKED`) and only then
   becomes Ready/Runnable — a favorite "gotcha" diagram question.
7. **Always re-check the condition in a `while` loop around `wait()`**, never
   assume one notification means the wait is over — spurious wakeups are
   real, and `notifyAll()` wakes multiple competitors for one update.
8. **Modern context worth knowing for an interview past OCJP:** since Java
   19, `wait`'s native call moved to a private `wait0`; since Java 24 (JEP
   491), `synchronized` + `wait`/`notify` no longer pins a virtual thread to
   its carrier; and most new code reaches for `java.util.concurrent` types
   (`BlockingQueue`, `CountDownLatch`) that implement this exact pattern
   internally rather than hand-writing `wait`/`notify`.

---

**Next:** Video 091 — Inter-thread communication part 2
