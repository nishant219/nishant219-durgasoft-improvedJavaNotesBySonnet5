# Video 057 — Overriding, Var-Args, and Polymorphism

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-7||overriding ||varargs method

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 57 of 203 |
| Series | OOPs · Part 7 |
| Topic | overriding, varargs method |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 49m 12s |
| Video ID | SrveBABPMFc |
| Watch | https://www.youtube.com/watch?v=SrveBABPMFc |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Last session finished overriding with respect to static methods (mixing
static and non-static is a compile error; both static is method hiding,
output parent/child/parent). This session:

1. Overriding with respect to **var-arg methods** — a parent var-arg method
   next to a child *normal* method looks like overriding but is overloading
2. What actually makes a var-arg method override-compatible
3. Overriding with respect to **variables** — fields are never overridden,
   only hidden, across all four static/instance combinations
4. The **nine differences** between overloading and overriding, as an
   interview-ready table
5. An exam-style question: given one parent method, which of five candidate
   child methods are valid, and by which concept
6. **Polymorphism** — definition, and three examples (overloading,
   overriding, a parent reference holding a child object)
7. When to declare a parent-type reference instead of the exact child type —
   a three-row interview table
8. The **three pillars of OOPs**, and a static-vs-dynamic polymorphism summary
9. A popular internet "definition" of polymorphism, offered as folklore, not
   as something to test on

---

## 00:05 — Recap and the var-arg reminder

Last session covered overriding with respect to **static methods** — that
chapter is complete. This session: overriding with respect to **var-arg
methods**. Sir assumes the room already knows what a var-arg method is from
Language Fundamentals (video 012); he only gives a one-line reminder before
getting to the override rule.

Var-arg methods arrived as a **new concept in 1.5** — a method that accepts
any number of arguments of a type, including zero:

```java
class NormalOneInt {
    public void m1(int x) {
        System.out.println("exactly one int");
    }

    public static void main(String[] args) {
        NormalOneInt t = new NormalOneInt();
        t.m1(10);
        // t.m1();        // CE: method m1(int) not applicable — no argument
        // t.m1(10, 20);   // CE: method m1(int) not applicable — two arguments
    }
}
```

```java
class VarArgAnyCount {
    public void m1(int... x) {
        System.out.println("var-arg method");
    }

    public static void main(String[] args) {
        VarArgAnyCount t = new VarArgAnyCount();
        t.m1();
        t.m1(10);
        t.m1(10, 20);
        t.m1(10, 20, 30);
        // all four calls print: var-arg method
    }
}
```

`m1(int... x)` — that is the 1.5 concept. Now the override rule.

## 01:40 — The trap: parent var-arg, child normal, three reference/object pairs

Parent class `P` has a **var-arg** method. Child class `C extends P` has a
**normal** method of the same name:

```java
class P {
    public void m1(int... x) {
        System.out.println("parent");
    }
}

class C extends P {
    public void m1(int x) { // normal method, not var-arg
        System.out.println("child");
    }
}

class Test {
    public static void main(String[] args) {
        P p = new P();
        p.m1(10);       // Case 1 — parent reference, parent object

        C c = new C();
        c.m1(10);       // Case 2 — child reference, child object

        P p1 = new C();
        p1.m1(10);      // Case 3 — parent reference, child object
    }
}
```

**Case 1 — parent reference, parent object.** Parent reference, parent
object → parent method. Easy: `parent`.

**Case 2 — child reference, child object.** Child reference, child object →
child method. Easy: `child`.

**Case 3 — parent reference, child object.** The dangerous one — same
reference/object pattern as the `marry()` demo from video 055. Sir asks the
room; most people shout **child**, reasoning by the overriding reflex: *"in
overriding, method resolution is always taken care of by the JVM based on
runtime object; the runtime object of `p1` is a child object, so child
should execute."*

## 04:46 — The answer is parent, and the reason is that it isn't overriding

