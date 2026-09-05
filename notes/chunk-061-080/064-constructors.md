# Video 064 — Constructors

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-14 || constructors

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 64 of 203 |
| Series | OOPs · Part 14 |
| Topic | constructors |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 04m 57s |
| Video ID | XWjhxt6ijLI |
| Watch | https://www.youtube.com/watch?v=XWjhxt6ijLI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is **OOPs Part 14**, "the last topic mostly related to OOPs": **constructors**.
Sir kills a common misconception up front — a constructor does not *create* an
object, it *initializes* one. He walks a `Student` class (`name`, `rollNumber`)
through four candidate places to initialize state, rules out three of them, and
lands on the constructor as the only place that gives every object different
values without the line count exploding. From there: constructor vs. instance
block (the classic "count how many objects got created" interview program),
the rules for writing a constructor (name must match the class, no return type
— not even `void`), which modifiers are legal, and how the compiler — never
the JVM — decides whether to hand you a default constructor.

---

### 00:04 — Topic: constructors; create vs. initialize

Next topic: **constructors**. Last topic mostly related to OOPs.

What is the need or purpose of a constructor? "Most of the people [have a]
misconception about constructor." He asks the room: is its purpose **to
create an object**, or **to initialize an object**?

**Make sure: we use constructors to initialize an object, not to create an
object.** He will explain in detail; the conclusion comes at the end.

### 01:00 — Board: `class Student`, two objects, then "600 students"

He writes `class Student`. For every student, **name** and **roll number**
are compulsory. Then `main`:

```java
class Student {
    String name;
    int rollNumber;

    public static void main(String[] args) {
        Student s1 = new Student();
        Student s2 = new Student();
        // ... 600 Student objects
    }
}
```

Target: assume 600 student objects (`s1`, `s2`, …). For every student a
**separate copy of the instance variables** is created — an instance variable
is always part of the object, and every object gets its own copy by default.

### 02:55 — No initialization → JVM defaults: `null` and `0`

After creating the object he performs **no initialization**. The JVM always
supplies **default values** for instance variables:

| Field | Type | Default value |
|---|---|---|
| `name` | `String` | `null` |
| `rollNumber` | `int` | `0` |

```java
class Student {
    String name;       // default null
    int rollNumber;    // default 0

    public static void main(String[] args) {
        Student s1 = new Student();
        Student s2 = new Student();
        // s1: name = null, rollNumber = 0
        // s2: name = null, rollNumber = 0
        // ... all 600: name = null, rollNumber = 0
    }
}
```

He "asks" the first student: what is your name? "My name is **null**, my roll
number is **zero**." Every one of the 600 students answers the same way.

### 04:01 — All 600 students named `null`: not recommended

Every student having the same name `null` and the same roll number `0` is
**meaningless** — not at all recommended. Once we create an object,
**compulsory we should perform initialization**; only then is the object in a
position to respond properly. Contrast:

```java
class StudentAfterInit {
    String name;
    int rollNumber;
    // desired state after initialization — not how we get there yet:
    // s1: name = "Durga", rollNumber = 101
    // s2: name = "Ravi",  rollNumber = 102
}
```

Now "what is your name?" gets "Durga" / "101", "Ravi" / "102" — meaningful.
**Object creation is not enough. Initialization is also very important.**

Point one is clear. Next question: **where** do we perform initialization?
Multiple places are possible; he will weigh each one.

### 07:05 — Place 1: initialization at declaration — not recommended

```java
class Student {
    String name = "Durga";
    int rollNumber = 101;
}
```

**Not recommended.** Every object gets the *same* initializer, so every
student ends up Durga / 101 — as meaningless as `null` / `0`. Object to
object, name and roll number **should change**.

### 08:29 — Place 2: instance block — not recommended

```java
class Student {
    String name;
    int rollNumber;

    {
        name = "Durga";
        rollNumber = 101;
    }
}
```

**Not recommended**, same reason: the same block executes for every object,
so every student again gets the same name and roll number.

### 09:21 — Place 3: after `new`, `s1.name = ...` — different values, but line count explodes

```java
class Student {
    String name;
    int rollNumber;

    public static void main(String[] args) {
        Student s1 = new Student();
        s1.name = "Durga";
        s1.rollNumber = 101;

        Student s2 = new Student();
        s2.name = "Ravi";
        s2.rollNumber = 102;
        // ...
    }
}
```

Can we get **different values for every object**? **Yes.** Recommended?
**Not recommended** — the length of the code increases without bound. 600
objects × 2 fields = **1200 lines** just for initialization. If the object
has 10 properties, 600 objects means **6000 lines** just for initialization.

### 11:14 — Two problems; best place is the constructor

Two problems on the table:

1. Every object needs **different values**.
2. **Code length should not explode.**

The place that solves both is the **constructor**.

