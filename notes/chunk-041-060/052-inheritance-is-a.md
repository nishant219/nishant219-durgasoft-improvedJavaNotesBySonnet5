# Video 052 — Inheritance (IS-A)

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-2 || Inheritance||is a relationship

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 52 of 203 |
| Series | OOPs · Part 2 |
| Topic | Inheritance, IS-A relationship |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 18m 49s |
| Video ID | 7m5WIj3lpcE |
| Watch | https://www.youtube.com/watch?v=7m5WIj3lpcE |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is **OOPs Part 2**, module 2 after the security module (data hiding,
abstraction, encapsulation) covered in Video 051. Sir does **not** teach
HAS-A, polymorphism, or overriding here — those are later videos. This
session is IS-A only:

1. What IS-A relationship means, and why it is also called inheritance
2. The `extends` keyword and reusability
3. Four reference-type loopholes — what a parent or child reference can and
   cannot call
4. Why inheritance saves code (the loan-module example)
5. How the whole Java API — `Object`, `Throwable`, the exception hierarchy —
   is built on inheritance
6. Why Java rejects multiple inheritance for classes but allows it for
   interfaces
7. Cyclic inheritance, and why it is rejected too

---

## 00:05 — Recap: last session started OOPs, module 1 was security

Last session started **OOPs**. Its first block of features was about
**security** — four ideas, all pointing at one word:

### 00:20 — Data hiding

**Data hiding:** an outside class can't access your internal data directly;
internal data should not go out directly.

### 00:36 — Abstraction

**Abstraction:** hide the internal implementation, and highlight only the
set of services you are offering.

### 00:54 — Encapsulation and tightly encapsulated class

Data hiding + abstraction is **encapsulation**. After encapsulation, module 1
covered the **tightly encapsulated class**.

Those four ideas are module one, and they are all one word: **security**.
Module two starts now.

---

## 01:40 — Module 2 starts: IS-A relationship = inheritance

**IS-A relationship** is the inheritance concept. What's the benefit, and
what are the loopholes — that's this video.

### 02:17 — Three outline points before any example

Theory first, no internals yet:

1. **IS-A relationship is also known as inheritance.**
2. It's implemented with the **`extends`** keyword.
3. Biggest advantage: **parent class members are by default available to the
   child.** A method written once in the parent can be called on a child
   object without rewriting it. That advantage is **reusability**.

```java
class Parent {
    void inherited() {
        System.out.println("written once in parent");
    }
}

class Child extends Parent {
    // inherited() is here by default — do not rewrite
}

class Test {
    public static void main(String[] args) {
        new Child().inherited();
        // prints written once in parent
    }
}
```

### 04:10 — Board: the three-point outline

> **Board — IS-A relationship**
> 1. It is also known as **inheritance**.
> 2. The main advantage of IS-A relationship is **code reusability**.
> 3. By using the **`extends`** keyword we can implement IS-A relationship.

```java
class P {
    void m1() {
        System.out.println("parent");
    }
}

class C extends P { // extends implements IS-A
}

class Test {
    public static void main(String[] args) {
        new C().m1(); // reuse — not rewritten in C
        // prints parent
    }
}
```

That's the outline. Next is what it means, and the loopholes.

---

## 06:19 — First example: `class P` with `m1`, `class C extends P` with `m2`

`class P` (parent) contains **one** method, `m1`. `class C extends P` adds
its own method, `m2`.

```java
class P {
    public void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    public void m2() {
        System.out.println("child");
    }
    // C has m1 (inherited) + m2 (own) = 2 methods
}
```

Parent class contains one method. Child class contains **two** — `m1` is by
default available to the child, because that's what inheritance means.

### 07:46 — Big B analogy (Amitabh → Abhishek → next child)

Whatever fame your parent has, the child gets by default, without defining
it anywhere. Sir's example: **Big B** (Amitabh Bachchan) is famous in India,
so **Abhishek Bachchan** inherits that fame automatically — he doesn't have
to earn it again. A future child of Abhishek gets Big B's fame *and*
Abhishek's, stacked, without writing a line to claim it.

