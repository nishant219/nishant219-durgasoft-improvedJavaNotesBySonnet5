# Video 065 — Default constructor

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-15 || default constructor

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 65 of 203 |
| Series | OOPs · Part 15 |
| Topic | default constructor |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 48m 56s |
| Video ID | misWPx3VTGI |
| Watch | https://www.youtube.com/watch?v=misWPx3VTGI |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is **OOPs Part 15**: the exact shape of the constructor the compiler
writes for you. Three rules — always no-arg, same access modifier as the
class, body is exactly `super();` — then six worked "programmer's code vs
compiler's code" examples showing *when* the compiler adds that code and when
it politely does nothing. From there the lecture turns to the syntax rules
around `super()`/`this()` as constructor calls (first line only, one or the
other, constructors only) versus `super`/`this` as ordinary keywords
(anywhere but static context, any number of times) — a favourite interview
comparison. The one rule this video treats as absolute — statements before
`super()`/`this()` are always illegal — is also the one Java has since
relaxed; see the callout under Case 1.

---

## 00:04 — Topic: prototype of the default constructor

What does the compiler-generated constructor actually look like? Given an
empty class:

```java
class Test {
}
```

the programmer wrote no constructor, so the compiler generates one. This
lecture nails down its exact prototype: three fixed points.

### 00:49 — Point 1: always a no-arg constructor

**The default constructor is always a no-argument constructor** — but the
converse is false: **every no-arg constructor is not a default constructor.**

If the programmer writes this:

```java
class Test {
    Test() {
    }
}
```

that is a constructor **provided by the programmer**. It is **not** a default
constructor, even though it takes no arguments. "Default constructor" means
specifically *compiler-generated*; it is a statement about origin, not shape.

### 02:05 — Point 2: access modifier same as the class

The default constructor's access modifier is **exactly the class's access
modifier**: `public` class → `public` default constructor; package-private
(default-access) class → package-private default constructor.

This rule only has two cases to state — public and default — because a
top-level class can never be declared `private` or `protected` in the first
place, so there is no "what if the class were private" scenario to cover for
a top-level class.

```java
private class Bad { }   // CE: modifier private not allowed here
```

### 03:10 — Point 3: body is exactly one line — `super();`

The default constructor contains **exactly one line**:

```java
super();
```

— a no-argument call to the superclass constructor. Nothing else.

### 04:12 — The three points, together

1. Always a **no-arg** constructor.
2. Access modifier is **exactly the same as** the class's access modifier
   (only meaningful for `public` and default, since top-level classes cannot
   be `private`/`protected`).
3. Contains **only one line**: `super();`.

---

## 06:55 — Six examples: programmer's code vs compiler's code

Sir works through six cases as two columns — **P's code** (what the
programmer typed) and **C's code** (the effective class after the compiler's
additions, shown here as what that class would look like if you wrote out
everything the compiler inserted).

### 07:47 — Example 1: empty class

**P's code:**

```java
class Test {
}
```

No constructor written → compiler generates the default constructor.

**Effective C's code:**

```java
class Test {
    Test() {
        super();
    }
}
```

### 08:31 — Example 2: `public` class

**P's code:**

```java
public class Test {
}
```

**Effective C's code:**

```java
public class Test {
    public Test() {
        super();
    }
}
```

Access modifier of the generated constructor matches the class: `public`.

### 09:17 — Example 3: a method named `test` is not a constructor

**P's code:**

```java
public class Test {
    void test() {
    }
}
```

`void test()` has a return type, so it is a **method**, not a constructor —
even though its name matches the class name. No constructor was written, so
the compiler still generates the default one.

**Effective C's code:**

```java
public class Test {
    public Test() {
        super();
    }

    void test() {
    }
}
```

```java
public class Ex3 {
    void test() { }
    public static void main(String[] args) {
        Ex3 e = new Ex3();          // compiler-generated Ex3() runs
        System.out.println("ok: " + e);
    }
}
```

This compiles and runs — confirming the default constructor is generated
independently of `test()`.

### 10:41 — Example 4: an empty no-arg constructor the programmer wrote

**P's code:**

```java
class Test {
    Test() {
    }
}
```

No default constructor is generated — the programmer already supplied a
constructor. But the compiler runs a **second check**: was that constructor
written *properly*? The rule: **the first statement inside every constructor
must be either a `super(...)` or a `this(...)` call.** If neither is present,
the compiler inserts `super();` as the first statement.

**Effective C's code:**

```java
class Test {
    Test() {
        super();   // inserted by the compiler
    }
}
```

