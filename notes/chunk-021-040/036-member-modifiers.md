# Video 036 — Member-level modifiers (and `strictfp`)

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-7||  MemberLevel Modifiers

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 36 of 203 |
| Series | Declarations and Access Modifiers · Part 7 |
| Topic | Class-level `strictfp` wrap-up, then member (method / variable) access: public, default, private, protected |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 25m 35s |
| Watch | https://www.youtube.com/watch?v=hzJPP0SvKro |
| Playlist | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Recap of the class-level modifiers already done: `public`, default, `final`, `abstract`.
2. The last class-level modifier: `strictfp` (Java 1.2) — legal on classes and methods, **not** variables.
3. Why `strictfp` exists: `10.0 / 3` used to print a different number of digits on different CPUs.
4. `strictfp` method → every floating-point calculation in that method follows IEEE 754.
5. `strictfp` class → every floating-point calculation in every **concrete** method follows IEEE 754.
6. `abstract` + `strictfp`: **illegal for methods**, **legal for classes** — he compiles both to prove it.
7. Member modifiers = method **or** variable level modifiers.
8. `public` members: accessible anywhere, **but** the enclosing class must itself be visible first (`pack1.A` vs `pack2.B`).
9. Default members: current package only (package-level access).
10. `private` members: same class only; `private` + `abstract` is illegal for methods.
11. `protected` — "the most misunderstood modifier in Java": same-package demo, then cross-package `pack2` demo, then the `D extends C extends A` demo.
12. Visibility summary table, plus the recommended modifiers (private data, public methods).

---

## 00:04 — Recap, then `strictfp`

Class-level modifiers already covered: public classes, default classes, `final`, `abstract`. The next one is **`strictfp`** — **strict floating-point**, added in **Java 1.2** (not there from 1.0).

`strictfp` is legal on **classes** and **methods**, same as `abstract` — and, same as `abstract`, illegal on a **variable**:

```java
strictfp class Test {
}

class Demo {
    strictfp void m1() {
        System.out.println(10.0 / 3);
    }

    // strictfp int x;   // CE: modifier strictfp not allowed here
}
```

## 02:00 — Need for `strictfp` — `10.0 / 3` is platform dependent

