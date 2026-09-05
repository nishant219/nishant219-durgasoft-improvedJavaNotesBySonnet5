# Video 083 — Ways of defining a Thread Part-2

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-3 || The ways of defining a Thread Part-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 83 of 203 |
| Series | Multi Threading · Part 3 |
| Topic | Defining a thread by implementing Runnable; case study start/run; which approach is best; Thread constructors; Durga's hybrid approach; get/set name; currentThread |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 18m 54s |
| Video ID | 8xnNgR0zeS8 |
| Watch URL | https://www.youtube.com/watch?v=8xnNgR0zeS8 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

## What this lecture covers

Part 2 of "ways of defining a thread." The first video covered `extends Thread`;
this one covers the second, recommended approach — `implements Runnable` — then
runs a six-case study of `start()` vs `run()` with and without a target
Runnable, settles the "which approach is best" interview question, lists
Thread's constructors, shows Durga's own hybrid (valid but non-standard) way
of wiring the two approaches together, and closes with getting/setting a
thread's name and `Thread.currentThread()`.

---

## 00:08 — Defining a thread by implementing Runnable

Sir puts the two approaches side by side. `Thread` itself already implements
`Runnable`, so approach one gets `run()` for free through inheritance:

```java
// First approach (reminder)
class MyThread extends Thread {
    public void run() { /* job */ }
}

// Second approach — implement Runnable directly, without touching Thread
class MyRunnable implements Runnable {
    public void run() { /* job */ }
}
```

### 03:47 — `Runnable` interface facts

- Lives in **`java.lang`**.
- Contains exactly **one** method.

```java
// java.lang.Runnable
public void run();
```

> ⚠️ **Modern Java — `Runnable` is now a `@FunctionalInterface`.**
> Since **Java 8**, a single-abstract-method interface can be implemented with
> a lambda instead of a named class. Sir's `MyRunnable` class is still exactly
> how the OCJP exam (and most legacy code) expects it, but day-to-day code
> today usually writes:
>
> ```java
> Runnable r = () -> {
>     for (int i = 0; i < 10; i++) System.out.println("Child Thread");
> };
> new Thread(r).start();
> ```
>
> Same target Runnable, same `start()`/`run()` rules below — a lambda is just
> a shorthand for the anonymous-class version of `MyRunnable`.

### 05:07 — Full second-approach example

```java
class MyRunnable implements Runnable {
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println("Child Thread");
        }
    }
}

class ThreadDemo {
    public static void main(String[] args) {
        MyRunnable r = new MyRunnable();   // main thread creates the MyRunnable object
        Thread t = new Thread(r);          // r becomes the target Runnable
        t.start();
        for (int i = 0; i < 10; i++) {
            System.out.println("Main Thread");
        }
    }
}
// output is interleaved — "Child Thread" and "Main Thread" lines mix unpredictably
```

Only one word changes between the two approaches: `implements Runnable`
instead of `extends Thread`. Sir's framing stays the same as Part 1: the code
inside `run()` is the **job** of the thread; the whole class that carries it is
what "defining a thread" means.

His car analogy for why `Thread` is still needed even though you're not
extending it: creating `new MyRunnable()` is like a car rolling off the line —
ready, but with no engine to drive it. `MyRunnable` has no `start()` (neither
does its parent interface `Runnable`), so you hand the "car" to something that
*can* start it — a `Thread`:

```java
Thread t = new Thread();
t.start();
// Thread's own run() runs — empty body, no visible output — not MyRunnable's run()
```

Only once `r` is passed into the constructor does `t.start()` end up calling
**`MyRunnable`'s `run()`**. That `r` is called the thread's **target
Runnable**. After `t.start()` there are two live threads: main finishes its
own loop, the new thread runs `run()`.

Sir also flags, in passing, that restarting an already-started thread — same
as covered in Part 1 — throws `IllegalThreadStateException`; that rule doesn't
change based on which approach defined the thread.