The answer is **parent**, not child. Sir stops the room: *"who told you this
is the overriding concept?"*

Overriding requires the method name **and argument types** to be the same.
Here the parent's argument is `int... x`; the child's is a plain `int x` —
same name, **different argument types**. Same name, different argument
types is the definition of **overloading**, not overriding:

```java
class P {
    public void m1(int... x) {
        System.out.println("parent");
    }
}

class C extends P {
    public void m1(int x) { // different argument type than int...
        System.out.println("child");
    }
}

class NotOverriding {
    public static void main(String[] args) {
        P p1 = new C();
        p1.m1(10);
        // prints parent — overloading, not overriding;
        // compiler binds using reference type P → P.m1(int...)
    }
}
```

**The rule:** a var-arg method can be overridden with **another var-arg
method only**. Try to "override" it with a normal method and it becomes
**overloading but not overriding** — resolved by the **compiler**, based on
**reference type**, exactly like any other overload:

| Call | Reference | Bound method |
|---|---|---|
| `p.m1(10)` | parent | parent (var-arg) |
| `c.m1(10)` | child | child (normal `int`) |
| `p1.m1(10)` | parent | parent (var-arg) |

If the child method is **also** var-arg, both methods now have the same
argument type, so it genuinely **is** overriding — and case 3 flips to
child, resolved by the **JVM** based on **runtime object**:

```java
class P {
    public void m1(int... x) {
        System.out.println("parent");
    }
}

class C extends P {
    public void m1(int... x) { // also var-arg → real override
        System.out.println("child");
    }
}

class BothVarArg {
    public static void main(String[] args) {
        P p = new P();
        p.m1(10);        // prints parent

        C c = new C();
        c.m1(10);        // prints child

        P p1 = new C();
        p1.m1(10);       // prints child — JVM, runtime object C
    }
}
```

> ❗ **Correction — "override with another var-arg method only" is stated a
> touch too narrowly.**
> The real requirement for overriding is an **identical parameter list after
> erasure**, not identical *syntax*. `int... x` erases to the array type
> `int[] x`, so a child method declared with a plain array parameter also
> overrides it — the compiler accepts `@Override`, and dispatch still
> happens at runtime through the parent reference:
> ```java
> class P {
>     public void m1(int... x) {
>         System.out.println("parent");
>     }
> }
>
> class C extends P {
>     @Override
>     public void m1(int[] x) { // no "...", still overrides — same erasure
>         System.out.println("child");
>     }
> }
>
> class ArrayParamOverride {
>     public static void main(String[] args) {
>         P p1 = new C();
>         p1.m1(10);
>         // prints child — the varargs call is resolved through P's
>         // varargs signature, then dispatched at runtime to C.m1(int[])
>     }
> }
> ```
> Sir's phrasing is the right OCJP answer for the 99% case where both sides
> write the "obvious" declaration. Just know the underlying test is
> *signature equality after erasure*, not "both declarations must use `...`".

## 08:21 — Live run confirms the output, then the flip

Sir types the first program (`P.m1(int...)`, `C.m1(int)` normal) into
`Test.java`, compiles, and runs it:

```java
javac Test.java
java Test
```

Predicted before running: parent, child, parent. Observed: **parent child
parent** — matches. He then asks: if the child method were **also** var-arg,
what changes? Parent, child, **child** — because now it is overriding, not
overloading. He confirms this live too.

## 11:45 — "We only passed one argument — is it still overloading?"

A student notes: if both methods were **normal** (`m1(int)` in both classes),
that genuinely is overriding — same argument type in both:

```java
class P {
    public void m1(int x) {
        System.out.println("parent");
    }
}

class C extends P {
    public void m1(int x) {
        System.out.println("child");
    }
}

class BothNormal {
    public static void main(String[] args) {
        P p1 = new C();
        p1.m1(10);
        // prints child — this IS overriding
    }
}
```

