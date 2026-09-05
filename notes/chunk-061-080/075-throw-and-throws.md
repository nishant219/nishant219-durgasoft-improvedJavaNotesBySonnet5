# Video 075 — throw and throws

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-5 || throw and throws

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 75 of 203 |
| Series | Exception Handling · Part 5 |
| Topic | throw and throws |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 50m 13s |
| Video ID | 4BkGDX_BvDY |
| Watch | https://www.youtube.com/watch?v=4BkGDX_BvDY |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

The video title promises both `throw` and `throws`, but on the board Sir only
finishes `throw` — his closing line is "that's all … throw keyword," and
Video 076 opens with "last session we covered throw; now throws." So this
note, like the lecture, stops at `throw`:

1. The ball-game picture: the programmer throws an exception object, the JVM
   catches it.
2. The same result two ways — `10 / 0` (the JVM creates the exception object
   internally) vs. `throw new ArithmeticException(...)` (the programmer
   creates it and hands it over).
3. Why you would deliberately throw one: ATM insufficient funds, an invalid
   recharge PIN — the best use of `throw` is **user-defined / customized
   exceptions**, not everyday ones like `ArithmeticException`.
4. Three rules for `throw`: `throw e` on a null reference gives
   `NullPointerException`; a statement written directly after `throw` is a
   compile error (unreachable); `throw` only accepts throwable types.

---

## 00:06 — First throw, then throws

Next up: the `throw` statement, then `throws`. Of the two, `throws` is the
one that carries real interview weight — `throw` itself is straightforward.
This video is `throw` only.

### 00:31 — Name it three ways

On the board it goes by three names for the same thing: throw **keyword**,
throw **statement**, throw **clause**.

### 00:48 — Ball game, not Java yet

Forget Java for a second: in a simple ball game, one person throws and
another catches. Map that onto Java:

| Ball game | Java |
|---|---|
| Person throwing | programmer |
| Person catching | JVM |
| The ball | exception object |

Sometimes the programmer **creates** an exception object and **hands it
over to the JVM**. The keyword for that hand-over is `throw`.

## 03:41 — Program 1: `10 / 0` (creation happens internally)

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10 / 0);
    }
}
// Exception in thread "main" java.lang.ArithmeticException: / by zero
//         at Test.main(Test.java:3)
```

Who is responsible for **creating** the exception object? The method in
which it's raised — this is the default exception handling from the earlier
sessions. Here that method is `main`: it creates an `ArithmeticException`
object and hands it to the JVM entirely **internally**. There's no `new` and
no `throw` anywhere in this code.

The JVM finds no handling code for it, so it hands the exception to the
**default exception handler**, which terminates the program abnormally and
prints the exception information to the console: exception in thread main,
`java.lang.ArithmeticException`, `/ by zero`, at `Test.main`.

## 06:00 — Doing the same job ourselves

Instead of letting `main` create the exception object internally, the
programmer can create it **explicitly** and hand it to the JVM **manually**.
That is what `throw` is for.

### 06:22 — Program 2: `throw new ArithmeticException(...)`

```java
class Test {
    public static void main(String[] args) {
        throw new ArithmeticException("division by zero");
    }
}
// Exception in thread "main" java.lang.ArithmeticException: division by zero
//         at Test.main(Test.java:3)
```

One line, two jobs:

1. `new ArithmeticException("division by zero")` — **creates** the exception
   object explicitly.
2. `throw` — **hands** that object to the JVM manually.

From there the story is identical to Program 1: no handling code, default
exception handler, abnormal termination, same kind of console print.

## 09:01 — Same result, different origin

The two programs print the same *shape* of output. The only difference is
where the creation and hand-over happen:

| `System.out.println(10 / 0)` | `throw new ArithmeticException(...)` |
|---|---|
| `main` creates the exception object and hands it to the JVM **internally** | the programmer creates it and hands it to the JVM **manually** |
| no handling code → default exception handler | same, after the `throw` |

**Sometimes we create an exception object explicitly and hand it to the JVM
manually. For that, we need the `throw` keyword.**

### 16:16 — Proving it's really "our" object

Change the message so the two runs are visibly different:

```java
class Test {
    public static void main(String[] args) {
        throw new ArithmeticException("division by zero explicitly");
    }
}
// Exception in thread "main" java.lang.ArithmeticException: division by zero explicitly
//         at Test.main(Test.java:3)
```

The description string is exactly whatever you pass to the constructor.
Same exception type, same default-handler story, same `at Test.main` — only
the message is the programmer's own.

## 20:56 — Then why create the problem on our own?

Reasonable objection: an exception is already "an unexpected event that
disturbs the flow" — why would you *manufacture* one? Because sometimes the
program genuinely requires it. Two everyday examples make the case.

### 21:29 — ATM: withdrawing more than the balance

An account holds ₹10,000. A withdrawal request for ₹20,000 must be rejected
before it goes anywhere near the ledger:

```java
class InsufficientFundsException extends RuntimeException {
}

