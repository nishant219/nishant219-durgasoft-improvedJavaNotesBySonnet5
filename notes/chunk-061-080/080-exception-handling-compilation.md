# Video 080 — Exception Handling Compilation

## Video info

**Title:** Java Exception Handling For  Certification & Interviews || Java Exception Handling || by Durga Sir

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 80 of 203 |
| Series | Exception Handling (mega compilation) |
| Topic | Java Exception Handling For Certification & Interviews |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 10h 05m 19s (36319 seconds) |
| Video ID | VHi9PedZCq8 |
| Watch | https://www.youtube.com/watch?v=VHi9PedZCq8 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

## What this file is

This upload is a **~10-hour re-package** of the individual Exception
Handling lectures already in this playlist (videos **070–079**). It does
**not** add new certification content on top of those — it is the same
material, stitched into one sitting.

YouTube has no usable auto-captions for this mega upload, so there is no
transcript to drive timestamped, board-level notes here the way the other
files in this chunk are built. Treat this file as an **index + revision
checklist**, not as a ninth pass over the same lecture content.

**Where the real notes live:** the timestamped, corrected, board-example
notes are in the component videos **070–079**, in this same directory. Study
those for the actual lecture flow; use this file to confirm you have covered
everything before moving to Multithreading.

## Mapping: compilation topics → individual playlist videos

| Compilation topic (Exception Handling stretch) | Playlist # | Individual title (short) | Detailed notes file |
|---|---|---|---|
| Introduction to exception handling | 070 | Introduction | `notes/chunk-061-080/070-exception-handling-intro.md` |
| Default exception handling | 071 | Default Exception Handling | `notes/chunk-061-080/071-default-exception-handling.md` |
| Checked vs unchecked | 072 | Checked vs Unchecked Exceptions | `notes/chunk-061-080/072-checked-vs-unchecked.md` |
| Customized handling — try-catch | 073 | Customized Exception Handling by try-catch | `notes/chunk-061-080/073-try-catch.md` |
| `finally` block | 074 | finally block | `notes/chunk-061-080/074-finally-block.md` |
| `throw` and `throws` (intro) | 075 | throw and throws | `notes/chunk-061-080/075-throw-and-throws.md` |
| `throws` keyword (deep) | 076 | throws keyword | `notes/chunk-061-080/076-throws-keyword.md` |
| Customized / user-defined exceptions | 077 | Customized Exceptions | `notes/chunk-061-080/077-customized-exceptions.md` |
| Top-10 exceptions | 078 | Top-10 Exceptions in java | `notes/chunk-061-080/078-top-10-exceptions.md` |
| try-with-resources & multi-catch | 079 | try with resources and multi-catch block | `notes/chunk-061-080/079-try-with-resources.md` |

Watch URLs for the component videos: `https://www.youtube.com/watch?v=<VideoID>`, IDs from `notes/playlist.tsv` rows 070–079.

## OCJP study checklist

Use this as a revision checklist; tick off after reading the matching
component note. Each item below is unchanged in current Java unless a
callout says otherwise.

- [ ] **Exception vs Error** — both extend `Throwable`; the default handler
      (`printStackTrace` + thread termination) fires whenever nothing else
      catches the exception first.
- [ ] **Checked vs unchecked** — the compiler forces a checked exception to
      be caught or declared; `RuntimeException` and `Error` (and their
      subtypes) are unchecked and need no such declaration.
- [ ] **Fully vs partially checked** — `Exception` and `Throwable` are
      *partially* checked (some children are unchecked); `IOException` is
      *fully* checked (every child is also checked).
- [ ] **try-catch control flow** — first matching `catch` runs; no match
      propagates the exception up the call stack; no exception at all skips
      every `catch`.
- [ ] **Multiple catch** — child exception type before parent, or the
      compiler rejects the parent-first order as unreachable.
- [ ] **`finally`** — runs whether the try succeeded, threw, or the
      exception was caught, with one carve-out: `System.exit(...)` inside the
      try skips `finally` because the JVM halts before it gets there.
- [ ] **`final` vs `finally` vs `finalize`** — modifier vs block vs an
      `Object` method the GC used to call on its way to reclaiming an object.
- [ ] **try / catch / finally combinations** — `catch` and `finally` cannot
      stand alone; a `try` needs at least one of `catch` or `finally`.
- [ ] **`throw`** — `throw new SomeThrowable(...)`; the operand must be
      `Throwable` or a subtype; code immediately after an unconditional
      `throw` is unreachable.
