# Video 096 — java.util.concurrent Package (Locks Intro)

## Video info

**Title:** Core Java With OCJP/SCJP: Multithreading Enhancement  Part- 2|| java.util.concurrent package

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 96 of 203 |
| Series | Multithreading Enhancement · Part 2 |
| Topic | java.util.concurrent package / problems with synchronized; Lock interface intro |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 45m 55s |
| Video ID | OXDYAHLftRw |
| Watch | https://www.youtube.com/watch?v=OXDYAHLftRw |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

The previous session covered the `synchronized` keyword. This one makes the
case for replacing it with `java.util.concurrent.locks`:

1. Five concrete gaps in `synchronized` — no non-blocking try, no timeout,
   no fairness control, no visibility into waiting threads, no locking across
   method boundaries.
2. The `Lock` interface and its one implementation discussed here,
   `ReentrantLock`.
3. Five `Lock` methods: `lock()`, `tryLock()`, `tryLock(long, TimeUnit)`,
   `lockInterruptibly()`, `unlock()`.
4. The `TimeUnit` enum that the timed methods take as an argument.

`ReentrantLock` itself — its constructors, fairness flag, and query methods
— is deferred to the next video.

---

## 00:07 — Topic: `java.util.concurrent` and its `locks` sub-package

Board heading: **java.util.concurrent** package, and its sub-package
**locks**. The last sessions covered the `synchronized` keyword; this one is
about the problems traditional synchronization has, and the package Sun
introduced to fix them.

## 00:38 — Two headline problems with `synchronized`

1. **Performance** goes down under contention.
2. Used carelessly, it is a direct route to **deadlock** — Sir's framing is
   that `synchronized` is "the only reason" deadlock situations appear.

To fix both, **`java.util.concurrent.locks`** — a sub-package of
`java.util.concurrent` — exists as an alternative.

> ❗ **Correction — `synchronized` is not the only path to deadlock.**
> Deadlock is a property of how *any* blocking resource is acquired, not of
> one specific keyword. Two threads taking two `ReentrantLock`s in opposite
> order deadlock exactly as badly as two threads taking two monitors in
> opposite order — the `Lock` API this lecture is building up to is just as
> capable of it. So are inconsistent-order database row locks, file locks, or
> a `wait()`/`notify()` protocol gone wrong. `synchronized` is Java's oldest
> and most common way to hit deadlock, not its only way.

## 01:17 — Problem 1: no try-for-lock without waiting

Requirement: "try for the lock; if it's available, give it to me; if not,
don't make me wait — I'll do something else instead."

With plain `synchronized` you have exactly one option: wait, for an unknown
amount of time. Sir's analogy: `synchronized` is queuing for a bus with no
way to check whether one is coming — you just wait. The flexible version
asks "is a bus available?" first, and takes an alternative route if not.

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

Lock lock = new ReentrantLock();

if (lock.tryLock()) {
    try {
        // got the lock — safe operations
    } finally {
        lock.unlock();
    }
} else {
    // lock not available — alternative operations, no waiting
}
```

`synchronized` alone cannot express this: you either get the block or you
block indefinitely waiting for it.

### 04:02 — No waiting means no question of deadlock, for this call

If a thread never waits when the lock is unavailable, *this particular
acquisition* cannot be one half of a deadlock cycle — there is no waiting
time to deadlock on. That is a real, useful property of `tryLock()`; it does
not make deadlock impossible for the program as a whole (see the correction
above) — only for code paths that exclusively use the non-blocking form.

## 04:27 — Problem 2: no fairness policy

If threads T1, T2, T3 are all waiting for a lock and it becomes free, which
one gets it with `synchronized`? Unspecified — it's up to the thread
scheduler. Sometimes you want a guarantee instead: the **longest-waiting**
thread gets it next. `synchronized` has no such option; the locks package
does, via a **fairness flag** you can set when constructing a lock (covered
with `ReentrantLock` next video).

> **Board:** If a thread releases a lock, which of the waiting threads gets
> it next — we have no control over this with `synchronized`.

## 05:41 — Problem 3: no API for the waiting-thread count

How many threads are currently waiting on a lock? With `synchronized` there
is simply no method to ask. The locks package exposes that information (also
covered next video, via `ReentrantLock`'s query methods).

## 07:38 — Problem 4: no maximum waiting time

Sometimes the requirement is "wait at most 10 minutes for the lock; if it's
still not free, move on with alternative work." `synchronized` offers no
such timeout — you wait until you get the lock, full stop, which is itself a
performance and deadlock risk if that wait is unbounded.

> **Board:** There is no way to specify a maximum waiting time for a thread
> to get the lock; the thread waits until it gets the lock, which may create
> performance problems and may cause deadlock.

## 11:08 — Problem 5: `synchronized` cannot span multiple methods

`synchronized` applies at exactly two granularities: an entire method, or a
block inside one method. Across *multiple* methods there is no clean way to
say "acquire here, release over there."

Scenario: acquire the lock partway through `m1()`, hold it through part of
`m2()` (which `m1()` calls), then release it mid-`m2()` so the remaining
work in `m2()` is open to other threads. The locks package expresses this
directly, because `lock()` and `unlock()` are just method calls that can sit
anywhere:

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class Shared {
    private final Lock lock = new ReentrantLock();

    void m1() {
        lock.lock();      // acquired here, inside m1
        m2();
    }

    void m2() {
        // ... work that still needs the lock ...
        lock.unlock();     // released here, inside m2 — other threads may now proceed
        // ... work that no longer needs the lock ...
    }
}
```

