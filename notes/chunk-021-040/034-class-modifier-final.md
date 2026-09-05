# Video 034 — Class level modifiers: final

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-5 || Class Level Modifiers: final

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 34 of 203 |
| Series | Declarations and Access Modifiers · Part 5 of 14 |
| Topic | Class-level modifiers, with final as the first modifier he drills |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 12m 44s (4364 seconds) |
| Video ID | hNaCIwcUHi8 |
| Watch | https://www.youtube.com/watch?v=hNaCIwcUHi8 |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** YouTube captions are blocked on this upload, so
> there are no timestamps — sections instead follow Durga Sir's board order,
> covered below. Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. After source-file structure, import, and package: **class-level modifiers**
2. Which modifiers are legal on a **top-level (outer)** class vs an **inner** class
3. `public` class vs `<default>` (package-level) class, with `pack1` / `pack2`
4. Public class **file name must match** the class name
5. `private class`, `protected class`, `static class` at top level → **CE**
6. `final class A {}` — we can create objects, we **cannot extend**
7. API examples: `String`, `System`, `Integer` are `final`
8. Why Java made those classes final (security / immutability / SCP)
9. Advantage and disadvantage of a final class
10. Methods inside a final class cannot be overridden (no child class exists)

---

## Where this lecture sits in the syllabus

Declarations and Access Modifiers is the OCJP module after Language
Fundamentals, Operators, and Flow-Control.

Board order so far:

1. Java source file structure (package → import → class)
2. `import` and static import
3. `package` statement
4. **Now: modifiers we can write on the `class` declaration**

Durga's sentence: whenever we write a class, we can specify some modifiers.
Those modifiers are **class-level modifiers**.

## The only modifiers allowed on a top-level class

He writes this list and says **memorize it**. For an **outer / top-level**
class, only these five are legal:

```java
public class A {
}

class B {
}

final class C {
}

abstract class D {
}

strictfp class E {
}
```

`<default>` is not a keyword. If you write no access modifier, that **is**
default access.

```java
class DefaultAccessDemo {
    public static void main(String[] args) {
        System.out.println("no modifier = default / package-level class");
    }
}
```

`abstract` is the next video. `strictfp` he only lists here: "strict
floating-point" so `float` / `double` results are platform-independent.
Implementation talk is later. This video's modifier is **`final`**.

> ⚠️ **Modern Java — the legal list gained two members, and one on it went inert.**
> Since **Java 17** (JEP 409), a top-level class can also be `sealed` or
> `non-sealed`. `sealed` names its permitted direct subclasses and closes the
> door to anyone else — a controlled middle ground between "anyone can
> extend" (no modifier) and Sir's blunt `final` ("no one can extend"):
>
> ```java
> sealed class Shape permits Circle, Square { }
> final class Circle extends Shape { }
> non-sealed class Square extends Shape { }   // Square re-opens extension
> ```
>
> And `strictfp`, also since **Java 17** (JEP 306), is a no-op: all
> floating-point math is strict by default now, so the modifier still parses
> and still compiles but changes nothing. `javac -Xlint:strictfp` confirms it:
> `warning: [strictfp] as of release 17, all floating-point expressions are
> evaluated strictly and 'strictfp' is not required`.

### Inner classes get extra modifiers

For a **top-level** class, `private`, `protected`, and `static` are illegal.
For an **inner** class they are legal. He puts this on the board so you do
not mix the two lists.

```java
class Outer {
    public class PublicInner {
    }

    class DefaultInner {
    }

    private class PrivateInner {
    }

    protected class ProtectedInner {
    }

    static class StaticInner {
    }

    final class FinalInner {
    }

    abstract class AbstractInner {
    }

    strictfp class StrictInner {
    }
}
```

Exam trap: "Can a class be `private`?" Answer: **not a top-level class**. An
inner class can.

## `public` class — accessible from anywhere

If the class is `public`, any other class in any package can use it (after
`import`, or with a fully qualified name).

```java
package pack1;

public class A {
    public void m1() {
        System.out.println("A class method");
    }
}
```

Same package:

```java
package pack1;

class B {
    public static void main(String[] args) {
        A a = new A();
        a.m1();
        // prints A class method
    }
}
```

Other package — class `A` must be `public`, and we `import pack1.A` (or use
`pack1.A`):

```java
package pack2;

import pack1.A;

class C {
    public static void main(String[] args) {
        A a = new A();
        a.m1();
        // prints A class method
    }
}
```

Compile / run the way he does it:

```java
class CompilePublicClassDemo {
    public static void main(String[] args) {
        // javac -d . A.java
        // javac -d . B.java
        // javac -d . C.java
        // java pack1.B
        // java pack2.C
        System.out.println("public class A is visible from pack1 and pack2");
    }
}
```

## `<default>` class — same package only

