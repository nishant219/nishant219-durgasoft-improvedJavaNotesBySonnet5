# Video 097 — java.util.concurrent.locks (ReentrantLock)

## Video info

**Title:** Core Java With OCJP/SCJP: Multithreading Enhancement  Part- 3|| java.util.concurrent.locks

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 97 of 203 |
| Series | Multithreading Enhancement · Part 3 |
| Topic | java.util.concurrent.locks · ReentrantLock |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 36m 50s |
| Video ID | q8kaFJ8-zVo |
| Watch | https://www.youtube.com/watch?v=q8kaFJ8-zVo |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

The previous session (Video 096) listed the five gaps in `synchronized` and
introduced the `Lock` interface. This one puts `Lock` to work through its one
implementation class, **`ReentrantLock`**:

1. Why the class is called "reentrant" — a thread's **hold count**.
2. Both constructors, and the **fairness** flag's default value.
3. The eight extra query methods `ReentrantLock` adds beyond `Lock`'s five —
   and which ones you can actually call from outside the class.
4. Two worked demos: the `Display.wish()` synchronization example rebuilt
   with `ReentrantLock` instead of `synchronized`, then `tryLock()` — first
   the no-wait form, then the timed form with a retry loop.

---

## 00:05 — Recap: the `Lock` interface's five methods

Last session covered `java.util.concurrent.locks` (arrived in Java 1.5) as
the fix for `synchronized`'s performance, deadlock, and missing-API problems,
and its `Lock` interface:

```java
void lock();
boolean tryLock();
boolean tryLock(long time, TimeUnit unit) throws InterruptedException;
void lockInterruptibly() throws InterruptedException;
void unlock();
```

## 01:43 — `ReentrantLock`: the implementation class

