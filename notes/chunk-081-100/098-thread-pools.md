# Video 098 — Java Thread Pools (Executor Framework)

## Video info

**Title:** Core Java With OCJP/SCJP: Multithreading Enhancement  Part- 4|| java thread pools

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 98 of 203 |
| Series | Multithreading Enhancement · Part 4 |
| Topic | java thread pools · Executor framework · Callable & Future |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 00m 27s |
| Video ID | Qgz6p-y-YUE |
| Watch | https://www.youtube.com/watch?v=Qgz6p-y-YUE |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Part 4 of Multithreading Enhancement introduces the **Executor framework** —
`java.util.concurrent`'s answer to "stop creating a brand-new `Thread` for
every job." Sir builds the motivation from a connection-pool analogy,
demonstrates a fixed thread pool live at five different sizes, then pivots to
`Runnable`'s one real limitation — it can't hand anything back to the caller —
and introduces `Callable` and `Future` as the fix. He closes with the
six-point Runnable-vs-Callable comparison that OCJP and interviews both like
to ask about.

---

## 00:05 — Topic: thread pools (Executor framework)

Board: **Thread pools (Executor framework)**.

## 00:45 — Why thread pools: the connection-pool analogy

Sir's starting point is JDBC connection pooling. Opening a database
connection, using it, and closing it — every single time — costs performance
and memory. The fix already familiar from JDBC: create a **pool** of
connections once, borrow one when needed, return it when done, reuse it for
the next request.

**Replace "connection" with "thread"** and the same argument applies to jobs:
creating a new `Thread` for every independent job, running it, and letting it
terminate is exactly the same waste, repeated once per job. Ten independent
jobs would mean ten `Thread` objects created and thrown away. Instead: create
a pool of, say, five threads up front, submit jobs to the pool, and let the
same threads execute jobs one after another as they free up — five jobs run
first, then the same five threads pick up the remaining five. A single thread
being reused for multiple jobs is the entire benefit, stated twice by Sir for
emphasis: performance and memory utilization both improve by default.

```java
/*
Creating a new thread for every job
may create performance and memory problems.

To overcome this we should go for Thread pool.

Thread pool is a pool of already created threads
ready to do our job.

Java 1.5 version introduces the thread pool framework
to implement thread pools.

Thread pool framework is also known as the Executor framework.
*/
```

Mechanically: the programmer's job is only to **define** the job and
**submit** it; the Executor framework takes care of creating, starting, and
reusing the threads that actually run it.

## 06:39 — Creating a thread pool

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

ExecutorService service = Executors.newFixedThreadPool(3);
// a pool of 3 already-created threads — use 4, 10, ... as the job calls for
```

> ⚠️ **Modern Java — `Executors` factories are no longer the only entry
> point, and `shutdown()` is no longer the only way to close a pool.**
> Two additions since this recording change how a pool gets created and torn
> down in current code:
>
> - **`ExecutorService` implements `AutoCloseable`** since **Java 19**
>   (JDK-8284866), so it can be opened in a `try`-with-resources statement
>   instead of a manual `shutdown()` call — `close()` initiates an orderly
>   shutdown and then blocks until every submitted task finishes:
>   ```java
>   try (ExecutorService service = Executors.newFixedThreadPool(3)) {
>       service.submit(job);
>   } // service.close() runs automatically here — equivalent to shutdown()
>     // followed by an unbounded awaitTermination()
>   ```
> - **`Executors.newVirtualThreadPerTaskExecutor()`**, finalized in **Java 21**
>   (JEP 444), creates an executor that starts a brand-new, cheap **virtual
>   thread** for every submitted task instead of pulling from a fixed pool.
>   For the I/O-bound, one-thread-blocks-on-one-request jobs this lecture
>   uses as examples, it removes the entire reason to size a pool in the
>   first place — you can go back to "one thread per job," because the
>   thread is now nearly free:
>   ```java
>   try (ExecutorService service = Executors.newVirtualThreadPerTaskExecutor()) {
>       service.submit(job);   // runs on its own virtual thread, not a pooled one
>   }
>   ```
>   Verified on JDK 21: this compiles and each submitted task reports running
>   on a distinct `VirtualThread[#N]`, not on a shared `pool-1-thread-N`.
>   `newFixedThreadPool` still exists and is still the right tool for
>   CPU-bound work you deliberately want to throttle — virtual threads don't
>   replace it, they widen the choice.

## 08:05 — Submitting a Runnable job; shutting down

```java
class MyRunnable implements Runnable {
    public void run() {
        // job
    }
}

MyRunnable job = new MyRunnable();
service.submit(job);

// once every submitted job is done:
service.shutdown();
```

```java
/*
We can submit a Runnable job by using the submit method.
We can shut down an ExecutorService by using the shutdown method.
*/
```

## 10:16 — Demo: PrintJob and ExecutorDemo

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

class PrintJob implements Runnable {
    String name;

    PrintJob(String name) {
        this.name = name;
    }

    public void run() {
        System.out.println(name + " job started by "
                + Thread.currentThread().getName());
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
        }
        System.out.println(name + " job completed by "
                + Thread.currentThread().getName());
    }
}

