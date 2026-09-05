# Video 062 — Instance control flow

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-12 || instance control flow

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 62 of 203 |
| Series | OOPs · Part 12 |
| Topic | instance control flow |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 06m 38s |
| Video ID | q4hbAd7cHuQ |
| Watch | https://www.youtube.com/watch?v=q4hbAd7cHuQ |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

OOPs Part 12, continuing straight from static block / static control flow
(video 061). Sir works through:

1. Instance control flow for a single, non-inherited class: three steps —
   identify instance members top to bottom, execute variable assignments and
   instance blocks top to bottom, execute the constructor — and the trap that
   **none of it runs** unless something calls `new`.
2. Why static control flow always runs first regardless, is a **one-time**
   event at class loading, while instance control flow repeats **for every
   object**.
3. The same three steps extended to a parent/child relationship. Identification
   still runs parent-to-child in one pass, but the assignment/block/constructor
   work does **not** interleave: the parent finishes completely (its
   assignments and blocks, then its constructor) before the child starts.
4. Numbered traces of both scenarios — single class: steps 1–16; parent/child:
   steps 1–28 — pinning exact print order, including the classic "prints `0`"
   trap when an instance block calls a method that reads a field whose
   initializer hasn't run yet.

Mixing instance and static control flow together in one class is deferred to
video 063.

---

## 00:05 — Single-class instance control flow (no inheritance)

Last session covered **static control flow**: if everything in a class is
static, what order do things run in? This session is the instance version —
instance variables, instance methods, instance blocks, and a constructor —
and, more importantly, **whether they run at all**.

### 01:03 — Board example: class `Test`

```java
class Test {
    int i = 10;

    {
        m1();
        System.out.println("First instance block");
    }

    Test() {
        System.out.println("Constructor");
    }

    public static void main(String[] args) {
        System.out.println("main");
    }

    public void m1() {
        System.out.println(j);
    }

    {
        System.out.println("Second instance block");
    }

    int j = 20;
}
```

Members, top to bottom: instance variable `i`; an instance block that calls
`m1()`; a constructor; the lone **static** member, `main`; instance method
`m1()` (printing a field `j` not declared until later); a second instance
block; instance variable `j`. Note that `main` still contains no `new Test()`
— that comes next.

### 04:01 — The class's guess, and why it is wrong

Asked to predict the output, a student says the first line will be `0` —
correctly remembering **RIWO** (Read Indirectly Write Only) from the
static-control-flow session: a field read before its own initializer runs
still holds its default value. Full class guess:

```text
0
First instance block
Second instance block
Constructor
main
```

That is the right order — *if* an object gets created. Nobody has created one
yet, and that is the trap about to spring.

### 05:08 — Why the real default output is only `main`

Whenever a Java class runs, **static control flow starts first**, unconditionally:

1. Identify static members, top to bottom.
2. Execute static variable assignments and static blocks, top to bottom.
3. Execute `main`.

**Instance members are identified only when an object is created.** `Test`
has exactly one static member (`main`) and creates no object anywhere in it,
so step 2 is empty and step 3 just prints `"main"` — the instance block,
constructor, and `m1()` never even get identified, let alone run.

```java
class DemoNoObject {
    {
        System.out.println("instance block — will NOT run");
    }

    DemoNoObject() {
        System.out.println("constructor — will NOT run");
    }

    public static void main(String[] args) {
        System.out.println("main");
    }
}
```

```text
// java DemoNoObject
main
```

### 06:16 — Confirmed live: typed, compiled, run

The same board program, typed into the editor. `javac Test.java` compiles
cleanly; `java Test` prints only `main` — no object, no instance activity,
exactly as predicted.

### 07:32 — Creating an object starts the instance story

Add one line to `main`:

```java
public static void main(String[] args) {
    Test t = new Test();
    System.out.println("main");
}
```

The instinct is "constructor runs, then main." Sir heads that off: **every
object creation also runs the instance blocks** — first block, second block,
*then* the constructor.

### 08:30 — The three steps of instance control flow

Whenever static control flow (specifically, its step 3 — executing `main`)
creates an object, this sequence runs **for every object creation**:

1. Identification of instance members, top to bottom.
2. Execution of instance variable assignments and instance blocks, top to bottom.
3. Execution of the constructor.

Object creation is complete once the constructor finishes. **Static control
flow is a one-time activity, performed at class loading. Instance control flow
is not one-time — it runs for every `new`.**

### 11:26 — Minimal demo of the three steps

