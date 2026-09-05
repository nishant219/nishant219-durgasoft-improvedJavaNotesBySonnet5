# Video 095 — Thread Group (Multithreading Enhancement Part-1)

## Video info

**Title:** Core Java With OCJP/SCJP: Multithreading Enhancement  Part- 1|| Introduction || Thread Group

| Field | Detail |  |  |
|---|---|---|---|
| Playlist | java tutorial by durga sir |  |  |
| Position | Video 95 of 203 |  |  |
| Series | Multithreading Enhancement · Part 1 |  |  |
| Topic | Introduction |  | Thread Group |
| Instructor | Durga Sir (Durga Software Solutions) |  |  |
| Duration | 1h 28m 54s |  |  |
| Video ID | B2L-vVpFP7Y |  |  |
| Watch | https://www.youtube.com/watch?v=B2L-vVpFP7Y |  |  |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |  |  |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This opens a new block Sir calls **Multithreading Enhancements** — beyond the
basics (start/run, priorities, synchronization, wait/notify) into: Thread
Group, Thread Local, alternatives to the `synchronized` block, the
`java.util.concurrent` package, and the Executor framework. He flags it as a
step up in difficulty and terminology from what came before.

This video is entirely **ThreadGroup**: what it is, why grouping threads
helps, the `main`/`system` hierarchy every thread already lives in, both
constructors, the important methods (with a genuine loophole in
`setMaxPriority`), and two full demo programs — one walking a parent/child
group tree, one listing every active thread under the JVM's **system** group.

---

## 00:52 — What is a thread group?

> A **thread group** is a group of threads, based on **functionality**, kept
> as a single unit.

Producer threads together, consumer threads together, printing threads
together — group by what the threads *do*, not by anything else.

```java
// Based on functionality we group threads into a single unit,
// which is nothing but a Thread Group.
// A Thread Group contains a group of threads.
```

### 01:48 — A thread group can also contain sub-thread-groups

A thread group holds threads directly, and it can also hold **nested
thread groups**, each with threads of its own — groups all the way down.

```java
// In addition to threads, a thread group can also contain sub thread groups.
```

## 02:42 — The payoff: common operations become one operation

Sir's analogy: Yahoo Messenger let you file contacts into groups —
*Friends*, *Relatives*. Right-click the *Friends* group, send one "Happy
Friendship Day" message, and everyone in it gets it in one shot. Without
groups you'd look up each friend and message them one at a time.

Threads work the same way once they're grouped:

- Suspend all consumer threads in one call.
- Stop all producer threads in one call.
- Raise the max priority for every printing thread at once.
- Lower the max priority for every header thread at once.

> ⚠️ **Modern Java — the bulk stop/suspend Sir gestures at here is gone; the
> modern answer to "manage many threads as one unit" is a different
> mechanism entirely.**
> `ThreadGroup` really did carry `stop()`, `suspend()`, and `resume()`
> methods that did exactly this — kill or pause every thread in the group in
> one call — but they were deprecated back in Java 1.2 for the same safety
> reasons `Thread.stop()`/`suspend()`/`resume()` were (see Video 094): killing
> or freezing a thread mid-work leaves shared state and resources in an
> unknown mess. On the JDK used for this note (26) they aren't merely
> deprecated, they're **gone** — `javap -p java.lang.ThreadGroup` lists no
> `stop`, `suspend`, `resume`, or `allowThreadSuspension` at all. Java's
> current answer to "treat a bunch of related threads as one unit" is
> **structured concurrency** (`java.util.concurrent.StructuredTaskScope`,
> still a preview API as of Java 25/26, `--enable-preview` required): you
> `fork()` related subtasks into one scope, and cancelling or closing the
> scope cancels every subtask together. Different mechanism, same motivating
> idea — and unlike `ThreadGroup.stop()`, it's designed to leave things in a
> consistent state.

## 08:25 — Every thread belongs to some thread group

