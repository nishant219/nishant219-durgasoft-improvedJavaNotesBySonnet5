# Video 076 — throws keyword

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-6 || throws keyword

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 76 of 203 |
| Series | Exception Handling · Part 6 |
| Topic | throws keyword |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 39m 31s |
| Video ID | ogOy-dU8AmY |
| Watch | https://www.youtube.com/watch?v=ogOy-dU8AmY |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

He opens by promising the **difference between `throw` and `throws`** "at
last." He never delivers that comparison in these 99 minutes — this video is
`throws` only:

1. Two worked examples (`PrintWriter`, `Thread.sleep`) that show *why* the
   compiler forces a choice between handling and delegating a checked
   exception.
2. The purpose of `throws` — delegate responsibility to the caller — and
   three conclusions that follow from it.
3. A three-method delegation chain (`main` → `doStuff` → `doMoreStuff`) that
   shows `throws` must be repeated at **every** level, not just the top.
4. Four "cases," the last two flagged as the dangerous ones: `throws` on
   class vs. constructor vs. method; `throws` for throwable vs. normal
   types; `throw new Exception()` vs. `throw new Error()`; and catching a
   fully checked exception type a `try` block can never actually raise.

### 00:06 — Last session was `throw`; this session is `throws`

Last session covered **`throw`**. This session is **`throws`** — the most
valuable concept of this part, he says. A student asks for the difference
between `throw` and `throws` right away; he defers it to the end (and, per
Video 075's notes, never actually reaches it there either). First: the
**purpose** of `throws`, which is easy once you already know checked vs.
unchecked exceptions.

### 01:18 — Example 1: writing "hello" to `abc.txt`

Class `Test`, `public static void main(String[] args)`. Create a
`PrintWriter` for file `abc.txt` and write `"hello"`. `PrintWriter` lives in
`java.io`; Sir adds the import so nobody blames a missing import for the
failure.

```java
import java.io.PrintWriter;

class Test {
    public static void main(String[] args) {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
        // CE: unreported exception java.io.FileNotFoundException;
        //     must be caught or declared to be thrown
    }
}
```

### 02:10 — Ask the compiler: valid or invalid?

Asking the compiler to compile this, it refuses: you're writing `"hello"` to
`abc.txt`, and at runtime that file **may not be available**. There is a
**possibility** of `FileNotFoundException`, which is a **checked**
exception. Possibility, not certainty — and possibility is enough. **In our
program, if there is a possibility of raising a checked exception, then
compulsorily we should handle that checked exception. Otherwise we get a
compile-time error saying:**

```text
unreported exception XXX must be caught or declared to be thrown
```

### 03:22 — "Must be caught or declared to be thrown"

The phrase splits into its two halves right here: **"must be caught"** means
try-catch; **"declared to be thrown"** means `throws`. That phrase *is* the
compile-time error, verbatim, and it recurs for the rest of the video.

### 04:39 — Live `javac Test.java` for example 1

```java
import java.io.PrintWriter;

class Test {
    public static void main(String[] args) {
        PrintWriter pw = new PrintWriter("abc.txt"); // CE here
        pw.println("hello");
    }
}
// javac Test.java
// unreported exception java.io.FileNotFoundException
// must be caught or declared to be thrown
```

Same rule: a possibility of a checked exception, unhandled, is a
compile-time error — full stop. Example one, done.

### 08:53 — Example 2: `Thread.sleep(10000)`

Same shape of problem, no import required (`java.lang`):

```java
class Test {
    public static void main(String[] args) {
        Thread.sleep(10000);
        // CE: unreported exception java.lang.InterruptedException
        //     must be caught or declared to be thrown
    }
}
```

Whenever `sleep` is called, the calling thread may enter the sleeping state;
while sleeping, another thread may **interrupt** it — hence a possibility of
`InterruptedException`, which is checked.

### 13:08 — The compiler's own message hands you two solutions

The message itself spells out both fixes:

| Half of the message | Meaning | How to satisfy it |
|---|---|---|
| "must be **caught**" | handle it yourself | **try-catch** |
| "or declared to be **thrown**" | pass it on | **`throws`** |

### 14:20 — First way: try-catch (compiler checks only that catch exists)

```java
class Test {
    public static void main(String[] args) {
        try {
            Thread.sleep(10000);
        } catch (InterruptedException e) {
            // empty catch is enough for the compiler
        }
    }
}
// compiles; runs; sleeps ~10 seconds; then ends
```

The compiler's responsibility ends at **whether you wrote a catch block at
all**. What's inside it — even nothing — is not the compiler's concern; it
only enforces syntax, not effort.

### 17:24 — Second way: `throws` keyword

The purpose still hasn't been explained — that's next.

### 18:00 — Assignment analogy: do it yourself vs. delegate to a friend

Given a homework assignment, you have two options: do it yourself, or
delegate it to a friend. Same for a checked exception:

- Handle it **on your own** → **try-catch**.
- "Boss, I don't want to handle this — my **caller** will take care of it" →
  **`throws`**.

### 19:16 — Purpose: delegate responsibility of exception handling to the caller

`throws` delegates responsibility of exception handling **to the caller** —
which may be **JVM** or **another method**. `main` uses `throws
InterruptedException` to tell the compiler "ask my caller." The caller of
`main` is the **JVM**, which can handle it — so the code compiles.

```java
class Test {
    public static void main(String[] args) throws InterruptedException {
        Thread.sleep(10000);
    }
}
// compiles: main delegated InterruptedException to JVM
```

### 23:19 — Spell it out: `throws InterruptedException`, not `throws I`

Sir's aside: write the full exception name, don't abbreviate to a single
`I` on the board — read aloud, that sounds like "Internet Explorer," not
`InterruptedException`. A small joke, but the underlying advice (spell out
the full type) is real.

### 24:18 — Three conclusions about `throws`

**Conclusion 1 — purpose:** delegate responsibility of exception handling to
the caller (a method or the JVM).

**Conclusion 2 — checked only:** `throws` is required **only for checked
exceptions**. For **unchecked** exceptions it is meaningless — legal to
write, but with **no impact**, because the compiler's "unreported
exception…" objection is only ever raised for checked exceptions:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10 / 0);
        // compiles: ArithmeticException is unchecked
        // RE: Exception in thread "main" java.lang.ArithmeticException: / by zero
    }
}
```

```java
class Test {
    public static void main(String[] args) throws ArithmeticException {
        System.out.println(10 / 0);
        // still compiles — throws on unchecked has no impact
        // still RE: ArithmeticException: / by zero
    }
}
```

### 25:36 — Conclusion 3: only to convince the compiler

Without `throws`, CE; with it, no CE. So `throws` exists **only to convince
the compiler**. If the declared exception really does occur at runtime, the
JVM is the one left holding it — and JVM handling means **abnormal
termination**. Using `throws` does **not** prevent that: every `throws`
chain ends somewhere, and if it really fires, that "somewhere" terminates
the program abnormally regardless. That is why **try-catch is recommended
over `throws`**: try-catch gives normal termination if the exception
occurs; `throws` still ends in abnormal termination if it does.

```java
class Test {
    public static void main(String[] args) throws InterruptedException {
        Thread.sleep(10000);
        // compiles (compiler is convinced)
        // if InterruptedException really occurs at runtime:
        //   JVM default handler → abnormal termination
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        try {
            Thread.sleep(10000);
        } catch (InterruptedException e) {
            // handled here → if it occurs, still normal termination
        }
    }
}
```

### 30:05 — Big picture: impact of `throws` across three methods

`main` calls `doStuff`; `doStuff` calls `doMoreStuff`; `doMoreStuff` calls
`Thread.sleep(10000)`. Ask the compiler: will this compile?

```java
class Test {
    public static void main(String[] args) {
        doStuff();
    }
    public static void doStuff() {
        doMoreStuff();
    }
    public static void doMoreStuff() {
        Thread.sleep(10000);
        // CE: unreported exception java.lang.InterruptedException
        //     must be caught or declared to be thrown
    }
}
```

**No.** The compiler stops at `doMoreStuff`, where the possibility of
`InterruptedException` first appears.

### 32:52 — `doMoreStuff` delegates; the CE moves up to `doStuff`

```java
class Test {
    public static void main(String[] args) {
        doStuff();
    }
    public static void doStuff() {
        doMoreStuff();
        // CE: unreported exception java.lang.InterruptedException
        //     must be caught or declared to be thrown
    }
    public static void doMoreStuff() throws InterruptedException {
        Thread.sleep(10000);
    }
}
```

Once `doMoreStuff` declares `throws`, the compiler asks its caller —
`doStuff` — the same question: where are you handling this? The CE simply
relocates.

### 34:10 — `doStuff` delegates too; the CE moves up again, to `main`

```java
class Test {
    public static void main(String[] args) {
        doStuff();
        // CE: unreported exception java.lang.InterruptedException
        //     must be caught or declared to be thrown
    }
    public static void doStuff() throws InterruptedException {
        doMoreStuff();
    }
    public static void doMoreStuff() throws InterruptedException {
        Thread.sleep(10000);
    }
}
```

### 35:04 — `main` delegates too; caller of `main` is the JVM — compiles

```java
class Test {
    public static void main(String[] args) throws InterruptedException {
        doStuff();
    }
    public static void doStuff() throws InterruptedException {
        doMoreStuff();
    }
    public static void doMoreStuff() throws InterruptedException {
        Thread.sleep(10000);
    }
}
// compiles: three-level delegation, last caller = JVM
// runs; sleeps ~10s; ends normally (IE never actually occurs — only one thread)
```

**Different levels of delegation:** `doMoreStuff` → `doStuff` → `main` →
**JVM**. That is the purpose of `throws` in full: delegate, and the caller
becomes responsible.

### 36:01 — Live coding: CE at line 13, with none of the three methods delegating

```java
class Test {                                          // 1
    public static void main(String[] args) {          // 2
        doStuff();                                    // 5
    }                                                 // 6
    public static void doStuff() {                    // 7
        doMoreStuff();                                // 9
    }                                                 // 10
    public static void doMoreStuff() {                // 11
        Thread.sleep(10000);                          // 13  CE here first
    }
}
```

### 37:10 — `doMoreStuff throws InterruptedException` → CE moves to line 9

```java
class Test {
    public static void main(String[] args) {
        doStuff();
    }
    public static void doStuff() {
        doMoreStuff(); // CE at line 9
    }
    public static void doMoreStuff() throws InterruptedException {
        Thread.sleep(10000);
    }
}
```

### 37:44 — `doStuff throws` too → CE moves to line 5 (`main`'s call)

```java
class Test {
    public static void main(String[] args) {
        doStuff(); // CE at line 5
    }
    public static void doStuff() throws InterruptedException {
        doMoreStuff();
    }
    public static void doMoreStuff() throws InterruptedException {
        Thread.sleep(10000);
    }
}
```

### 38:18 — `main throws` too: compiles; sleeps 10 seconds; no real interrupt

For `main` also declaring `throws InterruptedException`: compiles cleanly.
At runtime the possibility never becomes real — there is only one thread in
this program, so nothing can interrupt it — but the compiler only needed
the *possibility* handled, and now every level has.

### 42:05 — Trap: `throws` only on `main`, not on the two methods beneath it

```java
class Test {
    public static void main(String[] args) throws InterruptedException {
        doStuff();
    }
    public static void doStuff() {
        doMoreStuff();
    }
    public static void doMoreStuff() {
        Thread.sleep(10000);
        // CE: unreported exception java.lang.InterruptedException
        //     must be caught or declared to be thrown
    }
}
```

### 43:19 — Compiler: "main *can* handle it — but has anyone delegated to main?"

The natural objection: "my `main` method already throws — check again."
The compiler's answer is the whole point of this trap: **I saw that main
*can* handle it — but has it been *delegated* to main?** Without delegation
at every intermediate level, `main` never gets asked. The CE stays exactly
where it was, still inside `doMoreStuff`.

### 45:10 — Delegating one level at a time still isn't enough

```java
class Test {
    public static void main(String[] args) throws InterruptedException {
        doStuff();
    }
    public static void doStuff() {
        doMoreStuff(); // CE: unreported exception InterruptedException
    }
    public static void doMoreStuff() throws InterruptedException {
        Thread.sleep(10000);
    }
}
```

`doMoreStuff` delegated to `doStuff` — but `doStuff` didn't relay it further,
so the CE now sits at `doStuff`'s call to `doMoreStuff()`. `doStuff`
protests that `main` is already handling it; the compiler's reply is the
same as before — not delegated, not asked.

### 46:17 — Only once every level delegates does it compile

```java
class Test {
    public static void main(String[] args) throws InterruptedException {
        doStuff();
    }
    public static void doStuff() throws InterruptedException {
        doMoreStuff();
    }
    public static void doMoreStuff() throws InterruptedException {
        Thread.sleep(10000);
    }
}
// compiles
```

**Board rule:** in a call chain, if we remove **at least one** `throws`
along the chain, the code stops compiling.

### 47:30 — Doubt: "In my apps only `main throws` and it works — why not here?"

Because those apps have **only one method**: `main`. With one method,
`throws` on it is enough — there's no chain to walk. The moment `main`
calls `m1`, which calls `m2`, the same chain rule kicks in: **every level**
must delegate.

```java
class Test {
    public static void main(String[] args) throws Exception {
        m1();
    }
    public static void m1() throws Exception {
        m2();
    }
    public static void m2() throws Exception {
        Thread.sleep(10000);
    }
}
// compiles: every level delegated
```

### 49:22 — Board summary: the three conclusions, restated

1. **Delegate** responsibility of exception handling to the caller (a
   method or the JVM).
2. Required **only for checked** exceptions; for unchecked, **no impact**.
3. Exists **only to convince the compiler**; does **not** prevent
   **abnormal termination**. **Try-catch is recommended over `throws`.**

> ⚠️ **Modern Java — a functional-interface caller often can't accept the
> delegation.**
> The whole "delegate to the caller" model assumes the caller is a method
> you also control, or the JVM. Since **Java 8**, a very common caller is a
> **lambda body** matched to a standard functional interface (`Runnable`,
> `Consumer`, `Function`, the `Stream` pipeline methods) — and none of
> those interfaces declare any checked exception on their abstract method.
> `throws` has nowhere to go:
> ```java
> Runnable r = () -> {
>     Thread.sleep(1000);
>     // CE: unreported exception InterruptedException;
>     //     must be caught or declared to be thrown
>     // — Runnable.run() declares no throws clause to delegate to
> };
> ```
> Verified: `javac` rejects this exactly as shown. The two standard
> workarounds — wrap the checked exception in an unchecked one (`throw new
> RuntimeException(e)`), or catch it inside the lambda body — both amount
> to the same lesson Sir teaches here: when you can't delegate any further,
> you're back to try-catch.

### 56:40 — Case 1: `throws` on class vs. constructor vs. method

```java
class Test throws Exception {          // CE: '{' expected — throws has no
                                        //     place in a class declaration
    Test() throws Exception {          // valid: constructor may declare throws
    }
    public void m1() throws Exception { // valid: method may declare throws
    }
}
```

`throws` is legal on **methods and constructors**, because both can be
**called** — and the caller of a call is exactly who `throws` delegates to.
A **class** cannot be called; only its members can. That's why `throws` at
class level makes no sense and doesn't even parse.

```java
class Test {
    Test() throws Exception {
    }
    public static void main(String[] args) {
        new Test();
        // CE: unreported exception java.lang.Exception
        //     must be caught or declared to be thrown
        // (constructor declared throws; caller of new Test() must handle)
    }
}
```

**Board rule:** `throws` is usable for methods and constructors, but not
for classes.

### 59:55 — Case 2: `throws Test`, where `Test` is a normal class

```java
class Test {
    public void m1() throws Test {
        // CE: incompatible types
        //     found    : Test
        //     required : java.lang.Throwable
    }
}
```

**Invalid — `throws` applies only to throwable types.** `Test` here is a
plain Java class, unrelated to `Throwable`, so the compiler rejects it
outright.

### 1:01:40 — Same method, `Test extends RuntimeException`

```java
class Test extends RuntimeException {
    public void m1() throws Test {
        // valid: Test is a throwable type (unchecked, but still Throwable)
    }
}
```

**Valid**, because `Test` is now under `Throwable` — checked or unchecked
doesn't matter for this rule; only "is it a `Throwable`" does.

> ❗ **Correction — the compiler's wording for this CE has changed.**
> Older javac (the era this lecture was recorded in) reported this failure
> as a two-line `found: Test` / `required: java.lang.Throwable` message.
> Compiling the same code on a current JDK (verified here, JDK 26) instead
> prints a single line: `incompatible types: Test cannot be converted to
> Throwable`. Same defect, same root cause — `throws` still demands a
> `Throwable` — only the diagnostic's phrasing changed. Don't be thrown if
> your own terminal's message doesn't match Sir's board text word for word.

**Board rule:** `throws` works only for throwable types; for normal Java
classes it fails with `incompatible types`.

### 1:06:11 — Case 3 intro: the two "dangerous" cases

Sir's memory hook here is a Telugu-cinema analogy: after a blockbuster like
*Pokiri* put Mahesh Babu at number one, expectations for whatever came next
were sky-high, and nobody could actually predict how it would land. Same
warning for these last two cases — they're the ones you genuinely cannot
guess your way through; take extra care.

### 1:08:27 — Case 3: `throw new Exception()` vs. `throw new Error()`

```java
class Test {
    public static void main(String[] args) {
        throw new Exception();
        // CE: unreported exception java.lang.Exception
        //     must be caught or declared to be thrown
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        throw new Error();
        // compiles (Error is unchecked)
        // RE: Exception in thread "main" java.lang.Error
        //     at Test.main(...)
    }
}
```

Only **one** of these fails to compile. The reasoning is the same rule from
the top of the video: a possibility of a **checked** exception must be
handled or declared, or it's a CE. `Exception` is checked, so `throw new
Exception()` alone in `main` is a compile-time error. `Error` is
**unchecked** — the compiler never objects to it, so `throw new Error()`
compiles cleanly; the failure only shows up at runtime, as an uncaught
error printed by the JVM's default handler.

```java
class Test {
    public static void main(String[] args) throws Exception {
        throw new Exception();
        // compiles; then JVM → abnormal termination if it actually throws
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        try {
            throw new Exception();
        } catch (Exception e) {
        }
        // compiles; handled → normal termination
    }
}
```

**Board rule:** `throw new Exception()` (checked) → compile-time error.
`throw new Error()` (unchecked) → compiles, then runtime error.

### 1:17:52 — Case 4: five `try`/`catch` programs — the "most dangerous" concept

Five programs, each `try { System.out.println("hello"); } catch (SomeType
e) { }` — the `try` body never actually raises anything. Which catches are
legal?

```java
class Test {
    public static void main(String[] args) {
        try {
            System.out.println("hello");
        } catch (ArithmeticException e) {
        }
    }
}
// compiles; prints hello
```

```java
class Test {
    public static void main(String[] args) {
        try {
            System.out.println("hello");
        } catch (Exception e) {
        }
    }
}
// compiles; prints hello
```

```java
import java.io.IOException;

