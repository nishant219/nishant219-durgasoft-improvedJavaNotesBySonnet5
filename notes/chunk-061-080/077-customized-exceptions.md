# Video 077 — Customized exceptions

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-7 || Customized Exceptions

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 77 of 203 |
| Series | Exception Handling · Part 7 |
| Topic | Customized Exceptions |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 05m 45s |
| Video ID | t-9RCfuHsAk |
| Watch | https://www.youtube.com/watch?v=t-9RCfuHsAk |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This session closes out the five exception-handling keywords
(`try`/`catch`/`finally`/`throw`/`throws`), revisits the eight compile-time
errors the series has produced along the way, then spends the bulk of its
time on **customized (user-defined) exceptions** — how to define one, how to
raise it with `throw`, and three conclusions worth memorizing verbatim:

1. `throw` is the right tool for raising *your own* exceptions — the JVM
   raises predefined ones automatically, but only you know your business rule.
2. Extend `RuntimeException` (unchecked), not `Exception` (checked).
3. Always call `super(msg)` — it is the only way your message reaches
   `Throwable`, which is what the default handler's `printStackTrace()`
   actually prints.

The lecture's running example is a matrimonial-website age check (register
only between 18 and 60), used purely as a vehicle for two custom exception
classes, `TooYoungException` and `TooOldException`. A long, non-technical
tangent about matrimonial sites sits in the middle of the recording — it
contains no Java content and is skipped here.

---

## 00:07 — Recap: the five exception-handling keywords

Before customized exceptions, Sir re-drills the five keywords covered across
this series — a favorite interview question in its own right.

| Keyword | Purpose |
|---|---|
| `try` | To maintain risky code |
| `catch` | To maintain exception-handling code |
| `finally` | To maintain cleanup code |
| `throw` | To hand over our created exception object to the JVM manually |
| `throws` | To delegate responsibility of exception handling to the caller |

**`thrown` is not a Java keyword.** Sir compares it to English verb triples
(*give/gave/given*, *take/took/taken*) to warn that students invent a past
participle that doesn't exist: `throw` and `throws` are both real keywords,
`thrown` is not one of them and never has been. If an interviewer or an FAQ
book asks about it, the correct answer is exactly that — there is no
`thrown` keyword — not a story about what it might do.

---

## 08:40 — Eight compile-time errors, revisited

Sir lists all eight compile errors this exception-handling series has
produced, on the grounds that **each error message is itself an exam
conclusion worth memorizing**. All eight were verified against a current
`javac` below; the wording matches what the compiler still emits today.

```java
// CE: unreported exception IOException; must be caught or declared to be thrown
class Demo1 {
    void m1() {
        throw new java.io.IOException("fail");
    }
}
```

```java
// CE: exception ArithmeticException has already been caught
class Demo2 {
    public static void main(String[] args) {
        try {
            int x = 10 / 0;
        } catch (Exception e) {
        } catch (ArithmeticException e) { // duplicate — already caught above
        }
    }
}
```

```java
// CE: exception FileNotFoundException is never thrown in body of corresponding try statement
class Demo3 {
    public static void main(String[] args) {
        try {
            System.out.println("hello");
        } catch (java.io.FileNotFoundException e) {
        }
    }
}
```

```java
// CE: unreachable statement
class Demo4 {
    public static void main(String[] args) {
        throw new RuntimeException();
        System.out.println("hello"); // unreachable — nothing may follow throw
    }
}
```

```java
// CE: incompatible types: String cannot be converted to Throwable
class Demo5 {
    public static void main(String[] args) {
        throw "not an exception"; // throw needs a Throwable, not a String
    }
}
```

```java
// CE: 'try' without 'catch', 'finally' or resource declarations
class Demo6 {
    public static void main(String[] args) {
        try {
            System.out.println("risky");
        } // missing catch or finally
    }
}
```

```java
// CE: 'catch' without 'try'
class Demo7 {
    public static void main(String[] args) {
        catch (Exception e) { // illegal without a preceding try
        }
    }
}
```