```java
class Amitabh {
    public void fame() {
        System.out.println("Big B fame");
    }
}

class Abhishek extends Amitabh {
    // fame() by default available — not rewritten
}

class NextBachchan extends Abhishek {
    // fame() from Amitabh + anything Abhishek has — by default
}

class Test {
    public static void main(String[] args) {
        new NextBachchan().fame();
        // prints Big B fame
    }
}
```

---

## 09:35 — Loopholes start: `class Test`, four cases

Four cases, each its own conclusion.

### 10:10 — Case 1: parent reference, parent object

```java
P p = new P();
p.m1();   // valid — parent reference, parent method
p.m2();   // ?
```

`p.m1()` is **100% valid** — parent reference, parent object, parent method.

`p.m2()` is a **compile-time error**. Parent members are available to the
child by default, but child members are **not** available to the parent.
`m2` is child-specific — `P` doesn't have it.

```java
class Test {
    public static void main(String[] args) {
        P p = new P();
        p.m2();
        // CE: cannot find symbol
        // symbol: method m2()
        // location: class P
    }
}
```

Conclusion: **on a parent reference, child-specific methods can't be
called.**

### 12:12 — Case 2: child reference, child object

```java
class Test {
    public static void main(String[] args) {
        C c = new C();
        c.m1();   // valid — parent method, by default available to child
        c.m2();   // valid — child's own method
        // prints parent
        // prints child
    }
}
```

No surprises here.

### 12:54 — Case 3: parent reference holding child object (dangerous)

```java
P p1 = new C();   // parent reference holding a child object — valid
```

**No problem at all** — a parent reference can hold a child object.

`p1.m1()` is valid — a parent method, available on the child.

`p1.m2()` is **100% invalid, compile-time error**, even though the runtime
object is a `C`. **The compiler resolves calls by the reference's declared
type, not the object's runtime type.** `p1` is declared `P`; `P` has no
`m2`.

```java
class Test {
    public static void main(String[] args) {
        P p1 = new C();
        p1.m1();
        // prints parent
        p1.m2();
        // CE: cannot find symbol
        // symbol: method m2()
        // location: class P
        // runtime object is C, but the compiler checks reference type P
    }
}
```

Sir plants the obvious question: *if you can't call the child-specific
method through it, what's the point of holding a child object in a parent
reference?* The answer is **polymorphism** — covered in a later session.

### 15:05 — Case 4: child reference holding parent object

```java
C c1 = new P();
```

**Invalid.** A parent reference can hold a child object, but a child
reference **cannot** hold a parent object — a `P` is not guaranteed to have
everything a `C` has.

```java
class Test {
    public static void main(String[] args) {
        C c1 = new P();
        // CE: incompatible types: P cannot be converted to C
    }
}
```

The dangerous one is case 3 — people expect it to work because the runtime
object *is* the child, forgetting that the compiler only ever looks at the
reference type.

### 16:30 — Board: the full P / C / Test example, in one place

```java
class P {
    public void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    public void m2() {
        System.out.println("child");
    }
}

class Test {
    public static void main(String[] args) {
        P p = new P();
        p.m1();
        p.m2();
        // CE: cannot find symbol
        // symbol: method m2()
        // location: class P

        C c = new C();
        c.m1();
        c.m2();
        // prints parent
        // prints child

        P p1 = new C();
        p1.m1();
        p1.m2();
        // CE: cannot find symbol
        // symbol: method m2()
        // location: class P

        C c1 = new P();
        // CE: incompatible types: P cannot be converted to C
    }
}
```

Both `m2`-on-a-`P`-reference cases fail with the **same** compile-time
error — same reason both times.

---

## 20:08 — The four conclusions

### 20:24 — Conclusion 1

> **Board:** Whatever methods parent has, by default available to the
> child, and hence on the child reference we can call both parent and
> child class methods.

```java
C c = new C();
c.m1(); // parent method on child reference
c.m2(); // child method on child reference
```

