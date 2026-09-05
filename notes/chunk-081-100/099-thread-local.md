# Video 099 — ThreadLocal

## Video info

**Title:** Core Java With OCJP/SCJP: Multithreading Enhancement  Part- 5|| java thread local

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 99 of 203 |
| Series | Multithreading Enhancement · Part 5 |
| Topic | java thread local |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 11m 48s |
| Video ID | 4ZLkbWWpkyk |
| Watch | https://www.youtube.com/watch?v=4ZLkbWWpkyk |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Part 5 of Multithreading Enhancement is entirely about **`ThreadLocal`**: what
"thread-local" means, why you'd want it (a Servlet-attribute-scope analogy,
then a method-call-chain problem), the four-method API (`get`/`set`/
`initialValue`/`remove`), two live demos, and then the trickier half —
**`InheritableThreadLocal`** and its `childValue()` hook for parent-to-child
data flow between threads.

---

### 00:05 — Topic introduction: what "thread local" means

**Question on the board:** *What does "thread local" mean?*

**Answer:** Something **local to a thread** — data that belongs to one
particular thread and is readable wherever that thread executes, without
other threads seeing or sharing it.

### 00:39 — Servlet scope analogy (request, session, application)

Sir sets up the idea of *scope* with Servlet attribute scopes, for anyone who
has already seen the Servlet module:

| Scope | Availability | Analogy |
|---|---|---|
| Request scope | Only for that one HTTP request; gone once the request completes | An attribute set on `HttpServletRequest` |
| Session scope | All requests in the same session, until logout | Gmail: log in once, send ten mails, check the inbox — no re-login until you log out |
| Application / context scope | The entire web application's lifetime | Global shared configuration |

**ThreadLocal defines a fourth kind of scope — thread scope.** The boundary
is neither the request nor the session; it is the **thread** that happens to
be executing.

### 02:20 — Why thread scope is needed (a method-call chain)

**The problem, from class discussion:** `main()` runs on the main thread and
calls `yam1()`, which calls `yam2()`. Partway through `yam1()` the thread
fetches some data (say, from the database) that `yam2()` — several calls
deeper — also needs. Threading that value through every method signature in
between is exactly the boilerplate nobody wants.

**Solution:** attach the data to the **thread itself**. Any method that
thread later executes, at any depth, can retrieve it — no extra parameter
needed.

```java
public class CallChainDemo {
    public static void main(String[] args) {
        yam1();   // runs on the main thread
    }

    static void yam1() {
        Object dbData = fetchFromDatabase();
        // attach dbData to THIS thread (conceptually — ThreadLocal does this)
        yam2();
    }

    static void yam2() {
        // dbData is needed here too, without it being a parameter
        // ThreadLocal: retrieve dbData without ever passing it down
    }

    static Object fetchFromDatabase() { return "db-result"; }
}
```

### 03:24 — ThreadLocal purpose and definition

**Typical requirements that call for `ThreadLocal`:**

- a separate `Connection` per thread
- a separate counter per thread
- a separate customer ID per thread

**Board (paraphrased):** *`ThreadLocal` defines thread-local variables.
Wherever a thread executes, its thread-local variable is reachable. Once a
value is set for a thread on a `ThreadLocal`, that thread can read it from
anywhere.*

### 04:33 — The "box" analogy: one ThreadLocal, many per-thread copies

For a per-thread `count`, you create **one** `ThreadLocal` object — it
maintains a **separate copy per thread** internally:

```text
ThreadLocal box
├── Thread-1 → count = 1
├── Thread-2 → count = 2
└── Thread-3 → count = 3
```

```java
ThreadLocal<Integer> countBox = new ThreadLocal<>();

// Thread-1's own copy
countBox.set(1);
System.out.println(countBox.get());   // 1, on thread-1

// Thread-2's own copy — independent of thread-1's
countBox.set(2);
System.out.println(countBox.get());   // 2, on thread-2
```

### 05:34 — Without ThreadLocal: the programmer's burden

