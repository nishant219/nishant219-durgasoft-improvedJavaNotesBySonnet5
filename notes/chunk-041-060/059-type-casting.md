# Video 059 — Type casting

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-9||type casting

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 59 of 203 |
| Series | OOPs · Part 9 |
| Topic | type casting |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 41m 29s |
| Video ID | CrVLBpKIe0E |
| Watch | https://www.youtube.com/watch?v=CrVLBpKIe0E |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Video 058 already worked through type casting's **syntax and three rules**:
two checks done by the compiler, one check done by the JVM. This session is
the **internal picture** — what a cast actually does to the object sitting on
the heap — followed by four exam-style boards built on top of it:

1. Internal meaning of a cast: no new object, just another typed reference
2. `String` → `Object`, then `Integer` → `Number` → `Object` — still **one** heap object
3. Multilevel upcast `C` → `(B)` → `(A)`: the compile-time type changes, the runtime object never does
4. A parent reference holding a child object: which method calls through it are legal
5. The same three-level cast, tried three ways — overriding, static hiding, and field access resolve completely differently

---

### 00:06 — Recap: three type-casting rules from last session

Sir points back at video 058: related to type casting there are **just three
rules** — **two checked by the compiler**, **one checked by the JVM**. Those
rules decide, syntactically, which casts are valid. He recaps the only three
possible outcomes:

1. Compile-time error — **inconvertible types**
2. Compile-time error — **incompatible types**
3. Runtime exception — **`ClassCastException`**

He does not re-derive last session's examples here; this video assumes those
boards and moves straight to internals: **through a cast, what are we actually
doing?**

### 01:00 — Internal meaning: a cast does not create a new object

"Listen very carefully." One `String` object, cast to `Object`:

```java
class StringCastDemo {
    public static void main(String[] args) {
        String s = new String("Durga");
        Object o = (Object) s;
        // heap: one String object, "Durga"
        //   s ──┐
        //       ├──▶ String("Durga")
        //   o ──┘   (o is typed Object, same object)
        System.out.println(s == o);   // true
    }
}
```

Walking the three rules on `Object o = (Object) s`:

- `String` and `Object` are **parent–child** → check one passes.
- The cast target is `Object`; destination type is `Object` → **same type**, check two passes.
- The runtime object behind `s` is a `String`, and `String` is a **child class of `Object`** → the JVM accepts it. **Valid type casting.**

Then the question he presses on: *because of this cast, did a new object get
created?* Students answer yes — "I'm performing type casting, man." Sir: **no.**
Strictly speaking, a cast creates **no new object**. It only supplies **another
typed reference to the existing object**. One object, two reference variables
(`s` and `o`) — `s == o` printing `true` is the proof.

### 03:01 — Type casting, not object casting

That is why the topic is **type casting** (type conversion), never **object
casting**. The object never changes — it is always the same `String`; only the
reference's declared type changes. Board line, dictated slowly for notes:

> *Strictly speaking, through type casting we are not creating any new object.
> For the existing object we are providing another type of reference variable.
> That is we are performing* ***type casting***, *but not* ***object casting***.

### 04:15 — Combined into one line

The two lines collapse into one, equivalently:

```java
class CombinedUpcast {
    public static void main(String[] args) {
        Object o = new String("Durga");
        // compile-time type of o: Object
        // runtime object: String
    }
}
```

Reference type: `Object`. Object underneath: `String`. Through the cast we
created a new **reference variable**, never a new **object** — that
distinction is the whole lesson.

### 06:41 — Board copy: same example, under the heap diagram

He re-copies the identical example onto the board (~06:41–08:00) so the theory
sits directly under a heap diagram — same code as above, one `String` object,
two references. "Through type casting we are not creating any new object; for
the existing object we are trying to provide another type of reference
variable. This is what you people should be aware of."

### 08:02 — Example 2: `Integer` → `Number` → `Object`

"Take very very special care." A second example, chained two casts deep:

```java
class Example2 {
    public static void main(String[] args) {
        Integer i = new Integer(10);
        Number n = (Number) i;
        Object o = (Object) n;
    }
}
```

