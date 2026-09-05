# Video 069 — Constructors (Default + Overloading)

## Video info

**Title:** Constructors in java | default constructor | Constructor Overloading

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 69 of 203 |
| Series | Constructors (standalone / compilation-style lecture) |
| Topic | default constructor, constructor overloading |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 2h 27m 05s |
| Video ID | Jll2gxAdfxI |
| Watch | https://www.youtube.com/watch?v=Jll2gxAdfxI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

A long standalone pass through constructors, expected to be worth **2–4**
questions on the certification exam. It heavily overlaps three shorter
playlist videos — **064** (constructors intro/rules), **065** (default
constructor), **066** (overloaded constructors) — but works through every
case with full board demonstrations rather than a quick pass, so it is kept
here in full:

1. Why constructors exist — objects created without initialization
2. The two rules every constructor obeys (name, no return type)
3. Which access modifiers a constructor can take
4. The compiler-generated default constructor and its three-rule prototype
5. `super()`/`this()` as constructor calls vs. `super`/`this` as keywords
6. Constructor overloading and chaining
7. Why constructors don't inherit or override
8. Where constructors are legal (class, abstract class) and illegal (interface)
9. Recursive constructor invocation vs. recursive method calls
10. Parent constructors, implicit `super()`, and checked exceptions

---

## 00:11 — Why constructors? A student without initialization

After OO features (including typecasting), the next exam-heavy topic is
**constructors**.

Board: every student must have a **name** and a **roll number**.

```java
class Student {
    String name;
    int rollNumber;
}
```

Create many objects without assigning values:

```java
class Student {
    String name;
    int rollNumber;

    public static void main(String[] args) {
        Student s1 = new Student();
        Student s2 = new Student();
        // … imagine 600 Student objects
    }
}
```

For every object the JVM allocates a **separate copy** of the instance
variables and fills in **default values**:

- `name` (`String`) → `null`
- `rollNumber` (`int`) → `0`

Ask any of the 600 students their details and you get "my name is null, my
roll number is 0" — meaningless. An object created without initialization
cannot do useful work; it needs distinct values (Durga/101, Ravi/102,
Shiva/103) before it is meaningful. **Initializing instance variables is
compulsory** for an object to be useful.

### 06:10 — Who initializes? The purpose of a constructor

Something has to perform that initialization: the **constructor**. Its job
is to **initialize an object**, not to create it — it runs immediately after
object creation finishes.

First sketch of a `Student` constructor (rules covered in detail below):

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }
}
```

Rules preview: the constructor's name equals the class name, its parameters
match what must be initialized, and `this.name = name` assigns the argument
into the instance field. IDEs (Eclipse/NetBeans) can generate a constructor
for you, but the syntax itself is fixed.

### 09:16 — Creating objects with constructor arguments

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }

    public static void main(String[] args) {
        Student s1 = new Student("Durga", 101);
    }
}
```

**Misconception killed:** "a constructor's main purpose is to create the
object." Wrong — the constructor's job is to **initialize**; `new` **creates**.

### 10:39 — The full story of one `new` line

For `Student s1 = new Student("Durga", 101);`, three things happen in order:

1. `new` creates the `Student` object.
2. The constructor performs initialization.
3. The reference is stored in `s1`.

Walked through in detail: `new` first allocates the object with separate
copies of `name` and `rollNumber`, and the JVM fills them with defaults
(`null`, `0`) — **the constructor has not run yet**. Only then does the
constructor call `Student("Durga", 101)` execute: the arguments bind, and
`this.name = name` / `this.rollNumber = rollNumber` overwrite the defaults
with `"Durga"` and `101`. `this` refers to the object the constructor is
currently running on.

A second object follows the identical path:

```java
Student s2 = new Student("Ravi", 102);
```

`new` allocates and defaults, then the constructor replaces the defaults
with `"Ravi"`/`102`. Two objects, two independent runs of the same
constructor — its purpose is initialization, never creation.

### 18:21 — Executable `Student` demo

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }

    public static void main(String[] args) {
        Student s1 = new Student("Durga", 101);
        Student s2 = new Student("Ravi", 102);
        System.out.println(s1.name + " " + s1.rollNumber);
        System.out.println(s2.name + " " + s2.rollNumber);
    }
}
```

```text
Durga 101
Ravi 102
```

Two objects means the constructor executes **twice**, once per object.

### 21:37 — How many times does a constructor run?

A constructor runs **after** object creation, **once per object**. Ten
`new` calls run it ten times:

```java
class Test {
    Test() {
        System.out.println("constructor");
    }

