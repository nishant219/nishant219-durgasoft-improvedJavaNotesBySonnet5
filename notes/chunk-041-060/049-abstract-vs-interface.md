# Video 049 — Abstract Class vs Interface

## Video info

**Title:** Java -  Interface and Abstract class Loopholes Part-6 || Abstract class Vs Interface

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 49 of 203 |
| Series | Interface and Abstract class Loopholes · Part 6 |
| Topic | Abstract class Vs Interface |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 19m 41s |
| Video ID | uNwIQ-mJPCI |
| Watch | https://www.youtube.com/watch?v=uNwIQ-mJPCI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is the loophole Sir listed back in Part 1 of this series: inside an
interface we can take only abstract methods, but inside an abstract class we
can *also* take only abstract methods, based on requirement — so both sides
can look identical. Then what is the actual need of an interface? Can you
just replace it with an abstract class and call it a day? The whole video is
one interview-style question answered two ways: a plain-language analogy,
then two concrete technical reasons.

---

## 00:27 — Two columns: only-abstract in both

Sir's framing: put interface on one side of the board, abstract class on the
other, and watch them collapse into the same shape. Inside interfaces we can
take only abstract methods (still the Java 1.7 rule for this comparison —
he flags the 1.8 changes later). But inside an abstract class, too, you can
choose to make every method abstract:

```java
interface X {
    void m1();
    void m2();
}
```

```java
abstract class X {
    abstract void m1();
    abstract void m2();
}
```

Both compile, both look the same on the page. **So what is the need of
interface?**

## 00:50 — Can we replace interface with abstract class?

The interview-style version of the question: *is it possible to replace the
interface concept with an abstract class, or not?* Up to Java 1.7, an
interface can hold only abstract methods (plus implicitly-`public static
final` constants). If an abstract class can be made to look exactly the
same, is the interface concept just redundant?

## 01:39 — Why did Java give two concepts, if they're interchangeable?

Sir's first-cut argument: if interface really could always be replaced by
abstract class, the language designers would have combined them into one
concept and been done with it. **Two concepts still exist — which already
tells you they are not the same thing**, even in the case where both happen
to contain nothing but abstract methods.

## 02:00 — The answer: yes, but not good practice

**Can you replace interface with abstract class? Yes.** Every interface that
holds only abstract methods can be rewritten as an abstract class with the
same abstract methods, and it will compile. **But it is not good
programming practice.** The rest of the video is why — first an analogy,
then the technical reasons.

## 02:29 — Analogy: the IAS officer hired to sweep

Durga Soft has 19 or 20 classrooms; they all need sweeping at day's end, or
the place turns horrible to sit in. So Sir places a newspaper ad: *Wanted —
sweepers.* Then he sets the eligibility bar absurdly high: must be an **IAS
officer** with **20+ years of government service**. Publish that and you'll
get a phone call from a startled officer within the hour — his actual "job
posting" was recruiting an IAS officer for a sweeping job.

Would the officer *sweep* if asked? Yes — nothing stops him physically. But
hiring him for it **misuses the role**: an officer's range covers big,
top-level responsibilities; pointing him at a low-level chore wastes what he
is for. Officer, before he became an officer, could sweep too — that was
never the question. The question is *role*.

**Mapped onto the two concepts:** interface is a low-level concept — it
never talks about implementation, only specification. Abstract class is a
richer concept — it *can* talk about implementation. Using an abstract class
where an interface would do is exactly the officer-sweeping mismatch: it
works, but it misuses the abstract class's role.

## 05:36 — Recap before the technical reasons

Can you replace interface with abstract class? **Yes.** Is it good practice?
**No.** The analogy sells the intuition; two concrete technical reasons back
it up.

## 06:02 — If everything is abstract: two options, one recommendation

When every method you need is abstract, you have exactly two legal shapes to
choose from — interface or abstract class — and **interface is the
recommended one.** Going for abstract class here is never recommended. Two
problems explain why.

## 06:48 — Problem 1: you keep the inheritance benefit with interface

While *implementing* an interface, a class is still free to *extend* some
other class — you lose nothing:

```java
class A {
}

interface X {
    void m1();
}

class Test extends A implements X {
    public void m1() {
    }

    public static void main(String[] args) {
        Test t = new Test();
    }
}
```

`class Test extends A implements X` compiles. Implementing an interface
never costs you your one shot at class inheritance.

## 07:36 — Abstract class: you cannot extend anything else

