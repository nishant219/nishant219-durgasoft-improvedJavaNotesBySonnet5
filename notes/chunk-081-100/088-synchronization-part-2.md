# Video 088 — Synchronization Part 2

## Video info

**Title:** Core Java with OCJP/SCJP: Multi Threading Part-8 || synchronization part-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 88 of 203 |
| Series | Multi Threading · Part 8 |
| Topic | synchronization part-2 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 53m 43s |
| Video ID | 945WfTjpF2w |
| Watch | https://www.youtube.com/watch?v=945WfTjpF2w |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Part 8 continues straight from Part 7's `Display.wish(String)` demo: one
`Display` object, two threads, `wish` declared `synchronized`. This video asks
what happens when you change *only* the object count, then only the modifier,
building the two rules every OCJP question in this area is really testing:
**synchronization is about the object, not the method or the thread count**,
and **`static synchronized` locks the class, not any instance**. It closes
with a second, independent example — `displayN`/`displayC` on one `Display` —
that isolates plain object-level locking one more time before the series
moves on to the synchronized block.

---

## 00:06 — Recap: one object, two threads needs synchronization

Same `Display`/`MyThread` pair as Part 7: one `Display` object, two threads
calling its `synchronized` `wish` method.

```java
class Display {
    public synchronized void wish(String name) {
        for (int i = 1; i <= 10; i++) {
            System.out.print("Good Morning: ");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) { }
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

class SynchronizedDemo1 {
    public static void main(String[] args) {
        Display d = new Display();
        MyThread t1 = new MyThread(d, "Dhoni");
        MyThread t2 = new MyThread(d, "Yuvi");
        t1.start();
        t2.start();
    }
}
// prints regular output: the full Dhoni block, then the full Yuvi block
// (which name goes first is not guaranteed)
```

**The rule as stated so far:** if multiple threads operate simultaneously on
the same Java object, synchronization is required — at any moment only one
thread should be allowed to touch that object, which is why `wish` was made
`synchronized`.

---

## 01:01 — One change: two `Display` objects instead of one

Sir keeps everything else identical and changes exactly one thing: `t1` and
`t2` now each get their own `Display`.

```java
class SynchronizedDemo2 {
    public static void main(String[] args) {
        Display d1 = new Display();
        Display d2 = new Display();

        MyThread t1 = new MyThread(d1, "Dhoni");
        MyThread t2 = new MyThread(d2, "Yuvraj");

        t1.start();
        t2.start();
    }
}
```

The question he puts to the room: regular output, or irregular? Most students
answer **regular** — "`wish` is synchronized, so it must be regular." Sir's
answer is the opposite: **irregular**, and the reasoning is the whole point of
today's lecture.

- **T1** wants to run `wish` on **d1** → it needs the **lock of d1**.
- **T2** wants to run `wish` on **d2** → it needs the **lock of d2**.
- Those are two different locks. T1 gets d1's lock and starts; T2 gets d2's
  lock and starts — at the same time. Neither is waiting on the other.

```java
// T1 holds d1's object lock, T2 holds d2's object lock — no contention,
// because a synchronized method's lock belongs to the object it runs on,
// not to the method itself.
```

Confirmed by running it (with a short sleep to keep the transcript readable):

```text
Good Morning: Good Morning: Yuvraj
Good Morning: Dhoni
Good Morning: Yuvraj
Good Morning: Dhoni
...
```

**Even though `wish` is a synchronized method, the output is irregular,
because the two threads are operating on different Java objects.** The
`synchronized` keyword serializes access to *one object's* monitor; it says
nothing about a second object's monitor.

---

## 06:38 — The real rule: count objects, not threads

The two demos side by side settle it:

| Situation | Synchronization needed? |
|---|---|
| Multiple threads on the **same** Java object | **Required** |
| Multiple threads on **different** Java objects | **Not required** |

**Biryani-plate analogy, revisited from Part 7:** three dogs sharing one
biryani plate need to take turns — synchronization required. Three dogs, each
with their own plate, never interact — synchronization not required, however
many dogs (threads) there are.

**Bank-account version:** wife and husband both operating on the *same* joint
account object need to be serialized — simultaneous withdrawals against one
balance risk inconsistency. But you operating on your account while someone
else operates on *their* account needs no coordination at all — why should
either of you wait for the other over two unrelated objects?

