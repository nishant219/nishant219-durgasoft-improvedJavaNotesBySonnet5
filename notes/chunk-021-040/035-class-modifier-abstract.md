# Video 035 — Class level modifiers: abstract

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-6|| Class Level Modifiers: abstract

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 35 of 203 |
| Series | Declarations and Access Modifiers · Part 6 of 14 |
| Topic | Abstract classes and abstract methods; modifier combinations |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 19m 08s (4748 seconds) |
| Video ID | UykTzY45Jyc |
| Watch | https://www.youtube.com/watch?v=UykTzY45Jyc |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** YouTube captions are blocked on this upload, so
> there is no timestamped transcript — sections below follow the lecture's own
> topic order instead of clock time. Two kinds of callout interrupt the
> teaching where it needs it: **⚠️ Modern Java** — what Sir taught was right
> for Java 6/7, and has since changed. **❗ Correction** — what was stated is
> not accurate, then or now. Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Concrete class vs abstract class
2. Abstract method = signature, no body
3. `new AbstractClass()` is a compile error
4. If a class has even one abstract method, the class **must** be abstract
5. A class **may** be abstract even with **zero** abstract methods (HttpServlet-style)
6. Child must implement every inherited abstract method **or** declare itself abstract
7. Three-level Parent / Child / GrandChild with `m1`, `m2`, `m3`
8. `abstract` is for **classes and methods**, never variables
9. Every legal / illegal modifier combination, as compilable or CE snippets
10. Empty abstract class is legal

---

## Concrete class vs abstract class

**Concrete class:** a class for which we **can** create an object. Almost every class written so far in this course is one.

```java
class Test {
}

class Demo {
    public static void main(String[] args) {
        Test t = new Test();
        System.out.println("object created");
        // prints object created
    }
}
```

**Abstract class:** a class for which we **cannot** create an object. Declared with the `abstract` modifier.

```java
abstract class Test {
}

class Demo {
    public static void main(String[] args) {
        Test t = new Test(); // CE: Test is abstract; cannot be instantiated
    }
}
```

Sir's line: an abstract class is **incomplete**. The JVM will not hand you an object of an incomplete type.

## We can still declare a reference

`new` is illegal, but a **reference variable** of the abstract type is fine — it just has to point at a concrete child object (polymorphism, covered later).

```java
abstract class Parent {
}

class Child extends Parent {
}

class Test {
    public static void main(String[] args) {
        Parent p;              // valid — reference only
        p = new Child();       // valid — object is concrete Child
        System.out.println(p);
        // prints Child@hashcode
        // Parent p2 = new Parent(); // CE
    }
}
```

## Abstract method

A method **without implementation** — no body, just a semicolon after the signature. It is incomplete, so it **must** be marked `abstract`.

```java
abstract class Test {
    public abstract void m1();
}
```

A body on an abstract method is illegal:

```java
abstract class Test {
    public abstract void m1() { // CE: abstract methods cannot have a body
        System.out.println("no");
    }
}
```

A concrete method in the same abstract class is legal — an abstract class can mix complete and incomplete members:

```java
abstract class Test {
    public abstract void m1();

    public void m2() {
        System.out.println("concrete method");
    }
}
```

```java
class Demo extends Test {
    public void m1() {
        System.out.println("implemented m1");
    }

    public static void main(String[] args) {
        Demo d = new Demo();
        d.m1();
        // prints implemented m1
        d.m2();
        // prints concrete method
    }
}
```

## If the class has an abstract method, the class must be abstract

Otherwise it is a compile error: *Test is not abstract and does not override abstract method m1()*.

```java
class Test {
    public abstract void m1(); // CE: Test is not abstract and does not override abstract method m1()
}
```

Fix: mark the class abstract.

```java
abstract class Test {
    public abstract void m1();
}
```

## Empty abstract class is legal

Zero abstract methods, still abstract. The modifier means "do not instantiate this class," nothing more.

```java
abstract class Test {
}
```

```java
class Demo {
    public static void main(String[] args) {
        Test t = new Test(); // CE: Test is abstract; cannot be instantiated
    }
}
```

An abstract class can even hold only concrete methods and still refuse instantiation:

```java
abstract class Test {
    public void m1() {
        System.out.println("m1");
    }

    public void m2() {
        System.out.println("m2");
    }
}

class Demo {
    public static void main(String[] args) {
        Test t = new Test(); // CE: Test is abstract; cannot be instantiated
    }
}
```

Sir's API story: `HttpServlet` is an abstract class whose `service`/`doGet`/`doPost` methods already have default implementations, yet it stays abstract so nobody writes `new HttpServlet()`. You extend it (`MyServlet extends HttpServlet`) and override only what you need.

```java
abstract class HttpServletDemo {
    public void doGet() {
        System.out.println("default doGet");
    }

    public void doPost() {
        System.out.println("default doPost");
    }
}

class MyServlet extends HttpServletDemo {
    public void doGet() {
        System.out.println("my doGet");
    }

    public static void main(String[] args) {
        MyServlet s = new MyServlet();
        s.doGet();
        // prints my doGet
        s.doPost();
        // prints default doPost
        // new HttpServletDemo(); // CE
    }
}
```

## Why abstract methods exist

The parent knows **that** a child must do something, but not **how**. Every vehicle has wheels, but the count differs:

```java
abstract class Vehicle {
    public abstract int getNoOfWheels();
}

class Bus extends Vehicle {
    public int getNoOfWheels() {
        return 6;
    }
}

class Auto extends Vehicle {
    public int getNoOfWheels() {
        return 3;
    }
}

class Test {
    public static void main(String[] args) {
        Vehicle v1 = new Bus();
        System.out.println(v1.getNoOfWheels());
        // prints 6
        Vehicle v2 = new Auto();
        System.out.println(v2.getNoOfWheels());
        // prints 3
        // Vehicle v3 = new Vehicle(); // CE
    }
}
```

Same idea with a person and their work:

```java
abstract class Person {
    String name;
    int age;

    public abstract void work();
}

class Student extends Person {
    public void work() {
        System.out.println("studies");
    }
}

class Employee extends Person {
    public void work() {
        System.out.println("job");
    }
}

class Test {
    public static void main(String[] args) {
        Person p1 = new Student();
        p1.work();
        // prints studies
        Person p2 = new Employee();
        p2.work();
        // prints job
    }
}
```

## Child must implement or stay abstract

If the parent has abstract methods, a child has exactly two legal choices:

1. Implement **every** abstract method → the child can be concrete.
2. Leave any of them unimplemented → the child **must** be `abstract` too.

```java
abstract class Parent {
    public abstract void m1();
    public abstract void m2();
    public abstract void m3();
}
```

`Child` implements only `m1` → still incomplete → must be abstract:

```java
abstract class Child extends Parent {
    public void m1() {
        System.out.println("m1");
    }
}
```

Forgetting `abstract` on `Child` is a compile error:

```java
class Child extends Parent { // CE: Child is not abstract and does not override abstract method m2()
    public void m1() {
        System.out.println("m1");
    }
}
```

`GrandChild` implements the rest → concrete:

```java
class GrandChild extends Child {
    public void m2() {
        System.out.println("m2");
    }

    public void m3() {
        System.out.println("m3");
    }
}
```

Who can we `new`?

```java
class Test {
    public static void main(String[] args) {
        // Parent p = new Parent();       // CE: Parent is abstract
        // Child c = new Child();         // CE: Child is abstract
        GrandChild g = new GrandChild();
        g.m1();
        // prints m1
        g.m2();
        // prints m2
        g.m3();
        // prints m3
        Parent p = new GrandChild();
        p.m1();
        // prints m1
    }
}
```

A partially-implemented `GrandChild` is still abstract:

```java
abstract class GrandChild extends Child {
    public void m2() {
        System.out.println("m2");
    }
    // m3 still abstract
}
```

## Abstract class can have a `main` method — we can even run it

You cannot instantiate an abstract class, but you **can** start the JVM against one, because `main` only needs to exist as a static entry point — no object required.

```java
abstract class Test {
    public static void main(String[] args) {
        System.out.println("abstract class main");
        // prints abstract class main
    }
}
```

```text
javac Test.java
java Test
// prints abstract class main
```

