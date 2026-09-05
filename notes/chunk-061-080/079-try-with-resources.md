# Video 079 — try-with-resources and multi-catch

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-9 || try with resources and multi-catch block

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 79 of 203 |
| Series | Exception Handling · Part 9 |
| Topic | try with resources and multi-catch block |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 51m 30s |
| Video ID | 0n4Rh2Anlbw |
| Watch | https://www.youtube.com/watch?v=0n4Rh2Anlbw |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is Exception Handling **Part 9**. The first ~32 minutes finish the
**top 10 exceptions** started in the morning session: items 7–10
(`IllegalArgumentException`, `NumberFormatException`, `IllegalStateException`,
`AssertionError`) plus the JVM-vs-programmatic summary. The middle of the
video is the **two Java 1.7 exception-handling enhancements**:
try-with-resources and multi-catch. The last ~7 minutes cover two more
vocabulary words: **exception propagation** and **rethrowing an exception**.

Sir does **not** teach suppressed exceptions, the reverse close order of
multiple resources, or the Java 9 existing-variable form of
try-with-resources in this video — those are noted below only as forward
references, not backfilled into his teaching.

---

## 00:07 — Recap: six down, four to go

Six exception classes were already covered in the morning — each classified
as checked/unchecked and as a **JVM exception** or a **programmatic
exception**. Four remain.

### 00:29 — Seventh: `IllegalArgumentException`

`IllegalArgumentException` is a child class of `RuntimeException`, and hence
**unchecked**.

**When do we get it?** Every `Thread` has a **priority**, and the valid range
of thread priorities is **1 to 10**.

```java
class ThreadPriority {
    public static void main(String[] args) {
        Thread t = new Thread();
        t.setPriority(7);   // valid — inside 1..10
        t.setPriority(15);  // 15 is outside 1..10
    }
}
// runtime: IllegalArgumentException
```

`setPriority(15)` immediately raises a runtime `IllegalArgumentException`.

Who decides whether an argument is legal? Either the **programmer** or the
**API developer** — the JVM has no idea what counts as a valid priority.
That is why `IllegalArgumentException` is not a JVM exception; it is a
**programmatic exception**.

**Board:**

1. Child class of `RuntimeException`, hence unchecked.
2. Raised explicitly, by the programmer or the API developer, to indicate
   that a method has been invoked with an illegal argument.

> ⚠️ **Modern Java — thread priority is close to meaningless for virtual threads (21).**
> `Thread.MIN_PRIORITY` (1) and `Thread.MAX_PRIORITY` (10) are unchanged, and
> everything above is still exactly how priority works for **platform**
> threads. But a **virtual thread** (Project Loom, Java 21) always reports
> `Thread.NORM_PRIORITY` (5), and `setPriority(...)` on one is a silent no-op:
>
> ```java
> Thread vt = Thread.ofVirtual().unstarted(() -> {});
> vt.setPriority(1);
> System.out.println(vt.getPriority()); // 5 — unchanged
> ```
> Verified on JDK 26. Priority still throws `IllegalArgumentException` for an
> out-of-range value on *any* thread — that check runs before the JVM even
> looks at whether the thread is virtual.

### 06:56 — Eighth: `NumberFormatException`

```java
int i = Integer.parseInt("10");  // valid
int j = Integer.parseInt("ten"); // "ten" is not a properly formatted number
```

`parseInt("10")` works fine. `parseInt("ten")` raises a runtime
`NumberFormatException` — the string is not properly formatted, it does not
represent a number.

Think one level higher: `"10"` is a *legal* argument, `"ten"` is an *illegal*
one. `NumberFormatException` is not a new, separate idea — it is a **special
case of `IllegalArgumentException`**, and in the API `NumberFormatException`
is its direct child class.

Sir starts to write "direct child class of `RuntimeException`" on the board,
catches himself mid-sentence — "sorry, sorry, wrong" — and corrects it to
**direct child of `IllegalArgumentException`**, which is itself a child of
`RuntimeException`. Confirmed against the JDK: `NumberFormatException`'s
superclass is `IllegalArgumentException`. Unchecked either way.

**Board:**