The board example:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10.0 / 3);
        // mathematically: 3.333... forever
        // Sir's classroom picture: a 16-bit CPU might print five or six 3s (3.33333),
        // a 32-bit CPU 14-15 decimal places — floating-point arithmetic used to vary
        // from platform to platform on 1990s hardware.
    }
}
```

Java is meant to be platform-independent, so if you do not want platform-dependent floating-point results, declare `strictfp`.

> **Board:** Usually the result of floating-point arithmetic is varied from platform
> to platform. If we want platform-independent results for floating-point
> arithmetic, then we should go for the `strictfp` modifier.

## 07:00 — `strictfp` method

```java
class Test {
    public strictfp void m1() {
        System.out.println(10.0 / 3);   // prints 3.3333333333333335
    }
}
```

If a method is declared `strictfp`, all floating-point calculations in that method have to follow the **IEEE 754** standard, giving platform-independent results. Sir's classroom picture for IEEE 754: "whether the CPU is 16-bit, 32-bit, or 64-bit, consider only four digits after the decimal point." The exact rule set is out of scope for the Java-programmer exam — internally, `strictfp` is implemented based on IEEE 754.

> ❗ **Correction — `strictfp` is not "only keep four digits after the decimal."**
> That classroom picture is a simplification, and taken literally it is wrong: a
> `strictfp` `double` still carries its normal ~15–17 significant decimal digits
> (`10.0 / 3` prints `3.3333333333333335`, all of it, `strictfp` or not). What
> `strictfp` actually pins down is the **exponent range and precision of every
> intermediate float/double value** to the IEEE 754 single/double formats — it
> stops the JIT from using the extended 80-bit x87 floating-point registers some
> older CPUs offered for intermediate results, which is what actually caused
> answers to drift between platforms. Digit count was never the mechanism.

## 10:33 — `abstract` + `strictfp` is illegal for **methods**

`strictfp` always talks about **implementation** — the calculations inside the method body. `abstract` never talks about implementation — there is no body. Contradiction → illegal combination for methods:

```java
abstract class Test {
    abstract strictfp void m1();
    // CE: illegal combination of modifiers: abstract and strictfp
}
```

Verified against `javac`: this is still exactly the error message today.

## 12:45 — `strictfp` class

Picture a class with concrete methods `m1`, `m2`, `m3`, … `m100`, and abstract methods `mx`, `my`, `mz`. Two ways to get IEEE 754 on every concrete method:

1. Declare **every concrete method** `strictfp`, or
2. Declare the **class** `strictfp` — simpler.

If a class is declared `strictfp`, every floating-point calculation in every **concrete** method has to follow IEEE 754:

```java
strictfp class Test {
    public void m1() {
        System.out.println(10.0 / 3);   // automatically strictfp
    }

    public void m2() {
        double d = 22.0 / 7;
        System.out.println(d);          // prints 3.142857142857143
    }
}
```

## 15:10 — `abstract` + `strictfp` is **legal for classes**

`strictfp` talks about **concrete** methods; `abstract` talks about **abstract** methods. No contradiction at class level. If the class has at least one abstract method, the class itself must be declared `abstract` — you can still mark it `strictfp` for the concrete methods:

```java
abstract strictfp class Test {
    public void m1() {
        System.out.println(10.0 / 3);   // concrete — covered by strictfp
    }

    public abstract void mx();          // abstract — covered by abstract
}
```

> **Board:** The `abstract strictfp` combination is legal for **classes**; it is
> legal for classes but illegal for methods.

## 19:25 — He compiles both, side by side

```java
abstract strictfp class Test {
    // valid — javac Test.java compiles clean
}
```

```java
class MethodCombo {
    abstract strictfp void m1();
    // CE: illegal combination of modifiers: abstract and strictfp
}
```

Contrast: **`final` + `abstract` is illegal at both class level and method level** (covered in the previous two videos). `abstract` + `strictfp` is illegal only at method level.

These five are the class-level modifiers as Sir counts them here: **public, default, final, abstract, `strictfp`**.

> ⚠️ **Modern Java — `strictfp` is now a no-op, and the class-modifier list has grown.**
>
> Since **Java 17** (JEP 306), *every* floating-point expression is evaluated
> strictly by default — the platform drift `strictfp` was built to fix stopped
> happening everywhere, on every JVM, without the keyword. `strictfp` still
> parses and still compiles, but changes nothing:
>
> ```text
> warning: [strictfp] as of release 17, all floating-point expressions are
> evaluated strictly and 'strictfp' is not required
> ```
>
> Verified: `javac -Xlint:strictfp` on a `strictfp class` prints exactly that
> warning under Java 17+, and `10.0 / 3` prints the same `3.3333333333333335`
> with or without the modifier. It was worth marks in the OCJP era; today
> writing it is dead code, kept only for source compatibility.
>
> Separately, **Java 17** also added two *new* class-level modifiers this
> lecture's "five" list never anticipated: **`sealed`** and **`non-sealed`**,
> which restrict which classes may extend a type (JEP 409):
>
> ```java
> sealed class Shape permits Circle, Square { }
> final class Circle extends Shape { }
> non-sealed class Square extends Shape { }   // reopens Shape for further subclassing
> ```
> Confirmed: this compiles under `--release 17` and fails under `--release 16`
> with "sealed classes are not supported in -source 16". So the current, complete
> list of class-level modifiers is **public, default, final, abstract, `strictfp`,
> `sealed`, `non-sealed`** — seven, not five.

---

## 23:11 — Member modifiers = method or variable level

Member means **method or variable**. Member modifiers are method-level or variable-level modifiers:

```java
class MemberMeans {
    int x;        // variable = member
    void m1() {    // method = member
    }
}
```

## 24:19 — Public members

If a member is declared `public`, it can be accessed from **anywhere** — inside the package or outside it — same story as a public class:

```java
package pack1;

public class A {
    public void m1() {
        System.out.println("A class public method");
    }
}
```

**Twist:** don't get too happy yet. Even if the **member** is public, class visibility is checked first. A public method in a non-public class is useless from outside the package.

### 25:40 — `pack1.A` is **not** public; `pack2.B` tries `a.m1()`

`A.java`:

```java
package pack1;

class A {
    public void m1() {
        System.out.println("A class method");
        // method is public; class A itself is default (not public)
    }
}
```

`B.java`:

```java
package pack2;

import pack1.A;
// CE at the import: A is not public in pack1; cannot be accessed from outside package

