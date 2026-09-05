# Video 053 — Inheritance HAS-A relationship

## Video info

**Title:** Core Java With OCJP/SCJP:OOPs(Object Oriented Programming)Part-3 || Inheritance||has a relationship

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 53 of 203 |
| Series | OOPs · Part 3 |
| Topic | Inheritance, HAS-A relationship |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 21m 57s |
| Video ID | 2GM56vHVLzM |
| Watch | https://www.youtube.com/watch?v=2GM56vHVLzM |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is OOPs Part 3, picking up right after IS-A (Video 052). Board flow:
HAS-A → composition vs aggregation → IS-A vs HAS-A → method signature →
start of method overloading.

1. **HAS-A** — the everyday relationship you already use without naming it
   (a `Student` has a `name`), and its payoff: assemble an object from parts
   written once, used everywhere (the `Engine`/`Car` story).
2. **Composition vs aggregation** — the "small minor difference" that cost a
   real student a job offer: strong association (University→Department,
   closes together) vs weak association (Department→Professor, survives
   independently).
3. **IS-A vs HAS-A, side by side** — want *all* of a class's functionality
   automatically → `extends`. Want only a slice of it → hold a reference,
   call the one or two methods you need.
4. **Method signature** — name + argument types only, never the return type
   or the modifiers. Every overloading/overriding rule from here on leans on
   this definition.
5. **Method overloading, introduced** — same name, different argument
   types; why C forces `abs`/`labs`/`fabs` and Java doesn't; and the first
   hint that overloading resolves at compile time, by reference type.

### 00:06 — Recap: last session was IS-A (inheritance)

Last session covered **IS-A** — the inheritance concept — and its important
loopholes. This session's relationship is **HAS-A**: very important for the
interview room, and something every OCJP candidate needs total clarity on.
What is it, what's it for, what's the advantage — that's the agenda.

### 00:44 — HAS-A is the most commonly used relation (often without noticing)

IS-A gets all the terminology attention, but the relationship used most often
in day-to-day coding is actually **HAS-A** — we just don't usually name it.
We use it constantly without saying the word.

### 01:22 — Everyday example: Student has a name / roll number

This pattern already appeared repeatedly in earlier classes:

```java
class Student {
    String name;
    int rollno;
}
```

What is the relation between `Student` and `name`? **Student has-a name.**
Student has-a roll number. That's HAS-A, even though nobody in the room ever
called it that — it's been HAS-A the whole time.

### 02:03 — Advantage of HAS-A: Car composed from many vendors

The biggest-advantage story: building a car. A car needs a number of
**components**, and not every component of a Honda City comes from Honda —
wheels, engine, and other parts may come from different vendors. Honda
**composes** those parts into one car object and releases it to market.

Building a big object out of several individual components is
**composition** or **aggregation**.

### 03:19 — Engine class written once; Car holds Engine reference

Engine functionality is required by every car, so write `Engine` once, separately:

```java
class Engine {
    void start() {
        System.out.println("engine start");
    }

    void stop() {
        System.out.println("engine stop");
    }
}
```

`Car` requires engine functionality, so it creates an Engine object:

```java
class Car {
    Engine e = new Engine(); // Car HAS-A Engine reference
}
```

The relation between `Car` and `Engine` is **Car has-a Engine reference**.
By using `e`, Car can call Engine's methods without redefining them — this
relationship is **composition** / **HAS-A**:

```java
class Engine {
    void start() {
        System.out.println("engine start");
    }
}

class Car {
    Engine e = new Engine();

    void drive() {
        e.start(); // reuse Engine functionality via HAS-A
        System.out.println("car driving");
    }
}

class Test {
    public static void main(String[] args) {
        new Car().drive();
        // prints engine start
        // prints car driving
    }
}
```