1. Direct child of `IllegalArgumentException`, which is a child of
   `RuntimeException` — unchecked.
2. Raised explicitly, by the programmer or API developer, to indicate that a
   string-to-number conversion failed because the string is not properly
   formatted.

### 14:09 — Ninth: `IllegalStateException`

**Story:** a person happily sleeping — calling *wake up* on them is legal,
appropriate, the right time. A person who is dead — calling *wake up* on
them is illegal; you invoked the method at the **wrong time**, and there is
no defined next state. That "no defined next state after a wrong-time call"
is the shape of `IllegalStateException`. (The story itself maps to no real
Java type; the technical example is `Thread.start()` called twice, next.)

**Board:**

1. Child class of `RuntimeException` — unchecked.
2. Raised explicitly, by the programmer or API developer, to indicate that a
   method has been invoked at the wrong time.

**Technical example:** a thread, like a person, has a life cycle. Starting
it once is the right time.

```java
Thread t = new Thread();
t.start(); // valid — thread's life cycle starts
```

Calling `start()` a **second time** on the same thread is calling it at the
wrong time — like asking to restart a life that already ended:

```java
class RestartSameThread {
    public static void main(String[] args) {
        Thread t = new Thread();
        t.start(); // first time — appropriate
        t.start(); // second time — inappropriate
    }
}
// runtime: IllegalThreadStateException
```

Sir describes the result as "`IllegalStateException` only — by default we
get `IllegalThreadStateException`," i.e. `IllegalThreadStateException` as a
more specific subclass of `IllegalStateException`.

> ❗ **Correction — `IllegalThreadStateException` is not a subclass of `IllegalStateException`.**
> Despite the name, and despite illustrating exactly the "method called at
> the wrong time" idea `IllegalStateException` is built around, the JDK
> hierarchy is:
>
> ```
> IllegalThreadStateException → IllegalArgumentException → RuntimeException
> ```
>
> Verified with `IllegalThreadStateException.class.getSuperclass()` on
> JDK 26, which returns `java.lang.IllegalArgumentException` — the two classes
> (`IllegalStateException` and `IllegalThreadStateException`) share a
> grandparent (`RuntimeException`) but neither extends the other. It is a
> genuine, long-standing naming quirk in `java.lang`, and a good exam trap in
> its own right: don't infer hierarchy from a class name that merely sounds
> related. Both are still unchecked, and calling `start()` twice still throws
> exactly `IllegalThreadStateException` in current Java.

### 23:31 — Tenth: `AssertionError`

Child class of **`Error`**, hence unchecked. Raised explicitly, by the
programmer or API developer, to indicate that an `assert` statement failed.

```java
class AssertDemo {
    public static void main(String[] args) {
        int x = 5;
        assert x > 10; // if everything's fine, x should be > 10 here
    }
}
// runtime: AssertionError   (only when assertions are enabled: java -ea AssertDemo)
```

If `x` is not greater than 10 at that point, something went wrong, and the
JVM raises `AssertionError` — but only when assertions are enabled at
launch. This behaviour (assertions off by default, `-ea` to enable) is
unchanged since `assert` arrived in Java 1.4 and is still true today.

### 27:09 — Summary: JVM exceptions vs programmatic exceptions

| # | Exception | Raised by | Notes |
|---|---|---|---|
| 1 | `ArrayIndexOutOfBoundsException` | JVM | automatic |
| 2 | `NullPointerException` | JVM | automatic |
| 3 | `ClassCastException` | JVM | automatic |
| 4 | `StackOverflowError` | JVM | automatic |
| 5 | `NoClassDefFoundError` | JVM | automatic |
| 6 | `ExceptionInInitializerError` | JVM | automatic — **exam trap**, new to most people |
| 7 | `IllegalArgumentException` | programmer / API developer | explicit |
| 8 | `NumberFormatException` | programmer / API developer | explicit; special case of #7 |
| 9 | `IllegalStateException` | programmer / API developer | explicit |
| 10 | `AssertionError` | programmer / API developer | explicit |

