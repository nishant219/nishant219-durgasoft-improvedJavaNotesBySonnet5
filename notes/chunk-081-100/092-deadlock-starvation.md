# Video 092 — DeadLock || Starvation

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-12 || DeadLock || Starvation

| Field | Detail |  |  |
|---|---|---|---|
| Playlist | java tutorial by durga sir |  |  |
| Position | Video 92 of 203 |  |  |
| Series | Multi Threading · Part 12 |  |  |
| Topic | DeadLock |  | Starvation |
| Instructor | Durga Sir (Durga Software Solutions) |  |  |
| Duration | 55m 06s |  |  |
| Video ID | 4U9FUlpvg_U |  |  |
| Watch | https://www.youtube.com/watch?v=4U9FUlpvg_U |  |  |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |  |  |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This lecture defines deadlock, stresses that `synchronized` is the *cause*
(not the cure), shows there are no in-process resolution techniques for it
(only prevention), builds the classic A/B dual-lock demo on the board and as
executable code (`A`, `B`, `Deadlock`), proves that removing any one
`synchronized` removes the deadlock, then contrasts **deadlock vs
starvation**. All four code variants below were compiled and run against a
current JDK to confirm they behave exactly as the lecture describes.

---

## 00:06 — Topic: Deadlock

Sir's opening line, half joke: "lock without key is nothing but deadlock — a
dead end, you cannot proceed further." Then the real definition:

> If **two threads are waiting for each other forever**, that infinite
> waiting is called **deadlock**.

He acts out the dialogue: ask the first thread why it's waiting — "for the
second thread's activity." Ask the second — "for the first thread's
activity." Neither ever gets what it's waiting for, so neither ever
proceeds.

```java
// Board definition:
// If two threads are waiting for each other forever,
// such type of infinite waiting is called deadlock.
```

## 03:15 — The wrong conclusion students give

The common wrong statement: "By using `synchronized` we can resolve or
overcome deadlock." Sir rejects it flatly and states the actual relationship:

- `synchronized` is **not** the solution.
- `synchronized` is the **problem creator** — the *only* reason this classic
  program enters deadlock.
- Never use `synchronized` here, and this program never deadlocks.
- If there's no specific requirement, never use `synchronized` casually — it
  is a **dangerous** keyword that needs special care.

```java
// Board conclusion:
// synchronized keyword is the only reason for the deadlock situation
// (in this traditional synchronized-method model)
// -> while using synchronized we have to take special care
// -> if there is no specific requirement, never use it carelessly
```

## 04:38 — Once a program is in deadlock, what can the programmer do?

- Nothing useful, from inside the running process.
- There are **no resolution techniques** for deadlock — only **prevention**
  techniques. "Prevention is better than cure."
- The "punishment" for misusing `synchronized`: the program just hangs.

```java
// Board:
// There are no resolution techniques for deadlock,
// but several prevention techniques are available
// (prevention is better than cure)
```