> ⚠️ **Modern Java — `var` (10) shortens every one of these declarations.**
> `Engine e = new Engine();` already names the type twice. Since **Java 10**
> (JEP 286), a local variable with an initializer can drop the explicit type
> and let the compiler infer it — the declared type is still `Engine`, just
> unwritten:
> ```java
> class Car {
>     var e = new Engine();
>     // CE: 'var' is not allowed here — var is LOCAL-variable-only
> }
>
> class Test {
>     public static void main(String[] args) {
>         var car = new Car();  // inferred type: Car
>         car.drive();
>         // prints engine start
>         // prints car driving
>     }
> }
> ```
> `var` only works for **local variables** with an initializer (locals in a
> method, constructor, or initializer block, including for-loop and
> try-with-resources variables) — never for fields, method parameters, or
> return types, so `Engine e = new Engine();` as a *field* stays exactly as
> Sir wrote it. Confirmed on JDK 26.

### 05:28 — Point 1: HAS-A = composition or aggregation

**First point about HAS-A:** it is also known as **composition** or
**aggregation** — composing a car from several individual objects.

### 05:56 — Point 2: no specific keyword (mostly `new`)

**Second:** there is **no specific keyword** to implement HAS-A.

- Instance functionality → create an object (`new`) and use it.
- Static functionality → not even an object is required.

Most of the time we just depend on `new`.

```java
class Engine {
    static void serviceTip() {
        System.out.println("change oil");
    }

    void start() {
        System.out.println("start");
    }
}

class Car {
    Engine e = new Engine(); // HAS-A via new (instance)

    void demo() {
        e.start();
        Engine.serviceTip(); // static — object not required
        // prints start
        // prints change oil
    }
}
```

### 06:31 — Point 3: biggest advantage = code reusability

Write engine functionality **once**. Wherever engine functionality is
required, create an object and call it. Same reusability advantage IS-A
gives you — just achieved through HAS-A instead.

### 07:09 — Summary of three HAS-A points (board)

1. HAS-A is also known as **composition** or **aggregation**.
2. **No specific keyword** to implement HAS-A; most of the time we depend on **`new`**.
3. Main advantage of HAS-A: **code reusability**.

```java
class Engine {
    void start() {
        System.out.println("written once in Engine");
    }
}

class Car {
    Engine e = new Engine(); // HAS-A — composition / aggregation
}

class Bike {
    Engine e = new Engine(); // reuse Engine again
}

class Test {
    public static void main(String[] args) {
        new Car().e.start();
        new Bike().e.start();
        // prints written once in Engine
        // prints written once in Engine
    }
}
```

### 09:46 — Board example again: Car has Engine reference

Terminology drilled once more: **Car has-a Engine reference.**

```java
class Engine {
    String type = "petrol";
}

class Car {
    Engine e = new Engine();
}

class Test {
    public static void main(String[] args) {
        Car c = new Car();
        System.out.println(c.e.type);
        // prints petrol
    }
}
```

### 11:04 — Interview story: composition vs aggregation (SCJP vs interview)

For the SCJP/OCJP exam, the three points above are enough. But a student who
walked into an interview learned otherwise.

The interviewer asked to explain IS-A and HAS-A. The student answered
correctly: IS-A is inheritance, HAS-A is also known as composition or
aggregation — the exact board points above. Then the interviewer asked:
**what's the difference between composition and aggregation?** The student
said both are the same, both are HAS-A — and got rejected. He came back
asking for the real answer.

**Both are HAS-A, but there's a small, minor difference between the two** —
and one student missed a job over that half-point.

### 13:18 — Composition: University and Department (strong association)

There is one **University**, and within it several **departments** (CSE,
ECE, Civil, Mechanical, …). The relation: **University has-a department.**

- University = **container object**
- Department objects = **contained objects**

Suppose the government closes the university tomorrow for illegal activity.
All its departments close automatically — a department is part of the
university, and **without the university, there is no chance of the
department existing.**

Without the container object, if there is **no chance** of the contained
objects existing, container and contained are **strongly associated**. This
strong association is nothing but **composition**.

```java
class Department {
    String name;

    Department(String name) {
        this.name = name;
    }

    void close() {
        System.out.println(name + " closed");
    }
}

class University {
    // container holds contained objects directly — composition
    Department d1 = new Department("CSE");
    Department d2 = new Department("ECE");

    void shutDown() {
        // closing container → contained go with it (composition story)
        d1.close();
        d2.close();
        System.out.println("university closed");
    }
}

class Test {
    public static void main(String[] args) {
        new University().shutDown();
        // prints CSE closed
        // prints ECE closed
        // prints university closed
    }
}
```

