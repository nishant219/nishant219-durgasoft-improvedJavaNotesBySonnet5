# Video 094 — Green Thread, stop(), suspend(), resume()

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-14 || Green Thread,stop(),suspend(),resume()

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 94 of 203 |
| Series | Multi Threading · Part 14 |
| Topic | Green Thread, stop(), suspend(), resume() |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 35m 56s |
| Video ID | 21KT--VtawI |
| Watch | https://www.youtube.com/watch?v=21KT--VtawI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This short Part-14 covers the **Green Thread model vs. Native OS model**, why
`stop()` / `suspend()` / `resume()` are **deprecated**, a small `stop()` demo
with its deprecation warning, then the **full thread life-cycle diagram**
tying `yield`, `join`, `sleep`, `wait`/`notify`, `suspend`/`resume`, and `stop`
together — the diagram Sir says ends most interviewer follow-up questions on
multithreading.

---

## 00:07 — Green Thread: the interview trap

Sir's cold open, as a joke: don't expect "Red Thread" or "Yellow Thread" next
— there is exactly one concept named for a colour, **Green Thread**, and the
name is a historical label, not a description. The trap: in an interview,
never answer "what is a green thread" with "the thread which is in green
colour" — that answer, verbatim, is what he's warning against.

## 00:55 — Two models of Java multithreading

> Java multithreading is implemented using **two models**: the **Green
> Thread model** and the **Native OS model**.

```java
// Board:
// Java multi-threading concept is implemented by using
// the following two models:
// 1. Green Thread model
// 2. Native OS model
```

## 01:29 — Green Thread model

**Green thread:** a thread managed **completely by the JVM**, **without**
taking underlying **OS** support.

Drawback: without OS/processor-level scheduling help, some features may not
work correctly — OS support is often what's actually needed. Most operating
systems never provided it; the notable exception was **Sun Solaris**, whose
early JVM literally shipped a user-level "green threads" library before
native threads existed.

**Status:** the Green Thread model is legacy and unused in any current JVM.

```java
// Board:
// Green Thread model:
// The thread which is managed completely by JVM
// without taking underlying OS support
// is called Green Thread
//
// Very few operating systems like Sun Solaris
// provide support for Green Thread model
//
// Anyway Green Thread model is not used currently
```

## 02:56 — Native OS model

**Native OS model:** a thread's life cycle managed by the JVM **with the
help of** the underlying **OS**. Every Windows-based OS supports only this
model — there is no Windows green-thread JVM.

Interview answer, condensed: Green thread = completely managed by the JVM
without OS support; with OS support, it's the native OS model, i.e. native
threads. This is the model every current JVM uses.

```java
// Board:
// Native OS model:
// The thread which is managed by the JVM
// with the help of underlying OS
// is called Native OS model
//
// All Windows based operating systems
// provide support for Native OS model
```

> ⚠️ **Modern Java — the JVM now runs a second scheduling model again, and it
> is not the old Green Thread model.**
> Since **Java 21** (JEP 444, virtual threads — preview from Java 19/JEP 425),
> the JVM schedules lightweight **virtual threads** onto a small pool of
> ordinary OS threads called **carrier threads**: many virtual threads share
> one carrier, unmounting whenever they block on I/O so the carrier can run a
> different one. That is JVM-managed, M:N scheduling — the same *idea* Sir's
> "Green Thread" definition describes.
>
> It is not the same *thing*. The 1990s Green Thread model ran cooperatively
> on a single OS thread with no real parallelism and no OS help at all;
> virtual threads still run on native OS threads underneath (via the carrier
> pool) and get genuine multi-core parallelism, with the JVM only handling the
> *mounting/unmounting*, not pretending the OS doesn't exist. Don't answer
> "green threads are back" in an interview — say virtual threads are a
> modern, safe M:N model descended from the same motivation, not a revival of
> the deprecated one.
>
> ```java
> Thread vt = Thread.ofVirtual().start(() -> System.out.println("virtual"));
> vt.join();
> ```

---

## 08:45 — How to stop a thread

Starting a thread is `t.start()`. Stopping one is exactly as simple:
`t.stop()`.

