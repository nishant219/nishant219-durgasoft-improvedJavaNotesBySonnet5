# Video 067 — Singleton class

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-17 || singleton class

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 67 of 203 |
| Series | OOPs · Part 17 |
| Topic | singleton class |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 35m 18s |
| Video ID | SniLNfFejiU |
| Watch | https://www.youtube.com/watch?v=SniLNfFejiU |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

**Continuity.** This is the next application of **private constructors** after
the earlier constructor videos: **singleton classes**. He defines the term,
names `Runtime` / Business Delegate / Service Locator as real examples, tells
the ₹3-lakh one-to-one-vs-batch story to motivate reuse, shows
`Runtime.getRuntime()` as a factory method, then writes two ways to build a
singleton by hand. He closes with a twist — a class that isn't `final` but
still can't be subclassed — which ends the OOPs/constructor stretch of the
course. He does **not** cover enum singleton, double-checked locking,
`volatile`, serialization, `clone()`, or reflection in this video; those gaps
are filled below with Modern Java callouts.

---

### 00:05 — Next use of private constructors: singleton classes

Private constructors already appeared in earlier videos. This is their next
big application: **singleton classes**. Keep that link in mind for the whole
lecture — singleton is not a keyword, it's a class design that *needs* a
private constructor to work.

### 00:18 — Interview questions he flags

Five questions to be able to answer on the spot:

- What is a singleton class?
- What is the advantage of a singleton class?
- Is it possible to create our own singleton class?
- How do you create one — with an example?
- The whole reasoning ("story") behind singleton classes.

### 00:46 — Definition

> **For any Java class, if we are allowed to create only one object, such a
> type of class is called a singleton class.**

Not "a class with one method," not "a class with only static members." The
restriction is purely on **object count**: exactly one, ever.

### 01:01 — Examples: `Runtime`, Business Delegate, Service Locator

- **`Runtime`** — a real JDK singleton (`java.lang.Runtime`).
- **Business Delegate** — a J2EE design pattern, implemented as a singleton.
- **Service Locator** — another J2EE pattern, also singleton.

```java
Runtime
```

- Business Delegate
- Service Locator
- etc.

> ⚠️ **Modern Java — Business Delegate and Service Locator are legacy J2EE
> patterns.** Both come from the EJB 2.x era, where every call to a remote EJB
> was expensive, so an app wrapped remote lookups behind a local façade
> (Business Delegate) and cached JNDI lookups (Service Locator). Modern
> Jakarta EE and Spring applications use dependency injection (`@Inject`,
> `@Autowired`) instead — the container hands you the collaborator directly,
> so there is nothing left to delegate or locate. Both patterns are still
> asked about in interviews as *classic* GoF/J2EE catalog entries, but you
> will rarely find fresh code writing them today.

### 01:39 — Struts `ActionServlet`: a genuine disagreement

Some people count Struts's **`ActionServlet`** as a singleton, some don't — he
does not settle it, just notes the debate exists. The three examples he
commits to are **`Runtime`, Business Delegate, Service Locator**. He will not
implement the latter two here; the class he actually writes is `Test`, plus
the real `Runtime`.

> The disagreement is reasonable: a servlet container creates exactly one
> instance of a servlet by default (so `ActionServlet` behaves like a
> singleton *in practice*), but nothing in its code enforces "only one object
> ever" the way a private constructor does — the container's contract, not
> the class design, is what limits it to one instance.

> ⚠️ **Modern Java — Struts itself has faded.** Struts 1 (the version with
> `ActionServlet`) reached end-of-life in 2013. Struts 2 is still maintained
> but has had a string of serious CVEs and is a shrinking share of new work;
> modern Java web apps mostly use Spring MVC or a REST framework instead.

### 02:10–02:25 — Board heading and definition (restated)

**Singleton classes**

**For any Java class, if we are allowed to create only one object, such a
type of class is called singleton class.**

**Example:** `Runtime`, Business Delegate, Service Locator, etc.

### 03:33 — Advantage: the office story starts

Heading: **Advantage of singleton class.** The concept is small; he motivates
it with a story before touching code.

### 04:05 — "I want SCJP class" → next batch, no problem

