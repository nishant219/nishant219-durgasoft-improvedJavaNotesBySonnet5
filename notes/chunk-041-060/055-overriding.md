# Video 055 — Overriding

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-5 ||overriding

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 55 of 203 |
| Series | OOPs · Part 5 |
| Topic | overriding |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 22m 38s |
| Video ID | MYzaDgNGmTg |
| Watch | https://www.youtube.com/watch?v=MYzaDgNGmTg |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

OOPs Part 5, continuing straight from overloading. Sir works through:

1. What overriding is (the parent/child property-and-marriage story) and the
   overridden-method / overriding-method terminology.
2. The three reference/object combinations, and why overriding is checked by
   the **compiler** for syntax but resolved by the **JVM** at the actual call
   — runtime polymorphism, contrasted with overloading's compile-time
   resolution.
3. The rule list: matching signatures, return types (same until 1.4,
   covariant from 1.5), private methods (exempt), final methods (exempt),
   abstract ↔ concrete either direction, `synchronized`/`native`/`strictfp`
   (no restriction), and access modifiers (widen only, never narrow).

`static` is named but explicitly deferred to a later video, and `throws` is
only mentioned as a future check — neither is taught here. Both continue in
video 056.

---

## 00:07 — From overloading to overriding

Overloading, Sir recaps, is simple: method names must match, argument types
must differ. That's the whole check.

```java
class OverloadingIsSimple {
    public void m1(int i) {
        System.out.println("int");
    }
    public void m1(String s) {
        System.out.println("String");
    }
    public static void main(String[] args) {
        OverloadingIsSimple t = new OverloadingIsSimple();
        t.m1(10);      // int
        t.m1("durga"); // String
    }
}
```

Overriding is a different, and much stricter, kind of check: method names,
argument types, return types, modifiers, `throws`, access modifiers — every
one of them has a rule to satisfy.

## 00:54 — What overriding is

A parent class's methods and variables are, by inheritance, available to the
child automatically. Two things can happen with an inherited method:

1. The child is **satisfied** with the parent's implementation → uses it as-is.
2. The child is **not satisfied** → the child **redefines** that method in its
   own body. That redefinition is **overriding**.

```java
class P0 {
    public void m1() {
        System.out.println("parent implementation");
    }
}
class C0 extends P0 {
    // satisfied — no redefinition
}
class TestSatisfied {
    public static void main(String[] args) {
        C0 c = new C0();
        c.m1(); // prints "parent implementation"
    }
}
```

## 02:27 — The property/marriage story

Sir's memory hook: a parent gives the child two things — **property**
(cash + land + gold) and an arranged **marriage**. The property, the child
is happy to inherit as-is. The marriage, the child wants to redefine.

```java
class P {
    public void property() {
        System.out.println("cash+land+gold");
    }
    public void marry() {
        System.out.println("Subbalakshmi"); // parent's choice
    }
}
class C extends P {
    public void marry() {
        System.out.println("Trisha"); // child's own choice
    }
}
```

`property()` is inherited and never touched — the child is satisfied.
`marry()` is redefined in `C` — that's overriding.

## 06:44 — Overridden method vs. overriding method

The vocabulary Sir wants memorized:

- The parent's method that gets redefined = the **overridden method**.
- The child's redefinition = the **overriding method**.

Here, `P.marry()` is the overridden method and `C.marry()` is the overriding
method. `property()` is neither — it's plain inheritance, nothing about it is
overridden.

> Whatever methods a parent has are, by default, available to the child
> through inheritance. If the child is not satisfied with the parent's
> implementation, it may redefine that method based on its own requirement.
> This process is called **overriding**.

## 13:16 — Three reference/object combinations

Same `P`/`C` from above, called from three different `Test` classes.

**Case 1 — parent reference, parent object.**

```java
class TestCase1 {
    public static void main(String[] args) {
        P p = new P();
        p.marry(); // Subbalakshmi — nothing here touches C at all
    }
}
```

**Case 2 — child reference, child object.**