The first six are raised **automatically by the JVM** — JVM exceptions. The
remaining four are raised **explicitly** by a programmer or API developer —
programmatic exceptions. The typical exam question spells out four or five
of these and asks which are which; `ExceptionInInitializerError` is the one
most people get wrong.

---

## 32:45 — Two 1.7 enhancements to exception handling

Java **1.7** introduced two concepts here: **try-with-resources** and
**multi-catch block**.

## 34:57 — Try-with-resources

### 35:09 — Until 1.6: open in try, close in finally

Until 1.6, whatever resource you opened inside a try block, you had to close
inside a `finally` block — and only after checking it was non-null, since
the `try` could have failed before assignment.

```java
import java.io.*;

class Until16CloseInFinally {
    public static void main(String[] args) throws IOException {
        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader("input.txt"));
            // use br
        } catch (IOException e) {
            // handling code
        } finally {
            if (br != null) {
                br.close();
            }
        }
    }
}
```

**Problems with this approach:**

1. The programmer is *compulsorily* responsible for closing every resource
   inside `finally` — forget it once, and you leak a resource.
2. `finally` is compulsory to write — it lengthens the code and hurts
   readability.

### 39:05 — 1.7: resources close automatically

```java
import java.io.*;

class TryWithResources17 {
    public static void main(String[] args) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
            // use br
            // br closes automatically once control reaches end of try block,
            // normally or abnormally — no explicit close(), no finally needed
        } catch (IOException e) {
            // handling code
        }
    }
}
```

Whatever resource is opened in the `try (...)` clause — a `BufferedReader`,
a database connection, a socket, a `FileWriter`, anything — is **closed
automatically** once control leaves the try block, whether that happens
normally or via an exception. `finally` is no longer required. Complexity
goes down, code length goes down, readability goes up. Until 1.6, `finally`
was the hero of resource cleanup; from 1.7 onward it is a dummy — zero.

### Conclusions about try-with-resources

**Conclusion 1 — declare any number of resources, separated by semicolons.**

```java
import java.io.*;

class MultipleResources {
    public static void main(String[] args) throws IOException {
        try (FileWriter fw = new FileWriter("output.txt");
             FileReader fr = new FileReader("input.txt")) {
            // first resource — write to output.txt
            // second resource — read from input.txt
        }
    }
}
```

**Conclusion 2 — every resource must be `AutoCloseable`.** A resource is
AutoCloseable if and only if its class implements `java.lang.AutoCloseable`.
All the IO, database (`Connection`), and network resources you'd normally
use already implement it — you don't need to do anything as a programmer
beyond being aware of the rule.

```java
package java.lang;

public interface AutoCloseable {
    void close() throws Exception;
}
```

> ❗ **Correction — `close()` is not a bare, exception-free method.**
> Sir dictates `public void close` with no `throws` clause. The real
> interface, confirmed with `javap java.lang.AutoCloseable` on JDK 26, is
> `void close() throws Exception;` — the broad `Exception` is deliberate, so
> any resource type can declare whatever close-time failure fits it.
> `java.io.Closeable` (which `FileReader`, `FileWriter`, `BufferedReader`,
> and friends implement) narrows that to `void close() throws IOException;`
> via `javap java.io.Closeable`. Practically this rarely bites you — you're
> consuming these interfaces, not implementing `close()` yourself — but if
> you ever write your own `AutoCloseable` resource, its `close()` can throw
> checked `Exception` unless you narrow it.

**Conclusion 3 — resource reference variables are implicitly final.**

```java
import java.io.*;

class TryWithResources {
    public static void main(String[] args) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader("input.txt"))) {
            br = new BufferedReader(new FileReader("output.txt"));
        }
    }
}
// CE: auto-closeable resource br may not be assigned
```

Verified: `javac` reports exactly `auto-closeable resource br may not be
assigned`. The reasoning: if `br` were reassigned mid-block, which
`BufferedReader` should the try syntax close — the old one pointing at
`input.txt`, or the new one pointing at `output.txt`? To remove that
ambiguity, every resource variable declared in the `try (...)` clause is
**implicitly final**; reassigning it inside the block is a compile-time
error.