There is no such thing as a thread that exists outside any group — every
thread in Java, without exception, belongs to one.

### 08:51 — Demo: which group does `main` belong to?

```java
class Test {
    public static void main(String[] args) {
        System.out.println(
            Thread.currentThread().getThreadGroup().getName()
        );
        // prints: main
    }
}
```

**Three "main"s — do not confuse them:**

1. the `main` **method**
2. the `main` **thread** (the one that calls the method)
3. the `main` **thread group** (the one the thread belongs to)

The method is called by the thread; the thread belongs to the group. All
three happen to share the name `main`, which is exactly why the printed
output above is `main` — and exactly why it confuses people the first time.

## 11:24 — `main`'s parent group is `system`

Every thread group is a child — directly or indirectly — of one root group
called **system**, the same way every class in Java is, directly or
indirectly, a child of `Object`. `Object` is the root for classes; `system`
is the root for thread groups.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(
            Thread.currentThread().getThreadGroup().getName()
        );
        // prints: main

        System.out.println(
            Thread.currentThread().getThreadGroup().getParent().getName()
        );
        // prints: system
    }
}
```

```text
system  (root — like Object for classes)
  └── main   (the group your own code's threads land in by default)
```

### 17:47 — What does `system` contain?

The **system** group holds the JVM's own housekeeping threads — for
example **Finalizer**, **Reference Handler**, **Signal Dispatcher**, and
**Attach Listener**. The exact list isn't fixed; different JVMs and JVM
options add or drop a few.

> ❗ **Correction — "every Java program has exactly two threads, `main` and
> the garbage collector" is wrong, and Sir says so** — there are *several*
> system-level threads, not one GC thread. But his own shorthand for one of
> them overshoots too: **"Finalizer is nothing but our garbage collector"
> is not accurate.** The `Finalizer` thread's job is narrower — it pulls
> objects the collector has already identified as unreachable off a queue
> and runs their `finalize()` method. It does not do the collecting itself;
> the actual collector (G1, ZGC, whichever is active) runs its own internal
> native threads that never show up as `java.lang.Thread` objects at all, so
> they can never appear in any `ThreadGroup.enumerate()` result. "Finalizer"
> and "the garbage collector" are related but not the same thread.

> ⚠️ **Modern Java — the finalizer mechanism this thread exists for is being
> retired, and the actual thread roster has moved on.**
> `Object.finalize()` was deprecated for removal in **Java 9** and, since
> **Java 18**, finalization is **disabled by default** (`java -XX:+/-Finalization`,
> or `--finalization=enabled` in newer syntax, turns it back on). Its
> replacement, `java.lang.ref.Cleaner`, shipped alongside the deprecation in
> Java 9. Running this lecture's own thread-listing demo (see 1:18:45 below)
> on a current JDK shows the roster has changed to match:
> ```text
> Reference Handler ........ true
> Finalizer ........ true
> Signal Dispatcher ........ true
> Notification Thread ........ true
> Common-Cleaner ........ true
> ```
> `Attach Listener` doesn't appear unless the attach subsystem gets engaged
> (matches Sir's own "don't feel only these four, it varies"). `Notification
> Thread` (JMX) and `Common-Cleaner` (the shared `Cleaner`, the `finalize()`
> replacement) didn't exist in the Java 6/7 era this was recorded in.
> `Finalizer` itself is still there — it isn't gone, just increasingly
> unused now that `Cleaner` is the recommended path.

## 25:02 — `ThreadGroup` is a `java.lang` class

`ThreadGroup` lives in **`java.lang`** and is a **direct child of `Object`**
— same as `Thread`.

```java
// ThreadGroup is a class in java.lang,
// and it is the direct child class of Object.
```

## 26:33 — Constructor 1: `ThreadGroup(String name)`

```java
ThreadGroup g = new ThreadGroup(String groupName);
// Creates a new thread group with the given name.
// Its parent is the thread group of the *currently executing* thread —
// whichever thread runs this line.
```

```java
ThreadGroup g1 = new ThreadGroup("First Group");
System.out.println(g1.getParent().getName());
// prints: main
// — because main thread executes this line, and main thread's group is main
```

If this same line ran on a thread that itself belonged to some group `XYZ`,
the new group's parent would be `XYZ`, not `main`.

## 31:41 — Constructor 2: choose the parent explicitly

Sometimes the new group needs a specific parent — not just whatever group
happens to be running the line. The second constructor takes the parent as
an argument:

```java
ThreadGroup g = new ThreadGroup(ThreadGroup parent, String groupName);
// Creates a new thread group with the given name.
// Its parent is the specified parent group, not the caller's own group.
```

```java
class Test {
    public static void main(String[] args) {
        ThreadGroup g1 = new ThreadGroup("First Group");
        System.out.println(g1.getParent().getName());
        // prints: main

        ThreadGroup g2 = new ThreadGroup(g1, "Second Group");
        System.out.println(g2.getParent().getName());
        // prints: First Group
    }
}
```

```text
system
 └── main
      └── First Group
           └── Second Group
```

## 39:53 — Important methods of `ThreadGroup`

Already used above: `getName()`, `getParent()`. The rest, one at a time.

### `String getName()`

```java
public String getName();
// returns the name of this thread group
```

### `int getMaxPriority()` / `void setMaxPriority(int p)`

```java
public int getMaxPriority();
// returns this group's max priority

public void setMaxPriority(int p);
// sets this group's max priority
```

The **default max priority of a new group is 10** — same ceiling as
`Thread.MAX_PRIORITY`.

### 43:34 — The `setMaxPriority` loophole

```java
ThreadGroup g1 = new ThreadGroup("TG");
// default max priority of g1 = 10

Thread t1 = new Thread(g1, "First Thread");   // default priority 5 — allowed (≤ 10)
Thread t2 = new Thread(g1, "Second Thread");  // priority 5 — allowed

g1.setMaxPriority(3);   // group max drops to 3

Thread t3 = new Thread(g1, "Third Thread");   // newly added — capped to 3

System.out.println(t1.getPriority());   // 5
System.out.println(t2.getPriority());   // 5
System.out.println(t3.getPriority());   // 3
```

The twist: after `g1.setMaxPriority(3)`, do `t1` and `t2` — already sitting
at priority 5 — get pulled down to 3? **No.** Threads *already in the group*
keep whatever priority they had; the new cap only ever applies to threads
**added after** the call. Verified against a current JDK — output is exactly
`5, 5, 3`, unchanged from what the recording shows.

### 54:41 — `getParent()`, `list()`, `activeCount()`, `activeGroupCount()`

```java
public ThreadGroup getParent();
// returns this group's parent group

public void list();
// prints this group's threads and sub-groups to the console

public int activeCount();
// returns the number of active threads in this group (and its sub-groups)

public int activeGroupCount();
// returns the number of active sub-groups under this group
```

### 58:17 — `enumerate(Thread[] t)`

Copies every active thread of this group — including threads in its
sub-groups — into the array you provide:

```java
Thread[] t = new Thread[10];
g.enumerate(t);
// every active thread in g, and in g's sub-groups, is copied into t
```

### 1:01:42 — `enumerate(ThreadGroup[] g)`

```java
public int enumerate(ThreadGroup[] g);
// copies this group's active sub-groups into the given array
```

### 1:02:24 — Daemon / interrupt / destroy, at the group level

```java
public boolean isDaemon();
// is this group flagged as a daemon group?

public void setDaemon(boolean b);
// changes the daemon flag on this group

public void interrupt();
// interrupts every waiting or sleeping thread in this group

public void destroy();
// destroys this group and its sub-groups
```

> ⚠️ **Modern Java — most of this group's own bookkeeping methods are
> deprecated for removal.**
> Checked against the current JDK's `ThreadGroup` (`javap -v`): `setDaemon`,
> `isDaemon`, `isDestroyed`, and `destroy` have carried
> `@Deprecated(since="16", forRemoval=true)` since Java 16, and `checkAccess`
> the same since Java 17. `javac -Xlint:deprecation` on code that calls
> `destroy()` or `setDaemon()` on a `ThreadGroup` today prints exactly a
> `[removal]` warning, not a plain `[deprecation]` one — the "for removal"
> flavor. The reasoning tracks Video 094's `Thread.stop()`/`suspend()`
> story: a daemon flag or a "destroy everything under me" call at the
> *group* level is just as unsafe as at the thread level, and virtual
> threads (Java 21+) don't fit this bookkeeping model at all (more below).
> `getName`, `getParent`, `getMaxPriority`/`setMaxPriority`, `list`,
> `activeCount`, `activeGroupCount`, both `enumerate` overloads, and
> `interrupt` are **not** on the deprecated list — those still have a clean
> future.

## 1:04:33 — Demo: `activeCount`, `activeGroupCount`, `list()` together

```java
class MyThread extends Thread {
    MyThread(ThreadGroup g, String name) {
        super(g, name);   // associates this thread with a group + a name
    }

    public void run() {
        System.out.println("Child Thread");
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
        }
    }
}