Follow-up: in the var-arg-vs-normal case, only **one** argument was ever
passed — does that make it overriding? No. Even though a single `int` is
passed, **overloading still dominates** because the *declared* argument
types differ (`int...` vs `int`). The reference type decides which method
gets the chance, regardless of what you happen to pass at the call site.

If the parent had **also** declared an exact-match normal `m1(int)`
alongside its var-arg version, *that* overload would win instead (var-arg is
the lowest-priority match — same rule as overload resolution in video 012):

```java
class P {
    public void m1(int... x) {
        System.out.println("parent var-arg");
    }

    public void m1(int x) {
        System.out.println("parent normal");
    }
}

class C extends P {
    public void m1(int x) { // overrides P.m1(int), not P.m1(int...)
        System.out.println("child");
    }
}

class ParentAlsoHasNormal {
    public static void main(String[] args) {
        P p1 = new C();
        p1.m1(10);
        // prints child — P.m1(int) is the exact-match overload chosen,
        // and C overrides that one, so runtime object C wins
    }
}
```

## 14:36 — Replace the child method with var-arg, and it becomes overriding

Taking the original program and swapping the child's normal method for a
var-arg one turns overloading into overriding. Output goes from
**parent child parent** to **parent child child**:

```java
class P {
    public void m1(int... x) {
        System.out.println("parent");
    }
}

class C extends P {
    public void m1(int... x) { // replaced the normal method with var-arg
        System.out.println("child");
    }
}

class Test {
    public static void main(String[] args) {
        P p = new P();
        p.m1(10);       // prints parent

        C c = new C();
        c.m1(10);       // prints child

        P p1 = new C();
        p1.m1(10);      // prints child — now overriding
    }
}
```

That is what to be aware of for overriding with respect to var-arg methods.

---

## 16:06 — Overriding with respect to variables

New heading: **overriding with respect to variables**. Sir sets it up with
strong, memorable values instead of `10` — parent field `888`, child field
`999`, same name:

```java
class P {
    int x = 888;
}

class C extends P {
    int x = 999;
}

class Test {
    public static void main(String[] args) {
        P p = new P();
        System.out.println(p.x);

        C c = new C();
        System.out.println(c.x);

        P p1 = new C();
        System.out.println(p1.x);
    }
}
```

## 18:38 — The trap: applying the method rule to a variable

- `p.x` — parent reference, parent object → **888**
- `c.x` — child reference, child object → **999**
- `p1.x` — parent reference, **child object**

The room applies the overriding reflex again: both are instance variables,
resolution is "based on runtime object," runtime object is child, so they
shout **999**. The actual answer is **888**.

## 19:40 — Overriding does not apply to variables at all

*"Who told you this is overriding?"* **Overriding is applicable only to
methods, never to variables.** If `x` were a method, resolution would indeed
follow the runtime object. Because it is a field, that rule never engages.

**Variable resolution is always handled by the compiler, based on reference
type** — full stop, regardless of whether the variable is instance or
static:

- parent reference → 888
- child reference → 999
- parent reference holding a child object → still **888**

## 20:34 — All four static/instance combinations give the same answer

Sir works through every combination of static/non-static on `P.x` and
`C.x`. The rule never changes — it is always compiler + reference type:

| Parent `x` | Child `x` | `p.x` | `c.x` | `p1.x` |
|---|---|---|---|---|
| instance | instance | 888 | 999 | 888 |
| static | instance | 888 | 999 | 888 |
| instance | static | 888 | 999 | 888 |
| static | static | 888 | 999 | 888 |

```java
class P {
    int x = 888;       // toggle static on P and/or C — the output never changes
}

class C extends P {
    int x = 999;
}

class Test {
    public static void main(String[] args) {
        P p = new P();
        System.out.println(p.x);
        C c = new C();
        System.out.println(c.x);
        P p1 = new C();
        System.out.println(p1.x);
        // prints 888, 999, 888 — in all four static/non-static combinations
    }
}
```