> ⚠️ **Modern Java — Java 9 lets you reuse an already-final(-enough) variable directly (JEP 213).**
> Until Java 8, the resource had to be declared *inside* the parentheses, as
> above. From **Java 9** onward, if a variable is already final or
> effectively final, you can hand it to `try (...)` by name, with no
> re-declaration:
>
> ```java
> BufferedReader br = new BufferedReader(new FileReader("input.txt"));
> try (br) {
>     // use br — still closed automatically at the end of the block
> }
> ```
> Verified compiling with `javac --release 9`. It still can't be reassigned
> anywhere it would stop being effectively final — the "implicitly final"
> rule from Conclusion 3 doesn't go away, it just no longer forces a fresh
> declaration.

**Conclusion 4 — try-with-resources needs neither `catch` nor `finally`.**

Until 1.6, a `try` had to be followed by `catch` or `finally` — a bare `try`
was a compile error:

```java
class TryAlone {
    public static void main(String[] args) {
        try {
            System.out.println("only try");
        }
    }
}
// CE: 'try' without 'catch', 'finally' or resource declarations
```

From 1.7 onward, `try (resource) { ... }` alone is perfectly valid — whatever
`finally` used to do (closing the resource), the resource clause now does:

```java
import java.io.*;

class OnlyTryWithResource {
    public static void main(String[] args) throws IOException {
        try (FileReader r = new FileReader("input.txt")) {
            // valid from 1.7, with no catch or finally
        }
    }
}
```

**Summary:** the main advantage of try-with-resources is that resources
close automatically at the end of the try block — normal or abnormal exit —
so you're never required to close them explicitly or write a `finally`
block for cleanup. Until 1.6, `finally` was the hero of resource management;
from 1.7 on, it's optional dead weight for that job.

---

## 1:20:48 — Multi-catch block

### 1:21:20 — Until 1.6: same handling code still needs separate catch blocks

Even when two *different* exception types need *identical* handling code,
1.6 forces a separate `catch` for each — unless one is the parent of the
other, in which case the parent alone suffices.

```java
import java.io.*;

class Until16SeparateCatch {
    void m() {
        try {
            // ...
        } catch (ArithmeticException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (NullPointerException e) {
            System.out.println(e.getMessage());
        } catch (InterruptedException e) {
            System.out.println(e.getMessage());
        }
    }
}
// CE: exception IOException is never thrown in body of corresponding try statement
// CE: exception InterruptedException is never thrown in body of corresponding try statement
```

(The two `// CE` lines are the compiler's own reaction to an empty try body
— shown here to confirm the *shape* of the catch chain compiles cleanly once
the try body actually can throw those types; verified against `javac`.)

`ArithmeticException`/`IOException` share `printStackTrace()`;
`NullPointerException`/`InterruptedException` share `e.getMessage()` — but
because none of the four is a parent of another, all four catch blocks are
required. That increases code length and hurts readability.

### 1:24:26 — 1.7: one catch block, multiple types

