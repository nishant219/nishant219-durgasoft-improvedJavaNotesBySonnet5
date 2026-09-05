# Video 066 — Overloaded Constructors

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-16 || overloaded constructor

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 66 of 203 |
| Series | OOPs · Part 16 |
| Topic | overloaded constructor |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 12m 01s |
| Video ID | 9qA_MNNqkK0 |
| Watch | https://www.youtube.com/watch?v=9qA_MNNqkK0 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is not a generic constructor-overloading intro. After the morning
session on constructor rules and the default-constructor prototype (video
065), Sir (1) writes a three-constructor `Test` with `this()` chaining and
automatic promotion, (2) motivates overloading with a `Person` object that
can be created from different amounts of data, (3) proves inheritance and
overriding are **not** applicable to constructors, (4) shows an abstract
class **can** have a constructor and an interface **cannot**, then (5)
drills three exam cases: recursive constructor invocation, a parent
argument-constructor with a child's compiler-generated default `super()`,
and a parent constructor that `throws` a checked exception.

---

### 00:04 — Recap: constructors, rules, default-constructor prototype

The morning session (video 065) covered the rules for constructors and the
default-constructor prototype. This video does not re-teach those; it opens
the next subtopic directly.

### 00:23 — Next subtopic: overloaded constructors

Board heading: **overloaded constructors**.

Opening line: **a class can contain any number of constructors.**

### 00:57 — Board: class `Test` with three constructors and `this()` chaining

Best example. Class `Test`. No-arg constructor. Inside it, `this(10)` — that
call goes to the int-arg constructor. Then print `no-arg constructor`.

Int-arg constructor `Test(int i)`. Inside it, `this(10.5)` — that call goes
to the double-arg constructor. Then print `int-arg constructor`.

Double-arg constructor `Test(double d)`. Print `double-arg constructor`. No
further `this()` call.

```java
class Test {
    Test() {
        this(10);
        System.out.println("no-arg constructor");
    }

    Test(int i) {
        this(10.5);
        System.out.println("int-arg constructor");
    }

    Test(double d) {
        System.out.println("double-arg constructor");
    }
}
```

### 02:09 — Same name, different argument types → overloaded constructors

How many constructors inside `Test`? **Three.** All have the **same name**
(`Test`) but **different argument types**: no-arg, int-arg, double-arg. Same
name, different types of arguments, is the overloading concept — these are
by default considered **overloaded constructors**.

### 02:50 — `main`: `new Test()` output

```java
class Test {
    Test() {
        this(10);
        System.out.println("no-arg constructor");
    }

    Test(int i) {
        this(10.5);
        System.out.println("int-arg constructor");
    }

    Test(double d) {
        System.out.println("double-arg constructor");
    }

    public static void main(String[] args) {
        Test t1 = new Test();
        // prints double-arg constructor
        // prints int-arg constructor
        // prints no-arg constructor
    }
}
```

`new Test()` calls the **no-arg** constructor, which calls the **int-arg**
constructor (`this(10)`), which calls the **double-arg** constructor
(`this(10.5)`). The prints happen on the way **back out** of that chain:
double-arg, then int-arg, then no-arg. Verified against `javac`/`java` 26 —
this is exactly what runs.

### 03:51 — `new Test(10)` and `new Test(10.5)`

```java
class Test {
    Test() {
        this(10);
        System.out.println("no-arg constructor");
    }

    Test(int i) {
        this(10.5);
        System.out.println("int-arg constructor");
    }

    Test(double d) {
        System.out.println("double-arg constructor");
    }

    public static void main(String[] args) {
        Test t2 = new Test(10);
        // prints double-arg constructor
        // prints int-arg constructor
    }
}
```

Argument passed is `int`. Int-arg constructor runs; at its start `this(10.5)`
fires the double-arg constructor first. Output: double-arg, then int-arg.
No-arg is **not** in this chain.