```java
class TestCase2 {
    public static void main(String[] args) {
        C c = new C();
        c.marry(); // Trisha — everything here is C
    }
}
```

**Case 3 (the important one) — parent reference, child object.**

```java
class C2 extends P {
    public void marry() {
        System.out.println("Trisha");
    }
    public void childSpecific() {
        System.out.println("only on C2");
    }
}
class TestChildSpecific {
    public static void main(String[] args) {
        P p1 = new C2();
        p1.marry();
        // prints Trisha
        // p1.childSpecific();
        // CE: cannot find symbol — method childSpecific() not in P
    }
}
```

A parent reference can hold a child object — but through that reference you
can only *call* methods that exist in the parent's type. Child-only methods
(like `childSpecific()`) are invisible through a `P` reference, even though
the underlying object is a `C2`.

## 16:00 — Compiler checks the reference type; JVM checks the object

For `p1.marry()` above:

- **Compiler**: `p1` is declared `P`. Does `P` have a `marry()`? Yes → it
  compiles. The compiler never looks at what object `p1` actually holds.
- **JVM, at runtime**: what's the *actual* object — `P` or `C2`?
  - If it's a `P` → run `P`'s method.
  - If it's a `C2` → check whether `C2` overrides that method.
    - Not overridden → the inherited parent body runs.
    - Overridden → the **child's** method runs, because resolution is based
      on the runtime object, not the reference type.

If `C2` had *not* overridden `marry()`, `P p1 = new C2()` would still print
the parent's `Subbalakshmi` — it's simply inherited, unchanged:

```java
class CNoOverride extends P {
    // no marry() here
}
class TestNoOverride {
    public static void main(String[] args) {
        P p1 = new CNoOverride();
        p1.marry(); // Subbalakshmi — not overridden, so the parent body runs
    }
}
```

## 18:39 — Overriding is runtime polymorphism; overloading is compile-time

Because method resolution always looks at the **runtime object**, overriding
is also called **runtime polymorphism**, **dynamic polymorphism**, or **late
binding** — the JVM can't know which body will run until the object exists.

```java
class TestAllThree {
    public static void main(String[] args) {
        P p = new P();
        p.marry();          // Subbalakshmi — runtime object is P

        C c = new C();
        c.marry();          // Trisha — runtime object is C

        P p1 = new C();
        p1.marry();         // Trisha — runtime object is C
    }
}
```

Contrast with **overloading**: resolution is always done by the **compiler**,
based on the **reference type** plus argument types — hence overloading is
**compile-time polymorphism**, **static polymorphism**, or **early binding**.

| | Resolved by | Based on | Also known as |
|---|---|---|---|
| Overloading | compiler | reference type + argument types | compile-time / static / early binding |
| Overriding | JVM | runtime object | runtime / dynamic polymorphism / late binding |

```java
class OL {
    public void m1(int i) {
        System.out.println("int version");
    }
    public void m1(double d) {
        System.out.println("double version");
    }
}
class OverloadingResolution {
    public static void main(String[] args) {
        OL x = new OL();
        x.m1(10); // int version — chosen at compile time from reference + argument
    }
}
```

## 23:57 — The rule list begins

Sir's analogy: overloading is a simple pairing, but overriding is like an
arranged marriage the child wants renegotiated — there are conditions to
satisfy on every side, and getting one wrong means the compiler (or the JVM,
for the parts it checks) rejects the whole thing. The rules: method name,
argument types, return types, modifiers, `throws`, access modifiers.

### 25:30 — Rule 1: signatures must match

Method name and argument types must be **identical** to the parent's — the
opposite of overloading, where argument types must differ.

```java
class P {
    public void m1() {
        System.out.println("parent m1");
    }
}
class C extends P {
    public void m1() {
        System.out.println("child m1");
    }
}
```

Change the argument list in the child and you get **overloading**, not
overriding — the parent's version is still separately callable:

```java
class P2 {
    public void m1() {
        System.out.println("parent m1()");
    }
}
class C2 extends P2 {
    public void m1(int i) {
        System.out.println("child m1(int)");
    }
}
class TestNotOverride {
    public static void main(String[] args) {
        P2 p = new C2();
        p.m1();
        // parent m1() — m1() and m1(int) don't collide
        C2 c = new C2();
        c.m1(10);
        // child m1(int)
    }
}
```

### 27:22 — Rule 2: return types — same until 1.4, covariant from 1.5

Until Java 1.4, the child's return type had to match the parent's exactly.
From **Java 1.5**, the child may return a **covariant type** — the same type
or any subtype of it.

```java
class P {
    public Object m1() {
        return null;
    }
}
class C extends P {
    public String m1() { // String is-a Object: covariant, valid from 1.5
        return null;
    }
}
```

Sir live-compiles this same file three ways:

```text
javac P.java              → OK (compiles under any modern default too)
javac -source 1.4 P.java  → CE: m1 in C cannot override m1 in P;
                             attempting to use incompatible return type;
                             found String, required Object
javac -source 1.5 P.java  → OK
```

> ⚠️ **Modern Java — you can no longer ask `javac` to pretend it's 1.4.**
> Verified on JDK 26: `javac -source 1.4` and even `javac --release 7` both
> fail with `error: Source option 1.4 is no longer supported. Use 8 or
> later.` The oldest source level any current `javac` will accept is **8**.
> The rule itself hasn't moved — covariant returns have been legal from 1.5
> onward and still are today — but the "watch it fail on 1.4, then pass on
> 1.5" live demo can't be reproduced on a current JDK; you'd need an actual
> old JDK toolchain installed to see the CE.

Direction matters: the child's type may be the same or **more specific**,
never more general.

```java
class P {
    public String m1() {
        return null;
    }
}
class C extends P {
    public Object m1() { // Object is a supertype of String — wrong direction
        return null;
    }
    // CE: m1() in C cannot override m1() in P
    // attempting to use incompatible return type
    // found: Object, required: String
}
```

And covariance is an **object-type-only** concept — it does not apply to
primitives, even ones that otherwise widen freely:

```java
class P {
    public double m1() {
        return 10.5;
    }
}
class C extends P {
    public int m1() { // int does NOT covary with double
        return 10;
    }
    // CE: m1() in C cannot override m1() in P
    // return type int is not compatible with double
}
```

A quick reference for what's legal for a few common parent return types (any
of these is either the same type or a genuine reference subtype):

| Parent return type | Legal child return types (1.5+) |
|---|---|
| `Object` | `Object`, `String`, `StringBuffer`, … any reference subtype |
| `Number` | `Number`, `Integer`, `Float`, `Double`, … |
| `String` | `String` only — no further useful reference subtype |

### 43:13 — Rule 3: private methods are exempt

A parent's `private` method is **not inherited** by the child at all — so
there's nothing to override.

```java
class P {
    private void m1() {
        System.out.println("parent private");
    }
    public void callM1() {
        m1();
    }
}
class C extends P {
    private void m1() { // a brand-new, unrelated method — not an override
        System.out.println("child private");
    }
    public void callChildM1() {
        m1();
    }
}
class TestPrivate {
    public static void main(String[] args) {
        P p = new C();
        p.callM1();
        // prints parent private — P.m1() never sees C.m1()
        C c = new C();
        c.callChildM1();
        // prints child private
    }
}
```

Writing the identical `private void m1()` in the child **compiles fine** — it
is just a separate, private-to-that-class method, not overriding.
**Overriding does not apply to private methods.**

### 48:20 — Rule 4: final methods can't be overridden

Public-to-public is ordinary valid overriding. But if the parent marks the
method `final`, the child cannot redefine it at all — final means "this
implementation is not negotiable."

```java
class P {
    public final void m1() {
    }
}
class C extends P {
    public void m1() {
    }
    // CE: m1() in C cannot override m1() in P
    // overridden method is final
}
```

The error names the **overridden** (parent) method as final, and it fires
regardless of whether the child's attempt is itself `final` or not —
final-to-non-final and final-to-final both fail:

```java
class C2 extends P {
    public final void m1() {
    }
    // CE: m1() in C2 cannot override m1() in P
    // overridden method is final — illegal even though C2's copy is final too
}
```

The reverse — non-final parent, `final` child — is fine. It just locks the
method starting from that subclass downward:

```java
class P2 {
    public void m1() {
        System.out.println("parent");
    }
}
class C3 extends P2 {
    public final void m1() {
        System.out.println("child final");
    }
}
class SubC extends C3 {
    // public void m1() { }
    // CE: m1() in SubC cannot override m1() in C3
    // overridden method is final
}
class TestNonFinalToFinal {
    public static void main(String[] args) {
        P2 p = new C3();
        p.m1(); // child final
    }
}
```

### 54:11 — Rule 5: abstract and concrete override each other freely

**Abstract parent → concrete child** isn't just allowed, it's compulsory
somewhere in the hierarchy — providing the body is the whole point of
declaring `abstract` in the first place:

```java
abstract class P {
    public abstract void m1();
}
class C extends P {
    public void m1() {
        System.out.println("provided implementation");
    }
}
```

**Concrete parent → abstract child** is also valid, if less obviously useful.
Sir's analogy: a crying baby who wants *something* but can't say what — the
same shape as "I don't want the parent's implementation, but I don't know
what mine should be yet." Declaring the override `abstract` says exactly
that:

```java
class P {
    public void m1() {
        System.out.println("parent concrete");
    }
}
abstract class C extends P {
    public abstract void m1();
}
```

The advantage: it **cuts off** the parent's implementation from every class
further down the hierarchy. The next concrete subclass is *forced* to write
its own body — it can no longer silently fall back to the parent's:

```java
class SubC extends C {
    public void m1() {
        System.out.println("SubC must write its own");
    }
}
class TestStopParentImpl {
    public static void main(String[] args) {
        P p = new SubC();
        p.m1();
        // "SubC must write its own" — P's original body is unreachable from here on
        // C c = new C();
        // CE: C is abstract; cannot be instantiated
    }
}
```

### 1:04:40 — Rule 6: `synchronized`, `native`, `strictfp` — no restriction either way

Unlike `final` and access modifiers, these three keywords never block an
override in any direction — parent and child can differ freely.

```java
class P {
    public synchronized void m1() {
    }
}
class C extends P {
    public void m1() { // dropping synchronized: fine
    }
}
```

```java
class P2 {
    public native void m1();
}
class C2 extends P2 {
    public void m1() { // native parent, Java-body child: fine
        System.out.println("Java implementation instead of native");
    }
}
```

The canonical example is `Object.hashCode()`, which the JDK implements as a
`native` method — yet every class overrides it with an ordinary Java body:

```java
class MyClass {
    public int hashCode() {
        return 10;
    }
}
class TestHashCode {
    public static void main(String[] args) {
        MyClass c = new MyClass();
        System.out.println(c.hashCode()); // 10
    }
}
```

Verified on JDK 26 by reflection (`Modifier.toString(Object.class
.getDeclaredMethod("hashCode").getModifiers())` → `"public native"`):
`Object.hashCode()` is still `native`, and the override-freely rule for
`native` has not changed.

```java
class P3 {
    public strictfp void m1() {
    }
}
class C3 extends P3 {
    public void m1() { // no strictfp: still fine
    }
}
```