> ⚠️ **Modern Java — `new Integer(10)` is deprecated.**
> Since **Java 9** (JDK-8145468) the boxed-type constructors (`new Integer(...)`,
> `new Long(...)`, `new Boolean(...)`, etc.) are deprecated — `javac` warns:
> `Integer(int) in Integer has been deprecated`. They were never needed: the
> JVM already caches `Integer` values from -128 to 127, so `new Integer(10)`
> wastefully allocates a duplicate object every call. Write `Integer i = 10;`
> (autoboxing) or `Integer.valueOf(10)` instead. Sir's `new Integer(10)` is
> still legal and still compiles today — it is just legacy style now, kept
> here because it is what makes the *next* line's cast worth walking through.

Is `(Number) i` valid? Check all three rules:

- `Integer` and `Number` are **parent–child** (`Integer extends Number`).
- Destination `Number` vs `Number` — same type.
- Runtime object of `i` is `Integer`, a **child of `Number`**. **Valid.**

Then `Object o = (Object) n`:

- `n` is typed `Number`; `Number` and `Object` are parent–child.
- Destination `Object` vs `Object` — same type.
- `n` points at the same `Integer` object as `i`, so the runtime object is
  **`Integer`**, a child of `Object`. **Valid.**

### 10:03 — Still one object; three reference variables

`Integer i = new Integer(10)` creates the object. `Number n = (Number) i` — a
**new object** or a **new reference variable**? New **reference variable**;
`n` is another arrow to the same heap object. `Object o = (Object) n` — again
a new reference, not a new object.

**Total objects created: one. Reference variables: three** (`i`, `n`, `o` —
typed `Integer`, `Number`, `Object`).

### 11:09 — `==` proves it, then the combined lines

Cross-check with `==`:

```java
class Example2SameObject {
    public static void main(String[] args) {
        Integer i = new Integer(10);
        Number n = (Number) i;
        Object o = (Object) n;

        System.out.println(i == n);   // true
        System.out.println(n == o);   // true
    }
}
```

Both pairs point at the same object, so both print `true`. The first two
lines combine into one:

```java
class CombinedNumberRef {
    public static void main(String[] args) {
        Number n = new Integer(10);
        // acceptable: Number reference, Integer runtime object
    }
}
```

And all three combine into one, reference `Object`, runtime object `Integer`:

```java
class CombinedObjectRef {
    public static void main(String[] args) {
        Object o = new Integer(10);
        // for the Integer object we provided an Object-type reference;
        // beyond that, nothing
    }
}
```

"These many lines you are doing — what is it, nothing but: for the `Integer`
object we are providing an `Object` type of reference variable. Beyond that,
nothing."

### 12:39 — Board copy: example 2 with the diagram

Copy pause (~12:39–14:33, including a music break) while students take down
the same example plus the heap diagram and the equivalent one-line forms. "Take
clearly, including the diagram also — diagram, equivalent lines. Based on this
type casting, internally what things are required — that part I will discuss
for you people."

### 14:35 — Exam setup: multilevel `A` ← `B` ← `C`

"Just another point. Observe a bit carefully." From here, **what possible
questions you people can expect for the exam** — three or four boards. "Don't
write, just listen." Classes `A`, `B`, `C`: **`B` is the child of `A`. `C` is
the child of `B`. `A` is the grandparent of `C`.** Multilevel inheritance.

```java
class A { }
class B extends A { }
class C extends B { }

class MultilevelCast {
    public static void main(String[] args) {
        C c = new C();
        // compile-time type of c: C
        // runtime object: C
    }
}
```

### 16:00 — Cast `C` to `B`, then that result to `A`

Cast `c` to `B`: is `C → B` acceptable? **Yes** — `B` is the parent, `C` the
child; a **child object cast to a parent type is never a problem**. After
`(B) c`, the compile-time type is `B`, but the internal runtime object is still
**`C`**.

Cast that whole thing again, to `A`:

```java
class MultilevelCast2 {
    public static void main(String[] args) {
        C c = new C();

        B mid = (B) c;
        // compile-time type: B
        // runtime object: still C

        A top = (A) ((B) c);
        // compile-time type: A
        // runtime object: still C
    }
}
```

