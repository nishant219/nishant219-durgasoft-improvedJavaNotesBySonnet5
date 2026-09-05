# Video 074 — finally block

## Video info

**Title:** Core Java with OCJP/SCJP: Exception Handling Part-4 || finally block

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 74 of 203 |
| Series | Exception Handling · Part 4 |
| Topic | finally block |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 47m 40s |
| Video ID | 2ui_RS0Q7x4 |
| Watch | https://www.youtube.com/watch?v=2ui_RS0Q7x4 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Exception Handling Part 4, two board topics only:

1. The interview line — the difference between `final`, `finally`, and
   `finalize` — including the garbage-collector "last wish" story, and why
   finally-cleanup is try-block-level while finalize-cleanup is object-level.
2. **25 numbered combinations** of try / catch / finally (he numbers the
   board 1–25 at 38:59), boiled down to six syntax rules.

He does **not** run the four finally control-flow cases (exception raised or
not, handled or not) with print statements in this video, does not show
`System.exit()`, does not compare `return` in try vs. in finally, and does
not touch try-with-resources — that last one is Video 079's job, three
videos later, and is exactly the feature that changes Rule 2 below.

---

### 00:06 — Interview question: `final` vs `finally` vs `finalize`

He opens with the difference between `final`, `finally`, and `finalize`.
Why is this such a valuable question? The three words *look* alike, which is
precisely why interviewers reach for it — a candidate who confuses them
hasn't understood any of the three.

### 00:33 — `final` is a modifier

`final` is a **modifier**, applicable to **classes, methods, and variables**.

- **Class** declared `final` → cannot be extended. Inheritance is not possible.
- **Method** declared `final` → cannot be overridden in a child class.
- **Variable** declared `final` → cannot be reassigned. It becomes a constant
  with a fixed value.

```java
final class P {
}

class C extends P {
    // CE: cannot inherit from final class P
}
```

```java
class P {
    public final void m1() {
    }
}

class C extends P {
    public void m1() {
        // CE: m1() in C cannot override m1() in P
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        final int x = 10;
        x = 20;
        // CE: cannot assign a value to final variable x
    }
}
```

### 04:54 — Second word: `finally`

`finally` is a **block**, always associated with try-catch, purpose: to
maintain **cleanup code**.

| Block | Code it holds |
|---|---|
| `try` | risky code |
| `catch` | handling code |
| `finally` | cleanup code |

```java
class Test {
    public static void main(String[] args) {
        try {
            // risky code
        } catch (Exception e) {
            // handling code
        } finally {
            // cleanup code
        }
    }
}
```

### 07:44 — Speciality of finally (the interview sentence)

The speciality of the finally block: **it will be executed always**,
irrespective of whether an exception is raised or not, and whether it is
handled or not.

> ❗ **Correction — "always" has real exceptions.**
> This is the standard OCJP-level statement and it is fine as a working rule:
> finally *does* run in all four combinations of raised/handled that the exam
> asks about. But "always" is not literally true. `finally` is **skipped**
> when:
>
> - the JVM exits mid-try via `System.exit(...)` (or `Runtime.halt`),
> - the JVM itself crashes or the machine loses power,
> - the thread running the try block is killed (`Thread.stop()` — see the
>   Modern Java note below), or
> - the try block never finishes — an infinite loop, or a `finally` on a
>   *different*, unreached frame.
>
> ```java
> class NoFinally {
>     public static void main(String[] args) {
>         try {
>             System.out.println("in try");
>             System.exit(0);
>         } finally {
>             System.out.println("never printed");
>         }
>     }
> }
> // prints only: in try
> ```
>
> Interviewers who already know the "always" line sometimes ask this exact
> follow-up ("does finally *ever* not run?") specifically to see whether you
> know the boundary. `System.exit()` is the answer they are fishing for.

### 08:50 — Third word: `finalize` is a method

`finalize` is a **method**. The GC story, tightened: an object with no
reference is useless and eligible for garbage collection. Before destroying
it, the garbage collector gives it one "bumper offer" — a last wish. The
object's last wish is to close its open network and database connections.
To grant that wish, the GC calls the object's **`finalize`** method; once
`finalize` completes, the GC destroys the object.