If we remove `public` from class `A`, it becomes a **package-level** class.
Only classes in `pack1` can see it.

```java
package pack1;

class A {
    public void m1() {
        System.out.println("A class method");
    }
}
```

Same package still compiles:

```java
package pack1;

class B {
    public static void main(String[] args) {
        A a = new A();
        a.m1();
        // prints A class method
    }
}
```

Other package — **CE**, even if method `m1` is `public`. You cannot use a
type you cannot see.

```java
package pack2;

import pack1.A; // CE: pack1.A is not public; cannot be accessed from outside package

class C {
    public static void main(String[] args) {
        A a = new A(); // CE
        a.m1();
    }
}
```

Without the import, fully qualified name also fails:

```java
package pack2;

class C {
    public static void main(String[] args) {
        pack1.A a = new pack1.A(); // CE: pack1.A is not public
    }
}
```

Durga's line: **default = package-level access / package-private /
friendly.** Not a keyword. Do not write `default class A`.

```java
default class A { // CE: default is not a class modifier keyword here
}
```

## Public class file-name rule

If a class is `public`, the source file name **must** be `ThatClassName.java`.
Otherwise CE.

Legal — file `A.java`:

```java
public class A {
    public static void main(String[] args) {
        System.out.println("file A.java, public class A");
    }
}
```

Illegal — file `B.java` containing `public class A`:

```java
public class A { // CE: class A is public, should be declared in a file named A.java
}
```

A file can have **at most one** `public` class. Extra non-public classes in
the same file are allowed (source-file structure lecture).

```java
public class A {
}

class B {
}

class C {
}
```

If **no** class is public, the file name can be anything: `A.java`, `B.java`,
`Durga.java`.

```java
class A {
}

class B {
}
```

```java
class FileNameDemo {
    public static void main(String[] args) {
        // save the two default classes above as Durga.java — valid
        // javac Durga.java  → produces A.class and B.class
        System.out.println("no public class → any file name");
    }
}
```

Two public classes in one file — CE (already hammered in Part-1; he repeats
it):

```java
public class A {
}

public class B { // CE: class B is public, should be declared in a file named B.java
}
```

> ⚠️ **Modern Java — two features carve exceptions into this rule.**
> Sir's rule is still exactly right for `javac` compiling any `public class`.
> Two later additions loosen it for specific cases:
>
> 1. **Single-file source-launch (Java 11, JEP 330).** `java SomeFile.java`
>    compiles the file in memory and runs it directly, with **no filename
>    check at all** — it doesn't matter whether the file even contains a
>    public class. A file `Weird.java` holding `public class NotWeird` runs
>    fine via `java Weird.java`; run `javac Weird.java` on the exact same
>    file and you get the classic "should be declared in a file named
>    NotWeird.java" CE. The rule was always a `javac` rule, not a language
>    rule — this just exposed that.
> 2. **Implicit (unnamed) classes (Java 25, JEP 512, previewed since 21).**
>    A trivial program no longer needs a `class` declaration — public or
>    otherwise:
>    ```java
>    void main() {
>        System.out.println("no class keyword needed");
>    }
>    ```
>    The compiler wraps this in a synthetic unnamed class. There is nothing
>    named, so there is nothing for the filename rule to check against.

## `private`, `protected`, `static` at top level — CE

He writes it, compiles, shows the error. **Modifier private not allowed
here.**

```java
private class A { // CE: modifier private not allowed here
}
```

Same for `protected` and `static` on an outer class:

```java
protected class A { // CE: modifier protected not allowed here
}
```

```java
static class A { // CE: modifier static not allowed here
}
```

`static` on a class is only for **inner** classes (static nested class). Not
for top-level.

```java
class Outer {
    static class Nested {
        public static void main(String[] args) {
            System.out.println("static nested class is legal");
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        Outer.Nested n = new Outer.Nested();
        System.out.println("created static nested from outside");
    }
}
```

## What `final` means on a class

If a class is declared `final`, we **cannot extend** it. Parent–child is
impossible. Inheritance is closed.

```java
final class A {
}

class B extends A { // CE: cannot inherit from final A
}
```

We **can** create objects of a final class. Final does not mean "cannot
instantiate." It means "cannot be a parent."

```java
final class A {
    public void m1() {
        System.out.println("final class method");
    }
}

class Test {
    public static void main(String[] args) {
        A a = new A();
        a.m1();
        // prints final class method
    }
}
```

Empty final class is legal:

```java
final class A {
}
```

```java
class Test {
    public static void main(String[] args) {
        A a = new A();
        System.out.println(a);
        // prints A@hashcode  (Object.toString)
    }
}
```