> **Board:** We are compelled to use `synchronized` either at method level or
> within a method, and it is not possible to use it across multiple methods.

### 14:28 — Five problems → `java.util.concurrent.locks` arrives in 1.5

| # | Problem with `synchronized` |
|---|---|
| 1 | No flexibility to try for a lock without waiting |
| 2 | No way to specify a maximum waiting time |
| 3 | No control over which waiting thread gets a released lock |
| 4 | No API to list or count waiting threads |
| 5 | Cannot hold a lock across multiple methods, only within one |

To fix all five, Sun introduced **`java.util.concurrent.locks`** in **Java
1.5**. The package is not only a `synchronized` replacement — it also adds
enhancements for finer control over concurrency generally.

> ⚠️ **Modern Java — the locks package grew a third implementation.**
> In 1.5 the package offered `ReentrantLock` and `ReentrantReadWriteLock`.
> **Java 8** added **`StampedLock`**, which supports an *optimistic* read
> mode: a reader can proceed without blocking writers at all and only pay the
> cost of re-checking (or falling back to a normal read lock) if a write
> actually happened concurrently. It's a niche tool for read-heavy,
> low-contention data, not a `ReentrantLock` replacement — but it's the
> answer if an interviewer asks what's in `java.util.concurrent.locks` beyond
> what this lecture covers.

## 16:42 — What you need: the `Lock` interface and `ReentrantLock`

Two things to know for this topic:

- the interface: **`Lock`**
- its implementation covered here: **`ReentrantLock`**

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

Lock lock = new ReentrantLock();
```

## 17:32 — A `Lock` object vs the implicit lock

A `Lock` implementation object is conceptually the same as the **implicit
lock** a thread acquires entering a `synchronized` method or block — except
it is created **explicitly**, and it supports more operations than the
implicit lock does (how many threads are waiting, releasing on demand
instead of only at block exit, and so on).

> **Board:** A lock object is similar to the implicit lock acquired by a
> thread to execute a synchronized method or synchronized block. Lock
> implementations provide more extensive operations than traditional
> implicit locks.

> ⚠️ **Modern Java — the two kinds of lock now differ in how virtual threads
> treat them.**
> Java 21 (JEP 444) added virtual threads. From 21 through 23, a virtual
> thread that blocked *inside a `synchronized` block* was **pinned** to its
> carrier platform thread instead of being unmounted — so a long or
> contended `synchronized` section could tie up a carrier and hurt
> scalability under heavy virtual-thread use, in a way that blocking on a
> `java.util.concurrent.locks.Lock` did not. **Java 24** (JEP 491) removed
> most of that pinning, so this specific gap between the implicit lock and
> the explicit `Lock` API has narrowed since. It's still a reason some
> concurrent code prefers `Lock` on older runtimes, and still worth knowing
> the JEP number if it comes up.

## 19:56 — `void lock()`

```java
void lock();
```

- Lock **available** → the current thread acquires it immediately and
  continues.
- Lock **not available** → wait until it becomes available.

Exactly the same behavior as the traditional `synchronized` keyword: wait
forever if you must.

## 23:08 — `boolean tryLock()`

Sir's framing, condensed: most people who have an idea never try it; of
those who try, most give up at the first setback — like the choppy water
near the shore, calm again further out. The moral for `tryLock()`: just try
once.

```java
boolean tryLock();
```

- Available → acquire it and return **`true`**.
- Not available → return **`false`** immediately; the thread continues
  **without waiting**. It never enters the waiting state for this call.

```java
Lock lock = new ReentrantLock();

if (lock.tryLock()) {
    try {
        // safe operations
    } finally {
        lock.unlock();
    }
} else {
    // alternative operations
}
```

> **Board:** `boolean tryLock()` — to acquire the lock without waiting. If
> the lock is available, the thread acquires it and returns `true`. If it is
> not available, the method returns `false` and the thread can continue
> execution without waiting; the thread is never entered into a waiting
> state.

## 31:23 — Comparing `lock()` and `tryLock()`; introducing the timed form

- `lock()` — available? get it. Not? **wait until** you do.
- `tryLock()` — available? get it. Not? **don't wait**, continue.
- A middle ground: try, and if not available wait **up to some limit** (say,
  one hour); if still nothing after that, continue anyway.

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;

// wait up to 1 hour, then give up and continue either way
boolean acquired = lock.tryLock(1, TimeUnit.HOURS);
```

## 32:55 — `boolean tryLock(long time, TimeUnit unit)`

```java
boolean tryLock(long time, TimeUnit unit) throws InterruptedException;
```

