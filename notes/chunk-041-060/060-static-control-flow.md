# Video 060 — Static control flow

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-10 ||static control flow

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 60 of 203 |
| Series | OOPs · Part 10 |
| Topic | static control flow |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 48m 45s |
| Video ID | B_tYO3Yn61U |
| Watch | https://www.youtube.com/watch?v=B_tYO3Yn61U |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is **OOPs Part 10**, a new topic: **static control flow** — if everything
in a class is static, in *which order* do identification, assignments, static
blocks, and `main` actually run? Sir walks one `class Base` with numbered
steps 1–15, live-compiles it, then defines **direct read vs indirect read**
and **RIWO (read indirectly write only)**, then three loophole examples —
`10` then `NoSuchMethodError: main`; a compile-time `illegal forward
reference`; `0` then `NoSuchMethodError: main` — demonstrated on **JDK 1.6**,
with 1.7's changed behaviour explicitly deferred. The next lecture picks up
with a postmortem on static blocks.

---

## 00:04 — Topic: static control flow

"The most valuable topic — not a traditional one." If everything is static —
static variable, static block, static method — in which order do they
execute? That is the whole lecture.

### 00:50 — Board program: `class Base`

He starts to write `class Test`, then switches: "class Base." One class only.

```java
class Base {
    static int i = 10;

    static {
        m1();
        System.out.println("First static block");
    }

    public static void main(String[] args) {
        m1();
        System.out.println("Main method");
    }

    public static void m1() {
        System.out.println(j);
    }

    static {
        System.out.println("Second static block");
    }

    static int j = 20;
}
```

Built in this order, matching the board:

1. `static int i = 10` — static variable.
2. First static block: call `m1()`, then print `"First static block"`.
3. `public static void main(String[] args)` — call `m1()` again, then print
   `"Main method"`.
4. `public static void m1()` — also static, because it is called **directly
   from the static area**. Inside: `System.out.println(j)`. `j` is not yet
   declared — "I will declare soon."
5. Second static block: print `"Second static block"`.
6. `static int j = 20`.

### 03:31 — Everything is static; do not expect a compile error

Every member here is static — the variable, both blocks, `main`, `m1`, the
second variable. So in which order does it all run? "Don't tell compile-time
error. Perfectly the code compiles and runs fine."

The classroom guesses land on `20 / first static block / second static
block`, in various orders — all wrong. "Majority of the people, I'm sure your
answer is wrong." Two static blocks and a main method: what is the *exact*
order?

### 05:31 — Three activities when executing a Java class

Whenever a Java class runs, three things happen, always in this order:

1. **Identification of static members** from top to bottom.
2. **Execution of static variable assignments and static blocks** from top to
   bottom.
3. **Execution of the `main` method** — last.

Compiling `Base.java` produces exactly one `.class` file (`Base.class`).
Running `java Base` walks through those three activities against it.

### 08:05 — `main` is last, not first

Most people feel `main` is the starting point of program execution. "Strictly
speaking, in static control flow, `main` is the last thing which is going to
be executed." Everything static-related runs before it does.

### 08:25 — Step 1: identification (steps 1–6) and the RIWO default `0`

First activity: identify every static member, top to bottom.

1. Static variable `i`. Since it is a variable, **the JVM assigns the
   default value at the time of identification** — the initializer `10` is
   *not* run yet. `i` becomes `0`. This state is **read indirectly write
   only (RIWO)** — explained in full later.
2. First static block — identify it.
3. `main` — identify it.
4. `m1` — identify it.
5. Second static block — identify it.
6. Static variable `j` — also a variable, so `j = 0`, RIWO.

Six static members, steps **1–6**, all spent on identification alone.

### 10:38 — Step 2: assignments and static blocks (steps 7–12)

Second activity: execute static variable assignments and static blocks, top
to bottom, continuing the step count from 7.