Sir runs all four combinations live and confirms **888 999 888** every
time. Make sure you are aware: **overriding concept applicable only for
methods but not for variables.** Overriding rules are now complete.

---

## 28:33 — Nine differences between overloading and overriding

*"What is the difference between overloading and overriding? Tell all the
differences"* — a very common, very important interview question. Sir goes
point by point, then dictates the whole table. The one-line summary at the
end matters as much as the table: **overloading checks only two things;
overriding checks everything.**

| Property | Overloading | Overriding |
|---|---|---|
| Method names | must be same | must be same |
| Argument types | must be different (at least order) | must be same, including order |
| Method signatures | must be different | must be same |
| Return types | no restrictions | must be same until 1.4; from 1.5 onward, covariant return types are also allowed |
| Private, static, final methods | can be overloaded | cannot be overridden |
| Access modifiers | no restrictions | scope cannot be reduced; it can be increased |
| Throws clause | no restrictions | if the child method throws a checked exception, the parent must throw the same checked exception or its parent — unchecked exceptions are unrestricted |
| Method resolution | always by the compiler, based on reference type | always by the JVM, based on runtime object |
| Also known as | compile-time polymorphism, static polymorphism, early binding | runtime polymorphism, dynamic polymorphism, late binding |

Code for the properties that are easy to lose in prose:

```java
// argument types — overloading needs at least a different order
class OverloadAtLeastOrder {
    public void m1(int i, float f) { System.out.println("int, float"); }
    public void m1(float f, int i) { System.out.println("float, int"); }
}

// return types — covariant since 1.5
class P { public Object m1() { return null; } }
class C extends P {
    public String m1() { return "child"; } // covariant return, valid
}

// private/static/final — overloaded freely, never overridden
class P2 {
    private void m1() { }
    static void m2() { }
    final void m3() { }
}
class C2 extends P2 {
    private void m1() { } // unrelated method — parent's private is not even visible here
    static void m2() { }  // method hiding, not overriding
    // final void m3() { } // CE: m3() in C2 cannot override m3() in P2; overridden method is final
}

// access modifiers — cannot reduce scope
class P3 { public void m1() { } }
class C3 extends P3 {
    // void m1() { } // CE: attempting to assign weaker access privileges; was public
    public void m1() { } // OK — same scope
}

// throws clause — child's checked exception must match or be narrower
import java.io.IOException;
import java.io.FileNotFoundException;
class P4 { public void m1() throws IOException { } }
class C4a extends P4 {
    public void m1() throws FileNotFoundException { } // OK — FileNotFoundException is-a IOException
}
class C4b extends P4 {
    // public void m1() throws Exception { }
    // CE: m1() in C4b cannot override m1() in P4;
    //     overridden method does not throw java.lang.Exception
}
```

Conclusion Sir wants in the notebook: **in overloading we only have to check
method names (same) and argument types (different)** — return type, access
modifier, and throws are free. **In overriding everything has to check
out** — names, arguments, return type, access modifier, throws: the
complete prototype of the method. Overloading is the simple process;
overriding is the complex one.

## 51:46 — Exam question: one parent method, five candidate overrides

Parent class:

```java
import java.io.IOException;

class P {
    public void m1(int x) throws IOException {
    }
}
```

In the child class, which of the following are valid, and by which concept?

```java
// 1
public void m1(int i)

// 2
public static int m1(long l)

// 3
public static void m1(int i)

// 4
public void m1(int i) throws Exception

// 5
public static abstract void m1(double d)
```

**Option 1 — `public void m1(int i)`.** Same name, same argument type →
overriding. The child throws nothing, which is allowed (a checked exception
can be dropped, never widened). **Valid, by overriding.**

**Option 2 — `public static int m1(long l)`.** The room's first instinct is
"invalid" — non-static to static, `void` to `int` — reasoning as if this
*were* overriding. It is not: the argument type is `long`, not `int`, so
names match but arguments differ — **overloading**. Once arguments differ,
return type, `static`, and access modifier are all free to vary. **Valid, by
overloading.**