```java
// CE: 'finally' without 'try'
class Demo8 {
    public static void main(String[] args) {
        finally {
            System.out.println("cleanup");
        }
    }
}
```

These were already demonstrated with fuller examples across the series;
here they're a checklist. Note that each error message names the actual
problem — that's the exam-relevant detail, not the exact punctuation, which
can drift a little between JDK releases.

---

## 14:01 — What are customized exceptions?

> **Sometimes, to meet our program requirement, we can create our own
> exceptions. Such exceptions are called customized exceptions, user-defined
> exceptions, or programmer-defined exceptions.**

Sir's motivating example: a matrimonial website that only accepts
registrations between ages 18 and 60. Someone registering at 99 should get a
`TooYoungException` with a "wait for a better match" message; someone
registering at 14 should get a `TooOldException` saying they're already past
marriage age. Neither of these is a real Java exception — the JVM has no
idea what a valid registration age is for *this* application. That's the
whole point: **customized exceptions exist because the JVM cannot know your
program's business rules**, only you can.

Other names used in the lecture for the same idea: `InsufficientFundsException`
for a banking app that won't let a withdrawal exceed the balance — the same
shape, a different domain.

---

## 37:40 — How to define a customized exception

**Every exception is a Java class.** To define your own, that class must be
a child of `Throwable` — directly or indirectly. Sir's strong recommendation
is to make it indirect, by extending `RuntimeException` (the reasoning is
Conclusion 2, below).

```java
class TooYoungException extends RuntimeException {
    TooYoungException(String msg) {
        super(msg);
    }
}

class TooOldException extends RuntimeException {
    TooOldException(String msg) {
        super(msg);
    }
}
```

If no description is ever needed, even the constructor is optional — an
empty class extending `RuntimeException` is a complete, legal exception:

```java
class TooYoungException extends RuntimeException {
}
```

**General template:**

```java
// 1. name it *Exception by convention
// 2. extend RuntimeException (recommended — see Conclusion 2)
// 3. add a String constructor that calls super(msg) if a message is needed

class MyCustomException extends RuntimeException {
    MyCustomException(String msg) {
        super(msg); // makes the description available to the default handler
    }
}
```

> ⚠️ **Modern Java — sealed classes give you a closed exception hierarchy (17).**
> Nothing in Java 6/7 stopped another package from writing a third subclass
> of your exception. Since **Java 17** you can close the hierarchy Sir is
> building here with `sealed`/`permits`, so `TooYoungException` and
> `TooOldException` are declared as the *only* kinds of registration failure
> that can exist:
>
> ```java
> sealed class RegistrationException extends RuntimeException
>         permits TooYoungException, TooOldException {
>     RegistrationException(String msg) { super(msg); }
> }
>
> final class TooYoungException extends RegistrationException {
>     TooYoungException(String msg) { super(msg); }
> }
>
> final class TooOldException extends RegistrationException {
>     TooOldException(String msg) { super(msg); }
> }
> ```
>
> A `switch` over a sealed exception type can then be checked exhaustively by
> the compiler (Java 21 pattern matching for switch) — useful once an
> application has more than a couple of custom exception types. One related
> question that comes up: could `TooYoungException` be a `record` instead of
> a class, to save typing? No — a record implicitly extends `java.lang.Record`,
> and Java has single inheritance, so a record can never extend `Throwable`.
> Custom exceptions stay plain classes.

---

## 41:08 — Full demo: matrimonial-site age validation

```java
class TooYoungException extends RuntimeException {
    TooYoungException(String msg) {
        super(msg);
    }
}

class TooOldException extends RuntimeException {
    TooOldException(String msg) {
        super(msg);
    }
}

class CustomExceptionDemo {
    public static void main(String[] args) {
        int age = Integer.parseInt(args[0]);

        if (age > 60) {
            throw new TooYoungException(
                "Please wait some more time. You will get the best match soon.");
        } else if (age < 18) {
            throw new TooOldException(
                "Your age already crossed marriage age. No chance of getting marriage.");
        } else {
            System.out.println("You will get match details soon by email.");
        }
    }
}
```