Someone at the office asks for an SCJP class → a batch starts next month, fine.

### 04:18–04:34 — "I want one-to-one" → "I want Durga's classes only"

The request escalates. First: "no, I want one-to-one class" — fine, junior
faculty can handle one-to-one sessions. Then: "no, I want Durga's classes
only" — now it has to be him personally, so the office calls him directly:
someone wants one-to-one, and insists only Durga Sir can be the faculty; what
should they tell the person?

### 05:00 — He can do it — but the fee is ₹3 lakhs

He agrees, but names a fee: **₹3 lakhs** for a solo session. Reasoning: a
normal batch has **100 students** paying **₹3,000** each (100 × ₹3,000 = ₹3
lakhs). Spending the same time on one person only, instead of on 100, costs
that same total, so the fee has to cover it. Quoting ₹3 lakhs for one-to-one
reliably makes the person "not come one second" back to the office — it's too
much even for a dedicated slot — but there's no cheaper option if it really
has to be solo, only-him, one-to-one.

### 05:56–06:29 — The batch model is *why* students actually come

If every student had to pay ₹3 lakhs individually, nobody would enroll. But
100 students with the *same requirement* (SCJP) sitting in **one classroom**
means the same ₹3 lakhs splits 100 ways → ₹3,000 each, which people can
afford — and do pay.

### 07:07 — The punch line

> **If several people have the same requirement, don't create a separate
> object for every person — create only one object and reuse it for every
> requirement. Memory utilization and performance improve by default.**

One faculty, one session, 100 students — not 100 separate one-to-one setups.
That's the whole singleton idea, translated later into `Runtime` and `Test`.

### 07:26 — Same idea with `Runtime`

First caller wants a `Runtime` object → one gets created. Second caller wants
one too → same purpose, so **reuse** the existing object instead of making a
new one. Third caller, same thing. Scale that to **one lakh** (100,000)
callers: still reuse, never create a second object.

Creating **one** shared object versus **one lakh** separate ones — sharing
wins on memory and performance. That's singleton, in Java terms.

### 08:23–08:56 — Board dictation: need and advantage

> **If several people have the same requirement, then it is not recommended
> to create a separate object for every requirement. We have to create only
> one object and we can reuse the same object for every similar requirement,
> so that performance and memory utilization will be improved.**

That's the central advantage of singleton classes, full stop.

### 11:18 — How does the first caller actually get `Runtime`?

Not `new Runtime()` — **singleton objects can't be created with a constructor
or `new` operator from outside**, because if that door were open, anyone
could create as many objects as they wanted, defeating the whole design. So
singleton objects are obtained through a **factory method** instead.

### 11:55 — `Runtime r1 = Runtime.getRuntime();`

```java
class FirstPersonRuntime {
    public static void main(String[] args) {
        Runtime r1 = Runtime.getRuntime();
    }
}
```

Trying `new` from outside fails, verified against `javac` 26:

```java
class CannotNewRuntime {
    public static void main(String[] args) {
        Runtime r = new Runtime();
        // CE: Runtime() has private access in Runtime
    }
}
```

### 12:03–12:21 — Why `Runtime`? To talk to the JVM — and repeat calls reuse it

A `Runtime` object is how code communicates with the JVM (memory info,
`exec`, shutdown hooks, and similar). A second caller wanting the same thing
gets the **same object back** — `getRuntime()` never manufactures a new one:

```java
class SecondPersonRuntime {
    public static void main(String[] args) {
        Runtime r1 = Runtime.getRuntime();
        Runtime r2 = Runtime.getRuntime();
        // r1 == r2 : same existing Runtime object, not a second one
    }
}
```

### 13:03–13:50 — One lakh callers, still one object

```java
class RuntimeFactoryDemo {
    public static void main(String[] args) {
        Runtime r1 = Runtime.getRuntime();
        Runtime r2 = Runtime.getRuntime();
        // ...
        Runtime r1Lakh = Runtime.getRuntime();
        // one lakh callers — still only ONE Runtime object exists
    }
}
```

### 15:04–15:47 — Building your own singleton: two approaches, private constructor mandatory

Yes, you can build your own singleton (`Test` class, allowed only one
object). Both approaches he shows require a **private constructor**.