```java
class Test {
    protected void finalize() {
        // last wish: close DB / network associated with THIS object
        // GC calls this just before destroying the object
    }
}
```

**One line:** just before destroying an object, the garbage collector always
calls `finalize` to perform cleanup activities. Once `finalize` completes,
the GC destroys that object.

> ❗ **Correction — "GC always calls finalize before destroying" overstates the guarantee.**
> Two things the story skips:
>
> 1. **`finalize` runs at most once per object**, and only if the object is
>    actually garbage collected. If the JVM exits (normally or via
>    `System.exit`) before GC ever gets to that object, `finalize` is simply
>    never called — there is no promise the JVM will collect everything, or
>    collect it at all, before shutdown.
> 2. Even when GC does run, the JLS never promised *when* `finalize` runs
>    relative to program logic, and a slow or throwing `finalize` can delay
>    or break collection of that object's whole generation.
>
> This unreliability is exactly why the mechanism was deprecated (below) —
> Sir's story is the mental model the exam wants, but "resource cleanup you
> can actually depend on" was never really true of `finalize`.

> ⚠️ **Modern Java — `finalize()` is deprecated and now disabled by default.**
>
> | Version | Status |
> |---|---|
> | Java 6/7 (this lecture) | the only two GC cleanup hooks anyone taught: `finalize()`, or manual close |
> | Java 9 | `Object.finalize()` **deprecated** (JEP-style javadoc warning; `-Xlint:deprecation` reports `[removal]`) |
> | Java 18 | finalization **disabled by default** JVM-wide (JEP 421) — `finalize()` methods no longer run unless you opt back in with `--finalization=enabled` |
> | Future release | scheduled for outright **removal** |
>
> ```text
> warning: [removal] finalize() in Object has been deprecated and marked for removal
> ```
>
> The replacement for "run cleanup when a resource is no longer needed" is
> **try-with-resources** (`AutoCloseable`, Java 7 — Video 079) for
> deterministic cleanup, or `java.lang.ref.Cleaner` (Java 9) when you truly
> need a GC-triggered hook. New code should never override `finalize()`.
> Legacy code that still does keeps working (finalization is merely
> *disabled*, not removed, through at least Java 25) — but this is
> now a "know it existed" answer, not a "write it this way" answer.

### 14:48 — finally-cleanup vs finalize-cleanup: same idea, different level

Both are cleanup, but the **context differs**:

| | Cleans up | Level |
|---|---|---|
| `finally` block | resources opened **as part of the try block** | try-block level |
| `finalize` method | resources associated **with the object** | object level |

Whatever you opened inside try, close inside finally. Whatever a specific
object is holding onto, deallocate it in that object's `finalize` before the
GC reclaims it.

```java
class Test {
    public static void main(String[] args) {
        try {
            // open resources as part of try (DB, file, network, …)
        } catch (Exception e) {
            // handling code
        } finally {
            // close those SAME try-block resources
        }
    }
}
```

```java
class Test {
    protected void finalize() {
        // deallocate resources associated with THIS object
        // then GC destroys the object
    }
}
```

### 19:42 — Two most valuable interview questions in exception handling (so far)

1. Difference between **checked exception** and **unchecked exception** (previous video).
2. Difference between **`final`, `finally`, `finalize`** (this video).

---

## 20:12 — Various possible combinations of try-catch-finally

He works through combinations one at a time, then numbers the board 1–25 at
38:59. Presented here already numbered.

### Case 1 — try-catch — valid

```java
class Case01 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        }
    }
}
```

### Case 2 — try with two catch blocks (different types) — valid

```java
class Case02 {
    public static void main(String[] args) {
        try {
        } catch (ArithmeticException e) {
        } catch (Exception e) {
        }
    }
}
```

### Case 3 — two catch blocks for the **same** exception — invalid

```java
class Case03 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        } catch (Exception x) {
        }
        // CE: exception Exception has already been caught
    }
}
```

Verified against `javac 26`: `error: exception Exception has already been caught` — same message today.

### Case 4 — try-catch-finally — valid

```java
class Case04 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        } finally {
        }
    }
}
```

### Case 5 — try-finally, no catch — valid