But if you choose abstract class instead, a class *extending* it cannot also
extend some other class — Java classes have single inheritance, full stop:

```java
abstract class X {
    abstract void m1();
}

class J {
}

class Test extends X, J {   // CE: '{' expected — a class may extend only one class
    public void m1() {
    }
}
```

**Problem 1, stated plainly:** implementing an interface costs you nothing
in the inheritance department; extending an abstract class spends your one
`extends` slot on it, and you lose the chance to extend anything else.

> ⚠️ **Modern Java — records make this problem sharper, not weaker.**
> A **record** (Java 16) can `implements` any number of interfaces but can
> **never `extends` anything** — not another class, not an abstract class,
> not even `Object` explicitly (the compiler already makes every record
> extend the special class `java.lang.Record`, and that slot is taken). So
> for a record, "use an abstract class instead of an interface" was never on
> the table to begin with — interfaces are the *only* way to attach shared
> abstract behaviour to a record type:
> ```java
> interface Greet { default String hi() { return "hi"; } }
> record Point(int x, int y) implements Greet { }
> // new Point(1, 2).hi() -> "hi" — works; Point could never have `extends`ed
> // an abstract class carrying the same default instead.
> ```
> This didn't exist in the Java 6/7 era Sir is teaching, but it is the modern,
> sharpest illustration of exactly the point he is making here.

## 08:20 — Problem 2: interface implementers are cheaper to construct

Second reason. Interface never contains an instance variable and never
contains a constructor — so when you create an object of a class that
merely `implements` an interface, there is no interface-side constructor or
instance block that has to run first:

```java
interface X {
    void m1();
}

class Test implements X {
    public void m1() {
    }

    public static void main(String[] args) {
        Test t = new Test();
        // no interface constructor, no interface instance block to run —
        // his teaching shorthand: "2 minutes" of construction cost
    }
}
```

## 09:32 — Extending abstract class: the parent's constructor and instance block both run

Create an object of a class that `extends` an abstract class instead, and
the parent's instance block and constructor run first, as part of building
that one object:

```java
abstract class X {
    {
        // parent instance block — runs for the child object
    }

    X() {
        // parent constructor — runs for the child object
    }

    abstract void m1();
}

class Test extends X {
    public void m1() {
    }

    public static void main(String[] args) {
        Test t = new Test();
        // parent instance block + parent constructor both execute —
        // his teaching shorthand: "20 minutes" of construction cost
    }
}
```

Sir is explicit that the "2 minutes" / "20 minutes" numbers are not a real
clock — just a way to say "cheaper" vs. "more expensive," not a benchmark
claim. Confirmed by compiling and running the equivalent: the parent
instance block and parent constructor genuinely do execute, in that order,
before `Test`'s own construction finishes.

## 09:59 — Recommendation from the two problems

1. Implementing an interface keeps your inheritance option open; extending
   an abstract class spends it — that's the abstract-class side's
   inheritance loss.
2. Implementing an interface is cheaper to construct; extending an abstract
   class runs extra parent-side machinery on every object you create.

**If everything is abstract, go for interface.** Reaching for an abstract
class in that situation is the IAS-officer-sweeping move again.

## 11:13 — The Java 1.8 doubt: default and static methods

The obvious follow-up: from Java 1.8, interfaces can hold `default` methods
and `static` methods — concrete, runnable code. Doesn't that make interface
and abstract class the same thing now?

**No.** A default method is still not equal to what an abstract class can
do. Sir's framing: abstract class is the "richer" of the two — it can carry
real state (instance variables) alongside real implementation. Interface
default methods, in his words, are still "dummy" methods relative to that:
they can run code, but they still have nothing to read except `static
final` constants and whatever the implementing class's own fields expose.

```java
interface X {
    default void m1() {
        // 1.8 — default methods run against the implementing object,
        // but still cannot read or write a per-object field of X itself
    }

    static void m2() {
    }

    void m3(); // interfaces can still declare plain abstract methods too
}
```