class Test {
    public static void main(String[] args) {
        try {
            System.out.println("hello");
        } catch (IOException e) {
        }
        // CE: exception java.io.IOException is never thrown
        //     in body of corresponding try statement
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        try {
            System.out.println("hello");
        } catch (InterruptedException e) {
        }
        // CE: exception java.lang.InterruptedException is never thrown
        //     in body of corresponding try statement
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        try {
            System.out.println("hello");
        } catch (Error e) {
        }
    }
}
// compiles; prints hello
```

Sir plays a small trick with the room here: he first hints "three of these
are CE, two compile," lets students commit to guesses, then flips it —
"actually, two are CE, three compile" — to see who was really reasoning
through the checked/unchecked split rather than just repeating a hint back.

### 1:25:31 — Answer: 1, 2, and 5 compile; 3 and 4 are CE

| Catch type | Kind (as classified here) | `try` body has no chance of it | Result |
|---|---|---|---|
| `ArithmeticException` | unchecked | yes | compiles, prints `hello` |
| `Exception` | partially checked | yes | compiles, prints `hello` |
| `IOException` | **fully checked** | yes | CE: never thrown in body of try |
| `InterruptedException` | **fully checked** | yes | CE: never thrown in body of try |
| `Error` | unchecked | yes | compiles, prints `hello` |

### 1:26:14 — Why `catch (IOException)` (and `InterruptedException`) fail here

`IOException` only ever arises from an IO operation — `println` isn't one,
so there is **no chance** of it inside this `try`. Writing a catch block
for an exception that can never occur is flagged as dead, unreachable
handling:

```text
exception java.io.IOException is never thrown in body of corresponding try statement
```

Same story for `InterruptedException`: it arises from `sleep`/`wait`/
`join`, none of which appear in the `try`, so the catch is illegal for the
same reason. If the `try` *did* call `sleep`, the same catch becomes valid
(this was the first way, at 14:20):

```java
class Test {
    public static void main(String[] args) {
        try {
            Thread.sleep(10000);
        } catch (InterruptedException e) {
        }
        // compiles: sleep can throw InterruptedException
    }
}
```

### 1:27:59 — This rule applies only to fully checked exceptions

The "never thrown in body of corresponding try statement" CE fires only
for **fully checked** types (`IOException`, `InterruptedException`). It
does **not** apply to:

- **unchecked** types (`ArithmeticException`, `Error`) — always legal to
  catch, thrown or not, because the JVM can raise them at any point anyway.
- **`Exception`**, classified here as **partially checked** — since it's
  also the supertype of every unchecked exception, a `try` block can always
  be said to have "a chance" of it, so the catch is never flagged as dead.

**Board rule:** within a `try`, a catch for a type that block cannot raise
is illegal — *but only when that type is fully checked.*

### 1:32:31 — Live compile of all five, confirmed

All five behave exactly as predicted: `ArithmeticException`, `Exception`,
and `Error` compile and print `hello`; `IOException` and `InterruptedException`
(the two fully checked types, here written as fully qualified names with no
import) both fail with "is never thrown in body of corresponding try
statement."

---

## Exam and interview points

1. **The compiler's own CE spells out both fixes** — "must be **caught**"
   (try-catch) "or declared to be **thrown**" (`throws`). Memorize the exact
   phrase; OCJP quotes it.
2. **`throws` delegates responsibility to the caller** — a method, or the
   JVM if the caller is `main`. It is required only for **checked**
   exceptions; on unchecked exceptions it compiles but changes nothing.
3. **`throws` only convinces the compiler — it never prevents abnormal
   termination.** If the declared exception really occurs at runtime and
   nothing else catches it, the JVM's default handler still terminates the
   program abnormally. That's the stated reason **try-catch is recommended
   over `throws`.**
4. **In a call chain, every level must delegate, not just the outermost
   one.** `throws` on `main` alone does nothing if the methods it calls
   never declare it — the compile-time error tracks back to wherever the
   chain of delegation actually breaks, one call site at a time.
5. **`throws` is legal on methods and constructors, never on a class** — a
   class itself is never called, so there is no caller to delegate to; the
   attempt doesn't even parse.
6. **`throws` requires a throwable type.** `throws SomeNormalClass` is
   `incompatible types`; `throws SomeClass` where `SomeClass extends
   RuntimeException` (or any `Throwable`) is fine — checked vs. unchecked
   doesn't matter for this rule.
7. **`throw new Exception()` (checked) is a compile-time error un-delegated;
   `throw new Error()` (unchecked) always compiles**, and only fails at
   runtime if actually reached. The checked/unchecked split is the entire
   explanation — memorize which family each belongs to.
8. **A `catch` for a type the `try` body cannot raise is illegal — but only
   for fully checked types** (`IOException`, `InterruptedException`).
   Unchecked types and `Exception` (partially checked, since it's also the
   supertype of every `RuntimeException`) are always a legal catch, thrown
   or not.
9. **The `throw` vs. `throws` comparison Sir promises is never delivered**
   in this video (nor, per Video 075's notes, in the one before it) — don't
   go looking for it here.
10. **Lambdas complicate "delegate to the caller."** Since Java 8, a very
    common caller is a functional-interface method (`Runnable.run()`,
    `Consumer.accept()`, a `Stream` operation) — and none of those declare
    checked exceptions, so `throws` inside the lambda has nowhere to go.
    Wrapping in an unchecked exception or catching inline is the modern
    version of "I can't delegate any further."

---

**Next:** Video 077 — Customized exceptions