The distinction Sir stresses: this is not a new *default constructor* — it is
the compiler filling in the missing `super();` inside the programmer's own
constructor.

### 13:05 — Example 5: an arg constructor with an explicit `super()`

```java
class Test {
    Test(int i) {
        super();
    }
}
```

The programmer wrote a constructor, and its first line is already
`super()` — written properly. The compiler adds nothing at all. This is the
best-case style: every line in the constructor is the programmer's own.

### 14:06 — Example 6: `this(10)` chaining, missing `super` elsewhere

**P's code:**

```java
class Test {
    Test() {
        this(10);
    }

    Test(int i) {
    }
}
```

Two constructors, so no default constructor is generated. Checking each one:
the first constructor's first line is `this(10)` — properly written, no
insertion needed there. The second constructor has neither `super` nor
`this` as its first line, so the compiler inserts `super();`.

**Effective C's code:**

```java
class Test {
    Test() {
        this(10);
    }

    Test(int i) {
        super();   // inserted by the compiler
    }
}
```

```java
class Ex4 {
    Ex4() { this(10); }
    Ex4(int i) { System.out.println("i=" + i); }
    public static void main(String[] args) { new Ex4(); }   // prints "i=10"
}
```

---

## 20:34 — Restating the rule

**The first line inside every constructor must be either `super(...)` or
`this(...)`.** If the programmer writes neither, the compiler always inserts
`super();`. From that single rule, three important cases follow.

### 22:22 — Case 1: `super`/`this` only as the *first* statement

```java
class Test {
    Test() {
        System.out.println("Constructor");
        super();
    }
}
// CE: call to super must be first statement in constructor
```

Moving the `println` after `super()` fixes it:

```java
class Test {
    Test() {
        super();
        System.out.println("Constructor");
    }
}
```

> ⚠️ **Modern Java — this rule has been relaxed. Statements are now allowed *before* `super()`/`this()`.**
> Through Java 21, "call to `super()`/`this()` must be the first statement"
> was an absolute rule — exactly as taught here. **Flexible Constructor
> Bodies** (JEP 447 → JEP 482 → JEP 492 as successive previews in Java
> 22–24, **finalized as a standard feature in Java 25**, JEP 513) changed
> that: a constructor may now contain *prologue* statements before the
> explicit `super(...)`/`this(...)` call, as long as those statements do not
> read or write the instance being constructed — no `this`, no instance
> field, no instance method call, no `super` field/method access:
>
> ```java
> class Test {
>     Test() {
>         System.out.println("Constructor");   // OK from Java 25 — no 'this' used
>         super();
>     }
> }
> ```
>
> compiles cleanly under `javac --release 25` (verified). But this still fails,
> at any Java version, because it touches the instance before it exists:
>
> ```java
> class Test2 extends Object {
>     Test2() {
>         System.out.println(this.hashCode());   // CE even on 25: reference to
>         super();                                // this may only appear after
>     }                                            // an explicit constructor invocation
> }
> ```
>
> The motivating case is validating constructor arguments before delegating
> — e.g. `if (age < 0) throw new IllegalArgumentException();` ahead of
> `super(age);` — something you previously had to route through a private
> static helper method or a `this(...)` chain to a validating constructor.
> Sir's rule is still exactly right for any code compiled at source level 21
> or below (which is most legacy code, and the OCJP target for this course).

### 26:34 — Case 2: either `super` or `this`, never both

```java
class Test {
    Test() {
        super();
        this();
    }
}
// CE: call to this must be first statement in constructor
```

A constructor may make **one** explicit constructor-call — `super(...)` or
`this(...)`, never both — because only one statement can occupy that "first
line" slot.

> ⚠️ **Modern Java — this still holds, only the diagnostic text changed.**
> Verified on `javac --release 25`: the same code now reports
> `error: redundant explicit constructor invocation` instead of the classic
> `call to this must be first statement in constructor`. The wording changed
> because flexible constructor bodies made "first statement" no longer the
> right way to describe the restriction; the restriction itself — one
> explicit constructor call per constructor — is unchanged.

### 28:40 — Case 3: only inside a constructor, never inside a method

```java
class Test {
    public void m1() {
        super();
    }
}
// CE: explicit constructor invocation may only appear within a constructor body
```

`super(...)`/`this(...)` are constructor calls — they exist to invoke a
superclass constructor or another constructor of the current class directly.
That is only meaningful from inside a constructor; a regular method has no
such thing to invoke.

