# Video 058 — Coupling, Cohesion, and Object Type Casting

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-8||coupling

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 58 of 203 |
| Series | OOPs · Part 8 |
| Topic | coupling |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 33m 17s |
| Video ID | HpJTGW9AwX0 |
| Watch | https://www.youtube.com/watch?v=HpJTGW9AwX0 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Despite the title, this Part-8 lecture actually runs through three topics
end-to-end — **coupling** → **cohesion** → the start of **object type
casting**. Video 059 continues the type-casting internals.

1. Two more "advanced" OOPs features beyond overloading/overriding/inheritance/encapsulation: **coupling** and **cohesion**
2. Coupling = the degree of dependency between components; loosely vs tightly coupled
3. Classic tightly-coupled example: a static `A → B → C → D` chain
4. Three disadvantages of tight coupling: hard to enhance, kills reusability, hurts maintainability (apartment-vs-independent-house analogy)
5. Cohesion = how clearly a component's responsibility is defined; high vs low
6. Low-cohesion demo: one mega `TotalServlet`; high-cohesion redesign: separate `login.jsp` / `ValidateServlet` / `inbox.jsp` / MVC
7. Exam slogan: **loosely coupling + high cohesion = good programming practices**
8. Object type casting: two prerequisites — parent reference holding a child object, interface reference holding an implementing-class object
9. The motivating puzzle: `Object o = new String("Durga"); StringBuffer sb = (StringBuffer) o;` — valid, CE, or `ClassCastException`?
10. Cast syntax `A b = (C) d`, and the **three mantras** — two compile-time checks plus one runtime check
11. Worked examples of each mantra with `String` / `StringBuffer` / `Object`, then a `Base1`/`Base2`/`Derived1..4` hierarchy drill

---

### 00:04 — Agenda: two advanced OOPs features

Last session covered overloading, overriding, inheritance, and encapsulation —
the major OOPs concepts. Two more remain. At **basic** level they look minor;
at **advanced / framework / HLD** level (MVC, Struts, Spring, enterprise
design) they matter a lot.

| Feature | Role |
|---|---|
| Coupling | Degree of dependency between components |
| Cohesion | How cleanly each component's responsibility is defined |

Do not say encapsulation, polymorphism, and inheritance are the *only* OOPs
features — coupling and cohesion are also OOPs features, just **advanced**
ones. The basic idea is required even in this Core Java course; the deep
design use comes later at framework level.

### 01:40 — What is coupling? (measurement analogy)

In computer networks you already heard **loosely coupled** / **tightly
coupled**. Every measurable thing has a unit — height in metres, milk in
litres, weight in kilograms, temperature in °C. **Dependency** needs a
measurement too:

> **The degree of dependency between the components is called coupling.**

| Dependency | Coupling |
|---|---|
| More dependency | Tightly coupled |
| Less dependency | Loosely coupled |

Only two practical levels matter here: loosely vs tightly.

### 04:24 — Tight vs loose (board form)

> If dependency is **more**, it is considered **tight coupling**. If
> dependency is **less**, it is considered **loose coupling**.

Which is good practice? Answered after the coding example below.

### 05:50 — Classic tightly coupled example: `A` → `B` → `C` → `D`

Four components chained by static dependencies:

```java
class A {
    static int i = B.j;
}

class B {
    static int j = C.k;
}

class C {
    static int k = D.m1();
}

class D {
    public static int m1() {
        return 10;
    }
}
```

`i` is `B.j`; `j` is `C.k`; `k` is the return of `D.m1()`; `D.m1()` returns
`10`. Reading `A.i` forces the JVM to load and initialize `B`, `C`, and `D` in
turn (JLS §12.4.1 — a static field reference triggers class initialization).
**These four components are tightly coupled** — the dependency between them
is high.

```java
class TightCouplingDemo {
    public static void main(String[] args) {
        System.out.println(A.i);
        // prints 10 — verified on JDK 26
        // A depends on B, B on C, C on D — change D and everyone feels it
    }
}
```

### 08:07 — Tight coupling is the *worst* practice (apartment analogy)

**Tight coupling is the worst programming practice**, because dependency
always brings problems; independence avoids most of them.

