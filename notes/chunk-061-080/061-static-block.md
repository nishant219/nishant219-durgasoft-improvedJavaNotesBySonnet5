# Video 061 — Static Block

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-11 ||static block

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 61 of 203 |
| Series | OOPs · Part 11 |
| Topic | static block |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 11m 00s |
| Video ID | T-vbOoCzxI4 |
| Watch | https://www.youtube.com/watch?v=T-vbOoCzxI4 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is **OOPs Part 11**, a postmortem on the static block introduced
alongside static control flow in Video 060: what it's for, how many a class
can hold, and two classic interview loopholes — printing to the console
without `main`, and printing without `main` *or* a static block. Two real
motivating examples anchor the "why": loading native libraries at
class-load time, and how a JDBC driver auto-registers with `DriverManager`.
The back half returns to static control flow, now across a **parent–child**
pair (`Base` / `Derived`), tracing all three activities across both classes
and contrasting `java Derived` with `java Base`.

---

## 00:04 — Agenda: postmortem on the static block

Following on from static control flow (Video 060), four questions drive this
video:

- What is the need of a static block?
- How do we declare one?
- How many static blocks can a class hold?
- When exactly is a static block executed?

### 00:34 — When is a static block executed?

**Rule:** a static block runs **at the time of class loading**.

> *At the time of class loading, if we want to perform any activity → go
> for a **static block**.*

```java
class DemoNeed {
    static {
        System.out.println("class loading activity");
    }

    public static void main(String[] args) {
        System.out.println("main");
    }
}
// prints:
//   class loading activity
//   main
```

The static block runs first, automatically, before `main` — it needs no
call.

---

## 02:34 — When is a static block actually required?

Two classic real-world cases:

1. Loading **native libraries** at class-load time.
2. Registering a **JDBC driver** with `DriverManager` at class-load time.

### 02:47 — Example 1: loading native libraries

```java
class Test {
    static {
        System.loadLibrary("native_library_path");
    }
}
```

`System.loadLibrary(...)` takes the native library's name. When `Test`
loads, the static block runs and the library loads with it — a one-time
activity that has to happen exactly at class-load time, which is precisely
what a static block guarantees.

This is not a pattern Sir invented for the demo — every predefined class
that needs a native library follows it too.

### 06:01 — Proof from the JDK: `Object` and `Thread`

`java.lang.Object` ships several **native** methods (`hashCode()`, `wait()`,
…), so its native library has to load when `Object` loads. The real source
does this with a static block calling `registerNatives()` — the same idea
as `System.loadLibrary`, simplified here to compile standalone:

```java
class ObjectDemo {
    private static native void registerNatives();

    static {
        registerNatives();
    }

    // native methods such as hashCode(), wait(), etc. live here too
}
```

`java.lang.Thread` has native methods too (`start()`, `yield()`, …) and
follows the identical pattern:

```java
class ThreadDemo implements Runnable {
    private static native void registerNatives();

    static {
        registerNatives();
    }

    public void run() { }
    // native start(), yield(), etc. live here too
}
```

**Takeaway:** if an activity must happen exactly when a class is loaded, it
belongs in a static block — loading native libraries is the textbook case.

### 07:53 — Example 2: JDBC driver registration (very important)

Basic JDBC, core-Java style:

```java
class JdbcFlow {
    static void demo() throws Exception {
        Class.forName("oracle.jdbc.driver.OracleDriver");                // 1: load driver class
        // Connection con = DriverManager.getConnection(url, user, pwd); // 2: get a connection
        // PreparedStatement pst = con.prepareStatement(sql);            // 3: prepare a statement
        // ResultSet rs = pst.executeQuery();                            // 4: execute, read ResultSet
    }
}
```

**The puzzle:** a machine can have several DB drivers installed at once
(Oracle, MySQL, DB2, …). Right after `Class.forName(...)` loads the driver
class, the code asks `DriverManager` for a connection — nobody ever writes
a line that "registers" the driver. So how does `DriverManager` know which
driver we just loaded?

**The answer:** as per the JDBC specification, every driver class must
contain a static block that registers itself with `DriverManager`.

```java
class DBDriver {
    static {
        // register this driver with DriverManager
        // (real drivers call DriverManager.registerDriver(...) here)
    }
}
```

```java
class DriverLoad {
    static void demo() throws ClassNotFoundException {
        Class.forName("com.mysql.cj.jdbc.Driver");
        // 1) the driver class is loaded
        // 2) its static block runs automatically
        // 3) the driver registers itself with DriverManager
        // -> we are NOT responsible for registering explicitly
    }
}
```

If you write your own driver class, this static-block registration is
**compulsory** under the spec — which is exactly why "register with
`DriverManager`" never appears as its own step in a basic JDBC walkthrough.