```java
class Test {
    Test() {
        this(10);
        System.out.println("no-arg constructor");
    }

    Test(int i) {
        this(10.5);
        System.out.println("int-arg constructor");
    }

    Test(double d) {
        System.out.println("double-arg constructor");
    }

    public static void main(String[] args) {
        Test t3 = new Test(10.5);
        // prints double-arg constructor
    }
}
```

`10.5` is `double` — directly the double-arg constructor. That is all.

### 04:41 — `new Test(10L)`: automatic promotion in overloading

```java
class Test {
    Test() {
        this(10);
        System.out.println("no-arg constructor");
    }

    Test(int i) {
        this(10.5);
        System.out.println("int-arg constructor");
    }

    Test(double d) {
        System.out.println("double-arg constructor");
    }

    public static void main(String[] args) {
        Test t4 = new Test(10L);
        // prints double-arg constructor
    }
}
```

`10L` is `long`. Is there a constructor that takes `long`? No. Automatic
promotion in overloading (video 054) widens `long` toward `double`, and
`Test(double d)` accepts it directly — the compiler does not route through
`Test(int i)` or `Test()` first. Output: double-arg constructor only.

### 05:28 — Overloading is applicable for constructors

Within a class you can declare multiple constructors — all sharing one name,
each with a different argument list. Hence the overloading concept applies to
constructors, and overloaded constructors are legal.

### 06:02 — Theory dictation

- Within a class we can declare **multiple constructors**.
- All these constructors have the **same name** but **different types of
  arguments**.
- Hence all of them are considered **overloaded constructors**.
- Hence **the overloading concept is applicable for constructors**.

### 07:41 — Same `Test` example, entire output

```java
class Test {
    Test() {
        this(10);
        System.out.println("no-arg constructor");
    }

    Test(int i) {
        this(10.5);
        System.out.println("int-arg constructor");
    }

    Test(double d) {
        System.out.println("double-arg constructor");
    }

    public static void main(String[] args) {
        Test t1 = new Test();
        Test t2 = new Test(10);
        Test t3 = new Test(10.5);
        Test t4 = new Test(10L);
        // prints double-arg constructor
        // prints int-arg constructor
        // prints no-arg constructor
        // prints double-arg constructor
        // prints int-arg constructor
        // prints double-arg constructor
        // prints double-arg constructor
    }
}
```

Take the **entire output**, not just one call — which constructor runs
depends on the information you provide at the call site. Automatic promotion
is applicable even for constructors, no differently than for methods.

### 09:46 — Why we need this: build a `Person` from whatever data we have

Sometimes you want to create a `Person` and you only know the name.
Sometimes name and age. Sometimes name, age, father's name, mother's name.
Whichever data you have, the matching constructor should exist.

### 10:40 — `Person` has many properties

One `Person` class, several properties: name, age, height, weight, father's
name, mother's name.

### 11:03 — Object with only name: `new Person("Durga")`

```java
class Person {
    String name;
    int age;
    double height;
    double weight;
    String fatherName;
    String motherName;

    Person(String name) {
        this.name = name;
    }
}

class Test {
    public static void main(String[] args) {
        Person p = new Person("Durga");
        // remaining fields keep their default values
    }
}
```

### 11:43 — Object with name and age: `new Person("Ravi", 30)`

The name-only constructor can't be reused for this data. Add a second one:

```java
class Person {
    String name;
    int age;

    Person(String name) {
        this.name = name;
    }

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

class Test {
    public static void main(String[] args) {
        Person p2 = new Person("Ravi", 30);
    }
}
```

### 12:29 — Object with name, age, father's name, mother's name

```java
class Person {
    String name;
    int age;
    String fatherName;
    String motherName;

    Person(String name) {
        this.name = name;
    }

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    Person(String name, int age, String fatherName, String motherName) {
        this.name = name;
        this.age = age;
        this.fatherName = fatherName;
        this.motherName = motherName;
    }
}

class Test {
    public static void main(String[] args) {
        Person p3 = new Person("Shiva", 30, "Ram", "xyz");
    }
}
```