### 22:04 — Conclusion 2

> **Board:** Whatever methods a child has, by default not available to the
> parent, and hence on the parent reference we can't call child-specific
> methods.

```java
P p = new P();
p.m1(); // OK
p.m2(); // CE: cannot find symbol — child-specific method, not on P
```

### 23:15 — Conclusion 3 (the dangerous one)

> **Board:** Parent reference can be used to hold a child object, but by
> using that reference we can't call child-specific methods — we can call
> only the methods present in the parent class.

```java
P p1 = new C(); // hold child object — allowed
p1.m1();        // parent method — allowed
p1.m2();        // CE: cannot find symbol — child-specific, not on P
// (polymorphism benefit — later session)
```

### 25:16 — Conclusion 4

> **Board:** Parent reference can be used to hold a child object, but
> child reference cannot be used to hold a parent object.

```java
P p1 = new C(); // OK
C c1 = new P(); // CE: incompatible types: P cannot be converted to C
```

| # | Conclusion |
|---|---|
| 1 | Parent methods by default available to child → on child reference we can call both parent and child methods |
| 2 | Child methods by default not available to parent → on parent reference we can't call child-specific methods |
| 3 | Parent reference can hold child object, but through that reference only parent methods (polymorphism benefit — later) |
| 4 | Parent reference can hold child object, but child reference cannot hold parent object |

---

## 26:31 — Advantage of inheritance, and when to reach for it

Biggest advantage: **code reusability**. Sir builds it with a loan module,
pretending for a moment he doesn't know `extends` exists.

### 27:37 — Without inheritance vs. with inheritance (loan module)

A loan module needs several loan types: **vehicle loan**, **personal
loan**, **home loan**, and more.

### 28:09 — Without inheritance: three classes, 300 methods each

```java
class VehicleLoan {
    // 300 methods
}

class HomeLoan {
    // around 300 methods
}

class PersonalLoan {
    // 300 methods
}

// 900 methods total, ~90 hours of development time (Sir's rough numbers)
```

### 29:22 — The expert programmer's question

Sir plays the naive author, shows the code to an "expert programmer," and
gets asked: *do you know inheritance? If you did, you wouldn't need this
much code or this much time.*

### 30:06 — With inheritance: 250 common methods move into `class Loan`

Of the 300 methods per loan type, about **250 are common** to every loan.
Pull those into one class:

```java
class Loan {
    // 250 common methods — applicable to any type of loan
    void calculateInterest() {
        System.out.println("common loan interest logic");
    }
}
```

### 31:12 — `VehicleLoan extends Loan` — only 50 specific methods left

```java
class VehicleLoan extends Loan {
    // 250 parent methods by default available — do not rewrite
    void registerVehicle() {
        System.out.println("vehicle-loan specific");
    }
    // ... 49 more specific methods (50 total)
}
```

### 32:00 — `HousingLoan` and `PersonalLoan` extend `Loan` the same way

```java
class HousingLoan extends Loan {
    void registerHouse() {
        System.out.println("housing-loan specific");
    }
    // 50 specific methods
}

class PersonalLoan extends Loan {
    void checkSalary() {
        System.out.println("personal-loan specific");
    }
    // 50 specific methods
}
```

### 33:02 — 400 methods, 40 hours

Total: 250 + 50 + 50 + 50 = **400 methods**, roughly **40 hours** —
against 900 methods and 90 hours without inheritance. The second approach
is the only defensible one: same requirement, less code, less time.

### 33:45 — What "code reusability" actually means; the redundancy problem

Without inheritance, the 250 common methods are written **three times** —
**code redundancy**. Change one of them and you must change it in three
places (same failure mode as denormalized data in a database). With
inheritance those 250 methods are written **once** and reused on every
child.

