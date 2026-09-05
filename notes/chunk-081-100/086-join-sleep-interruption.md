# Video 086 — join(), sleep(), and thread interruption

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-6 || join() || sleep() || Thread Interruption

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 86 of 203 |
| Series | Multi Threading · Part 6 |
| Topic | join(), sleep(), Thread Interruption |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 46m 34s |
| Video ID | naQZrm9XNFI |
| Watch | https://www.youtube.com/watch?v=naQZrm9XNFI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Multi Threading Part 5 ended with **Case 1** of `join()`: the main thread called
`t.join()` and waited for the child to finish. Part 6 continues from there:

1. **`join()` loopholes** — Case 2 (child waits for main), Case 3 (mutual join
   deadlock), Case 4 (self-join deadlock).
2. **`sleep()`** — purpose, both overloaded signatures, its effect on the
   thread life cycle, a slide-rotator demo.
3. **Thread interruption** — `interrupt()`, the deferred-interrupt loophole,
   and a closing comparison of `yield()` / `join()` / `sleep()`.

---

## 00:10 — Case 2: child waits for main

In the previous video's example, the **main thread** called `t.join()` and had
to wait until the **child thread** completed. Case 2 reverses it: the **child
thread** must wait until the **main thread** completes.

> **Waiting of child thread until completing main thread.**

The terminology to get straight: *which* thread calls `join()`, and *on which*
thread object?

### 01:17 — The problem: the child has no reference to main

Inside `MyThread.run()`, the child thread must call `join()` on the **main
thread object**. But the child does not have a reference to the main thread by
default — nothing hands it one automatically.

**Fix:** give `MyThread` a **static `Thread` field**, and have `main` assign
it before starting the child:

```java
class MyThread extends Thread {
    static Thread mt;   // will hold the main thread's reference

    public void run() {
        // the child will call join() on main via mt
    }
}
```

`run()` is executed by the **child** thread, not main. The static field is
what lets the child reach the main thread object that started it.

### 02:38 — run() calls mt.join()

```java
class MyThread extends Thread {
    static Thread mt;

    public void run() {
        try {
            mt.join();   // child waits until main completes
        } catch (InterruptedException e) {
            // handle
        }
        for (int i = 0; i < 10; i++) {
            System.out.println("Child Thread");
        }
    }
}
```

| Thread | Responsibility after `t.start()` |
|---|---|
| Main | Runs its own `for` loop, prints "Main Thread" |
| Child | Calls `mt.join()` → enters waiting until main finishes |

### 03:55 — Assigning the main reference: ThreadJoinDemo1

```java
class ThreadJoinDemo1 {
    public static void main(String[] args) throws InterruptedException {
        MyThread.mt = Thread.currentThread();   // mt → main thread

        MyThread t = new MyThread();
        t.start();

        for (int i = 0; i < 10; i++) {
            System.out.println("Main Thread");
            Thread.sleep(2000);   // main sleeps 2 seconds each iteration
        }
    }
}
```

`Thread.currentThread()` returns whichever thread executes that line — here,
main. `mt` is `static`, so it is reachable as `MyThread.mt` from outside the
class. After the assignment, `mt` points at the main thread object, which is
exactly what the child needs inside `run()`.

**Thread count right after `t.start()`:** two — main and child.

### 05:26 — Main's loop, child's wait

Main keeps working; the child is parked on `mt.join()` and cannot proceed:

```java
for (int i = 0; i < 10; i++) {
    System.out.println("Main Thread");
    Thread.sleep(2000);
}
```

Main must handle `sleep()`'s checked `InterruptedException` — here via
`throws` on `main`.

### 06:32 — Semantics of mt.join()

```java
try {
    mt.join();   // child calls join() on the main thread object
} catch (InterruptedException e) {
}
```

- Executed by: the **child** thread.
- Called on: the **main thread** object (`mt`).
- Effect: the child enters the **waiting** state until `main()` returns.

Once main completes, the child resumes and prints `"Child Thread"` ten times.

### 08:13 — Case 2's expected output

```text
Main Thread
Main Thread
... (10 times)
Child Thread
Child Thread
... (10 times)
```

The child cannot print a single line until main finishes — `mt.join()` blocks
it completely. As Sir puts it: *main can wait for child, and child can wait
for main — both directions go through `join()`.*