Board line (dictated):

> *Without existing container object, if there is no chance of existing
> contained objects, then container and contained objects are ***strongly
> associated***. This strong association is nothing but ***composition***.*

Example restated: University consists of several departments. Without an
existing university, there's no chance of an existing department — hence
University and Department are strongly associated → **composition**.

### 20:34 — Aggregation: Department and Professor (weak association)

Second part: **aggregation**. There is one **Department**, and within it
several **professors** work (P1, P2, … Pn).

Suppose the college decides to close the department (demand for IT/MCA
falls). Do the professors close with it? **No.** The university can
**transfer** them to another department, or **release** them to join
another university altogether.

**Without the department (container), there may still be a chance of the
professor objects (contained) existing.** That is a **weak association** —
nothing but **aggregation**.

- Composition: objects **strongly** associated
- Aggregation: objects **weakly** associated

```java
class Professor {
    String name;

    Professor(String name) {
        this.name = name;
    }

    void teach() {
        System.out.println(name + " teaching");
    }
}

class Department {
    // container just holds references — professors can outlive it
    Professor p1;
    Professor p2;

    Department(Professor p1, Professor p2) {
        this.p1 = p1;
        this.p2 = p2;
    }
}

class Test {
    public static void main(String[] args) {
        Professor a = new Professor("P1");
        Professor b = new Professor("P2");
        Department it = new Department(a, b);
        // close department conceptually — professors still usable
        it = null;
        a.teach();
        b.teach();
        // prints P1 teaching
        // prints P2 teaching
    }
}
```

Board line (dictated):

> *Without existing container object, if there is a chance of existing
> contained objects, then container and contained objects are ***weakly
> associated***. This weak association is nothing but ***aggregation***.*

Example restated: Department consists of several professors. Without an
existing department, there may still be a chance of existing professor
objects — hence Department and Professor are weakly associated →
**aggregation**.

### 28:36 — Note 1: strong vs weak

- In **composition**, objects are **strongly** associated.
- In **aggregation**, objects are **weakly** associated.

```java
// COMPOSITION — strong: contained dies with container (conceptual)
class University {
    private final Department dept = new Department("CSE");
}

// AGGREGATION — weak: container only uses contained
class Department {
    private Professor professor; // reference only; professor may outlive department

    void assign(Professor p) {
        this.professor = p;
    }
}
```

### 29:55 — Note 2: holds object vs holds reference

Special care — one more difference:

- In **composition**: contained objects are **directly** within the container (part of the whole).
- In **aggregation**: the container just holds the **reference** of the contained objects.

A department has to exist within the university, but a professor can serve
that department from outside, may leave after classes, and can even work in
two departments at once — the container just holds references.

```java
class Engine {
    // part of Car — composition style (owned)
}

class Car {
    private Engine engine = new Engine(); // holds / owns contained object directly
}

class Professor {
}

class Department {
    private Professor professor; // holds just a reference (aggregation)

    void setProfessor(Professor p) {
        this.professor = p;
    }
}
```

Board (dictated):

> *In composition, container object holds ***directly*** the contained objects.*

> *Whereas in aggregation, container object holds ***just the references*** of contained objects.*

If anyone in an interview asks the difference between composition and
aggregation, this is the answer to give:

|  | Composition | Aggregation |
|---|---|---|
| Association | Strong | Weak |
| Lifetime | Without container → no contained | Without container → contained may still exist |
| Holding | Holds contained object directly (part of) | Holds just references |
| Example | University–Department | Department–Professor |