- Lock available → acquire it and continue.
- Not available → wait up to the **specified amount of time**.
- Still not available after that → the method returns `false` and the
  thread continues execution.

> **Board:** If the lock is available, get it and continue. If not
> available, wait until the specified amount of time. If still not
> available after that, the thread can continue execution.

### 35:25 — The `TimeUnit` enum

`TimeUnit` is an **enum** (a group of constants), living in
**`java.util.concurrent`** — not in the `locks` sub-package, so both need
importing when a timed lock method is in play.

```java
import java.util.concurrent.TimeUnit;

// Allowed TimeUnit constants:
// NANOSECONDS, MICROSECONDS, MILLISECONDS,
// SECONDS, MINUTES, HOURS, DAYS
```

Sir checks this on the board by running `javap` against
`java.util.concurrent.TimeUnit` and reads its output as "an abstract class,
but strictly speaking, an enum."

> ❗ **Correction — `javap` on `TimeUnit` does not print "abstract class."**
> Run on a current JDK, `javap java.util.concurrent.TimeUnit` prints:
> ```text
> public final class java.util.concurrent.TimeUnit extends java.lang.Enum<java.util.concurrent.TimeUnit>
> ```
> — `final class ... extends Enum`, exactly what every compiled Java `enum`
> looks like at the bytecode level, never `abstract`. Whatever javap output
> Sir was reading from at the time, the underlying fact he draws from it —
> "it's really an enum" — is correct and is the part worth remembering:
> `TimeUnit.MILLISECONDS.getClass().isEnum()` returns `true`.

## 39:03 — Example: `tryLock` with milliseconds

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;

if (lock.tryLock(1000, TimeUnit.MILLISECONDS)) {
    try {
        // got the lock within 1000 ms
    } finally {
        lock.unlock();
    }
} else {
    // still no lock after waiting up to 1000 ms
}
```

## 39:51 — `void lockInterruptibly()`

```java
void lockInterruptibly() throws InterruptedException;
```

- Lock available → acquire it and return immediately.
- Not available → wait.
- While waiting, if the thread is **interrupted** → it does **not** get the
  lock; an `InterruptedException` propagates instead.

> **Board:** `void lockInterruptibly()` — acquires the lock if it is
> available and returns immediately. If the lock is not available, it
> waits. While waiting, if the thread is interrupted, then the thread won't
> get the lock.

## 42:12 — `void unlock()`

```java
void unlock();
```

Releases the lock. The twist: only the **owner** — the thread that actually
holds the lock — may call `unlock()` on it.

```java
Lock lock = new ReentrantLock();

lock.lock();
// safe operations
lock.unlock();          // fine — the calling thread owns the lock

// a different thread that never called lock() on the same object:
lock.unlock();           // IllegalMonitorStateException at runtime
```

> **Board:** To call `unlock()`, the current thread must be the owner of the
> lock; otherwise we get a runtime exception, `IllegalMonitorStateException`.

Verified: constructing a fresh `ReentrantLock` and calling `unlock()` on it
without ever locking it first throws `IllegalMonitorStateException` exactly
as described.

## 45:03 — Five methods of `Lock`; next class is `ReentrantLock`

| # | Method |
|---|---|
| 1 | `lock()` |
| 2 | `tryLock()` |
| 3 | `tryLock(long, TimeUnit)` |
| 4 | `lockInterruptibly()` |
| 5 | `unlock()` |

The implementation class for the next session: **`ReentrantLock`**.

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

Lock lock = new ReentrantLock();
```

---

## Exam and interview points

1. **`java.util.concurrent.locks` arrived in Java 1.5** to fix five specific
   gaps in `synchronized`: no non-blocking try, no timeout, no fairness
   control, no waiting-thread count, no locking across method boundaries.
2. **`Lock` has five methods**: `lock()`, `tryLock()`,
   `tryLock(long, TimeUnit)`, `lockInterruptibly()`, `unlock()`.
   `ReentrantLock` is the implementation class covered next.
3. **`tryLock()` never blocks** — it returns `false` immediately if the lock
   is unavailable, unlike `lock()`, which behaves exactly like entering a
   `synchronized` block.
4. **`unlock()` requires ownership.** Calling it from a thread that never
   acquired the lock throws `IllegalMonitorStateException` at runtime — this
   is directly testable and easy to trigger by accident (e.g. unlocking in a
   `finally` block that runs even when `tryLock()` returned `false`).
5. **`TimeUnit` lives in `java.util.concurrent`, not `...locks`** — both
   packages need importing when using the timed `tryLock` overload. It is a
   genuine `enum`, whatever a given `javap` invocation prints.
6. **Deadlock is not exclusive to `synchronized`.** Any two-resource,
   inconsistent-order acquisition deadlocks — including two `Lock` objects
   taken in opposite order by two threads.
7. **Since Java 24 (JEP 491), `synchronized` no longer pins virtual
   threads** the way it did in Java 21–23 — a real narrowing of the
   historical gap between implicit locks and the explicit `Lock` API.

---

**Next:** Video 097 — java.util.concurrent.locks (ReentrantLock)