    public static void main(String[] args) {
        Test t1 = new Test();
        Test t2 = new Test();
        Test t3 = new Test();
    }
}
```

```text
constructor
constructor
constructor
```

A fourth `new Test()` would print a fourth line.

---

## 26:00 — Rule 1: constructor name must equal class name

```java
class Test {
    Test() {
        // constructor
    }
}
```

## 27:26 — Rule 2: no return type — not even `void`

A constructor runs **automatically** on `new`; you never call it like a
method. So the return-type concept simply does not apply to it, `void`
included.

**Trap:** write `void` by mistake and the compiler treats the member as a
plain **method**, not a constructor:

```java
class Test {
    void Test() {
        System.out.println("Hello");
    }

    public static void main(String[] args) {
        Test t1 = new Test();
        Test t2 = new Test();
    }
}
```

```text
(nothing prints — void Test() is a method; new never auto-runs it)
```

If `Test()` were really a constructor, "Hello" would print twice. It does
not, which proves it is an ordinary method — one you'd have to call explicitly:

```java
class Test {
    void Test() {
        System.out.println("Hello");
    }

    public static void main(String[] args) {
        Test t1 = new Test();
        t1.Test(); // ordinary method call
    }
}
```

```text
Hello
```

A method whose name happens to equal the class name is **legal but not
recommended** — it compiles, but it confuses anyone expecting `Test()` to be
the constructor.

Rules so far: (1) constructor name = class name; (2) no return type, not even
`void` — write one and you've declared a method instead.

---

## 35:14 — Which modifiers apply to a constructor?

Java has roughly a dozen modifiers overall, but only **four** apply to a
constructor:

```java
public Test() { }      // valid
Test() { }             // default (no modifier) — valid
protected Test() { }   // valid
private Test() { }     // valid
```

Everything else — `final`, `static`, `abstract`, `native`, `synchronized`,
`strictfp` — is a compile error:

```java
class Test {
    final Test() { }
}
// CE: modifier final not allowed here
```

```java
class Test {
    static Test() { }
}
// CE: modifier static not allowed here
```

```java
class Test {
    synchronized Test() { }
}
// CE: modifier synchronized not allowed here
```

Verified against `javac` (26): the same is true for `abstract` and `native`
(`modifier abstract/native not allowed here`).

Access meaning, at a glance:

| Modifier | Object can be created from… |
|---|---|
| `public` | anywhere — same package or another |
| default (no modifier) | the same package only |
| `protected` | the same package, or a child class outside it |
| `private` | only inside that class |

**Private constructors** are how **singleton** classes (only ever one
instance) restrict object creation from outside — the pattern behind
`DateFormat`/`NumberFormat`-style factories. Video **067** covers singleton
in depth.

---

## 40:41 — The default constructor

Does an empty class contain a constructor?

```java
class Test {
}
```

**Yes.** The programmer wrote none, so the **compiler** inserts a **default
constructor** at compile time.

- Every class — including **abstract** classes — has a constructor. No class
  exists without one.
- The **compiler** generates it, never the JVM. (Verified: `javac` inserts it
  at compile time; some third-party material wrongly attributes this to the
  JVM.)
- It is generated **only if the class declares no constructor at all**. Write
  even one, and the compiler adds nothing:

```java
class Test {
    Test(int i) {
    }
}
// no default constructor generated — a constructor already exists
```

A class never has both a "default" one and a custom one — either you wrote
none and the compiler supplies exactly one, or you wrote at least one and the
compiler supplies none. An abstract class follows the same rule: it can
(and, per the discussion below, often should) declare a constructor.

### 46:22 — The default constructor's prototype (three rules)

1. It is always a **no-arg** constructor.
2. Its access modifier matches the **class's** modifier: a `public` class
   gets `public Test()`; a default (package-private) class gets a
   package-private `Test()`. (A top-level class can't be `private` or
   `protected`, so those cases never arise; other modifiers like `final` or
   `static` aren't constructor modifiers anyway.)
3. Its body contains exactly **one line**: `super();` — a no-arg call to the
   superclass constructor.

An important distinction:

```java
class Test {
    Test() {
    }
}
```

This is a no-arg constructor **you wrote**, not a default one. "Default"
means *only* the one the compiler itself generates.

> *A default constructor is always no-arg, but not every no-arg constructor
> is a default constructor.*

What the compiler actually inserts for an empty class:

```java
class Test {
    Test() {
        super();
    }
}
```

### 52:18 — Programmer code vs. compiler code, case by case

"P-code" is what you write; "C-code" is what the compiler generates on top of it.

**Case A — empty default class**

```java
// P-code
class Test {
}
```
```java
// C-code
class Test {
    Test() {
        super();
    }
}
```

**Case B — public empty class**

```java
// P-code
public class Test {
}
```
```java
// C-code
public class Test {
    public Test() {
        super();
    }
}
```

**Case C — a method that shares the class's name (returns `void`)**

```java
// P-code
class Test {
    void Test() {
    }
}
```
```java
// C-code — default constructor is still added; the method stays too
class Test {
    Test() {
        super();
    }