Overloaded constructors here are not a stylistic nicety — they are required.
Whichever slice of the data you have, an overload matching it must exist.
Same name, different argument types, once again.

### 13:42 — Next question: do overriding and inheritance apply to constructors?

Can a parent class constructor, by default, be available to the child class?
Most people have a **misconception** here — first pin down what inheritance
means, then ask whether it applies to constructors.

### 14:24 — Inheritance **is** applicable for methods

```java
class P {
    public void m1() {
    }
}

class C extends P {
    public void m2() {
    }
}

class Test {
    public static void main(String[] args) {
        C c = new C();
        c.m1();
        c.m2();
    }
}
```

Parent class has one method: `m1`. Child class has **two**: `m1` (inherited)
and `m2`. Both `c.m1()` and `c.m2()` compile — the parent's method is
available on the child automatically, no extra code required. That is why
inheritance is applicable for methods.

### 15:47 — Now constructors: parent no-arg, child int-arg — the child has **one** constructor, not two

```java
class P {
    P() {
    }
}

class C extends P {
    C(int i) {
    }
}
```

If method-style inheritance applied, the child would have two constructors.
It does not — the child has **one constructor only**.

```java
class P {
    P() {
    }
}

class C extends P {
    C(int i) {
    }
}

class Test {
    public static void main(String[] args) {
        C c = new C();
        // CE: constructor C in class C cannot be applied to given types
        //   required: int
        //   found:    no arguments
    }
}
```

`new C()` looks for a no-arg constructor **in `C`**. It exists in `P`, but
that is `P`'s constructor, not `C`'s. Whatever methods the parent has are
available to the child by default; whatever constructor the parent has is
**not** — you may **call** it, but calling is not inheriting.

**Inheritance is not applicable for constructors.**

> ⚠️ **Modern Java — the diagnostic text has changed since this was recorded; the rule hasn't.**
> OCJP-era javac reported this family of errors as a flat
> `cannot find symbol` / `symbol: constructor C()` / `location: class C`.
> Recompiled just now on current javac (26), the message instead names the
> constructor that *does* exist and explains the arity mismatch directly
> (`cannot be applied to given types … reason: actual and formal argument
> lists differ in length`) — verified above and reproduced at every later
> "cannot find symbol constructor" moment in this video (Case 2 and Q9).
> This is the same javac diagnostics rewrite (~JDK 7 onward) already covered
> in video 054's Modern Java note for overloaded methods; it changed the
> wording of the message, never the underlying rule.

### 17:28 — Overriding is also not applicable

Overriding means: the parent's method is available to the child, and the
child redefines it. If the parent's constructor was never available to the
child in the first place, there is nothing to redefine.

**Inheritance and overriding are not applicable for constructors.**

### 18:02 — Board conclusion (dictation)

For constructors:

- inheritance and overriding concepts are **not applicable**
- **but** the overloading concept **is applicable**

### 19:11 — Every class, including abstract, can contain a constructor; an interface cannot

```java
class Test {
    Test() {
    }
}
// valid

abstract class Test {
    Test() {
    }
}
// also valid — an abstract class can declare a constructor,
// even though you can never `new` the abstract class itself

interface Test {
    Test();
    // CE: <identifier> expected — interface cannot contain a constructor
}
```

### 21:38 — Why an interface cannot have a constructor

A constructor's job is to initialize an object — meaning to initialize
**instance variables**. Every field declared inside an interface is
implicitly `public static final`; there is never an instance variable to
initialize. No instance state, no reason for a constructor.

> ⚠️ **Modern Java — records give the taxonomy a fourth member.**
> Records (**Java 16**) are classes with instance state, so they need
> constructors too — but the compiler writes one for you: the **canonical
> constructor**, one parameter per record component, generated automatically
> the same way a default no-arg constructor is generated for an ordinary
> class with none written. Records take the `this()`-chaining rule taught in
> this lecture and make it compulsory: any constructor you write that is not
> the canonical one **must** invoke another constructor of the same record as
> its first statement, or it is a compile error —
> ```text
> error: constructor is not canonical, so it must invoke another
> constructor of class Point
> ```
> (verified on javac 26). The class/abstract-class/interface split Sir draws
> here is unchanged; records just add a class flavor whose default
> constructor is never a plain no-arg one.