class B {
    public static void main(String[] args) {
        A a = new A();
        a.m1();
    }
}
```

Compiled and confirmed: `javac -d . A.java` succeeds; `javac -d . B.java` fails, because the import itself cannot see a package-private class from another package. Board takeaways:

- If a member is public, we can access it from anywhere — **but the corresponding class must be visible first.**
- Before checking **member** visibility, check **class** visibility.
- Even though `m1` is public, `B` cannot reach it, because class `A` is not public.
- **Only when both the class and the method are public** can the method be reached from outside the package.

Fixed version (both public):

```java
package pack1;

public class A {
    public void m1() {
        System.out.println("A class method");
    }
}
```

```java
package pack2;

import pack1.A;

class B {
    public static void main(String[] args) {
        A a = new A();
        a.m1();
        // prints: A class method
    }
}
```

Verified: this pair compiles and runs, printing `A class method`.

## 34:00 — Default members

Declare nothing, and it is **default**. A default member (variable or method) can be accessed **only within the current package** — hence default access is also called **package-level access**.

Flip the previous twist: **class public, method default**.

```java
package pack1;

public class A {
    void m1() {
        System.out.println("A class default method");
    }
}
```

```java
package pack2;

import pack1.A;

class B {
    public static void main(String[] args) {
        A a = new A();
        a.m1();
        // CE: m1() is not public in A; cannot be accessed from outside package
    }
}
```

```java
package pack1;

class SamePackage {
    public static void main(String[] args) {
        A a = new A();
        a.m1();
        // prints: A class default method  (same package — OK)
    }
}
```

Compiled and confirmed both outcomes: `pack2.B` fails to compile with the message above; `pack1.SamePackage` runs and prints `A class default method`.

## 36:41 — Private members

If a member is private, it can be accessed **only within the class** — not from outside it:

```java
class A {
    private void m1() {
        System.out.println("private m1");
    }

    public void m2() {
        m1(); // same class — OK
    }

    public static void main(String[] args) {
        A a = new A();
        a.m1();   // prints: private m1
        a.m2();   // prints: private m1
    }
}
```

```java
class B {
    public static void main(String[] args) {
        A a = new A();
        a.m1(); // CE: m1() has private access in A
    }
}
```

Verified with `javac`/`java`: the single-class version compiles and prints `private m1` twice; a second top-level class calling `a.m1()` fails with `m1() has private access in A`.

### 38:04 — `private` + `abstract` is illegal for methods

Already established: `final` + `abstract` and `strictfp` + `abstract` are illegal for methods. **`private` + `abstract` is also illegal**, and the reason is different: an abstract method has to be implemented in a **child** class, so it must be *available* to child classes. A `private` method is never available outside its own class — contradiction.

```java
abstract class P {
    abstract void m1();     // must be reachable from a child to implement
}

class Child extends P {
    public void m1() {
        System.out.println("child implements m1");
    }
}
```

```java
abstract class P {
    private abstract void m1();
    // CE: illegal combination of modifiers: abstract and private
}
```

```java
abstract class P {
    private void m1() {
        System.out.println("private concrete");
        // private + a body is fine — this is not abstract
    }
}
```

Verified: `javac` rejects `private abstract void m1();` with exactly that message.

## 41:44 — Protected members — "the most misunderstood modifier"

If a member is `protected`:

- **Within the current package: anywhere** (child class or not).
- **Outside the package: only in child classes**, and — as the twist below shows — only through a *child-typed reference*.

Sir's slogan:

**`protected` = default + kids** (kids = child classes)

### 45:28 — Same package: parent reference or child reference — all valid

`A` is public (so the file must be `A.java`); `main` lives in class `B`, in the same file:

```java
package pack1;

public class A {
    protected void m1() {
        System.out.println("the most misunderstood modifier");
    }
}

class B extends A {
    public static void main(String[] args) {
        A a = new A();
        a.m1();              // parent ref, parent object — valid

        B b = new B();
        b.m1();              // child ref, child object — valid (inherited)

        A a1 = new B();
        a1.m1();             // parent ref holding child object — valid
    }
}
```

Compiled and run: `javac -d . A.java` then `java pack1.B` prints `the most misunderstood modifier` **three times**. Within the current package, a protected member is reachable through a parent reference or a child reference — no restriction either way.

### 51:04 — Outside package `pack2.C` — only **child reference** is valid

```java
package pack2;

