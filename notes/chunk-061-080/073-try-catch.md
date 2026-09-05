# Video 073 — Customized exception handling (try-catch)

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-3B|| Customized Exception Haning by try-catch

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 73 of 203 |
| Series | Exception Handling · Part 3B |
| Topic | Customized Exception Handling by try-catch |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 14m 59s |
| Video ID | GljHUIBS9YY |
| Watch | https://www.youtube.com/watch?v=GljHUIBS9YY |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## 00:06 — Why customize exception handling

Up to this video the theory is done: what an exception is, the hierarchy,
checked vs unchecked, partially vs fully checked. From here it's the
**keywords** — `try` and `catch` in this video, `finally` in the next — and
the syntactical loopholes around them.

### 00:44 — Default handling vs customized handling

Default handling was already covered: if nobody handles a problem, the
**default exception handler** takes over and the program is **terminated
abnormally**. Sir doesn't want that, for two reasons:

- we may **miss** something — later statements never run
- we may **waste a resource** — a connection opened and never closed

So we handle the exception **our own way**, using try-catch: **customized
exception handling by using try-catch.** He puts the same short program on the
board twice — without try-catch, then with it.

## 01:51 — Without try-catch: abnormal termination

```java
class Test {
    public static void main(String[] args) {
        System.out.println("statement one");
        System.out.println(10 / 0);
        System.out.println("statement three");
    }
}
// statement one
// Exception in thread "main" java.lang.ArithmeticException: / by zero
//     at Test.main(Test.java:4)
```

`"statement one"` runs, `10 / 0` raises `ArithmeticException`, nobody handles
it, the default handler kills the program — `"statement three"` never runs.
**Abnormal termination. Not recommended.**

### 04:03 — Why that's not graceful: the database cinema

Read the three lines as *open connection → read data → close connection*:

```java
class DbCinema {
    public static void main(String[] args) {
        System.out.println("open database connection");
        System.out.println(10 / 0);   // stand-in for "read data" raising an exception
        System.out.println("close database connection");
    }
}
// open database connection
// then ArithmeticException — abnormal termination, close() never runs
```

The connection opens fine. Reading fails. Nobody closes it — one connection
sits blocked. That's the cost of abnormal termination: you miss work *and*
leak a resource. Not at all recommended.

> ⚠️ **Modern Java — this exact leak has a dedicated fix: try-with-resources.**
> Since **Java 7**, a resource that implements `AutoCloseable` can be declared
> in the `try` itself, and the JVM guarantees `close()` runs even if the body
> throws — no `finally` needed:
>
> ```java
> try (Connection c = DriverManager.getConnection(url)) {
>     read(c);          // if this throws, c.close() still runs
> } catch (SQLException e) {
>     System.out.println("use MySQL DB instead of Oracle DB");
> }
> ```
>
> Sir's fix in this lecture — put the risky read in `try`, handle the
> exception in `catch` — is still exactly right and is why the pattern below
> works. Try-with-resources is the modern refinement for the specific case
> where the risky code owns a resource that must be closed either way.

## 05:06 — The same cinema, with try-catch

Only `System.out.println(10 / 0)` can raise an exception — **the code that may
raise an exception is called risky code, and risky code has to go inside a
try block.** `"statement one"` is not risky, so it stays outside `try`. The
exception it may raise is `ArithmeticException`, so that's the catch
parameter; the catch body performs an alternative arithmetic operation
instead of dying.

```java
class Test {
    public static void main(String[] args) {
        System.out.println("statement one");
        try {
            System.out.println(10 / 0);        // risky code
        } catch (ArithmeticException e) {
            System.out.println(10 / 2);         // alternative arithmetic operation
        }
        System.out.println("statement three");
    }
}
// statement one
// 5
// statement three
```

### 07:28 — Terminology, and the whiskey joke

**Inside `try`:** risky code. Sir's joke while writing it: "whiskey is also
risky, right" — a pun to make "risky" stick, not a claim about the keyword.
**Inside `catch`:** the handling code for the exception type you named.