> ⚠️ **Modern Java — records (16) give composition a built-in, immutable shape.**
> When the container genuinely *owns* its parts for their whole lifetime —
> the composition case — a **record** (Java 16, JEP 395) says that in one
> line: the constructor, accessors, `equals`/`hashCode`/`toString` are all
> generated from the component list, and every component is `final`:
> ```java
> record Engine(String type) {
>     void start() {
>         System.out.println(type + " engine start");
>     }
> }
>
> record Car(Engine engine) {          // Car HAS-A Engine — composition
>     void drive() {
>         engine.start();
>         System.out.println("car driving");
>     }
> }
>
> class Test {
>     public static void main(String[] args) {
>         var car = new Car(new Engine("petrol"));
>         car.drive();
>         // prints petrol engine start
>         // prints car driving
>     }
> }
> ```
> Confirmed on JDK 26 (and back to 16 with `--release 16`). This is a fit for
> composition specifically — the contained `Engine` is handed in once and
> can't be swapped out — not for aggregation, where the whole point is that
> the reference can be reassigned or transferred (`department.assign(newProf)`),
> which a record's `final` components don't allow. Sir's `new`-in-the-field
> style is still exactly how OCJP-era code (and most mutable Java code today)
> is written; records are the newer option when immutability is what you want.

### 33:00 — Purpose of IS-A; when IS-A vs when HAS-A

The main purpose of IS-A is **reusability** of code — same as HAS-A. The
question is which one to reach for.

**If the total functionality** of a class is required — that functionality
is part of your requirement — go for **IS-A**.

```java
class Person {
    String name;
    int age;

    void walk() {
        System.out.println("person walk");
    }

    void talk() {
        System.out.println("person talk");
    }
}

class Student extends Person {
    // total Person functionality by default available — IS-A
    int rollno;
}

class Test {
    public static void main(String[] args) {
        Student s = new Student();
        s.walk();
        s.talk();
        // prints person walk
        // prints person talk
    }
}
```

**If you don't need the total functionality** — say a `Test` class has 100
methods and a `Demo` only needs one or two — create a `Test` object and call
just what you need. That's **HAS-A**.

```java
class Test {
    void m1() {
        System.out.println("m1");
    }

    void m2() {
        System.out.println("m2");
    }

    // ... imagine ~100 methods
    void m100() {
        System.out.println("m100");
    }
}

class Demo {
    Test t = new Test(); // HAS-A — only need part of Test

    void use() {
        t.m1(); // only what we need
        // prints m1
        // do NOT inherit all 100 methods via extends
    }
}
```

Rule:

- Want **total** functionality of a class automatically as part of your type → **IS-A**
- Want **part of** the functionality (call one or two methods) → **HAS-A**

Both concepts ultimately serve **reusability** — write once, use everywhere.

### 36:22 — Board: IS-A vs HAS-A

Board recap, same rule, generalized:

- Total functionality automatically → **IS-A**.
- Specific / part functionality only → **HAS-A**.

```java
class Person {
    void eat() {
        System.out.println("eat");
    }
}

class Student extends Person {
    // complete functionality of Person required for Student → IS-A
}

class Utility {
    void m1() {
        System.out.println("need this");
    }

    void m2() {
        System.out.println("need this too");
    }

    void m3() { /* ... */ }
    // ... many more not needed by client
}

class Client {
    Utility u = new Utility(); // HAS-A — part of functionality

    void run() {
        u.m1();
        u.m2();
        // prints need this
        // prints need this too
    }
}
```

That's all of IS-A and HAS-A for this module.

### 39:39 — Bridge topic before overloading/overriding: method signature

Next up: **overloading** and **overriding**. Before that, one concept needs
to be crystal clear, because it gets used repeatedly in both:
**method signature**.

- In **overloading**, method signatures must be **different**.
- In **overriding**, method signatures must be **same**.

### 40:34 — What is method signature in Java?

```java
public static int m1(int i, float f) {
    return 10;
}
```

What's the signature of this method? Not the whole declaration.

**Method declaration** includes modifiers, return type, method name, and
argument list. **Method signature** is narrower: **method name followed by
argument types** — nothing else.

- Return type is **not** part of the method signature.
- Modifiers are **not** part of the method signature.

For the example above, the signature is **`m1(int, float)`**.

```java
class Demo {
    // declaration: modifiers + return type + name + args
    public static int m1(int i, float f) {
        return 10;
    }
    // signature in Java: m1(int, float)
    // NOT part of signature: public, static, int (return type)
}
```