`Lock` alone is unusable — you need an implementation. **`ReentrantLock`**
implements `Lock`, and is a **direct child class of `Object`** (verified:
`ReentrantLock.class.getSuperclass()` is `java.lang.Object`; it also
implements `java.io.Serializable`, which this lecture doesn't cover).

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

// Board:
// ReentrantLock is the implementation class of the Lock interface,
// and it is the direct child class of Object.
```

## 02:12 — Why the word "reentrant"?

Not a namesake — the name describes the behavior: **again and again**. The
same thread can call `lock()` on the same `ReentrantLock` object multiple
times, and the JVM tracks how many times with a **hold count** per thread.

```java
ReentrantLock l = new ReentrantLock();

l.lock(); // hold count 0 → 1
l.lock(); // hold count 1 → 2
l.lock(); // hold count 2 → 3

l.unlock(); // hold count 3 → 2  (lock NOT released yet)
l.unlock(); // hold count 2 → 1
l.unlock(); // hold count 1 → 0  → lock released
```

One `unlock()` does not release a lock held three times over — the lock is
released only when the hold count reaches **zero**.

```java
// Board:
// Reentrant means a thread can acquire the same lock multiple times
// without any issue. Internally, ReentrantLock increments the calling
// thread's hold count on every lock() call, and decrements it on every
// unlock() call. The lock is released only when the count reaches zero.
```

## 09:07 — Constructors of `ReentrantLock`

**No-arg:**

```java
ReentrantLock l = new ReentrantLock();
// creates an instance with the default (unfair) policy
```

**With a fairness flag:**

```java
ReentrantLock l = new ReentrantLock(boolean fairness);
// creates an instance with the given fairness policy
```

Sir's gloss on "fairness": be a bit fair, don't be biased. The allowed values
are `true` and `false`:

- **`fairness = true`** → the **longest-waiting** thread acquires the lock
  when it becomes available — first-come-first-served.
- **`fairness = false`** → which waiting thread gets the chance is
  unspecified.
- **Default (no-arg constructor): `false`.**

```java
// Board:
// If fairness is true, the longest-waiting thread acquires the lock
// when it becomes available (first-come-first-served).
// If fairness is false, which waiting thread gets the chance is
// unspecified.
// Default value for fairness is false.
```

> ❗ **Correction — the fairness guarantee has one documented exception:
> plain `tryLock()`.**
> `ReentrantLock`'s own Javadoc is explicit about this: *"Even when this lock
> has been set to use a fair ordering policy, a call to `tryLock()` will
> immediately acquire the lock if it is available, whether or not other
> threads are currently waiting for the lock."* Barging past a queue this
> way is legal and documented — only `lock()`, `lockInterruptibly()`, and the
> **timed** `tryLock(time, unit)` honor the fairness setting. If you want a
> timed acquire that also respects fairness, the Javadoc's own advice is
> `tryLock(0, TimeUnit.SECONDS)` rather than the no-arg overload. This
> matters directly for Demo 3 and Demo 4 below, both of which use `tryLock`.

## 15:34 — Exam drill: which declarations are equal?

```java
ReentrantLock l1 = new ReentrantLock();
ReentrantLock l2 = new ReentrantLock(true);
ReentrantLock l3 = new ReentrantLock(false);
```

**`l1` and `l3` are equivalent** — the no-arg constructor's default fairness
is `false`, same as passing `false` explicitly.

## 17:20 — Important methods of `ReentrantLock`

Because `ReentrantLock` implements `Lock`, it inherits all five `Lock`
methods, plus eight of its own:

```java
// From Lock:
void lock();
boolean tryLock();
boolean tryLock(long time, TimeUnit unit) throws InterruptedException;
void lockInterruptibly() throws InterruptedException;
void unlock();

// ReentrantLock's own query methods:
int getHoldCount();
boolean isHeldByCurrentThread();
int getQueueLength();
java.util.Collection<Thread> getQueuedThreads();
boolean hasQueuedThreads();
boolean isLocked();
boolean isFair();
Thread getOwner();
```

| Method | What it returns |
|---|---|
| `getHoldCount()` | number of holds on this lock by the **current** thread |
| `isHeldByCurrentThread()` | `true` iff the lock is held by the current thread |
| `getQueueLength()` | number of threads waiting for the lock |
| `getQueuedThreads()` | a `Collection` of threads waiting to get the lock |
| `hasQueuedThreads()` | `true` if any thread is waiting to get the lock |
| `isLocked()` | `true` if the lock is held by some thread (same or another) |
| `isFair()` | `true` if the fairness policy was set to `true` |
| `getOwner()` | the `Thread` currently holding the lock |

> ❗ **Correction — `getQueuedThreads()` and `getOwner()` are not directly
> callable; the other six are.**
> Verified against `javap java.util.concurrent.locks.ReentrantLock`: both
> are declared **`protected`**, not `public`. Calling either from ordinary
> code — even `main` in the same package, if it's a different class — is a
> compile error:
> ```text
> error: getQueuedThreads() has protected access in ReentrantLock
> error: getOwner() has protected access in ReentrantLock
> ```
> They exist for **subclasses** that want to build a monitoring or debugging
> tool on top of `ReentrantLock` — the class's own Javadoc shows exactly
> this pattern, subclassing `ReentrantLock` to expose them publicly. The
> other six methods in the table — `getHoldCount`, `isHeldByCurrentThread`,
> `getQueueLength`, `hasQueuedThreads`, `isLocked`, `isFair` — are ordinary
> `public` methods and behave exactly as taught. This is why the runnable
> example below (`ReentrantLockDemo2`) only ever calls those six.

## 28:08 — Example 1: `ReentrantLockDemo2` (method familiarity)

```java
import java.util.concurrent.locks.ReentrantLock;

class ReentrantLockDemo2 {
    public static void main(String[] args) {
        ReentrantLock l = new ReentrantLock();

        l.lock();
        l.lock();
        System.out.println(l.isLocked());              // true
        System.out.println(l.isHeldByCurrentThread());  // true
        System.out.println(l.getQueueLength());         // 0
        System.out.println(l.getHoldCount());           // 2

        l.unlock();
        System.out.println(l.getHoldCount());           // 1
        System.out.println(l.isLocked());                // true

        l.unlock();
        System.out.println(l.isLocked());                // false
        System.out.println(l.isFair());                  // false
    }
}
```

Verified on JDK 26: compiles and prints, in order, `true true 0 2 1 true
false false` — exactly what the comments above claim. `getQueueLength()`
prints `0` because `main` is the only thread here; there is no one else
waiting.

## 36:48 — Example 2: replacing `synchronized` (the `wish` demo, again)

Same classic demo as the synchronized-block sessions: `Display.wish(String
name)` prints `"Good Morning: "`, sleeps 2 seconds, then prints the name, ten
times in a loop. Two threads share one `Display`, named **Dhoni** and
**Yuvi**.

**Without any synchronization** — irregular, interleaved output:

```java
class Display {
    public void wish(String name) {
        for (int i = 0; i < 10; i++) {
            System.out.print("Good Morning: ");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
            }
            System.out.println(name);
        }
    }
}

class MyThread extends Thread {
    Display d;
    String name;

    MyThread(Display d, String name) {
        this.d = d;
        this.name = name;
    }

    public void run() {
        d.wish(name);
    }
}