Why is this valid with no handling code at all? Because you can still want
**cleanup without recovery**: let the exception cause abnormal termination,
but close the database connection first.

```java
class Case05 {
    public static void main(String[] args) {
        try {
            // risky code (e.g. use DB connection)
            // if exception is raised: accept abnormal termination
        } finally {
            // close DB connection — runs BEFORE abnormal termination
        }
    }
}
```

### Case 6 — try-catch, then another try-catch — valid

```java
class Case06 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        }
        try {
        } catch (Exception e) {
        }
    }
}
```

### Case 7 — try-catch, then try-finally — valid

```java
class Case07 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        }
        try {
        } finally {
        }
    }
}
```

### Case 8 — only try (no catch, no finally) — invalid

```java
class Case08 {
    public static void main(String[] args) {
        try {
        }
        // CE: 'try' without 'catch', 'finally' or resource declarations
    }
}
```

Verified against `javac 26` — the actual message today.

> ⚠️ **Modern Java — Rule 2 (below) gained an exception in Java 7.**
> This lecture predates **try-with-resources** (Video 079). Since Java 7, a
> try block genuinely needs neither catch nor finally *if it declares a
> resource*:
>
> ```java
> try (java.io.StringReader r = new java.io.StringReader("hi")) {
>     System.out.println(r.read());
> }
> // valid — no catch, no finally; the resource's close() is the cleanup
> ```
>
> The compiler's own error message reflects this: it no longer says "try
> without catch or finally" — it says **"'try' without 'catch', 'finally' or
> resource declarations"**, spelling out the third legal exit that didn't
> exist when this video was recorded.

### Case 9 — only catch — invalid

```java
class Case09 {
    public static void main(String[] args) {
        catch (Exception e) {
        }
        // CE: 'catch' without 'try'
    }
}
```

### Case 10 — only finally — invalid

```java
class Case10 {
    public static void main(String[] args) {
        finally {
        }
        // CE: 'finally' without 'try'
    }
}
```

Try-catch-finally: only try, or only catch, or only finally, are all invalid syntax.

### Case 11 — try-finally, then catch — invalid

Order matters: first try, then catch, then finally. Put finally before catch
and the catch block becomes orphaned.

```java
class Case11 {
    public static void main(String[] args) {
        try {
        } finally {
        }
        catch (Exception e) {
        }
        // CE: catch without try
        // try-finally already completed; this catch is alone
    }
}
```

### Case 12 — try, a statement, then catch — invalid (two errors)

```java
class Case12 {
    public static void main(String[] args) {
        try {
        }
        System.out.println("hello");
        catch (Exception e) {
        }
        // CE: try without catch or finally
        // CE: catch without try
    }
}
```

### Case 13 — try-catch, a statement, then another catch — invalid

```java
class Case13 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        }
        System.out.println("hello");
        catch (Exception y) {
        }
        // CE: catch without try
    }
}
```

### Case 14 — try-catch, a statement, then finally — invalid

```java
class Case14 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        }
        System.out.println("hello");
        finally {
        }
        // CE: finally without try
    }
}
```

### Case 15 — try containing try-catch, then an outer catch for the same exception — valid

The same-exception rule (Case 3) only blocks **two catches on the same
try**. An inner try-catch and an outer catch belong to different try blocks,
so it's fine even when both catch the same type.

```java
class Case15 {
    public static void main(String[] args) {
        try {
            try {
            } catch (Exception e) {
            }
        } catch (Exception e) {
        }
    }
}
```

### Case 16 — try containing a try with no catch/finally, then outer catch — invalid

Don't reach for the outer catch to cover an inner try — that inner try still
needs its own catch or finally.

```java
class Case16 {
    public static void main(String[] args) {
        try {
            try {
            }
        } catch (Exception e) {
        }
        // CE: try without catch or finally   (the INNER try)
    }
}
```

### Case 17 — try containing try-finally, then outer catch — valid

```java
class Case17 {
    public static void main(String[] args) {
        try {
            try {
            } finally {
            }
        } catch (Exception e) {
        }
    }
}
```

### Case 18 — try-catch, and inside catch a try-finally — valid