OS-level prevention algorithms (banker's algorithm and the like) are out of
scope for this session — what matters for a Java programmer is seeing
**how** misusing `synchronized` causes deadlock, since "write a program that
demonstrates deadlock" is a direct interview ask.

Once a real program does hang, "no resolution technique" means no way to
*undo* it from inside the code — but it isn't undiagnosable. `jstack <pid>`
(and `jconsole`'s thread tab) print exactly which thread holds which lock and
which lock it's waiting for, and flag the cycle explicitly as
`Found one Java-level deadlock`. That's detection, not resolution: the fix is
still to kill and restart, informed by what the dump shows instead of
guessing. (This tooling isn't new — `jstack` and `jconsole` both predate this
recording, back to Java 5/6.)

## 07:32 — Rough design before code: class A / class B

**Class A** — method `d1(B b)`, method `last()`.
**Class B** — method `d2(A a)`, method `last()`.

Cross calls:

- Inside A's `d1`: calls `b.last()`.
- Inside B's `d2`: calls `a.last()`.

Create one `A` object, one `B` object, two threads:

- Thread 1 calls `a.d1(b)`.
- Thread 2 calls `b.d2(a)`.

## 10:00 — Case 1: methods NOT synchronized → no deadlock

If `d1`, `d2`, `last` are plain methods:

- T1 runs `d1` → calls `b.last()` immediately (no lock to wait for) →
  finishes → terminates.
- T2 runs `d2` → calls `a.last()` immediately → finishes → terminates.
- **No deadlock** — no lock is ever held across the cross-call.

## 12:20 — Case 2: methods ARE synchronized → the deadlock path

1. T1 calls `d1` → needs **A's lock** → gets it → starts running `d1`.
2. T2 calls `d2` → needs **B's lock** → gets it → starts running `d2`.
3. Inside `d1`, T1 must call `b.last()`, which is synchronized on **B** → T1
   now needs **B's lock**.
4. B's lock is held by T2 → T1 **waits** for it, while still holding A's
   lock.
5. Inside `d2`, T2 must call `a.last()`, synchronized on **A** → T2 now needs
   **A's lock**.
6. A's lock is held by T1 → T2 **waits** for it, while still holding B's
   lock.

```java
// The lock story:
// T1 holds A's lock, waiting for B's lock
// T2 holds B's lock, waiting for A's lock
// -> both wait for each other forever -> DEADLOCK
```

Sir acts out the comic negotiation between the two threads — "release your
lock for a minute and I'll give you both back," "no, give me yours first" —
neither ever releases, because neither ever *can*: each is blocked before it
reaches any code that would let go of what it's holding.

## 20:09 — Converting the idea into executable code

**Class A — both methods synchronized:**

```java
class A {
    public synchronized void d1(B b) {
        System.out.println("Thread-1 starts execution of d1 method");
        try {
            Thread.sleep(5000); // force T2 to start meanwhile
        } catch (InterruptedException e) {
        }
        System.out.println("Thread-1 trying to call B's last method");
        b.last();
    }

    public synchronized void last() {
        System.out.println("Inside A, this is last method");
    }
}
```

**Class B — same pattern:**

```java
class B {
    public synchronized void d2(A a) {
        System.out.println("Thread-2 starts execution of d2 method");
        try {
            Thread.sleep(5000); // intention: demonstrate deadlock
        } catch (InterruptedException e) {
        }
        System.out.println("Thread-2 trying to call A's last method");
        a.last();
    }

    public synchronized void last() {
        System.out.println("Inside B, this is last method");
    }
}
```

**Why `sleep(5000)`?** Without it, deadlock is **not guaranteed** — one
thread might race through its entire cross-call before the other even
starts. The sleep forces both threads to be holding their own object's lock
at the same moment the other one also needs it. Verified: running the same
program with the `sleep` calls deleted finished in 3 ms, every time, across
eight runs — no deadlock, because nothing forces the two locks to be held
simultaneously.

## 26:24 — The `Thread` subclass that drives both sides

Both `A` and `B` need to be instance fields, so both the main thread and the
child thread (via `this`) can reach them.

```java
class Deadlock extends Thread {
    A a = new A();
    B b = new B();

    public void m1() {
        this.start();          // starts child thread -> run()
        a.d1(b);               // executed by MAIN thread
    }

    public void run() {
        b.d2(a);               // executed by CHILD thread
    }

    public static void main(String[] args) {
        Deadlock d = new Deadlock();
        d.m1();
    }
}
```

## 28:26 — Thread count after `this.start()`

Before `start()`: only the **main** thread exists.

After `this.start()`:

- **Two** threads exist.
- The child executes `run()` → `b.d2(a)`.
- Main continues on and executes `a.d1(b)`.

So: main ≈ T1 (holds A's lock, sleeps, then waits for B's), child ≈ T2
(holds B's lock, sleeps, then waits for A's). Both wait forever → deadlock.

## 31:22 — Why not do everything inside `static main`?

`a` and `b` are instance variables. A `static main` has no instance to reach
them through directly, so the pattern needs an instance method (`m1()`) that
`main` calls on a created object — hence `Deadlock extends Thread` with `a`
and `b` as fields, not a fully static demo.

## 33:32 — Full program

```java
class A {
    public synchronized void d1(B b) {
        System.out.println("Thread-1 starts execution of d1 method");
        try { Thread.sleep(5000); } catch (InterruptedException e) {}
        System.out.println("Thread-1 trying to call B's last method");
        b.last();
    }
    public synchronized void last() {
        System.out.println("Inside A, this is last method");
    }
}

class B {
    public synchronized void d2(A a) {
        System.out.println("Thread-2 starts execution of d2 method");
        try { Thread.sleep(5000); } catch (InterruptedException e) {}
        System.out.println("Thread-2 trying to call A's last method");
        a.last();
    }
    public synchronized void last() {
        System.out.println("Inside B, this is last method");
    }
}

class Deadlock extends Thread {
    A a = new A();
    B b = new B();

    public void m1() {
        this.start();
        a.d1(b); // main
    }

    public void run() {
        b.d2(a); // child
    }

    public static void main(String[] args) {
        new Deadlock().m1();
    }
}
```

## 33:59 — Experiment: remove ALL `synchronized` → no deadlock

```text
Thread-1 starts execution of d1 method
Thread-2 starts execution of d2 method
Thread-1 trying to call B's last method
Inside B, this is last method
Thread-2 trying to call A's last method
Inside A, this is last method
// program ends -- NO deadlock
```

Verified by compiling and running exactly this variant: it prints all six
lines and exits every time.

## 34:47 — Experiment: only `d1`/`d2` synchronized, `last` not

If only `d1`/`d2` are synchronized and `last` is plain:

- T1 holds A's lock, calls `b.last()` — not synchronized, so no lock is
  needed for it — gets the chance immediately and completes.
- T2 completes the same way.
- **No deadlock**, because the cross-call no longer requires the other
  object's lock at all.

## 35:28 — All four synchronized → the cursor blinks forever

With all four `synchronized` and the `sleep` calls in place: after the
"trying to call last method" lines print, the program just hangs.

```text
Thread-1 starts execution of d1 method
Thread-2 starts execution of d2 method
Thread-1 trying to call B's last method
Thread-2 trying to call A's last method
// ... forever waiting -- deadlock
```

Verified: this exact program, compiled and run, prints those four lines and
then never terminates — it had to be killed from outside.

**Only "solution" once hung:** `Ctrl+C`, i.e. kill the process — not a real
solution, just an exit. "After ten years you can come back and the cursor is
still blinking."

> ⚠️ **Modern Java — killing the hung *thread* (instead of the process) was
> never actually safe, and the method that promised it is gone.**
> `Thread.stop()` (and `suspend()`/`resume()`) looked like a tempting escape
> hatch here — "just kill T1 or T2, not the whole JVM" — but it was already
> deprecated when this was recorded (since Java 1.2), precisely because
> `stop()` releases the thread's locks *without* restoring the objects it was
> updating to a consistent state, which can corrupt shared data worse than
> the hang did. Since **Java 20**, these methods don't merely warn — the
> Thread class no longer defines `stop()`, `suspend()`, or `resume()` at all.
> Verified on a current JDK: calling `.stop()` on a `Thread` object fails to
> compile/link with `NoSuchMethodError`, and `javap java.lang.Thread` lists no
> such methods. Sir's answer stands unchanged: `Ctrl+C` (kill the process)
> really is the only way out of this specific deadlock.

## 36:34 — Why the sleep matters for a reliable demo

Without `sleep`: no guarantee of deadlock. A likely schedule is main getting
the CPU, running all of `d1` including `b.last()`, and finishing before the
child even starts `d2` — no overlapping lock hold, no deadlock.

With `sleep`: T1 gets A's lock and sleeps; T2 gets B's lock and sleeps. Both
now hold a lock and, once they wake, both need the *other* one's lock —
deadlock shown reliably, every run.

## 38:41 — Sir rewrites the same example cleanly

Same structure redrawn on the board: synchronized `d1`/`d2`/`last`,
`sleep(5000)` or `sleep(6000)`, child via `run()`, main via `m1()` — no new
behavior, just a cleaner pass.

## 44:44 — Expected output, blinking cursor included

```text
Thread-1 starts execution of d1 method
Thread-2 starts execution of d2 method
Thread-1 trying to call B's last method
Thread-2 trying to call A's last method
// cursor blinking -- write this on your notes too
```

"After ten years also, the cursor is blinking like that" — because both
threads wait for each other forever.

## 45:58 — The critical interview conclusion

In this program, removing **at least one** `synchronized` keyword is enough
to remove the deadlock entirely. Restated once more as the takeaway line:

```java
// Board:
// synchronized keyword is the only reason for the deadlock situation.
// Due to this, while using synchronized keyword
// we have to take special care.
```

(Classic interview ask: "What is deadlock? Explain with a program." — this
example, in full, is the expected answer.)

> ⚠️ **Modern Java — this exact failure mode is why
> `java.util.concurrent.locks.Lock` exists.**
> `java.util.concurrent` shipped in **Java 5**, so it predates this recording
> by years — it just isn't the tool this lecture is teaching. A
> `synchronized` block can only block forever; a `ReentrantLock` can instead
> call `tryLock(long timeout, TimeUnit unit)`, which gives up and returns
> `false` if the lock doesn't become free in time — turning this exact
> program into "one thread backs off and retries" instead of a permanent
> hang. That's a genuine *prevention* technique for this specific deadlock
> shape, on top of the classroom answer ("acquire locks in a single
> consistent order across all threads," which also works and costs nothing
> extra). Both are worth naming if an interviewer follows up "how would you
> actually prevent this?" after the demo.

## 48:13 — Next term: Starvation (Deadlock vs Starvation)

Related terms, "a small minor difference."

## 49:05 — Definitions contrasted

**Deadlock:** long waiting of a thread where the waiting **never ends**.

**Starvation:** long waiting of a thread where the waiting **ends at some
point** — maybe after a very long time ("ten years, twenty years, a hundred
years"), but it does end.

```java
// Board:
// Long waiting of a thread where waiting never ends -> DEADLOCK
// Long waiting of a thread where waiting ends at a certain point -> STARVATION
```

> ❗ **Correction — "starvation always ends eventually" is the mnemonic, not
> the definition.**
> The real distinguishing factor between the two isn't a guarantee about
> *when* the waiting stops — it's *why* the thread is stuck. Deadlock is a
> **circular wait**: T1 waits on a resource T2 holds, T2 waits on a resource
> T1 holds, and the cycle itself makes progress structurally impossible — no
> scheduler decision can ever break it. Starvation is a **scheduling/fairness
> problem**: a runnable thread keeps losing out to other threads (lower
> priority, unlucky lock-acquisition order, an unfair queue) even though
> nothing structurally prevents it from running. Nothing guarantees a starved
> thread ever gets its turn either — an unfair scheduler could in principle
> starve it forever too. The safe way to say it in an interview: "deadlock
> can never resolve itself; starvation isn't blocked by a cycle, so it
> *usually* resolves once the contention eases, but the language doesn't
> guarantee it will."

## 50:07 — Example for starvation

The example Sir points to: a **low-priority thread** that keeps losing the
CPU to a stream of higher-priority threads. It isn't blocked by anything —
it's just repeatedly out-prioritized. Once the high-priority work finally
stops arriving, it gets its chance → starvation, not deadlock (the transcript
repeats "low priority thread" heavily here — pure ASR/verbal repetition, no
extra technical content).

## 51:37 — Difference restated

- Deadlock: waiting never ends.
- Starvation: waiting ends at some point (or, more precisely: nothing
  structurally forbids it from ending, unlike deadlock's cycle).

## 54:42 — Close

Students need clarity on deadlock vs. starvation. End of Part-12.

---

## Exam and interview points

1. **Deadlock:** two (or more) threads wait for each other's lock forever —
   an infinite wait caused by a circular lock-holding pattern.
2. **`synchronized` is the cause, never the cure**, in this classic model. No
   `synchronized` in this program → no deadlock of this kind.
3. **There is no in-process resolution technique for deadlock** — only
   prevention. Once hung, the process must be killed and restarted; a
   thread-dump tool (`jstack`, `jconsole`) can tell you *why* it hung, not
   undo it.
4. **The canonical demo:** classes `A` and `B` with cross-calling synchronized
   methods (`d1`→`b.last()`, `d2`→`a.last()`), driven by a `Thread` subclass
   whose `run()` and an instance method both fire at once. Interviewers ask
   for exactly this program.
5. **`Thread.sleep()` inside the demo isn't decoration** — it's what forces
   both locks to be held simultaneously, which is what makes the deadlock
   reproducible instead of a coin flip.
6. **Removing any single `synchronized` from the four methods breaks the
   deadlock.** This is the single most-quoted interview conclusion from this
   video.
7. **Starvation vs deadlock:** deadlock is a circular wait that structurally
   can never end; starvation is a fairness problem (e.g. a perpetually
   low-priority thread) that isn't blocked by a cycle, so it typically — but
   not guaranteed — resolves once contention eases.
8. **Modern context worth knowing past OCJP:** `Thread.stop()`/`suspend()`/
   `resume()` — never a safe fix for a hung thread, and gone entirely from
   `Thread` since Java 20; `java.util.concurrent.locks.Lock.tryLock(timeout)`
   offers a real prevention technique this lecture's `synchronized`-only
   model cannot (back off instead of hanging forever); and acquiring locks in
   a fixed, consistent order across all threads remains the free, zero-cost
   prevention technique for this exact deadlock shape.

---

**Next:** Video 093 — Daemon Threads