class Account {
    double balance = 10000;

    void withdraw(double amount) {
        if (amount > balance) {
            throw new InsufficientFundsException();
        }
    }
}
```

This is a **program requirement**, not an artificial problem. Exceptions
created this way — for a specific business rule rather than a JVM-detected
failure — are called **user-defined** or **customized exceptions**.

### 24:11 — Recharge cards: an invalid PIN

Same idea with an old-style mobile recharge card: if the entered number
doesn't match anything in the database, the request cannot proceed.

```java
class InvalidPinException extends RuntimeException {
}

class Recharge {
    void enterPin() {
        throw new InvalidPinException();
    }
}
```

### 25:37 — Board note

> **Best use of the `throw` keyword is for user-defined exceptions or
> customized exceptions** — not for predefined ones like `ArithmeticException`
> or `NullPointerException`, which the JVM already raises for you.

---

## 26:24 — Case 1: `throw e` and the state of `e`

```java
class Test {
    static ArithmeticException e = new ArithmeticException();

    public static void main(String[] args) {
        throw e;
    }
}
// Exception in thread "main" java.lang.ArithmeticException
//         at Test.<clinit>(Test.java:2)
```

`e` is a static field of type `ArithmeticException`, created up front.
`throw e` throws that object. `ArithmeticException` has two constructors —
one taking a `String` message, one taking none — and here it's the no-arg
one, so the default print carries no message, just the exception's class
name.

> ❗ **Correction — the stack trace points at `<clinit>`, not `main`.**
> A `Throwable`'s stack trace is captured the moment it is **constructed**
> (`fillInStackTrace()` runs inside every `Throwable` constructor), not the
> moment it is thrown. Here the object is built as part of the static field
> initializer, which the JVM runs in a synthetic method called `<clinit>`
> — so `at Test.<clinit>` is what actually prints, confirmed against a real
> `javac`/`java` run. This has been true since Java 1.0; it is not a
> version-dependent detail. If the field were assigned inside `main` itself
> (`ArithmeticException e = new ArithmeticException(); throw e;`), the trace
> would correctly read `at Test.main` — the frame recorded is wherever
> `new` actually ran.

### 28:06 — Case 1 continued: `throw e` when `e` is null

```java
class Test {
    static ArithmeticException e;

    public static void main(String[] args) {
        throw e;
    }
}
// Exception in thread "main" java.lang.NullPointerException
//         at Test.main(Test.java:5)
```

Only a reference variable this time, never assigned. Compile-time error or
runtime exception? **The compiler only checks syntax** — `throw e` is
syntactically fine because `e` is declared as an `ArithmeticException`, a
throwable type. Whether an actual object sits behind that reference at
runtime is not the compiler's concern. This compiles cleanly.

At runtime, though: a static field's default value is `null`, so `e` refers
to nothing, and `throw null` immediately becomes a `NullPointerException` —
not `ArithmeticException`.

> **Board:** `throw e;` — if `e` refers to `null`, we get `NullPointerException`.

> ⚠️ **Modern Java — this NPE now names the problem for you.**
> Since **Java 14** (JEP 358, on by default from Java 15), a JVM-generated
> `NullPointerException` carries a *helpful* message identifying exactly
> what was null. Confirmed on a current JDK, this exact program prints:
> ```text
> Exception in thread "main" java.lang.NullPointerException: Cannot throw exception because "Test.e" is null
>         at Test.main(Test.java:4)
> ```
> instead of a bare `java.lang.NullPointerException` with no message. Same
> exception, same rule Sir is teaching — the diagnosis is just no longer a
> guessing game.

## 33:16 — Case 2: nothing may follow `throw` directly

### 33:37 — Program A: `10 / 0` then `"Hello"` — compiles

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10 / 0);
        System.out.println("Hello");
    }
}
// Exception in thread "main" java.lang.ArithmeticException: / by zero
//         at Test.main(Test.java:3)
```

`"Hello"` never actually prints, but the compiler has no way to know that —
`10 / 0` looks like an ordinary expression to it. The code compiles; the
failure to reach `"Hello"` is purely a runtime fact.

### 34:11 — Program B: `throw` then `"Hello"` — does not compile