### 08:27 — Why this is graceful termination

`"statement one"` prints, `10 / 0` raises `ArithmeticException`, control jumps
**immediately** to the matching catch, catch prints `5`, and once catch
finishes, the code *after* the try-catch resumes — `"statement three"` runs.
The exception rose, but nothing was missed: **normal / graceful
termination.**

**It is highly recommended to handle exceptions.** Risky code → `try`.
Corresponding handling code → `catch`.

## 12:01 — Side by side

| Without try-catch | With try-catch |
|---|---|
| abnormal termination | normal termination |
| not recommended | highly recommended, graceful |

```java
class WithoutTryCatch {
    public static void main(String[] args) {
        System.out.println("statement one");
        System.out.println(10 / 0);
        System.out.println("statement three");
    }
}
// statement one, then ArithmeticException — abnormal termination
```

```java
class WithTryCatch {
    public static void main(String[] args) {
        System.out.println("statement one");
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
            System.out.println(10 / 2);
        }
        System.out.println("statement three");
    }
}
// statement one, 5, statement three — normal termination
```

## 15:05 — Control flow in try-catch

The skeleton for the whole next stretch: one `try` with three statements, one
`catch` with statement 4, then statement 5 after the try-catch. For each
case, the question is: **in what order do statements run, and is termination
normal or abnormal?**

```java
class ControlFlow {
    public static void main(String[] args) {
        try {
            // statement 1
            // statement 2
            // statement 3
        } catch (Exception e) {
            // statement 4
        }
        // statement 5
    }
}
```

### 16:53 — Case 1: no exception → 1, 2, 3, 5 (normal)

If nothing goes wrong, `catch` never runs.

```java
class Case1 {
    public static void main(String[] args) {
        try {
            System.out.println("1");
            System.out.println("2");
            System.out.println("3");
        } catch (Exception e) {
            System.out.println("4");
        }
        System.out.println("5");
    }
}
// 1
// 2
// 3
// 5
```

### 17:48 — Case 2: exception at statement 2, catch matches → 1, 4, 5

```java
class Case2 {
    public static void main(String[] args) {
        try {
            System.out.println("1");
            System.out.println(10 / 0);    // statement 2 — ArithmeticException
            System.out.println("3");
        } catch (Exception e) {            // matched
            System.out.println("4");
        }
        System.out.println("5");
    }
}
// 1
// 4
// 5
```

Statement 3 does **not** run, even though the exception was handled: **within
a try block, once an exception rises anywhere, control goes to the matching
catch and never returns to try.** Catch is the alternative to the rest of
try, not a resumption point.

### 19:11 — Corollary: keep try as short as possible

Because the rest of `try` is dead the moment an exception fires partway
through, `try` should contain **only risky code**, and as little of it as
possible. In the very first `Test` example, only `System.out.println(10 / 0)`
went inside `try` — `"statement one"` and `"statement three"` never can fail
on their own, so they stayed outside.

### 20:30 — Anti-pattern: one `try` around the whole `main`

```java
class WholeMainInTry {
    public static void main(String[] args) {
        try {
            System.out.println("line 1");
            // ... imagine 9,999 more lines of mixed normal + risky code ...
            System.out.println("line 10000");
        } catch (Exception e) {
        }
    }
}
```

If line 1 already throws, none of the other 9,999 lines run. Wrapping
everything in one giant `try` throws away exactly the control you're trying
to get. **Don't put normal code inside try. Keep try as short as possible.**

### 21:32 — Several risky areas → several try-catch blocks

If a program has three independent risky spots, don't enclose all three in
one `try` — a failure in the first would skip the other two entirely. Give
each its own try-catch:

