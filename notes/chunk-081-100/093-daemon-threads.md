# Video 093 — Daemon Threads

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-13 || Daemon Threads

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 93 of 203 |
| Series | Multi Threading · Part 13 |
| Topic | Daemon Threads |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 50m 20s |
| Video ID | u5OunWJhKoE |
| Watch | https://www.youtube.com/watch?v=u5OunWJhKoE |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Multi-threading Part 13: **daemon threads** — what marks a thread as
background support staff, the movie-shoot analogy for why they exist, the
GC-priority story, the `isDaemon`/`setDaemon` API and the one rule about when
you're allowed to call it, how daemon status defaults and inherits
parent-to-child, why main's daemon status can never be changed, and the
closing rule that decides everything: once the **last non-daemon thread**
dies, every daemon thread dies with it — proved live with `DaemonThreadDemo`.

---

## 00:09 — Topic: Daemon threads

Board heading: **Daemon threads**. Sir flags it as interview-heavy material.

## 00:30 — Definition + examples

**Definition:** the thread which is executing in the **background** is
called a **daemon thread**.

**Best examples — real JVM-internal threads:**

1. Garbage collector
2. Attach Listener
3. Signal Dispatcher

> **Board:**
> The threads which are executing in the background are called daemon
> threads. Examples: Garbage collector, Signal Dispatcher, Attach Listener,
> etc.

A quick dump of a plain `Hello World` process (`Thread.getAllStackTraces()`,
JDK 26) confirms the shape of this, if not the exact three names: `main` is
the only non-daemon thread, alongside daemon threads named `Reference
Handler`, `Finalizer`, `Notification Thread`, `Signal Dispatcher`, and
`Common-Cleaner`. **Attach Listener** specifically only starts on demand —
the first time something attaches to the JVM (`jstack`, `jcmd`, a profiler) —
so it won't appear in every dump, but it is a real daemon thread with exactly
that name once triggered.

## 02:46 — Advantage / purpose (the movie-shoot analogy)

Sir's analogy: on a 70&nbsp;mm screen you might see two actors talking in a
park, but shooting that scene needs a producer, a director, a makeup team,
food arrangements, crowd control, a dozen buses — over a hundred people
working unseen so those two can perform. The people never on screen still
make the shoot possible.

| Analogy | Threads |
|---|---|
| Hero / heroine on screen | non-daemon threads (e.g. `main`) |
| Background crew | daemon threads |

The main purpose of daemon threads: **provide support for non-daemon
threads.**

## 08:34 — Concrete JVM example: the garbage collector

`main` is running and suddenly faces a memory problem. The JVM runs the
**garbage collector** — a daemon — to destroy unreachable objects and free
bytes, so `main` can keep going. Indirectly, GC's whole purpose is to support
`main` (or whichever non-daemon thread needed the memory), exactly like the
crew supports the actor.

> **Board:**
> The main objective of daemon threads is to provide support for non-daemon
> threads (main thread). If a main thread runs with low memory, the JVM runs
> the garbage collector to destroy useless objects, so free memory improves
> and main can continue.

## 12:08 — Priority of daemon threads

Sir's story: assume `main` has priority 5 and GC has priority 1 — `main`
keeps getting the processor. If a memory problem shows up, the JVM "raises"
GC's priority from 1 to 10 so it can reclaim memory fast; once enough is
free, the JVM "lowers" it back to 1 and `main` continues.

**The twist to remember:** daemon threads are usually low priority, **but a
daemon can run at high priority when the situation calls for it** — never
answer "daemon threads always run at low priority."

> **Board:**
> Usually daemon threads have low priority. But based on our requirement,
> daemon threads can run with high priority also.

> ❗ **Correction — the "JVM dials GC's priority from 1 up to 10 and back"
> story is a teaching simplification, not literally how a JVM behaves.**
> Real JVM-internal threads are assigned a fixed priority once, at creation —
> they are not dynamically raised and lowered per allocation failure. A dump
> of a plain `Hello World` process (JDK 26) shows this:
>
> | Thread | Daemon | Priority |
> |---|---|---|
> | `main` | false | 5 |
> | `Reference Handler` | true | 10 |
> | `Notification Thread` | true | 9 |
> | `Signal Dispatcher` | true | 9 |
> | `Finalizer` | true | 8 |
> | `Common-Cleaner` | true | 8 |
>
> Several daemon threads already sit above `main`'s priority by default —
> real evidence for Sir's twist that daemons "can run with high priority
> also." But nothing here hops between 1 and 10 in response to a memory
> shortage; the numbers are fixed at thread creation. On top of that, thread
> priority has always been only an **advisory hint** to the OS scheduler
> (JLS §17.9) — the JVM passes it down, but whether the underlying OS
> actually reorders threads by it is platform-dependent, and commonly ignored
> outright on ordinary (non-real-time) scheduling. None of this is a Java
> 6/7-vs-today difference — the mental model just needs correcting: "daemons
> are commonly low-to-mid priority, a few run high" is the true takeaway, not
> "the JVM live-tunes GC's priority."