> ⚠️ **Modern Java — `Class.forName(...)` stopped being necessary in 2006.**
> Since **JDBC 4.0**, shipped with **Java 6**, a compliant driver jar lists
> its driver class in `META-INF/services/java.sql.Driver`, and
> `DriverManager`'s own static initializer uses `ServiceLoader` to discover
> and load every driver on the classpath automatically. `Class.forName(...)`
> is what triggers the static block in *this* lecture's telling, and it is
> still harmless and widely written defensively (older drivers, OSGi/shaded
> classpaths, or just habit), but for a JDBC-4-compliant driver it is
> optional, not the first required step. The static-block mechanism Sir
> describes is exactly right either way — `Class.forName` and
> `ServiceLoader` just differ in *what* triggers that static block to run.

**Need of a static block (summary):**

> **Board:** At the time of class loading, if we want to perform certain
> activity automatically, go for a static block.

---

## 15:04 — How many static blocks in a class?

Any number — and all of them run **top to bottom**.

```java
class MultiStatic {
    static {
        System.out.println("first static block");
    }

    static {
        System.out.println("second static block");
    }

    static {
        System.out.println("third static block");
    }

    public static void main(String[] args) {
        System.out.println("main");
    }
}
// prints:
//   first static block
//   second static block
//   third static block
//   main
```

---

## 16:23 — Interview Q1: print without `main`?

**Question:** without writing a `main` method, is it possible to print to
the console?

**Answer (≤ Java 1.6):** yes — with a static block.

```java
class Test {
    static {
        System.out.println("Hello I can print");
    }
}
// on JDK <= 1.6:
//   prints "Hello I can print"
//   then: Exception in thread "main" java.lang.NoSuchMethodError: main
```

The class loads, the static block runs and prints, and only *then* does the
JVM go looking for `main`. It isn't there, so it fails — but only after the
static block has already done its job. To stop the JVM from bothering to
look, call `System.exit(0)` from inside the block:

```java
class Test {
    static {
        System.out.println("Hello I can print");
        System.exit(0);
    }
}
// on JDK <= 1.6: prints "Hello I can print" — JVM exits, no NoSuchMethodError
```

*(`NoSuchMethodError` is an `Error`, not an exception — see Video 060's
correction on that point.)*

## 21:10 — Interview Q2: without `main` **and** without a static block?

**Question:** without writing `main` and without writing a static block, is
it still possible to print to the console?

First instinct: no. **Correct answer (≤ Java 1.6): yes — multiple ways.**

### 22:41 — Way 1: static variable assignment calls a static method

```java
class Test {
    static int x = m1();

    public static int m1() {
        System.out.println("Hello I can print");
        System.exit(0);
        return 10; // syntactically required — m1's return type is int
    }
}
// on JDK <= 1.6: prints "Hello I can print" — no main, no static block
```

Static control flow (Video 060) says: identify static members, then execute
static variable assignments. `x = m1()` is an assignment, so `m1()` runs as
part of it — no `main`, no static block, and it still prints.

### 25:37 — Way 2: static object triggers an instance block

```java
class Test {
    static Test t = new Test();

    {
        System.out.println("Hello I can print");
        System.exit(0);
    }
}
// on JDK <= 1.6: prints "Hello I can print"
```

`new Test()` runs during the static assignment `t = new Test()`, and object
creation runs the **instance block** — which fires at object-creation time,
not class-load time, unlike a static block.

### 27:36 — Way 3: static object triggers a constructor

```java
class Test {
    static Test t = new Test();

    Test() {
        System.out.println("Hello I can print");
        System.exit(0);
    }
}
// on JDK <= 1.6: prints "Hello I can print"
```

Same trigger (`new Test()` during static assignment), but this time the
print comes from the constructor instead of an instance block.

**Q2 summary:** without `main` and without a static block — yes, multiple
ways (a static assignment calling a method; an instance block; a
constructor), each running because it's reachable from a *static variable
assignment*, which static control flow already guarantees will execute.

## 32:43 — The version twist (very important)

Everything above — printing with no `main`, or with no `main` and no static
block — is **only true up to Java 1.6**.

> **Board:** From 1.7 onwards, main method is mandatory to start a program
> execution. Hence, without writing `main`, it is impossible to print some
> statements to the console.

```java
// Java >= 1.7: this alone can no longer start a program
class Test {
    static {
        System.out.println("Hello I can print");
        System.exit(0);
    }
}
```

(Same point is covered in the main-method-fundamentals lectures.)