    void Test() {
    }
}
```

No real constructor was written here — `void Test()` is a method — so the
compiler's default-constructor rule still fires.

**Case D — a no-arg constructor with an empty body**

```java
// P-code
class Test {
    Test() {
    }
}
```

The compiler does **not** add a second constructor. It does, however, still
guarantee that every constructor's first line is a `super(...)` or
`this(...)` call — writing neither gets you an inserted `super();`:

```java
// C-code
class Test {
    Test() {
        super(); // inserted by the compiler
    }
}
```

**Case E — overloaded constructors, one chaining via `this()`**

```java
// P-code
class Test {
    Test(int i) {
        this();
    }

    Test() {
    }
}
```
```java
// C-code
class Test {
    Test(int i) {
        this();
    }

    Test() {
        super(); // inserted
    }
}
```

**Case F — the programmer already wrote `super()`**

```java
// P-code / C-code — identical, nothing extra generated
class Test {
    Test(int i) {
        super();
    }
}
```

Summary: a default constructor appears only when **no** constructor is
written; its shape is always no-arg / class-access / `super();`-only body.
Every constructor's first line, meanwhile, must be `super(...)` or
`this(...)` — and the compiler inserts `super();` for you if you wrote
neither.

---

## 1:05:06 — `super`/`this` as constructor calls: case studies

**Case 1 — `super()` not the first statement**

```java
class Test {
    Test() {
        System.out.println("constructor");
        super(); // CE, pre-Java 25 — not the first statement
    }
}
```

```text
CE: call to super must be first statement in constructor
```

Fix: put `super();` first.

```java
class Test {
    Test() {
        super();
        System.out.println("constructor");
    }
}
```

> ⚠️ **Modern Java — "first statement" stopped being absolute in Java 25.**
> JEP 513, *Flexible Constructor Bodies*, finalized in **Java 25** (preview
> in 22–24 as JEP 447/482/492). A constructor may now contain statements
> *before* the `super(...)`/`this(...)` call, as long as those statements do
> not read or write the instance under construction (no `this`, no instance
> field, no instance method call — `static` members and local variables are
> fine). Verified directly:
>
> ```java
> class Test {
>     Test() {
>         System.out.println("before super"); // now legal
>         super();
>     }
> }
> ```
>
> `javac --release 24` and earlier reject this
> (`flexible constructors is not supported in -source 24`); `javac --release 25`
> and `26` accept it. Two things stay exactly as Sir describes even on Java
> 25+: you still can't reference `this`/instance state before the call
> (`reference to val may only appear after an explicit constructor
> invocation`), and wrapping the call itself in `try`/`catch` still fails
> (see the checked-exception case study near the end of this note) — the
> call must still stand as its own top-level statement. For the OCJP exam
> this course targets, and for any codebase compiled below Java 25, treat
> "first statement, no exceptions" as the rule.

**Case 2 — both `super()` and `this()`**

```java
class Test {
    Test() {
        super();
        this(); // CE — cannot use both
        System.out.println("constructor");
    }
}
```

```text
CE: call to this must be first statement in constructor
```

You may use **either** `super(...)` **or** `this(...)`, never both — this
part is unaffected by JEP 513; a modern compiler now phrases it as
`redundant explicit constructor invocation`, but the rule (at most one
delegating call) is identical.

**Case 3 — `super()` called from an ordinary method**

```java
class Test {
    public void m1() {
        super(); // CE — not inside a constructor
        System.out.println("method");
    }
}
```

```text
CE: call to super must be first statement in constructor
```

`super(...)`/`this(...)` can only appear inside a constructor, calling
another constructor — never from an ordinary method. (A current compiler
phrases the same restriction as `explicit constructor invocation may only
appear within a constructor body`.)

### 1:19:06 — Rules for `super()`/`this()` constructor calls

| Rule | Detail |
|---|---|
| Where | Only inside a constructor |
| Position | The delegating call itself must be a standalone statement — no longer required to be literally first (Java 25+); still must be first in legacy code / the exam rule |
| How many | Only one — either `super(...)` or `this(...)`, never both |

Exam loophole territory.

### 1:21:00 — `super`/`this` as **keywords**, not calls

Distinct from `super(...)`/`this(...)`:

- **Constructor calls:** `super(...)`, `this(...)` — invoke the parent's or
  the current class's constructor.
- **Keywords:** `super.x`, `this.x`, `super.m1()`, `this.m1()` — refer to
  the superclass's or the current class's **instance members**.

Parent and child both declare `s`:

```java
class P {
    String s = "parent variable";
}