### 09:56 — Live run

Compiling and running `ThreadJoinDemo1` shows exactly that: main prints with
its 2-second pauses, the child stays silent throughout, and only after main's
loop ends does the child print its ten lines — deterministically, on any
machine, because the wait is enforced by `join()`, not by scheduling luck.

### 15:15 — Output, restated

```text
Main Thread .......... (×10)
Child Thread ......... (×10)
```

I verified Case 2 end-to-end — compiled and ran a shortened version (3
iterations, 200 ms sleeps instead of 10×2000 ms) and got exactly this order
every time.

---

## 15:52 — Case 3: mutual join → deadlock

**Scenario:** both threads call `join()` on each other.

```java
class MyThread extends Thread {
    static Thread mt;

    public void run() {
        try {
            mt.join();   // executed by CHILD — child waits for main
        } catch (InterruptedException e) {
        }
        for (int i = 0; i < 10; i++) {
            System.out.println("Child Thread");
        }
    }
}
```

```java
class ThreadJoinDemo3 {
    public static void main(String[] args) throws InterruptedException {
        MyThread.mt = Thread.currentThread();
        MyThread t = new MyThread();
        t.start();
        t.join();   // executed by MAIN — main waits for child — DEADLOCK
    }
}
```

| Thread | Action after `t.start()` |
|---|---|
| Main | `t.join()` → waits for the child to finish |
| Child | `mt.join()` → waits for main to finish |

Neither condition can ever be satisfied, so both wait forever. **This is a
deadlock.**

### 17:10 — What actually happens when you run it

The code **compiles** cleanly and the program **runs**, but the cursor just
sits there — it never returns. Both threads are blocked on each other's
completion, permanently. I compiled and ran an equivalent program (with `t`
joined by main and `mt.join()` inside `run()`) and confirmed it: the process
does not exit on its own and has to be killed.

---

## 19:54 — Case 4: self-join deadlock

**Scenario:** a thread calls `join()` on **itself**.

```java
class Test {
    public static void main(String[] args) throws InterruptedException {
        Thread.currentThread().join();
    }
}
```

| Question | Answer |
|---|---|
| How many threads exist? | One — main only |
| Who executes `join()`? | Main |
| What does `Thread.currentThread()` return here? | Main itself |
| What is main asking for? | To wait until *itself* completes |

The paradox: main must **finish** to satisfy the `join()` call, but it cannot
reach the end of `main()` while it is still blocked on that same line. It
waits forever.

I compiled and ran this exact program: it compiles with no errors, and the
process hangs indefinitely — confirmed by checking after two seconds that it
was still alive and had to be force-killed.

### 25:08 — The four join() loopholes, together

| Case | Description | Result |
|---|---|---|
| 1 (Part 5) | Main calls `t.join()` on child | Main waits for child |
| 2 | Child calls `mt.join()` on main (via static field) | Child waits for main |
| 3 | Both call `join()` on each other | Deadlock |
| 4 | A thread calls `join()` on itself | Deadlock |

## Quick reference — join() signatures

```java
// declared in java.lang.Thread — shown for reference, not standalone code
public final void join() throws InterruptedException;
public final void join(long millis) throws InterruptedException;
public final void join(long millis, int nanos) throws InterruptedException;
```

All three are **final instance methods**, called on a `Thread` reference:

```java
t.join();              // wait forever
t.join(5000);          // wait up to 5 seconds
t.join(5000, 0);       // wait up to 5 seconds + 0 nanos
```

> ⚠️ **Modern Java — join() gained a fourth overload in Java 19.**
> `public final boolean join(Duration duration) throws InterruptedException`
> takes a `java.time.Duration` and, unlike the other three, **returns
> `boolean`** — `true` if the thread had terminated by the time the wait
> ended, `false` if the deadline passed first:
>
> ```java
> import java.time.Duration;
>
> boolean finished = t.join(Duration.ofSeconds(5));
> if (!finished) {
>     // t is still running — decide what to do
> }
> ```
>
> The three overloads Sir teaches are unchanged — same signatures, same
> `final`, same checked exception, same semantics — and remain the ones OCJP
> asks about. The `Duration` overload is the one you're likelier to reach for
> in code written after Java 19, because it reports success without a
> separate `isAlive()` check.

---