> ⚠️ **Modern Java — records get `final` for free.**
> Since **Java 16**, `record Point(int x, int y) { }` declares an implicitly
> `final` class — you never type the keyword, the compiler adds it, and
> extending one is a CE exactly like extending Sir's `final class A`:
>
> ```java
> record Point(int x, int y) { }
> class Bad extends Point { } // CE: cannot inherit from final Point
> ```
>
> Same rule, just applied automatically instead of by hand.

## Why would we make a class final?

Durga's board: **security** and **guaranteed behaviour**.

If other people can extend our class and override methods, they can change
behaviour. For some classes (String, class-loader names, password-style
data) that is dangerous.

If the implementation is **complete** and we do not want a child to change
it, we mark the class `final`.

**Advantage:** security; method behaviour cannot be overridden.

**Disadvantage:** we cannot use inheritance, so we miss the main benefit of
OOP. Use `final` on a class only when we really mean "no child." (`sealed`,
introduced above, is the modern middle ground when "no one" is too strict but
"anyone" is too loose.)

## `String` is `final`

He writes `extends String` and compiles. CE.

```java
class MyString extends String { // CE: cannot inherit from final java.lang.String
}
```

We still **use** String every day. Using ≠ extending.

```java
class Test {
    public static void main(String[] args) {
        String s = new String("durga");
        System.out.println(s);
        // prints durga
        String s2 = "software";
        System.out.println(s2);
        // prints software
    }
}
```

`StringBuffer` and `StringBuilder` are also final:

```java
class MyBuffer extends StringBuffer { // CE: cannot inherit from final java.lang.StringBuffer
}
```

```java
class MyBuilder extends StringBuilder { // CE: cannot inherit from final java.lang.StringBuilder
}
```

```java
class Test {
    public static void main(String[] args) {
        StringBuffer sb = new StringBuffer("durga");
        System.out.println(sb);
        // prints durga
    }
}
```

Why String is final (he lists these; details come in `java.lang` String
videos):

1. **Immutability** — a child could add setters and break the immutability
   contract
2. **Security** — class names, network, class loading use String
3. **String constant pool / performance** — JVM can intern and cache hash
   codes safely only if no child can change the class

## `System` is `final`

```java
class MySystem extends System { // CE: cannot inherit from final java.lang.System
}
```

We use `System.out`, we do not extend `System`.

```java
class Test {
    public static void main(String[] args) {
        System.out.println("hello");
        // prints hello
    }
}
```

## `Integer` is `final` (all wrapper classes)

```java
class MyInteger extends Integer { // CE: cannot inherit from final java.lang.Integer
}
```

Same idea for the other wrappers:

```java
class MyByte extends Byte { // CE
}

class MyShort extends Short { // CE
}

class MyLong extends Long { // CE
}

class MyFloat extends Float { // CE
}

class MyDouble extends Double { // CE
}

class MyCharacter extends Character { // CE
}

class MyBoolean extends Boolean { // CE
}
```

We still create / use Integer objects:

```java
class Test {
    public static void main(String[] args) {
        Integer i = new Integer(10);   // deprecated since Java 9 — see below
        System.out.println(i);
        // prints 10
        Integer j = Integer.valueOf(20);
        System.out.println(j);
        // prints 20
    }
}
```

> ⚠️ **Modern Java — `new Integer(10)` is deprecated.**
> Since **Java 9**, the boxed-type constructors — `new Integer(...)`,
> `new Long(...)`, `new Boolean(...)`, all eight wrappers — are deprecated in
> favour of `valueOf(...)` or plain autoboxing. The constructor always
> allocates a new object; `valueOf` may return a cached instance (`Integer`
> caches −128..127 by default):
>
> ```java
> Integer i = Integer.valueOf(10);   // preferred — may reuse a cached instance
> Integer j = 10;                    // autoboxing — same effect
> Integer k = new Integer(10);       // still compiles, warns: [deprecation]
> ```
>
> The classes themselves are still `final`, for exactly the reason Sir gives —
> only the constructor call is out of favour.

## Final class vs final method (preview)

A **final class** cannot have a child, so **no method can be overridden**.
Every method is "final in effect."

```java
final class A {
    public void m1() {
        System.out.println("m1");
    }

    public void m2() {
        System.out.println("m2");
    }
}

class B extends A { // CE: cannot inherit from final A
    public void m1() { // never reached — class B itself is illegal
        System.out.println("override attempt");
    }
}
```

A **non-final** class can still mark **selected** methods `final`. Child can
extend, but cannot override those methods. That is a member-level topic; he
plants the seed here.

```java
class Parent {
    public final void m1() {
        System.out.println("this method cannot be overridden");
    }

    public void m2() {
        System.out.println("this method can be overridden");
    }
}

class Child extends Parent {
    public void m1() { // CE: m1() in Child cannot override m1() in Parent; overridden method is final
        System.out.println("no");
    }

    public void m2() {
        System.out.println("override ok");
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        Parent p = new Child();
        p.m2();
        // if m1 override is removed, prints: override ok
    }
}
```

