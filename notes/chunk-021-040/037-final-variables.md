# Video 037 — Final Variables

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-8|| final variables

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 37 of 203 |
| Series | Declarations and Access Modifiers · Part 8 |
| Topic | final instance variables, final static variables, final local variables, formal parameters |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 28m 32s |
| Video ID | gDXucIITZqs |
| Watch | https://www.youtube.com/watch?v=gDXucIITZqs |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Last session closed out class-level modifiers and member access modifiers
(`public` / `private` / `protected` / default). `final` on a class and `final`
on a method were covered earlier; this entire ~1.5-hour session is **`final`
on a variable** — and every one of the three variable kinds behaves differently:

1. **Final instance variable** — JVM gives it no default; must be assigned
   before constructor completion.
2. **Final static variable** — JVM gives it no default; must be assigned
   before class-loading completion.
3. **Final local variable** — JVM never defaults *any* local, final or not;
   must be assigned before it is *used* — an unused blank final local is legal.
4. **The only modifier a local variable accepts is `final`.** Every other
   modifier is a compile error, because access-modifier terminology does not
   apply to something whose scope is already fixed to one block.
5. **Formal parameters act as local variables** — they may be declared
   `final`, which blocks reassignment inside the method body.

---

## 00:04 — Agenda: three variable kinds, then `final` on each

All variables split into three kinds — instance, static, local. This lecture
asks, for each kind in turn: what happens when it is declared `final`?

## 01:19 — Final instance variables

### 01:19 — What is an instance variable?

Sir's running example is `class Student`. Every student needs a name and a
roll number — but the *value* differs per student:

```java
class Student {
    String name;
    int rollNumber;
}

class Demo {
    public static void main(String[] args) {
        Student s1 = new Student();
        s1.name = "Durga";
        s1.rollNumber = 101;

        Student s2 = new Student();
        s2.name = "Ravi";
        s2.rollNumber = 102;

        System.out.println(s1.name + " " + s1.rollNumber);   // Durga 101
        System.out.println(s2.name + " " + s2.rollNumber);   // Ravi 102
    }
}
```

If a variable's value **varies from object to object**, it is an **instance
variable** — a separate copy per object. 600 students means 600 names and 600
roll numbers, each living inside its own object.

### 06:09 — Plain instance variable: JVM default `0`

```java
class Test {
    int x;

    public static void main(String[] args) {
        Test t = new Test();
        System.out.println(t.x);   // 0
    }
}
```

Instance variables never need explicit initialization — the JVM always
supplies a default (`0` for `int`).

### 08:48 — `final` on it: the default disappears

```java
class Test {
    final int x;
    // CE: variable x might not have been initialized
}
```

Declare `final int x;` and give it nothing else, and the class fails to
compile — whether or not `x` is ever read. **Board:** *if the instance
variable is declared `final`, initialization is compulsory, whether we use it
or not, and the JVM won't provide a default.*

### 13:41 — Rule: initialize before constructor completion

A final instance variable must be assigned **before constructor completion**.
Instance control flow runs: instance-variable assignments and instance blocks,
*then* the constructor body — so an assignment at declaration or inside an
instance block still lands before the constructor finishes.

### 15:19 — Three allowed places, and only these three

```java
class Test {
    final int x = 10;   // 1. at declaration — valid
}

class Test {
    final int x;
    { x = 10; }          // 2. inside an instance block — valid (runs before the constructor)
}

class Test {
    final int x;
    Test() { x = 10; }   // 3. inside a constructor — valid (still before completion)
}
```

### 21:30 — Not inside a method

A method always runs **after** the constructor has already completed — you
need an object to call it on. So a method is not a legal place to give a
blank final its first value:

```java
class Test {
    final int x;

    public void m1() {
        x = 10;
        // CE: cannot assign a value to final variable x
    }
}
```

