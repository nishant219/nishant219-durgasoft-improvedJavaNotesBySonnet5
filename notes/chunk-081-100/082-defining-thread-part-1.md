# Video 082 — Ways of defining a Thread Part-1

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-2 || The ways of defining a Thread Part-1

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 82 of 203 |
| Series | Multi Threading · Part 2 |
| Topic | Defining a thread by extending Thread; thread scheduler; start vs run; overloading run; overriding start; life cycle; IllegalThreadStateException |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 44m 56s |
| Video ID | fd3TAYCHRfw |
| Watch URL | https://www.youtube.com/watch?v=fd3TAYCHRfw |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

### 00:10 — Recap from Part-1

Already covered: multitasking, process-based vs thread-based multitasking, and
why thread-based wins at the programmatic level — the main advantage is
**performance** (the overall task finishes in less time).

Now: what is a thread, and **in how many ways** can we define one.

### 01:00 — What is a thread?

Sir will use the word "thread" thousands of times over the two days. Students
offer synonyms — flow of execution, independent job, lightweight process — and
all of them are valid.

Working definition: a **thread is a separate flow of execution**. One flow
means single-threaded (just the main thread); multiple flows mean multiple
threads, each carrying a **separate job**. Two independent jobs mean two
threads, both executing simultaneously, so the overall job finishes sooner.

### 03:54 — Board: Defining a thread — two ways

We can define a thread in **two ways**:

1. By **extending the `Thread` class**
2. By **implementing the `Runnable` interface**

This video covers the first way in depth — it is the foundation the rest of
multi-threading is built on. Implementing `Runnable` is Part-3.

> ⚠️ **Modern Java — a third way exists now: virtual threads.**
> Since **Java 21** (JEP 444), `Thread.ofVirtual().start(runnable)` or
> `Executors.newVirtualThreadPerTaskExecutor()` hands you a thread-like unit of
> execution without touching `Thread` or `Runnable` at the class-declaration
> level at all. It is not a third way of *defining* a thread in Sir's sense —
> you still typically pass a `Runnable` — but it is a third way of *obtaining*
> one, and it is the modern default for I/O-bound concurrency (thousands of
> cheap virtual threads instead of a small pool of expensive platform
> threads). The extends-`Thread` / implements-`Runnable` split taught here is
> still exactly right for platform threads, and every case in this video
> applies unchanged to them.

### 06:03 — First approach: extend Thread, override run

```java
class MyThread extends Thread {
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println("Child Thread");
        }
    }
}
```

- Write a class that **extends `Thread`**.
- **Override `run`** (it is already declared in `Thread`, doing nothing).
- The code inside `run` is the **job of the thread** — start this thread and
  it performs this job.
- Writing such a class is called **defining a thread**; the job itself is
  defined **inside `run`**.

### 08:37 — ThreadDemo: instantiate and start

```java
class ThreadDemo {
    public static void main(String[] args) {
        MyThread t = new MyThread(); // main thread creates the child thread object
        t.start();                   // main thread starts the child thread
        for (int i = 0; i < 10; i++) {
            System.out.println("Main Thread");
        }
    }
}
// mixed output — no guaranteed order
```

Key vocabulary:

- Before any of this runs, there is **one** thread — the **main thread**
  (daemon threads such as the garbage collector run internally too; covered
  later). The main thread executes `main`.
- `new MyThread()`, executed by main, is **thread instantiation** — main
  creates the child thread object.
- `t.start()`, executed by main, **starts** the child thread. After it
  returns, there are **two** threads: main and child.
- The child executes `run` (the `"Child Thread"` loop); main executes the rest
  of its own code (the `"Main Thread"` loop). Both run simultaneously, so the
  console output is **mixed**.

**Main method ≠ main thread.** The main method is code; the **main thread** is
what executes it.

Mixed order is fine here because the two loops are **independent jobs** — if
order mattered (one job depended on the other), this style of multi-threading
would be the wrong tool.

### 19:11 — Case 1: The thread scheduler

- The thread scheduler is responsible for deciding, when multiple threads are
  waiting for a turn, **which one runs next**.
- Its algorithm (FCFS, round robin, shortest-job, …) is **not specified by the
  language** — it varies by JVM/OS, so you cannot rely on any particular
  scheduling policy.
- Consequently, there is **no guaranteed output** for a multi-threaded
  program — only a set of *possible* outputs.
- OCJP/SCJP asks "which of the following is a **possible** output," never
  "what is **the** output," for a multi-threaded example.