---

## 16:32 — Case study: with vs without a Runnable argument

```java
MyRunnable r = new MyRunnable();
Thread t1 = new Thread();    // no target Runnable
Thread t2 = new Thread(r);   // target Runnable is r
```

Six calls, six outcomes:

| # | Call | New thread? | What actually runs |
|---|---|---|---|
| 1 | `t1.start()` | ✅ yes | `Thread`'s own `run()` — empty, so effectively nothing |
| 2 | `t1.run()` | ❌ no | `Thread`'s `run()` as a plain method call on the calling thread |
| 3 | `t2.start()` | ✅ yes | `MyRunnable`'s `run()` — the correct, intended way |
| 4 | `t2.run()` | ❌ no | `MyRunnable`'s `run()` as a plain method call on the calling thread |
| 5 | `r.start()` | — | **compile error** — `MyRunnable` has no `start()` |
| 6 | `r.run()` | ❌ no | `MyRunnable`'s `run()` as a plain method call |

```java
r.start();
// CE: cannot find symbol
//   symbol:   method start()
//   location: variable r of type MyRunnable
```

The pattern to memorise: **`start()` always spins up a new thread; `run()`
called directly is just an ordinary method call on whichever thread is already
executing.** Whether the job that runs is `Thread`'s (empty) or `MyRunnable`'s
depends only on whether a target Runnable was passed to the `Thread`
constructor — nothing else changes that. `Runnable` itself never gained a
`start()` method; the reason a `Thread` wrapper is required is unchanged from
1997.

---

## 30:11 — Which approach is best? (interview question)

Sir's drill: "in how many ways can you define a thread" → two. "Which is
recommended" → **implementing `Runnable`**. The reasoning he wants recited:

- **`extends Thread`**: the class's single shot at extending something is
  spent on `Thread`. Java has no multiple inheritance of classes, so this
  class can never extend anything else — you lose the option of inheriting
  from a more useful superclass.
- **`implements Runnable`**: implementing an interface costs nothing in
  Java's single-inheritance-of-class model. The class is free to `extends`
  some other class *and* implement `Runnable` at the same time.

```java
// First approach — inheritance already "spent" on Thread
class MyThread extends Thread {
    public void run() { /* job */ }
}

// Second — free to extend something else too
class MyRunnable extends SomeOtherClass implements Runnable {
    public void run() { /* job */ }
}
```

Sir adds, without going into specifics, that there are also reported
memory- and performance-level reasons favouring `Runnable`, but the
inheritance argument is the one to give in an interview.

> ⚠️ **Modern Java — the recommendation got a second, sharper reason: virtual threads.**
> Since **Java 21** (JEP 444), `Thread.ofVirtual()` and `Thread.ofPlatform()`
> are the standard way to build threads, and their builder only accepts a
> `Runnable` — there is no hook for a `Thread` subclass's overridden `run()`:
>
> ```java
> Thread vt = Thread.ofVirtual().start(() -> System.out.println(
>         "running on " + Thread.currentThread()));
> vt.join();
> // running on VirtualThread[#27]/runnable@ForkJoinPool-1-worker-1
> ```
>
> A lightweight virtual thread (you can run millions of them) is reachable
> only through the Runnable-based APIs. So "implement `Runnable`, don't extend
> `Thread`" isn't just cleaner OOP any more — it's the only style that also
> works with virtual threads. `extends Thread` still compiles and still works
> for classic platform threads; it just cannot opt into this newer model.

---

## 38:24 — Thread class constructors

Sir lists every constructor `Thread` carries, whether a given program uses it
or not:

```java
Thread t = new Thread();
Thread t = new Thread(Runnable r);
Thread t = new Thread(String name);
Thread t = new Thread(Runnable r, String name);
Thread t = new Thread(ThreadGroup g, String name);
Thread t = new Thread(ThreadGroup g, Runnable r);
Thread t = new Thread(ThreadGroup g, Runnable r, String name);
Thread t = new Thread(ThreadGroup g, Runnable r, String name, long stackSize);
```