### 22:21 — Same three examples, terminology settled

Concrete class with a constructor: valid. Abstract class with a constructor:
valid. Interface with a constructor: compile error. Terminology set, ready
for the three exam cases.

### 23:04 — Three important cases

Three cases follow; each one is itself an important conclusion.

### 23:18 — Case 1: recursive `m1` ↔ `m2`, never called — output is `hello`

```java
class Test {
    public static void m1() {
        m2();
    }

    public static void m2() {
        m1();
    }

    public static void main(String[] args) {
        System.out.println("hello");
        // prints hello
    }
}
```

`m1` calls `m2`, `m2` calls `m1` — but `main` never calls either. Some people
guess `StackOverflowError` on reflex, because of the recursion. Sir's
analogy: a petrol tank next to a matchbox does not ignite itself — someone
has to strike the match. `m1`/`m2` calling each other is the tank and
matchbox; nobody in `main` lit it. Output is plainly `hello`.

### 25:21 — Now call `m1()`: one runtime stack, then overflow

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
        System.out.println("hello");
        // RE: Exception in thread "main" java.lang.StackOverflowError
    }
}
```

One thread here — the main thread — and the JVM gives every thread one
runtime stack. `main` calls `m1`, `m1` calls `m2`, `m2` calls `m1`, and so on;
every call is pushed onto that stack until it overflows. `hello` never
prints, because control never returns from `m1()`.

> ❗ **Correction — `StackOverflowError` is not a "runtime exception."**
> Sir calls this "a runtime exception saying `StackOverflowError`." It *is*
> unchecked and it *does* surface at runtime, but "runtime exception" is also
> the name of a specific class, `java.lang.RuntimeException`, and
> `StackOverflowError` is not one. The hierarchy: `Throwable` splits into
> `Exception` (checked, unless it is a `RuntimeException`) and `Error`.
> `StackOverflowError extends Error` — it signals a JVM resource limit being
> exhausted, not a caught-able logic mistake, which is exactly why you are
> not expected to catch it in normal code. Say "runtime error" or "unchecked
> throwable" for the general idea; reserve "runtime exception" for actual
> `RuntimeException` subclasses (`NullPointerException`,
> `ArrayIndexOutOfBoundsException`, and the like).

### 26:31 — Why this, if it looks unrelated to constructors?

The method version is staged first so the constructor version can be
contrasted against it directly. Comment out the `m1()` call and the output
goes back to a plain `hello` — `m1` and `m2` still call each other, but
nobody calls into the cycle.

### 27:17 — Live: without the call → `hello`; with it → `StackOverflowError`

```bash
javac Test.java
java Test
```

Without `m1();` in `main`: `hello`. Adding `m1();` back: compiles fine, then
`Exception in thread "main"` … `StackOverflowError` at run time. Recursive
**method** calls fail at runtime, and only if something actually calls into
the cycle. Now apply the same idea to constructors.

### 28:52 — Same pattern with constructors: `this(10)` / `this()`

```java
class Test {
    Test() {
        this(10);
    }

    Test(int i) {
        this();
    }