Demo: running the same `MyThread` / `ThreadDemo` program repeatedly produces
Main-then-Child, Child-then-Main, and interleaved patterns on different runs.

> ❗ **Correction — "the thread scheduler is part of the JVM" is not quite where the decision is made.**
> For ordinary (**platform**) threads, HotSpot maps each Java thread 1:1 onto a
> native OS thread — has done so since Java 1.2, replacing the old green-thread
> model. The **operating system's** scheduler, not the JVM's, actually decides
> which thread runs when; the JVM just requests OS threads and stays out of
> the way. The exam-relevant conclusion Sir draws — *no guaranteed order,
> policy varies by platform* — is completely correct; only the "which
> component owns the algorithm" detail needed fixing.
>
> ⚠️ **Modern Java — virtual threads do have a real JVM-level scheduler.**
> Virtual threads (Java 21) are scheduled **by the JVM's own runtime**, not the
> OS: many virtual threads are multiplexed onto a small pool of platform
> "carrier" threads via a `ForkJoinPool`-based work-stealing scheduler. So the
> "scheduler lives inside the JVM" mental model Sir teaches — not quite true
> for platform threads — becomes literally true for virtual threads.

### 27:31 — Possible outputs for the above program

Any interleaving of ten `"Main Thread"` and ten `"Child Thread"` lines is a
valid possible output, including:

| # | Pattern |
|---|---|
| 1 | Main Thread ×10, then Child Thread ×10 |
| 2 | Child Thread ×10, then Main Thread ×10 |
| 3 | Main, Child, Main, Child, … alternating |
| 4 | Child, Main, Child, Main, … alternating |
| 5 | Any other mix (Main ×2, Child ×2, …) |

If a student asks "with no guarantee, how do we use this in real apps?" —
when the jobs are genuinely independent, the order never mattered in the
first place.

### 31:17 — Case 2: `t.start()` vs `t.run()`

An interview favorite.

**`t.start()`:** `t` has no `start` method of its own, so Java resolves it to
`Thread.start()` — which does the setup work and then **internally calls
`run()`** on a **new** thread.

**`t.run()`, called directly:** `run` executes as an **ordinary method call**
on whichever thread called it (here, main). **No new thread is created.**

```java
class MyThread extends Thread {
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println("Child Thread");
        }
    }
}

class ThreadDemo {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.run(); // NOT t.start()
        for (int i = 0; i < 10; i++) {
            System.out.println("Main Thread");
        }
    }
}
// Child Thread ×10, then Main Thread ×10 — every run, every machine
// (only one thread ever exists, so there is nothing to interleave with)
```

Swap `t.start()` for `t.run()` and the output becomes deterministic — Child
Thread ten times, then Main Thread ten times — because the whole program now
runs on a single thread.

### 41:03 — Case 3: Why `start()` matters

Why must you call `start()` at all, rather than just `run()`?

Sir's analogy: you cannot drop a child at the school gate and declare them a
student — admission formalities have to happen first, and only then does the
school recognize the child. A thread needs the equivalent "joining
formalities" — registering with the scheduler and so on — before its job can
run as a real thread. You call `t.start()`; `Thread.start()` performs those
formalities and only then invokes `run()`.

```java
// Conceptual contents of Thread.start(), as Sir describes it —
// not literal JDK source:
/*
1. register this thread with the thread scheduler
2. perform the other mandatory setup for this thread
3. invoke run()
*/
```