## 25:45 — sleep(): purpose and effect on the thread life cycle

**Human analogy:** when you're tired, you rest. For a thread: when it should
not perform any operation for a specific amount of time, use `sleep()`.

> *If a thread does not want to perform any operation for a particular amount
> of time → use the sleep method.*

*(Sir's aside here is a motivational digression on sleep habits — a Proverbs
quote about excessive sleep making one poor, and a recommendation to cap
sleep at around six hours. It is not Java content and is omitted below.)*

### 33:12 — Where sleep() actually gets used

**PowerPoint slide rotator:** one thread displays a slide, then sleeps for a
configured interval before advancing — 2 minutes for a live presentation, 20
or 30 seconds for a photo-album slideshow.

**Blinking bulb (GUI):** a thread toggles a bulb on, sleeps one second, turns
it off, sleeps, turns it on again — the blink is nothing but a loop around
`sleep()`.

**The pattern:** anywhere a program needs to pause for a specific, known
duration, that's `Thread.sleep()`.

### 36:37 — The two sleep() signatures

`join()` has three overloads because it can wait *forever* (no-arg form) or
for a bounded time. `sleep()` has no such no-arg form — "sleep forever
without a time period" is not a meaningful request, so every `sleep()` call
must state how long:

```java
// declared in java.lang.Thread — shown for reference, not standalone code
public static native void sleep(long millis) throws InterruptedException;
public static void sleep(long millis, int nanos) throws InterruptedException;
```

| Overload | Native? | Parameters |
|---|---|---|
| `sleep(long millis)` | Yes (JNI, in Java 6/7) | milliseconds only |
| `sleep(long millis, int nanos)` | No — implemented in Java | milliseconds + nanoseconds |

```java
// There is no such method:
// Thread.sleep();  // "sleep forever" — not in the API
```

> ⚠️ **Modern Java — a third overload, and neither is `native` any more.**
> Since **Java 19**, when `Thread` was reworked to support virtual threads
> (JEP 425 / JEP 444), both classic overloads became ordinary Java methods.
> `sleep(long millis)` now delegates to a private `sleepNanos(long)` helper,
> which itself calls a native method only when running on a **platform**
> thread — a **virtual** thread instead runs the JDK's own park/unpark logic.
> Confirmed by inspecting the JDK 26 source and bytecode directly:
>
> ```text
> public static void sleep(long) throws java.lang.InterruptedException;
> public static void sleep(long, int) throws java.lang.InterruptedException;
> public static void sleep(java.time.Duration) throws java.lang.InterruptedException;
> ```
>
> `sleep(Duration)` is the third overload, added in **Java 19**:
>
> ```java
> import java.time.Duration;
>
> Thread.sleep(Duration.ofSeconds(3));
> ```
>
> For the OCJP-era exam this course targets, "two overloads, the `long`-only
> one is native" is exactly right. For a current interview, say three
> overloads and that neither is native at the public-API level any more —
> that split only existed for platform threads before virtual threads
> existed.

### 40:11 — sleep() always throws a checked exception

Every `sleep()` overload declares `throws InterruptedException` — a
**checked** exception, so it must be handled:

```java
try {
    Thread.sleep(2000);
} catch (InterruptedException e) {
    // handle interruption
}
```

or declared:

```java
public static void main(String[] args) throws InterruptedException {
    Thread.sleep(2000);
}
```

Skip both and it is a **compile-time error** — not a runtime one.

> *Whenever we use the sleep method, we must compulsorily handle
> `InterruptedException`, either by try-catch or by throws. Otherwise,
> compile-time error.*

### 43:46 — sleep()'s place in the thread life cycle

**Normal life cycle:**

```text
NEW/BORN → start() → READY/RUNNABLE → scheduler assigns CPU → RUNNING
    → run() completes → DEAD
```

**When a running thread calls sleep:**

```java
Thread.sleep(1000);          // overload 1
Thread.sleep(1000, 100);     // overload 2 — millis + nanos
```

The running thread drops into a **sleeping** state (conceptually close to
waiting). It leaves that state one of two ways:

| Way out | Condition |
|---|---|
| 1 | The sleep duration elapses |
| 2 | The sleeping thread is interrupted |

Either way, the thread returns to **READY/RUNNABLE**, and from there the
scheduler may hand it the CPU again → **RUNNING** → eventually **DEAD**.