> ⚠️ **Modern Java — `strictfp` is a no-op since Java 17.**
> JEP 306 made *all* floating-point arithmetic strict by default, which is
> exactly what `strictfp` used to opt into. This override rule ("no
> restriction in either direction") still holds — but it's now trivially
> true, because there's no longer a "non-strict" mode for the keyword to
> differ over. Writing `strictfp` today compiles fine but with a lint
> warning and changes nothing at runtime: `javac -Xlint:strictfp` reports
> *"as of release 17, all floating-point expressions are evaluated strictly
> and 'strictfp' is not required."*

### 1:11:17 — `static` is missing on purpose

Of the method-level modifiers, `final`, `abstract`, `synchronized`, `native`,
`strictfp` are covered here. **`static`** is deliberately left out — Sir
flags it as having enough rules of its own (static methods are hidden, not
overridden, and resolved by reference type, not runtime object) to deserve a
separate video. Not taught here.

### 1:12:01 — Rule 7: access modifiers can only widen, never narrow

Public parent, default (package-private) child: **compile-time error**.
While overriding, you may **increase** a method's accessibility but never
**reduce** it.

```java
class P {
    public void m1() {
    }
}
class C extends P {
    void m1() {
    }
    // CE: m1() in C cannot override m1() in P
    // attempting to assign weaker access privileges; was public
}
```

Widening is always fine — default→public, protected→public, and
default→protected all pass:

```java
class P1 { void m1() {} }
class C1 extends P1 { public void m1() {} }      // default -> public: OK

class P2 { protected void m1() {} }
class C2 extends P2 { public void m1() {} }       // protected -> public: OK

class P3 { void m1() {} }
class C3 extends P3 { protected void m1() {} }    // default -> protected: OK
```

Narrowing always fails the same way — public→protected and protected→default
both give the "weaker access privileges" error:

```java
class P4 { public void m1() {} }
class C4 extends P4 {
    protected void m1() {}
    // CE: attempting to assign weaker access privileges; was public
}

class P5 { protected void m1() {} }
class C5 extends P5 {
    void m1() {}
    // CE: attempting to assign weaker access privileges; was protected
}
```

### 1:18:32 — The accessibility ladder

From most restricted to most open:

**`private` < *default* < `protected` < `public`**

### 1:19:12 — Full access-modifier table

| Parent's access | Legal child access |
|---|---|
| `public` | `public` only |
| `protected` | `protected` or `public` |
| *default* | *default*, `protected`, or `public` |
| `private` | n/a — private isn't inherited, so "overriding" doesn't apply |

```java
class P { private void m1() {} }
class C extends P {
    public void m1() {} // compiles, but this is a NEW method, not an override
}
```

---

## Exam and interview points

1. **Overriding checks everything**: name, arguments, return type,
   modifiers, `throws`, access — overloading only checks name plus different
   arguments.
2. **Resolution**: overloading is decided by the **compiler** from the
   **reference type** (compile-time / static / early binding); overriding is
   decided by the **JVM** from the **runtime object** (runtime / dynamic
   polymorphism / late binding).
3. **`P p1 = new C()`** — calling an overridden method through a parent
   reference still runs the **child's** version; calling a child-only method
   through that same reference is a compile error, because the compiler only
   ever sees `P`.
4. **Return types**: must match exactly until 1.4; **covariant** (same type
   or a subtype) from 1.5 onward. Covariance applies to **object types
   only** — never to primitives, even "compatible" ones like `double`→`int`.
5. **Private methods are never overridden** — they aren't inherited, so a
   same-named private method in the child is just a separate, unrelated
   method.
6. **Final methods can never be overridden**, in either direction (final or
   non-final child) — CE: *"overridden method is final."* Non-final → final
   is fine; it just locks the method starting from that subclass downward.
7. **Abstract ↔ concrete works both ways**: abstract-to-concrete provides the
   implementation (the entire point of `abstract`); concrete-to-abstract is
   also legal, and its use is to **force every further subclass** to supply
   its own body, cutting off inheritance of the original implementation.
8. **`synchronized`, `native`, `strictfp` place zero restriction** on
   overriding, in either direction. `Object.hashCode()` (`native`) being
   freely overridden with a plain Java body is the standard proof.
9. **Access modifiers can only widen, never narrow**, when overriding:
   `private < default < protected < public`. Narrowing gives CE:
   *"attempting to assign weaker access privileges."*
10. **`static` has its own separate rule set** (method hiding, not
    overriding) — not covered in this video; continues later in the course.

---

**Next:** Video 056 — Overriding and access modifiers