import pack1.A;

class C extends A {
    public static void main(String[] args) {
        A a = new A();
        a.m1();              // 1 — CE

        C c = new C();
        c.m1();              // 2 — valid

        A a1 = new C();
        a1.m1();             // 3 — CE
    }
}
```

Classroom guesses drifted ("two valid one invalid", then "one valid two invalid") before landing on the right answer: **only line 2 is valid.** Lines 1 and 3 both use a **parent-typed** reference (`a` and `a1` are both type `A`); line 2 uses a **child-typed** reference (`c` is type `C`) — that is the whole difference.

Rule as Sir states it:

- Within the current package, a protected member is reachable through a parent or child reference.
- Outside the package, a protected member is reachable **only from a child class**, and only through a **child reference**.
- A parent reference cannot be used to reach a protected member from outside the package.

```java
package pack2;

import pack1.A;

class C extends A {
    public static void main(String[] args) {
        // A a = new A();
        // a.m1();           // CE: m1() has protected access in A

        C c = new C();
        c.m1();
        // prints: the most misunderstood modifier

        // A a1 = new C();
        // a1.m1();          // CE: m1() has protected access in A
    }
}
```

Verified with `javac`: the commented-out lines fail with `m1() has protected access in A` (the modern message drops the fully-qualified `pack1.` prefix Sir's era printed, but the rule is identical); the `c.m1()` line compiles and prints the board line.

### 1:04:05 — More dangerous twist — `D extends C` (six cases, only one valid)

Hierarchy: `A` (pack1) ← `C` (pack2) ← `D` (pack2). `main` lives in **`D`**:

```java
package pack2;

import pack1.A;

class C extends A {
}

class D extends C {
    public static void main(String[] args) {
        A a = new A();
        a.m1();              // 1 — CE

        C c = new C();
        c.m1();              // 2 — CE (classroom guessed valid)

        D d = new D();
        d.m1();              // 3 — the ONLY valid line

        A a1 = new C();
        a1.m1();             // 4 — CE

        A a2 = new D();
        a2.m1();             // 5 — CE

        C c1 = new D();
        c1.m1();             // 6 — CE (classroom guessed valid)
    }
}
```

Compiled and confirmed with `javac`: lines 1, 2, 4, 5, and 6 all fail with `m1() has protected access in A`; only line 3 compiles. The tighter rule:

- From outside the package, a protected member is reachable **only from a child class**.
- And only through **that specific child class's own reference type** — accessing from `D` requires a `D` reference, accessing from `C` requires a `C` reference. A `C`-typed reference standing inside `D` (line 6) still doesn't qualify, and neither does a `C` object accessed from within `C` itself (line 2) once you're outside the declaring package.

That is why Sir calls it the **most misunderstood** modifier: same-package rules and outside-package rules genuinely differ, and the outside-package rule is stricter than "any subclass, any reference" — it demands the exact reference type of the class you are standing in.

---

## 1:14:22 — Summary table of `private` / default / `protected` / `public`

| Access from | `private` | default | `protected` | `public` |
|---|---|---|---|---|
| Within the same class | yes | yes | yes | yes |
| Child class, same package | no | yes | yes | yes |
| Non-child class, same package | no | yes | yes | yes |
| Child class, outside package | no | no | yes (child reference only) | yes |
| Non-child class, outside package | no | no | no | yes |

Tiny proofs matching the table:

```java
class SameClass {
    private int a = 1;
    int b = 2;
    protected int c = 3;
    public int d = 4;

    void show() {
        System.out.println(a + b + c + d);
        // prints 10 — all four are visible inside the declaring class
    }
}
```

```java
package pack1;

public class Parent {
    private void priv() { }
    void def() { }
    protected void prot() { }
    public void pub() { }
}

class ChildSamePack extends Parent {
    public static void main(String[] args) {
        Parent p = new Parent();
        // p.priv(); // CE: private access
        p.def();
        p.prot();
        p.pub();
    }
}

class NonChildSamePack {
    public static void main(String[] args) {
        Parent p = new Parent();
        // p.priv(); // CE
        p.def();     // same package, child or non-child — default is OK
        p.prot();
        p.pub();
    }
}
```

```java
package pack2;

import pack1.Parent;