```text
RUNNING --sleep()--> SLEEPING --time expires OR interrupt--> READY/RUNNABLE --> RUNNING --> DEAD
```

The JDK's own vocabulary for this state (`Thread.State.TIMED_WAITING`) has
existed since `Thread.State` was added in Java 5 — this isn't a naming change
between the recording and now, just the formal term for what Sir calls
"sleeping."

### 49:44 — SlideRotator: a minimal working demo

```java
class SlideRotator {
    public static void main(String[] args) throws InterruptedException {
        for (int i = 1; i <= 10; i++) {
            System.out.println("Slide " + i);
            Thread.sleep(5000);   // 5-second pause between slides
        }
    }
}
```

Slide 1 prints, then a 5-second wait, then Slide 2, and so on through Slide
10. The same pattern covers a photo-album slideshow at a longer interval:

```java
// Photo album variant — same pattern, longer pause
for (int i = 1; i <= photoCount; i++) {
    System.out.println("Photo " + i);
    Thread.sleep(20000);   // 20 seconds per photo
}
```

### 51:36 — Live run

`SlideRotator.java` compiles and runs exactly as expected: each slide appears
five seconds after the previous one. The interval is just a number you
configure per requirement.

---

## 54:33 — Thread interruption

A theme kept surfacing while covering `join()` and `sleep()`: a **waiting**
thread (blocked in `join()`) or a **sleeping** thread (blocked in `sleep()`)
can be **interrupted** by another thread. Is that good or bad?

> **Depends on the situation** — usually considered bad, but sometimes
> genuinely required.

### 55:53 — Analogy: the last bus

Traveling roughly 50 km to your native place, waiting at the bus stop for the
last bus at 11:30 PM, you tell the fellow villagers waiting with you: *"I'm
going to sleep — wake me when the bus comes."* They forget. You wake up at
2:30 AM, the bus long gone, and now you wait hours for the next one.

The lesson: interruption is sometimes exactly what you need — not always
something to avoid.

### 57:51 — The interrupt() method

`Thread` provides an **instance** method (not static) for one thread to
interrupt another:

```java
// declared in java.lang.Thread — shown for reference, not standalone code
public void interrupt();
```

| Target thread's state | Can it be interrupted? |
|---|---|
| Sleeping | Yes |
| Waiting (e.g. blocked on `join()`) | Yes |
| Running (not sleeping/waiting) | Special behavior — see the loophole below |

> *A thread can interrupt a sleeping or a waiting thread using the
> `interrupt()` method of the `Thread` class.*

### 1:00:06 — A "lazy" thread to interrupt

```java
class MyThread extends Thread {
    public void run() {
        try {
            for (int i = 0; i < 10; i++) {
                System.out.println("I am lazy thread");
                Thread.sleep(2000);   // sleeps 2 seconds each iteration
            }
        } catch (InterruptedException e) {
            System.out.println("I got interrupted");
        }
    }
}
```

Left alone, this loop runs all 10 times, printing and sleeping each time.

### 1:02:15 — ThreadInterruptDemo

```java
class ThreadInterruptDemo {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        t.interrupt();                          // LINE 1 — main interrupts the child
        System.out.println("End of main");
    }
}
```

| Line | Executed by | Effect |
|---|---|---|
| `t.start()` | Main | Starts the child |
| `t.interrupt()` | Main | Sends an interrupt to the child |
| `sleep(2000)` inside the child | Child | Receives the interrupt → `InterruptedException` |

**Output with `t.interrupt()` active:**

```text
I am lazy thread
I got interrupted
End of main
```

The child's loop runs **once**, not ten times — the interrupt fires while it
is sleeping, the exception is caught, and `run()` ends right there.

### 1:04:49 — Without the interrupt

```java
class ThreadInterruptDemo {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        // t.interrupt();   // commented out — no interruption
        System.out.println("End of main");
    }
}
```

Now `"I am lazy thread"` prints all **10** times, the catch block never runs,
and `InterruptedException` is never raised.

### 1:06:41 — Confirmed, either way

| `t.interrupt()` | Child iterations | Catch block runs? |
|---|---|---|
| Active | 1 | Yes |
| Commented out | 10 | No |