Call it, and the thread **immediately enters the dead state** — killed mid
execution, whatever it was doing. Sir's word for it: not stopping, *murder*.
Is killing something mid-task ever the recommended move? No — which is
exactly why **`stop()` is deprecated**.

## 10:19 — Why stop() is dangerous: the DB-connection example

Take a `run()` with three steps:

```java
public void run() {
    // 1. open DB connection
    // 2. read data
    // 3. close DB connection
}
```

If another thread calls `t.stop()` while this thread is in step 2 — mid
read — the thread enters the dead state right there. Step 3 never runs.
Nobody closes the connection; the resource leaks. Killing a thread in the
middle of a multi-step job leaves whatever it was holding in an unknown
state, and that is the actual reason Oracle's own thread-deprecation
rationale gives for deprecating `stop()`: not "it's rude," but "it leaves
shared state and resources inconsistent, because the thread had no chance to
clean up or even finish an atomic operation."

## 12:12 — Demo: without stop(), the child finishes on its own

```java
class MyThread extends Thread {
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println("Child Thread");
        }
    }
}

class Test {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        System.out.println("End of main thread");
        // t.stop();  // commented out — nobody kills the child
    }
}
```

I compiled and ran this exact program. Output (order of the two threads'
lines can interleave, but the child always completes all ten):

```text
End of main thread
Child Thread
Child Thread
Child Thread
Child Thread
Child Thread
Child Thread
Child Thread
Child Thread
Child Thread
Child Thread
```

Main finishing first does not stop the child — Sir's aside, tightened: it's
like a film where the hero leaves early but the story keeps going without
him; nothing forces the child to die just because main is done.

## 14:01 — Same demo, with t.stop() — and the deprecation warning

```java
class Test {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        System.out.println("End of main thread");
        t.stop();   // main kills the child right after starting it
    }
}
```

Compiling this (on a JDK where `stop()` still exists — see the Modern Java
box below) prints:

```text
Note: Test.java uses or overrides a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
```

Recompiling with the flag names exactly which API:

```text
javac -Xlint:deprecation Test.java
warning: [deprecation] stop() in java.lang.Thread has been deprecated
```

Because main calls `stop()` almost immediately after `start()`, the child
rarely gets to print all ten lines — output is timing-dependent, anywhere
from zero lines to a partial run, never a guaranteed ten:

```text
End of main thread
// zero, some, or (rarely) all "Child Thread" lines, depending on timing
```

> **Board:** We can stop a thread's execution by using the `stop()` method of
> the `Thread` class. If we call `stop()`, the thread immediately enters the
> dead state. `stop()` is deprecated and not recommended for use.

## 17:25 — suspend() and resume(): the government-office analogy

Sir's analogy, tightened: a government employee accused of misconduct is
first **suspended** — services paused, not ended — while a committee
investigates; guilty means termination, innocent means **resume**, services
continue. Threads borrow the same two verbs: one thread can pause another
with `suspend()`, and bring it back with `resume()`.

```java
public final void suspend();   // → target thread enters the suspended state
public final void resume();    // → a suspended thread continues execution
```

`t.suspend()` parks the target thread; `t.resume()` lets it continue exactly
where it paused. Main might suspend a child and resume it later — same idea
as the demo pattern for `stop()`, just non-lethal.

**Why they're actually dangerous, beyond "it's rare":** unlike `stop()`,
which just kills, `suspend()` is **inherently deadlock-prone**. If the
suspended thread was holding a lock when it got paused — and the thread that
would call `resume()` needs that same lock to make progress — neither thread
can ever move again. The suspended thread can't finish and release the lock
because it's frozen; the resuming thread can't reach its `resume()` call
because it's blocked on the lock the frozen thread is still holding. Nobody
threw an exception, nothing crashed — the program simply stops making
progress. That is the concrete failure mode behind "deprecated and not
recommended," not just poor taste.

```java
// Board:
// We can suspend a thread by using suspend() method of Thread class
// Immediately the thread enters the suspended state
//
// We can resume a suspended thread by using resume() method of Thread class
// Then the suspended thread can continue its execution
//
// Anyway these methods are deprecated and not recommended to use
```