class ExecutorDemo {
    public static void main(String[] args) {
        PrintJob[] jobs = {
            new PrintJob("Durga"),
            new PrintJob("Ravi"),
            new PrintJob("Shiva"),
            new PrintJob("Pavan"),
            new PrintJob("Suresh"),
            new PrintJob("Anil")
        };

        ExecutorService service = Executors.newFixedThreadPool(3);

        for (PrintJob job : jobs) {
            service.submit(job);
        }
        service.shutdown();
    }
}
```

Verified: compiles and runs — each `PrintJob` prints a start/complete pair
tagged with a `pool-1-thread-N` name, confirming the same three threads carry
all six jobs between them.

Without the executor, doing this by hand would mean six `Runnable`
implementations, six `new Thread(runnable)` calls, and six `.start()` calls —
all written and managed by the programmer. With the pool, that entire block
collapses to "define the jobs, submit them" — thread creation, starting, and
reuse are the framework's problem, not the programmer's.

## 13:45 — Live runs: pool size 1 through 5, six jobs

Sir reruns `ExecutorDemo` five times, changing only the pool size, to make
the reuse behavior visible:

| Pool size | Jobs | Behavior he narrates |
|---|---|---|
| 1 | 6 | One thread runs every job in sequence — Durga → Ravi → Shiva → Pavan → Suresh → Anil — the slowest of the five runs |
| 2 | 6 | Two jobs run at a time; each thread ends up doing about three jobs |
| 3 | 6 | Three jobs start together, then the remaining three; each thread does about two jobs |
| 4 | 6 | Four jobs start on four threads; once two finish, the freed threads pick up the last two — so two of the four threads end up doing a second job |
| 5 | 6 | Five jobs start immediately; one job is left over, so exactly one thread ends up doing a second job |

The one constant across every run, restated on the board once the code was
copied over:

```java
/*
In the above example, three threads are responsible
for executing six jobs,
so that a single thread can be reused for multiple jobs.
*/
```

*Which* thread picks up a second job (thread-1 and thread-3 in Sir's
pool-of-4 run, thread-4 in his pool-of-5 run) is not something the pool
guarantees — it depends on which thread happens to free up first, which the
JVM's scheduler decides. The guarantee is only that *some* thread gets
reused when jobs outnumber threads, not *which* one.

## 28:11 — Where thread pools are used: web and app servers

Every web or application server keeps a pool of threads ready. Each incoming
request is handed a thread from that pool to process it; once the request
finishes, the thread returns to the pool for the next request — exactly the
submit/reuse pattern just demonstrated, just triggered by network requests
instead of a `for` loop. Pool size is configurable from the server's admin
console rather than fixed.

```java
// Board note:
// While developing web servers and application servers
// we can use the thread pool concept.
```

> ❗ **Correction — "default thread pool size is 60" is not a Java rule, and
> isn't a reliable number even as a rule of thumb.**
> Thread-pool sizing on a web or application server is a **server-specific
> configuration value**, not something the Java platform defines. It varies
> by server, connector type, and version — for example, Apache Tomcat's HTTP
> connector has long defaulted its `maxThreads` setting to **200**, not 60.
> The teaching point stands regardless of the exact number: application
> servers pool worker threads and hand them out per request, and the pool
> size is tunable in the server's own configuration. Just don't repeat "60"
> as a fact about Java or about servers in general.

## 30:33 — Runnable's limitation: no return value

```java
class MyRunnable implements Runnable {
    public void run() {
        // job
    }
}