```java
class ThreeRiskyAreas {
    public static void main(String[] args) {
        // normal code
        try {
            // risky area 1
        } catch (Exception e) {
            // handling for area 1
        }
        // normal code
        try {
            // risky area 2
        } catch (Exception e) {
            // handling for area 2
        }
        // normal code
        try {
            // risky area 3
        } catch (Exception e) {
            // handling for area 3
        }
    }
}
```

### 23:26 — Case 3: exception at statement 2, catch does **not** match

```java
class Case3 {
    public static void main(String[] args) {
        try {
            System.out.println("1");
            System.out.println(10 / 0);         // statement 2 — ArithmeticException
            System.out.println("3");
        } catch (NullPointerException e) {      // not matched
            System.out.println("4");
        }
        System.out.println("5");
    }
}
// 1
// then default handler: ArithmeticException: / by zero — abnormal termination
```

Statement 1 runs; there's no matching catch for `ArithmeticException`, so the
default handler takes over. **1, then abnormal termination** — 3, 4, and 5
never run.

### 24:38 — Exceptions aren't only raised inside `try`

Most people assume exceptions can only rise inside `try`. They can also rise
inside `catch` and `finally` — those are Java code too. Sir's cinema: a
problem hits Oracle inside `try`; the `catch` handles it by falling back to
MySQL — but MySQL has no guarantee of working either, so the *catch body*
can raise its own exception.

### 26:01 — Thumb rule: outside `try` is always abnormal

**Any statement that raises an exception and is not part of a `try` block
always ends in abnormal termination** — there is no catch that could ever be
matched against it, because it was never offered to one.

```java
class CaseStatement4 {
    public static void main(String[] args) {
        try {
            System.out.println("1");
            System.out.println(10 / 0);    // needed so catch runs
            System.out.println("3");
        } catch (Exception e) {
            System.out.println(10 / 0);    // statement 4 — not inside a try
        }
        System.out.println("5");
    }
}
// 1
// then ArithmeticException thrown from inside the catch body — abnormal termination
```

```java
class CaseStatement5 {
    public static void main(String[] args) {
        try {
            System.out.println("1");
            System.out.println("2");
            System.out.println("3");
        } catch (Exception e) {
            System.out.println("4");
        }
        System.out.println(10 / 0);        // statement 5 — not inside a try
    }
}
// 1
// 2
// 3
// then ArithmeticException at statement 5 — abnormal termination
```

An exception at statement 4 or 5 is **always** abnormal, because neither
statement is inside any `try`.

### 28:25 — Notes, as dictated

1. Within `try`, once an exception rises anywhere, the rest of `try` never
   runs — even after a successful catch. So `try` should hold only risky
   code, kept as short as possible.
2. `catch` and `finally` can raise exceptions too — don't assume exceptions
   only happen inside `try`.
3. Any statement outside every `try` that raises an exception is always
   abnormal termination.

## 33:13 — Methods to print exception information

Three methods answer "what exactly went wrong," each giving a different
amount of detail: `printStackTrace()`, `toString()`, `getMessage()`.

### 34:10 — Demo skeleton

```java
class Test {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
            e.printStackTrace();
            // System.out.println(e);
            // System.out.println(e.toString());
            // System.out.println(e.getMessage());
        }
    }
}
```

`System.out.println(e)` and `System.out.println(e.toString())` are
**identical** — printing an object reference internally calls `toString()`.

### 36:18 — What each one prints

Using this exception: name `java.lang.ArithmeticException`, description
`division by zero` (JVM text: `/ by zero`), location `Test.main`.

| Method | Printable format |
|---|---|
| `printStackTrace()` | name : description, then the full stack trace |
| `toString()` (or `System.out.println(e)`) | name : description only |
| `getMessage()` | description only |

### 38:54 — Compiled and run, one at a time

```java
class PrintStackTraceDemo {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
            e.printStackTrace();
        }
    }
}
// java.lang.ArithmeticException: / by zero
//     at PrintStackTraceDemo.main(PrintStackTraceDemo.java:4)
```

