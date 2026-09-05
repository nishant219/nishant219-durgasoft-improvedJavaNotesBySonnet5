# Video 087 — Synchronization part-1

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-7 || synchronization part-1

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 87 of 203 |
| Series | Multi Threading · Part 7 |
| Topic | synchronization part-1 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 35m 15s |
| Video ID | equLV2F0vLA |
| Watch | https://www.youtube.com/watch?v=equLV2F0vLA |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

This lecture introduces synchronization: the need for it (data inconsistency),
`synchronized` as a modifier, the object-lock model, synchronized vs.
non-synchronized areas of an object, then the big `Display.wish` demo run
with and without `synchronized`.

### 00:09 — Topic: synchronization (most valuable in multi-threading)

Sir calls synchronization the most valuable concept in all of multi-threading,
and opens with a student's line from that morning: "I know multi-threading but
I'm not perfect with synchronization" — common enough that he treats it as the
default anxiety around this topic.

He calls it a **nursery-standard** concept — don't panic — and budgets roughly
**2½ to 3 hours** across this and the next video to cover it fully: synchronized
method, synchronized block, object-level lock, class-level lock.

### 01:54 — Need / purpose; first rule: where `synchronized` applies

**First point — `synchronized` is a modifier:**

- Can I declare a **method** as synchronized? **Yes.**
- Can I declare a **variable** as synchronized? **No** — synchronized variables don't exist.
- Can I declare a **class** as synchronized? **No** — synchronized classes don't exist.

There **is** a synchronized method and a synchronized block, and nothing else.

```java
// synchronized is a modifier applicable ONLY for methods and blocks
// NOT for classes and variables

class Demo {
    // OK
    public synchronized void m1() { }

    // OK — synchronized block inside a method
    public void m2() {
        synchronized (this) { }
    }

    // NOT allowed: synchronized variable
    // synchronized int x = 10; // CE: modifier synchronized not allowed here

    // NOT allowed: synchronized class
    // synchronized class X { } // CE: modifier synchronized not allowed here
}
```

Both `synchronized int x = 10;` and `synchronized class X { }` were compiled
against JDK 26 while writing this note — both fail with the exact message
`modifier synchronized not allowed here`, on a top-level class and on a nested
class alike. Nothing here has changed since Java 6/7.

### 03:00 — Biryani plate analogy → "Biryani inconsistency problem"

Sunday afternoon Biryani plate story (Hyderabad common food). He throws a
leftover plate to a roadside dustbin. One dog finds it and is thrilled — but
before it can pick a side to start from, a second dog arrives, then a third,
then every dog is fighting every other dog. A fourth dog quietly starts eating
from the far side; the three fighters realize fighting gets them nothing, so
each one instead grabs and pulls the plate — and the Biryani spills on the
ground and becomes useless to everyone.

**If multiple dogs operate simultaneously on the same Biryani object → Biryani
inconsistency problem.**

| Analogy | Java |
|---|---|
| Biryani plate | one Java object |
| each dog | one thread |

**If multiple threads try to operate simultaneously on the same Java object,
there is a chance of data inconsistency** — one thread adding, one getting,
one replacing, producing abnormal results.

### 10:33 — Technical scenarios: reservation & joint account

**Online booking / railway or bus reservation**

- System shows **4 seats** available.
- One user requests **3 tickets**, another simultaneously requests **2 tickets**.
- If both are processed together, both may see "seats available" before either
  booking is committed — inconsistency.

**Joint account (husband + wife)**

- Account has **10,000**.
- Husband pays online **9,000**.
- Wife, at a mall, pays about **7,000** with the same card, at the same time.
- Same account object, both operating simultaneously → chance of inconsistency.

**To overcome this: the `synchronized` keyword is required.**

**Need of `synchronized`:** to resolve data inconsistency problems.

### 14:01 — Security-person / one-by-one nature

On the Biryani object, a dog can perform **eat**. Now place a **security
person** at the plate:

1. First dog asks security → no one is eating → allowed → starts eating.
2. Second dog asks → one is already eating → "please wait until it finishes" → waiting.
3. After the first finishes, the second gets its turn, then the third, and so on.

One-by-one → **no data inconsistency**.

If a method or block is declared `synchronized`, **at a time only one thread
is allowed to execute that method/block on the given object**.

```java
class JavaObject {
    // at a time only ONE thread can execute this on a given object
    public synchronized void m1() {
        // critical section
    }
}
```

The biggest advantage of `synchronized`: it **resolves data inconsistency** by
forcing one-by-one execution.