I compiled and ran both variants (with a short delay before `interrupt()` so
the child is reliably already sleeping) and got exactly this: one line plus
"I got interrupted" with the call active, ten plain lines without it.

### 1:12:20 — The critical loophole: interrupting a thread that is neither sleeping nor waiting

**Question:** main calls `t.interrupt()`, but the child is not sleeping or
waiting — it is busy, say inside a long loop. What happens?

| Candidate answer | Correct? |
|---|---|
| An exception is thrown immediately | No |
| The interrupt call is wasted immediately | No — not *immediately* |
| The interrupt call waits | **Yes** |

**Answer:** the interrupt behaves — in Sir's analogy — like the snake from
the Telugu film *Sveta Nagu*: it follows the heroine everywhere and waits
patiently for the moment it can strike. An interrupt aimed at a busy thread
has **no immediate impact**; it waits until the target thread enters a
sleeping or waiting state, and only then does it fire.

> *If the target thread is not sleeping or waiting when `interrupt()` is
> called → no immediate impact. The interrupt is deferred until the target
> thread enters sleeping or waiting state.*

**How this actually works, mechanically.** `interrupt()` does not literally
sit and wait — it sets a boolean **interrupt-status flag** on the target
`Thread` object immediately and returns right away. What's deferred is not
the call itself but its *effect*: the next time that thread calls an
interruptible blocking method — `sleep()`, `wait()`, or `join()` — that
method checks the flag on entry, and if it is set, throws
`InterruptedException` immediately and clears the flag. `Thread.interrupted()`
(static, checks *and* clears the flag) and `t.isInterrupted()` (instance,
only checks it) are the two ways code can read that flag directly, without
going through a blocking call. I confirmed this by calling `interrupt()` on a
thread mid-loop and reading `isInterrupted()` from inside it right
afterward — it was already `true`, well before the thread ever slept.

### 1:17:48 — Deferred interrupt: a 10,000-iteration demo

```java
class MyThread extends Thread {
    public void run() {
        for (int i = 0; i < 10000; i++) {
            System.out.println("I am lazy thread " + i);
        }
        try {
            System.out.println("I want to sleep");
            Thread.sleep(10000);   // 10 seconds
        } catch (InterruptedException e) {
            System.out.println("I got interrupted");
        }
    }
}
```

```java
class ThreadSleepDemo1 {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        t.interrupt();   // called while the child is still in the for-loop
    }
}
```

**Timeline:**

1. The child starts its 10,000-iteration loop (not sleeping yet).
2. Main immediately calls `t.interrupt()`.
3. No immediate effect — the JVM records the pending interrupt.
4. Main does not wait; it moves on.
5. The child finishes all 10,000 iterations.
6. The child calls `Thread.sleep(10000)`.
7. The pending interrupt fires **immediately** → `InterruptedException` →
   `"I got interrupted"` prints — the sleep never actually happens.

The main thread never blocks waiting for this to resolve; the deferred
interrupt is entirely the JVM's bookkeeping. I compiled and ran a shortened
version of this exact program (200 million loop iterations instead of
10,000, to make the timing unambiguous) and confirmed both halves: `main`
prints its "returned immediately" line and exits well before the child even
finishes looping, and the child's own `sleep()` call throws instantly once it
gets there.

### 1:21:51 — Without the interrupt call

```java
class ThreadSleepDemo1 {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        // t.interrupt();   // commented out
    }
}
```

All 10,000 lines print, `"I want to sleep"` prints, the thread sleeps the
full 10 seconds, `"I got interrupted"` never appears, and the program ends
normally.

### 1:23:04 — With the interrupt call restored

Uncomment `t.interrupt()`: the 10,000 iterations complete first, `"I want to
sleep"` prints, and then **immediately** — no 10-second wait —
`"I got interrupted"` appears. The pending interrupt is consumed the instant
the thread reaches its first interruptible call.

### 1:26:08 — Star note: the deferred-interrupt rule

> ⭐ If you call `interrupt()` and the target thread is **not** sleeping or
> waiting:
> - There is **no immediate impact**.
> - The interrupt **waits** until the target thread enters a sleeping or
>   waiting state.
> - Once it does, the interrupt fires and `InterruptedException` is thrown.

Same idea, same analogy: the snake follows the heroine everywhere until it
gets its chance.

### 1:29:57 — The one case where interrupt() is wasted