**Option 3 — `public static void m1(int i)`.** Same name, same argument →
overriding. Overriding a non-static method with a static one is not
possible. **Invalid**, confirmed by `javac`:

```text
error: m1(int) in C cannot override m1(int) in P
  overriding method is static
```

**Option 4 — `public void m1(int i) throws Exception`.** Same name, same
argument → overriding. `Exception` is a **parent** of `IOException`, and
the rule runs the other way: the child may throw the same checked exception
or a subtype of it, never a supertype. **Invalid**:

```text
error: m1(int) in C cannot override m1(int) in P
  overridden method does not throw java.lang.Exception
```

**Option 5 — `public static abstract void m1(double d)`.** Different
argument type (`double`), so it looks like a clean overload and people mark
it valid. It is not: `static` and `abstract` is an **illegal combination of
modifiers** — you cannot declare a method both static and abstract, in any
class, overriding or not. **Invalid**, and the failure has nothing to do
with overloading or overriding:

```text
error: illegal combination of modifiers: abstract and static
```

---

## 1:01:37 — Polymorphism: definition and life example

Overloading and overriding are both, by default, considered **polymorphism**.
Greek: *poly* (many) + *morphs* (forms) → many forms. **One name, but
multiple forms, is the concept of polymorphism.**

Sir's analogy for it: you are innocent in front of your parents at home,
switch entirely to slang and opinions about cinema and brands with friends
outside, and pick up a whole new "colour" moving to a city from a village —
same person, different behaviour depending on where you are. Same name
(you), multiple forms (behaviour).

## 1:04:38 — Example 1: `abs` — overloading is polymorphism

One method name, `abs`, applied across `int`, `long`, and `float` — same
name, multiple forms of argument. This is **overloading**, and overloading
is an example of polymorphism:

```java
class AbsOverload {
    public int abs(int i) { return i < 0 ? -i : i; }
    public long abs(long l) { return l < 0 ? -l : l; }
    public float abs(float f) { return f < 0 ? -f : f; }
}
```

## 1:05:20 — Example 2: `marry()` — overriding is polymorphism

Same method signature, different implementation in parent vs. child (Sir's
running gag: the parent's arranged match vs. the child's own choice) — same
name, multiple forms of *behaviour*. This is **overriding**, also an
example of polymorphism:

```java
class P {
    public void marry() {
        System.out.println("Subbalakshmi"); // parent's implementation
    }
}

class C extends P {
    public void marry() {
        System.out.println("Charmi"); // child's own implementation
    }
}
```

## 1:10:51 — Example 3: a parent reference holding any child object

`List` is an interface in `java.util`, with several implementation classes.
The same `List` reference can be reassigned across any of them:

```java
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Stack;
import java.util.Vector;

class ListParentRef {
    public static void main(String[] args) {
        List l = new ArrayList();
        l = new LinkedList();
        l = new Stack();
        l = new Vector();
        // same reference type; runtime object can be any List implementation
    }
}
```

The reference stays the same; the runtime object can be anything that
`implements List`. **Using a parent reference to hold any child-type object
is also polymorphism.**

> ⚠️ **Modern Java — two of these four implementations are legacy, and a
> fifth, immutable option now exists.**
> `Vector` and `Stack` predate the Collections Framework (retrofitted into
> it in Java 1.2) and both synchronize every operation, which nobody wants
> by default in single-threaded code. `Stack` additionally extends `Vector`
> instead of composing it — a design Sun itself has called a mistake — so
> it inherits index-based methods that break the stack discipline it is
> meant to enforce. Modern code reaches for:
> - `ArrayList` / `LinkedList` in place of `Vector`,
> - `ArrayDeque` (Java 6, but rarely taught pre-collections) in place of
>   `Stack`, via its `push`/`pop`/`peek` methods,
> - `Collections.synchronizedList(...)` or a `java.util.concurrent`
>   collection where you actually need thread safety.
>
> Since **Java 9**, there is also a fifth kind of `List` to assign into the
> same reference: an **immutable** one, `List.of(1, 2, 3)`. Unlike the four
> above, it throws `UnsupportedOperationException` on any mutating call —
> worth knowing before you plug it into code that expects to `add()` to it.