> ⚠️ **Modern Java — records give you this pattern for free.**
> Since **Java 16** (JEP 395), a `record` declares its components as `private
> final` fields, assigned once by the compiler-generated canonical constructor
> — exactly the "final instance variable, set exactly once, before construction
> completes" discipline this section teaches, minus the boilerplate:
>
> ```java
> record Point(int x, int y) { }   // x and y are private final fields
>
> Point p = new Point(3, 4);
> System.out.println(p.x() + "," + p.y());   // 3,4
> ```
>
> Everything Sir demonstrates with a hand-written blank final still applies —
> records just generate it for you when the class's only job is to hold final
> data.

## 25:14 — Final static variables

### 25:14 — What is a static variable?

Same `Student` class, plus a college name. Name and roll number vary per
student; **college name does not** — every `Student` object in that college
holds the identical string. Storing it as an instance variable would mean 600
separate copies of `"DurgaSoft"`, which wastes memory for no benefit:

```java
class Student {
    String name;
    int rollNumber;
    static String collegeName = "DurgaSoft";
}

class Demo {
    public static void main(String[] args) {
        Student s1 = new Student();
        s1.name = "Durga"; s1.rollNumber = 101;
        Student s2 = new Student();
        s2.name = "Ravi";  s2.rollNumber = 102;

        System.out.println(s1.collegeName);   // DurgaSoft
        System.out.println(s2.collegeName);   // DurgaSoft — same single copy
        System.out.println(Student.collegeName); // DurgaSoft
    }
}
```

**Board:** *if a variable's value is not varied from object to object, do not
declare it as an instance variable — declare it at class level with `static`,
so one copy is shared by every object.*

- Instance: object-level, a separate copy per object.
- Static: class-level, a single copy shared by every object of the class.

### 33:42 — Plain static variable: JVM default `0`

```java
class Test {
    static int x;

    public static void main(String[] args) {
        System.out.println(x);   // 0
    }
}
```

### 36:15 — `final` on it: same story, no default

```java
class Test {
    final static int x;
    // CE: variable x might not have been initialized
}
```

Modifier order never matters: `final static` and `static final` are both
fine, exactly like `public static` and `static public`.

### 39:49 — Rule: initialize before class-loading completion

Final instance → before **constructor** completion. Final static → before
**class-loading** completion — the analogous rule one level up.

### 41:48 — Two allowed places, and only these two

```java
class Test {
    final static int x = 10;   // 1. at declaration — valid (runs at class loading)
}

class Test {
    final static int x;
    static { x = 10; }          // 2. inside a static block — valid (also runs at class loading)
}
```

### 43:30 — Not inside a method — even a static one

A static method is still a *method*: it runs on demand, always after class
loading has completed, so it is too late — regardless of whether the method
itself is static:

```java
class Test {
    final static int x;

    public static void m1() {
        x = 10;
        // CE: cannot assign a value to final variable x
    }
}
```

## 49:05 — Final local variables

### 49:05 — What is a local variable?

Anything declared inside a method, constructor, block, or `for` loop —
temporary data, needed only while that method/loop/block is executing:

```java
class Test {
    Test() {
        int inConstructor = 1;   // local to the constructor
    }

    { int inBlock = 2; }         // local to the instance block

    static { int inStaticBlock = 3; }   // local to the static block

    public void m1() {
        int x = 10;              // local to m1
        for (int i = 0; i < 5; i++) {
            // i is local to the for loop
        }
        // i is not available here
    }
}
```

Other names for the same thing: **temporary variables**, **stack variables**
(stored in stack memory), **automatic variables**. Instance variable = part of
the object; static variable = part of the class; local = temporary data that
does not survive its block.

### 54:01 — The JVM never defaults a local — final or not

Instance and static variables get JVM defaults. Locals never do — you must
initialize explicitly. But the twist is **only before use**: an unused local
needs no initializer at all.

```java
class Test {
    public static void main(String[] args) {
        int x;
        System.out.println("Hello");   // valid — x is declared but never used
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int x;
        System.out.println(x);
        // CE: variable x might not have been initialized
    }
}
```

**Board:** *for local variables the JVM won't provide any default values;
initialization is compulsory before using that local — if you are not using
it, initialization is not required.*

### 1:01:42 — Even a `final` local can stay blank if unused