## 14:26 — How to check / change daemon status: the API

Two methods on `Thread`:

```java
public final boolean isDaemon()
public final void setDaemon(boolean on)
```

`isDaemon()` checks whether a thread is a daemon. `setDaemon(true)` makes it
a daemon; `setDaemon(false)` makes it non-daemon. (Both methods are declared
`final` — confirmed via `javap java.lang.Thread` on JDK 26 — so this is not
something a subclass can override.)

## 15:41 — Twist: changing daemon status only works before `start()`

Changing daemon status is possible **only before starting** the thread. If
the thread has already been `start()`ed and you call `setDaemon(...)`, you
get a runtime exception:

```java
// java.lang.IllegalThreadStateException
```

> **Board:**
> Changing daemon nature is possible before starting of a thread only. After
> starting a thread, if we try to change daemon nature →
> `IllegalThreadStateException`.

> ❗ **Correction — the exact rule is "not alive," not "before start."**
> Sir's rule is exactly right for the OCJP exam and for every case this
> lecture demos: call `setDaemon` on a running thread and it throws. But the
> JDK's actual contract (and the JLS) is narrower than "before start()" —
> `setDaemon` throws `IllegalThreadStateException` only **if the thread is
> alive** (`isAlive()` is `true`). A thread that has already finished running
> is no longer alive, so its daemon flag can technically still be flipped
> afterward, pointless as that is:
>
> ```java
> Thread t = new Thread(() -> {});
> t.start();
> t.join();             // t has now finished; isAlive() == false
> t.setDaemon(true);     // no exception — verified on JDK 26
> ```
>
> Nobody does this on purpose in real code, so "before start only" remains
> the right rule of thumb to carry into an interview — just don't be thrown
> if a sharper question probes the exact boundary.

## 19:55 — Default nature

- By default, **main is always non-daemon**.
- For every other thread, daemon status is **inherited from parent to
  child** at the moment of creation: daemon parent → daemon child;
  non-daemon parent → non-daemon child.

> **Board:**
> By default main thread is always non-daemon. For all remaining threads,
> daemon nature is inherited from parent to child. If parent is daemon,
> child is also daemon; if parent is non-daemon, child is also non-daemon.

## 23:02 — Can we change daemon status of `main`?

**Impossible.** By the time your `main` method's first line runs, `main` is
already alive — the JVM created and started it before handing control to
your code — so any `setDaemon` call on it hits the same "thread is alive"
exception as any other running thread. For threads **you** create, changing
daemon status before `start()` is no problem at all.

> **Board:**
> It is impossible to change daemon nature of main thread, because it is
> already started by the JVM at the beginning.

## 25:07 — Live demo: check main, fail to set main, succeed on a child

```java
class MyThread extends Thread {
}

class Test {
    public static void main(String[] args) {
        System.out.println(Thread.currentThread().isDaemon());
        // false

        Thread.currentThread().setDaemon(true);
        // compiles; at runtime:
        // Exception in thread "main" java.lang.IllegalThreadStateException

        MyThread t = new MyThread();   // parent (main) is non-daemon → child non-daemon
        System.out.println(t.isDaemon());
        // false

        t.setDaemon(true);   // OK — t was never started
        System.out.println(t.isDaemon());
        // true
    }
}
```

Compiled and run stepwise on JDK 26 — output matches exactly: `false`, then
the `IllegalThreadStateException` on `main`, then `false`, then `true` for
the child.

## 33:32 — The last major point: when the last non-daemon ends, daemons die

Back to the analogy: shooting wraps and the actors leave — is the makeup
person still required? The cameraman? No. Once the **last non-daemon
thread** completes, daemon threads are no longer needed.

**Rule:** whenever the last non-daemon thread terminates, **all daemon
threads are terminated automatically**, **irrespective of their position** —
mid-loop, just starting, wherever they are, they are killed.

> **Board:**
> Whenever last non-daemon thread terminates, automatically all daemon
> threads will be terminated, irrespective of their position.

## 36:42 — Program: `DaemonThreadDemo`

```java
class MyThread extends Thread {
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println("Child Thread");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
            }
        }
    }
}

class DaemonThreadDemo {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        // Line 1:
        t.setDaemon(true);
        t.start();
        System.out.println("End of main thread");
    }
}
```