```java
class Test {
    public static void main(String[] args) {
        throw new ArithmeticException("division by zero");
        System.out.println("Hello");
        // CE: unreachable statement
    }
}
```

`throw`'s entire job is to raise an exception right there — so, unlike a
plain expression, the compiler *does* know execution can never fall through
to the next statement. That makes the line after `throw` **unreachable**,
and unreachable code is a compile-time error in Java, not a warning.

> **Board:** After a `throw` statement, we are not allowed to write any
> statement directly. Otherwise: compile-time error, unreachable statement.

### 38:27 — Directly vs. indirectly

You cannot write a statement *directly* after `throw` in the same block, but
you can write one *indirectly* — inside a branch that isn't always taken:

```java
class Test {
    public static void main(String[] args) {
        if (args.length == 0) {
            throw new ArithmeticException("division by zero");
        } else {
            System.out.println("Hello");
        }
    }
}
```

`"Hello"` here lives in the `else` branch, not immediately after the
`throw`, so the compiler can't prove it's unreachable — this compiles.

## 41:24 — Case 3: `throw` only accepts throwable types

```java
class Test {
    public static void main(String[] args) {
        throw new Test();
        // CE: incompatible types: Test cannot be converted to Throwable
    }
}
```

Every object is not throwable — only exceptions and errors are. `Test`
extends nothing throwable, so this is a compile-time error. (The exact
wording has moved since Java 6/7 — see the callout below — but the reason
is unchanged: `throw` demands a `Throwable`.)

### 44:18 — Make `Test` throwable: `extends RuntimeException`

```java
class Test extends RuntimeException {
    public static void main(String[] args) {
        throw new Test();
    }
}
// Exception in thread "main" Test
//         at Test.main(Test.java:3)
```

Once `Test` extends `RuntimeException`, it *is* a throwable type, and
`throw new Test()` is perfectly valid — no syntax error. The default
handler prints the exception's own name, `Test`, because that's what the
class is called. This `extends RuntimeException` shape is exactly how the
course later teaches you to define your own exceptions (Video 077).

> ❗ **Correction — the compiler's wording for the CE has changed.**
> Older javac (the era this lecture was recorded in) reported this failure
> as a two-line `found: Test` / `required: java.lang.Throwable` message.
> Compiling the same code on a current JDK (tested here) instead prints a
> single line: `incompatible types: Test cannot be converted to Throwable`.
> Same defect, same root cause — don't be thrown by the different phrasing
> if your compiler's message doesn't match Sir's board text word for word.

### 46:50 — Case 3 board dictation

> We can use the `throw` keyword only for throwable types. If we try to use
> it for a normal Java object, we get a compile-time error saying
> incompatible types.

## 49:58 — Close: throw only

Sir stops at `throw` — no comparison with `throws`, no `public void m1()
throws Exception` in this video. `throws` is Video 076.

---

## Exam and interview points

1. **The purpose of `throw`:** to hand over a created exception object to
   the JVM manually, in place of the JVM/method creating and handing it
   over internally. Same eventual console output either way.
2. **Best use of `throw` is customized/user-defined exceptions** — the ATM
   `InsufficientFundsException` and recharge `InvalidPinException` examples
   are the two to reproduce on demand. `throw` for predefined exceptions
   like `ArithmeticException` is legal but not the point of the feature.
3. **`throw e;` on a null reference → `NullPointerException`, not whatever
   type `e` declares.** The compiler only checks that `e`'s declared type is
   throwable; it never checks whether an object actually exists behind it.
4. **A stack trace is captured at construction time, not at `throw` time.**
   If the exception object is built inside a static field initializer, the
   trace reads `at ClassName.<clinit>`, not the method that threw it — a
   detail worth having ready if an interviewer pushes on "where exactly
   does the stack trace point."
5. **No statement may follow `throw` directly in the same block** — that's
   a compile-time "unreachable statement" error, not a runtime concern. It
   is still legal indirectly, e.g. inside an `if`/`else` where the `throw`
   is only one of the branches.
6. **`throw` only accepts throwable types** — plain classes fail to compile
   with an "incompatible types" error until they `extends
   Exception`/`RuntimeException`/`Error` (directly or transitively).
7. **Since Java 14, a JVM-thrown `NullPointerException` names the null
   reference in its message** (`Cannot throw exception because "Test.e" is
   null`) — the mechanism from Case 1 is a good concrete example to keep
   for that topic.
8. This video's title mentions `throws`, but the lecture itself only
   reaches `throw` — don't expect a `throws` explanation until Video 076.

---

**Next:** Video 076 — throws keyword