```java
class InstanceControlFlowSteps {
    // 1. identification of instance members (top → bottom)
    int i = 10;                          // identified, then later assigned
    { System.out.println("block"); }     // identified, then later executed
    InstanceControlFlowSteps() {         // identified, executed LAST
        System.out.println("Constructor");
    }
    public static void main(String[] args) {
        new InstanceControlFlowSteps();  // this line STARTS the 3 steps
        System.out.println("main");
    }
}
```

```text
block
Constructor
main
```

> ⚠️ **Modern Java — records don't have this three-step model at all.**
> Since **Java 16**, a `record` cannot declare an instance initializer block —
> it is a flat compile error:
>
> ```java
> record Point(int x, int y) {
>     {
>         System.out.println("block");   // CE: instance initializers not allowed in records
>     }
> }
> ```
>
> A record's fields are all assigned inside its (compact or canonical)
> constructor, in one place, with no separate "identification, then later
> assignment" phase for anything to observe. That is deliberate: records are
> transparent data carriers, and the language closes off the exact
> half-initialized state (RIWO) this lecture spends an hour exploring. The
> three-step model above still applies to every ordinary `class` — this is a
> restriction specific to `record`.

### 14:09 — Static flow is the base; instance flow nests inside `new`

Static control flow stays the outer frame. Its step 3 — executing `main` — is
*where* `new` gets called, and each `new` triggers the instance sequence
inline, before control returns to the rest of `main`.

### 15:07 — Full numbered trace (steps 1–16)

**Base flow = static control flow.** Step 1: identify static members — only
`main`. Step 2: execute static variable assignments/blocks — none. Step 3:
execute `main`. Inside `main`, `Test t = new Test();` is where the "cinema"
starts — numbered as overall **step 2**.

```java
class Test {
    int i = 10; // 3: i=0 RIWO     9: i=10 R&W

    {           // 4: identified
        m1();   // 10: call m1
        System.out.println("First instance block"); // 12
    }

    Test() {    // 5: identified   15: execute
        System.out.println("Constructor");
    }

    public static void main(String[] args) { // 1: identified
        Test t = new Test();                 // 2: cinema starts
        System.out.println("main");          // 16
    }

    public void m1() { // 6: identified
        System.out.println(j); // 11: j still 0
    }

    { // 7: identified   13: execute
        System.out.println("Second instance block");
    }

    int j = 20; // 8: j=0 RIWO     14: j=20 R&W
}
```

**Instance CF step 1 — identification of instance members, top to bottom
(overall 3–8):**

| Overall | Member | After identification |
|---|---|---|
| 3 | `int i = 10` | `i = 0`, RIWO |
| 4 | first instance block | identified |
| 5 | constructor | identified |
| 6 | `m1()` | identified |
| 7 | second instance block | identified |
| 8 | `int j = 20` | `j = 0`, RIWO |

RIWO = Read Indirectly Write Only: the default value (`0` for `int`) has been
assigned. Another method can **read** it; the explicit `= 10` / `= 20` has not
run yet.

**Instance CF step 2 — execution of instance variable assignments and instance
blocks, top to bottom (overall 9–14):**