### 16:11–17:37 — Approach 1: eager, static field + factory method

```java
class Test {
    private static Test t = new Test();

    private Test() {
    }

    public static Test getTest() {
        return t; // always the same existing object
    }
}

class Client {
    public static void main(String[] args) {
        Test t1 = Test.getTest();   // not: new Test()
    }
}
```

- `private static Test t = new Test();` — the one object, created **when the
  class is loaded**, before anyone even calls `getTest()`.
- `private Test() { }` — blocks `new Test()` from any code outside the class.
  Verified:

```java
class Outside {
    public static void main(String[] args) {
        Test t1 = new Test();
        // CE: Test() has private access in Test
    }
}
```

- `getTest()` never builds anything — it just returns the field that already
  exists, no matter how many times or how many callers ask.

### 18:00–18:21 — The static field already exists before the first call

`t` is a **static** variable, so it is created **when the class is loaded** —
before any caller has invoked `getTest()` even once. The first caller's
`Test t1 = Test.getTest();` doesn't trigger creation; it just reads `t`,
which was already sitting there. A second caller, and a one-lakh-th caller,
get exactly the same treatment:

```java
class ManyCallers {
    public static void main(String[] args) {
        Test t1 = Test.getTest();
        Test t2 = Test.getTest();
        // ...
        Test t1Lakh = Test.getTest();
        // getTest() called one lakh times — always returns the same object
        // how many Test objects were ever created? exactly one
    }
}
```

At any point in time, only one `Test` object exists — that's the whole reason
`Test` qualifies as a singleton class.

### 19:16 — `Runtime` is implemented with this same approach

```java
public class Runtime {
    private static Runtime currentRuntime = new Runtime();

    private Runtime() {
    }

    public static Runtime getRuntime() {
        return currentRuntime;
    }
}
```

This is a teaching sketch of the shape, not a copy of the JDK source — the
three load-bearing pieces are the private static field created eagerly, a
private constructor, and a factory method that only ever returns the
existing field.

> The real `java.lang.Runtime` marks that field `private static final` (the
> reference itself never changes after class init) — a detail the board sketch
> skips but doesn't contradict.

### 20:50 — Three ingredients, always

1. private constructor
2. private static variable
3. public factory method

### 23:20–24:43 — The problem with approach 1, and approach 2 (lazy)

Approach 1's object is created **at class-loading time**, whether or not
anyone ever calls `getTest()` — wasted if unused. Approach 2 defers creation
to the *first* real request:

```java
class Test {
    private static Test t = null;

    private Test() {
    }

    public static Test getTest() {
        if (t == null) {      // first call: true → create
            t = new Test();
        }
        return t;             // later calls: existing object
    }
}
```

First call: `t` is `null`, so a new object is created and returned. Every
call after that: `t` is not `null`, so the `if` is skipped and the existing
object is returned directly. He calls this the "recommended" approach and
notes it's "a bit more complex."

