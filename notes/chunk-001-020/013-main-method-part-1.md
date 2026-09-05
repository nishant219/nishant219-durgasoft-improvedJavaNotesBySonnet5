# Video 013 — main() method, part 1

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-13 || main() method part-1

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 13 of 203 |
| Series | Language Fundamentals · Part 13 of 16 |
| Topic | main() method (part 1): signature, modifiers, JVM contract |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 06m 40s (4000 seconds) |
| Video ID | AipADVI3OG0 |
| Watch | https://www.youtube.com/watch?v=AipADVI3OG0 |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** YouTube has captions disabled on this upload, so
> there are no burned-in timestamps here — sections follow the lecture's own
> structure instead. Two kinds of callout interrupt the teaching where it needs
> it: **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Why `main` exists (the JVM's entry point)
2. Word-by-word meaning of `public static void main(String[] args)`
3. What happens if you drop or change each word (`NoSuchMethodError`)
4. Legal rearrangements and extra modifiers
5. `String[] args` vs `String args[]` vs `String... args`
6. Changing the name `args`

Durga's throughline: `main` is a **protocol between programmer and JVM**, not a
language keyword — and OCJP tests the edges of that protocol, not the headline
signature.

---

## Who calls `main`?

You never call `main` from your own code as the start of the program. You type:

```java
java Test
```

The **JVM** loads `Test`, then looks for a method with a **fixed protocol**:

```java
public static void main(String[] args)
```

If that exact contract is missing, you do **not** get a compiler error for "no
main" in a normal class compile. You get a **runtime** error when you launch:

```java
NoSuchMethodError: main
```

(On a current JDK the message is friendlier — confirmed on JDK 26:
`Error: Main method not found in class Test, please define the main method
as: public static void main(String[] args)`.)

`main` is an **identifier**, not a reserved word (video 001). That is why
`Main` is a legal but different method — same spelling rules, different
capitalisation, different method entirely.

## `public`

The JVM is **outside** your class (it is not your code). It must be allowed to
call `main` from anywhere → `public`.

```java
class Test {
    private static void main(String[] args) { }   // compiles; launches: Main method not found
}
```

Same story for default (no modifier) and `protected` — the classic JVM search
was for **public** `main` specifically. (See the Modern Java box below: this
has changed.)

## `static`

The JVM calls `main` **without creating an object**. There is no `new Test()`
before `main` runs, so `main` must be `static`.

```java
class Test {
    public void main(String[] args) { }  // compiles; launches: Main method not found (classic rule)
}
```

If `main` were an instance method, the JVM would have to guess a constructor
and build an object before it could call anything — Java's classic launch
sequence never did that.

## `void`

The JVM does not use a return value from `main`. The return type must be
`void`.

```java
class Test {
    public static int main(String[] args) {
        return 0;   // compiles; launches: Main method not found — wrong return type
    }
}
```

(C's `int main` is a different language with a different contract — its
return value becomes the process exit code. Java's `main` has no such role;
use `System.exit(code)` if you need one.)

> ⚠️ **Modern Java — this protocol got a lot looser.**
> Everything above is still exactly right for the OCJP exam this course targets, and
> it is still what every real Java program should write. But starting with **JDK 25**
> (JEP 512, *Compact Source Files and Instance Main Methods* — after four rounds of
> preview as JEP 445/463/477/495 across JDK 21–24), the `java` launcher's search for an
> entry point became far more permissive. Confirmed on JDK 26 — every one of these now
> launches with `java ClassName`, where none of them did before:
>
> ```java
> class T1 { static void main(String[] args) { /* ... */ } }          // package-private static
> class T2 { protected static void main(String[] args) { /* ... */ } } // protected static
> class T3 { public void main(String[] args) { /* ... */ } }           // instance, not static
> class T4 { public static void main() { /* ... */ } }                 // no parameter at all
> class T5 { void main() { /* ... */ } }                               // package-private instance, no params
> ```
>
> For an **instance** `main` the launcher does the equivalent of `new T3().main(args)`
> — it builds the object with a no-arg constructor first, then calls `main` on it
> (confirmed: a constructor with a `println` in it runs before the instance `main`
> body does). The one access level that still fails is **`private`**:
> `private static void main(String[] args)` still prints `Error: Main method not
> found...` on JDK 26. So "public" relaxed to "anything but private," not to "anything."
>
> Untouched by JEP 512: the return type must still be `void` (`public static int main`
> still fails to launch), the name must still be exactly `main`, and an array
> parameter, if present, must still be `String[]` (`main(int[] args)` still fails).
>
> The same JEP also permits a `.java` file with **no `class` declaration at all** — an
> "unnamed class." A file containing only
> `void main() { System.out.println("hi"); }` is a complete, runnable program
> (confirmed on JDK 26). That is the mechanism behind the one-line "hello world" demos
> in JDK 21+ onboarding material — a beginner-friendly on-ramp, not part of the OCJP
> syllabus this course teaches, and not how you should write a shipped program.

## `main` — the name

The name must be **`main`**, exact case, on both the classic and the modern
protocol.

```java
public static void Main(String[] args) { }  // compiles; launches: Main method not found
public static void MAIN(String[] args) { }  // compiles; launches: Main method not found
```

Those compile as ordinary methods. The JVM just will not call them as the
entry point.

## `String[] args`

Command-line arguments are strings (video 015), so the parameter is an array
of `String`.

Legal forms Durga writes — all confirmed compiling and launching identically:

```java
public static void main(String[] args) { }
public static void main(String args[]) { }
public static void main(String []args) { }
```

From Java 1.5, the var-arg form is also an entry point (a varargs parameter is
an array under the hood):

```java
public static void main(String... args) { }
```

Not an entry point, on either protocol:

```java
public static void main(String args) { }     // one String, not an array
public static void main(int[] args) { }      // wrong element type
```

Those compile; the launcher ignores them.

## Parameter name is your identifier

`args` is only a convention (video 016, coding standards — even `args` is just
the usual name). Any valid identifier works:

```java
public static void main(String[] a) { }
public static void main(String[] dhanush) { }
public static void main(String[] values) { }
```

Still the entry point. Inside the body, use that name: `dhanush.length`, not
`args.length`.

## Order of `public` and `static`

Modifier order is not fixed:

```java
static public void main(String[] args) { }   // valid entry point
```

`void` must stay immediately before the name — Java always writes
`<modifiers> <return type> <name>(<params>)`, and that ordering is not special
to `main`. You cannot write `public static main void`.

## Extra modifiers that are still an entry point

You may add:

- **`final`** — a subclass cannot redeclare (hide) a static method with the
  same signature; the JVM still calls this `main` exactly the same way.
- **`synchronized`** — the JVM still calls it; the call just acquires the lock
  on the class object first.
- **`strictfp`** — historically forced IEEE 754 strict floating-point
  arithmetic for the method body.

```java
public static final synchronized strictfp void main(String[] args) { }
```

Confirmed: this compiles and launches as a normal entry point on JDK 26.
Durga puts this on the board as a "don't panic in the exam" example — a wall
of modifiers in front of `main` is still just `main`.

> ⚠️ **Modern Java — `strictfp` on `main` is now a no-op.**
> Since **Java 17** (JEP 306), all floating-point arithmetic is strict by
> default — which is what `strictfp` used to opt into. The keyword still
> parses and the method above still compiles, but `javac` now flags it
> (confirmed on JDK 26):
>
> ```text
> warning: [strictfp] as of release 17, all floating-point expressions are
> evaluated strictly and 'strictfp' is not required
> ```
>
> It was a legitimate OCJP trick option in this course's era. Today it is
> dead weight on the signature — harmless, but pointless.

Two modifiers Sir warns off `main` outright:

- **`abstract`** — an abstract method has no body, and the class containing
  it would have to be declared abstract too.
- **`native`** — a native method has no *Java* body; its implementation lives
  in a loaded native library.

```java
public static abstract void main(String[] args);   // CE, see correction below

public static native void main(String[] args);     // compiles
```

> ❗ **Correction — the two fail differently, and not the way "no runnable
> body" suggests.**
> `abstract` fails at **compile time**, and the reason is not "no body": Java
> simply forbids combining `abstract` with `static` at all, body or no body.
> `javac` reports (confirmed on JDK 26):
> ```text
> error: illegal combination of modifiers: abstract and static
> ```
> `native static void main(String[] args)` **does compile**, and the launcher
> **does find it and call it** as a valid entry point — it only fails when the
> JVM tries to link the missing native implementation, with (confirmed on
> JDK 26):
> ```text
> Exception in thread "main" java.lang.UnsatisfiedLinkError: 'void Test.main(java.lang.String[])'
> ```
> not a "main not found" message. So `native` *is* treated as the entry point
> (and then crashes); `abstract` never gets past the compiler. Either way,
> Sir's exam advice is the right one — keep both off `main`.

## Putting it together

```java
class Test {
    static public final synchronized strictfp void main(String... dhanush) {
        System.out.println("entry point");
        System.out.println(dhanush.length);
    }

    public static void main(int[] args) {
        System.out.println("overloaded — JVM ignores this on launch");
    }
}
```

Launch:

```java
java Test
```

Confirmed output: `entry point` then `0`. The `int[]` overload compiles and
sits there, unused — the JVM only ever calls the one method matching its
exact protocol, no matter how many other `main`s share the class (overloading
`main` proper is video 014's topic).

## Compile vs run — the two-step check

For each variant, ask two separate questions:

1. **Does it compile?** (ordinary Java language rules)
2. **Can we launch with `java ClassName`?** (the JVM's separate protocol search)

| Declaration | Compile? | `java Test`? |
|---|---|---|
| `public static void main(String[] args)` | yes | yes |
| `static public void main(String[] args)` | yes | yes |
| `public static void main(String... args)` | yes | yes |
| `public static void main(String args[])` | yes | yes |
| `public void main(String[] args)` | yes | Main not found *(classic) — launches since JDK 25, see box above* |
| `public static void Main(String[] args)` | yes | Main not found |
| `public static int main(String[] args)` | yes | Main not found |
| `private static void main(String[] args)` | yes | Main not found |
| `public static void main(int[] args)` | yes | Main not found |

The class can still have those methods — they compile fine and can be called
normally from other code. They just are not (all of them, still) the JVM's
entry point.

## Why this is "language fundamentals"

OCJP loves mixing:

- a legal `main` that is not the protocol
- two methods named `main` (overloading — video 014)
- `String[]` vs `String...`

Part 1 is: **one method, torn apart word by word.**

## `String` is not a keyword

Reminder from video 001: you could theoretically name a variable `String`,
which would make `String[] args` a mess to read. Don't. The parameter type
must resolve to `java.lang.String`, and shadowing that name with a variable
is legal but actively unhelpful — exactly the Rule 6 trap from that lecture.

---

## Exam and interview points

1. **`main` is an identifier, not a keyword.** `Main`, `MAIN`, and any other
   casing compile as ordinary methods; the JVM just will not launch them.
2. **A class without a matching `main` still compiles.** The failure is a
   **runtime** launch error, not a compiler error.
3. **The classic protocol is exactly `public static void main(String[] args)`**
   (or `String args[]`, or `String... args` since 1.5) — this is still the
   correct OCJP answer and still the correct signature for any real program.
4. **`public` and `static` may swap order**; `void` may not move away from
   immediately before the method name.
5. **`final`, `synchronized`, and `strictfp` may all be added** to `main` and
   it remains a valid entry point; `abstract` cannot combine with `static` at
   all (compile error), and `native` compiles and *is* found by the launcher
   but crashes with `UnsatisfiedLinkError`.
6. **The parameter name is yours to choose** (`args`, `a`, `dhanush`,
   anything valid) — only the type (`String[]`) is fixed by the protocol.
7. **`strictfp` has been a no-op since Java 17** (JEP 306) — worth marks on
   this course's exam, dead weight in current code.
8. **Since JDK 25 (JEP 512), the launcher's search is far more permissive**:
   `main` may now be an instance method (the JVM constructs the object first),
   may be package-private or protected instead of public, and may take zero
   parameters. Only `private` access, a non-`void` return, the wrong name, and
   a non-`String[]` array parameter still fail. A current interviewer asking
   "does `main` have to be `public static`?" is testing whether you know this
   changed — the OCJP-era answer ("yes, always") is no longer the whole truth.
9. **JEP 512 also allows a `.java` file with no `class` declaration** — a bare
   `void main() { ... }` is a runnable program. Useful to recognise in modern
   sample code; not a substitute for the full class-based protocol this
   lecture teaches.

---

**Next:** Video 014 — main() method, part 2