    public static void main(String[] args) {
        System.out.println("hello");
        // CE: recursive constructor invocation
    }
}
```

The no-arg constructor calls `this(10)`; the int-arg constructor calls
`this()`. `main` never creates a `Test` object — by the method-call logic
just established, the reflex answer is `hello`. It is **not**. The compiler
detects the **possibility** of recursive constructor invocation at compile
time — you do not have to actually trigger it — and rejects the class
outright: `recursive constructor invocation`. Verified on javac 26: the file
does not compile, full stop.

### 32:02 — Recursive method call vs. recursive constructor invocation

Recursive **method** calls are a **runtime** failure (`StackOverflowError`),
and only when something calls into the cycle. Recursive **constructor**
invocation is caught at **compile time**, purely from the possibility of the
cycle existing — no object needs to ever be created.

### 33:29 — Case 1 dictation

- Recursive method call is a runtime failure: `StackOverflowError`.
- If there is a *chance* of recursive constructor invocation, the code will
  not compile — `recursive constructor invocation` is a compile-time error.

### 35:07 — Both examples, side by side

```java
class Test {
    public static void m1() { m2(); }
    public static void m2() { m1(); }

    public static void main(String[] args) {
        m1();
        System.out.println("hello");
        // RE: java.lang.StackOverflowError
    }
}
```

```java
class Test {
    Test() { this(10); }
    Test(int i) { this(); }

    public static void main(String[] args) {
        System.out.println("hello");
        // CE: recursive constructor invocation
    }
}
```

Case 1 is done.

### 37:22 — Case 2: three "innocent" parent–child programs

```java
class P { }
class C extends P { }
// program 1: valid
```

```java
class P {
    P() {
    }
}
class C extends P { }
// program 2: valid
```

```java
class P {
    P(int i) {
    }
}
class C extends P { }
// program 3: invalid — cannot compile
```

Programs 1 and 2 are unremarkable and valid. Program 3 looks equally
innocent — "100% pakka" it fails to compile anyway.

### 39:28 — Why 1 and 2 compile, and 3 does not: the compiler inserts `super()`

Program 1: no constructor is written anywhere. The compiler generates a
no-arg constructor with `super()` in both `P` and `C`:

```java
class P {
    P() { super(); }
}

class C extends P {
    C() { super(); }
}
```

Program 2: the compiler still generates `C() { super(); }`; `P` already has
a matching no-arg constructor. No problem.

Program 3: the compiler still generates `C`'s default constructor with
`super()` inside it — but `super()` needs a **no-arg** constructor in `P`,
and `P` only has `P(int i)`. Because the programmer wrote an argument
constructor, the compiler does **not** add a default no-arg one to `P`. The
match the generated `super()` needs simply isn't there:

```java
class P {
    P(int i) {
    }
}

class C extends P {
    // compiler generates:
    // C() { super(); }
    // CE: constructor P in class P cannot be applied to given types
    //   required: int
    //   found:    no arguments
}
```

It is not the programmer's mistake in the visible code — the compiler's own
generated `super()` is what breaks.

### 41:20 — If the parent has an argument constructor, take special care in the child

If a parent class declares any argument constructor, the child needs
deliberate attention with respect to constructors, or a mismatch like this
one can slip through.

### 41:54 — Highly recommended: whenever you write an argument constructor, write a no-arg one too

```java
class P {
    P() {
    }

    P(int i) {
    }
}

class C extends P { }
```

Now the compiler-generated `C() { super(); }` finds `P()` and compiles.

### 42:18 — Live compile of case 2

`P` and `C extends P` with no constructors: valid. Adding `P()` alone: valid.
Switching to `P(int i)` alone: invalid, with the constructor-not-applicable
error shown above. First two compile; the last does not, because no matching
constructor exists in the parent for the child's generated `super()`.

### 45:35 — Two notes for case 2

**Note 1.** If a parent class has any argument constructor, take special
care with constructors when writing child classes.

**Note 2 — the more valuable one.** Whenever you write an argument
constructor, it is highly recommended to write a no-arg constructor too.
With both present, the compiler-generated `super()` in the child always has
somewhere to land.

### 48:20 — Case 3: a checked exception and its caller

```java
import java.io.*;

class Test {
    public void m1() {
        m2();
        // CE: unreported exception IOException; must be caught or declared to be thrown
    }

    public void m2() throws IOException {
    }
}
```

`IOException` is checked. If a method throws a checked exception, its
**caller** is responsible for handling it — here, `m1` is the caller of
`m2`, and it does neither.

### 50:02 — Two ways the caller can handle it: try-catch or `throws`

```java
import java.io.*;