## 39:33 — Case A: comment out Line 1 (`setDaemon`)

Main is non-daemon; the child, inheriting from main, is also non-daemon.
Both run to their own completion — the child prints `Child Thread` all 10
times, continuing after `End of main thread` prints.

## 40:10 — Case B: Line 1 active (`t.setDaemon(true)`)

Main is non-daemon; the child is now a **daemon**. When main terminates, the
child is terminated with it — it does **not** reliably finish 10 iterations.
Compiled and run three times on JDK 26 with the code above: every run printed
`End of main thread` followed by exactly **one** `Child Thread` line, then
exited — consistent with Sir's "no guarantee, zero or at most one" claim.
There is no guarantee even that one print happens; it depends on how far the
scheduler lets the child get before the JVM notices main is done.

> **Board recap:**
> Commenting Line 1 → both threads are non-daemon → both run to completion
> (child prints 10 times). Leaving Line 1 in → main is non-daemon and child
> is daemon → whenever main terminates, the child is terminated with it.
> Typical output: `End of main thread` plus at most one `Child Thread` —
> never all 10.

> ⚠️ **Modern Java — virtual threads (Java 21) are always daemon.**
> Everything above concerns *platform* threads (the only kind that existed in
> Java 6/7). A virtual thread (Project Loom, JEP 444) is unconditionally
> daemon:
>
> - `isDaemon()` on a virtual thread always returns `true`.
> - `setDaemon(true)` is a no-op — it already is one.
> - `setDaemon(false)` does not silently fail like on a live platform thread —
>   it throws `IllegalArgumentException`, not `IllegalThreadStateException`:
>
> ```java
> Thread vt = Thread.ofVirtual().unstarted(() -> {});
> System.out.println(vt.isDaemon());   // true
> vt.setDaemon(false);
> // java.lang.IllegalArgumentException: 'false' not legal for virtual threads
> ```
>
> Verified on JDK 26. The practical payoff follows straight from this
> lecture's closing rule: because a virtual thread can never be non-daemon,
> it can never be the thread that keeps the JVM process alive. Spawn a
> million virtual threads doing background work — none of them will stop
> `main` (or any other platform non-daemon thread) from ending the process
> the moment it finishes. The "last non-daemon thread" that decides shutdown
> is always a platform thread.
>
> Separately, Java 21 also adds a one-line way to build a daemon platform
> thread without subclassing `Thread`:
>
> ```java
> Thread t = Thread.ofPlatform().daemon(true).start(() -> {
>     System.out.println("Child Thread");
> });
> ```
>
> Verified on JDK 26 — same daemon rules underneath, just less boilerplate
> than `extends Thread` + `setDaemon(true)` + `start()`.

## 49:52 — Final conclusion

Whenever the last non-daemon thread terminates, every daemon thread is
terminated automatically by default. End of Part-13.

---

## Exam and interview points

1. **Daemon = background support thread.** Real examples: garbage collector,
   Signal Dispatcher, Attach Listener (JVM-internal daemon threads you can
   see today via `Thread.getAllStackTraces()`).
2. **Purpose of daemon threads: support non-daemon threads**, not run
   independent work of their own.
3. **`isDaemon()` and `setDaemon(boolean)` are `public final` on `Thread`.**
   `setDaemon(true)` → daemon; `setDaemon(false)` → non-daemon.
4. **`setDaemon` throws `IllegalThreadStateException` once the thread is
   alive** — in practice, "call it before `start()`." (The precise boundary
   is `isAlive()`, so it also works again after the thread has finished —
   never relevant in real code.)
5. **Main is always non-daemon by default, and its daemon status can never
   be changed** — main is already alive by the time your code runs.
6. **Every other thread inherits daemon status from its parent at creation
   time**, not from any global default.
7. **Daemons are usually low priority but can run at high priority when
   required** — don't answer "daemons always run at low priority." (In a
   real JVM, priority is fixed per internal thread at startup, not
   dynamically raised and lowered — a teaching-story detail, not exam
   content.)
8. **The decisive rule: once the last non-daemon thread terminates, every
   daemon thread is terminated automatically, regardless of its position.**
   A daemon thread mid-loop does not get to finish.
9. **Virtual threads (Java 21) are always daemon** — `isDaemon()` is always
   `true`, and `setDaemon(false)` throws `IllegalArgumentException`. This is
   why spawning virtual threads never keeps a program running after its last
   platform non-daemon thread ends.

**Next:** Video 094 — Green Thread, stop(), suspend(), resume()