Sir's analogy: an apartment (2/3 BHK) shares water, maintenance, the lift, and
the politics of who is president — many people to coordinate, and
restrictions on parties or lift usage. An independent house has far fewer
shared concerns. Same idea in code: **less dependency is good practice**;
**tight coupling is the worst**.

### 10:10 — Disadvantage 1: enhancement becomes difficult

In the `A`–`B`–`C`–`D` chain, if you change `D.m1()` from `return 10` to
`return 20`, everyone depending on `D` — directly or transitively — is
affected:

```java
class D {
    public static int m1() {
        return 20; // was 10 — A, B, C all see the new value
    }
}
```

You cannot modify one component without affecting the others → **enhancement
becomes difficult**.

### 11:26 — Disadvantage 2: suppresses reusability

Suppose you need only `A`'s functionality (say ~10 lines) somewhere else:

- Ask `A` to come along → `A` says fine, but **`B` must come too** (I depend on `B`).
- Ask `B` → `B` says only if **`C`** comes.
- Ask `C` → `C` says only if **`D`** comes.

To reuse 10 lines you must drag `B`, `C`, and `D` along. Faced with that risk,
most developers just **rewrite** the 10 lines instead:

```java
// Want only A's logic elsewhere — but A needs B, B needs C, C needs D.
class SomewhereElse {
    // developer rewrites the 10 lines rather than importing A+B+C+D
    static int localCopy() {
        return 10;
    }
}
```

→ **Tight coupling suppresses reusability of the code.**

### 13:48 — Disadvantage 3: maintainability goes down

Because you cannot change freely, and reuse is painful, **maintainability of
the application is reduced**. Frameworks that advertise "loose coupling" are
considered good design precisely for this reason — the terminology shows up
constantly at the design-patterns / Spring / Struts level.

> **Board:** The above components are tightly coupled with each other,
> because dependency between them is more. Tight coupling is not good
> practice, because:
>
> 1. Without affecting remaining components, we can't modify any component →
>    **enhancement becomes difficult**.
> 2. It **suppresses reusability of the code**.
> 3. It **reduces maintainability of the application**.
>
> Hence keep dependency between components **as low as possible** — that is
> **loose coupling**, and loose coupling is good programming practice.

### 21:13 — Cohesion (the next advanced OOPs feature)

Physics memory hook: cohesive forces vs adhesive forces. In design / MVC /
Spring MVC you hear **high cohesion** / **low cohesion** constantly — Spring
MVC is the textbook high-cohesion example.

### 22:13 — What is high cohesion?

Give every component a **clear, well-defined functionality**:

| Component | Job |
|---|---|
| One component | database operations |
| Another | logging |
| Another | presentation logic |
| Another | business logic |

Components with a single clear job follow **high cohesion**. A component that
is a **mixture** of unrelated responsibilities has **low cohesion**.

| Cohesion | Meaning | Practice |
|---|---|---|
| High | Clear, specialized responsibility per component | Good |
| Low | Mixed / unclear responsibilities in one component | Bad |

### 24:05 — Board form: high cohesion definition

> For every component, a clear, well-defined functionality is defined; then
> that component is said to follow **high cohesion**.

High cohesion is always good practice, for the reasons the mail-app demo
below shows.

### 25:28 — Low cohesion demo: one `TotalServlet` mail app

Design a Gmail-like mail app: login page, credential validation, inbox,
reply, compose, error page, and so on.

**Bad design:** put *everything* in one servlet — Sir's joke name,
**`TotalServlet`**:

```java
// Low cohesion — one mega-component does everything
public class TotalServlet /* extends HttpServlet */ {
    // login page display
    // validation
    // inbox page
    // reply page
    // compose page
    // error page
    // "70 lakh lines" — Sir's hyperbole for "huge"
    public void service(/* req, resp */) {
        // mixture of ALL mail-app functionalities
    }
}
```

It would *work*. Working is not the same as good design — clear,
well-defined functionality is missing, so by definition this is **low
cohesion**.

### 28:27 — Problems of low cohesion / `TotalServlet`

**1. Enhancement difficult.** Change the login page's look-and-feel every few
weeks (colours, festival images) and you have to hunt the login fragment
inside a 70-lakh-line servlet, changing it carefully for fear of side
effects.