### 11:40 — Constructor: `Student(String name, int rollNumber)`

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
    }
}
```

Whenever we create `s1`, the constructor executes automatically and assigns
the given values to the current object: `s1` → Durga / 101. `s2` runs the
*same* constructor with Ravi / 102.

### 13:33 — Different values, and the two assignment lines are reused

Can we maintain different values? **Yes.** Is the code length increasing?
**No** — the same two lines (`this.name = name; this.rollNumber = rollNumber;`)
serve every object. Create 600 objects and those same two lines are enough.
This is why the constructor is the best place for initialization.

### 14:04 — Role of constructor: initialize, not create

Whenever we create an object, some piece of code executes immediately to
perform initialization — that piece of code is the constructor. It is a
**specially designed concept to perform initialization of an object**.
Declaration-time init, instance block, and per-object field assignment all
fall short; the constructor is the best choice.

> *Whenever we are creating an object, some piece of the code will be
> executed automatically to perform initialization of the object. This piece
> of the code is nothing but **constructor**. Hence the main purpose of
> constructor is to perform initialization of an object.*

### 19:09 — Note: initialize, but not create

> *The main purpose of constructor is to perform initialization of an
> object, **but not to create object**.*

Role of constructor: to perform initialization of an object, **not** to
create one. **To create an object we use the `new` operator; to perform
initialization, the constructor takes over.** That is the basic introduction
to what a constructor is.

---

### 20:16 — Heading: difference between constructor and instance block

There is already a concept named **instance block** — it too runs for every
object creation. So what is the difference?

### 20:59 — Constructor initializes; instance block is "other than initialization"

Purpose of constructor: **to perform initialization of an object**. Purpose
of instance block: **other than initialization** — for every object creation
we want some *other* activity to happen. Sir's examples:

- **Updating one record in the database** whenever an object is created.
- **Incrementing a count** of how many objects of this class got created.

Constructor's job and instance block's job are **different**; replacing one
with the other is **not possible**.

> *The main purpose of constructor is to perform initialization of an
> object. But other than initialization, if we want to perform any activity
> for every object creation, then we should go for **instance block** (like
> updating one entry in the database for every object creation, or
> incrementing count value for every object creation, etc.). Both
> constructor and instance block have their own different purposes, and
> replacing one concept with another concept may not work always.*

### 27:22 — Both run per object; instance block **first**, then constructor

> *Both constructor and instance block will be executed for every object
> creation, but instance block first, followed by constructor.*

> ⚠️ **Modern Java — the precise rule, for the record.**
> Sir's ordering is correct and unchanged since Java 1.0: instance
> initializer blocks and instance-variable initializers run, top to bottom in
> source order, **right after the implicit or explicit `super()` call, before
> the rest of the constructor body** (JLS §12.5). "Instance block, then
> constructor" is the simplified, exam-accurate version of that.

### 28:42 — Requirement: print how many objects were created

```java
class Test {
    static int count = 0;

    Test() {
    }

    Test(int i) {
    }

    Test(double d) {
    }

    public static void main(String[] args) {
        Test t1 = new Test();       // no-arg constructor
        Test t2 = new Test(10);     // int constructor
        Test t3 = new Test(10.5);   // double constructor
    }
}
```

One static variable `static int count = 0`, three constructors picked based
on what the caller passes. Requirement: print how many objects were created.

### 31:11 — Doing it only with constructors: `count++` in every constructor — not recommended

Pretend we don't know about instance blocks. `count++` has to go in *every*
constructor, because at runtime we don't know in advance which one gets
called:

```java
class Test {
    static int count = 0;

    Test() {
        count++;
    }

    Test(int i) {
        count++;
    }

    Test(double d) {
        count++;
    }

    public static void main(String[] args) {
        Test t1 = new Test();
        Test t2 = new Test(10);
        Test t3 = new Test(10.5);
    }
}
```

`count++` is written **three times** — code redundancy.

### 32:00 — Second problem: `this(10)` makes `count++` run twice for **one** object

If one constructor delegates to another with `this(10)`, that second
constructor's `count++` also runs — so **one** object increments `count`
**twice**:

```java
class Test {
    static int count = 0;

    Test() {
        this(10); // also runs Test(int)
        count++;
    }

    Test(int i) {
        count++;
    }

    Test(double d) {
        count++;
    }
    // one object via new Test() → count incremented twice — wrong
}
```

Verified: `new Test()` alone leaves `count == 2` for a single object. That's
why, for "other than initialization" activity on every object creation,
**don't run the show with the constructor** — not recommended.

### 32:46 — Instance block: write `count++` **once**

```java
class Test {
    static int count = 0;

    {
        count++; // instance block — once per object, before the constructor body
    }

    Test() {
    }

    Test(int i) {
    }

    Test(double d) {
    }

