# Video 089 — Synchronized block

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-9 || synchronized block

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 89 of 203 |
| Series | Multi Threading · Part 9 |
| Topic | synchronized block |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 12m 47s |
| Video ID | ORzmjiYmOJg |
| Watch | https://www.youtube.com/watch?v=ORzmjiYmOJg |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Multi-threading Part 9 continues directly from Part 8 (Video 088): synchronized
method, object-level lock, class-level lock. This session narrows the lens to
the **synchronized block** — why declaring an entire method synchronized is
often overkill, the three ways to declare a block (current-object lock, a
named object's lock, class-level lock), a rerun of the `Display.wish()` demo
trimmed down to synchronizing only the `for` loop, why primitives can never
be locked on, and a long FAQ set covering race conditions, holding multiple
locks at once, and the (mis)understood term "synchronized statement."

---

### 00:09 — Why synchronized block? (Dilsukhnagar bomb analogy)

Sir opens with a real event: bomb blasts at **Dilsukhnagar**, Hyderabad, a
year or two before this recording. The absurd overreaction he imagines:
because of a blast at Dilsukhnagar, ground every flight out of **New York**,
stop every city bus in **London**, halt every local train in **Sydney** —
punishing the whole world for a problem confined to one small area. The sane
response is to cordon off Dilsukhnagar (or Hyderabad at most), not the planet.

Programmers make the identical mistake:

- A method has roughly **10,000 lines**.
- Only about **10 lines** (say, a database update) actually need
  synchronization.
- The common — and wrong — fix: declare the **entire method** `synchronized`.

That's the equivalent of grounding flights worldwide over one local incident:
every thread now queues for all 10,000 lines when it only needed exclusive
access to 10 of them, so waiting time — and with it, overall performance —
collapses.

**Rule of thumb:**

- Only a few lines need synchronization → wrap just those lines in a
  **synchronized block** (local to that region).
- The whole method needs synchronization → declare the method
  **synchronized** (global to the method).

**Advantage of a synchronized block over a synchronized method:** outside the
block, any number of threads run freely and simultaneously; only the small
critical section is ever exclusive to one thread at a time — so waiting time
drops and performance improves.

### 08:22 — Hyderabad → Vijayawada / narrow bridge analogy

A second analogy for the same point. Hyderabad to Vijayawada is roughly
300 km — about 6 hours on the old road, closer to 4 on today's four-lane
highway. Partway, near Kodad, sits a **narrow bridge** where only one vehicle
can cross at a time.

The worst possible rule: because of that one bridge, allow only **one
vehicle for the entire 300 km journey** — a handful of vehicles per day, so
slow that a lifetime might not be enough to see your own vehicle reach
Vijayawada. The sensible rule: let traffic flow freely on the highway and
synchronize only the bridge itself — a driver waits roughly a minute there,
not six hours for the whole route.

Same moral as the bomb-blast story: don't synchronize 300 km of code when
only a handful of lines — the "bridge" — actually need mutual exclusion.

### 13:26 — Board dictation: advantage

> **Board:**
> - If very few lines of code require synchronization, it is not
>   recommended to declare the entire method as synchronized — enclose just
>   those few lines in a synchronized block.
> - Main advantage of synchronized block over synchronized method: it
>   reduces waiting time of threads and improves performance of the
>   system/application.

> ⚠️ **Modern Java — a synchronized block can still stall a whole platform
> thread when used from a virtual thread (fixed in Java 24).**
> Everything above holds for ordinary ("platform") threads without
> qualification. But before **JDK 24**, if a **virtual thread** (Project
> Loom, JEP 444, Java 21) blocked *inside* a `synchronized` block or
> method — say, on I/O or `Thread.sleep()` — the JVM **pinned** it to its
> underlying carrier platform thread instead of freeing that carrier for
> other virtual threads to use. With potentially millions of virtual threads
> sharing a small pool of carriers, that pinning could quietly erase the
> scalability virtual threads exist to provide, and the advice going around
> at the time was "avoid `synchronized` if you're using virtual threads."
>
> **JEP 491**, delivered in **JDK 24**, removed this pinning: the monitor is
> now associated with the virtual thread itself rather than its carrier, so
> a virtual thread that blocks inside a synchronized block releases its
> carrier just as it would while waiting on a `java.util.concurrent.locks.Lock`.
> The synchronized-block performance story taught in this lecture is
> unaffected by any of this — it's purely a virtual-threads footnote worth
> knowing if you maintain code written for the JDK 21–23 window.

### 15:48 — How to declare a synchronized block (3 forms)

**1) Lock of the current object — `synchronized(this)`**

```java
synchronized (this) {
    // if a thread got the lock of the current object,
    // then only it is allowed to execute this area
}
```

**2) Lock of a particular object `b`**

```java
synchronized (b) {
    // if a thread got the lock of particular object b,
    // then only it is allowed to execute this area
}
```