Without it, a program with 1000 threads needing a per-thread counter would
need **1000 separate variables**, hand-maintained. With `ThreadLocal`, the
class maintains those 1000 copies internally behind **one** object:

```java
// WITHOUT ThreadLocal — one variable per thread, doesn't scale
int countForThread1;
int countForThread2;
int countForThread3;
// ... 1000 threads → 1000 separate variables

// WITH ThreadLocal — one object, per-thread copies handled internally
ThreadLocal<Integer> count = new ThreadLocal<>();
```

### 06:19 — ThreadLocal class: board notes

**Package:** `java.lang` — no import needed, same as `String` or `Thread`.

1. `ThreadLocal` provides thread-local variables.
2. It maintains values on a **per-thread basis**.
3. Each `ThreadLocal` object maintains a separate value (a user ID,
   transaction ID, etc.) **for every thread** that touches it.
4. A thread can access, change, or remove its own local value.
5. That value is reachable from **any part of the code the thread
   executes** — not just the method that set it.

### 09:34 — Real-world example: a Servlet transaction ID

**Scenario:** a Servlet invokes several business methods, and every request
needs its own unique transaction ID threaded through all of them.

**Mapping to threads:** in the Servlet single-instance, multi-threaded
model, Sir's claim is that *"every request gets its own thread."* One
request → one thread → one transaction ID per thread → `ThreadLocal` is
exactly the right tool.

```java
public class TransactionServlet extends HttpServlet {
    // ONE ThreadLocal object — a separate transaction ID per request-thread
    static final ThreadLocal<String> transactionId = new ThreadLocal<>();

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) {
        transactionId.set(generateUniqueId());
        try {
            businessMethod1();
            businessMethod2();
        } finally {
            transactionId.remove();   // see the correction below
        }
    }

    void businessMethod1() {
        String id = transactionId.get();   // same thread's ID, no parameter needed
    }

    void businessMethod2() {
        String id = transactionId.get();
    }

    String generateUniqueId() { return "TXN-" + System.nanoTime(); }
}
```

> ❗ **Correction — "a new thread for every request" is not how real
> containers behave.** Tomcat, Jetty, and every production container run
> requests on a **bounded worker thread pool**, reusing the same physical
> threads across many requests over time — they do not spawn a fresh thread
> per hit. That distinction is exactly why the `try/finally { transactionId
> .remove(); }` above is not optional: a `ThreadLocal.set()` value that is
> never removed **survives on the pooled thread** and leaks into whichever
> unrelated request that thread services next — a real, well-documented
> class of bug (stale transaction IDs, security-context bleed between
> users). Sir's model is the right mental picture for "how does a thread
> reach a value set earlier," but assume a thread pool underneath, and
> always clean up in a `finally` block.

### 12:35 — Version history

- **`ThreadLocal` was introduced in Java 1.2** (Sir is explicit that it is
  *not* 1.5 — a common guess).
- It was **enhanced in Java 1.5**, which added the **`remove()`** method.
- `InheritableThreadLocal` shipped alongside it, also in **Java 1.2**.

Verified against the JDK's own source (`@since` tags in
`java.lang.ThreadLocal` / `java.lang.InheritableThreadLocal`): both classes
are `@since 1.2`; `remove()` is `@since 1.5`. Sir's dates are correct.

**Further theory points from the board:**

- ThreadLocal can be associated with **thread scope**.
- **All** code executed by a thread has access to that thread's
  thread-local variables.
- A thread can access **only its own** entry — T1's value is never visible
  to T2.
- Once a thread reaches the **dead** state, its ThreadLocal entries become
  **eligible for garbage collection**.

```java
ThreadLocal<Integer> tl = new ThreadLocal<>();
// Thread T1: tl.set(10); tl.get() → 10
// Thread T2: tl.get() → null (or T2's own value, never T1's 10)
```

### 16:28 — Constructor

```java
ThreadLocal<Object> tl = new ThreadLocal<>();
```

Whichever thread accesses this one object gets its own maintained copy —
count, username, connection, anything.

### 17:35 — ThreadLocal API: four methods