```java
class Test {
    public static void main(String[] args) {
        final int x;
        System.out.println("Hello");   // valid — prints Hello
    }
}
```

This is the one place `final` behaves *less* strictly than for instance or
static: a blank final instance/static variable is a compile error the moment
it exists unassigned, used or not. A blank final **local** is fine, precisely
because the "must initialize" rule for locals was always "before use," never
"unconditionally."

> ⚠️ **Modern Java — this is also why the compiler can require `final` (or its
> equivalent) on captured locals.**
> Since **Java 8**, a local variable read from inside a lambda or an anonymous
> inner class must be **final or effectively final** — assigned once and never
> reassigned afterward, even without writing the keyword:
>
> ```java
> int x = 5;
> Supplier<Integer> s = () -> x;   // valid — x is effectively final
> System.out.println(s.get());    // 5
> ```
>
> ```java
> int x = 5;
> Supplier<Integer> s = () -> x;
> x = 6;
> // CE: local variables referenced from a lambda expression
> //     must be final or effectively final
> ```
>
> Before Java 8, only an *explicitly* `final` local could be captured by an
> anonymous inner class; "effectively final" inference is what let lambdas
> (also new in 8) skip the keyword. Sir's rules about *where* a local gets its
> one value still decide whether a lambda can legally capture it.

## 1:06:26 — Access modifiers apply to instance/static — not to locals

```java
class Test {
    int x;                 // instance
    static int y;          // static

    public static void main(String[] args) {
        int z = 30;         // local
    }
}
```

The four access levels (`public`, default, `private`, `protected`) apply
identically to instance and static members:

```java
class Test {
    public int x;           // anywhere
    int x2;                 // default — current package
    private int x3;         // same class only
    protected int x4;       // package + subclasses

    public static int y;
    static int y2;
    private static int y3;
    protected static int y4;
}
```

A local variable is only ever reachable inside the block that declares it —
its scope is already fixed, so access-modifier terminology has nothing to add.
**The only modifier a local variable accepts is `final`**, and locals are not
final by default; you opt in only if you want the value locked.

### 1:11:11 — Illegal modifiers on locals — `illegal start of expression`

```java
class Test {
    public static void main(String[] args) {
        public int x = 10;
        // CE: illegal start of expression
    }
}
```

`private`, `protected`, `static`, `transient`, and `volatile` all fail the
same way on a local. Only `final` is accepted:

```java
class Test {
    public static void main(String[] args) {
        final int x = 10;
        System.out.println(x);   // 10
    }
}
```

| Modifier tried on a local | Result |
|---|---|
| `public` | CE: illegal start of expression |
| `private` | CE: illegal start of expression |
| `protected` | CE: illegal start of expression |
| `static` | CE: illegal start of expression |
| `transient` | CE: illegal start of expression |
| `volatile` | CE: illegal start of expression |
| `final` | valid — the only one |

### 1:14:25 — Story: "Java is not working on my system"

A working professional in Sir's class once reported, at the end of a
session, that Java "wasn't working properly" on her machine — some programs
compiled and ran, others didn't, so she suspected a broken `PATH` or
classpath. If that were true, *nothing* would compile. Asked for a failing
example, she produced:

```java
class Test {
    public static void main(String[] args) {
        public int x = 10;
        System.out.println(x);
        // CE: illegal start of expression
    }
}
```

The diagnosis: a local declared `public` — terminology that simply does not
apply there. **The problem was with the program, not with Java.**

### 1:17:08 — "No modifier means default access" is not for locals

```java
class Test {
    int x = 10;             // instance, no modifier → default access

    public static void main(String[] args) {
        int z = 30;         // local, no modifier — NOT "default access";
        System.out.println(z);   // 30
    }
}
```

"No modifier ⇒ default access" is a rule about *instance and static*
variables only. A local with no modifier isn't sitting at "default access" —
default access is a package-visibility concept, and a local was never visible
outside its own block to begin with.

## 1:20:08 — Formal parameters act as local variables

```java
class Test {
    public static void main(String[] args) {
        m1(10, 20);          // 10, 20 = actual parameters (arguments)
    }

    public static void m1(int x, int y) {   // x, y = formal parameters
        x = 100;
        y = 200;
        System.out.println(x + "..." + y);   // 100...200
    }
}
```