**3) Class-level lock — `synchronized(Display.class)`**

```java
synchronized (Display.class) {
    // if a thread got the class-level lock of Display class,
    // then only it is allowed to execute this area
}
```

`Display.class` is the `Class` object representing `Display` at runtime, and
every class has exactly one such object — so locking on `Display.class`
means locking on the one **class-level lock**, whether the class has one
`Display` instance or a thousand.

### 25:03 — Same wish demo, but only the `for` loop in a block

Assume `wish` has **one lakh lines** before the loop and another one lakh
after it — only the `for` loop itself needs synchronization:

```java
class Display {
    public void wish(String name) {
        // ..... 1 lakh lines of code .....
        // (multiple threads OK here)

        synchronized (this) {
            for (int i = 0; i < 10; i++) {
                System.out.print("Good Morning: ");
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                }
                System.out.println(name);
            }
        }

        // ..... another 1 lakh lines of code .....
        // (multiple threads OK here)
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
    }
}
```

Verified on JDK 26: compiles and runs; without any `synchronized` keyword
at all this program gives **irregular** output (the two threads' `for` loops
interleave).

Two ways to fix it:

1. Declare the entire `wish` method `synchronized` — the same fix as the
   previous session's demo, but it needlessly serializes the two lakh
   non-critical lines along with the loop.
2. Wrap **only the `for` loop** in `synchronized (this)`, as above — regular
   output for each wish cycle (`Good Morning: Dhoni` × 10, then `Yuvi` × 10,
   or vice versa), with far better throughput since the non-critical lines
   still run for both threads concurrently.

### 41:29 — Change: two `Display` objects + `synchronized(this)`

```java
class SynchronizedDemo {
    public static void main(String[] args) {
        Display d1 = new Display();
        Display d2 = new Display();
        MyThread t1 = new MyThread(d1, "Dhoni");
        MyThread t2 = new MyThread(d2, "Yuvi");
        t1.start();
        t2.start();
    }
}
```

With `synchronized(this)` inside `wish`, the lock a thread needs depends on
*which object it's operating on*:

- For `t1`, the current object is **`d1`**.
- For `t2`, the current object is **`d2`**.

Different objects mean different locks — both threads can enter their
blocks **simultaneously**, so the output goes back to **irregular**.

### 45:37 — Fix with a class-level lock in the block

Requirement: keep the output regular even with two separate `Display`
objects. That needs a lock that doesn't depend on which object each thread
is using — the **class-level lock**:

```java
class Display {
    public void wish(String name) {
        // ..... 1 lakh lines .....

        synchronized (Display.class) {
            for (int i = 0; i < 10; i++) {
                System.out.print("Good Morning: ");
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                }
                System.out.println(name);
            }
        }

        // ..... 1 lakh lines .....
    }
}
```

There is only **one** class-level lock for `Display`, no matter how many
`Display` instances exist. The first thread to arrive takes it; the second
waits — **regular output**, even though `d1 != d2`.

### 47:50 — Important conclusion: no lock for primitives