class Test {
    public void m1() {
        try {
            m2();
        } catch (IOException e) {
        }
    }

    public void m2() throws IOException {
    }
}
```

```java
import java.io.*;

class Test {
    public void m1() throws IOException {
        m2();
    }

    public void m2() throws IOException {
    }
}
```

Same rule, now applied to constructors: one constructor calling another
still has a "caller."

### 51:03 — Parent constructor `throws IOException`; empty child will not compile

```java
import java.io.*;

class P {
    P() throws IOException {
    }
}

class C extends P {
    // compiler generates:
    // C() { super(); }
    // CE: unreported exception IOException in default constructor
}
```

"100% pakka the code won't compile," and it's not the programmer's mistake —
the compiler's own generated default constructor is the caller of `P()`
here, and that generated constructor neither catches nor declares
`IOException`. Verified on javac 26: `unreported exception IOException in
default constructor`.

### 53:15 — Live compile of case 3

Same result live, once `java.io.IOException` is in scope (`import
java.io.*;`): the empty child fails with exactly that message.

### 54:06 — How to handle it: two ways, but try-catch **will not work** here

```java
import java.io.*;

class P {
    P() throws IOException {
    }
}

class C extends P {
    C() {
        try {
            super();
        } catch (IOException e) {
        }
        // CE: explicit constructor invocation (super/this) is not allowed
        //     here — it must be the very first statement in the constructor
    }
}
```

The first statement inside every constructor must be a direct `super(...)`
or `this(...)` call — never one wrapped in a `try`. Try-catch is off the
table for this case.

### 55:18 — The only fix: the child constructor must `throws` the same checked exception, or a parent of it

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
```

If you want to handle more than just `IOException`, that is fine too —
`Exception`, even `Throwable`, both cover `IOException` and both compile:

```java
class C extends P {
    C() throws Exception {
        super();
    }
}
```

```java
class C extends P {
    C() throws Throwable {
        super();
    }
}
```

**Conclusion:** if a parent constructor throws a checked exception, the
child constructor must throw the **same checked exception or a supertype of
it**. The rule is strict — a narrower type is not allowed.

### 56:12 — Live: `throws IOException` / `Exception` / `Throwable` all compile

Confirmed live for all three declarations above; each compiles cleanly.

### 59:24 — Case 3 dictation

If a parent class constructor throws any checked exception, the child class
constructor must throw the same checked exception or its parent — otherwise
the code will not compile.

These are the three important cases.

---

## 1:00:51 — Summary drill: which of the following is valid?

To close out the whole constructor topic, Sir runs an OCJP-style bit drill —
eighteen statements, each marked valid/invalid with a one-line reason.

### 1:01:29 — Q1–Q2: create vs. initialize

**Q1.** *"The main purpose of a constructor is to create an object."* —
**Invalid.** `new` creates the object; the constructor initializes it.

```java
class Student {
    String name;

    Student(String name) {
        this.name = name; // initialization, not creation
    }

    public static void main(String[] args) {
        Student s = new Student("Durga");
        // `new` creates the object; the constructor initializes `name`
    }
}
```

**Q2.** *"The main purpose of a constructor is to perform initialization of
an object."* — **Valid.**

### 1:02:29 — Q3: constructor name need not match the class name?

**Invalid.** It must match exactly, or it is not a constructor at all — just
a method missing a return type.

```java
class Test {
    Demo() {
        // CE: invalid method declaration; return type required
    }
}
```

### 1:02:54 — Q4: a return type is applicable for constructors, but only `void`?

**Invalid.** Writing any return type — including `void` — turns the
declaration into an ordinary method, not a constructor.

```java
class Test {
    void Test() {
        // legal — but it's a method named Test, not a constructor
    }

    public static void main(String[] args) {
        Test t = new Test(); // uses the compiler-generated default
                              // constructor, never void Test()
    }
}
```