Skip `start()` and there is **no way to start a new thread in Java** — which
is why Sir calls `Thread.start()` the **heart of multi-threading** (and jokes
that it hides "70,000 lines" you'd hate to write by hand).

### 51:44 — Case 4: Overloading `run`

```java
class MyThread extends Thread {
    public void run() {
        System.out.println("no-arg run");
    }

    public void run(int i) {
        System.out.println("int-arg run");
    }
}

class ThreadDemo {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
    }
}
// prints: no-arg run
```

Overloading `run` is perfectly legal — it is just a method name, and Java
allows any number of overloads. But `Thread.start()` is hard-wired to invoke
the **no-argument `run()`** only; any other overload has to be called
explicitly, like a normal method. It is the same rule as overloading `main`:
you may write `main(int i)` too, but the JVM only ever calls
`main(String[] args)`.

### 1:00:20 — Case 5: Not overriding `run`

```java
class MyThread extends Thread {
    // no run() override
}

class Test {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
    }
}
// (no output)
```

Perfectly valid: `start()` still runs, still calls `run()` — but it is
`Thread`'s own empty `run()`, so nothing prints. It is **strongly
recommended** to override `run`; skipping it means the thread has no job,
which defeats the point of writing one.

### 1:06:08 — Case 6: Overriding `start`

```java
class MyThread extends Thread {
    public void start() {
        System.out.println("start method");
    }

    public void run() {
        System.out.println("run method");
    }
}

class Test {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        System.out.println("main method");
    }
}
// start method
// main method
// (all of it produced by the main thread — run() never fires)
```

`t.start()` now resolves to `MyThread`'s own `start` — `Thread.start()` never
gets a chance to run, so **no new thread is created** and `run()` is never
invoked through the scheduler path. The overridden `start` executes as an
ordinary method; control then returns to main, which prints `"main method"`.
Same output on every run, because only the main thread ever exists.

**Overriding `start` is not recommended** — it defeats multi-threading
entirely.

### 1:15:31 — Case 6 continued: calling `super.start()`

Add one line — call `Thread`'s own `start` from inside the override:

```java
class MyThread extends Thread {
    public void start() {
        super.start(); // now Thread.start() runs too, on a new child thread
        System.out.println("start method");
    }

    public void run() {
        System.out.println("run method");
    }
}

class Test {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        System.out.println("main method");
    }
}
```

Now `super.start()` really does start a child thread, so two threads exist:
the child runs `run()`; main falls through the rest of `MyThread`'s `start`
body (`"start method"`) and then prints `"main method"`.

Only **three** outputs are possible:

1. `run method` → `start method` → `main method`
2. `start method` → `main method` → `run method`
3. `start method` → `run method` → `main method`

`"start method"` and `"main method"` are both produced by main, in that
order, on every run — they can never swap. Only the child's `"run method"`
line is free to land anywhere relative to them.

### 1:25:29 — Case 8: Thread life cycle (top level)

```java
MyThread t = new MyThread(); // New / Born state
t.start();                   // Ready / Runnable state
// scheduler allocates a processor → Running state (run() executing)
// run() completes           → Dead state
```

1. `new MyThread()` → **New / Born**
2. `t.start()` → **Ready / Runnable**
3. Scheduler allocates a processor → **Running**
4. `run()` completes → **Dead**

This is the simplified version. Later topics (`sleep`, `join`, `wait`,
`yield`) add intermediate waiting states to this picture; for now, this
four-state view is enough.

### 1:32:20 — Case 9: Restarting a thread → `IllegalThreadStateException`

Interview point: once a thread has been started, you cannot start the **same**
thread object a second time.

```java
class MyThread extends Thread {
    public void run() {
        System.out.println("run method");
    }
}

class Test {
    public static void main(String[] args) {
        MyThread t = new MyThread();
        t.start();
        t.start(); // second start on the same thread object
    }
}
// compiles fine
// at runtime: IllegalThreadStateException
```

Verified: on current JDKs this still throws `IllegalThreadStateException` at
the second `start()` call — the check and the exception are unchanged since
this recording.

### 1:44:26 — Close of Part-2

That covers every case tied to defining and starting a thread by **extending
`Thread`**. Next video: the second way — implementing `Runnable`.

---

## Exam and interview points

1. **Two ways to define a thread**: extend `Thread` and override `run`, or
   implement `Runnable`. This video is the first way only.
2. **`start()` vs `run()`** is a guaranteed interview question: `start()`
   creates a new thread and lets the scheduler invoke `run()` on it;
   calling `run()` directly is an ordinary method call on the current thread
   — no new thread, deterministic output.
3. **Overloaded `run` methods are legal, but only the no-arg `run()` ever
   gets called by `start()`** — exactly like `main`, where only
   `main(String[] args)` is special to the JVM.
4. **Not overriding `run`** compiles and runs — it just does nothing, because
   you're calling `Thread`'s own empty `run()`.
5. **Overriding `start` without `super.start()`** means no new thread is ever
   created; your override just runs as a plain method on the caller's thread.
   Call `super.start()` if you still want the real threading behavior.
6. **Restarting an already-started thread throws `IllegalThreadStateException`**
   at runtime — the program still compiles.
7. **No guaranteed output for multi-threaded code.** The scheduling policy is
   unspecified and platform-dependent; OCJP asks for a *possible* output,
   never *the* output.
8. **Simplified life cycle**: New → Runnable → Running → Dead. `sleep`,
   `join`, `wait`, and `yield` add more states, covered in later videos.
9. Know the modern landscape too: since **Java 21**, virtual threads give you
   a lightweight alternative to platform threads with their own JVM-level
   scheduler — useful context if an interviewer asks "how would you do this
   today."

---

**Next:** Video 083 — Ways of defining a Thread Part-2