An abstract class can also have constructors, static methods, instance methods, instance variables, and static variables — none of that requires the class itself to be instantiable, only a concrete descendant (whose constructor chains up through the abstract class's constructor).

```java
abstract class Test {
    int x = 10;
    static int y = 20;

    Test() {
        System.out.println("abstract class constructor");
    }

    public void m1() {
        System.out.println("instance method");
    }

    public static void m2() {
        System.out.println("static method");
    }

    public abstract void m3();
}

class Child extends Test {
    public void m3() {
        System.out.println("m3");
    }

    public static void main(String[] args) {
        Child c = new Child();
        // prints abstract class constructor
        System.out.println(c.x);
        // prints 10
        System.out.println(y);
        // prints 20
        c.m1();
        // prints instance method
        m2();
        // prints static method
        c.m3();
        // prints m3
    }
}
```

## `abstract` is never for variables

```java
class Test {
    abstract int x = 10; // CE: modifier abstract not allowed here
}
```

```java
abstract class Test {
    abstract int x; // CE: modifier abstract not allowed here
}
```

Instance, static, and local variables can never be abstract. Incomplete **behaviour** is a method problem, not a field problem.

## The modifier-combination table, as Java snippets

Sir fills a modifier-combination table on the board. Each cell below is a compilable (or deliberately broken) class or method declaration, not a prose row.

### Class: `public` + `abstract` — legal

```java
public abstract class Test {
    public abstract void m1();
}
```

```java
public abstract class EmptyPublicAbstract {
}
```

### Class: `public` + `final` — legal (previous video)

```java
public final class Test {
    public static void main(String[] args) {
        System.out.println("public final ok");
        // prints public final ok
    }
}
```

### Class: `final` + `abstract` — illegal

Opposite meanings collide: `final` says "cannot be extended," `abstract` says "must be extended to be usable."

```java
final abstract class Test { // CE: illegal combination of modifiers: abstract and final
}
```

```java
abstract final class Test2 { // CE: order does not matter; still illegal combination
}
```

```java
public final abstract class Test3 { // CE: illegal combination of modifiers: abstract and final
}
```

> ⚠️ **Modern Java — a third option now sits between `final` and `abstract`.**
> **Sealed classes** (Java **17**, JEP 409) let a class say "cannot be extended
> — except by this named list," which is a middle ground `final` and `abstract`
> never offered:
>
> ```java
> sealed abstract class Shape permits Circle, Square {
>     public abstract double area();
> }
>
> final class Circle extends Shape {
>     double r;
>     Circle(double r) { this.r = r; }
>     public double area() { return Math.PI * r * r; }
> }
>
> final class Square extends Shape {
>     double side;
>     Square(double side) { this.side = side; }
>     public double area() { return side * side; }
> }
> ```
>
> `sealed` and `abstract` combine on the same class (verified: compiles clean
> under `--release 17`) — a sealed class can still be abstract, and each
> `permits` subclass must itself be `final`, `sealed`, or `non-sealed`. The
> payoff arrives with **pattern matching for switch** (Java **21**): because the
> compiler knows the *complete* set of subtypes, a `switch` over a sealed
> hierarchy can be exhaustive with no `default` branch —
> `switch (s) { case Circle c -> c.area(); case Square sq -> sq.area(); }`
> compiles as-is (verified under `--release 21`). Separately, a **record** (Java
> **16**) is implicitly `final` and can never be `abstract`, but it can be one of
> a sealed interface's permitted cases — records and sealed types are usually
> taught together for exactly this reason.

### Class: `abstract` + `strictfp` — legal

`strictfp` on a **class** applies to the concrete code inside it. An abstract class is allowed to contain concrete methods, so the combination is legal.

```java
abstract strictfp class Test {
    public void m1() {
        System.out.println(10.0 / 3);
    }

    public abstract void m2();
}
```

```java
public abstract strictfp class Test2 {
}
```

### Class: `final` + `strictfp` — legal

```java
final strictfp class Test {
    public static void main(String[] args) {
        System.out.println(10.0 / 3);
    }
}
```

### Class: `public` + `strictfp` — legal

```java
public strictfp class Test {
}
```

### Method: `abstract` + `public` — legal (the common case)

```java
abstract class Test {
    public abstract void m1();
}
```

```java
abstract class Test2 {
    abstract void m1(); // default-access abstract method — also legal
}
```

```java
abstract class Test3 {
    protected abstract void m1(); // legal
}
```

### Method: `abstract` + `final` — illegal

A `final` method cannot be overridden. An `abstract` method **must** be overridden (implemented) in a child. The two contradict each other.

```java
abstract class Test {
    public abstract final void m1(); // CE: illegal combination of modifiers: abstract and final
}
```

```java
abstract class Test2 {
    final abstract void m1(); // CE
}
```

### Method: `abstract` + `private` — illegal

Private members are not visible in the child, so the child could never implement the method.

```java
abstract class Test {
    private abstract void m1(); // CE: illegal combination of modifiers: abstract and private
}
```

### Method: `abstract` + `static` — illegal

`static` is a class-level facility; `abstract` is about instance-level overriding. Static methods are not overridden anyway — they are hidden.

```java
abstract class Test {
    public abstract static void m1(); // CE: illegal combination of modifiers: abstract and static
}
```

```java
abstract class Test2 {
    static abstract void m1(); // CE
}
```

### Method: `abstract` + `synchronized` — illegal

`synchronized` describes locking behaviour **during the body's execution**. An abstract method has no body to lock around.

```java
abstract class Test {
    public abstract synchronized void m1(); // CE: illegal combination of modifiers: abstract and synchronized
}
```

### Method: `abstract` + `native` — illegal

`native` means "the body lives in C/C++." `abstract` means "no body here, the child supplies a Java body." Two mutually exclusive stories about where the missing body comes from.

```java
abstract class Test {
    public abstract native void m1(); // CE: illegal combination of modifiers: abstract and native
}
```

### Method: `abstract` + `strictfp` — illegal

`strictfp` governs **floating-point implementation**. No body means nothing for it to apply to.

```java
abstract class Test {
    public abstract strictfp void m1(); // CE: illegal combination of modifiers: abstract and strictfp
}
```

Contrast with class-level `abstract strictfp`, which **is** legal (snippet above) — the restriction is specifically about a body-less method, not about the class.

### Method: concrete + `strictfp` — legal

```java
class Test {
    public strictfp void m1() {
        System.out.println(10.0 / 3);
    }

    public static void main(String[] args) {
        new Test().m1();
    }
}
```

> ⚠️ **Modern Java — every `strictfp` in this section is now a no-op.**
> Since **Java 17** (JEP 306), all floating-point arithmetic is strict by
> default — the behaviour `strictfp` used to switch on. The keyword still
> parses and every legal combination above still compiles, but `javac
> -Xlint:strictfp` flags it (verified):
>
> ```text
> warning: [strictfp] as of release 17, all floating-point expressions are
> evaluated strictly and 'strictfp' is not required
> ```
>
> The *illegal* combinations (`abstract strictfp` on a method) are unchanged —
> the modifier-combination rule is a syntax check independent of what
> `strictfp` does semantically, and it still fires even though the keyword
> itself now does nothing. For the OCJP exam and for reading legacy code, learn
> every combination above as before; in code you write today, `strictfp` is
> dead weight.

## Implementation in the child is overriding

The child's method is a **concrete override** of the parent's abstract method. Signature rules (name, argument types, compatible return type, access no weaker than the parent's) are the general overriding rules, covered fully in the OOPs videos — this is the minimum needed here.

```java
abstract class Parent {
    public abstract void m1();
}

class Child extends Parent {
    public void m1() {
        System.out.println("override / implement");
    }

    public static void main(String[] args) {
        Parent p = new Child();
        p.m1();
        // prints override / implement
    }
}
```

Weakening the access modifier is a compile error (a preview of overriding + access):

```java
abstract class Parent {
    public abstract void m1();
}

class Child extends Parent {
    void m1() { // CE: m1() in Child cannot override m1() in Parent; attempting to assign weaker access privileges; was public
        System.out.println("default cannot hide public");
    }
}
```

## Abstract class vs interface (seed only)

Sir defers the full comparison to the interface videos. One board line for now: both can declare abstract methods; the differences (variables, constructors, multiple inheritance) come later.

```java
abstract class A {
    public abstract void m1();
}

interface B {
    void m1(); // public abstract by default — later videos
}
```

> ⚠️ **Modern Java — interfaces stopped being "abstract methods only" in Java 8.**
> When this was recorded, the contrast Sir is setting up was sharp: an abstract
> class could mix concrete and abstract members, an interface could not. That
> stopped being true with:
>
> - **Java 8** — `default` and `static` methods, so an interface can ship a real
>   implementation:
>   ```java
>   interface Greeter {
>       default void greet() {
>           System.out.println("hello");
>       }
>   }
>   ```
> - **Java 9** — `private` (and `private static`) interface methods, for helper
>   code shared between an interface's own `default` methods.
>
> An interface still cannot hold instance state (no instance variables beyond
> `public static final` constants) and still has no constructor — those two
> stay the real dividing line from an abstract class, and are exactly the "later
> videos" comparison Sir is pointing at.

## Code from the lecture

The Parent / Child / GrandChild board program, in full:

```java
abstract class Parent {
    public abstract void m1();
    public abstract void m2();
    public abstract void m3();
}

abstract class Child extends Parent {
    public void m1() {
        System.out.println("m1 method");
    }
}

class GrandChild extends Child {
    public void m2() {
        System.out.println("m2 method");
    }

    public void m3() {
        System.out.println("m3 method");
    }

    public static void main(String[] args) {
        GrandChild g = new GrandChild();
        g.m1();
        // prints m1 method
        g.m2();
        // prints m2 method
        g.m3();
        // prints m3 method
        Parent p = new GrandChild();
        p.m1();
        // prints m1 method
        // Parent p2 = new Parent(); // CE
        // Child c = new Child();     // CE
    }
}
```

## Rules

1. Abstract class → cannot instantiate (`new` is a compile error); a reference is fine.
2. Abstract method → no body; the class that contains it must be abstract.
3. An abstract class may have zero abstract methods.
4. A child that implements all inherited abstract methods may be concrete; otherwise it must stay abstract.
5. `abstract` + `final` (class or method) → CE.
6. `abstract` + `public` (class or method) → OK.
7. Method combos that are CE: `abstract` with `private`, `static`, `synchronized`, `native`, `strictfp`, `final`.
8. Class combo `abstract strictfp` is OK; method combo `abstract strictfp` is not.
9. Variables can never be `abstract`.
10. An empty `abstract class A {}` is valid.

## Exam and interview points

1. **"Abstract class cannot have a constructor / `main` / static method" is false.** It can have all three — only `new` on the abstract type itself is illegal.
2. **"Abstract class must have at least one abstract method" is false.** Zero is fine; `HttpServlet` is the standard example of an all-concrete abstract class.
3. **`abstract final class` is always CE**, in any modifier order — a favourite one-mark combination question.
4. **`new` on an abstract type is CE even with zero abstract methods** — it is the modifier that blocks instantiation, not the method count.
5. **Forgetting to mark a child `abstract`** when it still has unimplemented inherited methods (`m2`/`m3` in the drill above) is the most common miss in this topic.
6. **`public abstract strictfp void m1();` is CE; `abstract strictfp class Test { }` is not** — the illegal combination is specific to methods without a body.
7. **Method combos that are always CE:** `abstract` with `private`, `static`, `synchronized`, `native`, `final`, and (method-level only) `strictfp`.
8. **`strictfp` is legacy knowledge as of Java 17** — still correct for the exam and for reading old code, but writing it today changes nothing (JEP 306 made all floating-point math strict by default).
9. **Sealed classes (17) are the modern middle ground between `final` and `abstract`** — "no children, except this named list" — and pair with pattern matching for switch (21) for exhaustive, `default`-free dispatch over the hierarchy.
10. **Interfaces gained `default` (8), `static` (8), and `private` (9) methods**, so "interface = only abstract methods" is a Java 6/7 fact, not a current one. The real class-vs-interface line today is state and constructors, not method bodies.

---

**Next:** Video 036 — Member-level modifiers (and `strictfp`)