    public static void main(String[] args) {
        Test t1 = new Test();
        Test t2 = new Test(10);
        Test t3 = new Test(10.5);
        System.out.println("The number of objects created is " + count);
        // prints The number of objects created is 3
    }
}
```

Whichever constructor a caller invokes, the instance block runs first, so
`count++` needs writing **only once**. Even with a `this(10)` chain, the
instance block still runs only once per object — verified by compiling: it
fires right after the actual `super()` call at the bottom of the chain, not
once per constructor in the chain. This is the fix for the double-count bug
above, and the recommended pattern for "other than initialization, do this
once per object" requirements.

### 34:19 — Interview trap: "write a program to print number of objects created"

An interviewer asking this is really checking: **are you aware of the
instance-block concept?** If constructor and instance block did the same
job, there would be no reason for two concepts — they're different, with
different purposes.

---

### 37:18 — Heading: rules of writing constructors

### 37:48 — Rule 1: class name and constructor name must match

```java
class Test {
    Test() { // name matches class name → constructor
    }
}
```

### 38:35 — Rule 2: no return type — **not even `void`**

A constructor executes **automatically** when an object is created; we never
*call* it:

```java
class Test {
    Test() {
    }

    public static void main(String[] args) {
        Test t = new Test(); // constructor executes; we are not calling it
    }
}
```

If we were calling it, we'd expect a return value to use afterward. We're
not calling it — so the whole idea of a return type doesn't apply, **not
even `void`**.

### 40:09 — Doubt: `void Test()` — compile error or not?

```java
class Test {
    void Test() { // now what?
    }
}
```

**The code compiles.** No compile-time error, because the **compiler treats
it as a method** — a method that happens to share the class's name, not a
constructor.

### 41:24 — Can a method have the same name as the class?

**Possible**, yes. **Recommended**, no — that name already means "constructor"
to every reader; reusing it for a method is legal but confusing.

### 42:01 — Live: `Test.java` constructor prints; add `void` → nothing prints

```java
class Test {
    Test() {
        System.out.println("Constructor");
    }

    public static void main(String[] args) {
        Test t = new Test();
    }
}
```

`javac Test.java` compiles and runs fine, printing:

```text
Constructor
```

Add `void` and it becomes a plain method — creating the object no longer
triggers it automatically:

```java
class Test {
    void Test() { // method, not constructor
        System.out.println("Constructor");
    }