Board notes as he goes:

- Every thread has a **name** — default or programmer-supplied.
- Every thread belongs to some **`ThreadGroup`** — a way to group threads by
  functionality.
- For every thread the JVM allocates a **runtime stack**; the last
  constructor is the only one that lets you request a specific stack size.
- Total: **eight** constructors.

> ❗ **Correction — it's nine constructors now, and one changed meaning.**
> Confirmed against `java.lang.Thread` on a current JDK (`javap -p
> java.lang.Thread`): Sir's eight are still exactly there, unchanged. **Java 9**
> added a ninth public constructor:
>
> ```java
> public Thread(ThreadGroup group, Runnable target, String name,
>               long stackSize, boolean inheritInheritableThreadLocals)
> ```
>
> The extra `boolean` lets you opt a thread *out* of inheriting the creating
> thread's `InheritableThreadLocal` values — something none of the original
> eight could express. For OCJP/SCJP (Java 6/7-era), eight is the correct
> count; for a current interview, nine.

> ⚠️ **Modern Java — `ThreadGroup` is legacy, and there's a newer, nicer way to configure a thread.**
> `ThreadGroup`'s job (grouping threads, bulk operations like `stop()`/
> `suspend()`) has been superseded by the `java.util.concurrent` executor
> framework since Java 5, and most of its bulk-control methods are
> deprecated. It is not removed and Sir's constructors above still compile
> and work — this is background, not a correction to what he taught. Since
> **Java 21**, the readable way to build a configured thread is the builder
> API instead of memorising an eight/nine-constructor table:
>
> ```java
> Thread t = Thread.ofPlatform()
>                   .name("worker")
>                   .unstarted(() -> System.out.println("job"));
> t.start();
> ```
>
> `Thread.ofVirtual()` is the same builder shape for virtual threads. The
> constructor list above is still exam material and still valid Java; the
> builder is what new code reaches for.

---

## 45:49 — Durga's hybrid approach (valid, not recommended)

Sir shows a third wiring: **define** the thread with approach 1
(`extends Thread`) but **start** it the way approach 2 does — wrap the object
in `new Thread(target)` and start that wrapper instead:

```java
class MyThread extends Thread {
    public void run() {
        System.out.println("Child Thread");
    }
}

class ThreadDemo {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        Thread t1 = new Thread(t);   // t is-a Runnable, so it's a valid target
        t1.start();
        System.out.println("Main Thread");
    }
}
// "Child Thread" and "Main Thread" can print in either order
```

Why this compiles at all: `MyThread extends Thread`, and `Thread implements
Runnable`, so a `MyThread` object **is-a** `Runnable` — perfectly legal to
pass into `new Thread(...)`. Definition style borrowed from approach 1,
start-up style borrowed from approach 2. Sir's exam warning: if OCJP/SCJP
shows you this hybrid, **do not** mark it invalid — it compiles and runs. It
is simply not the pattern he teaches as standard, because it gains none of
approach 2's inheritance benefit while adding an extra, needless `Thread`
wrapper object.

---

## 51:19 — Getting and setting a thread's name

Every thread carries a name — either a JVM-generated default or one the
programmer sets. Two `final` methods handle both directions:

```java
public final String getName()
public final void setName(String name)
```

```java
class MyThread extends Thread {
    // run() intentionally omitted here — this demo is only about names
}

class Test {
    public static void main(String[] args) {
        System.out.println(Thread.currentThread().getName());
        // main

        MyThread t = new MyThread();
        System.out.println(t.getName());
        // Thread-0

        // a second MyThread here would print Thread-1, and so on

        Thread.currentThread().setName("Pavan Kalyan");
        System.out.println(Thread.currentThread().getName());
        // Pavan Kalyan
    }
}
```