> ❗ **Correction — this lazy form is not safe under concurrent access, and
> calling it flatly "recommended" glosses over that.** The check `if (t ==
> null)` and the assignment `t = new Test()` are two separate steps with no
> synchronization. If two threads call `getTest()` for the very first time at
> nearly the same moment, **both** can see `t == null`, and **both** can
> construct a `Test` — silently breaking the "only one object ever" guarantee
> the whole pattern exists to provide. Single-threaded code (which is most of
> what OCJP tests) never hits this, so the approach is fine as written for the
> exam and for legacy single-threaded call sites — but "recommended" for real
> multi-threaded code needs one more ingredient that this video does not
> cover. Three standard fixes, all verified against `javac` 26:
>
> ```java
> // Fix 1: synchronize the whole factory method — simplest, but every
> // call pays lock overhead forever, even after t is already set.
> class SyncTest {
>     private static SyncTest t = null;
>     private SyncTest() { }
>     public static synchronized SyncTest getTest() {
>         if (t == null) t = new SyncTest();
>         return t;
>     }
> }
> ```
> ```java
> // Fix 2: double-checked locking — lock only for the (rare) first creation;
> // `volatile` is not optional here, it stops another thread from ever
> // observing a half-constructed object through instruction reordering.
> class DclTest {
>     private static volatile DclTest t = null;
>     private DclTest() { }
>     public static DclTest getTest() {
>         if (t == null) {
>             synchronized (DclTest.class) {
>                 if (t == null) {
>                     t = new DclTest();
>                 }
>             }
>         }
>         return t;
>     }
> }
> ```
> ```java
> // Fix 3: initialization-on-demand holder idiom — lazy AND lock-free, using
> // the JVM's own guarantee that a class initializes exactly once.
> class HolderTest {
>     private HolderTest() { }
>     private static class Holder {
>         private static final HolderTest INSTANCE = new HolderTest();
>     }
>     public static HolderTest getTest() {
>         return Holder.INSTANCE;   // Holder class loads on first access
>     }
> }
> ```
>
> | Style | Lazy? | Thread-safe? | Cost per call after init |
> |---|---|---|---|
> | Approach 1 (eager, as taught) | no | yes (classloading is synchronized) | none |
> | Approach 2 (lazy, as taught) | yes | **no** | none, but unsafe |
> | Synchronized method | yes | yes | a lock, every call |
> | Double-checked locking + `volatile` | yes | yes | one `volatile` read |
> | Holder idiom | yes | yes | none |
> | `enum` (below) | effectively eager | yes | none |

### 26:42 — Both approaches valid; the difference

- **Approach 1 (eager):** object created up front, at class load.
- **Approach 2 (lazy):** object created on the first actual request.

Both guarantee "only one object at any point in time" — they differ only in
*when* that one object comes into existence.

> ⚠️ **Modern Java — the enum singleton sidesteps the whole thread-safety
> question.** *Effective Java* (Joshua Bloch) has recommended, since enums
> arrived in **Java 5**, writing a singleton as a one-element enum instead of
> a hand-rolled class:
> ```java
> enum Test {
>     INSTANCE;
>     void doWork() { /* ... */ }
> }
> // Test.INSTANCE.doWork();
> ```
> Verified this compiles and runs. The JVM guarantees enum constants are
> created exactly once, at class-init time, under a lock the class loader
> already holds — so it's eager-singleton-simple to write but free of the
> approach-2 race condition. It wasn't available for `Runtime` — a pre-Java-5
> JDK class — which is why `Runtime` still uses approach 1.
>
> It also closes two backdoors that a private constructor alone does not:
> - **Reflection.** `setAccessible(true)` on a private constructor lets any
>   caller build a second instance directly — verified against `javac` 26:
>   ```java
>   import java.lang.reflect.Constructor;
>   Constructor<Test> c = Test.class.getDeclaredConstructor();
>   c.setAccessible(true);
>   Test viaReflection = c.newInstance();
>   System.out.println(Test.getTest() == viaReflection);   // false — two objects
>   ```
>   The JVM specifically refuses this for enum constructors, so the same
>   attack on an `enum Test` throws `IllegalArgumentException: Cannot
>   reflectively create enum objects`.
> - **Serialization.** Deserializing a plain `Serializable` singleton with
>   `ObjectInputStream.readObject()` builds a *new* object unless the class
>   supplies `private Object readResolve()` to substitute the existing
>   instance back in. Enum serialization is handled specially, by constant
>   name, so no `readResolve()` is needed.

### 28:05 — Closing line for both `Test` versions

> **At any point of time, for `Test` class, we can create only one object.
> Hence `Test` class is singleton class.**

### 29:10 — Why private constructors exist: mainly this

Private constructors' main real-world use is building singleton classes —
that's the answer if asked "why would you ever make a constructor private?"

### 29:37–30:51 — Twist: not `final`, still no child class

A class marked `final` can't be subclassed — that part is old news. The
twist: a class that is **not** `final` can *still* block subclassing, by
declaring **every constructor `private`**:

```java
class P {
    private P() {
    }
}
```

`P` is not `final`, yet no class can extend it.

### 31:21 — Why: the child's constructor must call `super()`

```java
class P {
    private P() {
    }
}

class C extends P {
    // no constructor written → compiler generates:
    // C() { super(); }
}
```