**2. Reusability down.** Validation might be only ~10 lines, but reusing it
elsewhere means dragging the whole huge servlet — so, again, rewrite instead
of reuse.

**3. Maintainability down**, for the same reasons.

**Fix:** never put the total functionality in one servlet. Give every
functionality its own **separate component**.

### 31:03 — High cohesion redesign: separate JSP / servlet pieces

```java
// High cohesion sketch (web components as separate units)

// login.jsp          — display login page only
// ValidateServlet    — validation logic only
// inbox.jsp          — display inbox
// error.jsp          — display error
// reply.jsp          — reply UI
// compose.jsp        — compose UI
```

Flow: user opens `login.jsp`, enters username/password → submits to
**`ValidateServlet`** → success goes to `inbox.jsp`, failure goes to
`error.jsp` → from the inbox, on to `reply.jsp` / `compose.jsp` / etc. Each
component has one clear job — this is **high cohesion**.

```java
public class ValidateServlet /* extends HttpServlet */ {
    public void service(/* req, resp */) {
        // ONLY validation — success -> inbox.jsp, failure -> error.jsp
    }
}
```

### 33:05 — Advantages of high cohesion

1. Changing `login.jsp`'s look-and-feel has **no effect** on other
   components → **enhancement becomes easy**.
2. Wherever validation is needed, reuse the same `ValidateServlet` (~10 lines
   of responsibility) without rewriting → **promotes reusability**.
3. Different people can own the login / inbox / validation modules
   independently → **maintainability improves**.

**High cohesion is good programming practice.** The best design example is
**MVC**, specifically **Model-2** — born because mixing presentation logic
with business logic caused exactly these problems.

| MVC piece | Responsibility |
|---|---|
| View | Presentation logic |
| Controller | Controlling / coordinating logic |
| Model | Business logic |

That separation *is* high cohesion.

> **Board:** High cohesion is always a good programming practice, because:
>
> 1. Without affecting remaining components, we can modify any component →
>    **enhancement becomes easy**.
> 2. It **promotes reusability of the code** — wherever validation is
>    required, reuse the same `ValidateServlet` without rewriting.
> 3. It **improves maintainability of the application**.

### 42:12 — Exam note: couple these two slogans

```text
Loosely coupling  +  High cohesion  =  good programming practices
```

| Topic | Prefer |
|---|---|
| Coupling | Loose |
| Cohesion | High |

These are advanced OOPs features alongside polymorphism, encapsulation, and
inheritance. Basic OOPs courses touch them lightly; design-patterns / Spring
/ framework-level work brings them up constantly.

---

### 43:33 — Object type casting begins (three mantras)

Next topic: **object type casting** (primitive casting was already covered
under operators, video 020). Only **three mantras** — know them, and object
type casting is simple.

### 44:15 — Two prerequisites before casting

**1. A parent reference can hold a child object:**

```java
class ParentRefDemo {
    public static void main(String[] args) {
        Object o = new String("Durga");
        // Object = parent, String = child — valid
    }
}
```

**2. An interface reference can hold an implementing-class object:**

```java
class InterfaceRefDemo {
    public static void main(String[] args) {
        Runnable r = new Thread();
        // Runnable = interface, Thread = implementing class — valid
    }
}
```

> **Board:**
> ```java
> // We can use a parent reference to hold a child object.
> Object o = new String("Durga");
>
> // We can use an interface reference to hold an implemented class object.
> Runnable r = new Thread();
> ```

### 47:26 — Motivating puzzle (answer later)

```java
class CastPuzzle {
    public static void main(String[] args) {
        Object o = new String("Durga");
        StringBuffer sb = (StringBuffer) o;
        // Valid? CE? Runtime exception? Which?
    }
}
```

Polled live, almost everyone guesses "compile error." Sir's answer waits for
the three mantras. Spoiler: it **compiles, then fails at runtime** with
`ClassCastException` — confirmed below once all three checks are on the
table.

### 49:48 — Syntax of object type casting: `A b = (C) d`

```java
A b = (C) d;
```

| Symbol | Meaning |
|---|---|
| `A` | Class or interface name — type of the left-hand reference |
| `b` | Name of the reference variable |
| `C` | Class or interface name — cast / destination type |
| `d` | Reference variable being cast |

