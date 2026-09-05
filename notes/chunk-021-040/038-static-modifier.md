# Video 038 — static modifier

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-9||  static modifier

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 38 of 203 |
| Series | Declarations and Access Modifiers · Part 9 |
| Topic | static modifier |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 18m 34s |
| Video ID | ErbJRUtjlB0 |
| Watch | https://www.youtube.com/watch?v=ErbJRUtjlB0 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Final variables are done; the next modifier is **static**. Sir promises the
purpose of static, its loopholes, and a first look at `synchronized` before
Multi Threading covers it properly.

1. Where `static` applies: variables and methods; not top-level classes; inner classes may be static nested classes.
2. Instance vs static variables: separate copy per object vs one class-level copy shared by all objects (classic `888` / `20` exam output).
3. Access rules: instance members not accessible directly from static area; static members accessible from both areas.
4. Same-class declaration combinations (four declarations MCQ) plus "same name" traps for variables and methods.
5. Three cases for static methods: overloading (including `main`), inheritance (including `main`), method hiding (not overriding).
6. Thumb rule: when to declare instance vs static method (Student example).
7. `abstract` + `static` is illegal for methods.
8. Brief intro to `synchronized` (methods/blocks only): race condition, advantage, disadvantage; `abstract` + `synchronized` illegal. Full programs later in Multi Threading.

## 00:39 — Where can we apply `static`?

- We can declare a **variable** as static.
- We can declare a **method** as static.
- Can we declare a **class** as static? By default **no** — a top-level class cannot be static.
- Special case: an **inner class** can be declared static. Such inner classes are called **static nested classes** (full discussion in Inner Classes later).

Board conclusion:

> *`static` is a modifier applicable for methods and variables, but not for
> (top-level) classes. We can't declare a top-level class with `static`, but
> we can declare an inner class as static — such inner classes are called
> static nested classes.*

```java
// CE: modifier static not allowed here
static class Test {
}
```

```java
class Outer {
    // valid: static nested class (inner-class topic later)
    static class Nested {
    }
}
```

## 03:45 — Recap: instance variable vs static variable

| Kind | Copies |
|---|---|
| Instance variable | For every object a separate copy is created |
| Static variable | For the total class only one copy is created at class level and shared by every object of that class |

This difference drives the classic exam question that follows.

## 05:33 — Exam example: static `x`, instance `y`, change via `t1`, print via `t2`

```java
class Test {
    static int x = 10;
    int y = 20;

    public static void main(String[] args) {
        Test t1 = new Test();
        t1.x = 888;
        t1.y = 999;

        Test t2 = new Test();
        System.out.println(t2.x + "---" + t2.y);
        // prints 888---20
    }
}
```

Sir lists these as the MCQ options: `10---20`, `888---999`, `888---20`,
`10---999`, or compile-time error. **Correct output: `888---20`.**

Step-by-step (as on board):

1. Static `x = 10` is created first (at class loading — one copy).
2. `Test t1 = new Test()` → instance `y = 20` created for `t1`.
3. `t1.x = 888` — accessing static via object reference is allowed; changes the **only** static copy → `x` is now `888`.
4. `t1.y = 999` — changes only `t1`'s instance copy.
5. `Test t2 = new Test()` → **new** instance copy `y = 20` for `t2`. Static `x` is still the shared `888`.
6. `t2.x` → `888`; `t2.y` → `20`.

Rules to remember:

- One copy of a static variable → change via any reference is visible to all objects.
- Separate copy of an instance variable → change via one reference does **not** affect other objects.

## 12:14 — Instance area vs static area: what can we access?

```java
class Test {
    int x = 10;              // instance variable
    static int y = 20;       // static variable

    public void m1() {       // instance method → instance area
        System.out.println(x); // valid — instance from instance
        System.out.println(y); // valid — static from instance
    }

    public static void m2() { // static method → static area
        // System.out.println(x); // CE: non-static variable x cannot be referenced from a static context
        System.out.println(y);    // valid — static from static
    }
}
```