| Overall | Action |
|---|---|
| 9 | `i = 10` — now Read and Write |
| 10 | first instance block starts → calls `m1()` |
| 11 | `m1` prints `j` — still `0` (RIWO, its own assignment hasn't run) |
| 12 | print `"First instance block"` |
| 13 | second instance block → print `"Second instance block"` |
| 14 | `j = 20` — now Read and Write |

**Instance CF step 3 — execution of the constructor (overall 15):** prints
`"Constructor"`. Object creation is now complete; control returns to `main`
for the remaining statement — overall **step 16**, printing `"main"`.

**Full traced output, verified by compiling and running the program above:**

```text
// javac Test.java && java Test
0
First instance block
Second instance block
Constructor
main
```

The "cinema" started at step 2 (`new Test()`); execution comes back to `main`
only at step 16.

### 20:06 — Comment out the object, and it collapses back to `main`

Same file, `Test t = new Test();` commented out:

```java
public static void main(String[] args) {
    // Test t = new Test();  // commented
    System.out.println("main");
}
```

```text
main
```

One line — the `new` — is responsible for every other line of output. Sir
also relabels that line as **"line 1"** going forward: comment line 1, and
the output is just `main`; keep it, and the full instance sequence runs.

### 21:13 — "Object creation is the most costly operation"

Sir's framing: the "cinema" started at step 2 and only returned at step 16 —
that is a lot of machinery for one `new`. His conclusion: **don't create an
object without a specific requirement**; unnecessary objects drag performance
down.

> ❗ **Correction — "most costly operation" overstates it, then and now.**
> *Allocating* an object in HotSpot is not expensive by default — it is
> typically a bump-pointer write into a thread-local allocation buffer (TLAB),
> and if the object provably never escapes the method (as in the loop below),
> **escape analysis** (on by default since JDK 6 update 23, i.e. already
> current when this was recorded) can eliminate the allocation entirely via
> scalar replacement:
>
> ```java
> static Point alloc(int i) { return new Point(i); }   // never escapes alloc()
> // 50,000,000 calls in a tight loop: ~35ms on a current JDK
> ```
>
> What genuinely *is* expensive is whatever work the constructor, instance
> blocks, and field initializers actually do — I/O, big computation, another
> `new` inside them. "Avoid needless objects" remains sound advice; "object
> creation is the most costly operation in Java" is folklore that doesn't
> survive contact with the JIT.

### 27:11 — A second object: all three steps repeat

After `println("main")`, one more `new Test()`:

```java
class Test {
    int i = 10;
    {
        m1();
        System.out.println("First instance block");
    }
    Test() {
        System.out.println("Constructor");
    }
    public static void main(String[] args) {
        Test t = new Test();
        System.out.println("main");
        Test t1 = new Test();
    }
    public void m1() {
        System.out.println(j);
    }
    {
        System.out.println("Second instance block");
    }
    int j = 20;
}
```

```text
0
First instance block
Second instance block
Constructor
main
0
First instance block
Second instance block
Constructor
```

All three activities repeat for the second object — not just the constructor.
**Instance control flow is not a one-time activity; it happens for every
object creation.**

### 28:41 — Two notes to keep

**One-time vs. every object:**

> *Static control flow is a **one-time activity**, performed **at the time of
> class loading**. Instance control flow is **not** one-time — it is performed
> **for every object creation**.*

```java
class OnceVsEvery {
    static {
        System.out.println("static block — class loading, once");
    }
    {
        System.out.println("instance block — every new");
    }
    OnceVsEvery() {
        System.out.println("constructor — every new");
    }
    public static void main(String[] args) {
        new OnceVsEvery();
        new OnceVsEvery();
    }
}
```

```text
static block — class loading, once
instance block — every new
constructor — every new
instance block — every new
constructor — every new
```

**Cost:** *object creation is the most costly operation; don't create one
without a specific requirement* — see the correction above for how far that
claim actually holds today.

---

## 31:31 — Instance control flow in a parent-to-child relationship

The single-class story is done. Now: if it's parent-to-child, and we create a
**child object**, in what sequence do the activities run?

### 32:53 — Parent class on the board

```java
class Parent {
    int i = 10;

    {
        m1();
        System.out.println("Parent instance block");
    }

    Parent() {
        System.out.println("Parent constructor");
    }

    public static void main(String[] args) {
        Parent p = new Parent();
        System.out.println("Parent main");
    }

    public void m1() {
        System.out.println(j);
    }

    int j = 20;
}
```

Same shape as the single-class example, with one difference: only one
instance block in `Parent` — the multi-block behavior is already established,
so the second block is saved for `Child`.

### 35:29 — Child class on the board

```java
class Child extends Parent {
    int x = 100;

    {
        m2();
        System.out.println("Child first instance block");
    }

    Child() {
        System.out.println("Child constructor");
    }

    public static void main(String[] args) {
        Child c = new Child();
        System.out.println("Child main");
    }

    public void m2() {
        System.out.println(y);
    }

    {
        System.out.println("Child second instance block");
    }

    int y = 200;
}
```

`Child` gets its own two instance blocks (matching the original `Test`
shape), its own field/method pair (`x`/`m2`/`y`), and its own constructor
string — kept distinct from `Parent`'s (`"Parent constructor"` vs. `"Child
constructor"`) so the eventual trace isn't ambiguous. Both classes live in one
file, saved as `Parent.java`.

### 38:00 — Two `.class` files; run `java Child`

`javac Parent.java` produces **two** class files: `Parent.class` and
`Child.class`. Then: `java Child`.

Whenever any class runs — child, parent, or standalone — the **first** flow
is always static control flow, never instance control flow.

### 38:55 — Static control flow in parent-to-child (recall)

From the previous session, static control flow with inheritance runs:

1. Identification of static members, **parent to child**.
2. Execution of static variable assignments and static blocks, **parent to child**.
3. Execution of the class named on the command line — here, **`Child`'s** `main`.

`Parent`'s `main` gets identified (because loading `Child` loads `Parent`
first) but is never executed for `java Child`. Inside `Child.main`, creating a
child object is what kicks off everything below.