| Method | Thread asks… | Effect |
|---|---|---|
| `get()` | "What's my value?" | Returns the current thread's value |
| `initialValue()` | "What's my starting value?" | Called internally the first time a thread reads with nothing set; default returns `null` |
| `set(newValue)` | "Set my value to this." | Stores a value for the current thread |
| `remove()` *(Java 1.5+)* | "Forget my value." | Removes the current thread's entry |

```java
ThreadLocal<String> tl = new ThreadLocal<>();

tl.get();           // null — default initialValue()
tl.set("Durga");    // current thread's value = "Durga"
tl.get();           // "Durga"
tl.remove();        // remove current thread's entry
tl.get();           // null again — initialValue() is invoked internally, once more
```

> ❗ **Correction — the board wrote `public Object initialValue()`; the real
> signature is `protected`.** In the actual JDK source, both
> `initialValue()` and `InheritableThreadLocal.childValue()` are declared
> `protected T initialValue()` / `protected T childValue(T parentValue)`.
> Sir's demos still compile because Java lets an override **widen** access
> (`protected` → `public` is legal); what it will not let you do is
> **narrow** it. This is exam bait: "can you override `initialValue()` as
> `private`?" — no, that's not overriding, that's hiding, and it fails to
> compile. Confirmed by compiling a `public` override of the real
> `protected` method — it succeeds precisely because it widens, not because
> the original was public.

### 22:52 — Walk-through: get → set → get → remove → get

```java
public class ThreadLocalWalkthrough {
    public static void main(String[] args) {
        ThreadLocal<String> tl = new ThreadLocal<>();

        System.out.println(tl.get());   // null — nothing set yet
        tl.set("Durga");
        System.out.println(tl.get());   // Durga
        tl.remove();
        System.out.println(tl.get());   // null — initialValue() runs again
    }
}
```

**Key point after `remove()`:** the next `get()` re-invokes
`initialValue()` — default `null`, or your overridden value if you
customized it.

### 26:30 — Demo 1: basic create / get / set / remove

Sir live-codes with the board's raw type; it compiles (with an `unchecked`/
`rawtypes` warning), and the flow is identical with generics:

```java
class ThreadLocalDemo1 {
    public static void main(String[] args) {
        ThreadLocal tl = new ThreadLocal();   // raw type, as on the board

        System.out.println(tl.get());   // null
        tl.set("Durga");
        System.out.println(tl.get());   // Durga
        tl.remove();
        System.out.println(tl.get());   // null
    }
}
```

**Output:**

```text
null
Durga
null
```

### 30:43 — Demo 1A: overriding `initialValue()`

**Question:** can you override `initialValue()` to avoid the default `null`?
**Yes** — via an anonymous subclass:

```java
class ThreadLocalDemo1A {
    public static void main(String[] args) {
        ThreadLocal tl = new ThreadLocal() {
            public Object initialValue() {
                return "ABC";
            }
        };

        System.out.println(tl.get());   // ABC — not null
        tl.set("Durga");
        System.out.println(tl.get());   // Durga
        tl.remove();
        System.out.println(tl.get());   // ABC again — initialValue() re-runs, NOT null
    }
}
```

**Output:**

```text
ABC
Durga
ABC
```

> ⚠️ **Modern Java — `ThreadLocal.withInitial(Supplier)` (Java 8).** The
> anonymous-subclass dance above is exactly what a lambda replaces:
>
> ```java
> ThreadLocal<String> tl = ThreadLocal.withInitial(() -> "ABC");
> ```
>
> Same behaviour — `get()` returns `"ABC"` until `set()`, and again after
> `remove()` — one line instead of a five-line anonymous class. Still worth
> knowing the `initialValue()` override for OCJP (and for the rare case
> where the initial value needs per-call logic beyond a `Supplier`), but
> `withInitial` is what production code writes today.

### 34:45 — Demo 2: a separate customer/transaction ID per thread

**Scenario:** four `CustomerThread` objects (C1–C4) are started; each needs
its own customer ID. **How many `ThreadLocal` objects does that take? One** —
it maintains one ID per thread internally via an auto-incrementing
`initialValue()`.