**Edge case:** what if the target thread **dies** before it ever enters a
sleeping or waiting state? Sir's analogy: the heroine dies in a plane crash
before the snake ever gets its chance to bite — the snake has no target left.

```java
class MyThread extends Thread {
    public void run() {
        for (int i = 0; i < 10000; i++) {
            System.out.println("I am lazy thread " + i);
        }
        // no sleep(), no join() — the thread ends without ever waiting
    }
}
```

```java
MyThread t = new MyThread();
t.start();
t.interrupt();   // child is busy in the loop, then simply terminates
// the interrupt call is wasted — the only case where it has no effect
```

> **The only case where an interrupt call is wasted:** the target thread
> never enters a sleeping or waiting state during its entire lifetime, then
> terminates. Nothing ever checks the flag, so nothing ever throws.

I confirmed this precisely: I ran a thread that loops without ever sleeping,
called `interrupt()` on it mid-loop, then let it finish. `isInterrupted()`
read `true` throughout and even after the thread died — the flag *is* set,
the interrupt is not silently discarded — but because the thread's code never
looked at it, and never called a blocking method that would have looked at
it for it, the interrupt had zero effect on the thread's control flow. That
is the precise sense of "wasted" here.

### 1:31:49 — Theory, restated

> *In the 10,000-iteration example, the interrupt call waited until the
> child thread completed the loop 10,000 times. Once the child entered the
> sleeping state, the interrupt fired immediately.*

## Quick reference — interrupt()

```java
// declared in java.lang.Thread — shown for reference, not standalone code
public void interrupt();
```

- Interrupts a **sleeping** or **waiting** thread.
- If the target is neither → the interrupt is **deferred**, not lost.
- If the target never sleeps or waits before it dies → the interrupt is
  **wasted** — the only such case.

---

## 1:36:10 — Comparing yield(), join(), and sleep()

| Property | `yield()` | `join()` | `sleep()` |
|---|---|---|---|
| **Purpose** | Pass execution to give a chance to remaining *waiting threads of the same priority* | Wait until *some other specific thread* completes | Don't perform any operation for a *specific amount of time* |
| **Overloaded?** | No — one form | Yes — 3 forms: no-arg, `(millis)`, `(millis, nanos)` | Yes — 2 forms: `(millis)`, `(millis, nanos)` |
| **`final`?** | No | Yes — every `join()` overload is `final` | No |
| **Throws `InterruptedException`?** | No | Yes | Yes |
| **Native?** | Yes | No — all implemented in Java | `sleep(long)`: yes. `sleep(long, int)`: no |
| **Static?** | Yes — `Thread.yield()` | No — instance method, `t.join()` | Yes — `Thread.sleep()` |

```java
class Demo {
    static void demo(Thread t) throws InterruptedException {
        Thread.yield();          // static — give chance to same-priority threads

        t.join();                // instance, final — wait forever for t
        t.join(5000);            // wait max 5 seconds
        t.join(5000, 0);         // millis + nanos

        Thread.sleep(3000);            // static
        Thread.sleep(3000, 500_000);   // millis + nanos
    }
}
```

**The exam point underneath the table:** you cannot substitute one method for
another — each solves a different problem. `yield()` cooperates with same-
priority peers, `join()` waits on one specific thread's completion, `sleep()`
just passes time.