### 16:45 — Board notes (dictation)

1. `synchronized` is a modifier applicable **only for methods and blocks**, **not for classes and variables**.
2. If multiple threads try to operate **simultaneously on the same Java object**, there may be a chance of **data inconsistency problem**.
3. To overcome this → go for the **`synchronized` keyword**.
4. If a method or block is declared synchronized → **at a time only one thread** is allowed to execute that method/block **on the given object** → the data inconsistency problem is resolved.

### 20:21 — Advantage vs disadvantage; "never for style"

**Advantage:** overcomes / resolves data inconsistency problems.

**Disadvantage:** threads execute one by one. In a web app fielding thousands
of requests: until the first completes, the second waits; waiting time grows →
**performance problems**.

Hence: **if there is no specific requirement, never use `synchronized`** —
never for style or as a habit; it is harmful when unnecessary.

```java
// Board summary style
/*
Main advantage of synchronized keyword:
  we can resolve data inconsistency problems

Main disadvantage of synchronized keyword:
  it increases waiting time of threads
  and creates performance problems

Hence if there is no specific requirement
  then it is not recommended to use synchronized keyword
*/
```

Sir flags that `java.util.concurrent` has better solutions for some of this
("today's hero becomes zero later") but defers that to a future video — for
now, treat `synchronized` as the essential tool.

> ⚠️ **Modern Java — the `java.util.concurrent.locks` alternative Sir points to.**
> `ReentrantLock`, `ReadWriteLock`, and `StampedLock` (`java.util.concurrent.locks`)
> already existed in **Java 5**, before this recording — they are the "better
> solution" Sir is alluding to. Unlike `synchronized`, they support a
> non-blocking `tryLock()`, a `tryLock(timeout, unit)`, interruptible waits, and
> fairness policies:
>
> ```java
> import java.util.concurrent.locks.ReentrantLock;
>
> class Counter {
>     private final ReentrantLock lock = new ReentrantLock();
>     private int count = 0;
>
>     void increment() {
>         lock.lock();
>         try {
>             count++;
>         } finally {
>             lock.unlock();          // manual — unlike synchronized, JVM does NOT do this for you
>         }
>     }
> }
> ```
> `synchronized` is still the right default for a simple critical section — it
> is shorter, and the JVM releases the lock automatically even if an exception
> escapes. Reach for `ReentrantLock` only when you need what it adds:
> `tryLock`, timeouts, or interruptibility. This is covered in video 097 of
> this series.

### 25:28 — Internal idea: public telephone booth (lock)

Best analogy for how `synchronized` is implemented: **public telephone booth**
(cabin + lock).

1. First person gets the lock, starts calling.
2. Second person arrives → lock is with the first person → waits.
3. First finishes → releases the lock → the owner hands it to the second person.

**Every object in Java has a unique lock.** Internally, synchronization is
implemented using this **lock concept**.

- If a thread wants to execute a synchronized method on an object, it must
  first get the **lock of that object**.
- While T1 holds the lock and runs the sync method, T2 wanting the same
  object's lock must wait until T1 releases it.
- **Only when we use `synchronized`** does this lock concept come into play.
- Acquiring and releasing the lock is handled **automatically by the JVM**; the
  programmer writes no acquire/release code for `synchronized`.

```java
/*
Internally synchronization concept is implemented by using lock.
Every object in Java has a unique lock.
Whenever we are using synchronized keyword,
then only lock concept will come into the picture.

If a thread wants to execute synchronized method on the given object:
  first it has to get lock of that object
  once thread got the lock → allowed to execute any synchronized method on that object
  once method execution completes → automatically thread releases the lock

Acquiring and releasing lock internally takes care by JVM
and programmer not responsible for this activity
*/
```

> ⚠️ **Modern Java — `synchronized` and virtual threads.**
> Since **Java 21** (JEP 444), running a `synchronized` block or method on a
> *virtual* thread **pins** that virtual thread to its carrier (platform)
> thread for the whole duration — the JVM cannot unmount it the way it
> normally unmounts a blocked virtual thread. On code that synchronizes
> heavily, thousands of pinned virtual threads can exhaust the small platform-
> thread pool that carries them and stall the application. **Java 24** (JEP 491)
> removed this pinning: `synchronized` no longer blocks the carrier thread.
> Practical takeaway: on JDK 21–23, code that runs inside virtual threads and
> synchronizes a lot is often safer rewritten with `java.util.concurrent.locks.ReentrantLock`
> (see the box above); on JDK 24+, plain `synchronized` is fine again. This
> does not affect ordinary platform threads at all — everything Sir teaches
> here about `Thread`/`MyThread` is unaffected either way.