```java
class Case18 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
            try {
            } finally {
            }
        }
    }
}
```

### Case 19 — try-catch, and inside catch a finally with no matching try — invalid

```java
class Case19 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
            finally {
            }
        }
        // CE: finally without try
    }
}
```

### Case 20 — try-catch-finally, and inside finally a try-catch — valid

Nesting of try-catch-finally inside try, inside catch, or inside finally is
always allowed.

```java
class Case20 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        } finally {
            try {
            } catch (Exception e) {
            }
        }
    }
}
```

### Case 21 — try-catch-finally, and inside finally another finally — invalid

```java
class Case21 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        } finally {
            finally {
            }
        }
        // CE: finally without try
    }
}
```

### Case 22 — try-catch-finally, then a second finally — invalid

Only **one** finally is allowed per try. A second one is orphaned.

```java
class Case22 {
    public static void main(String[] args) {
        try {
        } catch (Exception e) {
        } finally {
        }
        finally {
        }
        // CE: finally without try
    }
}
```

### Cases 23–25 — curly braces missing on try / catch / finally — invalid

`try`, `catch`, and `finally` blocks require curly braces even for a single
statement — unlike `if`/`while`, there is no brace-free single-statement form.

```java
class Case23TryNoBraces {
    public static void main(String[] args) {
        try
            System.out.println("try");
        // CE: '{' expected   (curly braces mandatory for try)
    }
}
```

```java
class Case24CatchNoBraces {
    public static void main(String[] args) {
        try {
            System.out.println("try");
        } catch (Exception e)
            System.out.println("catch");
        // CE: '{' expected   (curly braces mandatory for catch)
    }
}
```

```java
class Case25FinallyNoBraces {
    public static void main(String[] args) {
        try {
            System.out.println("try");
        } catch (Exception e) {
            System.out.println("catch");
        } finally
            System.out.println("finally");
        // CE: '{' expected   (curly braces mandatory for finally)
    }
}
```

All 25 combinations above were checked against `javac 26` (`--release` did
not change any of these results — this is core block-grammar, unaffected by
release level, aside from the Case 8 message noted under Modern Java).

---

## 40:03 — Six syntax rules

1. **In try-catch-finally, order is important**: first try, next catch, next finally.
2. **Whenever we write try, either catch or finally is compulsory.**
   Try without catch or finally is invalid.
3. **Whenever we write catch, try is compulsory.** Catch without try is invalid.
4. **Whenever we write finally, try is compulsory.** Finally without try is invalid.
5. **Nesting of try-catch-finally is allowed** — inside try, inside catch, and inside finally.
6. **Curly braces are mandatory** for try, catch, and finally blocks.

---

## Exam and interview points

1. **`final`** is a modifier (class/method/variable — no child class / no
   override / no reassignment). **`finally`** is a block for cleanup code,
   always paired with try. **`finalize`** is an `Object` method the GC calls
   just before destroying an object.
2. **finally vs finalize**, the sentence to give in an interview: finally
   cleans up resources opened **in the try block**; finalize cleans up
   resources held **by the object**, and only if that object is ever
   collected.
3. `finally` "always" runs is the exam-level answer, but `System.exit()`,
   a JVM crash, or a killed thread all skip it — know the boundary.
4. `finalize()` is **deprecated since Java 9** and **disabled by default
   since Java 18** (JEP 421); modern cleanup is try-with-resources or
   `java.lang.ref.Cleaner`. Never write a new one.
5. **Try needs catch or finally, catch needs try, finally needs try** — the
   three "X without Y" compile errors, still exact today, plus Java 7's
   fourth path: a `try` with resource declarations needs neither.
6. **Only one finally per try**, but **multiple catch blocks are fine** as
   long as no two catch the same exception type on the same try — a
   different try (even nested inside) can catch the same type again.
7. **Curly braces are mandatory** on try, catch, and finally — the one place
   Java doesn't allow the single-statement shortcut it allows on `if`/`while`/`for`.
8. **Nesting try-catch-finally inside try, catch, or finally is always legal** —
   this is what makes "which try does this catch belong to" the real skill
   being tested across all 25 combinations.

**Next:** Video 075 — throw and throws