- Instance variable / instance member is always related to an **object**.
- Static area is **not** related to any particular object.
- Therefore: from static area we **cannot** access instance members **directly** (variable or method).
- Static variable exists from class loading → can be accessed from **anywhere** (instance area or static area) directly.

Conclusions on the board:

1. We can't access instance members directly from static area, but we can access them from instance area directly.
2. We can access static members from both instance and static areas directly.

## 15:49 — Exam MCQ: four declarations — which pairs can coexist?

Four declarations, same class (numbered as on board):

```java
// (1)
int x = 10;

// (2)
static int x = 10;

// (3)
public void m1() {
    System.out.println(x);
}

// (4)
public static void m1() {
    System.out.println(x);
}
```

| Option | Pair | Verdict |
|---|---|---|
| A | 1 and 3 | Valid — instance variable + instance method using x |
| B | 1 and 4 | Invalid — instance x from static m1 |
| C | 2 and 3 | Valid — static x from instance method |
| D | 2 and 4 | Valid — static x from static method |

```java
// Option A — valid (1 + 3)
class Test {
    int x = 10;

    public void m1() {
        System.out.println(x);
    }
}
```

```java
// Option B — invalid (1 + 4)
class Test {
    int x = 10;

    public static void m1() {
        System.out.println(x);
        // CE: non-static variable x cannot be referenced from a static context
    }
}
```

```java
// Option C — valid (2 + 3)
class Test {
    static int x = 10;

    public void m1() {
        System.out.println(x);
    }
}
```

```java
// Option D — valid (2 + 4)
class Test {
    static int x = 10;

    public static void m1() {
        System.out.println(x);
    }
}
```

Exact CE wording Sir stresses for option B: `non-static variable x cannot be referenced from a static context`.

## 21:36 — Extra trap: can we take (1) and (2) together?

Same simple name for an instance variable and a static variable in one class — **not allowed**.

```java
class Test {
    int x = 10;
    static int x = 10;
    // CE: variable x is already defined in Test
}
```

People often think "one instance, one static, different kinds → OK." Wrong —
`x` still means one class member twice: `variable x is already defined in Test`.

```java
class Test {
    static int x = 10;
    int x = 20;
    // CE: variable x is already defined in Test
}
```

(Contrast: a local variable with the same name as a static/instance field is a
different story — shadowing — allowed; here both are **class members**.)

## 23:16 — Extra trap: can we take (3) and (4) together?

An instance method `m1()` and a static method `m1()` with the **same signature** — **not allowed**.

```java
class Test {
    public void m1() {
        System.out.println("instance");
    }

    public static void m1() {
        System.out.println("static");
        // CE: m1() is already defined in Test
    }
}
```

Why? Method **signature** = name + argument types. Return type and modifiers
(`static`, `public`, …) are **not** part of the signature. Both are `m1` with
no arguments → duplicate: `m1() is already defined in Test`.

## 25:43 — Three important cases related to static methods

Overloading, inheritance, and "overriding-looking" behavior for static methods (including `main`).

## 25:54 — Case 1: Overloading is applicable for static methods (including `main`)

```java
class Test {
    public static void main(String[] args) {
        System.out.println("String array");
        main(new int[] {10, 20, 30}); // normal method call
    }

    public static void main(int[] args) {
        System.out.println("int array");
    }
}
// prints:
// String array
// int array
```

- Same name, different argument types → **overloading**, and overloading applies to static methods, **including** `main`.
- The JVM's launcher always calls `public static void main(String[] args)`.
- The `int[]` version is a **normal** overloaded method — it only runs if you call it yourself.

Without the self-call, `java Test` runs only the `String[]` version:

```java
class Test {
    public static void main(String[] args) {
        System.out.println("String array");
    }

    public static void main(int[] args) {
        System.out.println("int array");
    }
}
// java Test → prints only String array
```

Board Case 1:

> *Overloading concept applicable for static methods including main method.
> But JVM can always call the String[]-argument main method only. Other
> overloaded methods we have to call just like a normal method call.*

> ⚠️ **Modern Java — `main` is no longer the only entry point.**
> Since **Java 25** (JEP 512, finalized after four preview rounds starting at
> Java 21), a source file can skip the class declaration entirely and use an
> **instance** `main` with no `static`, no `public`, no `String[]`:
> ```java
> void main() {
>     System.out.println("instance main, no class needed");
> }
> ```
> `java Main.java` runs this directly. It compiles and runs unmodified on the
> JDK used for this note (26), and `javac --release 21` rejects it with
> *"implicitly declared classes are not supported in -source 21 (use -source
> 25 or higher...)"* — confirming the feature needs source level 25+. This is
> aimed at beginners and scripts; every rule in this lecture about overloading,
> inheritance, and hiding of `main` still applies in full to ordinary classes
> that declare `public static void main(String[] args)`, which remains the
> form real applications use.

## 31:07 — Case 2: Inheritance is applicable for static methods (including `main`)

```java
// file: P.java
class P {
    public static void main(String[] args) {
        System.out.println("Parent main");
    }
}

class C extends P {
    // no main method in child
}
```

```java
javac P.java
```

Two `.class` files come out — `P.class`, `C.class` — one per class.

```java
java P
```

→ prints `Parent main` (parent has `main`).

```java
java C
```

→ **also** prints `Parent main`. The child has no `main`, so the parent's
static `main` is available to it through inheritance — not
`NoSuchMethodError: main`.

Board Case 2:

> *Inheritance concept applicable for static methods including main method.
> Hence while executing child class, if child doesn't contain main method,
> then parent class main method will be executed.*

## 37:02 — Case 3: Both parent and child have `main` — method hiding, not overriding

```java
class P {
    public static void main(String[] args) {
        System.out.println("Parent main");
    }
}

class C extends P {
    public static void main(String[] args) {
        System.out.println("Child main");
    }
}
// java P → prints Parent main
// java C → prints Child main
```

Same name + same argument types looks like **overriding**, but for static
methods it is **method hiding**, **not** overriding.

Board Case 3:

> *It seems overriding concept applicable for static methods, but it is not
> overriding — it is method hiding.*