```java
class Loan {
    void common() {
        System.out.println("written once");
    }
}

class VehicleLoan extends Loan { }
class HousingLoan extends Loan { }
class PersonalLoan extends Loan { }

class Test {
    public static void main(String[] args) {
        new VehicleLoan().common();
        new HousingLoan().common();
        new PersonalLoan().common();
        // written once, reused three times — this is code reusability
    }
}
```

### 35:07 — Board: without inheritance | with inheritance

**Without inheritance**

```java
class VehicleLoan {  /* 300 methods */ }
class HousingLoan  {  /* 300 methods */ }
class PersonalLoan {  /* 300 methods */ }
// 900 methods, 90 hours of development time
```

**With inheritance**

```java
class Loan { /* 250 common methods */ }

class VehicleLoan  extends Loan { /* 50 specific methods */ }
class HousingLoan  extends Loan { /* 50 specific methods */ }
class PersonalLoan extends Loan { /* 50 specific methods */ }
// 400 methods, 40 hours of development time
```

### 38:16 — Where to define common vs. specific methods

> **Board:** The most common methods, applicable for any type of child, we
> have to define in the parent class. The specific methods, applicable
> only for a particular child, we have to define in the child class.

```java
class Loan {
    void commonForAnyLoan() {
        System.out.println("parent — any type of child");
    }
}

class VehicleLoan extends Loan {
    void vehicleOnly() {
        System.out.println("child — particular child only");
    }
}

class Test {
    public static void main(String[] args) {
        VehicleLoan v = new VehicleLoan();
        v.commonForAnyLoan();
        v.vehicleOnly();
        // prints parent — any type of child
        // prints child — particular child only
    }
}
```

---

## 40:20 — The entire Java API is built on inheritance

`Object`, `String`, `StringBuffer`, `Thread`, … all of Java's own API is
implemented using inheritance. **`Object`** is the root for all Java classes.

### 40:48 — Board sketch: `Object`, `String`, `StringBuffer`, `Throwable`

```java
// the java.lang / java.io hierarchy Sir sketches on the board
class Object { }

class String extends Object { }
class StringBuffer extends Object { }
class Throwable extends Object { }

class Exception extends Throwable { }
class Error extends Throwable { }

class RuntimeException extends Exception { }
class IOException extends Exception { }

class ArithmeticException extends RuntimeException { }
class NullPointerException extends RuntimeException { }

class OutOfMemoryError extends Error { }
```

### 42:13 — `Object`'s 11 methods, written once for 5,000+ classes

`Object` has **11 methods** — the ones common to every Java object. Written
once, automatically available to every one of the 5,000+ classes in the
JDK. Without inheritance, those 11 methods would need to be written 5,000
times over.

```java
class String extends Object {
    // does not rewrite Object's 11 methods
}

class Test {
    public static void main(String[] args) {
        String s = "durga";
        System.out.println(s.hashCode());
        // Object's method, available without rewriting in String
    }
}
```

> ⚠️ **Modern Java — one of those 11 methods is on its way out.**
> `Object.finalize()` was deprecated in **Java 9** as unreliable cleanup
> (no guaranteed timing, no guaranteed call at all, and it can resurrect a
> "dead" object). Since **Java 18** (JEP 421), finalization is **disabled
> by default** at the JVM level — `finalize()` methods simply do not run
> unless you opt back in with `--finalization=enabled`, a flag due for
> removal. The count of 11 is still correct as a historical fact about the
> class; the *working* replacement for cleanup logic is
> `java.lang.ref.Cleaner` (Java 9+) or try-with-resources, not
> `finalize()`.

### 43:45 — Why `Object` acts as root

Because the methods common to *any* Java object are defined there. Making
it the root means every class gets them without rewriting.

### 44:11 — Why `Throwable` is the root of the exception hierarchy

- Methods common to any **exception** → `Exception` class
- Methods common to any **error** → `Error` class
- Methods common to **exception or error** → `Throwable` class

That's why `Throwable` roots the exception hierarchy.

```java
class Throwable extends Object {
    // common methods for exception AND error
}

class Exception extends Throwable {
    // common methods for any exception
}

class Error extends Throwable {
    // common methods for any error
}
```