MyRunnable r = new MyRunnable();
Thread t = new Thread(r);
t.start();
// once the job finishes, the thread terminates;
// run()'s return type is void — it hands nothing back to the caller
```

If the caller needs the thread to **return something** once the job is
done, `Runnable` cannot do it — that's the job for **`Callable`**.

## 32:21 — Callable vs Runnable, first pass

| | `Runnable` | `Callable` |
|---|---|---|
| Method | `run()` | `call()` |
| Return type | `void` — returns nothing | `Object` — returns something |
| Checked exceptions in the body | must be handled with `try`/`catch` (`run()` can't declare `throws`) | `call()` already declares `throws Exception` |

```java
/*
Callable interface contains only one method: call
public Object call() throws Exception
*/
```

> ⚠️ **Modern Java — `Callable` and `Future` were already generic in this
> era; use the type parameter.**
> `Callable<V>` and `Future<V>` have been generic since **Java 5** — the same
> release that introduced them — so "`call()` returns `Object`" is really
> "`call()` returns `Object` only if you use the raw type," which is exactly
> what the board notes above do. Verified: the raw form Sir writes compiles
> and runs correctly, but `javac -Xlint:rawtypes,unchecked` flags every line
> that touches it:
> ```text
> warning: [rawtypes] found raw type: Callable
> warning: [rawtypes] found raw type: Future
> warning: [unchecked] unchecked method invocation: method submit in
>          interface ExecutorService is applied to given types
> ```
> Writing `Callable<Integer>` and `Future<Integer>` instead — as the demo
> code below does — removes every one of those warnings and gets a
> compile-time check that `call()` returns the type the caller expects. Keep
> "`call()`'s return type is `Object`" as the answer for the erasure-level
> OCJP question; write `Callable<V>` in anything you'd actually ship.

## 34:27 — Submitting a Callable; Future holds the result

```java
/*
In the case of a Runnable job,
the thread won't return anything after completing the job.

If a thread is required to return some result after execution,
then we should go for Callable.

Callable interface contains only one method: call
  public Object call() throws Exception

If we submit a Callable object to an executor,
then after completing the job
the thread returns an object of the type Future.

A Future object can be used to retrieve the result
from a Callable job.
*/
```

```java
import java.util.concurrent.*;

ExecutorService service = Executors.newFixedThreadPool(3);

for (Callable<Integer> job : callableJobs) {
    Future<Integer> f = service.submit(job);   // holds the returned value
    System.out.println(f.get());               // retrieve the result
}
service.shutdown();
```

> ❗ **Correction — this exact loop shape throws away the pool's
> concurrency.** `Future.get()` **blocks** the calling thread until that
> job's result is ready. Calling `submit()` and then immediately `get()`
> inside the same loop iteration means the next job is never submitted
> until the current one finishes — regardless of pool size, the jobs end up
> running one after another, not concurrently. Verified with three
> 500 ms `Callable` jobs on a 3-thread pool:
> ```text
> submit-then-get in the loop:  got 1 at t+511ms, got 2 at t+1031ms, got 3 at t+1532ms  → 1533ms total
> submit all, then get all:     got 1 at t+512ms, got 2 at t+525ms,  got 3 at t+525ms   → 525ms total
> ```
> Same jobs, same pool — nearly 3× slower with the pattern taught here,
> because the pool's three threads never get three jobs at once. The fix
> is to finish submitting everything first, then collect the results:
> ```java
> List<Future<Integer>> futures = new ArrayList<>();
> for (Callable<Integer> job : callableJobs) {
>     futures.add(service.submit(job));   // submit all first — nothing blocks yet
> }
> for (Future<Integer> f : futures) {
>     System.out.println(f.get());        // now collect, after every job is running
> }
> ```
> The `CallableFutureDemo` program below uses the same submit-then-get-per-job
> shape as the board code, so its jobs run mostly one at a time too — it
> still prints the right sums, since `get()` only blocks, it doesn't corrupt
> the result, but it is not actually demonstrating three jobs running at once.

## 41:04 — Demo: CallableFutureDemo — sum of first n numbers

```java
import java.util.concurrent.*;

class MyCallable implements Callable<Integer> {
    int num;

    MyCallable(int num) {
        this.num = num;
    }

    public Integer call() throws Exception {
        System.out.println(Thread.currentThread().getName()
                + " is responsible to find sum of first " + num + " numbers");
        int sum = 0;
        for (int i = 1; i <= num; i++) {
            sum = sum + i;
        }
        return sum;
    }
}