    public static void main(String[] args) {
        Test t = new Test();
        // default constructor runs silently; this method is NOT called automatically
        // prints nothing
    }
}
```

Verified by compiling both versions: the code compiles fine, and running it
prints nothing until the method is called explicitly, by its name, on the
object:

```java
class Test {
    void Test() { // method, not constructor
        System.out.println("Constructor");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.Test();
        // prints Constructor
    }
}
```

> *By mistake if we are trying to declare return type for the constructor,
> then we won't get any compile-time error, because compiler treats it as a
> method.*

> *Hence it is legal (but stupid) to have a method whose name is exactly
> same as class name.*

### 49:11 — Funny experience: a phone call in a VIP meeting

Years earlier, Sir's habit was to share his phone number with students after
a batch ended, for follow-up doubts. One evening he was mid-meeting with a
very senior contact he'd waited over a month to speak with — his phone kept
ringing, he kept declining, until the other person told him to check his
phone first. He stepped out and took the call, unrecognized number, no
introduction — just: **"Which modifiers applicable for constructors?"**

The caller turned out to be a former OCJP student, now in an interview,
panicking over that exact question and calling for confirmation before
answering — "job related, if I tell it wrong I may not get the job." After a
handful of similar calls, Sir stopped sharing his number. The point of the
story: **this is a genuinely popular interview question.**

### 53:40 — Only applicable modifiers: `public`, `private`, `protected`, default

The **only** applicable modifiers for a constructor are **`public`,
`private`, `protected`, and default (no modifier)**. Anything else is a
compile-time error.

### 54:09 — Board: `public` valid, `private` valid, `static` invalid

```java
class Test {
    public Test() { // valid
    }
}
```

```java
class Test {
    private Test() { // valid
    }
}
```

```java
class Test {
    protected Test() { // valid
    }
}
```

```java
class Test {
    Test() { // default (package) — valid
    }
}
```

```java
class Test {
    static Test() {
    }
    // CE: modifier static not allowed here
}
```

Verified with `javac`: `static Test() { }` fails to compile with exactly

```text
error: modifier static not allowed here
```

The same applies to `final`, `abstract`, `synchronized`, `native`, and the
other non-access modifiers — none of them are legal on a constructor.

---

### 57:14 — Heading: default constructor

### 57:39 — Who generates it: compiler, **not JVM**

> *Compiler is responsible to generate default constructor (but not JVM).*

If any extra code is required, the **compiler** takes care of it; the JVM's
job is just to *execute*, not to generate.

### 58:16 — Compiler does **not** always generate it

The compiler generates a default constructor **if and only if the class
writes no constructor at all**. Write even one, and the compiler leaves it
alone:

```java
class Test {
    // no constructor written by programmer
    // compiler generates: Test() { }
}
```

```java
class Test {
    Test(int i) {
    }
    // programmer already wrote a constructor
    // compiler will NOT generate Test()
}
```

### 1:00:10 — Every class has a constructor — default **or** customized, **not both**

> *Compiler is responsible to generate default constructor (but not JVM). If
> we are not writing any constructor, then only compiler will generate
> default constructor — that is, if we are writing at least one constructor,
> then compiler won't generate default constructor. Hence every class in
> Java can contain constructor. It may be default constructor generated by
> compiler, or customized constructor explicitly provided by programmer, but
> not both simultaneously.*

> ⚠️ **Modern Java — records get an implicit constructor too, on different terms.**
> A **record** (Java 16, JEP 395) always gets a **canonical constructor**
> whose parameters mirror its components — generated by the compiler if you
> don't write one, exactly like the default constructor rule here. The
> difference: you can override just the *validation* logic with a **compact
> constructor** (no parameter list, no field assignments) while the compiler
> still generates the assignments for you:
>
> ```java
> record StudentRec(String name, int rollNumber) {
>     StudentRec {   // compact canonical constructor
>         if (rollNumber < 0) throw new IllegalArgumentException("bad roll number");
>     }
>     // "this.name = name; this.rollNumber = rollNumber;" is generated for you
> }
> ```
>
> Compiled and run: `new StudentRec("Durga", 101)` prints
> `StudentRec[name=Durga, rollNumber=101]`. Records don't change the rule
> Sir teaches for ordinary classes — they add a second, narrower kind of
> compiler-generated constructor on top of it.

### 1:04:36 — Close of this lecture

"The compiler will generate default constructor always?" **No.** Only if no
constructor is written.

*(The captions end here; overloaded constructors and further constructor
rules continue in the next OOPs videos.)*

## What this video actually taught

1. Constructor **initializes**; it does **not** create. `new` creates the
   object; the constructor runs immediately after to initialize it.
2. `Student` without init: every object gets `name = null`, `rollNumber = 0`
   — meaningless. Init at **declaration** and in an **instance block** still
   give **the same values to every object**. After-`new` field assignments
   give different values but cost **600 × properties** lines. Constructor:
   different values, **two assignment lines reused**.
3. Instance block is **not** a constructor substitute — it is for "other
   than initialization" activity on every object (a DB insert, `count++`).
   Both run per object; **instance block first, then constructor**.
   `count++` in every constructor is redundant, and actively **wrong under
   `this(...)`** (two increments for one object — verified by compiling).
   Fix: `count++` once, in an instance block.
4. Constructor name **matches** the class name. **No return type, not even
   `void`.** `void Test()` compiles — it's a **method**, not a constructor;
   `new Test()` then prints nothing until `t.Test()` is called explicitly.
   Legal, but "stupid."
5. Only modifiers: **`public`, `private`, `protected`, default.**
   `static Test()` fails with exactly `modifier static not allowed here`
   (verified with `javac`). Default constructor is generated by the
   **compiler** (never the JVM), **only if the class writes none**. Every
   class has a constructor — default **or** customized, **never both**.

## Exam and interview points

1. **Constructor initializes, `new` creates** — the single most-tested
   distinction in this lecture. Say it exactly that way if asked.
2. **Instance block runs before the constructor body**, for every object,
   right after the (implicit or explicit) `super()` call — this still holds
   in every Java version.
3. **Constructor vs. instance block is about *what* the code is for**, not
   *when* it runs: constructor = initialization; instance block = any other
   per-object activity (DB writes, counters). Neither substitutes for the
   other.
4. **`count++` belongs in an instance block, not in every constructor** —
   putting it in constructors is redundant and breaks under `this(...)`
   chaining (verified: one object, `count` incremented twice).
5. **A constructor has no return type — not even `void`.** Adding one turns
   it into an ordinary method with the same name as the class: legal,
   compiles, but never runs automatically on `new`.
6. **Only `public`, `private`, `protected`, and default are legal
   constructor modifiers.** `static`, `final`, `abstract`, `synchronized`,
   and `native` are all compile errors on a constructor.
7. **The compiler generates a default constructor only when the class
   declares zero constructors.** The JVM never generates one. A class always
   has exactly one *kind* of constructor available — default or
   programmer-written, never both.
8. **Records (Java 16) generate a canonical constructor the same way** —
   compiler-provided unless you write one — but let you keep the generated
   field assignments while overriding just validation, via a compact
   constructor. Useful if an interviewer pushes past the OCJP-era rule into
   modern Java.

---

**Next:** Video 065 — Default constructor