class C extends P {
    String s = "child variable";

    public void m1() {
        System.out.println(s);        // child variable (default)
        System.out.println(this.s);   // child variable
        System.out.println(super.s);  // parent variable
    }

    public static void main(String[] args) {
        C c = new C();
        c.m1();
    }
}
```

```text
child variable
child variable
parent variable
```

The keywords are usable **anywhere** — methods or constructors — **any
number of times**, and even **together**, but never in a **static**
context, since they refer to an object's instance members:

```java
class C extends P {
    String s = "child variable";

    public static void m1() {
        System.out.println(this.s);  // CE
        System.out.println(super.s); // CE
    }
}
```

```text
CE: non-static variable this cannot be referenced from a static context
CE: non-static variable super cannot be referenced from a static context
```

### 1:30:03 — Constructor calls vs. keywords, side by side

| | `super()`/`this()` | `super`/`this` keywords |
|---|---|---|
| Purpose | Call the superclass's / current class's constructor | Refer to the superclass's / current class's instance members |
| Where | Only in a constructor, as a standalone statement | Anywhere except a static context |
| Count | At most one; never both together | Any number of times; can mix freely |

---

## 1:32:26 — Constructor overloading

A college automation system's inquiry desk needs different amounts of data
from different students — full details, or just a phone number, or just a
name — so the same `Inquiry` class ends up with several constructors, one
per shape of incoming data.

- A class may declare **any number** of constructors.
- Same name (the class name), **different argument lists** → overloading.
- Overloading **does** apply to constructors — a common interview question.

Board demo, chained via `this()`:

```java
class Test {
    Test(double d) {
        this(10);
        System.out.println("double-arg constructor");
    }

    Test(int i) {
        this();
        System.out.println("int-arg constructor");
    }

    Test() {
        System.out.println("no-arg constructor");
    }

    public static void main(String[] args) {
        Test t1 = new Test(10.5);
    }
}
```

`new Test(10.5)` runs the double-arg constructor, which calls `this(10)`
(int-arg), which calls `this()` (no-arg). Each print statement comes
*after* its `this(...)` call, so output unwinds in reverse chain order:

```text
no-arg constructor
int-arg constructor
double-arg constructor
```

Calling `new Test(10)` instead runs only the last two links of the chain:

```text
no-arg constructor
int-arg constructor
```

And `new Test()` runs just the base case:

```text
no-arg constructor
```

Which constructor runs is decided by the arguments at the call site;
`this(...)` always chains to another constructor of the **same** class.

---

## 1:44:20 — Overloading yes, inheritance/overriding no

- Overloading: **applies** to constructors.
- Inheritance and overriding: **do not apply** to constructors — only to methods.

Methods *do* inherit:

```java
class P {
    public void m1() {
        System.out.println("m1");
    }
}

class C extends P {
    public void m2() {
        System.out.println("m2");
    }