> ⚠️ **Modern Java — one more piece landed after default/static: private
> interface methods (Java 9).** An interface can now declare `private` (and
> `private static`) methods, used only to share code between its own
> default/static methods without exposing it as public API:
> ```java
> interface X2 {
>     private void helper() { System.out.println("shared logic"); }
>     default void m1() { helper(); }
>     default void m2() { helper(); }
> }
> ```
> This compiles and runs unchanged since Java 9. It still doesn't touch the
> core answer: interfaces have never been able to declare an instance
> variable or a constructor (see video 048), so however much behaviour piles
> up in default/static/private methods, an interface still cannot hold
> per-object state the way an abstract class can.
>
> Separately, **sealed types (Java 17)** give both interfaces and abstract
> classes a new, unrelated lever: `sealed interface X permits A, B` restricts
> who is allowed to implement `X` at all. That doesn't close the interface/
> abstract-class gap either — it's a third, independent axis (who may extend
> or implement this type), not a substitute for instance state.

## 12:10 — Board recap: the two-column comparison

Sir dictates this slowly for the notebook, boxing off just the two type
declarations and building the comparison underneath them:

| `interface X` | `abstract class X` |
|---|---|
| `void m1();` | `abstract void m1();` |

**Left column — implementing interface:**

```java
class A {
}

interface X {
    void m1();
}

class Test extends A implements X {   // valid
    public void m1() {
    }
}
```

While implementing interface, we can still extend some other class — **no
inheritance benefit lost.**

**Right column — extending abstract class:**

```java
abstract class X {
    abstract void m1();
}

class J {
}

class Test extends X, J {   // CE: '{' expected — a class may extend only one class
}
```

While extending abstract class, we cannot extend anything else —
**inheritance benefit lost.** First point: tick on the left, cross on the
right.

**Left column — object creation cost:**

```java
interface X {
    void m1();
}

class Test implements X {
    public void m1() {
    }
}

class Demo {
    public static void main(String[] args) {
        Test t = new Test();   // "2 minutes" — no interface ctor/instance block to run
    }
}
```

**Right column — object creation cost:**

```java
abstract class X {
    X() {
    }
    abstract void m1();
}

class Test extends X {
    public void m1() {
    }
}

class Demo {
    public static void main(String[] args) {
        Test t = new Test();   // "20 minutes" — parent ctor (+ instance block) run first
    }
}
```

Second point: object creation stays cheap on the interface side; it gets
more expensive on the abstract-class side, because the parent's constructor
and instance block have to run as part of building the child object.

## 19:01 — Close: don't misuse the role of abstract class

**If everything is abstract, it is highly recommended to go for interface,
not abstract class.** Reaching for abstract class there is misusing its
role — the same move as recruiting an IAS officer to sweep a room.

**Board recap, in Sir's own order:**

- If everything is abstract → highly recommended: interface, not abstract
  class.
- You *can* replace interface with abstract class, but it is not good
  programming practice (the IAS-officer-for-sweeping joke).
- Reason 1: implementing interface keeps the `extends` slot free; extending
  abstract class spends it. `Test extends A implements X` — tick. `Test
  extends X, J` — cross.
- Reason 2: `new Test()` after `implements X` is cheap (no interface
  constructor, no interface instance block); `new Test()` after `extends`
  an abstract `X` is costlier (parent constructor and instance block both
  run).
- Java 1.8 default/static methods do **not** make interface equal to
  abstract class. Abstract class remains the "richer" type — it alone can
  hold real per-object state.

---

## Exam and interview points

1. **You can always replace a pure-abstract interface with an equivalent
   abstract class** — it will compile. It is never good practice, because it
   misuses what an abstract class is for (Sir's IAS-officer-sweeping
   analogy).
2. **Reason 1 — inheritance benefit.** `implements` costs you nothing;
   `extends` on an abstract class spends your single class-inheritance slot.
   `class Test extends A implements X` compiles; `class Test extends X, J`
   does not (a class extends exactly one class).
3. **Reason 2 — construction cost.** An interface has no instance variables
   and no constructor, so implementing one adds no extra construction work.
   Extending an abstract class runs that class's instance block and
   constructor on every object you build.
4. **Java 8 default/static methods (and Java 9 private interface methods)
   add behaviour to interfaces, not state.** An interface still cannot
   declare an instance variable or a constructor — that boundary hasn't
   moved since Java 6/7 (see video 048 for the full constructor argument).
5. **Records (Java 16) make Reason 1 absolute, not just recommended:** a
   record can implement any number of interfaces but can never extend a
   class or abstract class at all, so for records the "just use an abstract
   class" escape hatch doesn't exist.
6. **Sealed interfaces (Java 17)** restrict *who* may implement a type — a
   separate, newer tool that answers a different question than "does this
   type hold state," and doesn't change the interface-vs-abstract-class
   comparison above.

---

**Next:** Video 050 — Interface, abstract class, constructor