### 35:16 — Critical misconception: lock is object-based, not method-based

Class `X` with:

- `m1` — synchronized
- `m2` — synchronized
- `m3` — normal (non-synchronized)

```java
class X {
    public synchronized void m1() { /* ... */ }
    public synchronized void m2() { /* ... */ }
    public void m3() { /* ... */ } // normal
}
```

Scenario on **one** `X` object:

| Thread | Wants | Result while T1 holds the lock and runs m1 |
|---|---|---|
| T1 | execute m1 | gets the lock, runs m1 |
| T2 | execute m1 | waits (needs the same object's lock) |
| T3 | execute m2 | also waits — different method, but still the same object's lock |
| T4 | execute m3 | runs immediately — non-synchronized, no lock needed |

Many students assume "`m2` is a different method, so T3 can run." **Wrong.**

**The lock is object-based, not method-based.** Even a different synchronized
method needs the **same object's lock**.

> *While a thread is executing a synchronized method on the given object, the
> remaining threads are **not** allowed to execute **any** synchronized method
> simultaneously on the **same** object — but remaining threads **are**
> allowed to execute **non-synchronized** methods simultaneously.*

```java
/*
Lock concept is implemented based on object
but not based on method.

While a thread executing synchronized method on the given object:
  remaining threads are NOT allowed to execute any synchronized method
  simultaneously on the same object
BUT
  remaining threads ARE allowed to execute non-synchronized methods
  simultaneously
*/
```

### 47:38 — Two areas on every object; when to synchronize

Doubt: object is "locked" by T1 — how can T4 still run `m3`?

For every object there are **two areas**:

1. **Synchronized area** — update operations (add / remove / delete / replace)
   where the **object's state changes** → only **one thread at a time**.
2. **Non-synchronized area** — read operations where the state doesn't
   change → **any number of threads simultaneously**.

Performing updates in the non-synchronized area is a **worst-practice** bug
waiting to happen.

```java
class ReservationSystem {
    // read only — object state not changed
    public void checkAvailabilityOfTickets() {
        // non-synchronized
    }

    // update — state changes (book seat)
    public synchronized void bookTicket() {
        // synchronized
    }
}
```

- `checkAvailabilityOfTickets` → non-synchronized (read).
- `bookTicket` → synchronized (update).

### 53:46 — Diagram dictation (object areas)

```java
/*
Java object
  ├── synchronized area
  │     accessed by only ONE thread at a time
  │     wherever update operation (add/remove/delete/replace)
  │     where state of object changing
  └── non-synchronized area
        accessed by ANY NUMBER of threads simultaneously
        wherever object state won't be changed
        like read operation
*/
```

### 1:00:14 — Big example: `Display.wish` without / with synchronized

He builds the classic wish demo carefully.

**Class `Display` — `wish(String name)`**

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
```

Behavior of one call with `"Dhoni"`: print `Good Morning: `, sleep 2s, print
the name, repeat **10 times**.

**Class `MyThread`**

```java
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
```

**Case 1 — one thread, one Display**

```java
class SynchronizedDemo {
    public static void main(String[] args) {
        Display d = new Display();
        MyThread t1 = new MyThread(d, "Dhoni");
        t1.start();
    }
}
```

One dog, one Biryani plate → **synchronization not required.** Output:
regular `Good Morning: Dhoni` × 10.

**Case 2 — two threads, same Display (no synchronized)**

```java
class SynchronizedDemo {
    public static void main(String[] args) {
        Display d = new Display();
        MyThread t1 = new MyThread(d, "Dhoni");
        MyThread t2 = new MyThread(d, "Yuvi");
        t1.start();
        t2.start();
    }
}
```

Both call `wish` simultaneously on the same object → **irregular / mixed
output**, e.g.:

```text
Good Morning: Good Morning: Dhoni
Good Morning: Yuvi
Good Morning: Yuvi
Good Morning: Dhoni
...
```

Flow: T1 prints `Good Morning:` → sleeps → T2 prints `Good Morning:` → sleeps
→ T1 wakes and prints its name → interleaving continues → irregular output.
With **four** threads (Dhoni, Yuvi, Kohli, Raina) on the same `Display`, the
irregularity only gets worse.

**Case 3 — declare `wish` synchronized**

```java
class Display {
    public synchronized void wish(String name) {
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
```

At a time only **one** thread executes `wish` on that `Display`. Even while
sleeping, the JVM does **not** hand the sync method to another thread on that
object — "whether sleeping or dancing, doesn't matter, it still holds the
lock." → **Regular output**: all 10 lines for one name, then all 10 for the
other.

Which thread runs first (Dhoni or Yuvi) is **not guaranteed** — it depends on
the thread scheduler. With four threads, one-by-one execution is still
guaranteed, but the **order** is not (Raina might finish before Yuvi, etc.).

```java
class SynchronizedDemo {
    public static void main(String[] args) {
        Display d = new Display();
        MyThread t1 = new MyThread(d, "Dhoni");
        MyThread t2 = new MyThread(d, "Yuvi");
        // optional four-thread demo:
        // MyThread t3 = new MyThread(d, "Kohli");
        // MyThread t4 = new MyThread(d, "Raina");
        t1.start();
        t2.start();
        // t3.start(); t4.start();
    }
}
```

**Without synchronized → irregular output. With synchronized → regular output.**
This was compiled and run against JDK 26 while writing this note (sleep
shortened to 200ms for a quick check) — the synchronized version reliably
prints all 10 `Dhoni` lines, then all 10 `Yuvi` lines, in that or the reverse
order, never interleaved.

Sample irregular (no sync):

```text
Good Morning: Good Morning: Yuvi
Good Morning: Dhoni
Good Morning: Yuvi
...
```

Sample regular (with sync) — one possible run:

```text
Good Morning: Dhoni
Good Morning: Dhoni
... (10 times)
Good Morning: Yuvi
Good Morning: Yuvi
... (10 times)
```

### 1:25:19 — `join` vs `synchronized` (different concepts)

Synchronization and `join` are **completely different**:

- `join`: "I want to wait until some other thread completes" — usually because
  I need that thread's result or a specific sequence. Other threads may still
  run meanwhile depending on how you use it.
- `synchronized`: the requirement is **at a time only one** thread in the
  shared critical section — no ordering guarantee among the waiters, but
  mutual exclusion is guaranteed.

Do not conflate the two mental models.

### 1:29:07 — Closing diagram + final rule

- One `Display` object.
- T1 calls `wish("Dhoni")` on it.
- T2 calls `wish("Yuvi")` on the same `Display`.

```java
/*
If we are NOT declaring wish method as synchronized:
  then both threads will be executed simultaneously
  and hence we will get irregular output

If we declare wish method as synchronized:
  then at a time only one thread is allowed to execute wish method
  on the given Display object
  hence we will get regular output
*/
```

End of part-1 (~1:35:00): the with-vs-without-synchronized impact is clear;
further synchronization topics — synchronized block, class-level lock —
continue in part-2.

## Exam and interview points

1. **`synchronized` is a modifier only for methods and blocks** — not for
   classes or variables. Verified against JDK 26: both `synchronized int x;`
   and `synchronized class X {}` fail with `modifier synchronized not allowed
   here`.
2. **The lock belongs to the object, not to the method.** A thread executing
   any one synchronized method on an object holds that object's *only* lock —
   so no other thread can execute *any* synchronized method on that same
   object at the same time, even a completely different one.
3. **Non-synchronized methods are always callable**, even while another thread
   holds the object's lock and is inside a synchronized method — the lock only
   gates synchronized code.
4. **`Thread.sleep()` inside a synchronized method does not release the
   lock.** A sleeping thread still owns the monitor; other threads wanting
   that lock keep waiting for the full sleep duration. (This is the classic
   trap distinguishing `sleep()` from `Object.wait()`, which *does* release
   the lock — covered later in this series.)
5. **Thread execution order under `synchronized` is never guaranteed** —
   only mutual exclusion is. Which of several waiting threads gets the lock
   next depends on the thread scheduler.
6. **`join()` and `synchronized` solve different problems.** `join` sequences
   one thread after another's completion; `synchronized` just guarantees
   mutual exclusion on a critical section, with no ordering promise.
7. **Rule of thumb for the exam and for real code:** put update operations
   (state-changing) behind `synchronized`; leave read-only operations
   non-synchronized so they can run concurrently.
8. **Modern context an interviewer may probe:** `java.util.concurrent.locks.ReentrantLock`
   is the explicit alternative when you need `tryLock`, timeouts, or
   interruptibility that `synchronized` cannot express; and since Java 21,
   `synchronized` pinned virtual threads to their carrier until Java 24
   (JEP 491) removed that pinning.

**Next:** Video 088 — Synchronization part 2
