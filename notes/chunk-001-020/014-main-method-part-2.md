# Video 014 — main() method, part 2

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-14 || main() method part-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 14 of 203 |
| Series | Language Fundamentals · Part 14 of 16 |
| Topic | main() method (part 2): overloading, inheritance, static block vs main |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 42m 20s (2540 seconds) |
| Video ID | l3s_6gbNFTg |
| Watch | https://www.youtube.com/watch?v=l3s_6gbNFTg |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Two kinds of callout interrupt the lecture where
> it needs it: **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and
> has since changed. **❗ Correction** — what was stated is not accurate, then
> or now. Everything else is Sir's teaching, cleaned up.
>
> *Captions are disabled on this upload, so these sections carry no timestamps.
> This is session 2 of the `main` postmortem video 012 announced; video 013
> was session 1 (the JVM contract, word by word). Command-line values
> (`java Test A B C`) are video 015, not this one.*

Every code sample, launcher error, and program output below was re-run against
`javac`/`java` 26.

## What this lecture covers

1. Overloading `main`
2. Which `main` the JVM picks when several exist
3. Inheritance and hiding of `main` in a child class
4. Static block vs `main` execution order
5. A class with a static block but no `main` — Java 1.6 vs 1.7+ behaviour (Durga's famous point)
6. Calling `main` yourself, like any other static method

---

## Overloading `main`

`main` is a method name. Like any other method, it can be **overloaded**.

```java
class Test {
    public static void main(String[] args) {
        System.out.println("String[] main");
    }

    public static void main(int[] args) {
        System.out.println("int[] main");
    }

    public static void main(double d) {
        System.out.println("double main");
    }
}
```

Running **`java Test`** always calls **`public static void main(String[] args)`**
(or its `String...` form) — that is the only overload the launcher looks for.
Every other overload is an ordinary static method: it runs only if **you**
call it.

```java
public static void main(String[] args) {
    main(10.5);
    main(new int[]{1, 2, 3});
}
```

Exam wording: "Can we overload `main`?" **Yes.** "Will the JVM call the
overloaded versions automatically?" **No.**

---

## Inheritance of `main`

`static` methods are inherited in the "available on the child" sense, but what
happens when a child redeclares one is **hiding**, not instance overriding.

```java
class Parent {
    public static void main(String[] args) {
        System.out.println("Parent main");
    }
}

class Child extends Parent {
}
```

```text
java Child   →   Parent main
```

`Child` declares no `main` of its own, so the JVM uses the inherited static
`main` from `Parent`. Durga's point: you can launch a child class that has no
`main` written in its own file, as long as some parent in the chain supplies
the protocol method.

If the child declares its own:

```java
class Child extends Parent {
    public static void main(String[] args) {
        System.out.println("Child main");
    }
}
```

```text
java Child   →   Child main
java Parent  →   Parent main
```

The child's `main` **hides** the parent's `main`. This is not `override` in
the instance / `@Override` sense — `static` methods don't participate in
runtime polymorphism.

---

## Static block vs `main`

Static blocks run when the class is **initialized**, which for `java Test`
happens before `main` is invoked.

```java
class Test {
    static {
        System.out.println("static block");
    }

    public static void main(String[] args) {
        System.out.println("main method");
    }
}
```

Output:

```text
static block
main method
```

Multiple static blocks run top to bottom, then `main`:

```java
class Test {
    static { System.out.println("block 1"); }
    static { System.out.println("block 2"); }
    public static void main(String[] args) {
        System.out.println("main");
    }
}
```

Output: `block 1`, `block 2`, `main`.

Static variable initializers are folded into the same class-init sequence
(more on this in the OOPs static-control-flow videos later in the playlist).

---

## Class **without** `main` — the version split Durga always teaches

```java
class Test {
    static {
        System.out.println("static block");
    }
}
```

**Java 1.6 and earlier:** the JVM initializes the class, the static block
**runs**, then launch fails:

```text
static block
NoSuchMethodError: main
```

**Java 1.7 and later — including every JDK still in use today (re-verified on
javac/java 26):** the JVM checks for `main` **first**, before touching the
class at all. You get a launcher error and the static block **does not run**:

```text
Error: Main method not found in class Test, please define the main method as:
   public static void main(String[] args)
or a JavaFX application class must extend javafx.application.Application
```

(The JavaFX clause is newer wording for a newer alternative entry point; it is
just boilerplate here since `Test` is not a JavaFX `Application`.)

This is one of Durga's highest-frequency interview points, and the behaviour
has been stable since 1.7 — always state the version when you answer it.

---

## Calling `main` yourself

Nothing magical prevents it:

```java
class Test {
    public static void main(String[] args) {
        System.out.println("main");
        if (args.length == 0) {
            Test.main(new String[]{"from code"});
        }
    }
}
```

That is an ordinary static call. Recursion without a base case still ends in
a `StackOverflowError`, same as any other method.

The JVM's launch is only the **first** call. After that, `main` is just a
method — call it, overload it, pass it around like any other static member.

---

## `main` outside a plain class

```java
interface IFace {
    static void main(String[] args) {
        System.out.println("interface main");
    }
}

enum E {
    A, B;
    public static void main(String[] args) {
        System.out.println("enum main");
    }
}
```

Both `java IFace` and `java E` launch and print, verified on javac/java 26.

> ❗ **Correction — enum `main` was never a "later Java" feature.**
> The original note filed both cases together as a post-lecture addition. Only
> the **interface** case is later: interfaces could not have static methods
> until interface static/default methods arrived in **Java 8**. `enum` has
> supported ordinary static methods since **Java 5** — the release that
> introduced `enum` itself, years before this lecture was recorded. A
> `public static void main` in an `enum` was always legal; there was nothing
> to wait for.

This OCJP-era lecture is about **classes**; keep the interface/enum forms as
a footnote unless a question specifically asks about them.

> ⚠️ **Modern Java — `main` doesn't need a class, `static`, or `args` at all (Java 25).**
> **JEP 512**, finalized in Java 25, lets a source file skip the class
> declaration and drop `static` and `String[] args`:
>
> ```java
> // Hello.java — no class, no static, no args
> void main() {
>     System.out.println("compact source file, instance main");
> }
> ```
>
> Run it directly, no separate compile step: `java Hello.java`. This is aimed
> at first programs and scripting, not at replacing the classic protocol —
> and the rules this lecture teaches still govern that protocol:
>
> ```java
> class Both {
>     public static void main(String[] args) {
>         System.out.println("static String[] main");
>     }
>     void main() {
>         System.out.println("instance main");
>     }
> }
> ```
>
> `java Both` prints **`static String[] main`** (verified on javac/java 26) —
> a classic `public static void main(String[] args)`, when present, is still
> what the JVM launches first. The instance form is a fallback for when no
> classic entry point exists, not a second protocol competing with it.

---

## Interaction with overloading + inheritance (exam combo)

```java
class P {
    public static void main(String[] args) {
        System.out.println("P");
    }
}

class C extends P {
    public static void main(int[] args) {
        System.out.println("C int");
    }
}
```

`java C` → **`P`** (verified).

`C`'s `main(int[])` does **not** hide `main(String[])` — different signature,
so it's a separate overload, not a redeclaration. The JVM still walks up to
`P.main(String[])`.

To hide the parent's entry point, the child must declare `main(String[])`
(or `String... args`) — nothing narrower.

---

## Code from the lecture

```java
class Parent {
    static {
        System.out.println("Parent static");
    }
    public static void main(String[] args) {
        System.out.println("Parent main");
        main(100);
    }
    public static void main(int x) {
        System.out.println("overloaded " + x);
    }
}

class Child extends Parent {
    static {
        System.out.println("Child static");
    }
    public static void main(String[] args) {
        System.out.println("Child main");
    }
}
```

`java Child` (verified):

```text
Parent static
Child static
Child main
```

`java Parent` (verified):

```text
Parent static
Parent main
overloaded 100
```

Parent is initialized before Child either way — that's the static-control-flow
rule (later videos), and it holds regardless of which class is launched.
Since `Child.main(String[])` hides `Parent.main(String[])`, launching `Child`
never runs `overloaded 100` — `Child.main` would have to call `Parent.main(args)`
explicitly to reach it; `super.main(...)` is not valid syntax for a `static`
method.

The takeaway for this lecture: **the class named on the command line is whose
`String[] main` gets searched, walking up the parent chain if the class
itself doesn't declare one.**

---

## Rules to memorize

1. Overload `main` freely; the JVM still only auto-calls the `String[]` /
   `String...` form.
2. A child without any `main` still launches if a parent supplies the
   `String[]` protocol method — found by walking up the inheritance chain.
3. A child's own `main(String[])` **hides** the parent's. That's static
   hiding, not instance overriding; `@Override` semantics don't apply to
   `static` methods.
4. Static blocks of the *launched* class run before `main`, top to bottom, but
   only once the class actually initializes.
5. No `main` anywhere in the chain: Java 1.6 runs the static block then throws
   `NoSuchMethodError`; Java 1.7 and every later JDK (checked up to 26) report
   "Main method not found" and skip the static block entirely.
6. Since Java 25, an instance `main()` with no modifiers or parameters is a
   legal fallback entry point — but only when no classic
   `public static void main(String[] args)` exists on the class.

---

## Exam and interview points

1. **"We cannot overload `main`" is false.** You can declare as many `main`
   overloads as you like; only `String[]`/`String...` is auto-called.
2. **A child with only `main(int[])` still runs the parent's `String[] main`**
   on `java Child` — a different parameter type is a different method, not a
   hiding redeclaration.
3. **"Static block without `main`" is a version question, not a yes/no one.**
   1.6: block runs, then `NoSuchMethodError`. 1.7 onward (still true today):
   "Main method not found," block never runs. Always name the version.
4. **`Main` in a child does not hide `main` in the parent.** Method names are
   case-exact; capitalization makes it an unrelated method.
5. **Overloaded `main`s are never auto-called, but nothing stops you calling
   them yourself** from inside the real entry point — recursion without a
   base case still ends in `StackOverflowError`, same as any other method.
6. **Enum `main` is not a "newer Java" trick.** It has worked since enums
   arrived in Java 5. Interface `main` (via Java 8 static interface methods)
   is the one genuinely later addition.
7. **Since Java 25 (JEP 512), `main` doesn't need `static`, `public`, or
   `String[] args` at all** in a compact source file — but a class's own
   classic `public static void main(String[] args)`, when present, is still
   what the JVM launches first. The overload/inheritance rules in this
   lecture are about that classic protocol and are unaffected.
8. **Know the exact modern launcher error text** — "Error: Main method not
   found in class X, please define the main method as: public static void
   main(String[] args) or a JavaFX application class must extend
   javafx.application.Application." The JavaFX clause is new wording for a
   newer alternative entry point, not new behaviour for this lecture's rules.

---

**Next:** Video 015 — Command Line Arguments