> ❗ **Correction — "in C/C++ return type is part of the method signature" is a widely repeated myth, and it's backwards for C++.**
> C has no method overloading at all, so it has no notion of "signature" to
> compare in the first place. C++ *does* have overloading, and its overload
> resolution — like Java's — deliberately **excludes** the return type. Two
> C++ functions differing only in return type are a compile error, not a
> valid overload:
> ```cpp
> int    m1(int i) { return i; }
> double m1(int i) { return i; } // error: functions that differ only in
>                                 // their return type cannot be overloaded
> ```
> Confirmed with `c++` (Clang) on this machine. Java's rule — name plus
> argument types, return type excluded — is not a Java oddity next to C/C++;
> it's the same rule every mainstream overloading language uses, because
> return type alone can't disambiguate a call site (`m1(5)` gives the
> compiler no return-type context to pick from).

### 42:15 — Board: method signature definition

Board version of the same rule: in Java, method signature = **method name
followed by argument types**.

```java
public static int m1(int i, float f) {
    return 0;
}
// signature → m1(int, float)

class Sample {
    void process(String s, int n) {
    }
    // signature: process(String, int)
}
```

### 43:41 — Return type is not part of method signature in Java

Repeated board point: **return type is not a part of method signature in Java.**

```java
class Check {
    int calc(int x) {
        return x;
    }
    // signature: calc(int) — return type int is NOT in the signature
}
```

### 44:24 — Who uses method signature? Compiler (method table)

Where does this get used? Take a class with two methods:

```java
class Test {
    public void m1(int i) {
    }

    public void m2(String s) {
    }
}
```

Two methods, two signatures: `m1(int)` and `m2(String)`. For every class the
compiler maintains a **method table** — for class `Test`, that table holds
`m1(int)` and `m2(String)`.

### 45:52 — Resolving calls with the method table

```java
class Test {
    public void m1(int i) {
        System.out.println("m1 int");
    }

    public void m2(String s) {
        System.out.println("m2 String");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10);
        // prints m1 int
        t.m2("Durga");
        // prints m2 String
    }
}
```

For `t.m1(10)`: calling `m1` with an **int** argument, on `t` of type
`Test`. Test's method table has `m1(int)` → valid call. For `t.m2("Durga")`:
calling `m2` with a **String**, and Test's table has `m2(String)` → legal.

### 47:13 — Invalid call: cannot find symbol

```java
class Test {
    public void m1(int i) {
    }

    public void m2(String s) {
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m3(10.5);
        // CE: cannot find symbol
        // symbol:   method m3(double)
        // location: variable t of type Test
    }
}
```

`10.5` is **double** by default. `Test`'s method table has no `m3(double)`
entry, so the compiler reports **cannot find symbol** — that missing
"symbol" is exactly the method signature it went looking for. This is the
compiler using the method signature to **invoke / resolve method calls**.

### 49:02 — Board conclusion: compiler resolves method calls via signature

**Compiler will use method signature to resolve method calls.**

```java
class Test {
    void m1(int i) {
        System.out.println("int");
    }

    void m2(String s) {
        System.out.println("String");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1(10);       // OK — signature m1(int) found
        t.m2("Durga");  // OK — signature m2(String) found
        // t.m3(10.5);  // CE: cannot find symbol — method m3(double)
    }
}
```

### 51:55 — Important conclusion: same signature not allowed in one class

```java
class Test {
    public void m1(int i) {
    }

    public int m1(int x) {
        return 10;
    }
}
```

Valid or invalid? **Invalid.** Both methods have the signature `m1(int)` —
the return type doesn't count, so this is a genuine duplicate. If you call
`t.m1(10)`, which method should respond? Ambiguity. The compiler objects
that `m1(int)` is already defined.

**Within a class, two methods with the same signature are not allowed** —
even with different return types, even if one is abstract and one is
static.

```java
class Test {
    public void m1(int i) {
    }

    public int m1(int x) {
        return 10;
        // CE: method m1(int) is already defined in Test
    }
}
```