> ❗ **Correction — the compiler error here is not the "first statement" message.**
> The transcript's live demo and this note's draft both reused
> `call to super must be first statement in constructor` for this case. That
> message is for Case 1 (right constructor, wrong position). Calling
> `super()`/`this()` from a **non-constructor method** — where there is no
> constructor at all to be "first" in — has always produced a different,
> more precise diagnostic: `explicit constructor invocation may only appear
> within a constructor body`. Confirmed unchanged on `javac --release 17`
> through the current JDK 26.

### 34:36 — The rule in one line

A constructor can be called directly — `super(...)` or `this(...)` — **only
from another constructor.**

### 35:19 — Summary: `super()`/`this()` as constructor calls

1. Only inside **constructors**.
2. Only as the **first line** *(through Java 21 — see the Case 1 callout)*.
3. Only **one** per constructor — never both.

---

## 37:47 — `super()`/`this()` vs `super`/`this`

An interview favourite: the constructor-call syntax and the keyword are
spelled the same but mean different things.

| | `super()` / `this()` | `super` / `this` |
|---|---|---|
| **What** | Constructor calls — invoke the superclass or current-class constructor | Keywords — refer to a superclass or current-class **instance member** |
| **Where** | Only inside constructors, as the first line | Anywhere except a static context |
| **How many** | At most one per constructor | Any number of times |

```java
class P {
    int x = 100;
}

class C extends P {
    int x = 200;

    public void m1() {
        System.out.println(this.x);    // current class's x  → 200
        System.out.println(super.x);   // superclass's x     → 100
    }
}
```

`this.x` reaches the current class's instance member; `super.x` reaches the
superclass's. Neither line is a constructor call — both are ordinary field
access through a keyword.

### 41:13 — Where each is legal

`super`/`this` (the keywords) may appear **anywhere except a static
context**, because they refer to instance members and a static context has
no current instance to refer to:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(super.hashCode());
    }
}
// CE: non-static variable super cannot be referenced from a static context
```

(Confirmed unchanged on `javac --release 17` and on the current JDK 26 — this
diagnostic has not moved.)

### 43:47 — How many times each can appear

`super()`/`this()` as a constructor call can appear **once** in a
constructor. `super`/`this` as keywords can appear **any number of times** —
`this.name`, `this.rollNumber`, `this.age`, and so on, with no limit.

### 44:44 — The comparison, in one table

| Point | `super()` / `this()` | `super` / `this` |
|---|---|---|
| What | Constructor calls — invoke the superclass/current-class constructor | Keywords — refer to superclass/current-class instance members |
| Where | Only in constructors, as the first line | Anywhere except a static context |
| How many | Once per constructor | Any number of times |

---

## Exam and interview points

1. **"Default constructor" means compiler-generated, not "takes no
   arguments."** A no-arg constructor the programmer writes is still not a
   default constructor — the distinction is about *who wrote it*.
2. **Three fixed points of the default constructor**: no-arg, same access
   modifier as the class, and a body of exactly one line — `super();`.
3. **The compiler runs two independent checks per class**: (a) did the
   programmer write *any* constructor — if not, generate the default one;
   (b) for whichever constructor(s) exist, does each start with `super(...)`
   or `this(...)` — if not, insert `super();`. These checks are not the same
   thing; example 4 in this lecture exercises check (b) alone.
4. **A method matching the class name is still just a method**, not a
   constructor, if it declares a return type (even `void`). The compiler
   still generates the default constructor in that case.
5. **`super()`/`this()` as constructor calls**: only inside a constructor,
   only as the first statement *(through Java 21 — see the modern-Java
   callout under Case 1)*, and only one of the two per constructor.
6. **`super`/`this` as keywords** behave completely differently from the
   constructor calls above: legal anywhere except a static context, and
   usable any number of times in one method or constructor.
7. **Since Java 25 (JEP 513, Flexible Constructor Bodies)**, a constructor
   may contain statements *before* its explicit `super(...)`/`this(...)`
   call, provided those statements never touch the instance being built (no
   `this`, no instance field/method, no `super` member access). This is the
   single biggest change to this lecture's content — know it as the modern
   answer, but know Sir's absolute "first statement, no exceptions" rule as
   the correct answer for any pre-25 source level, which is what OCJP and
   most production code still target.
8. **Three related but distinct compile errors**, easy to mix up under
   interview pressure: `call to super must be first statement in
   constructor` (wrong position, still a constructor), `call to this must
   be first statement in constructor` / `redundant explicit constructor
   invocation` (two constructor calls in one constructor), and `explicit
   constructor invocation may only appear within a constructor body` (used
   from a plain method, not a constructor at all).

---

**Next:** Video 066 — Overloaded constructors