## `final` + `abstract` on a class — illegal

`final` = cannot extend. `abstract` = must extend to complete the class.
Opposite ideas.

```java
final abstract class Test { // CE: illegal combination of modifiers: abstract and final
}
```

A final class cannot contain an abstract method (that method would need a
child implementation):

```java
final class Test {
    public abstract void m1(); // CE: Test is not abstract and does not override abstract method m1()
}
```

## `public` + `final` is legal

```java
public final class Test {
    public static void main(String[] args) {
        Test t = new Test();
        System.out.println("public final class is valid");
        // prints public final class is valid
    }
}
```

File must still be `Test.java` because the class is `public`.

```java
public final class A {
}
```

```java
class B extends A { // CE: cannot inherit from final A
}
```

## `final` + `strictfp` is legal

```java
final strictfp class Calc {
    public static void main(String[] args) {
        System.out.println(10.0 / 3);
    }
}
```

(`strictfp` itself is a no-op since Java 17 — see the callout earlier in this
note — but the combination still compiles cleanly.)

## Recap of legal / illegal outer-class declarations

```java
public class A {
}

class B {
}

final class C {
}

abstract class D {
}

strictfp class E {
}

public final class F {
}

public abstract class G {
}

public strictfp class H {
}

final strictfp class I {
}

abstract strictfp class J {
}

private class K { // CE: modifier private not allowed here
}

protected class L { // CE: modifier protected not allowed here
}

static class M { // CE: modifier static not allowed here
}

final abstract class N { // CE: illegal combination of modifiers: abstract and final
}

default class O { // CE: not this kind of default
}
```

## Code from the lecture

Full recap class for the `final class` story he compiles:

```java
final class Parent {
    public void m1() {
        System.out.println("Parent m1");
    }
}

class Child extends Parent { // CE: cannot inherit from final Parent
}

class Test {
    public static void main(String[] args) {
        Parent p = new Parent();
        p.m1();
        // prints Parent m1
        String s = "durga";
        System.out.println(s);
        // prints durga
        Integer i = new Integer(10);   // deprecated since Java 9
        System.out.println(i);
        // prints 10
        System.out.println("System is used, not extended");
        // prints System is used, not extended
    }
}
```

Public vs default recap:

```java
package pack1;

public class A {
    public void m1() {
        System.out.println("hello");
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
        // prints hello
    }
}
```

---

## Exam and interview points

1. **Only five modifiers are legal on a top-level class**: `public`,
   `<default>`, `final`, `abstract`, `strictfp`. `private`, `protected`, and
   `static` are legal only on an **inner** class.
2. **`<default>` is not a keyword.** Writing no access modifier on a class
   *is* default (package-private) access.
3. **`public` class → visible everywhere**; file name must equal the class
   name; at most one public class per file.
4. **Default class → visible only inside its own package**, even if every
   member on it is `public`.
5. **`private class A {}` at top level looks "more secure"; it is just a
   CE** (`modifier private not allowed here`) — same for `protected` and
   `static` on an outer class.
6. **`static class` is legal only as an inner (nested) class**, never at top
   level.
7. **`final class` → objects yes, `extends` no.** Final blocks inheritance,
   not instantiation.
8. **`String`, `StringBuffer`, `StringBuilder`, `System`, and every wrapper
   class (`Integer`, `Byte`, `Short`, `Long`, `Float`, `Double`, `Character`,
   `Boolean`) are `final`.** `class MyString extends String` is a favourite
   one-mark CE.
9. **Why final: security + guaranteed behaviour** (advantage); **loses
   inheritance** (disadvantage) — use it only when you mean "no child, ever."
10. **`final` + `abstract` on a class is always a CE** — opposite intents,
    cannot combine. `public final class` and `final strictfp class` are both
    legal.
11. **A final class's methods can never be overridden**, because no child
    class of it can exist. A non-final class can still mark individual
    methods `final` to block overriding on just those members.
12. **`default class A {}` is not Java** — `default` is a keyword only for
    default methods in interfaces (Java 8+) and default labels in
    switch/interfaces, never a class access modifier.
13. **Modern-Java addendum for interviews:** `sealed` / `non-sealed` (Java
    17) extend the top-level-modifier list with a controlled middle ground
    between `final` and open extension; `strictfp` has been a no-op since
    Java 17; records (Java 16) are implicitly final; and `new Integer(...)`
    has been deprecated since Java 9 in favour of `Integer.valueOf(...)` or
    autoboxing. Know Sir's OCJP-era answer *and* the current-Java answer, and
    know which one an interviewer is asking for.

---

**Next:** Video 035 — Class level modifiers: abstract