- [ ] **`throws`** — declares checked exceptions a method might propagate;
      the caller must then catch or re-declare them; an overriding method
      cannot declare broader checked exceptions than the method it overrides.
- [ ] **Custom exceptions** — extend `Exception` for a checked exception,
      `RuntimeException` for an unchecked one.
- [ ] **Top exam exceptions** — `NullPointerException`,
      `ClassCastException`, `ArrayIndexOutOfBoundsException`,
      `StackOverflowError`, `IllegalArgumentException`,
      `NumberFormatException`, `IllegalStateException`, `AssertionError`,
      and which of these are raised by the JVM versus by a programmer.
- [ ] **Java 7+** — try-with-resources (any `AutoCloseable`) and multi-catch
      (`catch (TypeA | TypeB e)`).

## Exam-checklist snippets

The blocks below are **exam-checklist snippets** distilled from the
component Exception Handling lectures (070–079) — not board timestamps or a
transcript of `VHi9PedZCq8`. Every snippet has been compiled against
current `javac` (JDK 26, `--release` where a version claim is version
sensitive); comments quote the exact compiler or runtime output.

### 1) Checked — must catch or declare

```java
import java.io.PrintWriter;
class Test {
    public static void main(String[] args) throws java.io.FileNotFoundException {
        PrintWriter pw = new PrintWriter("abc.txt");
        pw.println("hello");
    }
}
// Remove the `throws` clause (and add no try-catch) and this becomes:
// CE: unreported exception FileNotFoundException; must be caught or declared to be thrown
```

### 2) Unchecked — `ArithmeticException` needs no declaration

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10 / 0); // Runtime: ArithmeticException (unchecked)
    }
}
```

### 3) try-catch — handled path

```java
class Test {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
            System.out.println("handled"); // prints handled
        }
        System.out.println("after"); // prints after
    }
}
```

### 4) Multiple catch — order matters

```java
class Test {
    public static void main(String[] args) {
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
            System.out.println("AE"); // prints AE
        } catch (Exception e) {
            System.out.println("E");
        }
        // A third catch below the Exception catch is dead code:
        // catch (ArithmeticException e) { }
        // CE: exception ArithmeticException has already been caught
    }
}
```

### 5) `finally` — always runs (normal case)

```java
class Test {
    public static void main(String[] args) {
        try {
            System.out.println("try");
        } catch (Exception e) {
            System.out.println("catch");
        } finally {
            System.out.println("finally");
        }
        // prints: try
        //         finally
    }
}
```

### 6) `final` vs `finally` vs `finalize` (exam trio)

```java
final class P { }
// class C extends P { } // CE: cannot inherit from final P

class Test {
    final int x = 10;
    public static void main(String[] args) {
        // new Test().x = 20; // CE: cannot assign a value to final variable x
        try {
            // risky
        } catch (Exception e) {
            // handling
        } finally {
            // cleanup associated with try
        }
    }