Type casting does **two activities**:

1. Convert **`d`'s object** to type **`C`**.
2. Assign that **`C`-typed** result to the **`A`-typed** reference `b`.

**The compiler checks two conditions; the JVM checks one** — three conditions
total. All three must pass for the cast to succeed.

### 54:06 — Compiler check 1 + Mantra 1 (relation between `d` and `C`)

The compiler asks: is the **conversion** even legal? The type of `d` and the
type `C` must have **some relation** — child→parent, parent→child, or the
**same type**. Otherwise it is a compile error.

> **Mantra 1 (compile-time check 1).** The type of `d` and `C` must have some
> relation (child→parent, parent→child, or same type). Otherwise: a compile
> error, historically read out as
> ```text
> inconvertible types
> found   : <type of d>
> required: <C>
> ```

(Sir says "incompatible" and "inconvertible" almost interchangeably in
speech; the classic Java 6/7 `javac` wording for a no-relation cast really
was **inconvertible types**, as a distinct message from Mantra 2's
**incompatible types** below — see the Modern Java note after both examples.)

### 58:16 — Example 1 for Mantra 1: `Object` ↔ `StringBuffer` (relation OK)

```java
class Mantra1Example1 {
    public static void main(String[] args) {
        Object o = new String("Durga");
        StringBuffer sb = (StringBuffer) o;
        // Mantra 1: Object and StringBuffer — parent/child relation → OK so far
        // (Mantras 2 and 3 decide the final fate — see below)
    }
}
```

`javac` gives **no error from Mantra 1** here — the relation exists.
Verified: this compiles clean on JDK 26.

### 59:56 — Example 2 for Mantra 1: `String` ↔ `StringBuffer` (no relation → CE)

```java
class Mantra1Example2CE {
    public static void main(String[] args) {
        String s = new String("Durga");
        StringBuffer sb = (StringBuffer) s;
        // no parent-child relation between String and StringBuffer
    }
}
```

`String` and `StringBuffer` are both direct, unrelated subclasses of
`Object` — no parent–child relation between them → **Mantra 1 fails
immediately**. Compiled on JDK 26:

```text
error: incompatible types: String cannot be converted to StringBuffer
```

### 1:03:25 — Compiler check 2 + Mantra 2 (assignment `C` → `A`)

After the object is converted to `C`, it is assigned to `A`-typed `b`. The
rule (because a parent reference can hold a child object): `C` must be
**either the same as `A`, or a derived type (child) of `A`**. Otherwise it is
a compile error.

> **Mantra 2 (compile-time check 2).** `C` must be either the same as `A` or
> a derived type of `A`. Otherwise: a compile error, historically read out as
> ```text
> incompatible types
> found   : <C>
> required: <A>
> ```

### 1:06:43 — Example 1: both compiler rules pass (runtime still decides)

```java
class Mantra2Example1 {
    public static void main(String[] args) {
        Object o = new String("Durga");
        StringBuffer sb = (StringBuffer) o;
        // Mantra 1: Object <-> StringBuffer — relation OK
        // Mantra 2: C = StringBuffer, A = StringBuffer — same type OK
        // Compiles — Mantra 3 (runtime) is checked next
    }
}
```

### 1:08:25 — Example 2: Mantra 2 fails (`(String)` into a `StringBuffer` variable)

```java
class Mantra2Example2CE {
    public static void main(String[] args) {
        Object o = new String("Durga");
        StringBuffer sb = (String) o;
        // Mantra 1: Object <-> String — relation OK
        // Mantra 2: C = String; A = StringBuffer — String is NOT same/child of StringBuffer
    }
}
```

Mantra 1 passes (`Object`/`String` are related); Mantra 2 fails, because
`String` is neither `StringBuffer` nor a subtype of it. Compiled on JDK 26:

```text
error: incompatible types: String cannot be converted to StringBuffer
```

Reminder that carries the rest of the lecture: **the compiler looks at
reference types; the JVM looks at the underlying runtime object type.**