### 40:36 — Five steps when creating a child object

This is the important difference from the single-class case. Whenever a
**child class object** is created:

1. **Identification of instance members, parent to child.**
2. **Execution of instance variable assignments and instance blocks, only in the parent class.**
3. **Execution of the parent constructor.**
4. **Execution of instance variable assignments and instance blocks in the child class.**
5. **Execution of the child constructor.**

Only step 1 runs "parent to child" in a single pass. Everything after that is
**parent completely, then child completely** — not interleaved member by
member.

```java
class Parent {
    int i = 10;
    {
        m1();
        System.out.println("Parent instance block");
    }
    Parent() {
        System.out.println("Parent constructor");
    }
    public void m1() {
        System.out.println(j);
    }
    int j = 20;
}

class Child extends Parent {
    int x = 100;
    {
        m2();
        System.out.println("Child first instance block");
    }
    Child() {
        System.out.println("Child constructor");
    }
    public static void main(String[] args) {
        Child c = new Child(); // these 5 steps run here
        System.out.println("Child main");
    }
    public void m2() {
        System.out.println(y);
    }
    {
        System.out.println("Child second instance block");
    }
    int y = 200;
}
```

### 45:15 — Step 1: identification, parent then child (overall 4–14)

Static identification/`new` already used overall steps 1–3 (identify
`Parent.main`, identify `Child.main`, hit `new Child()`). Instance
identification continues from there — parent members first, then child's:

| Overall | Member | After identification |
|---|---|---|
| 4 | `int i` | `i = 0`, RIWO |
| 5 | parent instance block | identified |
| 6 | parent constructor | identified |
| 7 | `m1()` | identified |
| 8 | `int j` | `j = 0`, RIWO |
| 9 | `int x` | `x = 0`, RIWO |
| 10 | child first instance block | identified |
| 11 | child constructor | identified |
| 12 | `m2()` | identified |
| 13 | child second instance block | identified |
| 14 | `int y` | `y = 0`, RIWO |

`j`, `x`, and `y` are three separate fields, each getting its own default
value. Identification runs parent-to-child across steps **4–14**.

### 47:41 — Step 2: parent's own assignments and blocks (overall 15–19)

| Overall | Action |
|---|---|
| 15 | `i = 10` — R&W |
| 16 | parent instance block calls `m1()` |
| 17 | `m1` prints `j` → `0` (still RIWO) — **first line of output** |
| 18 | print `"Parent instance block"` |
| 19 | `j = 20` — R&W |

Nothing from `Child` runs yet — this step is parent-only.

### 49:43 — Step 3: parent constructor (overall 20)

One activity: `"Parent constructor"` prints.

### 50:16 — Step 4: child's own assignments and blocks (overall 21–26)

| Overall | Action |
|---|---|
| 21 | `x = 100` — R&W |
| 22 | child first instance block calls `m2()` |
| 23 | `m2` prints `y` → `0` (original value, not yet `200`) |
| 24 | print `"Child first instance block"` |
| 25 | print `"Child second instance block"` |
| 26 | `y = 200` — R&W |

### 52:05 — Step 5: child constructor (27), then back to `Child.main` (28)

Child constructor prints `"Child constructor"` — overall step **27**. The
cinema that began at step 3 (`Child c = new Child();`) is now finished; control
returns to the rest of `main` — step **28**, `"Child main"`.

**Full output for `java Child`, verified by compiling and running the pair above:**

```text
// javac Parent.java && java Child
0
Parent instance block
Parent constructor
0
Child first instance block
Child second instance block
Child constructor
Child main
```

`Parent.main` never runs for `java Child` — only `Parent main` being absent
from that list is the proof.

### 53:25 — Live demo: a typo, and two contrasting runs

Live-typed as `Parent1.java` / `Child1 extends Parent1` (renamed to dodge a
name clash with the board example). Mid-demo he mistypes the child variable's
declared type as `C` instead of `Child1` — fixed to `Child1 c = new
Child1();` — a reminder that the declared type on the left must be the actual
class, not a guess at a shorter name.

Compiling `Parent1.java` and running `java Child1` reproduces the trace above
exactly. Two contrasts worth keeping:

**Run the parent's own entry point instead** — `java Parent1` never loads
`Child1` at all (loading a parent never loads its children), so only a
`Parent1` object gets built:

```text
// java Parent1
0
Parent instance block
Parent constructor
Parent main
```

**Comment out the `new` in `Child1.main`** — static identification of both
classes still happens, but no instance cinema runs:

```java
class Child1 extends Parent1 {
    public static void main(String[] args) {
        // Child1 c = new Child1();
        System.out.println("Child main");
    }
}
```

```text
// java Child1
Child main
```

### 55:46 — The five steps, dictated with this example's numbers

> *Whenever we are creating a **child class object**, the following sequence
> of events is performed **automatically** as part of instance control flow:*
>
> 1. Identification of instance members from parent to child. *(steps **4–14**)*
> 2. Execution of instance variable assignments and instance blocks **only in
>    the parent class**. *(**15–19**)*
> 3. Execution of the parent constructor. *(**20**)*
> 4. Execution of instance variable assignments and instance blocks **in the
>    child class**. *(**21–26**)*
> 5. Execution of the child constructor. *(**27**)*
>
> The remaining `Child.main` print is step **28**.

### 1:02:51 — Only `Child`'s `main` runs — `Parent`'s never does

Because the command is `java Child`, **only `Child`'s `main` executes**;
`Parent`'s is identified and nothing more. This follows directly from last
session's class-loading rule, now shown with static blocks added so the
loading order itself is visible too:

```java
class Parent {
    static {
        System.out.println("Parent static");
    }
    public static void main(String[] args) {
        System.out.println("Parent main");
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

```text
// java Child
Parent static
Child static
Child main
// (Parent main is identified, never executed)

// java Parent
Parent static
Parent main
// (Child class not loaded — loading a parent never loads its children)
```

Loading `Child` always loads `Parent` first (a child needs its parent's
members); loading `Parent` never loads `Child` (a parent has no idea a child
exists).

### 1:04:26 — Closing recap

Sir restates the five steps once more for the notes, alongside the same
`java Child` output from 52:05 above (`0` / `Parent instance block` / `Parent
constructor` / `0` / `Child first instance block` / `Child second instance
block` / `Child constructor` / `Child main`) — no new example, just
reinforcement that this exact order is what the exam expects.

### 1:05:54 — Next session

Take special care with what "executing the child class" actually triggers
internally — that is today's whole point. Next video mixes instance control
flow **and** static control flow together in one class, with fresh examples;
that material is not covered here.

---

## Exam and interview points

1. **Instance members are identified only when an object is created.** A
   class full of instance blocks, a constructor, and instance methods, run
   with no `new` anywhere, prints nothing from any of them — only `main`
   (assuming `main` is the sole static member).
2. **The three single-class steps, in order:** identify instance members top
   to bottom → execute instance variable assignments and instance blocks top
   to bottom → execute the constructor. The constructor always runs **last**,
   even though it's usually declared right after the fields.
3. **Static control flow is one-time, at class loading. Instance control flow
   runs once per `new`.** Two objects of the same class run the full
   three-step sequence twice.
4. **RIWO (Read Indirectly Write Only):** a field's default value (`0`,
   `null`, `false`, …) exists as soon as it's identified. Code that runs
   before that field's own initializer line — e.g., an earlier instance block
   calling a method that reads it — sees the default, not the eventual value.
5. **Five steps for a child object**, and only step 1 runs parent-to-child in
   one pass:
   1. Identify instance members, parent → child.
   2. Execute instance variable assignments and instance blocks, **parent
      only**.
   3. Execute the parent constructor.
   4. Execute instance variable assignments and instance blocks, **child
      only**.
   5. Execute the child constructor.
6. **`java Child` never executes `Parent.main`** — only the `main` of the
   class named on the command line runs; the other class's `main` is merely
   identified because loading a child always loads its parent first.
7. **Loading a parent never loads a child.** `java Parent` doesn't touch
   `Child` at all, even if `Child extends Parent` exists in the same source
   file.
8. **"Object creation is expensive" is a simplification, not a fact about the
   JIT.** Allocation itself is cheap (TLAB bump-pointer, and often eliminated
   entirely by escape analysis); what's expensive is whatever real work the
   constructor and initializers actually do. For the OCJP exam the teaching
   point survives: don't create objects you don't need.
9. **Records (Java 16+) skip this whole model.** A `record` cannot declare an
   instance initializer block — all field assignment happens in one place,
   the canonical/compact constructor — precisely to avoid the half-initialized
   states (RIWO) this lecture traces in such detail.

---

**Next:** Video 063 — Instance + static control flow (mixed)