The exact difference between method hiding and overriding ("all rules are the
same with a small difference") is deferred to OOPs later — for now, remember
the terminology: static methods hide, they never override.

## 42:17 — Summary for static methods

- **Overloading** — applicable
- **Inheritance** — applicable
- **Overriding** — **not** applicable
- Instead of overriding → **method hiding** is applicable

## 44:02 — When instance variable vs static variable?

- Need a **separate copy for every object** → instance variable.
- Need **one common copy at class level** for all objects → static variable.

## 44:20 — When instance method vs static method? (thumb rule)

1. If the method uses **at least one instance variable** → it talks about a **particular object** → declare it as an **instance method**.
2. If the method uses **no instance variable** (whether or not it uses static variables) → it is not related to any particular object → declare it as a **static method**.

The whole criterion: are you using any instance variable or not?

## 50:21 — Student example: classify each method

```java
class Student {
    String name;
    int rollNumber;
    int marks;
    static String collegeName = "DurgaSoft"; // same college for all students

    public String getStudentInfo() {
        return name + "---" + marks;
        // uses instance data → instance method
    }

    public static String getCollegeInfo() {
        return collegeName;
        // uses only static data → static method
    }

    public static int getAverage(int x, int y) {
        return (x + y) / 2;
        // utility: only parameters, no instance vars → static method
    }

    public String getCompleteInfo() {
        return name + "---" + rollNumber + "---" + marks + "---" + collegeName;
        // uses instance vars (plus a static one) → still instance method
    }

    public static void main(String[] args) {
        Student s = new Student();
        s.name = "Ravi";
        s.rollNumber = 101;
        s.marks = 90;
        System.out.println(s.getStudentInfo());       // Ravi---90
        System.out.println(Student.getCollegeInfo());  // DurgaSoft
        System.out.println(Student.getAverage(80, 90)); // 85
        System.out.println(s.getCompleteInfo());       // Ravi---101---90---DurgaSoft
    }
}
```

| Method | Uses instance var? | Declare as |
|---|---|---|
| getStudentInfo | yes (name, marks) | instance |
| getCollegeInfo | no (only collegeName, static) | static |
| getAverage | no (only parameters — utility) | static |
| getCompleteInfo | yes (name, rollNumber, marks) | instance |

Even though `getCompleteInfo` also reads `collegeName` (static), **at least
one** instance variable is enough to force it to be an instance method.

## 58:31 — Static methods must have implementation; `abstract` + `static` illegal

- A static method → **must** have an implementation (body).
- An abstract method → **must not** have an implementation.
- Contradiction → **`abstract static` is an illegal combination** for methods.

```java
abstract class Test {
    public abstract static void m1();
    // CE: illegal combination of modifiers: abstract and static
}
```

```java
abstract class Test {
    // static needs a body
    public static void m1() {
        System.out.println("ok");
    }

    // abstract must not have a body
    public abstract void m2();
}
```

Board:

> *For static methods implementation should be available, whereas for
> abstract methods implementation should not be available. Hence abstract
> static combination is illegal for methods.*

## 1:00:31 — Next modifier teaser: `synchronized`

Full treatment comes later, in **Multi Threading**. Here: just the basic idea.

## 1:01:08 — Where does `synchronized` apply?

| Target | synchronized allowed? |
|---|---|
| Classes | No |
| Methods | Yes |
| Variables | No |
| Blocks | Yes (synchronized block) |

```java
// CE: modifier synchronized not allowed here
synchronized class Test {
}
```

```java
class Test {
    // CE: modifier synchronized not allowed here
    // synchronized int x;

    public synchronized void m1() {
        // valid: synchronized method
    }

    public void m2() {
        synchronized (this) {
            // valid: synchronized block
        }
    }
}
```

Board:

> *`synchronized` is a modifier applicable only for methods and blocks, but
> not for classes and variables.*

## 1:02:30 — Biryani-plate story → race condition (analogy)

Sir's story: someone drops a biryani plate on the roadside. One dog finds it
and eats happily; a second dog arrives and they fight over it; a third joins
in. A fourth, "smarter" dog starts eating from the far side while the others
are still fighting over the near side — everyone pulls at once, the plate
tears, and the biryani ends up wasted on the ground for nobody.

> *If multiple dogs are operating simultaneously on the same biryani plate,
> then we will get **biryani inconsistency problem**.*

| Analogy | Java |
|---|---|
| Biryani plate | Java object |
| Each dog | A thread |
| Fighting / messed-up plate | Data inconsistency |

> *If multiple threads try to operate simultaneously on the same Java object,
> there may be a chance of **data inconsistency problems**. This is called a
> **race condition**.*

To overcome it → use the **`synchronized`** keyword.

## 1:09:08 — Advantage of `synchronized`

Declare `eat` (the operation) as synchronized → at a time **only one**
dog/thread can perform that operation on the given object; the rest wait
until the first one finishes. One-by-one → no inconsistency.

```java
class BiryaniPlate {
    public synchronized void eat() {
        // at a time only one thread executes this on the given object
        System.out.println(Thread.currentThread().getName() + " eating");
    }
}
```

Board advantage:

> *If a method or block is declared as synchronized, then at a time only one
> thread is allowed to execute that method or block on the given object, so
> that data inconsistency problem will be resolved.*

## 1:10:38 — Disadvantage of `synchronized`

The second thread waits for the first to finish; the third waits for the
first two; and so on — this increases the **waiting time** of threads, which
becomes a **performance problem**.

Board:

> *Main disadvantage of synchronized keyword: it increases waiting time of
> threads. Hence if there is no specific requirement, it is **not
> recommended** to use synchronized keyword.*

> ⚠️ **Modern Java — the waiting-time cost got sharper, then got a fix.**
> Java 21 added **virtual threads** (lightweight threads the JVM multiplexes
> onto a small pool of OS "carrier" threads) as the mainstream answer to
> "synchronized code doesn't scale." But through JDK 21–23, a virtual thread
> blocked *inside* a `synchronized` method or block got **pinned** to its
> carrier thread instead of releasing it — turning Sir's "waiting time"
> disadvantage into "one stuck platform thread per waiting virtual thread,"
> which defeats the whole point of using thousands of virtual threads.
> **JEP 491 (JDK 24)** removed that pinning for the common case, so
> `synchronized` and virtual threads now compose properly. The underlying
> lesson is unchanged: `synchronized` still serializes access and still costs
> waiting time. For finer control — timeouts, fairness, non-blocking
> `tryLock()`, or an interruptible wait — reach for
> `java.util.concurrent.locks.ReentrantLock` (available since Java 5) instead
> of the raw `synchronized` keyword.

## 1:12:09 — Synchronized summary points

1. Multiple threads operating simultaneously on the same Java object → chance of data inconsistency → **race condition**.
2. Overcome by using **`synchronized`**.
3. A synchronized method/block → at a time only **one** thread executes it on the given object → inconsistency resolved.
4. Disadvantage: it increases waiting time of threads.
5. No specific requirement → **not recommended** to use `synchronized`.

## 1:16:03 — `abstract` + `synchronized` is also illegal

`synchronized` talks about **implementation** (only one thread may execute it
at a time); `abstract` has **no** implementation. Contradiction.

```java
abstract class Test {
    public abstract synchronized void m1();
    // CE: illegal combination of modifiers: abstract and synchronized
}
```

```java
class Test {
    // synchronized method must have a body
    public synchronized void m1() {
        System.out.println("one thread at a time");
    }
}
```

Board:

> *Synchronized method should compulsorily contain implementation, whereas
> abstract method doesn't contain any implementation. Hence abstract
> synchronized is illegal combination of modifiers for methods.*

## 1:18:18 — Close

That's the basic idea of the **synchronized** modifier — detailed programs
come in Multi Threading. The static-modifier portion of Declarations and
Access Modifiers Part-9 is complete; `synchronized` was introduced only for
awareness.

## Exam and interview points

1. `static` applies to variables and methods; never to a top-level class; an
   inner class can be static (a static nested class).
2. Static = one class-level copy, instance = one copy per object → the
   classic `888---20` output, verified above by compiling `Test`.
3. No direct access to instance members from a static context — the compiler
   error is exactly `non-static variable x cannot be referenced from a static
   context`.
4. Reusing a name for both an instance and a static member (a field, or a
   method with the same signature) is always `... is already defined in
   <Class>` — "different kind" does not save you.
5. Static methods support **overloading** and **inheritance**, including for
   `main`; they do **not** support overriding — same signature in a subclass
   is **method hiding**.
6. Thumb rule for instance vs static method: uses even one instance variable
   → instance method; otherwise → static method.
7. `abstract static` and `abstract synchronized` are both illegal
   combinations, for the same underlying reason: abstract forbids a body,
   static and synchronized both require one.
8. `synchronized` applies only to methods and blocks, never to classes or
   variables; it fixes race conditions at the cost of thread waiting time —
   don't reach for it without a specific need.
9. Since Java 25, `void main()` without `static`/`public`/`String[]` can be
   the program entry point (JEP 512) — an on-ramp for beginners, not a
   replacement for the `main` overloading/inheritance/hiding rules taught
   here, which still govern any class that declares `main` explicitly.
10. Since JDK 24 (JEP 491), a virtual thread blocked inside a `synchronized`
    block no longer pins its carrier platform thread — worth knowing if
    you're asked why `synchronized` was historically discouraged with
    virtual threads.

**Next:** Video 039 — native, static, transient