Verified on JDK 26 — javac's actual message is `method m1(int) is already
defined in class Test`.

### 55:45 — Same example rewritten on board

```java
class Test {
    public void m1(int i) {
        // signature: m1(int)
    }

    public int m1(int x) {
        return 10;
        // signature: m1(int) — same
        // CE: m1(int) is already defined in Test
        // return type is NOT part of method signature
    }
}
```

That's method signature — the piece overloading and overriding both lean on.

### 58:45 — Next major concept: method overloading

Two methods are said to be **overloaded** if and only if both have the
**same name** but **different argument types**.

`m1(int i)` and `m1(double d)` — overloaded? **Yes.**

```java
class Demo {
    void m1(int i) {
        System.out.println("int version");
    }

    void m1(double d) {
        System.out.println("double version");
    }
    // same name, different argument types → overloaded methods
}
```

### 1:01:01 — Why overloading matters: C vs Java (abs)

Is overloading there in **C**? No. `abs` returns the absolute value —
ignore the sign, `abs(10.5)` and `abs(-10.5)` both give `10.5`. In C, `abs`
covers `int` only; long needs **`labs`**; float needs **`fabs`** — a new
method name every time the argument type changes, because C doesn't allow
two methods with the same name and different argument types. That forces
more names to remember and increases the complexity of the program.

In **Java**, the same name `abs` works for int, long, float — same name,
different argument types is exactly what an **overloaded method** is.

```java
// C-style naming forced by lack of overloading (conceptual contrast)
class CStyleAbs {
    int abs(int i) {
        return i < 0 ? -i : i;
    }

    long labs(long l) { // different name required in C
        return l < 0 ? -l : l;
    }

    float fabs(float f) { // different name required in C
        return f < 0 ? -f : f;
    }
}

// Java: overloading — same name, different argument types
class JavaAbs {
    int abs(int i) {
        return i < 0 ? -i : i;
    }

    long abs(long l) {
        return l < 0 ? -l : l;
    }

    float abs(float f) {
        return f < 0 ? -f : f;
    }
}

class Test {
    public static void main(String[] args) {
        JavaAbs a = new JavaAbs();
        System.out.println(a.abs(-10));
        System.out.println(a.abs(-10L));
        System.out.println(a.abs(-10.5f));
        // prints 10
        // prints 10
        // prints 10.5
    }
}
```

### 1:06:17 — Board: C language — no overloading

Board recap: C has no method overloading concept, so multiple methods with
the same name but different argument types aren't allowed there. A change
in argument type forces a new method name, which increases the complexity
of the programming.

### 1:09:11 — Board: Java — overloaded methods

Java, by contrast, lets you declare multiple methods with the same name but
different argument types — **overloaded methods**. This reduces complexity
and gives the programmer more flexibility.

```java
class MathStyle {
    int abs(int i) {
        return i < 0 ? -i : i;
    }

    long abs(long l) {
        return l < 0 ? -l : l;
    }

    float abs(float f) {
        return f < 0 ? -f : f;
    }
    // overloaded methods
}
```

### 1:11:40 — Live example: three overloaded m1 methods

```java
class Test {
    public void m1() {
        System.out.println("no-arg method");
    }

    public void m1(int i) {
        System.out.println("int-arg method");
    }

    public void m1(double d) {
        System.out.println("double-arg method");
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1();
        // prints no-arg method
        t.m1(10);
        // prints int-arg method
        t.m1(10.5);
        // prints double-arg method
    }
}
```

Three methods, same name, different argument types → **overloaded methods**.

### 1:15:00 — Method resolution in overloading (important conclusion)

Here `t`'s reference type and underlying object are both `Test` — the same.
Later, parent-reference/child-object cases will appear.

**In overloading, method resolution is always taken care of by the compiler
based on reference type.** If parent and child both have overload-related
methods, which one gets the chance is decided by the **compile-time
reference type** (detail comes with the parent-child examples later).

Hence method overloading is also considered:

- **Compile-time polymorphism**
- **Static polymorphism**
- **Early binding**

— because method binding happens at compile time.

```java
class Parent {
    void m1(int i) {
        System.out.println("parent");
    }
}