The names and the ages look swapped, and they are — on screen Sir jokes that
he's "taking reverse exceptions... just for fun" while writing this. The
logic that actually runs is exactly what's above: too *old* an applicant
(`age > 60`) raises `TooYoungException`, too *young* (`age < 18`) raises
`TooOldException`. Follow the code, not the joke.

---

## 46:04 — Compile and run

```text
javac CustomExceptionDemo.java
```

```text
java CustomExceptionDemo 99
```
```text
// prints:
// Exception in thread "main" TooYoungException: Please wait some more time. You will get the best match soon.
```

```text
java CustomExceptionDemo 14
```
```text
// prints:
// Exception in thread "main" TooOldException: Your age already crossed marriage age. No chance of getting marriage.
```

```text
java CustomExceptionDemo 27
```
```text
// prints:
// You will get match details soon by email.
```

Verified against a current JDK: all three outputs are exactly as taught
(the uncaught-exception line also carries a stack trace underneath it in a
real run, trimmed here for focus).

---

## 53:17 — Conclusion 1: when to raise a customized exception

**Predefined exceptions** — the JVM/library already knows exactly when to
raise them:

| Exception | When raised |
|---|---|
| `ArithmeticException` | Division by zero |
| `NullPointerException` | An operation performed on a `null` reference |

> ⚠️ **Modern Java — an uncaught `NullPointerException` now names the null
> reference.** Since **Java 14** (JEP 358, default since 15), the message
> says exactly what was null and what you tried to do with it, instead of
> just pointing at a line number:
>
> ```text
> Exception in thread "main" java.lang.NullPointerException:
>     Cannot read field "balance" because "<local1>" is null
> ```
>
> Same exception class Sir is teaching, far less guesswork tracking it down.

**Customized exceptions** — the JVM has no idea when to raise these; *you*
decide, based on the program's requirement. If the matrimonial site's
supported age range changes from 18–60 to 21–70, only the boundary numbers
in the `if` conditions change — the mechanism (`throw new
TooYoungException(...)`) does not:

```java
if (age > 70) {
    throw new TooYoungException("Please wait some more time...");
} else if (age < 21) {
    throw new TooOldException("Your age already crossed marriage age...");
} else {
    System.out.println("You will get match details soon by email.");
}
```

Because the JVM cannot decide this for you, `throw` is the tool you reach
for: it is the **best fit for user-defined exceptions**, not typically for
predefined ones, precisely because predefined exceptions are already raised
automatically by the JVM or the library.

---

## 56:46 — Conclusion 2: extend `RuntimeException` (unchecked), not `Exception` (checked)

**Highly recommended:** make customized exceptions unchecked, by extending
`RuntimeException`. A child of `RuntimeException` is unchecked, so the
compiler never forces a `try`/`catch` or a `throws` clause on code that
raises it.

**Checked version (not recommended):**

```java
class TooYoungException extends Exception {
    TooYoungException(String msg) {
        super(msg);
    }
}

class CustomExceptionDemo {
    public static void main(String[] args) {
        int age = Integer.parseInt(args[0]);
        if (age > 60) {
            throw new TooYoungException("Please wait..."); // CE without try-catch or throws
        }
    }
}
// CE: unreported exception TooYoungException; must be caught or declared to be thrown
```

**Unchecked version (recommended):**

```java
class TooYoungException extends RuntimeException {
    TooYoungException(String msg) {
        super(msg);
    }
}

class CustomExceptionDemo {
    public static void main(String[] args) {
        int age = Integer.parseInt(args[0]);
        if (age > 60) {
            throw new TooYoungException("Please wait..."); // compiles fine
        }
    }
}
```