> ⚠️ **Modern Java — verified on JDK 26: none of the four tricks above print
> anything any more, and the failure looks different too.**
> Video 060 already traces *why* this changed: from Java 7 onward, the
> launcher checks for a `public static void main(String[])` by reflection
> **before** it initializes the class at all, not after. Re-running every
> example from this lecture on a current JDK confirms the same thing holds
> for all four tricks, not just the static-block case:
>
> ```text
> $ java Test        # static block only (Q1, no exit)
> Error: Main method not found in class Test, please define the main method as:
>    public static void main(String[] args)
> or a JavaFX application class must extend javafx.application.Application
> ```
>
> Way 1 (static assignment → static method), Way 2 (static object →
> instance block), and Way 3 (static object → constructor) all fail with the
> **identical** message — no output at all, not even "Hello I can print".
> That's the important shift: it isn't merely that `main` is "required
> eventually," it's that **class initialization itself never starts**
> without a `main` method present, so nothing that lives inside that
> class — static block, static assignment, instance block, constructor —
> gets a chance to run. Sir's `System.exit(0)` trick is moot for the same
> reason: there's nothing left to exit early from.

---

## 35:09 — Next: static control flow in a parent–child relationship

Covered so far: the need and timing of a static block, native-library and
JDBC examples, any number of static blocks, the two interview loopholes, and
the 1.7 rule. Next: if both a parent and a child class have static members,
what is the control flow when the *child* runs?

### 36:09 — Example: `Base` and `Derived`

Two classes in one file. `Derived` has the same shape as the single-class
static-control-flow example from Video 060 (two static blocks, `main`, and a
helper method).

```java
class Base {
    static int i = 10;

    static {
        m1();
        System.out.println("Base static block");
    }

    public static void main(String[] args) {
        m1();
        System.out.println("Base main");
    }

    public static void m1() {
        System.out.println(j);
    }

    static int j = 20;
}

class Derived extends Base {
    static int x = 100;

    static {
        m2();
        System.out.println("Derived first static block");
    }

    public static void main(String[] args) {
        m2();
        System.out.println("Derived main");
    }

    public static void m2() {
        System.out.println(y);
    }

    static {
        System.out.println("Derived second static block");
    }

    static int y = 200;
}
```

(Compared with Video 060's single-class demo, `Base` here drops the second
static block; otherwise the idea is identical.)

### 41:03 — Compile and run the child

```text
$ javac Base.java
$ java Derived
```

Compiling `Base.java` generates **two** class files — `Base.class` and
`Derived.class` — because `Derived` lives in the same source file.

**Key idea:** parent members are available to a child by default, so
whenever the **child** class loads, the **parent** loads first, and the
parent's static control flow runs before the child's.

### 42:44 — Three activities when executing the child

Running the **child** class performs three activities, in this order:

1. **Identification** of static members **from parent to child** (top to
   bottom: parent first, then child).
2. **Execution** of static variable assignments **and** static blocks
   **from parent to child**.
3. **Execution of only the child class's `main`** — we ran `java Derived`,
   not `java Base`.

If the child had **no** `main` of its own, the inherited **parent** `main`
would run instead. Here `Derived` already defines `main`, so `Base.main`
never executes.

### 45:24 — Trace step 1: identification (RIWO)