class SynchronizedDemo {
    public static void main(String[] args) {
        Display d = new Display();
        MyThread t1 = new MyThread(d, "Dhoni");
        MyThread t2 = new MyThread(d, "Yuvi");
        t1.start();
        t2.start();
        // prints mixed / irregular "Good Morning" lines
    }
}
```

**With `wish` declared `synchronized`** — regular output, one thread's full
ten-line cycle before the other's:

```java
public synchronized void wish(String name) { /* same body */ }
// prints all ten "Good Morning: Dhoni" lines, then all ten "Good Morning: Yuvi"
// (which name goes first is not guaranteed)
```

## 48:01 — Same example, `ReentrantLock` instead of `synchronized`

```java
import java.util.concurrent.locks.ReentrantLock;

class Display {
    ReentrantLock l = new ReentrantLock();

    public void wish(String name) {
        l.lock();                          // line 1
        try {
            for (int i = 0; i < 10; i++) {
                System.out.print("Good Morning: ");
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                }
                System.out.println(name);
            }
        } finally {
            l.unlock();                    // line 2
        }
    }
}

class MyThread extends Thread {
    Display d;
    String name;

    MyThread(Display d, String name) {
        this.d = d;
        this.name = name;
    }

    public void run() {
        d.wish(name);
    }
}

class ReentrantLockDemo1 {
    public static void main(String[] args) {
        Display d = new Display();
        MyThread t1 = new MyThread(d, "Dhoni");
        MyThread t2 = new MyThread(d, "Yuvi");
        t1.start();
        t2.start();
        // prints regular output — one thread completes its wish() before the other starts
    }
}
```

Verified on JDK 26: compiles and runs as described. Whichever thread reaches
`l.lock()` first — say Dhoni — holds the lock through its full ten-iteration
loop; Yuvi's thread blocks on `l.lock()` until Dhoni's `finally` block calls
`l.unlock()`. Same guarantee as `synchronized wish`, for this example — but
`ReentrantLock` can do more, as the `tryLock` demos below show.

## 59:51 — Ablation: comment out line 1 and line 2

```text
Comment out l.lock() (line 1) and l.unlock() (line 2):
  → both threads run wish() at once → irregular (interleaved) output.

Leave both lines in:
  → threads run one at a time inside wish() → regular output.
```

`try { … } finally { l.unlock(); }` around the body is what makes this safe:
if the loop body ever threw, `unlock()` still runs and the lock isn't held
forever. Sir's demo omits the `finally` when narrating the "comment out the
lock lines" experiment, but the working version above always wraps `unlock()`
in `finally` — an unlock a thread never reaches is a lock every other thread
waits on forever.

## 1:02:24 — Flexibility: `tryLock` without a wait, and with a time limit

`synchronized` cannot express "try for the lock, but don't make me wait" or
"wait up to N seconds, then give up." `ReentrantLock`'s `tryLock()` and
`tryLock(time, unit)` can — the next two demos show each.

### 1:02:42 — Demo 3: `tryLock()`, no waiting (`ReentrantLockDemo3`)

```java
import java.util.concurrent.locks.ReentrantLock;

class MyThread extends Thread {
    static ReentrantLock l = new ReentrantLock(); // one lock shared by every MyThread

    MyThread(String name) {
        super(name);
    }

    public void run() {
        if (l.tryLock()) {
            System.out.println(Thread.currentThread().getName()
                    + " got lock and performing safe operations");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
            }
            l.unlock();
        } else {
            System.out.println(Thread.currentThread().getName()
                    + " unable to get lock and hence performing alternative operations");
        }
    }
}

class ReentrantLockDemo3 {
    public static void main(String[] args) {
        MyThread t1 = new MyThread("First Thread");
        MyThread t2 = new MyThread("Second Thread");
        t1.start();
        t2.start();
    }
}
```

Verified on JDK 26 — a typical run:

```text
First Thread got lock and performing safe operations
Second Thread unable to get lock and hence performing alternative operations
```

`l` is `static` so every `MyThread` instance shares the **one** lock object —
the point of the demo is contention between the two threads, not two
independent locks. Whichever thread reaches `tryLock()` first wins it; there
is no guarantee it's always "First Thread" (Sir notes this too — with only a
couple of lines of work, the first-started thread usually wins the race, but
it isn't guaranteed). The loser never waits: `tryLock()` returns `false`
immediately and the `else` branch runs straight away. Traditional
`synchronized` has no equivalent — an unavailable lock always means waiting.

### 1:16:54 — Demo 4: `tryLock` with a time limit + retry loop (`ReentrantLockDemo4`)

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

class MyThread extends Thread {
    static ReentrantLock l = new ReentrantLock();

    MyThread(String name) {
        super(name);
    }

    public void run() {
        do {
            try {
                if (l.tryLock(5000, TimeUnit.MILLISECONDS)) {
                    System.out.println(Thread.currentThread().getName() + " got lock");
                    try {
                        Thread.sleep(30000); // 30 seconds
                    } catch (InterruptedException e) {
                    }
                    System.out.println(Thread.currentThread().getName() + " releases lock");
                    l.unlock();
                    break;
                } else {
                    System.out.println(Thread.currentThread().getName()
                            + " unable to get lock and will try again");
                }
            } catch (InterruptedException e) {
            }
        } while (true);
    }
}

class ReentrantLockDemo4 {
    public static void main(String[] args) {
        MyThread t1 = new MyThread("First Thread");
        MyThread t2 = new MyThread("Second Thread");
        t1.start();
        t2.start();
    }
}
```