> ⚠️ **Modern Java — "deprecated" became "gone" for all three methods, on two
> different timelines.**
>
> | Method | Deprecated | Deprecated *for removal* | Always throws `UnsupportedOperationException` | Removed from the API entirely |
> |---|---|---|---|---|
> | `suspend()` / `resume()` | 1.2 (1998) | 14 | 20 (`ThreadGroup`'s versions degraded a release earlier, in 19) | **23** |
> | `stop()` | 1.2 (1998) | 18 | 20 | **26** |
>
> Two things happened in stages, not one jump. First, in **Java 20**, all
> three methods were re-specified to **always throw
> `UnsupportedOperationException`** the instant you call them — the code
> still compiled, but calling it blew up at runtime instead of doing anything
> dangerous. Then, later, the methods were deleted from `Thread` altogether:
> `suspend()`/`resume()` in **Java 23**, `stop()` in **Java 26**. I confirmed
> the final state directly: on the JDK 26 installed in this environment,
> `t.stop()`, `t.suspend()`, and `t.resume()` all fail to compile with
> `cannot find symbol` — the methods are not merely deprecated, they no
> longer exist on `java.lang.Thread`. (Timeline sourced from OpenJDK's own
> tracking: JDK-8293843/JDK-8368237/JDK-8368370 for `stop()`,
> JDK-8231602/JDK-8293975/JDK-8320598 for `suspend()`/`resume()`.)
>
> Practical upshot: this lecture's demos compile and run as shown on Java 6
> through 19. On Java 20–22 they still compile but `t.stop()` throws
> `UnsupportedOperationException` instead of killing the child. From Java 23
> (`suspend`/`resume`) and Java 26 (`stop`) onward, they don't compile at all
> — there is no modern replacement API, because there is no safe way to force
> another thread to stop or pause from the outside. The safe alternative,
> then and now, is cooperative: have the thread check a flag (or its own
> interrupt status) and exit `run()` on its own.

---

## 23:22 — The full thread life-cycle diagram

Sir's framing: draw this diagram in an interview and most follow-up
multithreading questions answer themselves, because every method this course
covers appears somewhere on it.

**Basic path:**

```text
new MyThread()  --start()-->  Ready/Runnable  --scheduler assigns CPU-->  Running  --run() completes-->  Dead
```

- `new MyThread()` → **New / Born** state.
- `t.start()` → **Ready / Runnable**.
- The scheduler hands it a processor → **Running**.
- `run()` returns → **Dead**.

### 25:09 — Running → yield() → Ready/Runnable

A running thread calling `Thread.yield()` drops back to **Ready/Runnable**,
giving same-or-similar-priority waiting threads a chance to run.

### 25:49 — Running → join() → Waiting (blocked for joining)

A running thread calling `join()` — `t2.join()`, `t2.join(1000)`, or
`t2.join(1000, 100)` — enters **Waiting**, specifically "blocked for
joining." It leaves that state when `t2` completes, its timeout (if any)
expires, or it gets interrupted — then back to Ready/Runnable, and on to
Running once the scheduler allocates a processor again.

### 28:00 — Running → sleep() → Sleeping

`Thread.sleep(1000)` or `sleep(1000, 100)` puts the running thread into
**Sleeping**. It leaves when the time expires or it's interrupted, then
returns to Ready/Runnable.

### 29:34 — Running → wait() → Waiting (for notification), then Waiting (for the lock)

Inter-thread communication territory: `wait()` / `notify()` / `notifyAll()`.
A running thread calling `obj.wait()`, `obj.wait(1000)`, or
`obj.wait(1000, 100)` enters **Waiting**, specifically waiting for
notification. It leaves that wait on notification, on timeout, or on
interruption — but doesn't go straight back to Running: it moves to a
**second waiting state, waiting to reacquire the object's lock**, and only
once it actually gets that lock does it return to Ready/Runnable.

### 31:50 — Running → suspend() → Suspended; resume() → Ready/Runnable

`t.suspend()` on a running thread → **Suspended**. `t.resume()` on it →
back to Ready/Runnable, services continuing.

### 32:32 — Running → stop() → Dead

`t.stop()` on a running thread → immediately **Dead**, no intermediate
state.

### 32:51 — The whole diagram, in one pass

```text
New/Born --start()--> Ready/Runnable --processor allocated--> Running --run() ends--> Dead
Running --yield()--> Ready/Runnable
Running --join()--> Waiting (blocked for joining) --complete/timeout/interrupt--> Ready/Runnable
Running --sleep()--> Sleeping --timeout/interrupt--> Ready/Runnable
Running --wait()--> Waiting (notification) --notify/timeout/interrupt--> Waiting (for lock) --lock acquired--> Ready/Runnable
Running --suspend()--> Suspended --resume()--> Ready/Runnable
Running --stop()--> Dead
```

Sir closes Part-14 there: draw this, and interviewers rarely have more
multithreading questions left to ask, because `yield`, `join`, `sleep`,
`wait`/`notify`, `suspend`/`resume`, and `stop` are all sitting on the one
picture.

For interview terminology, Sir's seven informal buckets map cleanly onto
`java.lang.Thread.State` (the actual enum the JDK exposes, present since Java
5 — this part hasn't changed since the recording):

| Sir's term | `Thread.State` value |
|---|---|
| New / Born | `NEW` |
| Ready/Runnable *and* Running | both are `RUNNABLE` — the JVM's own model does not distinguish "waiting for a processor" from "actually running one" |
| Sleeping | `TIMED_WAITING` (also covers a *timed* `join`/`wait`) |
| Waiting (blocked for joining / for notification, untimed) | `WAITING` |
| Waiting for the lock (after `notify`, before re-entry) | `BLOCKED` — the same value used for a thread stuck entering a plain `synchronized` block |
| Suspended | **no equivalent** — `Thread.State` never had a `SUSPENDED` value, and now that `suspend()`/`resume()` are gone from the API entirely (see the box above), nothing in a modern program can even reach that bucket |
| Dead | `TERMINATED` |

---

## Exam and interview points

1. **Green thread = managed entirely by the JVM, no OS support.** Native OS
   model = managed by the JVM *with* OS help. Java's JVMs today all use the
   native OS model; Sun Solaris was the historical exception that ran green
   threads.
2. **`stop()` kills mid-execution into the dead state immediately** — no
   cleanup step runs, which is why a `run()` that opens then closes a
   resource can leak it if `stop()` fires in between. That's the concrete
   reason it's deprecated, not just "it's not nice."
3. **`suspend()`/`resume()` are inherently deadlock-prone**: if the suspended
   thread holds a lock the would-be resumer needs, neither thread can ever
   proceed.
4. **All three — `stop()`, `suspend()`, `resume()` — are gone from the JDK,
   not merely deprecated.** They started always throwing
   `UnsupportedOperationException` in Java 20, then were deleted outright:
   `suspend()`/`resume()` in Java 23, `stop()` in Java 26. There is no direct
   replacement — safe thread cancellation is cooperative (a checked flag or
   `interrupt()`), not external and forcible.
5. **The seven-state life-cycle diagram** — New/Born → Ready/Runnable →
   Running → Dead, with `yield`, `join`, `sleep`, `wait`/`notify`,
   `suspend`/`resume`, and `stop` as the branches off Running — is the single
   diagram Sir says answers most interview follow-ups on threading.
6. **The JDK's own `Thread.State` enum only has six values** (`NEW`,
   `RUNNABLE`, `BLOCKED`, `WAITING`, `TIMED_WAITING`, `TERMINATED`) — Ready
   and Running both collapse into `RUNNABLE`, and there has never been a
   `SUSPENDED` value, which matters more now that `suspend()` no longer
   exists to reach it.
7. **Virtual threads (Java 21) are a modern JVM-managed threading model, but
   they are not a revival of Green Thread** — they still run on real OS
   threads underneath and get genuine parallelism; only the mounting of many
   virtual threads onto few carrier threads is JVM-managed.

**Next:** Video 095 — Thread Group