### 1:03:26 — Q5: any modifier can be applied to a constructor?

**Invalid.** `public`, `private`, `protected`, or no modifier (default) are
allowed. `final`, `static`, and `strictfp` are not.

```java
class Test {
    public Test() { }
    private Test(int i) { }
    protected Test(double d) { }
    Test(String s) { }
}
```

```java
class Test {
    static Test() {
        // CE: modifier static not allowed here
    }

    final Test(int i) {
        // CE: modifier final not allowed here
    }
}
```

### 1:03:58 — Q6–Q9: who generates the default constructor, and when

**Q6.** *"Default constructor generated by the JVM."* — **False.** The
**compiler** generates it, never the JVM.

**Q7.** *"Compiler is responsible for generating the default constructor."*
— **True.**

**Q8.** *"Compiler will always generate a default constructor."* —
**False.** Only when the class declares **no constructor at all**.

```java
class Test {
    // compiler generates: Test() { super(); }
}

class Test2 {
    Test2(int i) {
    }
    // compiler does NOT generate a Test2() — one constructor already exists
}
```

**Q9.** *"If we are not writing a no-arg constructor, the compiler will
generate a default one."* — **Invalid.** The trigger is writing **no
constructor at all**, not specifically no-arg — writing any other-arg
constructor still suppresses generation.

```java
class Test {
    Test(int i) {
    }

    public static void main(String[] args) {
        Test t = new Test();
        // CE: constructor Test in class Test cannot be applied to given types
        //   required: int
        //   found:    no arguments
    }
}
```

### 1:05:59 — Q10–Q11: is every no-arg constructor "default"?

**Q10.** *"Every no-arg constructor is always a default constructor."* —
**False.** "Default constructor" means **compiler-generated**; a no-arg
constructor you write yourself is not one.

```java
class Test {
    Test() {
        // programmer-written no-arg constructor: NOT a default constructor
    }
}
```

**Q11.** *"A default constructor is always a no-arg constructor."* —
**True.** The implication runs one way only: default ⇒ no-arg, but no-arg
does not imply default.

### 1:06:56 — Q12: does the compiler insert `this()` when nothing is written?

**Invalid / False.** The compiler always inserts **`super()`**, never
`this()`.

```java
class Test {
    Test() {
        // compiler inserts super(); — NOT this();
        System.out.println("hello");
    }
}
```

```java
class Test {
    Test() {
        this(10);
        System.out.println("no-arg");
    }

    Test(int i) {
        super(); // first line is super() or this() — here, super() to Object
        System.out.println("int-arg");
    }
}
```

### 1:08:04 — Q13–Q14: overloading, overriding, inheritance for constructors

**Q13.** *"For constructors, both overloading and overriding are
applicable."* — **False.** Overloading only.

```java
class Test {
    Test() { }
    Test(int i) { }
    // overloading: yes
}
```

**Q14.** *"For constructors, inheritance is applicable, but not
overriding."* — **False.** Neither is applicable — see 15:47–17:28 above.

### 1:09:03 — Q15–Q16: abstract classes and interfaces

**Q15.** *"Only concrete classes can contain a constructor; abstract classes
cannot."* — **Invalid.** Abstract classes can, and often must.

```java
abstract class Test {
    Test() {
        // legal
    }
}
```

**Q16.** *"Interfaces can contain constructors."* — **Invalid.**

```java
interface Test {
    Test();
    // CE: interface cannot contain a constructor
}
```

### 1:10:00 — Q17: is recursive constructor invocation a runtime exception?

**Invalid.** It is a **compile-time error**.

```java
class Test {
    Test() {
        this(10);
    }

    Test(int i) {
        this();
    }
    // CE: recursive constructor invocation
}
```

### 1:10:30 — Q18: same checked exception "or its child"?

**False.** The rule is the same checked exception **or its parent** —
Sir's statement here deliberately swaps "parent" for "child" to test whether
you actually remember which direction the rule runs.

