# Video 078 — Top-10 Exceptions in Java

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-8 || Top-10 Exceptions in java

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 78 of 203 |
| Series | Exception Handling · Part 8 |
| Topic | Top-10 Exceptions in java |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 52m 53s |
| Video ID | b_o6NeSn8pU |
| Watch | https://www.youtube.com/watch?v=b_o6NeSn8pU |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## Session arc

After customized (user-defined) exceptions (prior videos), Sir introduces a
**second way to classify exceptions** — by **who raises them** (JVM vs
programmatic). He then begins the **top 10 commonly occurring exceptions**,
covering **six fully** in this session and **starting the seventh**
(`IllegalArgumentException`) at the very end. Items 7–10 are completed in
Video 079.

---

### 00:06 — Transition: customized exceptions → top 10

Up to this point the series covered how to define customized (user-defined)
exceptions and how to use them — an important OCJP/SCJP area.

The next topic: **top 10 exceptions** — ten important exception types, in
which case each is raised, with examples. Before listing them, Sir revisits
classification, but with a new division beyond checked vs unchecked.

### 00:51 — New classification: JVM exceptions vs programmatic exceptions

You already know one division from earlier lectures:

| Division (already covered) | Types |
|---|---|
| Checked exceptions | Compiler forces handling |
| Unchecked exceptions | No compile-time handling requirement |

**New division — based on who is raising the exception:**

| Category | Who raises | Meaning |
|---|---|---|
| JVM exceptions | JVM (automatically) | A runtime event occurs and the JVM raises an exception without any `throw new …` in your source |
| Programmatic exceptions | Programmer or API developer (explicitly) | Raised with `throw new …` to signal that something went wrong |

### 01:33 — Who can raise exceptions in Java?

Exceptions can be raised by **three** actors:

1. **JVM** — e.g. division by zero, calling a method on `null`.
2. **Programmer** — e.g. `throw new TooYoungException()`, `throw new InsufficientFundsException()` (the customized-exception examples).
3. **API developer** — the library/JDK author who wrote classes like `String`, `Thread`.

The **end user** of an application does not raise exceptions; they only use
the upper-layer service. The **compiler** checks syntax and reports
compile-time errors, but it is not counted as a fourth "raiser" of runtime
exceptions in this lecture's framework.

### 02:09 — JVM exception: division by zero (no `throw new` in your code)

Whenever a particular event occurs, the JVM automatically raises an
exception. You will never see `throw new ArithmeticException` in application
code for this — the JVM is responsible.

```java
class JvmDivisionByZero {
    public static void main(String[] args) {
        System.out.println(10 / 0);
    }
}
// runtime: ArithmeticException: / by zero
// Raised automatically by JVM — a JVM exception
```

Another JVM example mentioned: calling any method on `null` →
`NullPointerException` (covered in detail below).

### 03:04 — Programmatic exceptions: programmer and API developer

Programmatic exceptions are explicitly raised — either by the **programmer**
or by an **API developer** — to indicate that something went wrong.

```java
// Programmer raises — programmatic exception (from prior customized-exception lectures)
class TooYoung extends RuntimeException {
    TooYoung(String msg) { super(msg); }
}

class ProgrammerThrows {
    public static void main(String[] args) {
        int age = 15;
        if (age < 18) {
            throw new TooYoung("not eligible to vote");
        }
    }
}
// runtime: TooYoung — raised explicitly by programmer
```

| Raiser | Example context |
|---|---|
| Programmer | In your `Test` class: `throw new TooYoungException()` |
| API developer | Inside JDK classes like `Thread`: `throw new IllegalArgumentException()` |

All customized exceptions are programmatic exceptions — the programmer
raises them. Anything explicitly raised by either the programmer or the API
developer falls under this category.

### 05:24 — API developer example: `Thread.setPriority` → `IllegalArgumentException`

Students asked for at least one API developer example for clarity.