    @Override
    protected void finalize() {
        // last-wish cleanup the GC used to call before reclaiming the object
    }
}
```

> ⚠️ **Modern Java — `finalize()` is deprecated and now off by default.**
> `Object.finalize()` was marked `@Deprecated` in **Java 9**, and
> `javac -Xlint:deprecation` reports it as `[removal]`:
> `warning: [removal] finalize() in Object has been deprecated and marked for removal`.
> Since **Java 18** (JEP 421) finalization is **disabled by default** across
> the JVM — an overridden `finalize()` simply never runs unless the JVM is
> started with `--finalization=enabled`. Full detail and the `finally` vs
> `finalize` scope distinction is in `074-finally-block.md`; the summary for
> this checklist is: know the interview answer, never rely on it in new code.

### 7) Illegal combination — `catch` without `try`

```java
class Bad {
    public static void main(String[] args) {
        // catch (Exception e) { } // CE: 'catch' without 'try'
        // finally { }             // CE: 'finally' without 'try'
        try {
            System.out.println("ok");
        } finally {
            System.out.println("try-finally is valid"); // prints try-finally is valid
        }
    }
}
```

### 8) `throw` — explicit throwable

```java
class Test {
    public static void main(String[] args) {
        // throw new Test(); // CE: incompatible types: Test cannot be converted to Throwable
        throw new RuntimeException("boom");
        // System.out.println("hi"); // CE: unreachable statement
    }
}
```

### 9) `throws` — checked propagation

```java
import java.io.IOException;
class Test {
    public static void main(String[] args) throws IOException {
        doStuff();
    }
    public static void doStuff() throws IOException {
        doMoreStuff();
    }
    public static void doMoreStuff() throws IOException {
        throw new IOException("checked");
    }
}
```

### 10) Custom checked exception

```java
class TooYoungException extends Exception {
    TooYoungException(String s) {
        super(s);
    }
}
class Demo {
    static void register(int age) throws TooYoungException {
        if (age < 18) {
            throw new TooYoungException("not eligible");
        }
    }
    public static void main(String[] args) {
        try {
            register(16);
        } catch (TooYoungException e) {
            System.out.println(e.getMessage()); // prints not eligible
        }
    }
}
```

### 11) Multi-catch (Java 7+)

```java
class Test {
    public static void main(String[] args) {
        try {
            String s = null;
            System.out.println(s.length()); // NullPointerException
        } catch (ArithmeticException | NullPointerException e) {
            System.out.println("multi-catch"); // prints multi-catch
        }
    }
}
```

> ⚠️ **Modern Java — the exception message got much more useful (Java 14).**
> `s.length()` above threw a bare `NullPointerException` with no message on
> Java 6/7. Since **Java 14** (JEP 358, on by default from 15), the JVM
> generates a **helpful NPE** describing exactly what was null —
> `Cannot invoke "String.length()" because "s" is null` when compiled with
> variable debug info (the default for IDEs and most build tools; plain
> `javac` without `-g` prints `"<local1>"` instead of `"s"`). Same exception
> class, same catch clause — only the message changed. Detail in
> `075-throw-and-throws.md`.

### 12) try-with-resources (Java 7+)

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
class Test {
    public static void main(String[] args) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader("abc.txt"))) {
            System.out.println(br.readLine());
        } // br.close() called automatically
        // Resource type must implement AutoCloseable (Closeable extends it)
    }
}
```

> ⚠️ **Modern Java — Java 9 lets you reuse an existing variable directly (JEP 213).**
> The form above (declare the resource inside the parentheses) still works
> unchanged. Since **Java 9**, a variable that is already final or
> effectively final can be handed to `try (...)` by name, with no new
> declaration:
>
> ```java
> BufferedReader br2 = new BufferedReader(new FileReader("abc.txt"));
> try (br2) {
>     System.out.println(br2.readLine());
> }
> ```
>
> Full walkthrough, including why the variable must stay effectively final,
> is in `079-try-with-resources.md`.

## How to use this file

1. Prefer **videos 070–079** (and their `.md` note files) for board-level
   study — that is where the timestamps, corrections, and worked examples
   live.
2. Use **this** file when you land on the mega upload at position 80 and
   need a map plus a checklist to confirm you have covered the whole
   Exception Handling stretch.
3. Do not expect a minute-by-minute transcript here — auto-captions for
   `VHi9PedZCq8` are not usable for that purpose, and this compilation adds
   no lecture content beyond what 070–079 already teach.

---

## Exam and interview points

1. **This entry is an index, not a tenth lecture.** All teaching content
   lives in videos 070–079; this file only maps and drills it.
2. **Checked vs unchecked** is decided by the class hierarchy, not by intent:
   anything under `RuntimeException` or `Error` is unchecked, everything
   else under `Throwable` is checked.
3. **Catch order is child-before-parent**, or the compiler flags the later,
   unreachable catch as an error — confirmed above (`exception
   ArithmeticException has already been caught`).
4. **`finally` runs on every path except `System.exit`** — including when
   the `try` throws and no `catch` matches.
5. **`final` / `finally` / `finalize` is the classic interview trio**: a
   modifier, a block always paired with `try`, and a deprecated `Object`
   method the GC used to call — never confuse the three.
6. **`throw` needs a `Throwable`**, and anything unconditionally after it is
   a compile error, not dead code you can leave in.
7. **`throws` documents checked exceptions for the caller**; it does nothing
   for unchecked ones, which need no declaration at all.
8. **Custom exceptions pick their checked-ness by their superclass**:
   extend `Exception` to force callers to handle it, `RuntimeException` to
   leave that optional.
9. **Java 7 added two things** to this whole topic: try-with-resources and
   multi-catch. Everything else in the checklist predates it.
10. **Two things changed since this material was recorded that are worth
    naming in an interview**: helpful NPE messages (Java 14) and
    `finalize()` going from deprecated (Java 9) to off by default
    (Java 18, JEP 421).

---

**Next:** Video 081 — Multi Threading introduction