```java
import java.io.*;

class P {
    P() throws IOException {
    }
}

class C extends P {
    C() throws Exception { // a parent of IOException: legal
        super();
    }
}
```

A version that threw only a **child** of `IOException` (say,
`FileNotFoundException`) is not the rule taught — and would not satisfy the
compiler either, since `FileNotFoundException` does not cover every checked
exception `IOException` could throw.

### 1:11:37 — Close

The whole constructor topic — rules, overloading, inheritance/overriding,
abstract/interface, and the three exam cases — is now revised end to end.
End of video 066 (OOPs part 16).

---

## Board conclusions, in one place

1. A class can contain any number of constructors. Same name, different
   argument types → **overloaded constructors**. Overloading **is**
   applicable for constructors, automatic promotion included.
2. Inheritance and overriding are **not** applicable for constructors. A
   parent's constructor is never inherited; you may **call** it
   (`super(...)`), but calling is not inheriting, and overriding never
   arises for something that isn't inherited.
3. Every class in Java, **including abstract classes**, can contain a
   constructor. **Interfaces cannot** — there is no instance variable to
   initialize.
4. **Case 1:** a recursive method call is a runtime `StackOverflowError`,
   and only if something actually calls into the cycle. A recursive
   constructor invocation is a **compile-time error**, triggered by the mere
   *possibility* of the cycle, with no object ever created.
5. **Case 2:** if the parent has only an argument constructor, the
   compiler-generated child `super()` fails to find a match. Whenever you
   write an argument constructor, write a no-arg one too.
6. **Case 3:** if a parent constructor throws a checked exception, the child
   constructor must `throws` the same checked exception or a supertype of
   it. Wrapping `super()` in try-catch is illegal — the first statement must
   be a direct `super(...)` or `this(...)` call.

---

## Exam and interview points

1. **Overloading applies to constructors; inheritance and overriding do
   not.** A parent's constructor is never inherited by the child — it can
   only be called via `super(...)` — so the question of overriding it never
   even arises.
2. **Every class, abstract classes included, can declare a constructor.**
   Interfaces never can, in any Java version, because every interface field
   is implicitly `static final` — no instance state, no need to initialize
   it.
3. **Recursive method calls fail at runtime** (`StackOverflowError`, and
   only if actually invoked); **recursive constructor invocation fails at
   compile time**, from the mere possibility, whether or not an object is
   ever created. Note the vocabulary trap: `StackOverflowError` is an
   `Error`, not a `RuntimeException` — "unchecked" is accurate, "runtime
   exception" as a class name is not.
4. **A compiler-generated `super()` needs a matching no-arg constructor in
   the parent.** If the parent has only an argument constructor, an
   otherwise-empty child fails to compile — not because of anything wrong in
   the child's visible code. Rule of thumb: whenever you add an argument
   constructor, add a no-arg one too.
5. **A checked exception thrown by a parent constructor is the child
   constructor's responsibility**, exactly like a checked exception thrown
   by any called method — except try-catch cannot help here, because
   `super()`/`this()` must be the constructor's first statement. The child
   must `throws` the same exception or a supertype of it — never a subtype.
6. **"Default constructor" is a precise term**: compiler-generated, always
   no-arg, and only produced when the class declares **no constructor at
   all**. A no-arg constructor you write yourself is not a "default"
   constructor, even though it looks identical.
7. **Constructor modifiers are restricted**: `public`/`private`/`protected`/
   default access are legal; `static`, `final`, and `strictfp` are not,
   because a constructor is neither inherited nor overridden nor
   floating-point-specific by nature.
8. **Records (Java 16+)** extend this lecture's taxonomy: a class with
   instance state, none of whose constructors you wrote by hand, still gets
   one automatically — the canonical constructor — and any other constructor
   you add must delegate to it via `this(...)` as its first statement, a
   compiler-enforced version of the chaining Sir teaches by hand here.

---

**Next:** Video 067 — Singleton class