    public static void main(String[] args) {
        C c = new C();
        c.m1(); // inherited from P
        c.m2();
    }
}
```

```text
m1
m2
```

A child could also override `m1` if it wanted to — inheritance and
overriding are method concepts.

Constructors never inherit:

```java
class P {
    P() {
    }
}

class C extends P {
    C(int i) {
    }

    public static void main(String[] args) {
        // C c = new C(); // CE — C has no no-arg constructor; P's isn't inherited
        C c = new C(10);
    }
}
```

```text
// if the commented line ran:
CE: constructor C in class C cannot be applied to given types
  required: int
  found: no arguments
```

A child class has **only** the constructors it declares itself (plus the
compiler's default, if it declares none). A parent's constructors are never
inherited members of the child — and with nothing inherited, there is
nothing to override either.

---

## 1:51:19 — Where can constructors be written?

| Type | Constructor allowed? | Why |
|---|---|---|
| Concrete class | Yes | Initializes instance variables |
| Abstract class | Yes | May hold instance state a child needs initialized; runs via `super(...)` when the child object is created |
| Interface | No | Interface fields are implicitly `public static final` — there is no instance state to initialize |

```java
class Test {
    Test() {
    }
}
// valid — concrete class
```

```java
abstract class Test {
    int x;

    Test(int x) {
        this.x = x;
    }
}
// valid — abstract-class constructor initializes state a child inherits
```

```java
interface Test {
    Test() { }
}
// CE: <identifier> expected
```

```java
interface Test {
    int x; // no initializer
}
// CE: = expected — interface fields must be public static final and initialized
```

Both interface errors verified against `javac` (26) — an interface still
cannot declare a constructor, and an uninitialized interface field is still
a compile error, unchanged by default/static/private interface methods
(Java 8/9) since those add behavior, not state.

---

## 1:58:00 — Recursive method calls vs. recursive constructor calls

### Methods: nothing happens until you actually call one

```java
class Test {
    public static void m1() {
        m2();
    }