class CallableFutureDemo {
    public static void main(String[] args) throws Exception {
        MyCallable[] jobs = {
            new MyCallable(10),
            new MyCallable(20),
            new MyCallable(30),
            new MyCallable(40),
            new MyCallable(50),
            new MyCallable(60)
        };

        ExecutorService service = Executors.newFixedThreadPool(3);
        for (MyCallable job : jobs) {
            Future<Integer> f = service.submit(job);
            System.out.println(f.get());
        }
        service.shutdown();
    }
}
```

Verified: compiles and prints the expected sums, `n(n+1)/2` for each `n`:

```text
55    (sum 1..10)
210   (sum 1..20)
465   (sum 1..30)
820   (sum 1..40)
1275  (sum 1..50)
1830  (sum 1..60)
```

The rule Sir gives for choosing between the two: **if the thread must return
something, go `Callable`; if not, `Runnable`.**

## 50:24 — Runnable vs Callable, the full comparison

```java
/*
1. If a thread is not required to return anything after completing the job
     -> go for Runnable.
   If a thread is required to return something after completing the job
     -> go for Callable.

2. Runnable interface contains only one method: run
   Callable interface contains only one method: call

3. Runnable job is not required to return anything
     -> return type of the run method is void.
   Callable job is required to return something
     -> return type of the call method is Object.

4. Within the run method, if there is any chance of a checked exception
     -> it must compulsorily be handled with try-catch,
     -> because run cannot declare throws
        (its parent, Runnable.run, doesn't throw a checked exception,
         and the overriding rule forbids widening that).
   Within the call method, if there is any chance of a checked exception
     -> it is not required to be handled with try-catch,
     -> because call already declares throws Exception.

5. Runnable is present in the java.lang package.
   Callable is present in the java.util.concurrent package.

6. Runnable was introduced in version 1.0.
   Callable was introduced in version 1.5 (with thread pools / the Executor
   framework).
*/
```

The overriding rule behind point 4, made concrete:

```java
class MyRunnable implements Runnable {
    public void run() {
        try {
            Thread.sleep(1000);   // checked exception -> must be caught here
        } catch (InterruptedException e) {
        }
        // public void run() throws Exception { }
        // CE: run() in MyRunnable cannot implement run() in Runnable —
        //     overridden method does not throw Exception
    }
}

class MyCallable implements Callable<String> {
    public String call() throws Exception {
        Thread.sleep(1000);   // OK — call() already declares throws Exception
        return "ok";
    }
}
```

Verified: uncommenting `run() throws Exception` in `MyRunnable` produces
exactly that compile error — a checked exception can't be added to an
overriding method whose parent doesn't throw it, and `Runnable.run()`
doesn't.

## 59:55 — Session wrap

Covered: the advantage of thread pools, how to create one, the Executor
framework, why `Callable` and `Future` exist, and the Runnable-vs-Callable
differences — basic working knowledge, not the full API, by Sir's own
framing.

---

## Exam and interview points

1. **A thread pool reuses a fixed set of already-created threads across
   many jobs**, instead of spawning and discarding a new `Thread` per job —
   this is what improves both performance and memory usage.
2. **The Executor framework (`java.util.concurrent`) shipped in Java 1.5**
   and is also called "the thread pool framework"; `Executors.newFixedThreadPool(n)`
   is the everyday way to create a pool.
3. **`Runnable.run()` returns `void`** — a submitted `Runnable` job cannot
   hand any result back to the caller. **`Callable<V>.call()` returns `V`**
   (`Object` at the raw-type level Sir teaches) and can.
4. **Only `Callable.call()` declares `throws Exception`.** `Runnable.run()`
   cannot declare any checked exception, because the overriding rule forbids
   widening the throws clause of the method it overrides.
5. **`Future<V>` is what `submit(Callable)` returns**, and `Future.get()` is
   how the result is retrieved — but `get()` **blocks**, so submitting a job
   and immediately calling `get()` inside the same loop iteration serializes
   supposedly-parallel jobs. Submit everything first, then collect.
6. **Package and version, a favorite fact question:** `Runnable` is in
   `java.lang`, from Java 1.0. `Callable` is in `java.util.concurrent`, from
   Java 1.5, alongside the Executor framework itself.
7. **Web and application servers pool worker threads for incoming requests**
   — the exact same reuse idea as `ExecutorService`, just triggered by the
   network instead of a loop. The pool size is a server config value, not a
   Java-defined constant.
8. **Modern context worth knowing past OCJP:** `ExecutorService` implements
   `AutoCloseable` since Java 19, so a pool can be opened in
   try-with-resources instead of a manual `shutdown()`; `Executors.newVirtualThreadPerTaskExecutor()`
   (Java 21, JEP 444) gives every task its own cheap virtual thread, which
   removes the need to size a pool at all for I/O-bound work like this
   lecture's examples; and always parameterize `Callable<V>`/`Future<V>` in
   real code rather than using the raw types this recording boards.

---

**Next:** Video 099 — ThreadLocal