```java
import java.io.*;

class MultiCatch17 {
    void m() {
        try {
            // ...
        } catch (ArithmeticException | IOException e) {
            e.printStackTrace();
        } catch (NullPointerException | InterruptedException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

A single `catch (A | B e)` block now handles multiple, unrelated exception
types with one handler. Less code, more readable.

### 1:33:02 — Live demo: either exception, one catch

```java
class MultiCatchBlock {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
            String s = null;
            System.out.println(s.length());
        } catch (ArithmeticException | NullPointerException e) {
            System.out.println(e);
        }
    }
}
// prints java.lang.ArithmeticException: / by zero
```

`10 / 0` throws first, and the multi-catch handles it. Comment out the
division and the `NullPointerException` from `s.length()` surfaces instead —
the same catch block handles that too:

```java
// with `System.out.println(10 / 0);` commented out:
// prints java.lang.NullPointerException
```

Whichever of the two exceptions actually fires, the one catch block
responds — that's the entire point of multi-catch.

### 1:38:38 — The twist: no parent/child relation allowed between alternatives

```java
class MultiCatchParentChild {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException | Exception e) {
            e.printStackTrace();
        }
    }
}
// CE: Alternatives in a multi-catch statement cannot be related by subclassing
```

Verified — `javac` reports exactly `Alternatives in a multi-catch statement
cannot be related by subclassing`, plus `Alternative ArithmeticException is
a subclass of alternative Exception`. The logic: if `Exception` already
handles everything `ArithmeticException` would, listing
`ArithmeticException` alongside it is redundant — and the compiler refuses
rather than silently ignoring the redundant branch. **Rule:** in a
multi-catch, no two alternatives may be in a parent/child (or identical)
relationship, in either direction.

---

## 1:44:23 — Exception propagation

If a method raises an exception and doesn't handle it, the JVM propagates
the exception object up to the **caller**, whose responsibility it then
becomes to handle it. That's exception propagation — Sir hadn't used this
exact word before, but the underlying default-exception-handling behaviour
was already covered.

```java
class ExceptionPropagationDemo {
    public static void main(String[] args) {
        m1();
    }
    public static void m1() {
        m2(); // caller of m2
    }
    public static void m2() {
        System.out.println(10 / 0); // raised here, not handled here
    }
}
// runtime: ArithmeticException — propagated m2 -> m1 -> main -> JVM's default handler
```

## 1:47:31 — Rethrowing an exception

Catching one exception type and throwing a *different* type from the
handler is rethrowing:

```java
class RethrowDemo {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
            throw new NullPointerException();
        }
    }
}
// runtime: NullPointerException
```

**Why do this?** To convert one exception type into another that the rest of
the system already knows how to present. Sir's example: a web app has a
`web.xml` error page configured for `NullPointerException`; if
`ArithmeticException` should show the *same* error page, catch it and
rethrow as `NullPointerException` so the existing mapping applies.

---

## Exam and interview points

1. **`IllegalArgumentException` (7), `NumberFormatException` (8),
   `IllegalStateException` (9), `AssertionError` (10)** complete the top-10
   list; all four are **unchecked** and **programmatic** (raised explicitly,
   not automatically by the JVM).
2. **Hierarchy chain:** `NumberFormatException` → `IllegalArgumentException`
   → `RuntimeException`. Don't stop at "direct child of `RuntimeException`" —
   that's the mistake Sir catches himself making live.
3. **`IllegalThreadStateException` extends `IllegalArgumentException`, not
   `IllegalStateException`** — a genuine JDK naming trap, verified on JDK 26.
   Calling `Thread.start()` twice throws exactly this exception.
4. **`AssertionError` is a child of `Error`**, not `Exception` — and
   assertions are disabled by default; run with `-ea` to see them fire.
5. **Try-with-resources (1.7):** resources declared in `try (...)` close
   automatically at block exit, normal or abnormal. `finally` becomes
   optional for cleanup. Multiple resources are semicolon-separated and
   close in reverse declaration order. Resources must implement
   `AutoCloseable` (`void close() throws Exception`, narrowed to
   `throws IOException` by `Closeable`).
6. **Resource variables are implicitly final** — reassigning one inside the
   try block is a compile error (`auto-closeable resource X may not be
   assigned`). Since **Java 9**, an existing effectively-final variable can
   be passed to `try (...)` without re-declaring it.
7. **`try (resource) { }` alone is valid from 1.7** — no `catch` or
   `finally` required, unlike a bare `try` which is always a compile error.
8. **Multi-catch (`catch (A | B e)`, 1.7)** lets one handler cover multiple
   unrelated exception types. The alternatives must have **no
   parent/child (or identical) relationship** — violating that is a compile
   error: "Alternatives in a multi-catch statement cannot be related by
   subclassing."
9. **Exception propagation:** an unhandled exception's object moves up to
   the caller, whose job it becomes to handle it.
10. **Rethrowing:** catching one exception type and throwing a different one
    converts it — typically to funnel multiple failure types into one
    error-handling path (e.g. one configured error page).
11. **Thread priority (1–10) is essentially inert on virtual threads
    (Java 21)** — `setPriority(...)` is a no-op there, always reporting
    `NORM_PRIORITY`. The 1–10 range and its `IllegalArgumentException` check
    still apply in full to platform threads.

**Next:** Video 080 — Exception Handling compilation