## 1:14:16 — The catch: a parent reference can only call parent methods

Advantage established — but there is a real restriction. `Parent p = new
Child()` is valid, but through `p` you can call **only the methods declared
in the parent class**. Reach for a child-specific method and it is a
compile error, not a runtime one:

```java
class P {
    public void m1() {
        System.out.println("parent m1");
    }
}

class C extends P {
    public void m2() {
        System.out.println("child m2");
    }
}

class ParentRefRestriction {
    public static void main(String[] args) {
        P p = new C(); // valid — parent reference holding a child object
        p.m1();
        // prints parent m1
        p.m2();
        // CE: cannot find symbol
        //   symbol:   method m2()
        //   location: variable p of type P
    }
}
```

If a parent method **is** overridden in the child, the child's version
still runs (that part is ordinary overriding) — but it is still a method
that exists on the parent's type. Only methods that exist **exclusively** on
the child are unreachable through a parent reference. Using a **child**
reference instead removes the restriction entirely — both `m1()` and `m2()`
are callable — so the natural next question is: what is the parent
reference actually buying you?

## 1:21:19 — When to prefer the parent reference

**When you don't know the exact runtime type.** Two concrete cases:

**`ArrayList.get(0)` returns `Object`.** A (raw) list can hold heterogeneous
objects — a `Student`, a `Customer`, a `String`, anything. You cannot
declare a return type for `get()` that is specific to any one of them, so
the method is typed to return the one reference that can point at all of
them: `Object`.

```java
import java.util.ArrayList;

class Student { }
class Customer { }

class GetZero {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        l.add(new Student());
        l.add(new Customer());
        l.add("hello");

        Object o = l.get(0); // don't know the exact runtime type — Object covers all of them
    }
}
```

**A method that may return `ArrayList`, `LinkedList`, `Vector`, or `Stack`
depending on logic.** No single one of those four return types covers every
case; the common parent, `List`, does:

```java
import java.util.ArrayList;
import java.util.List;

class ReturnAnyList {
    public List m1() {
        return new ArrayList(); // could equally be LinkedList / Vector / Stack
    }

    public static void main(String[] args) {
        ReturnAnyList t = new ReturnAnyList();
        List l = t.m1(); // parent reference — caller doesn't know the exact runtime type
    }
}
```

If you **do** know the runtime type will always be one specific class —
"this always returns `ArrayList`" — declare the reference as that exact
class instead.

## 1:29:32 — Interview pair: `C c = new C()` vs `P p = new C()`

A very common interview framing, restated with `ArrayList`/`List` since it
is the same question:

| | `C c = new C();` / `ArrayList l = new ArrayList();` | `P p = new C();` / `List l = new ArrayList();` |
|---|---|---|
| **When** | use this when you know the exact runtime type | use this when you don't know the exact runtime type |
| **Methods reachable** | both parent and child methods — the advantage of this approach | only parent methods; child-specific methods are unreachable — the disadvantage |
| **What it can hold** | only that particular child type — the disadvantage | any child type of the parent — the advantage |

```java
class P { public void m1() { } }
class C extends P { public void m2() { } }

class ChildWhenWeKnow {
    public static void main(String[] args) {
        C c = new C(); // we know runtime type is C
        c.m1();
        c.m2();
        // both callable; can hold only C, not a sibling of C
    }
}

class ParentWhenWeDontKnow {
    public static void main(String[] args) {
        P p = new C(); // we don't know exactly which child type
        p.m1();
        // p.m2(); // CE: cannot find symbol
        // can hold any child of P
    }
}
```