```java
class ToStringDemo {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
            System.out.println(e);          // same as System.out.println(e.toString())
        }
    }
}
// java.lang.ArithmeticException: / by zero
```

```java
class GetMessageDemo {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
            System.out.println(e.getMessage());
        }
    }
}
// / by zero
```

### 40:35 — Why all three work on any exception or error

These three methods are declared on **`Throwable`**, the common parent of
both `Exception` and `Error` — so every exception object and every error
object can call all three.

### 47:33 — The default handler uses `printStackTrace()` internally

The console dump you get with no `try` at all has exactly the
`printStackTrace()` shape — name, colon, description, stack trace. That's
because **the default exception handler internally calls
`printStackTrace()`** to print to the console.

## 48:49 — Try with multiple catch blocks

Sir's analogy: answering every question — name, qualification, native place —
with "my name is Durga" is meaningless; you'd wonder if the speaker needs
help. **The answer should match the question.** Giving the same response to
every exception type is the programming equivalent.

### 51:01 — Handling varies from exception to exception

Because the right response to `ArithmeticException` is not the right response
to `SQLException`, it's recommended to give **every exception type its own
catch block.**

### 51:18 — Worst practice: one `catch (Exception e)` for everything

```java
class WorstPractice {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);   // risky code
        } catch (Exception e) {
            // same handling regardless of whether it's ArithmeticException,
            // IOException, SQLException, ...
        }
    }
}
```

One catch that can swallow *any* exception with the same response is the
**worst kind of programming practice** — the handling can't possibly be
right for all of them at once.

### 52:29 — Best practice: one catch per type, `Exception` last

```java
import java.io.FileNotFoundException;
import java.sql.SQLException;

class BestPractice {
    public static void main(String[] args) {
        try {
            risky();
        } catch (ArithmeticException e) {
            System.out.println("perform alternative arithmetic operations");
        } catch (SQLException e) {
            System.out.println("use MySQL DB instead of Oracle DB");
        } catch (FileNotFoundException e) {
            System.out.println("use local file instead of remote file");
        } catch (Exception e) {
            System.out.println("default exception handling");   // last — worst-case default
        }
    }

    static void risky() throws SQLException, FileNotFoundException {
        System.out.println(10 / 0);
    }
}
// perform alternative arithmetic operations
```

Each catch's meaning as Sir wrote it: `ArithmeticException` → try an
alternative arithmetic operation; `SQLException` → fall back to MySQL instead
of Oracle; `FileNotFoundException` → fall back to a local file instead of a
remote one; `Exception` at the end → a generic default for whatever's left,
the "worst choice" used only as a catch-all. **Multiple specific catches is
good programming practice** because the handling genuinely varies.

> ⚠️ **Modern Java — merge catches with `|`, when the handling is identical.**
> Since **Java 7**, unrelated exception types that need the *same* handling
> can share one catch block with a pipe:
>
> ```java
> catch (SQLException | FileNotFoundException e) {
>     System.out.println("use a fallback data source");
> }
> ```
>
> This doesn't contradict Sir's lesson — it's the opposite case. He's arguing
> *against* one catch when the handling differs; multi-catch is *for* the
> case where two types genuinely get the same response, so you don't repeat
> the body. The multi-catch variable is implicitly final and its static type
> is the lowest common supertype of the listed exceptions.

### 55:34 — Why bother with several catches if only one exception can rise?

At any moment, `try` can raise at most **one** exception — but we usually
don't know *which* one in advance. If we knew for certain it would be
`ArithmeticException`, one catch would be enough. Since we don't, we cover
every exception the risky code can plausibly throw.

### 58:03 — Both patterns, side by side

| Single `catch (Exception e)` | Multiple specific catches |
|---|---|
| worst programming practice | best programming practice |
| same response for every exception type | response matches each exception type |

## 1:00:51 — Loophole 1: order of catch blocks matters

Two syntaxes, and the question is **valid or invalid**, not recommended or
not:

```java
class ParentThenChild {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (Exception e) {
        } catch (ArithmeticException e) {
        }
    }
}
// CE: exception ArithmeticException has already been caught
```

```java
class ChildThenParent {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
        } catch (Exception e) {
        }
    }
}
// compiles and runs — ArithmeticException is handled by the first catch
```

Verified against a current `javac`: parent-then-child is rejected with
`error: exception ArithmeticException has already been caught`; child-then-parent
compiles and runs clean.

### 1:03:18 — Why parent-then-child is a compile error

The JVM checks catch blocks **top to bottom**. If `NullPointerException`
rises, the first catch (`Exception`) can handle it — done. If
`ArithmeticException` rises, the first catch (`Exception`) can *also* handle
it, since every exception is an `Exception`. The second catch
(`ArithmeticException`) can then never be reached — dead code the compiler
refuses to accept, and it says so: `exception ArithmeticException has
already been caught`.

### 1:05:21 — Why child-then-parent works

With `ArithmeticException` first and `Exception` second: an arithmetic
exception matches the first catch; anything else falls through to the
second. Both blocks get a real chance to run. **Rule: child before parent.
Parent before child is a compile-time error.**

### 1:08:27 — Confirmed by compiling both orders

Typing `catch (Exception e)` then `catch (ArithmeticException e)` fails with
the exact message above. Swapping the order compiles cleanly. **Order of
multiple catch blocks: most specific (child) first, most general (parent)
last — never the reverse.**

## 1:11:07 — Loophole 2: two catches for the same exception type

```java
class DuplicateCatch {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
        } catch (ArithmeticException e) {
        }
    }
}
// CE: exception ArithmeticException has already been caught
```

Same rule, same message: if `ArithmeticException` rises, the first catch
handles it, so the second catch is unreachable — the compiler rejects it for
the identical reason as loophole 1. **You cannot declare two catch blocks for
the same exception type.**

### 1:14:45 — Close

That closes try with multiple catch blocks. `finally` is next.

---

## Exam and interview points

1. **Risky code goes in `try`, its handling in `catch`.** Without try-catch,
   an unhandled exception is always abnormal termination; with it, a matched
   catch gives normal/graceful termination.
2. **Once an exception fires inside `try`, the rest of `try` is skipped for
   good** — control goes to the matching catch and never returns to `try`,
   even after the catch completes successfully. Corollary: keep `try` short,
   holding only the lines that can actually fail.
3. **Never wrap unrelated risky areas in one `try`.** A failure in the first
   skips every later risky area in the same block; give each its own
   try-catch.
4. **Exceptions can be raised inside `catch` and `finally`, not only `try`** —
   they're ordinary Java code. Any statement that raises an exception outside
   every `try` is *always* abnormal termination, with no possible match.
5. **Three `Throwable` printers, from most to least detail:**
   `printStackTrace()` (name : description + full stack), `toString()` /
   `System.out.println(e)` (name : description), `getMessage()` (description
   only). The JVM's own default handler is built on `printStackTrace()`.
6. **Multiple catch blocks are recommended, not just allowed** — handling
   genuinely varies by exception type, so a single `catch (Exception e)` that
   does the same thing for everything is the worst practice on the exam.
7. **Catch order is child-to-parent, always.** `catch(Exception)` before
   `catch(ArithmeticException)` is a compile-time error —
   `exception ArithmeticException has already been caught` — because the
   parent catch would make the child catch unreachable. The same error fires
   for two catch blocks on the identical exception type.
8. **Multi-catch (`catch (A | B e)`, Java 7)** is for the case Sir isn't
   arguing against: two types that need the *same* handling. It doesn't
   replace multiple specific catches when the handling differs.
9. **Try-with-resources (Java 7)** closes an `AutoCloseable` resource
   automatically, even when the try body throws — the modern fix for the
   exact "connection opened, exception raised, connection never closed"
   scenario in this lecture's database example.

**Next:** Video 074 — the `finally` block