During identification, static **variables** get their default values and
enter **RIWO** (Read Indirectly, Write Only — Video 060's term):

**Parent (`Base`), identified first:**

| Step | Member | Effect |
|---|---|---|
| 1 | `static int i` | `i = 0` (RIWO) |
| 2 | static block | identified |
| 3 | `main` | identified |
| 4 | `m1` | identified |
| 5 | `static int j` | `j = 0` (RIWO) |

**Child (`Derived`), numbering continues:**

| Step | Member | Effect |
|---|---|---|
| 6 | `static int x` | `x = 0` (RIWO) |
| 7 | first static block | identified |
| 8 | `main` | identified |
| 9 | `m2` | identified |
| 10 | second static block | identified |
| 11 | `static int y` | `y = 0` (RIWO) |

Steps **1–11** — identification complete, parent then child.

### 47:12 — Trace step 2: assignments and static blocks, parent → child

**Parent:**

| Step | Action | Output / effect |
|---|---|---|
| 12 | `i = 10` | read and write |
| 13–15 | static block → `m1()` → prints `j` | `j` is still `0` (its own assignment hasn't run yet) → prints `Base static block` |
| 16 | `j = 20` | read and write |

`m1()`'s `println(j)` prints `0` here — `j`'s real assignment is step 16,
still ahead of it.

**Child:**

| Step | Action | Output / effect |
|---|---|---|
| 17 | `x = 100` | read and write |
| 18–20 | first static block → `m2()` → prints `y` | `y` is still `0` → prints `Derived first static block` |
| 21 | second static block | prints `Derived second static block` |
| 22 | `y = 200` | read and write |

Same pattern as `Base`/`j`: `m2()`'s `println(y)` prints `0` here because
`y`'s assignment (step 22) hasn't executed yet. Steps **12–22** complete
this activity, parent fully finished before child begins.

### 50:56 — Trace step 3: only the child's `main`

| Step | Action | Output |
|---|---|---|
| 23–24 | `m2()` → prints `y` | `200` — now assigned |
| 25 | print `"Derived main"` | `Derived main` |

### 52:02 — Expected output for `java Derived`, verified

```text
$ javac Base.java
$ java Derived
0
Base static block
0
Derived first static block
Derived second static block
200
Derived main
```

Compiled and run exactly as shown above (same program, `Base` and
`Derived` — the lab used the filenames `Base1`/`Derived1`, but it's the
same code and the same output).

### 53:56 — Theory, dictated for the board

Whenever the **child** class runs, this sequence executes automatically:

1. Identification of static members, **parent to child** (steps 1–11).
2. Execution of static variable assignments and static blocks, **parent to
   child** (steps 12–22).
3. Execution of **only the child class's** `main` (steps 23–25).

Color hint from the lecture (for the notebook): red boxes for
identification, green boxes for assignments/static blocks, blue boxes for
the child's `main`.

### 1:02:41 — Child `main` vs. parent `main`

We're executing `Derived`, so `Derived.main` runs. If `Derived` had *no*
`main` of its own, `Base.main` would run instead — inherited members
include `main`. Here `Derived` does define `main`, so `Base.main` is never
called. If instead we run the **parent** (`java Base`), only `Base`'s
`main` runs and `Derived` isn't involved at all.

### 1:05:44 — Run the parent instead: `java Base`

**Question:** running the child loads the parent. Does running the
**parent** load the child?

**No.** Parent members are available to the child, but child members are
*not* available to the parent — so executing `Base` never loads `Derived`.
Only `Base`'s own static control flow runs:

```text
$ java Base
0
Base static block
20
Base main
```

`m1()` prints `j` twice for two different reasons now: `0` from the static
block (before `j = 20` has run), `20` from `main` (after it has).

```text
java Derived  →  0, Base static block, 0, Derived first..., Derived second..., 200, Derived main
java Base     →  0, Base static block, 20, Base main
```

### 1:08:14 — Closing rules (must remember)

1. **Loading the CHILD → the parent loads automatically** (parent members
   must be available to the child).
2. **Loading the PARENT → the child does *not* load** (child members are
   not available to the parent by default).

```text
Loading CHILD  -> parent loaded automatically
Loading PARENT -> child NOT loaded (child members aren't visible to the parent)
```

These are the important loopholes/exam traps for static control flow with
inheritance.

---

## Exam and interview points

1. **A static block runs exactly once, at class-loading time**, and needs
   no explicit call — the only static member the JVM runs automatically.
2. **Two classic reasons to reach for one**: loading a native library
   (`System.loadLibrary`, and the `registerNatives()` pattern in
   `Object`/`Thread`), and a JDBC driver registering itself with
   `DriverManager`.
3. **A class can declare any number of static blocks; they run top to
   bottom**, in source order.
4. **Print without `main` (≤ Java 1.6): yes**, via a static block — it runs
   before the JVM looks for `main` and fails with `NoSuchMethodError: main`
   (an `Error`, not an exception) if `main` is absent; `System.exit(0)`
   avoids that failure entirely.
5. **Print without `main` *and* without a static block (≤ Java 1.6): yes**,
   via any static variable assignment that reaches executable code — a
   method call, `new` triggering an instance block, or `new` triggering a
   constructor.
6. **From Java 1.7 onward, `main` is mandatory to start execution** — and on
   a current JDK this is stronger than Sir's "it fails after printing":
   verified on JDK 26, the launcher checks for `main` *before* any class
   initialization runs at all, so none of the four tricks above print
   anything any more; the diagnostic is `Error: Main method not found in
   class ...`, printed directly, not a thrown `Error` caught after the
   static phase (full derivation in Video 060).
7. **Static control flow with inheritance is three activities, run against
   the whole hierarchy**: identify static members parent → child, execute
   static assignments and static blocks parent → child, then execute
   *only* the class you actually launched — `main` runs from the parent
   only if the child doesn't define its own.
8. **Loading the child loads the parent first; loading the parent never
   loads the child** — parent members are visible to a child by default,
   child members are not visible to the parent.
9. **Since JDBC 4.0 (Java 6), `Class.forName(...)` is no longer strictly
   required** for a compliant driver — `DriverManager` auto-discovers
   drivers via `ServiceLoader` and `META-INF/services/java.sql.Driver`. The
   static-block registration mechanism this lecture teaches is unchanged;
   only what triggers it has an alternative today.

---

**Next:** Video 062 — Instance control flow