**Thread priority range:** every thread in Java has a priority; the valid
range is **1 to 10** (not 0–10).

```java
class ThreadPriorityDemo {
    public static void main(String[] args) {
        Thread t = new Thread();
        t.setPriority(5);  // valid — inside 1..10
    }
}
```

```java
class ThreadPriorityInvalid {
    public static void main(String[] args) {
        Thread t = new Thread();
        t.setPriority(15); // valid range is 1 to 10
    }
}
// runtime: IllegalArgumentException
// Raised by API developer logic inside Thread class — programmatic exception
```

**Why `IllegalArgumentException`?** Sir opens the `Thread` class source
(`java.lang.Thread` in the JDK `src`) and shows `setPriority(int newPriority)`:

```java
class ThreadPriorityTooLow {
    public static void main(String[] args) {
        Thread t = new Thread();
        t.setPriority(0); // less than MIN_PRIORITY (1)
    }
}
// runtime: IllegalArgumentException
```

```java
// Simplified from java.lang.Thread — JDK source (API developer code)
public final void setPriority(int newPriority) {
    if (newPriority > MAX_PRIORITY || newPriority < MIN_PRIORITY) {
        throw new IllegalArgumentException();
    }
    // ... actual priority update ...
}
```

- **Who wrote this `throw`?** → the API developer (Sun/Oracle JDK team), not Sir, not you: *"It is not my own creation; already defined by Thread.java."*
- **Therefore:** `IllegalArgumentException` here is a **programmatic** exception, not a JVM exception.
- If priority is less than 1 or greater than 10, `IllegalArgumentException` is thrown immediately.

> ⚠️ **Modern Java — thread priority is now cosmetic for virtual threads.**
> `Thread.setPriority` still validates the 1–10 range and still throws
> `IllegalArgumentException` outside it — that part of this lecture is
> unchanged in JDK 26. But since **virtual threads (Java 21, JEP 444)**, a
> virtual thread's priority is fixed at `NORM_PRIORITY` and `setPriority`
> silently does nothing to the value used for scheduling:
>
> ```java
> Thread t = Thread.ofVirtual().unstarted(() -> {});
> t.setPriority(15);   // still throws IllegalArgumentException (out of range)
> t.setPriority(1);    // no exception, but getPriority() still reports 5
> System.out.println(t.getPriority()); // 5, unchanged
> ```
>
> Verified on JDK 26. Virtual threads are scheduled cooperatively over a small
> carrier-thread pool, so a per-thread OS priority hint has nowhere to go.
> This does not change the OCJP answer — the exam only cares about the range
> check on platform threads — but it is worth knowing before you rely on
> thread priority for anything in new code.

### 10:12 — Summary: three raisers, two categories

| Who raises | Category |
|---|---|
| JVM | JVM exception |
| Programmer or API developer | Programmatic exception |

### 11:06 — Board dictation: JVM vs programmatic (formal definitions)

**Division:** all exceptions are divided into two categories based on who is
raising them:

1. **JVM exceptions**
2. **Programmatic exceptions**

**JVM exceptions — definition:**

> *The exceptions which are raised automatically by JVM whenever a
> particular event occurs.*

Examples on the board: `ArithmeticException`, `NullPointerException`, etc.

**Programmatic exceptions — definition:**

> *The exceptions which are raised explicitly either by programmer or by API
> developer to indicate that something goes wrong.*

Examples: customized exceptions (`TooYoungException`, etc.),
`IllegalArgumentException` from JDK APIs, etc.

### 16:03 — Introducing the top 10 commonly occurring exceptions

For each of the ten, Sir asks:

- Checked or unchecked?
- JVM exception or programmatic exception?
- In which particular case is it raised — with an example?

### 16:29 — #1: `ArrayIndexOutOfBoundsException`

**Spelling note:** one word — `ArrayIndexOutOfBoundsException` (ASR often
splits "Array" and "Index").

**Hierarchy:**