At the end the compile-time type is `A`; the runtime object is still `C`.
Both intermediate casts collapse into direct assignments — a **parent
reference can always be initialised straight from a child object**, no
explicit cast syntax needed:

```java
class ParentRefChildObj {
    public static void main(String[] args) {
        B b = new C();   // equivalent of (B) c — B type, C object underneath
        A a = new C();   // equivalent of (A)((B) c) — A type, C object underneath
    }
}
```

"I hope now you have this clarity, because I will use this concept in the
next example. That's why better to take note." (Copy pause to ~19:22.)

### 18:22 — The principle, in one line

Under the diagram: **parent reference can be used to hold child object.**
That single principle is all type casting between related classes ever is.

### 19:38 — Exam example 1: `Parent.m1` / `Child.m2` — which calls are valid?

"Now multiple examples I will talk — possible questions for the exam."
`Parent` declares `m1`; `Child` extends it and adds `m2`. A `Child` reference
therefore has **two** methods available: its own `m2`, plus `m1` inherited
from `Parent`.

```java
class Parent {
    public void m1() { System.out.println("m1"); }
}

class Child extends Parent {
    public void m2() { System.out.println("m2"); }
}

class ExamMethodCalls {
    public static void main(String[] args) {
        Child c = new Child();
        c.m1();            // valid
        c.m2();             // valid
        ((Parent) c).m1();  // valid
        // ((Parent) c).m2(); // CE: cannot find symbol: method m2()
    }
}
```

`c.m1()` — perfectly valid. `c.m2()` — valid too: **on a child reference you
can call both parent and child class methods**, no restriction. `((Parent)
c).m1()` — valid, same reasoning as the cast section above.

### 21:12 — Why `((Parent) c).m2()` fails

Because of the cast, internally: **parent reference can be used to hold child
object.** Equivalent, without the cast syntax:

```java
class ExamMethodCallsEquivalent {
    public static void main(String[] args) {
        Parent p = new Child();
        p.m1(); // valid — parent reference, parent method
        // p.m2(); // CE: cannot find symbol: method m2()
    }
}
```

`p.m1()` is fine: a parent reference can hold a child object, and through that
reference you can call methods **present in the parent class**. The last call,
`m2` — a **child-specific** method — through a parent-typed reference, is
**100% invalid**. Same rule as inheritance already taught: **a parent
reference can hold a child object, but through that reference you cannot call
child-specific methods.**

Predicted exam wording: *"Consider the following code. Which of the following
method calls are valid?"* — first three valid, last one invalid; know the
reason, not just the answer.

### 24:25 — Theory to file under example 1

> **Parent reference can be used to hold child object, but by using that
> reference we can't call child-specific methods — we can call only the
> methods available in the parent class.**

### 26:01 — Exam example 2: overriding `m1` in `A` / `B` / `C` → `C C C`

"This example is also very very important." `A`, `B`, `C` each declare `m1`
with the same signature — **overriding**.

```java
class A {
    public void m1() { System.out.println("A"); }
}

class B extends A {
    public void m1() { System.out.println("B"); }
}

class C extends B {
    public void m1() { System.out.println("C"); }
}

class OverrideAfterCast {
    public static void main(String[] args) {
        C c = new C();
        c.m1();              // C
        ((B) c).m1();        // C
        ((A) ((B) c)).m1();  // C
    }
}
```

Case by case: `c.m1()` → **C** (reference, object and method all agree).
`((B) c).m1()` → **C**, not B: the reference is `B`-typed but the runtime
object is still `C`. `((A) ((B) c)).m1()` → **C** again, for the same reason
one level further out.

**It is overriding. In overriding, method resolution is always based on the
runtime object type** — never the reference type — so the runtime object
being `C` in all three lines makes the output **`C`, `C`, `C`** regardless of
how many casts sit in front of the call.

### 30:20 — Theory to file under example 2

> **It is overriding, and method resolution is always based on runtime object
> type.**

### 31:08 — Exam example 3: same shape, `static` → method hiding → `C B A`

Same classes, same method names — but this time **all three `m1` methods are
`static`.** Static methods are not overridden, they are **hidden**, and hidden
methods resolve at **compile time**, based on the **reference type**:

```java
class A {
    public static void m1() { System.out.println("A"); }
}

class B extends A {
    public static void m1() { System.out.println("B"); }
}

class C extends B {
    public static void m1() { System.out.println("C"); }
}

class HideAfterCast {
    public static void main(String[] args) {
        C c = new C();
        c.m1();              // C — reference type C
        ((B) c).m1();        // B — reference type B
        ((A) ((B) c)).m1();  // A — reference type A
    }
}
```

`c.m1()`: reference type `C` → **C**. `((B) c).m1()`: equivalent to `B b = new
C();` — parent reference, child object, but **method hiding resolves by
reference type**, not runtime object → **B**. `((A) ((B) c)).m1()`: reference
type is now `A` → **A**.

"Compulsory you have to take the complete example" — don't shorthand it as
"same as above but static"; the whole point is that identical call syntax
produces a **different** answer from the overriding version.

### 34:29 — Theory to file under example 3

> **It is method hiding, and method resolution is always based on reference
> type.**

### 35:30 — Exam example 4 (last): instance variables `x` → `999 888 777`

Last example. Same `A` / `B` / `C` shape, this time with a shadowed instance
field `x` in each — Sir picks memorable values, **777 / 888 / 999**:

```java
class A {
    int x = 777;
}

class B extends A {
    int x = 888;
}

class C extends B {
    int x = 999;
}

class VarAfterCast {
    public static void main(String[] args) {
        C c = new C();
        System.out.println(c.x);               // 999
        System.out.println(((B) c).x);         // 888
        System.out.println(((A) ((B) c)).x);   // 777
    }
}
```

### 37:32 — Why `999, 888, 777` — fields resolve by reference type, always

`c.x` → **999**, reference and object agree. `((B) c).x` → **888**, not 999:
the reference is `B`-typed even though the runtime object is `C`. Last session
already covered this: **variable (field) resolution is always based on
reference type, never on the runtime object** — fields are not polymorphic in
Java, unlike methods. `((A) ((B) c)).x` → **777**, `A`'s field, by the same
rule.

### 39:40 — Theory to file under example 4

> **Variable resolution is always based on reference type, but not based on
> runtime object.**

### 40:46 — Close of type casting

"There ends the concept of type casting and related possible bits." Type
casting should not be a problem once you have: what happens internally, which
rules the compiler checks, which the JVM checks, what compile-time errors
result if they fail, and when to expect the runtime `ClassCastException`.

---

## Exam and interview points

1. **A cast never creates a new object.** It only produces another **typed
   reference variable** for the object that already exists on the heap — this
   is *type* casting, never *object* casting.
2. **`String s = new String("Durga"); Object o = (Object) s;` leaves one heap
   object and two references** (`s`, `o`), and `s == o` is `true`. Chaining
   `Integer → Number → Object` is still one object and three references —
   `i == n` and `n == o` are both `true`.
3. **A parent reference can always hold a child object** (`A a = new C();` is
   legal without any cast syntax at all) — this is the same "upcast" rule from
   inheritance, restated as the internal mechanism behind every valid cast in
   this lecture.
4. **Through a parent-typed reference, only parent-class methods are callable**
   — `((Parent) c).childOnlyMethod()` is a compile error (`cannot find
   symbol`), even though the runtime object really does have that method.
5. **The same three-deep cast (`c`, `(B) c`, `(A)((B) c)`) resolves three
   different ways** depending on what's being accessed through it — memorise
   all three, they are the classic OCJP trap:
   - **Overriding (instance methods):** resolved by **runtime object type** → `C C C`.
   - **Method hiding (`static` methods):** resolved by **reference type** → `C B A`.
   - **Field access (instance variables):** resolved by **reference type**, never runtime object → `999 888 777`.
6. **None of rules 1–5 have changed in any Java release** — casting mechanics,
   overriding's dynamic dispatch, static hiding, and field shadowing are all
   exactly as Sir describes them in current Java (25). The only thing that has
   dated is the constructor call used to build the demo objects — see the
   `new Integer(10)` callout above.

---

**Next:** Video 060 — Static control flow