    public static void m2() {
        m1();
    }

    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

```text
Hello
```

`m1`/`m2` are never invoked — declaring mutually recursive methods is like
having a matchbox next to a fuel tank: nothing happens until someone lights
it. Call `m1()` from `main` and it ignites:

```java
class Test {
    public static void m1() {
        m2();
    }

    public static void m2() {
        m1();
    }

    public static void main(String[] args) {
        m1();
    }
}
```

```text
// compiles fine
// RE: java.lang.StackOverflowError
```

Recursive **method** invocation compiles cleanly and only fails at
**runtime**, with a `StackOverflowError`.

### Constructors: the mere possibility is a compile error

```java
class Test {
    Test() {
        this(10);
    }

    Test(int i) {
        this();
    }

    public static void main(String[] args) {
        System.out.println("Hello"); // no object ever created
    }
}
```

```text
CE: recursive constructor invocation
```

Verified against `javac` (26) — still an error today, in every release
tested. The compiler is stricter about constructors than methods: if
recursive constructor invocation is merely **possible** — via the
`this(...)` chain the compiler can see statically — it is flagged at
**compile time**, whether or not any object is ever actually created.

| | Recursive methods | Recursive constructors |
|---|---|---|
| When it's a problem | Only if actually invoked | Even if never invoked |
| Error | Runtime `StackOverflowError` | Compile-time `recursive constructor invocation` |

---

## 2:07:23 — A parent's arg-only constructor vs. a child's implicit `super()`

Three situations:

**1 — both classes empty** → valid; both get a compiler-generated `super();`,
and `Object` has a no-arg constructor to receive it.

```java
class P {
}

class C extends P {
}
// valid
```

**2 — parent has an explicit no-arg constructor; child is empty** → valid;
the child's default constructor calls `super()`, and the parent has a
matching no-arg constructor.

```java
class P {
    P() {
    }
}

class C extends P {
}
// valid
```

**3 — parent has only an int-arg constructor; child is empty** → **invalid**.

```java
class P {
    P(int i) {
    }
}

class C extends P {
}
```

```text
CE: constructor P in class P cannot be applied to given types
  required: int
  found: no arguments
```

The child still gets a default constructor whose body is `super();` — but
the parent has no no-arg constructor for that call to match, hence the
error. (Verified — the message above is `javac`'s actual current wording.)

**Fixes.** Either give the child an explicit constructor that calls the
parent's real constructor:

```java
class P {
    P(int i) {
    }
}

class C extends P {
    C() {
        super(10);
    }
}
// valid
```

or (the recommended habit): whenever you add an arg-taking constructor to a
class, also keep a no-arg one, so any child's implicit `super()` still has
something to call:

```java
class P {
    P() {
    }

    P(int i) {
    }
}

class C extends P {
}
// valid — the child's default super() finds P()
```

---

## 2:17:42 — A parent constructor that `throws` a checked exception

```java
import java.io.*;

class P {
    P() throws IOException {
    }
}

class C extends P {
}
```

```text
CE: unreported exception IOException in default constructor
```

The child's compiler-generated default constructor calls `super()`. The
parent's constructor throws a checked `IOException`, so the caller — here,
that generated `super()` call — must handle it. But a default constructor
has neither a `try`/`catch` nor a `throws` clause, hence the error.
(`throws` delegates handling to the caller, which must either catch it or
declare the same `throws`, per the ordinary exception rules.)

Can the child wrap `super()` in a `try`/`catch` instead?

```java
import java.io.*;

class P {
    P() throws IOException {
    }
}

class C extends P {
    C() {
        try {
            super(); // CE — super() must stand alone; it cannot sit inside a try block
        } catch (IOException e) {
        }
    }
}
```

```text
CE: call to super must be first statement in constructor
```

No. Even under Java 25+'s relaxed "statements before super()" rule (see the
Modern Java box earlier in this note), `super(...)`/`this(...)` still can't
be wrapped in `try`/`catch` — verified directly against `javac` 26, which
still rejects it (`explicit constructor invocation not allowed here`). The
**only** workable fix is for the child constructor to `throws` the same
checked exception or a supertype of it:

```java
import java.io.*;

class P {
    P() throws IOException {
    }
}

class C extends P {
    C() throws IOException {
        super();
    }
}
// valid
```

```java
class C extends P {
    C() throws Exception {  // Exception is a supertype of IOException
        super();
    }
}
// valid
```

**Rule:** if a parent constructor throws a checked exception, every child
constructor must `throws` the same checked exception (or a supertype of
it) — a `try`/`catch` around `super()`/`this()` is never an option, because
that call must always be its own top-level statement.

---

## Exam and interview points

1. **A constructor initializes; `new` creates.** Every misconception in this
   lecture collapses back to this one split.
2. **No return type — not even `void`.** Writing one silently turns the
   member into a method with the class's name, which never auto-runs.
3. **Only four modifiers apply:** `public`, default, `protected`, `private`.
   `final`, `static`, `abstract`, `native`, `synchronized`, and `strictfp`
   are all compile errors on a constructor.
4. **A default constructor exists only when the class declares no
   constructor at all**, is always generated by the **compiler** (never the
   JVM), is always no-arg, matches the class's access modifier, and its body
   is exactly `super();`.
5. **Every constructor's first line is `super(...)` or `this(...)`** — write
   neither and the compiler inserts `super();`. In Java 25+, plain statements
   that don't touch instance state may precede that call (JEP 513); the
   call itself must still stand alone — it can never live inside a
   `try`/`catch`.
6. **`super(...)`/`this(...)` calls a constructor; `super.x`/`this.x` reads
   a member.** The call form is restricted to constructors and to a single
   use; the keyword form works anywhere non-static, any number of times.
7. **Constructors overload but never inherit or override.** A child has only
   the constructors it declares (plus its own default, if none) — a
   parent's constructors are never inherited members.
8. **Interfaces cannot declare constructors**; concrete and abstract classes
   both can, unaffected by default/static/private interface methods.
9. **Recursive constructor invocation is a compile-time error even if the
   constructor is never called** — recursive method calls only fail at
   runtime (`StackOverflowError`), and only if actually invoked.
10. **A parent's only constructor takes arguments → every child needs an
    explicit `super(args)`**, or the parent needs a no-arg constructor added
    back. A parent constructor that `throws` a checked exception forces
    every child constructor to declare the same `throws` — there is no
    `try`/`catch` escape.

---

**Next:** Video 070 — Exception handling introduction