7. Execute `i = 10`. `i` moves to **read and write** — its real value.
8. Execute the first static block: call `m1()`.
9. Inside `m1`: `System.out.println(j)`. `j`'s assignment (`j = 20`) hasn't
   run yet — its state is still the step-6 default. Prints **0**.
10. `m1()` returns; print **First static block**.
11. Next static element in source order is the second static block (`main`
    and `m1`'s own *declarations* already ran in step 1, and are not
    "variable assignment or static block" — they don't run again here).
    Print **Second static block**.
12. Execute `j = 20`. `j` is now **20**, read and write.

Steps **7–12** complete the second activity.

### 13:34 — Step 3: `main` (steps 13–15)

Third activity: run `main`.

13. `main` calls `m1()`.
14. `m1` prints `j` — now **20**.
15. Print **Main method**.

Full output, in order:

```text
0
First static block
Second static block
20
Main method
```

"I hope the terminology is very clear. If everything is static, in which
order do the things execute?" — the three steps, every time.

### 15:13 — Live compile and run: `javac Base.java` then `java Base`

```text
$ javac Base.java
$ java Base
0
First static block
Second static block
20
Main method
```

Same output the class derived by hand. One term is still abstract — **read
indirectly write only** — covered next.

### 16:43 — The three-step theory, as dictated

> *Whenever we are executing a Java class, the following sequence of steps
> will be executed as the part of static control flow.*

1. **Identification of static members from top to bottom** *(steps 1–6 in
   this example)*
2. **Execution of static variable assignments and static blocks from top to
   bottom** *(steps 7–12)*
3. **Execution of main method** *(steps 13–15)*

### 19:32 — The numbered `Base` example, board-copy

Take this down with the step numbers annotated in place, following the
sequence — "don't take blindly 7, 8, 10 and skip":

```java
class Base {
    static int i = 10;                          // 1 identify (i=0 RIWO); 7 assign i=10 (read/write)

    static {                                    // 2 identify
        m1();                                   // 8
        System.out.println("First static block"); // 10
    }

    public static void main(String[] args) {    // 3 identify; 13 run main
        m1();
        System.out.println("Main method");      // 15
    }

    public static void m1() {                   // 4 identify
        System.out.println(j);                  // 9 prints 0; 14 prints 20
    }

    static {                                    // 5 identify
        System.out.println("Second static block"); // 11
    }

    static int j = 20;                          // 6 identify (j=0 RIWO); 12 assign j=20 (read/write)
}
```

```text
0
First static block
Second static block
20
Main method
```

---

## 25:15 — Heading: Read Indirectly Write Only (RIWO)

Take special care here. Among all static members, which runs by default?
The **static block** — never called explicitly, the JVM runs it
automatically.

> `RIWO` is Sir's own exam-friendly nickname, not JLS wording. The JLS
> covers the same ground as "default value assignment" (§4.12.5) plus the
> **forward reference restriction on simple-name field access** (§8.3.3) —
> what this lecture calls "direct read."

### 25:53 — Direct read vs indirect read

- Inside a static block, reading a variable **directly** —
  `System.out.println(i)` — is a **direct read**.
- Calling a method from the static block, where *that method* reads the
  variable, is an **indirect read** — the method isn't run automatically, so
  the read only happens once you explicitly call it.

### 27:37 — Mini example: `println(i)` in the block vs. in `m1`

```java
class Test {
    static int i = 10;

    static {
        System.out.println(i); // direct read
        m1();
    }

    public static void m1() {
        System.out.println(i); // indirect read
    }
}
```

The `println(i)` sitting directly inside the static block is the **direct
read**; the `println(i)` inside `m1`, reached only through the call, is the
**indirect read**.

### 31:16 — When is a variable in RIWO state?

> *If a variable is just identified by the JVM and its original value not yet
> assigned, the variable is in read indirectly write only (RIWO) state.*

- In RIWO, **indirect read is fine**.
- In RIWO, **direct read is a compile-time error**: `illegal forward
  reference`.

Verified against `javac` — the exact message is:

```text
error: illegal forward reference
```

### 36:32 — Three loophole examples

"Take a bit special care" — three variations of `class Test`, testing
exactly this distinction.

**Example 1 — variable declared, then a static block directly reads it:**

```java
class Test {
    static int x = 10;
    static {
        System.out.println(x);
    }
}
// no main method
```

**Example 2 — static block directly reads `x` before `x` is declared:**

```java
class Test {
    static {
        System.out.println(x); // direct read, x still RIWO
    }
    static int x = 10;
}
```

**Example 3 — static block calls `m1`, `m1` reads `x` before `x` is declared:**

```java
class Test {
    static {
        m1();
    }

    public static void m1() {
        System.out.println(x); // indirect read, x still RIWO — allowed
    }

    static int x = 10;
}
// no main method
```

### 38:17 — Example 1: valid; prints `10`, then a search for `main` fails

- Identification: `x` identified, then the static block identified.
- Assignments/blocks: `x = 10` runs — `x` is now read-and-write, so a
  **direct** read is fine. `println(x)` prints **10**.
- After the static phase finishes, the JVM looks for `main`. There isn't
  one. Result (on the JDK Sir is running, 1.6): a **runtime error**,
  `NoSuchMethodError: main`.

> ❗ **Correction — this is not a "runtime exception," it's an `Error`.**
> `NoSuchMethodError` extends `IncompatibleClassChangeError` →
> `LinkageError` → `Error`, not `Exception`. It is unchecked, like a
> `RuntimeException`, but it does not sit in that hierarchy — worth the
> precise word if an interviewer asks you to place it on the exception tree.

### 39:30 — Example 2: compile error, `illegal forward reference`

- Identification: static block first, then `x`. At identification `x = 0`,
  RIWO.
- Assignments/blocks run top to bottom: the static block's `println(x)` is a
  **direct** read, but `x = 10` hasn't executed yet — `x` is still RIWO.
  Direct read + RIWO → **compile-time error: `illegal forward reference`**.
  This example never runs; it never compiles.

### 40:36 — Example 3: indirect read is fine; prints `0`, then a search for `main` fails

- Identification: `x = 0`, RIWO.
- The static block calls `m1()`. Inside `m1`, `println(x)` is an
  **indirect** read — allowed even while `x` is RIWO. Prints **0**.
- `x` is then assigned `10`. The JVM searches for `main`, doesn't find one:
  `NoSuchMethodError: main` (again, on JDK 1.6).

### 41:55 — "This explanation is with respect to Java 1.6"

"Whatever concept I'm explaining is with respect to 1.6. But in 1.7 small,
small changes are there — that part I will discuss at last." He does **not**
teach the 1.7 change in this video, and it is never picked up in a later one
in this playlist — so it is covered here instead.

> ⚠️ **Modern Java — the "no `main`" behaviour Sir demonstrates changed in
> Java 7, and stayed changed.**
> On JDK 1.6, the class is fully initialized (default values → assignments →
> static blocks) *before* the launcher looks for `main` — so a static block
> with no `main` still runs and prints, and only then does the JVM fail. From
> **Java 7 onward**, the launcher checks for a `public static void main(String[])`
> **before** it initializes the class at all. Re-running Sir's own three
> examples on a current JDK (26, verified here) confirms it:
>
> ```text
> $ java Ex1        # static int x = 10; static { println(x); }  — no main
> Error: Main method not found in class Ex1, please define the main method as:
>    public static void main(String[] args)
> or a JavaFX application class must extend javafx.application.Application
> ```
>
> No `10` is printed at all — the static block never runs. Example 3
> (indirect read, no `main`) behaves identically: no `0`, same message. Two
> things changed together:
> 1. **Timing** — the main-method check now happens *before* class
>    initialization, not after.
> 2. **Shape of the failure** — it is no longer a thrown `java.lang.Error`
>    caught by the launcher; it's a diagnostic the launcher prints directly,
>    with no stack trace to catch.
>
> Example 2 (`illegal forward reference`) is untouched by any of this — it's
> a compile-time error from `javac`, and the launcher never gets involved.

> ⚠️ **Modern Java — Java 25 removes the "must have `public static void
> main`" requirement entirely, for simple programs.**
> `JEP 512` ("Compact Source Files and Instance Main Methods"), standard
> since **Java 25**, lets a source file skip the class declaration and the
> `public static`/`String[] args` ceremony outright:
>
> ```java
> // Hello.java — compiles and runs on Java 25+, no class, no "public static", no args
> void main() {
>     System.out.println("hi");
> }
> ```
>
> Verified: `java Hello.java` on JDK 26 prints `hi` directly, no preview
> flag needed. The compiler still wraps this in an implicit top-level class
> behind the scenes, and everything this lecture teaches about static
> control flow still governs that class once you write it explicitly — this
> JEP only removes the boilerplate for small programs and teaching examples,
> it doesn't change static initialization order.

### 42:13 — Live on JDK 1.6: setting `PATH`, running all three

Sir sets the JVM explicitly to 1.6 (`PATH` to the JDK 1.6 `bin` directory)
before running the examples, precisely so the class shows the *pre-Java-7*
behaviour above.

**Example 1:** `javac Test.java` compiles fine. `java Test` prints `10`,
then `NoSuchMethodError: main`.

**Example 2:** compile-time `illegal forward reference` — "the best
example" for why declaring `x` after the static block that reads it directly
is a mistake, not just bad style.

**Example 3:** compiles fine (indirect read tolerates RIWO); `java Test`
prints `0`, then `NoSuchMethodError: main`.

---

## What this video actually taught

1. Executing a class is **three steps**: identify static members top→bottom
   (variables get defaults, RIWO); execute assignments + static blocks
   top→bottom; **then** `main`. `main` is last in static control flow.
2. The `Base` program's output is `0` / First static block / Second static
   block / `20` / Main method, because `m1` reads `j` once while `j` is
   still its default `0` (called from the first static block) and once
   after `j = 20` has run (called from `main`).
3. **Direct read** = reading a variable directly inside a static block.
   **Indirect read** = calling a method from that block, where the method
   itself reads the variable.
4. **RIWO**: identified, original value not yet assigned. Indirect read is
   fine; direct read is a compile-time `illegal forward reference`.
5. On **Java 1.6**, a class with a static block but no `main` still runs the
   static phase, then fails at runtime with `NoSuchMethodError: main`. From
   **Java 7 on**, that check moves earlier — the static phase never runs at
   all, and the failure is a printed diagnostic, not a thrown `Error`.

---

## Exam and interview points

1. **Three-step static control flow**: identification (defaults, top to
   bottom) → static variable assignments + static blocks (top to bottom) →
   `main` (last). This has not changed across any Java version.
2. **`main` is the *last* thing to run** in static control flow, not the
   first — a common exam trap, and the point of the whole `Base` walkthrough.
3. **RIWO (read indirectly write only)** is Sir's teaching name for a
   variable that has a default value but not its real one yet. Indirect
   read (through a method call) is legal; direct read is a compile-time
   `illegal forward reference`.
4. **A static block runs automatically** — it is the only static member
   that does not need to be called.
5. **`NoSuchMethodError: main` is an `Error`, not an "exception"** — unchecked,
   but on the `Error` branch of `Throwable`, not `Exception`.
6. **The "static block runs even with no `main`" behaviour is JDK-1.6-only.**
   From Java 7 onward the launcher checks for `main` *before* initializing
   the class, so the static block never runs and the failure is a printed
   message, not a thrown error — know which behaviour an interviewer is
   testing for.
7. **Since Java 25 (JEP 512), a top-level `void main() { }` with no class
   and no `public static` compiles and runs** for simple/teaching programs —
   useful to mention, but it does not change anything about static
   initialization order once a real class exists.

---

**Next:** Video 061 — static block