class ChildOtherPack extends Parent {
    public static void main(String[] args) {
        Parent p = new Parent();
        ChildOtherPack c = new ChildOtherPack();
        // p.priv(); // CE
        // p.def();  // CE: not public; cannot be accessed from outside package
        // p.prot(); // CE: protected access — parent reference, outside package
        c.prot();    // OK — child reference only
        p.pub();     // public is always OK
        c.pub();
    }
}

class NonChildOtherPack {
    public static void main(String[] args) {
        Parent p = new Parent();
        // p.priv(); // CE
        // p.def();  // CE
        // p.prot(); // CE — not a child, outside package
        p.pub();     // only public is visible
    }
}
```

All four classes compiled cleanly together with `javac`, confirming every row of the table.

## 1:21:55 — Most restricted / most accessible / recommended modifiers

- The **most restricted** access modifier is **`private`**.
- The **most accessible** is **`public`**.
- Ranking, lesser to greater visibility: **`private` < default < `protected` < `public`**.

```java
class Ranking {
    private int mostRestricted;
    int packageLevel;
    protected int kidsPlusPackage;
    public int mostAccessible;
}
```

- **Recommended modifier for a data member (variable): `private`** — data hiding, one of the four pillars of OOP. (C's default for a struct/global is effectively private too; Java's *default* access exists, but `private` is still the recommended choice for data.)
- **Recommended modifier for methods: `public`** — a method is a service, and a service should be reachable by whoever needs it.

```java
class Recommended {
    private int salary;          // data member — private

    public int getSalary() {     // method / service — public
        return salary;
    }

    public void setSalary(int salary) {
        this.salary = salary;
    }
}
```

## 1:25:13 — Close

This video covers the **access** modifiers for members. The remaining member modifiers — `static`, `synchronized`, `native` — are a bigger discussion, coming up next.

> ⚠️ **Modern Java — private methods now exist on interfaces too (Java 9).**
> This lecture's "private is not available to child classes, so private + abstract
> is illegal" rule was written when only classes had private members. Since
> **Java 9** (JEP 213), an interface can declare **private** methods and
> **private static** methods as helpers for its own `default`/`static` methods:
>
> ```java
> interface Calc {
>     private int helper() { return 42; }   // Java 9+ — must have a body
>     default int compute() {
>         return helper();
>     }
> }
> ```
>
> Confirmed: this compiles under `--release 9` and fails under `--release 8`
> with "private interface methods are not supported in -source 8". The
> underlying rule from this lecture is unaffected — an interface private method
> must have a body (it can never be `abstract`), for exactly the reason Sir gives
> here: nothing private can be handed to an implementing/child type.

---

## Exam and interview points

1. **`strictfp` (Java 1.2)** applies to classes and methods, never variables — same restriction shape as `abstract`.
2. **`abstract strictfp` is legal on a class, illegal on a method.** `strictfp` talks about implementation (concrete methods); `abstract` never does — no contradiction at class level, direct contradiction at method level. Contrast with `final abstract`, illegal at *both* levels.
3. **Class-level modifiers taught in this lecture: five** — public, default, `final`, `abstract`, `strictfp`. The complete modern list is **seven**, adding `sealed` and `non-sealed` (Java 17).
4. **Member = method or variable.** Member modifiers are `public`, default, `private`, `protected` (access), plus `static`/`synchronized`/`native` (next videos).
5. **Class visibility gates member visibility.** A `public` method in a non-`public` class cannot be reached from outside the package — the class must be visible before the member's own modifier even matters.
6. **Default access = package-level access.** No modifier written = reachable only from the same package.
7. **`private` = same class only**, and **`private abstract` is illegal for methods** — an abstract method must be reachable by a child class to be implemented; a private method never is.
8. **`protected` = default + kids.** Same package: parent or child reference, no restriction. Outside the package: only a child class, and only through *that specific child class's own reference type* — not any ancestor-typed reference, and not even a same-package sibling class's typed reference used from within the deeper child.
9. **Visibility ranking:** `private` < default < `protected` < `public`. Recommended: `private` for data (data hiding), `public` for methods (a method is a service).
10. **`strictfp` is a no-op since Java 17** — still legal syntax, changes nothing; `javac -Xlint:strictfp` says so explicitly. Know the OCJP-era rules for the exam this course targets, and know they're now dead weight in real code.

---

**Next:** Video 037 — final variables