> ⚠️ **Modern Java — `var` breaks this pattern if you reach for it here.**
> Local variable type inference (**Java 10**) infers the variable's static
> type from its initializer expression — not from any wider type you might
> have intended:
> ```java
> var p = new C(); // inferred type is C, not P
> p.m2();           // compiles — p's static type is C
> ```
> `var` is a genuine convenience elsewhere, but it cannot express "I want a
> parent-typed reference holding a child object" — that distinction only
> exists if you write the parent type out: `P p = new C();`. Anywhere this
> lecture's polymorphism argument depends on the *declared* type of the
> reference, `var` is the wrong tool.

---

## 1:39:17 — The three pillars of OOPs

Three concepts act as the pillars of OOPs — the first and third already
covered in earlier sessions, the second just discussed:

1. **Encapsulation** — one word: **security**.
2. **Polymorphism** — one word: **flexibility** (for the programmer).
3. **Inheritance** — one word: **reusability**.

## 1:43:28 — Static polymorphism vs. dynamic polymorphism

| Kind | Also known as | Examples |
|---|---|---|
| Static polymorphism | compile-time polymorphism, early binding | overloading, method hiding |
| Dynamic polymorphism | runtime polymorphism, late binding | overriding |

## 1:46:14 — A popular internet "definition" (offered as folklore)

Sir shares this with an explicit disclaimer — *"whether it is correct or
not, I don't know; I'm not having any experience in that area"* — and
invites the room to take it or leave it:

*A boy starts love with the word "friendship" — the usual bus-stop or
classroom line, "we're just friends." A girl ends love with the same word —
on the wedding day, a card that reads "we are friends forever." Same word,
different attitude, at the start versus the end.*

The one-line takeaway he wants kept: **the word is the same, but the
attitude is different** — not a technical claim, just a mnemonic for "same
name, different behaviour" that has nothing to do with correctness, and he
says so.

## 1:48:44 — Next

Coupling, cohesion, type casting, then instance control flow, static
control flow, and constructors.

---

## Exam and interview points

1. **A var-arg method is overridden only by another method with the same
   parameter list after erasure** — usually another var-arg method, but a
   plain array parameter of the same type also qualifies. Pair it with a
   *normal* (non-array) parameter instead and you get overloading: compiler
   + reference type, output `parent child parent`. Both var-arg (or
   var-arg/array-equivalent): real overriding, output `parent child child`.
2. **Overriding never applies to variables.** Field access is always
   resolved by the compiler from the reference's declared type, regardless
   of static/instance, in all four combinations — always `888 999 888` for
   `P p1 = new C(); p1.x`.
3. **The nine overloading-vs-overriding differences, compressed to one
   rule:** overloading checks only method names (same) and argument types
   (different); overriding checks the complete prototype — names,
   arguments, return type (covariant since 1.5), access modifier (can
   widen, never narrow), and throws clause (checked exceptions can only
   shrink toward the parent's type).
4. **Illegal modifier combinations fail before any overload/override
   analysis even starts.** `static abstract` on the same method is a
   straight compile error — it looks like a valid overload by argument type
   alone, but the modifiers are rejected first.
5. **A parent reference can call only methods declared on the parent type**,
   even when it holds a child object — reach for a child-specific method
   and it is `cannot find symbol`, a compile-time failure, not a runtime
   one. Use a parent-type reference specifically when the exact runtime
   type is unknown to the caller (`ArrayList.get(0)` returning `Object` is
   the canonical example); use the exact type when you know it.
6. **Three pillars, one word each:** encapsulation = security, polymorphism
   = flexibility, inheritance = reusability.
7. **`var` cannot express "parent reference, child object."** It infers the
   initializer's type, so `var p = new C();` gives `p` the type `C`, not
   `P` — write the parent type explicitly whenever the reference type
   itself is the point.

**Next:** Video 058 — Coupling