Default child-thread names run `Thread-0`, `Thread-1`, `Thread-2`, … in
creation order. Even the **main** thread's name can be changed — it is not
special in this respect. Sir's live demo of that: rename `main`, then force an
exception, to show the new name surfaces in the crash trace too:

```java
Thread.currentThread().setName("Pavan Kalyan");
System.out.println(10 / 0);
```

```text
Exception in thread "Pavan Kalyan" java.lang.ArithmeticException: / by zero
	at Test.main(Test.java:4)
```

The thread name printed in an uncaught-exception trace is whatever
`getName()` currently returns for that thread — `"main"` only because nobody
renamed it first.

---

## 1:08:25 — `Thread.currentThread()`

A **static** method on `Thread` that returns a reference to the thread that is
currently executing — whichever thread reaches that line of code:

```java
class MyThread extends Thread {
    public void run() {
        System.out.println(
            "run method executed by the thread "
                + Thread.currentThread().getName());
    }
}

class Test {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        System.out.println(
            "main method executed by the thread "
                + Thread.currentThread().getName());
    }
}
// order between the two println lines is not guaranteed
// one line reads: run method executed by the thread Thread-0
// the other reads: main method executed by the thread main
```

Inside `main`, `currentThread()` resolves to the **main** thread. Inside
`run()` — once it is actually running as a thread via `start()` — it resolves
to that **child** thread (`Thread-0`, by default). Same method, different
answer, purely based on who called it.

---

## 1:18:31 — Close of Part-3

Sir recaps: getting and setting a thread's name, and getting the current
executing thread's reference via `Thread.currentThread()`, are both covered.
Thread priorities are next in the series.

---

## Exam and interview points

1. **`Runnable` has exactly one method, `run()`, in `java.lang`** — implementing
   it directly is the second way to define a thread, and (since Java 8) it is
   a `@FunctionalInterface`, so a lambda can stand in for the whole class.
2. **`start()` always creates a new thread; `run()` called directly never
   does** — it just runs as an ordinary method call on the calling thread.
   This holds regardless of which approach (`extends Thread` or `implements
   Runnable`) defined the class.
3. **A `Thread` created with no target Runnable runs `Thread`'s own empty
   `run()`.** Pass a `Runnable` to the constructor and that object becomes
   the **target Runnable**, whose `run()` is what actually executes.
4. **`Runnable` has no `start()` method** — calling `.start()` on a plain
   `Runnable`/`MyRunnable` reference is a compile error, not a runtime one.
5. **Implementing `Runnable` is the recommended way to define a thread**,
   because `extends Thread` spends the class's one shot at inheritance,
   while `implements Runnable` leaves it free to extend something else.
   Since Java 21, virtual threads sharpen this further: they can only be
   built from a `Runnable`, never from a `Thread` subclass's `run()`.
6. **`Thread` has eight constructors** for the OCJP/SCJP era this course
   targets (no-arg; `Runnable`; `String`; `Runnable+String`;
   `ThreadGroup+String`; `ThreadGroup+Runnable`; `ThreadGroup+Runnable+String`;
   `ThreadGroup+Runnable+String+stackSize`). **Since Java 9 there is a ninth**,
   adding a trailing `boolean inheritInheritableThreadLocals`. Know both counts
   and which one is being asked for.
7. **A class can define a thread one way and start it another** — Durga's
   hybrid (`extends Thread`, but wrap the instance in `new Thread(target)`
   before calling `start()`) compiles and runs because a `Thread` subclass
   is-a `Runnable`. Valid on the exam; not the recommended teaching pattern.
8. **`getName()`/`setName(String)` are both `public final`**, work on any
   thread including `main`, and default child names are `Thread-0`,
   `Thread-1`, … in creation order.
9. **`Thread.currentThread()` is `static`** and returns whichever thread is
   executing the line that calls it — it answers differently depending on
   whether it's read from `main` or from inside a running `run()`.

**Next:** Video 084 — Thread Priorities