> **Board:** It is highly recommended to define customized exceptions as
> unchecked — i.e., extend `RuntimeException`, but not `Exception`.

Both compile-time behaviors above were verified against a current JDK and
match exactly: the checked version fails with "unreported exception ... must
be caught or declared to be thrown"; the unchecked version compiles clean.

---

## 1:00:38 — Conclusion 3: why `super(msg)` matters

When an exception goes uncaught, the **default exception handler** prints
it using `printStackTrace()`, which is defined on `Throwable` — the top of
the hierarchy every exception, including this one, sits under:

```text
TooYoungException
  └── RuntimeException
        └── Exception
              └── Throwable   ← printStackTrace() lives here
```

The message string has to travel up that whole chain to reach `Throwable`,
which is where it's actually stored:

```java
class TooYoungException extends RuntimeException {
    TooYoungException(String msg) {
        super(msg); // passes msg up: RuntimeException → Exception → Throwable
    }
}
```

`super(msg)` is that hand-off. `Throwable` stores the string, and
`printStackTrace()` reads it back out when the default handler prints to the
console.

> ❗ **Correction — without `super(msg)`, the message doesn't "maybe" show up; it never does.**
> Dropping the `super(msg)` call (or writing an empty constructor body)
> doesn't just risk losing the message — it guarantees it, because there is
> no other path for a `String` to reach `Throwable`'s stored message field.
> Verified directly:
>
> ```java
> class TooYoungException extends RuntimeException {
>     TooYoungException(String msg) {
>         // super(msg) missing — the message has nowhere to go
>     }
> }
> // throw new TooYoungException("Please wait some more time.");
> // prints only:
> // Exception in thread "main" TooYoungException
> //     at NoSuperMsg.main(NoSuperMsg.java:8)
> ```
>
> The constructor parameter `msg` is simply discarded. `printStackTrace()`
> has nothing to print beyond the class name.

---

## 1:05:22 — Session wrap-up: three key takeaways

1. **What customized/user-defined exceptions are** — your own exception
   classes, created to meet a program's own requirements.
2. **How to define one** — a class under the `Throwable` hierarchy,
   preferably extending `RuntimeException` directly.
3. **How to use one** — validate a business rule, then
   `throw new MyException("message")`.

---

## Exam and interview points

1. **The five exception-handling keywords and their purposes** —
   `try`/risky code, `catch`/handling code, `finally`/cleanup,
   `throw`/hand an object to the JVM, `throws`/delegate to the caller —
   plus the trap: **`thrown` is not a Java keyword.**
2. **Know all eight compile-time errors by name**, not just by cause: each
   one (unreported exception, already-caught, never-thrown-in-try,
   unreachable statement, incompatible types, and the three
   try/catch/finally-without-its-partner errors) is a standalone question.
3. **The JVM raises predefined exceptions automatically; it never raises
   your own.** That's the entire justification for customized exceptions,
   and for why `throw` — not the JVM — is how they get raised.
4. **Extend `RuntimeException`, not `Exception`, for your own exceptions.**
   Unchecked means the compiler never forces a `try`/`catch` or `throws` on
   code that raises it — checked forces exactly that, for no benefit when
   the exception is purely your own business rule.
5. **`super(msg)` is not optional if you want the message to print.** It is
   the only route by which the `String` reaches `Throwable`'s stored
   message, which `printStackTrace()` reads. Skip it and the description is
   gone, not just unreliable.
6. **Since Java 14/15, an uncaught `NullPointerException` names the exact
   null reference** — worth citing when discussing predefined exceptions
   like the `ArithmeticException`/`NullPointerException` pair above.
7. **Since Java 17, `sealed`/`permits` can close a custom exception
   hierarchy** to a fixed, named list of subclasses — a modern refinement of
   exactly the `TooYoungException`/`TooOldException` pattern taught here. A
   custom exception can never be a `record`, because records can't extend
   any class other than the implicit `java.lang.Record`.

---

**Next:** Video 078 — Top-10 exceptions in Java