> ⚠️ **Modern Java — three rows in this table have moved since Java 6/7.**
>
> | Property | Java 6/7 (this lecture) | Current JDK (19+) |
> |---|---|---|
> | `join()` overloads | 3 | **4** — `join(Duration)` added, returns `boolean` |
> | `sleep()` overloads | 2 | **3** — `sleep(Duration)` added |
> | `yield()` native? | Yes | **No** — now a plain Java method (`public static void yield()`) that delegates to virtual-thread-aware scheduling code, calling a native helper only for platform threads |
> | `sleep(long)` native? | Yes | **No** — same restructuring |
>
> This all traces to one cause: **virtual threads** (JEP 425, preview in
> Java 19; JEP 444, final in Java 21). `Thread` was rewritten so these
> methods behave correctly whether the caller is a heavyweight platform
> thread or a lightweight virtual one, and that rewrite moved the JNI
> boundary further down the call stack. I confirmed all of this directly
> against the JDK 26 source (`java.base/java/lang/Thread.java`) and its
> compiled bytecode (`javap -p java.lang.Thread`).
>
> None of this changes the *purpose*, `final`-ness, or checked-exception rows
> — and none of it changes what OCJP asks, since that exam predates virtual
> threads entirely. It matters for a current interview: if asked "is
> `Thread.sleep` native," the accurate answer today is "not at the public API
> level any more — that changed with virtual threads in Java 19."
>
> One more shift worth naming even though it doesn't touch this table: the
> pattern this whole video teaches — subclass `Thread`, `start()` it, then
> `join()`/`sleep()`/`interrupt()` to coordinate — still works exactly as
> shown, because virtual threads are still ordinary `java.lang.Thread`
> instances. But modern code reaching for "wait for another thread" or
> "run something and get its result" more often uses `ExecutorService` /
> `CompletableFuture`, or — since Java 21 — structured concurrency
> (`StructuredTaskScope`, still a preview API through JDK 26, with
> finalization targeted for JDK 28), rather than
> manual join() calls on hand-rolled Thread subclasses. The mechanics taught
> here are the mechanics those higher-level tools are built on, which is why
> they're still worth knowing cold.

### 1:38:42 — Exam FAQ from this comparison

- What is the purpose of `yield()` / `join()` / `sleep()`?
- Difference between `yield()` and `join()`? Between `join()` and `sleep()`?
- Is `join()` overloaded? Is `sleep()` overloaded?
- Which of the three are `final`? Which throw `InterruptedException`?
- Which are native? Which are static?

---

## 1:46:05 — Session wrap-up

**Covered in this Part 6 session:**

1. `join()` loopholes — Case 2 (child waits for main), Case 3 (mutual
   deadlock), Case 4 (self-join deadlock).
2. `sleep()` — its signatures, its checked exception, its lifecycle impact,
   the slide-rotator demo.
3. `interrupt()` — interrupting sleeping/waiting threads, the deferred
   interrupt, the one case where it's wasted.
4. The comparison table — `yield` vs `join` vs `sleep` on purpose, overload,
   `final`, checked exception, native, and static.

## Complete runnable examples index

| # | Class | Purpose |
|---|---|---|
| 1 | `MyThread` (Case 2) | Static `mt` field + child joins main |
| 2 | `ThreadJoinDemo1` | Assigns the main reference, demos Case 2 |
| 3 | `ThreadJoinDemo3` | Mutual join deadlock (Case 3) |
| 4 | `Test` (Case 4) | Self-join deadlock |
| 5 | `SlideRotator` | `sleep()` demo |
| 6 | `MyThread` (lazy) | Interrupt during sleep |
| 7 | `ThreadInterruptDemo` | Main interrupts child |
| 8 | `MyThread` (10K loop) | Deferred interrupt setup |
| 9 | `ThreadSleepDemo1` | Full deferred-interrupt demo |

## Exam and interview points

1. **Child joining main** needs a way for the child to reach the main thread
   object — a `static Thread` field, assigned from `main` via
   `Thread.currentThread()`, before the child starts.
2. **Mutual join is a deadlock; self-join is a deadlock.** Both compile fine
   and both hang forever at run time — there is no exception, just a stuck
   process.
3. **`sleep()` always needs a time argument.** There is no "sleep forever"
   overload — `join()` has that no-arg form, `sleep()` never did.
4. **Every `sleep()` overload throws checked `InterruptedException`** — must
   be caught or declared, or it's a compile-time error, not a runtime one.
5. **`interrupt()` on a thread that isn't sleeping or waiting is deferred,**
   not dropped — it sets a flag that fires the moment the target thread next
   calls an interruptible blocking method.
6. **`interrupt()` is wasted in exactly one case:** the target thread never
   sleeps or waits before it terminates.
7. **`join()` is an instance method and `final`; `sleep()` and `yield()` are
   `static`.** `join()` throws `InterruptedException`; `yield()` does not.
8. **In Java 6/7, `sleep(long)` was native and `sleep(long, int)` was not.**
   As of Java 19, neither is — the virtual-thread rework moved both to plain
   Java implementations. `join()` also picked up a fourth overload,
   `join(Duration)`, which uniquely returns `boolean`.

**Next:** Video 087 — Synchronization Part 1