```java
class ThreadLocalDemo2 {
    static int custId = 0;

    static ThreadLocal<Integer> tl = new ThreadLocal<Integer>() {
        public Integer initialValue() {
            return ++custId;
        }
    };

    public static void main(String[] args) {
        CustomerThread c1 = new CustomerThread("CustomerThread-1");
        CustomerThread c2 = new CustomerThread("CustomerThread-2");
        CustomerThread c3 = new CustomerThread("CustomerThread-3");
        CustomerThread c4 = new CustomerThread("CustomerThread-4");

        c1.start();
        c2.start();
        c3.start();
        c4.start();
    }
}

class CustomerThread extends Thread {
    CustomerThread(String name) {
        super(name);
    }

    public void run() {
        System.out.println(
            Thread.currentThread().getName()
            + " executing with customer ID "
            + ThreadLocalDemo2.tl.get()
        );
    }
}
```

**Sample output** (order not guaranteed — depends on the scheduler):

```text
CustomerThread-1 executing with customer ID 1
CustomerThread-3 executing with customer ID 4
CustomerThread-4 executing with customer ID 3
CustomerThread-2 executing with customer ID 2
```

Four threads → four unique IDs → **one** `ThreadLocal` object doing the
bookkeeping. Without it, the alternative is `custId1`, `custId2`, `custId3`…
by hand — unworkable at 1000 threads.

### 44:17 — ThreadLocal vs inheritance: setting up the question

Covered so far: what ThreadLocal is, its purpose, how to create one, and
its four methods. **Next question:** is a parent thread's ThreadLocal value
available to a child thread it starts, by default?

### 45:12 — Parent thread / child thread: the default answer is no

```java
class ParentThread extends Thread {
    static ThreadLocal<String> tl = new ThreadLocal<>();

    public void run() {
        tl.set("PP");
        System.out.println("Parent thread value: " + tl.get());   // PP

        ChildThread ct = new ChildThread();
        ct.start();
    }
}

class ChildThread extends Thread {
    public void run() {
        // static tl accessed via the class name
        System.out.println("Child thread value: " + ParentThread.tl.get());
    }
}
```

**Question:** parent set `"PP"` — does the child see it? **Answer: no,
`null`.** Even though `tl` is a `static` field (one shared reference), each
**thread** gets its own **entry** inside the `ThreadLocal`; the parent set
its own entry, and the child's entry was never touched.

### 51:14 — Demo 3: ThreadLocal — child gets null

```java
class ThreadLocalDemo3 {
    public static void main(String[] args) throws InterruptedException {
        ParentThread pt = new ParentThread();
        pt.start();
        pt.join();
    }
}
```

**Output:**

```text
Parent thread value: PP
Child thread value: null
```

Three threads are involved: **main** (creates and starts `ParentThread`),
**parent** (sets `"PP"`, starts `ChildThread`), **child** (reads `null`).

### 54:17 — InheritableThreadLocal: when the child should see the parent's value

**Requirement:** the child *should* see the parent's value. **Don't** use
plain `ThreadLocal` — use **`InheritableThreadLocal`**, which is a **subclass
of `ThreadLocal`**:

```java
class ParentThread extends Thread {
    static InheritableThreadLocal<String> tl = new InheritableThreadLocal<>();

    public void run() {
        tl.set("PP");
        System.out.println("Parent thread value: " + tl.get());   // PP

        ChildThread ct = new ChildThread();
        ct.start();
    }
}

class ChildThread extends Thread {
    public void run() {
        // inherits the parent's value at thread-creation time
        System.out.println("Child thread value: " + ParentThread.tl.get());   // PP
    }
}
```

**Output:**

```text
Parent thread value: PP
Child thread value: PP
```

### 56:26 — Overriding `childValue()` for a customized child value

By default a child's value is **exactly** the parent's. To hand the child
something different, override `childValue(Object parentValue)`:

```java
class ParentThread extends Thread {
    static InheritableThreadLocal<String> tl = new InheritableThreadLocal<String>() {
        protected String childValue(String parentValue) {
            // parentValue is "PP" here; return something else for the child
            return "CC";
        }
    };

    public void run() {
        tl.set("PP");
        System.out.println("Parent thread value: " + tl.get());   // PP

        ChildThread ct = new ChildThread();
        ct.start();
    }
}

class ChildThread extends Thread {
    public void run() {
        System.out.println("Child thread value: " + ParentThread.tl.get());   // CC
    }
}
```

**Output:**

```text
Parent thread value: PP
Child thread value: CC
```

**`childValue()` signature (board), default behaviour:**

```java
protected Object childValue(Object parentValue) {
    return parentValue;   // default: hand the child exactly the parent's value
}
```

### 57:54 — ThreadLocal vs inheritance: three summary points

1. A parent thread's `ThreadLocal` value is **not**, by default, visible to
   a child thread it starts.
2. To make it visible, use **`InheritableThreadLocal`**.
3. By default the child's value equals the parent's exactly; override
   **`childValue()`** to hand the child something different.

```java
// Need per-thread data, no parent→child sharing?         → ThreadLocal
// Need the parent's value inherited by the child thread?  → InheritableThreadLocal
// Need the child to get a DIFFERENT value than the parent? → InheritableThreadLocal + override childValue()
```

### 1:01:19 — InheritableThreadLocal class details

```java
InheritableThreadLocal<String> tl = new InheritableThreadLocal<>();
```

`InheritableThreadLocal` **is a child class of `ThreadLocal`** — it inherits
`get()`, `set()`, `initialValue()`, and `remove()` unchanged, and adds
exactly **one** extra method:

```java
protected Object childValue(Object parentValue)
```

### 1:04:10 — Complete demo: three scenarios, one program

```java
class ThreadLocalDemo3 {
    public static void main(String[] args) throws InterruptedException {
        ParentThread pt = new ParentThread();
        pt.start();
        pt.join();
    }
}

class ParentThread extends Thread {
    static InheritableThreadLocal<String> tl = new InheritableThreadLocal<String>() {
        protected String childValue(String parentValue) {
            return "CC";
        }
    };

    public void run() {
        tl.set("PP");
        System.out.println("Parent thread value: " + tl.get());

        ChildThread ct = new ChildThread();
        ct.start();
    }
}

class ChildThread extends Thread {
    public void run() {
        System.out.println("Child thread value: " + ParentThread.tl.get());
    }
}
```

### 1:08:22 — The three output scenarios, side by side

| Scenario | `tl` type | `childValue()` overridden? | Parent value | Child value |
|---|---|---|---|---|
| A | `ThreadLocal` | n/a | `PP` | `null` |
| B | `InheritableThreadLocal` | no | `PP` | `PP` |
| C | `InheritableThreadLocal` | yes → returns `"CC"` | `PP` | `CC` |

This table is the whole lecture compressed to one row each: plain
`ThreadLocal` never shares with the child; `InheritableThreadLocal` shares by
default; overriding `childValue()` lets you reshape what the child gets.

### 1:11:20 — Lecture wrap-up

| Topic | Class | Key idea |
|---|---|---|
| Per-thread local variable | `ThreadLocal` | Separate copy per thread; one object serves all threads |
| Constructor | `new ThreadLocal<>()` | Creates the container |
| `get()` | inherited | Current thread's value |
| `set(v)` | inherited | Set current thread's value |
| `initialValue()` | override optional | Default `null`; customize via subclass or `withInitial` |
| `remove()` | Java 1.5+ | Remove current thread's entry; next `get()` re-invokes `initialValue()` |
| Parent → child inheritance | `InheritableThreadLocal` | Child inherits the parent's value at thread-creation time |
| Custom child value | `childValue(parentValue)` | Override to give the child a different value than the parent |