```java
class Account {
    synchronized void withdraw() { /* ... */ }
}

Account jointAccount = new Account();   // wife + husband, same object → sync matters
Account myAccount    = new Account();   // only you touch it   → separate lock, no wait
Account hisAccount   = new Account();   // his account, independent of yours
```

**Conclusion to keep in notes:**

```java
/*
 * RULE 1: multiple threads on the SAME Java object      → synchronization IS required.
 * RULE 2: multiple threads on DIFFERENT Java objects    → synchronization is NOT required.
 */
```

The exam/interview habit this builds: when a question shows `synchronized`,
first count the **objects** involved, not just the threads or the keyword.

---

## 13:59 — Same two objects, but `wish` is now `static synchronized`

Sir keeps the two-`Display`, two-thread setup from the irregular-output demo
and changes only the modifier:

```java
class Display {
    public static synchronized void wish(String name) {
        for (int i = 1; i <= 10; i++) {
            System.out.print("Good Morning: ");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) { }
            System.out.println(name);
        }
    }
}
```

Objects are still different (`d1`, `d2`); the method is now `static
synchronized`. His framing: for every change there should be a reaction — and
here the output flips to **regular**, confirmed by running both versions back
to back:

| Run | Modifier | Objects | Output |
|---|---|---|---|
| Instance `synchronized` | different (`d1`, `d2`) | **Irregular** |
| `static synchronized` | different (`d1`, `d2`) | **Regular** |

```text
// static synchronized, two objects — Dhoni's 10 lines complete, then Yuvraj's;
// which name finishes first is scheduler-dependent, order between t1/t2 is not.
```

---

## 17:23 — Why: `static synchronized` needs the class lock, not the object lock

A `static synchronized` method can't lock on an instance — a static method
doesn't have a `this`. What it locks on instead is the **class itself**.

- T1 calling `wish` on d1 needs the **class-level lock of `Display`** — gets
  it, starts.
- T2 calling `wish` on d2 also needs the **class-level lock of `Display`** —
  already held by T1 — so T2 waits until T1 releases it.
- One thread at a time, for *any* `static synchronized` method of that class,
  regardless of which instance called it.

```java
/*
 * Every class in Java has one unique lock  → CLASS-LEVEL LOCK.
 * Every object in Java has its own lock    → OBJECT-LEVEL LOCK.
 * In Java, synchronized recognizes exactly these two kinds — there is no
 * third, "variable-level" lock.
 *
 * If a thread wants to run a STATIC SYNCHRONIZED method
 *   → it needs the CLASS-LEVEL LOCK.
 * Once it has that lock
 *   → it may run ANY static synchronized method of that class.
 * Once that method completes
 *   → it automatically releases the lock.
 */
```

The class-level lock isn't a separate JVM mechanism bolted on for this case —
Sir's internal detail is that every loaded class has one `Class` object
representing it (the same `Class` object `X.class` refers to), and the
"class-level lock" is just that object's monitor. `Display.class` is shared
by every `Display` instance, so any thread taking the class lock through
`d1` or `d2` is taking the same lock either way:

```java
Display a = new Display();
Display b = new Display();
System.out.println(a.getClass() == b.getClass()); // true — one Class object per class
```

> ⚠️ **Modern Java — `synchronized` no longer pins virtual threads (Java 24, JEP 491).**
> Everything above — object lock, class lock, one thread at a time — is
> exactly how `synchronized` still behaves today, for both platform and
> virtual threads. But from virtual threads' introduction in **Java 21**
> through **Java 23**, a virtual thread that *blocked while holding a
> `synchronized` lock* (blocking I/O, or `Object.wait()` inside the
> monitor) got **pinned** to its carrier platform thread instead of
> unmounting — which could starve the whole carrier pool under load if many
> virtual threads did this at once. **JEP 491**, delivered in **Java 24**,
> removed pinning for both of those cases. Verified on JDK 26: a virtual
> thread that sleeps inside a `synchronized (lock)` block, run with
> `-Djdk.tracePinnedThreads=full`, reports **no pinning** — the identical
> code on Java 21–23 would print a pinned-frame warning naming
> `MonitorEnter`. This changes nothing about the locking rules Sir teaches;
> it only matters once `synchronized` is mixed with virtual threads.