`x` and `y` here are **formal parameters**, scoped to `m1` exactly like any
other local. Because they *are* locals, they can be declared `final` — which
then blocks reassignment inside the method:

```java
class Test {
    public static void main(String[] args) {
        m1(10, 20);
    }

    public static void m1(final int x, int y) {
        x = 100;
        // CE: final parameter x may not be assigned
        y = 200;
        System.out.println(x + "..." + y);
    }
}
```

> ❗ **Correction — the compiler's actual wording differs from the note's
> paraphrase for this exact case.**
> A reassigned blank final *field* or *local* produces `cannot assign a value
> to final variable x`. A reassigned final **formal parameter** produces a
> distinct message, `final parameter x may not be assigned` — confirmed on
> `javac` from JDK 8 through JDK 26. Same underlying rule (can't rebind a
> final), different message because the compiler tracks parameters and other
> locals through separate code paths. Know the rule; don't over-memorize the
> exact string, because it depends on *which* kind of final variable you tried
> to reassign.

### 1:23:39 — Exam-style options

For the program above, four candidate explanations were offered:

1. There is no compile-time error.
2. Compile error — a formal parameter cannot be declared `final`.
3. Compile error — the method cannot reassign that final formal parameter.
4. No compile / no error.

**Answer: (3).** There *is* a compile error, but the reason is reassignment,
not the declaration. A formal parameter absolutely can be `final` — you just
cannot write to it afterward:

```java
class Test {
    public static void main(String[] args) {
        m1(10, 20);
    }

    public static void m1(final int x, final int y) {
        System.out.println(x + "..." + y);   // 10...20 — declared final, never reassigned
    }
}
```

**Board:** *formal parameters act as local variables of the method; hence a
formal parameter can be declared `final`; if it is, reassignment inside the
method is a compile-time error.*

## 1:28:00 — Close

Final instance, final static, final local, and formal parameters as locals —
that is the whole story of `final` on variables. Next session continues the
remaining member modifiers.

---

## Exam and interview points

1. **Final instance/static: no JVM default, ever** — even if `x` is never
   read, a blank `final` field that is never assigned is a compile error.
2. **Final instance must be assigned before constructor completion** — at
   declaration, in an instance block, or in a constructor. Never in a method.
3. **Final static must be assigned before class-loading completion** — at
   declaration or in a static block. Never in a method, static or otherwise.
4. **Modifier order is irrelevant**: `final static` ≡ `static final`,
   `public static` ≡ `static public`.
5. **Final local is the odd one out**: the JVM never defaults *any* local,
   final or not, but the requirement is only "initialize before use" — an
   unused blank `final int x;` is perfectly legal.
6. **The only modifier a local variable accepts is `final`.** Every other
   modifier (`public`, `private`, `protected`, `static`, `transient`,
   `volatile`) fails with `illegal start of expression` — a compile error in
   the program, not evidence of a broken JDK/PATH/classpath.
7. **"No modifier ⇒ default access" applies to instance and static only** —
   a local with no modifier is not "default access"; that concept doesn't
   extend to something whose scope was never wider than one block.
8. **Formal parameters are locals** and may be declared `final`; doing so
   blocks reassignment inside the method, but the exact compiler wording for
   that specific case is `final parameter x may not be assigned`, not the
   generic final-variable message.
9. **The classic MCQ trap**: "a formal parameter cannot be declared final" is
   the wrong reason for the compile error above — it *can* be declared final;
   what fails is the reassignment.
10. **Since Java 8, "effectively final" extends the same discipline to
    lambda/anonymous-class capture** — a captured local needs no `final`
    keyword as long as it is never reassigned after its one initialization,
    which is exactly the assign-once habit this lecture drills for locals.
11. **Since Java 16, records give you "final instance variable, set once
    before construction completes" as a language feature** — a record
    component is a `private final` field assigned by the generated
    constructor, no hand-written blank-final boilerplate required.

---

**Next:** Video 038 — static modifier