class ThreadGroupDemo3 {
    public static void main(String[] args) throws Exception {
        ThreadGroup pg = new ThreadGroup("Parent Group");
        ThreadGroup cg = new ThreadGroup(pg, "Child Group");

        MyThread t1 = new MyThread(pg, "Child Thread 1");
        MyThread t2 = new MyThread(pg, "Child Thread 2");
        t1.start();
        t2.start();
        // both print "Child Thread", then sleep 5s — still active

        System.out.println(pg.activeCount());       // 2
        System.out.println(pg.activeGroupCount());   // 1 (Child Group)
        pg.list();

        Thread.sleep(10000);
        // both children finish well inside 10s (they only slept 5s) — now dead

        System.out.println(pg.activeCount());        // 0
        System.out.println(pg.activeGroupCount());    // 1 — the sub-group itself never left
        pg.list();
    }
}
```

Verified run, real output:

```text
Child Thread
Child Thread
2
1
java.lang.ThreadGroup[name=Parent Group,maxpri=10]
    Thread[#26,Child Thread 1,5,Parent Group]
    Thread[#27,Child Thread 2,5,Parent Group]
    java.lang.ThreadGroup[name=Child Group,maxpri=10]
0
1
java.lang.ThreadGroup[name=Parent Group,maxpri=10]
    java.lang.ThreadGroup[name=Child Group,maxpri=10]
```

```text
system
 └── main
      └── Parent Group
           ├── Child Thread 1
           ├── Child Thread 2
           └── Child Group   (sub-group — survives even after both threads die)
```

> ⚠️ **Modern Java — `list()`'s per-thread line now carries a thread id.**
> Compare the run above to what the recording shows: back then a thread
> printed as `Thread[Child Thread 1,5,Parent Group]`; today it's
> `Thread[#26,Child Thread 1,5,Parent Group]`. `Thread.toString()` picked up
> the `#<id>` prefix once virtual threads arrived (Java 21) — many virtual
> threads can share a name, so the id is what actually disambiguates them in
> a dump. The rest of the format — name, priority, group — is unchanged.

## 1:17:55 — Who actually associates a thread with its group?

The **constructor's** job. `MyThread`'s `super(g, name)` call reaches
`Thread`'s own `(ThreadGroup, String)` constructor, and that's the one
constructor that does the associating — both the name and the group.

## 1:18:45 — Program: list every active thread under `system`

```java
class ThreadGroupDemo4 {
    public static void main(String[] args) {
        ThreadGroup system =
            Thread.currentThread()
                .getThreadGroup()
                .getParent();   // main's parent is system

        Thread[] t = new Thread[system.activeCount()];
        system.enumerate(t);

        for (Thread t1 : t) {
            System.out.println(
                t1.getName() + " ........ " + t1.isDaemon()
            );
        }
    }
}
```

Expected shape of the output (the exact set of system threads varies by
JVM):

```text
Reference Handler ........ true
Finalizer ........ true
Signal Dispatcher ........ true
Attach Listener ........ true
main ........ false
```

The takeaway holds regardless of the exact roster: every system-level
thread is a **daemon**; `main` is the one **non-daemon** thread in the tree.

> ⚠️ **Modern Java — virtual threads don't live in this tree at all.**
> Everything above assumes "thread" means a platform thread, which is all
> that existed when this was recorded. Since **Java 21** (`Thread.ofVirtual()`,
> `Thread.startVirtualThread(...)`), a virtual thread's `getThreadGroup()`
> returns one synthetic, shared group — verified on a current JDK:
> ```text
> Thread.startVirtualThread(() -> {}).getThreadGroup()
> // java.lang.ThreadGroup[name=VirtualThreads,maxpri=10]
> ```
> That `VirtualThreads` group's `activeCount()` returns `0` no matter how
> many virtual threads are actually running — it's a placeholder, not a real
> membership list, because tracking millions of short-lived virtual threads
> in a `ThreadGroup` the way this lecture tracks two `MyThread`s would defeat
> the point of them being cheap. So `ThreadGroupDemo4`'s enumerate-the-tree
> technique still works exactly as shown, but it only ever reports on
> platform threads — a fleet of virtual threads doing real work would be
> invisible to it.

### 1:28:28 — Close of Part-1

Covered: what a thread group is, its constructors, its methods, how many
active threads exist in a group, and what the `system` group itself
contains. The Multithreading Enhancement series continues with the next
parts.

---

## Exam and interview points

1. **Every thread belongs to exactly one thread group**, and every thread
   group is, directly or indirectly, a child of the root **`system`** group
   — the thread-group equivalent of `Object` being the root of every class.
2. **Three "main"s exist and are easy to conflate:** the `main` method, the
   `main` thread that calls it, and the `main` thread group that thread
   belongs to. All three share the name by coincidence, not by rule.
3. **Two constructors:** `ThreadGroup(String)` parents the new group under
   the *calling thread's own* group; `ThreadGroup(ThreadGroup, String)` lets
   you name the parent explicitly.
4. **The `setMaxPriority` loophole is a classic OCJP trap:** lowering a
   group's max priority never touches threads already in the group at a
   higher priority — it only caps threads added afterward.
5. **`activeCount()`/`activeGroupCount()`/both `enumerate()` overloads walk
   sub-groups too** — they were never limited to the group's direct
   membership.
6. **`destroy()`, `setDaemon()`, `isDaemon()`, `isDestroyed()`, and
   `checkAccess()` are deprecated for removal** (since Java 16, `checkAccess`
   since 17) — they still run today, but design new code without them.
7. **`ThreadGroup.stop()`/`suspend()`/`resume()`, the bulk operations this
   lecture's whole "why group threads" pitch leans on, are gone from the
   class entirely** on a current JDK — not deprecated, just absent. The
   modern way to manage a set of related tasks as one unit is **structured
   concurrency** (`StructuredTaskScope`, still preview in Java 25/26).
8. **Virtual threads (Java 21+) don't populate this hierarchy the normal
   way** — they all share one synthetic `VirtualThreads` group whose
   `activeCount()` is always `0`, so any code that walks a `ThreadGroup` tree
   to find "all active threads" only ever sees platform threads.
9. **The actual system-thread roster has moved on**: `Finalizer` is still
   present, but `Notification Thread` and `Common-Cleaner` are newcomers
   (`Cleaner`, Java 9's replacement for `finalize()`, wasn't part of this
   recording's Java 6/7 world) — the concept and the hierarchy-walking code
   are unchanged, only the guest list differs.

---

**Next:** Video 096 — java.util.concurrent package (locks intro)