---

## 23:08 — The OCJP lock table: class `X`, five methods, six threads

Sir's standard drill for this material: one class with every kind of method,
and enough threads to touch each one.

```java
class X {
    static synchronized void m1() { /* ... */ }
    static synchronized void m2() { /* ... */ }
    static void m3() { /* normal static — NOT synchronized */ }
    synchronized void m4() { /* instance synchronized */ }
    void m5() { /* normal instance */ }
}
```

```java
X obj = new X();
// T1 → m1()   static synchronized  → needs CLASS lock of X
// T2 → m1()   static synchronized  → needs CLASS lock → WAIT (T1 holds it)
// T3 → m2()   static synchronized  → needs CLASS lock → WAIT (T1 holds it)
// T4 → m3()   normal static        → no lock needed   → runs immediately
// T5 → m4()   instance synchronized → needs obj's OBJECT lock → available → runs
// T6 → m5()   normal instance       → no lock needed   → runs immediately
```

**State while T1 holds the class lock, running `m1`:**

| Thread | Method | Lock needed | Runs? |
|---|---|---|---|
| T1 | m1 | Class lock | Yes — holder |
| T2 | m1 | Class lock | No — waiting |
| T3 | m2 | Class lock | No — waiting (same class lock, different method) |
| T4 | m3 | None | Yes — in parallel |
| T5 | m4 | Object lock of `obj` | Yes — in parallel (a different lock) |
| T6 | m5 | None | Yes — in parallel |

**The insight the table is built to teach:** while a thread executes any
`static synchronized` method, no other thread may execute *any*
`static synchronized` method of that class — but normal static methods,
synchronized instance methods, and normal instance methods all keep running
simultaneously, because they need a different lock (or none at all).

```java
class Test {
    static synchronized void a() { }  // needs the class lock: Test.class
    synchronized void b() { }         // needs this instance's object lock
    static void c() { }               // needs no lock
    void d() { }                      // needs no lock
}
```

---

## 32:28 — Second example: `displayN` and `displayC` on one `Display`

A fresh, self-contained example to nail down object-level locking once more,
this time with **two different methods** sharing one object instead of one
method shared by two threads.

```java
class Display {
    public void displayN() {
        for (int i = 1; i <= 10; i++) {
            System.out.print(i + " ");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) { }
        }
        System.out.println();
    }

    public void displayC() {
        for (int i = 65; i <= 75; i++) {
            System.out.print((char) i + " ");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) { }
        }
        System.out.println();
    }
}
```

`displayN` prints 1 through 10. `displayC` prints the characters for ASCII
65–75.

> ❗ **Correction — 65 to 75 inclusive is 11 characters, not 10.**
> Sir describes `displayC` as printing "A to J" — ten characters, to match
> `displayN`'s ten numbers — but dictates the loop bound as `i <= 75`.
> `A` is 65 and `J` is 74; 75 is `K`. Compiling and running the loop exactly
> as given prints `A B C D E F G H I J K` — eleven characters, one past `J`.
> To get the ten characters Sir describes, the condition should be `i <= 74`.
> Harmless to the lesson (object-level locking doesn't care how many
> iterations a loop runs), but worth fixing if you copy this code verbatim.

Two thread classes, each with a single job on whatever `Display` they're
given:

```java
class MyThread1 extends Thread {
    Display d;

    MyThread1(Display d) {
        this.d = d;
    }

    public void run() {
        d.displayN();
    }
}

class MyThread2 extends Thread {
    Display d;

    MyThread2(Display d) {
        this.d = d;
    }

    public void run() {
        d.displayC();
    }
}
```

Both methods are instance methods, so calling either one requires a
`Display` reference — which is exactly what each thread class stores.

---

## 39:30 — Without `synchronized`: one object, mixed output

```java
class SynchronizeDemo {
    public static void main(String[] args) {
        Display d = new Display();

        MyThread1 t1 = new MyThread1(d);
        MyThread2 t2 = new MyThread2(d);

        t1.start();
        t2.start();
    }
}
```

One `Display` object, two threads: T1 calls `displayN` on it, T2 calls
`displayC` on it. Neither method is synchronized, so both run at the same
time on the same object, and the console gets a mixed interleaving of numbers
and letters — something like `1 A 2 B 3 C ...`, exact pattern depending on the
scheduler and the sleep timing.