Every constructor — written or compiler-generated — must invoke a superclass
constructor as its first action. `P`'s no-arg constructor exists, but it's
`private`, so it's callable only from *inside* `P` — never from a subclass.
That call is what fails.

### 32:32–33:41 — Verified against `javac`

```java
class P {
}

class C extends P {
}
// compiles fine — P's constructor is public-by-default
```

```java
class P {
    private P() {
    }
}

class C extends P {
}
// CE: P() has private access in P
```

```java
class P {
    private P() {
    }
}
// valid on its own — no subclass to fail super()
```

> Board rule: **By declaring every constructor as private, we can restrict
> child class creation** — without needing `final` at all.

> ⚠️ **Modern Java — `sealed` classes (Java 17) give a more precise version of
> this trick.** The private-constructor trick blocks *every* subclass, with
> no exceptions. A `sealed` class instead names exactly which classes may
> extend it:
> ```java
> sealed class Shape permits Circle, Square { }
> final class Circle extends Shape { }
> final class Square extends Shape { }
> // any other "class Triangle extends Shape" → CE: class is not allowed to extend sealed class
> ```
> Use the private-constructor pattern when the answer is "nobody, ever" (a
> singleton); reach for `sealed`/`permits` when the answer is "only this
> specific, known set of subclasses" — a case the pre-Java-17 language had no
> direct way to express.

### 34:52 — OOPs stretch ends here

This closes out the constructor-side application material inside OOPs.
Special note for interviews: singleton + the "not final but no child class"
trick are both common interview questions.

---

## Board recap

**Definition:** For any Java class, if we are allowed to create only one
object, such a type is called a singleton class.

**Examples:** `Runtime`, Business Delegate, Service Locator. Struts
`ActionServlet` — debated.

**Advantage:** if several requesters share the same requirement, create one
object and reuse it — memory and performance improve by default. (Story:
one-to-one with Durga Sir at ₹3 lakhs vs. 100 students × ₹3,000 in one
batch.)

**Getting `Runtime`:** never `new Runtime()` — always `Runtime.getRuntime()`,
which returns the one existing object every time.

**Own singleton needs three things:** private constructor + private static
field + public factory method.

| Approach | Field init | When the object is created | Notes |
|---|---|---|---|
| 1 — eager | `= new Test()` | at class load | how `Runtime` is built; simple, thread-safe by classloading, but always allocates |
| 2 — lazy | `= null` | on first `getTest()` call | avoids waste if unused; **not thread-safe as written** (see correction above) |

**Twist:** a class need not be `final` to block subclassing — make every
constructor `private`. A subclass's constructor must call `super()`, and a
private superclass constructor can't be reached from outside, so
`CE: P() has private access in P`.

---

## Exam and interview points

1. **Singleton = a class design constraint ("only one object, ever"), not a
   keyword.** It's enforced by construction, not by the language.
2. **`Runtime` is a real, predefined singleton** — obtained only via
   `Runtime.getRuntime()`, never `new Runtime()` (private constructor).
3. **Building your own singleton needs all three ingredients together:**
   private constructor, private static field, public static factory method.
   Missing any one breaks the guarantee.
4. **Eager (approach 1) vs. lazy (approach 2):** eager always allocates but is
   trivially safe; lazy defers allocation but, exactly as taught here, has a
   race condition under concurrent first access. Know the trade-off, not just
   the code.
5. **The modern, recommended way to write a hand-rolled singleton is a
   one-element `enum`** (Java 5+, per *Effective Java*) — thread-safe,
   serialization-safe, and reflection-proof with no extra code.
6. **A class can block subclassing without `final`** by making every
   constructor `private` — the classic interview twist. The mechanism is that
   a subclass constructor must call `super()`, and a private superclass
   constructor is unreachable from outside the class.
7. **`sealed` classes (Java 17)** are the modern tool when the goal is "let
   *only these specific classes* extend me," rather than "let nothing extend
   me" — a distinction the pre-17 language couldn't express directly.
8. **Business Delegate and Service Locator are legacy J2EE patterns** built
   around expensive remote EJB calls; dependency injection replaced the need
   for both in modern Jakarta EE / Spring code, though they remain standard
   interview vocabulary.

---

**Next:** Video 068 — OOPs Concepts compilation