class Child extends Parent {
    void m1(double d) {
        System.out.println("child");
    }
}

class Demo {
    public static void main(String[] args) {
        Parent p = new Child(); // parent reference, child object
        p.m1(10);
        // prints parent
        // overloading resolution: compiler uses reference type Parent
        // (full parent/child overloading cases — next sessions)
    }
}
```

### 1:18:51 — Star this theory point

**In overloading, method resolution always takes care by compiler based on
reference type.** Hence overloading is also compile-time polymorphism /
static polymorphism / early binding.

Method resolution means: **which method has to execute** when multiple
candidates exist (parent/child, or multiple overloads).

- Overloading → the compiler decides, based on **reference type** — the
  runtime object doesn't factor in.
- (Preview) Overriding → resolution is based on the **runtime object**
  instead, and the reference becomes effectively a "dummy" for that
  decision — covered in the overriding sessions.

This still holds exactly as taught: nothing about how overloading resolves
has changed in any later Java release — it is compile-time, reference-type
based, in Java 6 and in Java 25 alike.

### 1:21:32 — Closing: basic idea of overloading; cases next session

That's the basic idea of overloading. Five or six cases come next — each
one important for both interview and exam. Those cases are Video 054.

## Quick revision card

| Topic | Takeaway |
|---|---|
| HAS-A | Also composition / aggregation; no keyword (mostly new); advantage = reusability |
| Composition | Strong association; without container → no contained (University–Department) |
| Aggregation | Weak association; without container → contained may exist (Department–Professor) |
| IS-A vs HAS-A | Total functionality → IS-A; part of functionality → HAS-A |
| Method signature (Java) | method name + argument types; not return type / modifiers |
| Same signature in one class | Not allowed (even if return types differ) |
| Overloading | Same name, different argument types |
| Overloading resolution | Compiler, based on reference type → compile-time / static polymorphism / early binding |

## Exam and interview points

1. **HAS-A is composition or aggregation, implemented mostly through `new`** —
   there's no dedicated keyword, and the payoff is code reusability: write a
   class once, hold a reference to it wherever you need its behavior.
2. **The composition/aggregation half-point that costs interviews:**
   composition is a *strong* association — the contained object cannot
   exist without the container (University closes → Department closes with
   it) — while aggregation is *weak* — the contained object survives the
   container (Department closes → Professor transfers elsewhere). Both are
   HAS-A; only the lifetime coupling differs.
3. **Composition holds the contained object directly; aggregation holds
   only a reference to it** — a second, independent way to draw the same
   line, worth having ready alongside the strong/weak framing.
4. **IS-A vs HAS-A is a completeness question, not a preference:** want the
   *entire* functionality of a class automatically → `extends` (IS-A). Want
   only a slice of it → hold a reference and call what you need (HAS-A).
   Both exist for reusability.
5. **Method signature = name + argument types, full stop.** Return type and
   modifiers are never part of it in Java — and, contrary to a common myth,
   C++ excludes return type from overload resolution too; only C has no
   overloading concept to compare against at all.
6. **Two methods with the same signature cannot coexist in one class**, even
   with different return types, and even if one is `abstract` and the other
   `static` — the compiler has no way to pick between them at a call site.
7. **Overloading = same name, different argument types**, and it is the
   entire reason Java needs only one `abs` where C needs `abs`/`labs`/`fabs`
   — lack of overloading in C is what forces the extra names.
8. **Overloading resolves at compile time, based on the reference type** —
   which is why it's called compile-time polymorphism / static polymorphism
   / early binding. This is unchanged in every Java release since; overload
   resolution has never become a runtime decision.
9. **`var` (Java 10)** lets any of these local declarations drop the
   explicit type (`var e = new Engine();`) — locals only, never fields or
   parameters. **Records (Java 16)** give the *composition* case (owning,
   non-swappable parts) a one-line, immutable declaration; aggregation,
   where the reference can be reassigned, still wants a plain mutable field.

**Next:** Video 054 — Method Overloading Cases