---

## 43:50 — The fix: synchronize both methods

What Sir wants instead: all ten numbers, then all eleven characters — or the
reverse — never interleaved. The fix is to mark **both** methods
`synchronized`:

```java
class Display {
    public synchronized void displayN() {
        for (int i = 1; i <= 10; i++) {
            System.out.print(i + " ");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) { }
        }
        System.out.println();
    }

    public synchronized void displayC() {
        for (int i = 65; i <= 75; i++) {
            System.out.print((char) i + " ");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) { }
        }
        System.out.println();
    }
}
```

Both methods now share the **same object's lock** (`d`). Whichever thread
gets there first runs to completion before the other is allowed to start —
which one wins is not guaranteed, but the output is always one method's full
run followed by the other's, never mixed:

```java
/*
 * Both methods synchronized on the SAME object:
 *   - only ONE thread runs at a time,
 *   - which thread goes first is scheduler-decided, not guaranteed,
 *   - after it completes, the other runs — never interleaved.
 */
```

Running it confirms both orders are legal outcomes: usually the numbers
finish first and then the letters, but there is no guarantee — a run where
the letters go first is just as correct.

---

## 46:52 — Wrap-up: object lock vs class lock, synchronized block next

Sir's own closing summary for Part 8:

| Topic | Takeaway |
|---|---|
| Same object, multiple threads | Synchronization required for consistent access |
| Different objects, multiple threads | Instance `synchronized` does **not** block across objects |
| `static synchronized` | Uses the class-level lock — one thread at a time, for *all* static synchronized methods of that class |
| Class lock vs object lock | Independent locks — holding one never blocks a thread that only needs the other |
| Class `X` / M1–M5 | While a static-synchronized method runs, non-competing normal static, synchronized instance, and normal instance methods all still run |
| `displayN` / `displayC` | Two synchronized methods on the same object share one lock → mutual exclusion |

Every demo from this video, side by side:

| # | Setup | Method modifier | Objects | Output |
|---|---|---|---|---|
| 1 | `wish` — recap | instance `synchronized` | 1 | Regular |
| 2 | `wish` — d1, d2 | instance `synchronized` | 2 | Irregular |
| 3 | `wish` — d1, d2 | `static synchronized` | 2 | Regular |
| 4 | `displayN` + `displayC` | not synchronized | 1 | Irregular (mixed) |
| 5 | `displayN` + `displayC` | both `synchronized` | 1 | Regular |

Next in the series: the **synchronized block** — why it exists alongside the
synchronized method, its syntax, and when to reach for it instead.

---

## Exam and interview points

1. **The controlling factor is the object, not the thread count or the
   keyword by itself.** Two threads on one synchronized object → regular
   (serialized) output. Two threads on two different objects, even calling
   the *same* `synchronized` method → irregular output, because each thread
   acquires a different object's lock.
2. **A `static synchronized` method locks the class, not the instance.**
   Every class has exactly one class-level lock (backed by its one shared
   `Class` object), so two threads calling a `static synchronized` method
   through *different* instances still serialize — this is the one case
   where "different objects" does **not** buy you concurrency.
3. **Java recognizes exactly two kinds of intrinsic lock: object-level and
   class-level.** There is no third, "variable-level" lock — a trap answer
   worth ruling out explicitly.
4. **Class lock and object lock are independent.** A thread holding the
   class lock never blocks a thread that only needs an object lock (or
   needs no lock at all) — normal static methods, synchronized instance
   methods, and normal instance methods of the same class keep running in
   parallel with a static-synchronized method in progress.
5. **Two synchronized instance methods on the same object share one lock.**
   `displayN` and `displayC`, both `synchronized` on the same `Display`,
   mutually exclude each other even though they are different methods —
   the lock belongs to the object, not to any one method.
6. **Which thread wins the lock first is never guaranteed.** Regular output
   means "one complete run, then the other" — not "a specific order."
7. **Since Java 24 (JEP 491), `synchronized` no longer pins a virtual thread**
   that blocks while holding the lock — a genuinely new fact for anyone
   combining this classic locking model with Project Loom, even though the
   locking rules themselves are unchanged.

**Next:** Video 089 — Synchronized block