> ⚠️ **Modern Java — the two compile-time messages have merged into one wording.**
> Sir dictates two *different* Java 6/7 diagnostics: **`inconvertible types`**
> (Mantra 1, no relation at all between `d` and `C`) with a two-line
> `found:`/`required:` block, and a separately-worded **`incompatible
> types`** (Mantra 2, related types but the wrong one for `A`), also as two
> lines. Verified against the actual compiler on JDK 26: `javac` now reports
> **both** failures with the identical single-line wording
> `incompatible types: <found> cannot be converted to <required>` — the
> "inconvertible" phrasing is gone entirely, whichever mantra actually
> failed. Both examples above were compiled to confirm this: Mantra 1's
> `String`→`StringBuffer` failure and Mantra 2's `String`→`StringBuffer`
> failure print byte-for-byte the same message text today. The **two
> underlying compile-time rules are unchanged** — only the printed wording
> collapsed into one format, sometime after this Java 6/7-era recording (by
> JDK 8, and unchanged through JDK 26). If you're asked to *name* the error
> in an interview, "inconvertible types" is still the historically correct
> term for a Mantra 1 failure — you just won't see that string in a current
> terminal.

### 1:13:38 — Mantra 3: runtime checking (`ClassCastException`)

> **Mantra 3 (runtime check).** The underlying / runtime object type of `d`
> must be either the **same as `C`** or a **derived type of `C`**. Otherwise:
> a runtime `ClassCastException`.

The compiler can pass while the JVM still fails — that gap is exactly what
the motivating puzzle exploits:

```java
class Mantra3Run {
    public static void main(String[] args) {
        Object o = new String("Durga");
        StringBuffer sb = (StringBuffer) o;
        // Mantra 1 OK (Object <-> StringBuffer)
        // Mantra 2 OK (StringBuffer <-> StringBuffer)
        // Mantra 3 FAILS: runtime object is String, not same/child of StringBuffer
    }
}
```

Run on JDK 26:

```text
Exception in thread "main" java.lang.ClassCastException: class java.lang.String
cannot be cast to class java.lang.StringBuffer (java.lang.String and
java.lang.StringBuffer are in module java.base of loader 'bootstrap')
```