> ⚠️ **Modern Java — virtual threads (Java 21) and a lighter-weight
> alternative for this exact use case (Java 25).**
>
> **Virtual threads still play by these rules.** `ThreadLocal` and
> `InheritableThreadLocal` work the same way for a virtual thread as for a
> platform thread — each virtual thread gets its own copy, and a virtual
> thread still inherits an `InheritableThreadLocal` value from its creator
> at creation time (confirmed in `Thread`'s own class-level Javadoc). You can
> opt a thread out of that inheritance with
> `Thread.ofVirtual().inheritInheritableThreadLocals(false)`. The catch is
> scale: code that is fine with a few hundred platform threads holding
> thread-locals can become a real memory problem when a server creates a
> *virtual* thread per request and each one drags along a heavyweight
> thread-local value — the JDK team explicitly cautions against using
> `ThreadLocal` as a general extension mechanism (the way logging
> frameworks stash an MDC context, for instance) once thread counts move
> into the hundreds of thousands.
>
> **`ScopedValue` (finalized in Java 25, JEP 506) is the modern answer to
> exactly Sir's `yam1()`-calls-`yam2()` motivating example** — one-way,
> immutable data flowing down a call chain without adding a parameter to
> every method in between:
>
> ```java
> static final ScopedValue<String> TXN_ID = ScopedValue.newInstance();
>
> void doGet() {
>     ScopedValue.where(TXN_ID, generateUniqueId())
>                .run(() -> {
>                    businessMethod1();
>                    businessMethod2();
>                });
> }
>
> void businessMethod2() {
>     String id = TXN_ID.get();   // visible for the life of run(), then gone
> }
> ```
>
> Unlike `ThreadLocal`, a `ScopedValue` is bound only for the dynamic extent
> of `run()`, is immutable once bound, and needs no `remove()` — it cannot
> leak into the next task on a pooled or virtual thread, which is precisely
> the failure mode the servlet correction above warns about. It compiles
> and runs with no `--enable-preview` flag on JDK 25 or 26. Its companion,
> **`StructuredTaskScope`** (structured concurrency for fork-join-style
> parallel work), is still a **preview** API as of JDK 26 — it compiles only
> with `--enable-preview`, so treat it as "worth watching," not yet an exam
> or production-safe answer.
>
> None of this replaces the lecture's four-method API or
> `InheritableThreadLocal` — those are still exactly how legacy code (and
> most current code) does per-thread state, and still what OCJP asks about.
> It's the newest tool for the *specific* job this video's opening example
> describes.

---

## Exam and interview points

1. **`ThreadLocal` = one object, a separate value per thread.** The "box"
   analogy: create it once, every thread that touches it gets its own
   compartment.
2. **Default `initialValue()` returns `null`**; override it (or use
   `ThreadLocal.withInitial(Supplier)`, Java 8) to change that.
3. **After `remove()`, the next `get()` re-invokes `initialValue()`** — you
   get the initial value back, not a stale `null` forever.
4. **`remove()` was added in Java 1.5**; `ThreadLocal` itself (and
   `InheritableThreadLocal`) date to **Java 1.2** — both dates confirmed
   against the JDK's own source, not just the lecture's memory.
5. **Plain `ThreadLocal`: a child thread never sees its parent's value** —
   it gets its own entry, defaulting to `null` (or its own `initialValue()`).
6. **`InheritableThreadLocal` is a subclass of `ThreadLocal`** that copies
   the parent's value to the child **at thread-creation time**.
7. **Override `childValue(Object parentValue)`** to hand the child a value
   different from the parent's; the default implementation just returns
   `parentValue` unchanged.
8. **`initialValue()` and `childValue()` are declared `protected` in the
   real JDK**, not `public` — you may override with a wider modifier
   (`public`), never a narrower one.
9. **Thread pools break the naive "one thread, one request" mental model.**
   A `ThreadLocal` value set and never removed on a pooled thread leaks
   into whatever the pool hands that thread next — always `remove()` in a
   `finally` block.
10. **Package is `java.lang`** — no import required, same as `String`.
11. For new code that needs exactly the "pass this down the call chain
    without a parameter" pattern, **`ScopedValue` (Java 25)** is the modern,
    leak-proof alternative; `ThreadLocal`/`InheritableThreadLocal` remain
    the OCJP answer and the correct read of any legacy codebase.

---

**Next:** Video 100 — Inner Classes Part-1 Introduction