### 45:04 — Board: `Object` as root for all Java classes

> **Board:** Total Java API is implemented based on the inheritance
> concept. The most common methods applicable to any Java object are
> defined in `Object` class, and hence every class in Java is a child
> class of `Object`, either directly or indirectly, so that `Object`'s
> methods are by default available to every Java class without
> rewriting. Due to this, `Object` acts as root for all Java classes.

```java
class A {
    // does not extend anyone → still a child of Object (directly)
}

class B extends A {
    // child of A, grandchild of Object (indirectly)
}

class Test {
    public static void main(String[] args) {
        A a = new A();
        B b = new B();
        a.hashCode(); // Object method, no rewrite
        b.hashCode(); // Object method, no rewrite
    }
}
```

### 48:01 — Board: `Throwable` as root for the exception hierarchy

> **Board:** `Throwable` class defines the most common methods required
> for every exception and error class. Hence this class acts as root for
> the Java exception hierarchy.

```java
class Throwable extends Object {
    // most common methods required for every Exception and Error
}

class Exception extends Throwable { }
class Error extends Throwable { }
```

---

## 49:29 — Does Java support multiple inheritance?

**No** — a Java class can't extend more than one class at a time.

```java
class A extends B, C {
}
// CE: '{' expected — a class cannot list two direct superclasses;
// the grammar itself only allows one
```

### 50:18 — Board: multiple inheritance (classes)

> **Board:** A Java class can't extend more than one class at a time,
> hence Java won't provide support for multiple inheritance in classes
> (with respect to classes).

### 51:51 — Interview trap: "A extends B, and everything extends Object, so multiple inheritance exists"

An interviewer might argue: *`class A extends B`, and every class is also
a child of `Object` — so `A` extends two classes, `B` and `Object`, at
once — multiple inheritance!* This is wrong: `Object` is above `B` in the
chain, not a second, independent `extends` on `A`.

```java
class B { }

class A extends B { }

class Test {
    public static void main(String[] args) {
        A a = new A();
        System.out.println(a instanceof B);      // true
        System.out.println(a instanceof Object);  // true
        // true for Object because of the chain A → B → Object,
        // not because A has two separate superclasses
    }
}
```

```java
class A extends B, Object {
}
// CE: '{' expected — this is not what Java does
```

### 53:23 — Direct vs. indirect child of `Object`

If a class **doesn't extend any other class**, it is a **direct** child of
`Object`.

```java
class A {
    // then only A is DIRECT child class of Object
}
```

If a class **does extend another class**, it is only an **indirect** child
of `Object` — `A` is the child of `B`; `B` is the child of `Object`. This
is called **multi-level inheritance**, not multiple inheritance.

```java
class B { }

class A extends B {
    // A → B → Object — multi-level inheritance, NOT multiple inheritance
}
```

### 54:29 — Board note 1

> **Board:** If our class doesn't extend any other class, then only our
> class is direct child class of `Object`.

```java
class A { }

class Test {
    public static void main(String[] args) {
        System.out.println(new A() instanceof Object); // true
    }
}
```

### 55:46 — Board note 2

> **Board:** If our class extends any other class, then our class is
> indirect child class of `Object`.

```java
class B { }

class A extends B { }

class Test {
    public static void main(String[] args) {
        A a = new A();
        System.out.println(a instanceof B);      // true
        System.out.println(a instanceof Object);  // true
    }
}
```

The "A extends both B and Object" story gets the cross mark — invalid,
never happens. The correct picture is a straight chain:

```java
class Object { } // root
class B extends Object { }
class A extends B { }
// A the child of B, B the child of Object — multi-level, not multiple
```

### 57:17 — Either directly or indirectly, no multiple inheritance for classes

> **Board:** Either directly or indirectly, Java won't provide support for
> multiple inheritance with respect to classes.

### 58:27 — Why Java won't support multiple inheritance

### 59:10 — Ambiguity: `C extends P1, P2`, both have `m1()`