Java has **two** kinds of locks accessible through `synchronized`:
**object-level** and **class-level**. (This is specifically about the
built-in monitor lock behind the `synchronized` keyword — the
`java.util.concurrent.locks` API, covered in Video 097, adds explicit lock
types such as `ReentrantLock`, but that's a separate mechanism.) A lock
applies to an object or a class — **never to a primitive value**:

```java
class Test {
    public void m1() {
        int x = 10;
        synchronized (x) {
            // ...
        }
        // CE: unexpected type
        //   required: reference
        //   found:    int
    }
}
```

Verified on JDK 26 — `javac` rejects `synchronized (x)` for an `int x` with
exactly this message (`required: reference`, `found: int`).

> **Board:**
> - The lock concept is applicable for object types and class types, but
>   not for primitives.
> - Hence we can't pass a primitive type as an argument to a synchronized
>   block — otherwise we get a compile-time error: `unexpected type`,
>   `required: reference`, `found: int`.

### 53:04 — FAQs (interview / SCJP style)

**1. What is the `synchronized` keyword? Where can we apply it?**

A modifier applicable to **methods and blocks** — not to variables or
classes.

**2. Advantage of `synchronized`?**

Resolves **data-inconsistency** problems.

**3. Disadvantage?**

Increases threads' waiting time and creates **performance** problems.

**4. What is a race condition?**

Sir notes he'd already taught the concept without naming it. If multiple
threads operate simultaneously on the same Java object and cause data
inconsistency, that is a **race condition** — overcome it with the
`synchronized` modifier/keyword.

> **Board:**
> - If multiple threads are operating simultaneously on the same Java
>   object, there may be a chance of a data-inconsistency problem. This is
>   called a race condition.
> - We can overcome this problem by using the `synchronized` keyword.

**5. What is an object lock, and when is it required?**

Every object has a unique lock (its object lock), required whenever a
thread wants to execute an **instance** synchronized method (or a
synchronized block on that object).

**6. What is a class-level lock, and when is it required?**

Every class has a unique lock, required whenever a thread wants to execute
a **static** synchronized method (or `synchronized(ClassName.class)`).

**7. Difference between class-level and object-level lock?**

A static synchronized method needs the class lock; an instance synchronized
method needs the object lock.

**8. While a thread executes a synchronized method on an object, can the
remaining threads execute any *other* synchronized method on the same
object simultaneously?**

**No.**

**9. What is a synchronized block?** — as taught above.

**10. How do you declare a block for the current object's lock?**

```java
synchronized (this) { }
```

**11. How do you declare a block for a class-level lock?**

`synchronized (Display.class) { }` — or any `ClassName.class`.

**12. Advantage of a synchronized block over a method?**

Performance improves; waiting time reduces.

### 1:03:19 — Can a thread acquire multiple locks simultaneously?

Answer: **yes — from different objects.**

```java
class X {
    public synchronized void m1() {
        // thread needs the lock of the X object to enter m1

        Y y = new Y();
        synchronized (y) {
            // now the thread also holds the lock of y

            Z z = new Z();
            synchronized (z) {
                // now the thread holds the locks of x, y, and z simultaneously
            }
        }
    }
}

class Y { }
class Z { }

class Demo {
    public static void main(String[] args) {
        X x = new X();
        x.m1();
    }
}
```

Verified on JDK 26: compiles and runs cleanly.

> **Board:** Is a thread able to acquire multiple locks simultaneously? Yes,
> of course — from different objects.

### 1:09:56 — What is a "synchronized statement"?

Sir's framing here: as per the Java specification, there is no such official
terminology — interview folklore coined it, meaning "the statements present
inside a synchronized method or synchronized block."

> **Board:** Interview people created this terminology: the statements
> present in a synchronized method and a synchronized block are called
> synchronized statements.

> ❗ **Correction — "synchronized statement" is not folklore; it names
> something narrower than described.**
> The JLS *does* define this term — **§14.19, "The synchronized
> Statement"** — so it is genuine specification language, not something
> interviewers invented. But it means something more specific than "any
> statement sitting inside a synchronized method or block": in the JLS, the
> *synchronized statement* is the `synchronized (Expression) Block`
> construct **itself** — i.e. the synchronized-block form. A `synchronized`
> **method** is a distinct, separate construct; the JLS never refers to its
> body as a "synchronized statement." So the term is real, but its official
> scope is narrower than what's taught here — the functional point (a
> region only one thread executes at a time, for a given lock) still holds
> for both forms.

### 1:12:28 — Close

Sir closes by checking for clarity across the whole block of material:
synchronized method vs. block, object lock vs. class lock, when a block is
preferable, and the FAQ set — race condition, object/class locks, and
holding multiple locks at once.

---

## Exam and interview points

1. **Never synchronize more than you must.** If only a handful of lines in
   a long method need mutual exclusion, wrap just those lines in a
   `synchronized` block — declaring the whole method `synchronized`
   needlessly increases waiting time and hurts performance.
2. **Three ways to declare a synchronized block:** `synchronized (this)`
   (current object's lock), `synchronized (someObject)` (a specific
   object's lock), and `synchronized (SomeClass.class)` (that class's one
   class-level lock).
3. **`SomeClass.class` is the `Class` object for `SomeClass`**, and every
   class has exactly one — so `synchronized (SomeClass.class)` always locks
   the same single monitor, no matter how many instances of the class
   exist.
4. **Locking follows the object, not the code.** Two threads calling
   `wish()` on two *different* `Display` objects with `synchronized(this)`
   get two different locks and run concurrently (irregular output);
   switching to `synchronized(Display.class)` forces both onto the one
   class-level lock (regular output).
5. **You cannot synchronize on a primitive.** `synchronized (x)` where `x`
   is an `int` is a compile-time error — `unexpected type: required
   reference, found int` — because the lock concept applies only to
   objects and classes, never to primitive values.
6. **Race condition, defined:** multiple threads operating simultaneously
   on the same object cause a data-inconsistency problem; `synchronized`
   is the fix.
7. **A single thread can hold several different locks at once** — one per
   object it has entered a synchronized method/block on (nested `x`, then
   `y`, then `z`) — as long as each lock comes from a different object.
8. **"Synchronized statement" is real JLS terminology (§14.19)** for the
   `synchronized (Expression) Block` construct specifically — not, as
   folklore has it, an unofficial term interviewers invented for "any
   statement inside a synchronized method or block."
9. **Since Java 24 (JEP 491), a virtual thread blocking inside a
   `synchronized` block no longer pins its carrier platform thread** —
   know this if asked about `synchronized` in a virtual-threads/Project
   Loom context.

**Next:** Video 090 — Inter Thread Communication Part-1