- Child class of `IndexOutOfBoundsException`
- Which is a child class of `RuntimeException`
- Hence: **unchecked** (everything under `RuntimeException` is unchecked)

**When raised:** whenever we try to access an array element with an
out-of-range index (too high or negative).

```java
class ArrayIndexValid {
    public static void main(String[] args) {
        int[] x = new int[4];
        System.out.println(x[0]); // size 4 → valid indexes 0..3
    }
}
// prints 0
```

```java
class ArrayIndexTooHigh {
    public static void main(String[] args) {
        int[] x = new int[4];
        System.out.println(x[10]); // 10 is out of range
    }
}
// runtime: ArrayIndexOutOfBoundsException
```

```java
class ArrayIndexNegative {
    public static void main(String[] args) {
        int[] x = new int[4];
        System.out.println(x[-10]); // negative index — also out of range
    }
}
// runtime: ArrayIndexOutOfBoundsException
```

**Valid index range** for `new int[4]`: **0 to 3** only. Both **+10** and
**-10** are invalid → same exception type.

**Board summary for #1:**

| Point | Detail |
|---|---|
| Hierarchy | Child of `IndexOutOfBoundsException` → `RuntimeException` → unchecked |
| Raised by | JVM automatically (not programmatic) |
| When | Accessing an array element with an out-of-range index |

> ❗ **Correction — the board's "all three on one class" example needs a caveat.**
> Sir's board version combines all three accesses (`x[0]`, `x[10]`, `x[-10]`)
> in one `main`, but the first out-of-bounds access throws and ends the
> program before the next line ever runs — so only the *first* failing
> line's exception is ever observed in one execution, not all three. Run
> each case separately if you want to see all three outcomes, as the three
> individual classes above do. (`x[10]` also now reports
> `Index 10 out of bounds for length 4` rather than a bare `10` — see the
> modern-messages note below.)

```java
class ArrayIndexOutOfBoundsBoard {
    public static void main(String[] args) {
        int[] x = new int[4];
        System.out.println(x[0]);   // prints 0 — valid
        System.out.println(x[10]);  // ArrayIndexOutOfBoundsException — execution stops here
        System.out.println(x[-10]); // never reached
    }
}
```

> ⚠️ **Modern Java — out-of-bounds messages got a lot more useful.**
> On Java 6/7, `x[10]` on a length-4 array printed only
> `ArrayIndexOutOfBoundsException: 10`. Current JDKs print the index *and*
> the length:
>
> ```text
> Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException:
>     Index 10 out of bounds for length 4
> ```
>
> Verified on JDK 26. This is a message-text improvement only (the type and
> hierarchy Sir taught are unchanged) — but it means you no longer have to go
> find the array declaration to know how big it actually was.

### 22:22 — #2: `NullPointerException`

**Hierarchy:** child class of `RuntimeException` → **unchecked**.

**When raised:** automatically by the JVM whenever we try to perform any
operation on `null` — calling a method, accessing a property, etc.

```java
class NullPointerMethodCall {
    public static void main(String[] args) {
        String s = null;
        System.out.println(s.length()); // method call on null
    }
}
// runtime: NullPointerException
```

```java
class NullPointerPropertyAccess {
    public static void main(String[] args) {
        int[] arr = null;
        System.out.println(arr.length); // property (field) access on null
    }
}
// runtime: NullPointerException
```

**Board summary for #2:**

| Point | Detail |
|---|---|
| Hierarchy | Child of `RuntimeException` → unchecked |
| Raised by | JVM automatically |
| When | Any operation on `null` (method call, property access, etc.) |

```java
// Board dictation example
class NullPointerBoard {
    public static void main(String[] args) {
        String s = null;
        System.out.println(s.length()); // NullPointerException
    }
}
```