Assume (hypothetically — Java doesn't allow the syntax) `C extends P1,
P2`, and both `P1` and `P2` declare `m1()`. Calling `c.m1()` — which
version runs, `P1`'s or `P2`'s? There's no way to resolve that. That
ambiguity is the reason Java rejects multiple inheritance for classes.

```java
class P1 {
    public void m1() {
        System.out.println("P1 m1");
    }
}

class P2 {
    public void m1() {
        System.out.println("P2 m1");
    }
}

// class C extends P1, P2 { }   // not legal Java — illustrative only
// new C().m1();                // which m1 would run? Ambiguous, unresolvable.
```

> ⚠️ **Modern Java — a class can now limit who is allowed to extend it.**
> Since **Java 17** (JEP 409), a class can be declared `sealed` with an
> explicit `permits` list — only the named subclasses may extend it, and
> each of them must be `final`, `sealed`, or `non-sealed`:
>
> ```java
> sealed class Shape permits Circle, Square { }
> final class Circle extends Shape { }
> final class Square extends Shape { }
> final class Triangle extends Shape { }
> // CE: class is not allowed to extend sealed class: Shape
> // (as it is not listed in its 'permits' clause)
> ```
>
> This doesn't change anything Sir taught about single inheritance or the
> ambiguity argument — it adds a new axis of control *on top of* `extends`:
> not just "how many classes can I extend" but "who is allowed to extend
> **me**." A `record` (Java 16) sits at the opposite extreme: it implicitly
> extends the final class `java.lang.Record`, so a record can neither
> extend anything else nor be extended itself.

---

## 1:01:52 — But with interfaces, `C extends A, B` is valid

**`interface A`**, **`interface B`**, **`interface C extends A, B`** — this
is **100% valid**. **An interface can extend any number of interfaces
simultaneously**, so Java *does* support multiple inheritance with respect
to interfaces.

```java
interface A { }

interface B { }

interface C extends A, B {
    // valid — an interface can extend any number of interfaces
}
```

### 1:02:55 — Board: interfaces can extend any number of interfaces

> **Board:** An interface can extend any number of interfaces
> simultaneously, hence Java provides support for multiple inheritance
> with respect to interfaces.

### 1:04:26 — Why ambiguity doesn't show up in interfaces

### 1:05:18 — Multiple declarations, one implementation

`ParentInterface1` declares `m1()`. `ParentInterface2` declares the same
`m1()`. Neither has a **body** — an interface method (at the time this was
recorded) is only a declaration. Both declarations flow into
`ChildInterface`. The **implementing class** is the only place that
supplies a body, and there is exactly one such class, so there's exactly
one implementation. Multiple declarations, unique implementation — no
ambiguity.

```java
interface ParentInterface1 {
    void m1(); // declaration only — no body
}

interface ParentInterface2 {
    void m1(); // same m1 — still declaration only
}

interface ChildInterface extends ParentInterface1, ParentInterface2 {
    // m1 declaration comes from both parents — still no body
}

class ImplementationClass implements ChildInterface {
    public void m1() {
        System.out.println("unique implementation");
    }
}

class Test {
    public static void main(String[] args) {
        ChildInterface c = new ImplementationClass();
        c.m1();
        // prints unique implementation
    }
}
```

### 1:07:21 — Board diagram: two parent interfaces, one implementation class

Whichever of the two declarations "asks" for its implementation, the
answer is always the same object: the single implementing class. If the
implementations needed to differ, you'd need separate implementing
classes — but the declarations are identical, so one class satisfies both.

```java
interface PI1 { void m1(); }
interface PI2 { void m1(); }
interface CI extends PI1, PI2 { void m1(); }

class ImplementationClass implements CI {
    public void m1() {
        System.out.println("only one implementation for all declarations");
    }
}
```

### 1:08:51 — Board: multiple declarations, unique implementation, no ambiguity

> **Board:** Even though multiple method declarations are available, but
> implementation is unique, and hence there is no chance of ambiguity
> problem in interfaces.

> ⚠️ **Modern Java — default methods bring the ambiguity problem back.**
> Since **Java 8**, an interface method can carry a body (`default void
> m1() { ... }`). If two interfaces each give `m1()` a *different* default
> body, the "unique implementation" argument above no longer holds — the
> conflict is real, and the compiler refuses to guess:
>
> ```java
> interface A { default void m1() { System.out.println("A"); } }
> interface B { default void m1() { System.out.println("B"); } }
>
> interface C extends A, B {
> }
> // CE: interface C inherits unrelated defaults for m1() from types A and B
> ```
>
> You must resolve it yourself, by overriding `m1()` and picking (or
> combining) an implementation explicitly with `InterfaceName.super`:
>
> ```java
> interface C extends A, B {
>     default void m1() {
>         A.super.m1(); // explicitly choose A's version
>     }
> }
> // now valid — and any class implementing C inherits this resolution
> ```
>
> This is the classic "diamond problem" people associate with C++ multiple
> inheritance — Java only avoided it as long as interface methods had no
> bodies. Pre-8, Sir's reasoning is airtight; post-8, it holds only for
> interfaces that stick to abstract (body-less) methods.

### 1:10:05 — Strictly speaking: interfaces don't give you inheritance

**Strictly speaking, what you get through interfaces is not inheritance.**
Code reusability means implementation is available without rewriting it —
and here there's only a **declaration**, no implementation to reuse. So
strictly speaking, interfaces give neither inheritance nor multiple
inheritance, even though the `extends A, B` syntax makes it look that way.
Sir's own concession: *"majority of the people still consider it multiple
inheritance — even we are following the same style."*

```java
interface A { void m1(); } // declaration only — nothing to reuse
interface B { void m1(); } // declaration only

interface C extends A, B {
    // still no implementation — strictly speaking, not inheritance
}

class Impl implements C {
    public void m1() {
        System.out.println("implementation is here — not inherited from A or B");
    }
}
```

> ⚠️ **Modern Java — default methods make this argument only partly true
> now.** Sir's point rests entirely on "interface methods have no body, so
> there's nothing to reuse." Since **Java 8**, that premise fails for
> `default` (and `static`) interface methods — they carry a real,
> inheritable implementation:
>
> ```java
> interface Greeter {
>     default void greet() {
>         System.out.println("hello from the interface itself");
>     }
> }
>
> class Person implements Greeter {
>     // greet() is used as-is, with zero rewriting — genuine reuse
> }
>
> class Test {
>     public static void main(String[] args) {
>         new Person().greet();
>         // prints hello from the interface itself
>     }
> }
> ```
>
> So the modern, precise statement is: an interface built only from
> abstract methods still gives you no reusable implementation (Sir's
> "strictly not inheritance" stands). An interface with `default` methods
> genuinely does — and can genuinely collide the way two classes' methods
> would, which is exactly what the previous callout's diamond-problem
> example showed.

### 1:11:14 — Board: strictly speaking, no inheritance through interfaces

> **Board:** Strictly speaking, through interfaces we won't get any
> inheritance.

---

## 1:11:54 — Cyclic inheritance: `class A extends A`

```java
class A extends A {
}
```

Is a class allowed to extend itself? Or:

```java
class A extends B { }
class B extends A { }
```

Is that allowed? Both are **cyclic inheritance**, and **cyclic inheritance
is not allowed in Java.**

```java
class A extends A {
}
// CE: cyclic inheritance involving A
```

### 1:13:26 — Why cyclic inheritance is useless, not just illegal

`class A extends A`: `A`'s methods are already available inside `A` — it's
the same class. `extends A` adds nothing. `class A extends B` plus `class
B extends A`: if `B` needs `A`'s methods and `A` needs `B`'s methods, that
requirement is already satisfiable by putting everything in one class.
There's never a reason for the cycle — which is also why no mainstream
language allows it.

```java
class A extends B { }
class B extends A { }
// CE: cyclic inheritance involving A

// if A needs B's methods and B needs A's methods, put them in ONE class:
class Combined {
    void fromWouldBeA() { System.out.println("A's methods"); }
    void fromWouldBeB() { System.out.println("B's methods"); }
}
```

### 1:15:18 — Live compile: `javac A.java`

Sir compiles both cases to show the exact message:

```java
class A extends A {
}
// javac A.java
// CE: cyclic inheritance involving A
```

```java
class A extends B { }
class B extends A { }
// javac A.java
// CE: cyclic inheritance involving A
```

### 1:16:31 — Board: cyclic inheritance is not allowed

> **Board:** Cyclic inheritance is not allowed in Java. Of course, it is
> not required.

---

## 1:18:29 — Close: IS-A loopholes

That's the full set of loopholes for IS-A relationship, also known as
inheritance.

```java
// summary of this video's compile-time rules
class P {
    public void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    public void m2() {
        System.out.println("child");
    }
}

class Test {
    public static void main(String[] args) {
        C c = new C();
        c.m1();
        c.m2();
        // prints parent
        // prints child

        P p1 = new C();
        p1.m1();
        // prints parent
        // p1.m2();       // CE: cannot find symbol — method m2() — location: class P
        // C c1 = new P(); // CE: incompatible types: P cannot be converted to C
        // class A extends B, C { }  // CE: '{' expected — no multiple class inheritance
        // class A extends A { }     // CE: cyclic inheritance involving A
    }
}
```

---

## Exam and interview points

1. **Parent members are available to the child by default; child members
   are never available to the parent.** This single asymmetry explains all
   four reference-type loopholes.
2. **The compiler resolves method calls by the reference's declared type,
   not the object's runtime type.** `P p1 = new C(); p1.m2();` fails at
   compile time even though the runtime object is a `C` — this is the
   trap most people miss (it's not a polymorphism failure, it's ordinary
   compile-time type checking).
3. **A child reference can never hold a parent object** — `C c1 = new
   P();` is a compile-time `incompatible types` error, full stop.
4. **Java has no multiple inheritance for classes** (a class can extend
   only one class — it's a syntax rule, not just a semantic one) **but
   does have it for interfaces** (an interface can extend any number of
   interfaces).
5. **Why**: multiple class inheritance would create ambiguity with no way
   to resolve it (`C extends P1, P2`, both declare `m1()` — which runs?).
   Pre-Java-8 interfaces avoided this because method declarations carried
   no implementation, so there was only ever one implementation to run.
   Since Java 8, `default` methods can reintroduce exactly this ambiguity,
   and Java forces you to resolve it explicitly with `InterfaceName.super`.
6. **"A extends B, and everything extends Object" is not multiple
   inheritance** — it's multi-level inheritance (`A → B → Object`), a
   straight chain, not two independent superclasses.
7. **Cyclic inheritance (`class A extends A`, or `A extends B` /
   `B extends A`) is a compile-time error**: `cyclic inheritance involving
   A`. It's also logically pointless — anything a cycle could achieve, a
   single class already achieves.
8. **`Object` is the root of every Java class**, directly or indirectly,
   because it holds the 11 methods common to any Java object.
   **`Throwable` is the root of the exception hierarchy** for the same
   reason, one level down (exception-or-error-common methods live in
   `Throwable`; exception-only in `Exception`; error-only in `Error`).
9. **The practical case for inheritance is measurable, not aesthetic**:
   Sir's loan-module arithmetic (900 methods/90 hours without inheritance
   vs. 400 methods/40 hours with a shared `Loan` parent) is the standard
   answer to "why should I use inheritance" in an interview.
10. **Modern Java caveats worth naming out loud in an interview**:
    `finalize()` (one of `Object`'s 11 methods) is deprecated since Java 9
    and disabled by default since Java 18; `sealed` classes (Java 17) let
    a class restrict who may extend it, on top of — not instead of —
    single inheritance; `record` types (Java 16) can neither extend nor be
    extended.

---

**Next:** Video 053 — Inheritance HAS-A relationship
