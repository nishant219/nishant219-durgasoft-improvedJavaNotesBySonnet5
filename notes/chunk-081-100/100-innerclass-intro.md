# Video 100 — Inner Classes Part-1 Introduction

## Video info

**Title:** Core Java With OCJP/SCJP: Innerclass  Part- 1||Introduction

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 100 of 203 |
| Series | Inner Classes · Part 1 |
| Topic | Introduction to inner classes |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 21m 59s |
| Video ID | DcFWgoKs5B0 |
| Watch | https://www.youtube.com/watch?v=DcFWgoKs5B0 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Inner classes and generics are, by Sir's own count, the only two "difficult"
topics at OCJP/core-Java level. This first video covers: the definition, why
Sun added inner classes in Java 1.1, the one-line design rule for when to use
them (with three worked examples — University/Department, Car/Engine, and the
JDK's own Map/Entry), the has-a (not IS-A) relationship between outer and
inner, the four categories of inner class, and then a deep dive into the
first category — **normal/regular inner classes**: how they compile, why
they historically couldn't hold static members, and the three ways to reach
inner-class code from static code, from instance code, and from outside the
outer class entirely.

---

### 00:05 — Inner classes: hard topic (with generics)

Only two genuinely difficult topics at OCJP/core-Java level: **generics**
and **inner classes**. Inner classes bring new syntax and deserve special
care, but they are relatively simpler than generics.

### 00:52 — Definition

A class declared **inside another class** is an inner class.

```java
class Test {
    class A {
        // A is an inner class of Test
    }
}
```

```java
// Board:
// Sometimes we can declare a class inside another class
// Such type of classes are called inner classes
```

### 02:21 — History: why 1.1 introduced inner classes

Sun launched **Java 1.0** hyping a platform-independent, object-oriented,
robust, secure, simple language, and the industry was impressed — but two
weak spots showed up almost immediately:

1. **Performance** lagged badly behind C/C++.
1. **GUI (AWT)** had a buggy event model.

**Java 1.1** targeted both: a **JIT** (Just-In-Time) compiler for
performance — Sir's joke is that the gain was closer to `0.00001%` than a
real fix, and performance stayed Java's weak point for years — and a new
**event-handling/listener model** for GUI. **As part of that event-handling
rework, Sun first used a class declared inside another class** — inner
classes were born to fix AWT bugs, not as a general-purpose feature. Their
power made programmers adopt them for ordinary (non-GUI) code soon after.

```java
// Board:
// Inner classes concept introduced in 1.1 version
// to fix GUI bug as a part of event handling
// but because of powerful features and benefits of inner classes
// slowly programmers have started using in regular coding also
```

> ❗ **Correction — the Java 1.0 → 1.1 gap was about 13 months, not 3.**
> Java was **announced** in May 1995, but **JDK 1.0** itself didn't ship until
> **January 23, 1996**. **JDK 1.1** followed on **February 19, 1997** — roughly
> **thirteen months** later, not the "just 3 months" Sir states. The two
> weak spots he names (C/C++-beating performance, buggy AWT 1.0 event
> handling) are accurately the two headline 1.0 complaints of that era; only
> the timeline is compressed.

### 09:34 — When to use inner classes (design rule)

Parent-child reuse → inheritance. For inner classes, the rule is different:

**Without one type of object existing, if there is no chance of another type
of object existing → go for an inner class.**

Three examples make this concrete.

```java
// Board:
// Without existing one type of object
// if there is no chance of existing another type of object
// then we should go for inner classes
```

### 12:21 — Example 1: University and Department

A university has several departments (CS, Electronics, Electrical…). Close
the university and every department closes with it — a department is always
**part of** a university and cannot exist alone.

```java
class University {
    class Department {
        // Department is always part of University
    }
}
// University = outer class; Department = inner class
```

```java
// Board Example 1:
// University consists of several departments
// Without existing University there is no chance of existing Department
// Hence we have to declare Department class inside University class
```

### 16:37 — Example 2: Car and Engine

An engine is a major component of a car. Without a `Car` object, there is no
`Engine` object — an engine is always part of a car.

```java
class Car {
    class Engine {
        // Engine is always part of Car
    }
}
// Car = outer; Engine = inner
```

```java
// Board Example 2:
// Without existing Car object there is no chance of existing Engine object
// Hence we have to declare Engine class inside Car class
```

### 19:26 — Example 3: Map and Entry (from Java API)

Not an example Sir invented — it's straight out of the JDK. A `Map` is a
group of key-value pairs; each pair is an **Entry**. Without a `Map` object,
there's no `Entry` object, so **`interface Entry` is defined inside
`interface Map`**.

```java
interface Map {
    interface Entry {
        // Entry is always part of Map
    }
}
// Map = outer interface; Entry = inner interface
```

```java
// Board Example 3:
// Map is a group of key value pairs
// and each key value pair is called an Entry
// Without existing Map object there is no chance of existing Entry object
// Hence interface Entry is defined inside Map interface
```

> ⚠️ **Modern Java — `Map.Entry` gained generics and a factory method.**
> The real `java.util.Map.Entry` is generic (`interface Entry<K,V>`), and
> since **Java 9** you rarely build one by hand: `Map.entry(k, v)` returns an
> immutable entry directly, and `Map.ofEntries(...)` builds a whole immutable
> map from a list of them — siblings of the same release's `List.of`/`Map.of`
> factories. None of that touches the point of this example: `Entry` still
> lives inside `Map` today for exactly the reason Sir gives — an entry can't
> exist without the map that owns it.

### 24:07 — Note 1 from examples

```java
// Note 1:
// Without existing outer class object
// there is no chance of existing inner class object
```

### 25:50 — Note 2: relation is has-a, not IS-A

Outer as parent, inner as child? **No.** A University **has-a** Department;
a Car **has-a** Engine; a Map **has-a** Entry — composition/aggregation, not
inheritance.

```java
// Board:
// The relation between outer class and inner class
// is not IS-A relation
// and it is has-a relationship
// (composition or aggregation)
```

### 27:58 — Four types of inner classes

Based on **position of declaration** and **behavior**, there are four types:

```java
// Board:
// Based on position of declaration and behavior
// all inner classes are divided into four types
// 1. Normal or regular inner classes
// 2. Method local inner classes
// 3. Anonymous inner classes
// 4. Static nested classes
```

Why "nested," not "inner," for type 4? A real reason, saved for the lesson
that covers static nested classes specifically — not just a different name
for the same thing.

### 32:49 — Normal / regular inner class definition

```java
class Outer {
    class Inner {
    }
}
```

Static nested? No — no `static` modifier. Anonymous? No — it has a name.
Method-local? No — it isn't declared inside a method. Ruling out the other
three leaves **normal or regular inner class**.

Interview wording — state it positively, not as "none of the other three":

```java
// Board:
// If we are declaring any named class
// directly inside a class
// without static modifier
// such type of inner class is called
// normal or regular inner class
```

### 37:07 — Compiling Outer.java → two .class files

Saving both classes as `Outer.java` and compiling produces **two** `.class`
files, one per class:

```java
class Outer {
    class Inner {
    }
}
// javac Outer.java
// produces: Outer.class  and  Outer$Inner.class
```

- Outer → `Outer.class`
- Inner → **`Outer$Inner.class`** — the `$` marks it as an inner class, with
  the outer class name before the `$` and the inner class name after.

In a JAR listing, a `$` anywhere in a `.class` file's name is a reliable
signal that the file belongs to an inner class. Verified: `javac Outer.java`
on JDK 26 produces exactly `Outer.class` and `Outer$Inner.class`, same as
this lecture's JDK 1.6 demo.

### 39:25 — Running without main → NoSuchMethodError

Neither `Outer` nor `Inner` declares `main`:

```java
class Outer {
    class Inner {
    }
}
```

```text
java Outer
Exception in thread "main" java.lang.NoSuchMethodError: main

java Outer$Inner
Exception in thread "main" java.lang.NoSuchMethodError: main
```

(Sir re-demos this against a JDK 1.6 install; it compiles fine, same runtime
errors.)

> ⚠️ **Modern Java — the "missing main" message has changed.**
> I compiled and ran this exact class on the JDK installed here (build 26).
> Neither `java Outer` nor `java Outer$Inner` throws `NoSuchMethodError`
> any more — both now print:
> ```text
> Error: Main method not found in class Outer, please define the main method as:
>    public static void main(String[] args)
> or a JavaFX application class must extend javafx.application.Application
> ```
> (with `Outer$Inner` in place of `Outer` for the inner-class case). The
> underlying fact is unchanged — there is no runnable `main` — but a current
> JDK's launcher explains it instead of throwing a raw `NoSuchMethodError`.
> `NoSuchMethodError: main` is what the JDK 1.6 in this recording actually
> prints; don't be confused if a current JDK phrases the same problem
> differently.

### 43:24 — Example 1 on board (compile + run outcomes)

```java
class Outer {
    class Inner {
    }
}
// Normal or regular inner class
// javac Outer.java → Outer.class , Outer$Inner.class
// java Outer        → NoSuchMethodError: main
// java Outer$Inner  → NoSuchMethodError: main
```

### 45:53 — Example 2: main inside Outer

```java
class Outer {
    class Inner {
    }

    public static void main(String[] args) {
        System.out.println("Outer class main method");
        // prints: Outer class main method
    }
}
```

```java
// javac Outer.java → two class files
// java Outer       → prints Outer class main method
// java Outer$Inner → NoSuchMethodError: main  (Inner has no main)
```

### 50:36 — Example 3: main inside Inner → CE

Without an outer object, an inner object can't exist — inner classes are
**instance**-related, so (on the OCJP-era rule) **static members are not
allowed** inside a normal inner class, `main` included. Students commonly
expect this to compile and run; the reality this lecture teaches is a
**compile-time error**.

```java
class Outer {
    class Inner {
        public static void main(String[] args) {
            System.out.println("Inner class main method");
            // CE: inner classes cannot have static declarations
        }
    }
}
```

```java
// Board:
// Inside inner class we can't declare any static members
// hence we can't declare main method
// and we can't run inner class directly from command prompt
```

The compiler message Sir has students read back: **"inner classes cannot
have static declarations."**

> ⚠️ **Modern Java — static members in inner classes became legal in Java 16.**
> I compiled the class above with `javac --release 15` and `javac --release
> 16`: `error: Illegal static declaration in inner class Outer.Inner` on 15,
> **no error at all** on 16. Java 16 relaxed the JLS rule that previously let
> only compile-time-constant `static final` fields live in a non-static inner
> class — the change shipped alongside the records feature, but it applies to
> every ordinary inner class, static methods included:
> ```java
> class Outer {
>     class Inner {
>         static int counter = 0;                  // CE before Java 16, fine from 16
>         public static void main(String[] args) {  // CE before Java 16, fine from 16
>             System.out.println("Inner class main method");
>         }
>     }
> }
> ```
> On JDK 26 installed here, `java Outer$Inner` against this class prints
> `Inner class main method` — a normal inner class can now hold a runnable
> `main` and be launched directly, something this lecture (written for the
> OCJP exam's Java 6/7 baseline) correctly says is impossible. Sir's
> reasoning — "inner class always talks about instance, so there's no static
> home for it" — is still the right mental model for *why the rule existed*;
> it's simply no longer enforced. For the OCJP exam itself (still scoped to
> the older language), the CE answer above remains correct.

### 58:02 — Instance method inside Inner is OK

Static is out (pre-16); **instance** methods are fine — otherwise the class
would have no point at all.

```java
class Outer {
    class Inner {
        public void m1() {
            System.out.println("Inner class method");
            // prints: Inner class method  (when called via an Inner object)
        }
    }
}
```

### 59:23 — Case 1: access inner code from Outer's **static** area

Calling `m1` needs an `Inner` object; without an `Outer` object, there is no
`Inner` object.

```java
class Outer {
    class Inner {
        public void m1() {
            System.out.println("Inner class method");
        }
    }

    public static void main(String[] args) {
        Outer o = new Outer();
        Outer.Inner i = o.new Inner();
        i.m1();
        // prints: Inner class method

        // combine the two creation lines:
        Outer.Inner i2 = new Outer().new Inner();
        i2.m1();

        // combine creation and the call into one line:
        new Outer().new Inner().m1();
        // prints: Inner class method
    }
}
```

The `.class` file is named `Outer$Inner`, but in source code the inner class
is referred to as **`Outer.Inner`**, and an instance is created with
**`outerRef.new Inner()`**. Verified: this class compiles and runs exactly as
shown on the JDK installed here.

### 1:07:09 — Case 2: access from Outer's **instance** area (easier)

```java
class Outer {
    class Inner {
        public void m1() {
            System.out.println("Inner class method");
        }
    }

    public void m2() {
        Inner i = new Inner(); // an Outer object already exists — it's `this`
        i.m1();
        // prints: Inner class method
    }

    public static void main(String[] args) {
        Outer o = new Outer();
        o.m2();
    }
}
```

`new Inner()` works in `m2` without `outer.new` because entering `m2` at all
already required an `Outer` object — that object exists as `this`. Instance
area access is **easier** than static-area access: normal-looking syntax,
none of `new Outer().new Inner()`.

OCJP-style question this sets up: from a given line inside `m2`, which
snippet properly calls `m1`?

### 1:13:29 — Case 3: access from **outside** Outer (same code as Case 1)

```java
class Outer {
    class Inner {
        public void m1() {
            System.out.println("Inner class method");
        }
    }
}

class Test {
    public static void main(String[] args) {
        Outer o = new Outer();
        Outer.Inner i = o.new Inner();
        i.m1();
        // prints: Inner class method

        // or:
        new Outer().new Inner().m1();
    }
}
```

The code here is identical to accessing from Outer's static area.

### 1:17:47 — Summary of three cases

```java
// Fragment summary of Cases 1-3 above — not a standalone file (these lines
// need the surrounding class/method context shown in each case) —
// see Case 1/2 for the full compilable versions.

// From static area of outer class OR from outside of outer class:
Outer o = new Outer();
Outer.Inner i = o.new Inner();
i.m1();
// or: new Outer().new Inner().m1();

// From instance area of outer class:
Inner i = new Inner();
i.m1();
```

Both styles are worth being fluent in for OCJP.

---

## Exam and interview points

1. **An inner class is a class declared inside another class.** Four kinds,
   split by position of declaration and behavior: normal/regular,
   method-local, anonymous, static nested.
2. **Inner classes shipped in Java 1.1**, built for AWT's event-handling
   rework to fix GUI bugs — not originally a general-purpose feature. (The
   1.0→1.1 gap was ~13 months, not the "3 months" stated in the lecture.)
3. **Design rule:** no chance of the outer object existing → no chance of the
   inner object existing. The relationship is **has-a** (composition or
   aggregation), never IS-A. `Map.Entry` inside `Map` is the JDK's own
   example of this.
4. **Compiling `Outer` with a member class `Inner` yields two `.class`
   files**: `Outer.class` and `Outer$Inner.class`. A `$` anywhere in a class
   file's name is always an inner-class marker.
5. **Creating a normal inner class needs an enclosing instance**:
   `outerRef.new Inner()` (or `new Outer().new Inner()`) from static code or
   from outside `Outer`; plain `new Inner()` from inside an `Outer` instance
   method, where `this` already supplies the enclosing instance.
6. **OCJP-era rule (Java 6/7): a normal inner class cannot declare static
   members, `main` included** — compile error, "inner classes cannot have
   static declarations." **Since Java 16**, that restriction is lifted for
   every ordinary inner class (verified: `--release 15` rejects it,
   `--release 16` accepts it) — know both the exam-era answer and the current
   one, and which one you're being asked for.
7. **Three access styles, one exam trap:** static area of Outer and outside
   Outer use identical code (`outer.new Inner()`); Outer's own instance area
   gets the shortcut `new Inner()`. OCJP likes to ask, given a line number,
   which form is valid there.

**Next:** Video 101 — Innerclass Part-2 normal innerclass