> ⚠️ **Modern Java — "helpful NullPointerExceptions" (JEP 358).**
> On Java 6/7 the exception above carried no message at all — just
> `NullPointerException` and a stack trace pointing at the line. Since
> **Java 14** (opt-in via `-XX:+ShowCodeDetailsInExceptionMessages`) and **on
> by default since Java 15**, the JVM names the exact null expression:
>
> ```text
> Exception in thread "main" java.lang.NullPointerException:
>     Cannot invoke "String.length()" because "s" is null
> ```
>
> Verified on JDK 26 (a local variable shows as `<local1>` when debug symbols
> aren't compiled in — use `javac -g` to get the real name `s`). This is the
> single most useful debugging change since this lecture was recorded: a
> chained call like `a.getB().getC().getName()` used to be a guessing game
> about which link in the chain was null; now the message says so directly.

### 25:11 — #3: `ClassCastException`

**Hierarchy:** child class of `RuntimeException` → **unchecked**.

**Concept — type casting rules (review):**

- **Child → parent (upcast):** always valid. Every child object *is-a*
  parent type.
- **Parent → child (downcast):** valid only if the internal object is
  actually of the child type.

**Valid upcast — child reference, child object → parent type:**

```java
class ClassCastValidUpcast {
    public static void main(String[] args) {
        String s = new String("Durga");
        Object o = s; // child object → parent reference — VALID
    }
}
```

**Invalid downcast — parent object → child type:**

```java
class ClassCastInvalidDowncast {
    public static void main(String[] args) {
        Object o = new Object();
        String s = (String) o; // internal object is Object, not String
    }
}
// runtime: ClassCastException
// JVM automatically raises — JVM exception
```

**Valid downcast — parent reference, but internal object is child:**

```java
class ClassCastValidDowncast {
    public static void main(String[] args) {
        Object o = new String("Durga"); // parent ref, child object inside
        String s = (String) o;          // VALID — internal object is String
    }
}
```

**Key distinction Sir emphasizes:**

| Scenario | Internal object | Downcast to child |
|---|---|---|
| `Object o = new Object(); (String) o` | Parent (`Object`) | Invalid → `ClassCastException` |
| `Object o = new String("Durga"); (String) o` | Child (`String`) | Valid |

You will not see `throw new ClassCastException` in application code — the
JVM performs the runtime type check and raises it.

**Board summary for #3:**

| Point | Detail |
|---|---|
| Hierarchy | Child of `RuntimeException` → unchecked |
| Raised by | JVM automatically |
| When | Typecasting a parent object to a child type when the internal object is not of that child type |

```java
// Board — valid vs invalid; execution stops at the first ClassCastException
class ClassCastBoard {
    public static void main(String[] args) {
        // VALID: child → parent
        String s1 = new String("Durga");
        Object o1 = s1;

        // INVALID: parent object → child type
        Object o2 = new Object();
        String s2 = (String) o2; // ClassCastException — execution stops here

        // never reached, but valid on its own: parent ref, child object inside
        Object o3 = new String("Durga");
        String s3 = (String) o3;
    }
}
```

> ⚠️ **Modern Java — the message now names the modules involved.**
> Since the module system landed in **Java 9**, a failed cast reports where
> each class lives:
>
> ```text
> Exception in thread "main" java.lang.ClassCastException:
>     class java.lang.Object cannot be cast to class java.lang.String
>     (java.lang.Object and java.lang.String are in module java.base of loader 'bootstrap')
> ```
>
> Verified on JDK 26. Handy once your own classes live across different
> modules — you can immediately see whether the mismatch is a genuine bug or
> two class loaders holding two different copies of "the same" class.

### 32:25 — #4: `StackOverflowError`

Note the word *Error*, not *Exception*.

**Hierarchy:** child class of `Error` (not `Exception`) → **unchecked**
(errors and runtime exceptions are both unchecked).

**When raised:** automatically by the JVM when performing recursive method
calls without a proper base case — the runtime stack overflows.

**Runtime stack recap** (from early exception-handling lectures):

- For every thread, the JVM creates one runtime stack.
- In `main`, only one thread (the main thread) → one runtime stack.
- Each method invocation pushes a frame onto that thread's stack.

```java
class StackOverflowRecursive {
    public static void m1() {
        m2();
    }

    public static void m2() {
        m1();
    }

    public static void main(String[] args) {
        m1();
    }
}
// runtime: StackOverflowError
// m1 → m2 → m1 → m2 → … until the stack overflows
```

**Stack growth (conceptual):**

```text
main thread stack:
  main()
    m1()
      m2()
        m1()
          m2()
            m1()
              ... (continues until overflow)
```

At some point the stack overflows → `StackOverflowError` (Sir notes the name
literally contains "overflow").

**Board summary for #4:**

| Point | Detail |
|---|---|
| Hierarchy | Child of `Error` → unchecked |
| Raised by | JVM automatically |
| When | Recursive method call (infinite / unbounded recursion) |

### 38:27 — #5: `NoClassDefFoundError`

**Hierarchy:** child class of `Error` → **unchecked**.

**When raised:** automatically by the JVM when it is unable to find a
required `.class` file at runtime.

**Sir's scenario:** compile `Test.java`, then delete `Test.class` before
running `java Test` — the claim was that this prints
`NoClassDefFoundError: Test`.

```java
// Compile-time: this class exists and compiles fine
class Test {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

> ❗ **Correction — deleting the *main* class's own `.class` file does not
> produce `NoClassDefFoundError` on any JDK tested here.**
> Running `java Test` after removing `Test.class` gives:
>
> ```text
> Error: Could not find or load main class Test
> Caused by: java.lang.ClassNotFoundException: Test
> ```
>
> Verified on JDK 26. That message comes from the **launcher** (`bin/java`)
> failing to locate the class named on the command line — it never gets far
> enough into the JVM to raise a linkage error. `NoClassDefFoundError` is
> what you get when a class **already loaded and running** references
> *another* class whose `.class` file has since gone missing — that failure
> happens during linking, inside the JVM, not at launcher startup. The fix is
> a two-class demo:
>
> ```java
> // B.java — compiled, then its .class file is deleted before running A
> class B {
>     static void hello() { System.out.println("hi from B"); }
> }
> ```
>
> ```java
> // A.java — this is the class you actually run
> class A {
>     public static void main(String[] args) {
>         B.hello(); // JVM needs B.class here, at link time
>     }
> }
> ```
>
> ```text
> $ javac A.java B.java
> $ rm B.class
> $ java A
> Exception in thread "main" java.lang.NoClassDefFoundError: B
>     at A.main(A.java:3)
> Caused by: java.lang.ClassNotFoundException: B
> ```
>
> Verified on JDK 26. The concept Sir is teaching — "unchecked `Error`, JVM
> raises it automatically when a needed `.class` file can't be found" — is
> exactly right and exam-correct; only the specific command that reproduces
> it needed fixing.

**Board summary for #5:**

| Point | Detail |
|---|---|
| Hierarchy | Child of `Error` → unchecked |
| Raised by | JVM automatically |
| When | JVM unable to find a required `.class` file while linking a class it needs |

**Distinction to remember:** this is not `ClassNotFoundException` (checked,
typically from explicit reflective class loading, e.g. `Class.forName`).
`NoClassDefFoundError` is the unchecked `Error` the JVM itself raises when
linking a class it has already committed to using.

### 43:11 — #6: `ExceptionInInitializerError`

**Hierarchy:** child class of `Error` → **unchecked**.

Sir notes many students see this for the first time — a compulsory
OCJP/SCJP topic.

**When raised:** automatically by the JVM if any exception occurs while
executing:

- static variable assignments, or
- static blocks

during class initialization.

#### Example 1 — static variable: division by zero

```java
class ExceptionInInitializerExample1 {
    static int x = 10 / 0;
    public static void main(String[] args) { }
}
```

```text
$ javac ExceptionInInitializerExample1.java   # compiles fine
$ java ExceptionInInitializerExample1
Exception in thread "main" java.lang.ExceptionInInitializerError
Caused by: java.lang.ArithmeticException: / by zero
    at ExceptionInInitializerExample1.<clinit>(ExceptionInInitializerExample1.java:2)
```

- Root cause: `ArithmeticException` during static variable initialization.
- Wrapper: `ExceptionInInitializerError` — the JVM's way of reporting a
  failure in the initializer (static init phase).

Sir initially omitted `main` entirely and hit a JDK 1.6-vs-1.7 launcher
nuance (older launchers ran the static initializer regardless of whether
`main` existed; newer ones check for `main` first). He adds `main` and the
demo behaves the same on any JDK, including current ones.

#### Example 2 — static block: `NullPointerException`

```java
class ExceptionInInitializerExample2 {
    static {
        String s = null;
        System.out.println(s.length());
    }

    public static void main(String[] args) { }
}
```

```text
$ javac ExceptionInInitializerExample2.java
$ java ExceptionInInitializerExample2
Exception in thread "main" java.lang.ExceptionInInitializerError
Caused by: java.lang.NullPointerException: Cannot invoke "String.length()" because "s" is null
    at ExceptionInInitializerExample2.<clinit>(ExceptionInInitializerExample2.java:4)
```

**Board summary for #6:**

| Point | Detail |
|---|---|
| Hierarchy | Child of `Error` → unchecked |
| Raised by | JVM automatically |
| When | Any exception during static variable assignment or static block execution |

> ❗ **Correction — "child class of `Error`" is one generation short for all three `Error`s above.**
> `StackOverflowError`, `NoClassDefFoundError`, and `ExceptionInInitializerError`
> are unchecked because they descend from `Error` — that part is right, and
> it is all the OCJP exam actually asks. But none of them extends `Error`
> directly:
>
> ```text
> java.lang.Error
> ├── java.lang.VirtualMachineError
> │     └── java.lang.StackOverflowError
> └── java.lang.LinkageError
>       ├── java.lang.NoClassDefFoundError
>       └── java.lang.ExceptionInInitializerError
> ```
>
> Verified with `javap java.lang.StackOverflowError` (etc.) on JDK 26. This
> hierarchy predates this recording — it is a precision correction, not a
> modern-Java change. Sir's shorthand just skips a generation, and the exam
> only ever tests "`Error` subclass ⇒ unchecked," so the shorthand never cost
> anyone marks.

### 52:27 — #7 (started): `IllegalArgumentException`

Sir closes the sixth exception and begins the seventh —
`IllegalArgumentException` — with the session ending here (video ~52m 53s).
`IllegalArgumentException` was already introduced above via
`Thread.setPriority(15)` and the JDK `Thread` source. Full board treatment of
**#7–#10** (`IllegalArgumentException`, `NumberFormatException`,
`IllegalStateException`, `AssertionError`) plus a summary table of all 10
continues in **Video 079**.

Quick recap from this video for #7:

```java
class IllegalArgumentExceptionPreview {
    public static void main(String[] args) {
        Thread t = new Thread();
        t.setPriority(7);  // valid
        t.setPriority(15); // illegal argument — API developer throws this
    }
}
// runtime: IllegalArgumentException
// Programmatic exception (API developer), NOT JVM exception
```

---

## Progress checklist — top 10 (this video vs next)

| # | Name | Covered in 078? |
|---|---|---|
| 1 | `ArrayIndexOutOfBoundsException` | Yes — full |
| 2 | `NullPointerException` | Yes — full |
| 3 | `ClassCastException` | Yes — full |
| 4 | `StackOverflowError` | Yes — full |
| 5 | `NoClassDefFoundError` | Yes — full |
| 6 | `ExceptionInInitializerError` | Yes — full |
| 7 | `IllegalArgumentException` | Started (detailed in 079) |
| 8 | `NumberFormatException` | Video 079 |
| 9 | `IllegalStateException` | Video 079 |
| 10 | `AssertionError` | Video 079 |

## Master comparison table (exceptions covered in 078)

| Exception / Error | Immediate parent | Checked? | JVM or programmatic? | When raised |
|---|---|---|---|---|
| `ArrayIndexOutOfBoundsException` | `IndexOutOfBoundsException` | Unchecked | JVM | Array index out of range |
| `NullPointerException` | `RuntimeException` | Unchecked | JVM | Operation on `null` |
| `ClassCastException` | `RuntimeException` | Unchecked | JVM | Invalid parent→child cast |
| `StackOverflowError`* | `VirtualMachineError` | Unchecked | JVM | Unbounded recursion |
| `NoClassDefFoundError`* | `LinkageError` | Unchecked | JVM | A referenced `.class` file can't be found at link time |
| `ExceptionInInitializerError`* | `LinkageError` | Unchecked | JVM | Exception in static init |
| `IllegalArgumentException` | `RuntimeException` | Unchecked | Programmatic | Illegal method argument (preview) |

\* Board shorthand calls these "child of `Error`" — see the correction above
`IllegalArgumentException` for the exact intermediate class.

## Quick reference — exception hierarchy (board, corrected)

```text
java.lang.Throwable
  ├── Error                            (unchecked)
  │     ├── VirtualMachineError
  │     │     └── StackOverflowError
  │     └── LinkageError
  │           ├── NoClassDefFoundError
  │           └── ExceptionInInitializerError
  └── Exception
        ├── RuntimeException           (unchecked)
        │     ├── ArithmeticException
        │     ├── NullPointerException
        │     ├── IndexOutOfBoundsException
        │     │     └── ArrayIndexOutOfBoundsException
        │     ├── ClassCastException
        │     └── IllegalArgumentException
        └── ... checked exceptions ...
```

## Exam and interview points

1. **Two independent classifications:** checked/unchecked (compile-time
   contract) **vs** JVM/programmatic (who raised it) — a question can ask
   about either axis for the same exception.
2. **`Error` vs `Exception`:** `StackOverflowError`, `NoClassDefFoundError`,
   and `ExceptionInInitializerError` are `Error` subclasses, not `Exception`
   — still unchecked. Precisely: `StackOverflowError` is a
   `VirtualMachineError`; the other two are `LinkageError`s.
3. **`ExceptionInInitializerError`:** always ask *what caused it* — read the
   `Caused by:` line (`ArithmeticException`, `NullPointerException`, etc.).
4. **`ClassCastException`:** a downcast fails when the runtime object type
   does not match; a parent reference holding a child object can downcast
   safely.
5. **`NoClassDefFoundError` vs `ClassNotFoundException`:** the first is an
   unchecked `Error` the JVM raises while linking a class another loaded
   class needs; the second is a checked `Exception` from explicit reflective
   loading (`Class.forName`). Deleting the `.class` file of the class you
   actually launch produces neither — the launcher fails first with
   `Error: Could not find or load main class`.
6. **API developer exceptions** (e.g. `IllegalArgumentException` in
   `Thread.setPriority`) are programmatic, not JVM — the JVM does not know
   the valid priority range; the API method validates and throws.
7. **Interview-current framing:** `Thread.setPriority`'s range check
   (1–10, `IllegalArgumentException` outside it) is unchanged since this
   recording, but on a **virtual thread (Java 21+)** the value it sets is
   never actually used for scheduling — know the distinction if asked about
   virtual threads.
8. **Diagnostic messages have improved across the board** since this
   recording: helpful `NullPointerException` text (Java 14/15), descriptive
   `ArrayIndexOutOfBoundsException` bounds (JDK 11+), and module-aware
   `ClassCastException` text (Java 9+). None of this changes which exception
   type is thrown — only how much the message tells you.

**Next:** Video 079 — try-with-resources and multi-catch (finishes items 7–10 of the top 10)