Verified on JDK 26 (with a shortened 3-second sleep in place of 30, to keep
the test run short): the pattern holds exactly as narrated.

- First thread gets the lock immediately, then sleeps 30 seconds.
- Second thread's `tryLock(5000, TimeUnit.MILLISECONDS)` waits at most 5
  seconds each attempt; it keeps missing, logs "unable to get lock and will
  try again", and loops — roughly six attempts across the 30-second wait.
- When the first thread's `finally`-free `l.unlock()` runs and `break`s out,
  the second thread's next `tryLock` succeeds, it sleeps its own 30 seconds,
  unlocks, and `break`s too.

The `do { … } while (true)` is an intentional infinite loop; the only exit is
the `break` inside the `if` branch once the lock is actually acquired and
used. Both `TimeUnit` and `ReentrantLock` need importing from two different
packages — `TimeUnit` lives in `java.util.concurrent`, `ReentrantLock` in
`java.util.concurrent.locks`.

## 1:35:47 — Closing: prefer `Lock` over `synchronized`

Sir's verdict: once you know `Lock`/`ReentrantLock`, using plain
`synchronized` is "never recommended" — `tryLock()` (with or without a time
limit) gives flexibility `synchronized` simply doesn't have, yet most
developers stay in the habit of reaching for `synchronized` regardless.

> ⚠️ **Modern Java — "never recommended" overstates it; the historical
> reason to avoid `synchronized` has narrowed since Java 24.**
> Everything about `tryLock()`'s flexibility above is still true today —
> that part of the recommendation holds. But one specific reason to prefer
> the explicit `Lock` API — covered in Video 096's notes — has weakened:
> from Java 21 through 23, a **virtual thread** (JEP 444) blocking inside a
> `synchronized` block got **pinned** to its carrier platform thread, unlike
> blocking on a `java.util.concurrent.locks.Lock`. **JDK 24** (JEP 491)
> removed that pinning, closing most of the gap. The realistic modern
> guidance: reach for `synchronized` when you just need mutual exclusion —
> it's simpler, and you can't forget the `unlock()` — and reach for
> `ReentrantLock` specifically when you need something `synchronized` cannot
> express at all: `tryLock()`, a timeout, a fairness policy, or multiple
> `Condition`s on one lock. "Never use `synchronized`" was never quite right,
> even in the Java 6/7 era this lecture targets; it's less right now.

---

## Exam and interview points

1. **`ReentrantLock` implements `Lock` and directly extends `Object`** — not
   `Thread`, not any other concurrency type.
2. **"Reentrant" means a hold count, not a namesake.** The same thread can
   call `lock()` on the same object repeatedly; the lock is released only
   when as many `unlock()` calls have run as `lock()` calls did — the count
   reaches zero.
3. **Default fairness is `false`.** `new ReentrantLock()` and `new
   ReentrantLock(false)` are equivalent; only `new ReentrantLock(true)`
   guarantees the longest-waiting thread goes next — and even then, plain
   `tryLock()` is documented to barge past that queue regardless.
4. **Six of the eight extra methods are `public`; two are `protected`.**
   `getHoldCount`, `isHeldByCurrentThread`, `getQueueLength`,
   `hasQueuedThreads`, `isLocked`, `isFair` are callable directly.
   `getQueuedThreads()` and `getOwner()` are `protected` — meant for a
   subclass building a monitoring tool, not for ordinary calling code.
5. **`tryLock()` never blocks.** It returns `false` immediately if the lock
   is unavailable — the calling thread never enters a waiting state, unlike
   every form of `synchronized`.
6. **`tryLock(long, TimeUnit)` blocks up to a limit, then gives up.** Returns
   `true` if it acquired the lock within that window, `false` otherwise —
   the tool for "wait a bit, then do something else" that `synchronized`
   cannot express at all.
7. **Always pair `lock()` with `unlock()` in a `try`/`finally`.** A thread
   that acquires a lock and then throws before calling `unlock()` leaves
   every other thread waiting on that lock forever.
8. **Since JDK 24 (JEP 491), the main historical case for preferring
   `ReentrantLock` over `synchronized` for virtual-thread code has mostly
   gone away** — know this if "why prefer explicit locks" comes up in an
   interview that also touches virtual threads.

**Next:** Video 098 — Java thread pools (Executor framework)