> ⚠️ **Modern Java — `ClassCastException` messages now name the module and loader.**
> Sir's era wrote the short form:
> `ClassCastException: java.lang.String cannot be cast to java.lang.StringBuffer`.
> Since **Java 9**, alongside the Java Platform Module System, the JVM
> appends which module and class loader each class comes from — verified
> above on JDK 26. The core message — *what* was cast to *what* — has not changed;
> the parenthetical module/loader detail is new and genuinely useful once
> you're debugging a `ClassCastException` across two different classloaders
> (a common real-world cause the old short message couldn't distinguish).

### 1:20:11 — Example 2: all three mantras succeed

```java
class Mantra3Example2Valid {
    public static void main(String[] args) {
        Object o = new String("Durga");
        String o1 = (String) o;
        // Mantra 1: Object <-> String — relation OK
        // Mantra 2: C = String, A = String — same OK
        // Mantra 3: runtime object String <-> String — same OK
        System.out.println(o1);
    }
}
```

Compiles and runs on JDK 26, printing `Durga` — a perfectly valid cast.

### 1:22:17 — Three-mantra summary

| # | Who checks | Rule | On failure |
|---|---|---|---|
| 1 | Compiler | Type of `d` and `C` must be related (parent/child or same) | CE (Mantra 1) |
| 2 | Compiler | `C` must be same as `A`, or a child of `A` | CE (Mantra 2) |
| 3 | JVM | Runtime type of `d` must be same as `C`, or a child of `C` | `ClassCastException` |

Compiler reasons about reference types. JVM reasons about the runtime
object.

### 1:22:34 — Inheritance tree for practice casts

```text
                Object
               /      \
           Base1      Base2
          /    \      /    \
   Derived1  Derived2 Derived3  Derived4
```

```java
class Base1 { }
class Base2 { }
class Derived1 extends Base1 { }
class Derived2 extends Base1 { }
class Derived3 extends Base2 { }
class Derived4 extends Base2 { }
```

Setup shared by every case below (`Base1`/`Base2`/`Derived1..4` from the block
above are in scope in each):

```java
Base2 b = new Derived4();
// reference type: Base2
// runtime object: Derived4
```

For each cast, decide: valid / CE (which mantra) / `ClassCastException`.

### 1:23:57 — Case 1: `(Base2) b` into `Object` — valid

```java
class HierarchyCase1 {
    public static void main(String[] args) {
        Base2 b = new Derived4();
        Object o = (Base2) b;
        // Mantra 1: Base2 <-> Base2 — same, OK
        // Mantra 2: C = Base2; A = Object — Base2 is a child of Object, OK
        // Mantra 3: runtime Derived4 is a child of Base2, OK
        System.out.println(o);   // valid — verified on JDK 26
    }
}
```

### 1:26:06 — Case 2: `(Base1) b` into `Object` — CE, Mantra 1

```java
class HierarchyCase2CE {
    public static void main(String[] args) {
        Base2 b = new Derived4();
        Object o = (Base1) b;
        // Base2 (type of b) and Base1 are siblings under Object — no relation
    }
}
```

```text
error: incompatible types: Base2 cannot be converted to Base1
```

### 1:26:42 — Case 3: `(Derived3) b` into `Object` — `ClassCastException`

```java
class HierarchyCase3 {
    public static void main(String[] args) {
        Base2 b = new Derived4();
        Object o = (Derived3) b;
        // Mantra 1: Base2 <-> Derived3 — parent/child, OK
        // Mantra 2: Derived3 -> Object — OK
        // Mantra 3: runtime is Derived4, NOT same/child of Derived3 -> FAILS
        System.out.println(o);
    }
}
```

```text
Exception in thread "main" java.lang.ClassCastException: class Derived4
cannot be cast to class Derived3 (Derived4 and Derived3 are in unnamed
module of loader 'app')
```

### 1:27:28 — Case 4: `(Base1) b` into `Base2` — CE, Mantra 1 again

```java
class HierarchyCase4CE {
    public static void main(String[] args) {
        Base2 b = new Derived4();
        Base2 b1 = (Base1) b;
        // same Mantra 1 failure as Case 2 — Base1 and Base2 are unrelated
    }
}
```

```text
error: incompatible types: Base2 cannot be converted to Base1
```

### 1:27:46 — Case 5: `(Derived4) b` into `Base1` — CE, Mantra 2

```java
class HierarchyCase5CE {
    public static void main(String[] args) {
        Base2 b = new Derived4();
        Base1 b1 = (Derived4) b;
        // Mantra 1: Base2 <-> Derived4 — relation OK (Derived4 extends Base2)
        // Mantra 2: C = Derived4; A = Base1 — Derived4 is NOT same/child of Base1
    }
}
```

```text
error: incompatible types: Derived4 cannot be converted to Base1
```

### 1:28:54 — Case 6: `(Derived1) b` into `Base1` — CE, Mantra 1

```java
class HierarchyCase6CE {
    public static void main(String[] args) {
        Base2 b = new Derived4();
        Base1 b1 = (Derived1) b;
        // Base2 (type of b) and Derived1 — no relation at all
    }
}
```

```text
error: incompatible types: Base2 cannot be converted to Derived1
```

All six hierarchy cases were compiled and/or run on JDK 26 (each paired with
the `Base1`/`Base2`/`Derived1..4` declarations above in the same file) and
match exactly.

### 1:30:03 — Closing drill on the three rules

The hierarchy cases are the most valuable drill for applying all three
rules — for any cast, ask in order:

1. Is there a relation between the type of `d` and `C`? (Mantra 1)
2. Is `C` the same as, or a child of, `A`? (Mantra 2)
3. Is the runtime type of `d` the same as, or a child of, `C`? (Mantra 3)

```java
class OriginalPuzzleAnswer {
    public static void main(String[] args) {
        Object o = new String("Durga");
        StringBuffer sb = (StringBuffer) o;
        // NOT a compile error — Mantras 1 and 2 both pass
        // Runtime: ClassCastException
        // (java.lang.String cannot be cast to java.lang.StringBuffer)
    }
}
```

```java
class ContrastNoRelation {
    public static void main(String[] args) {
        String s = new String("Durga");
        StringBuffer sb = (StringBuffer) s;
        // CE (Mantra 1): incompatible types: String cannot be converted to StringBuffer
    }
}
```

```java
class ContrastValidDowncast {
    public static void main(String[] args) {
        Object o = new String("Durga");
        String s = (String) o;
        System.out.println(s);   // Durga
    }
}
```

> ⚠️ **Modern Java — pattern matching often removes the need to reason
> through all three mantras by hand.**
> Since **Java 16** (JDK 14 preview, JEP 394), `instanceof` can bind the
> checked-and-cast value directly, folding the runtime check (Mantra 3) and
> the cast into one expression with no `ClassCastException` risk:
>
> ```java
> class PatternMatchInstanceof {
>     public static void main(String[] args) {
>         Object o = new String("Durga");
>         if (o instanceof StringBuffer sb) {
>             System.out.println(sb.length());
>         } else {
>             System.out.println("not a StringBuffer");   // this branch runs — verified on JDK 26
>         }
>     }
> }
> ```
>
> This does not replace the three mantras — the compiler still runs Mantras
> 1 and 2 on the `instanceof` pattern itself, and understanding *why* a raw
> `(StringBuffer) o` cast can still blow up at runtime is exactly what makes
> this pattern worth reaching for. It is why modern code casts far less
> often than Sir's Java 6/7 codebase would have.

### 1:33:06 — End of video

That's all for this session.

---

## Exam and interview points

1. **Coupling is the degree of dependency between components.** Prefer
   **loose** coupling; **tight** coupling is the worst practice because it
   hurts enhancement, reusability, and maintainability all at once — proven
   with the static `A → B → C → D` chain.
2. **Cohesion is how clearly a single component's responsibility is
   defined.** Prefer **high** cohesion; **low** cohesion (one `TotalServlet`
   doing everything) hurts the same three things — enhancement, reuse,
   maintainability — for the mirror-image reason: too much crammed into one
   place instead of too much spread across many.
3. **Exam slogan:** *loosely coupling + high cohesion = good programming
   practices.* Both terms resurface constantly at the Spring / Struts / MVC
   level, even though the Core Java course only needs the basic idea.
4. **MVC Model-2 is the textbook high-cohesion example** — View
   (presentation), Controller (coordination), Model (business logic), kept
   apart on purpose.
5. **Object type casting rests on two prerequisites:** a parent reference can
   hold a child object (`Object o = new String(...)`), and an interface
   reference can hold an implementing-class object (`Runnable r = new
   Thread()`).
6. **Cast syntax `A b = (C) d` is governed by three mantras** — two
   compile-time (the compiler checking reference types) and one runtime (the
   JVM checking the actual object type):
   - Mantra 1: type of `d` and `C` must be related (parent/child/same), else CE.
   - Mantra 2: `C` must be same as, or a child of, `A`, else CE.
   - Mantra 3: the runtime type of `d` must be same as, or a child of, `C`, else `ClassCastException`.
7. **The classic puzzle** — `Object o = new String("Durga"); StringBuffer sb
   = (StringBuffer) o;` — **compiles** (Mantra 1: `Object` and `StringBuffer`
   are parent/child; Mantra 2: `C` and `A` are both `StringBuffer`) but
   throws `ClassCastException` **at runtime** (Mantra 3 fails: the actual
   object is a `String`, never a `StringBuffer`). The compiler cannot save
   you here because it only ever sees the *declared* type `Object`.
8. **The compiler reasons about reference types; the JVM reasons about the
   runtime object.** Every exam trick in this topic is built on that split.
9. **Modern `javac` (verified on JDK 26) no longer distinguishes "inconvertible
   types" from "incompatible types" in its wording** — both Mantra 1 and
   Mantra 2 failures now print the same `incompatible types: X cannot be
   converted to Y` single-line message. The two underlying rules Sir teaches
   are unchanged; only the diagnostic text merged, sometime after this
   Java 6/7-era recording.
10. **Modern `ClassCastException` messages (Java 9+) name the module and
    class loader of both classes involved**, not just the class names — a
    genuinely useful addition once classloader mismatches enter the picture.
11. **Pattern matching for `instanceof` (Java 16)** lets you test-and-cast in
    one expression — `if (o instanceof StringBuffer sb) { ... }` — sidestepping
    a large share of the raw-cast-plus-`ClassCastException` dance this
    lecture drills, without changing what the three mantras actually mean.

---

**Next:** Video 059 — Type casting
