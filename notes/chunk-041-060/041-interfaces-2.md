# Video 041 — Interface Methods, Variables, and Naming Conflicts

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-12|| interfaces-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 41 of 203 |
| Series | Declarations and Access Modifiers · Part 12 |
| Topic | interfaces-2 (interface methods; continue from video 040) |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 15m 27s |
| Video ID | PS8gY5CXVY0 |
| Watch | https://www.youtube.com/watch?v=PS8gY5CXVY0 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Continuing straight from video 040 (what an interface is, `extends` vs
`implements`, syntax), this session works through:

1. Interface methods — why every one is `public abstract`, which modifiers are
   illegal, and the equivalence of every legal way to write the same method.
2. Interface variables — why every one is `public static final`, why
   `transient`/`volatile` don't apply, and why initialization is mandatory at
   declaration.
3. Interface naming conflicts — what happens when a class implements two
   interfaces that declare colliding methods (three cases) or colliding
   variables (one case, with a fix).

This is the **Java 1.4 / OCJP-era** interface story: every method is public +
abstract, every variable is public static final, full stop. Sir explicitly
does not teach Java 8 `default` / `static` interface methods here — that
context is added below in callouts, not in his board work. Marker interfaces,
adapter classes, and interface-vs-abstract-class are flagged as "next" but not
reached in this recording.

---

## 00:05 — Board heading: interface methods

Video 040 already started interfaces; this session picks up with **interface
methods**.

## 00:28 — Every method inside an interface is always public and abstract

**Board:**

> Every method present inside interface is always public and abstract, whether
> we are declaring or not.

Sir flags the interview trap directly: they won't just ask *what* the
modifiers are, they'll ask *why* — why always public, why always abstract.
Have both reasons ready, not a one-word answer.

```java
interface Inter {
    void m1();
    // compiler treats this as:
    // public abstract void m1();
}
```

### 02:08 — Why the method is always public

Who implements `m1()`? The **implementation class** — and that class may sit
in the **same package** or an **outside package**. To make the method
reachable from either, it has no choice but to be `public`.

```java
package p1;

public interface Inter {
    void m1(); // must be public so every impl can see it
}

package p1;

public class SamePack implements Inter {
    public void m1() {
        System.out.println("same package impl");
    }
}

package p2;

public class OtherPack implements p1.Inter {
    public void m1() {
        System.out.println("outside package impl");
    }
}
```

**Board:**

> To make this method available to every implementation class, compulsory
> this method should be public.

### 03:10 — Why the method is always abstract

An interface is a **requirement specification** — "this is the service I
want." The implementation class provides the service; the interface itself
never contains implementation.

```java
interface Inter {
    void m1();
    // no body — specification only
    // implementation class is responsible to provide implementation
}

class Test implements Inter {
    public void m1() {
        System.out.println("service implemented here");
    }
}
```

**Board:**

> Interface is a requirement specification. Implementation class is
> responsible to provide implementation. That is why the method should be
> abstract.

### 05:40 — Are these four declarations equal?

He puts four spellings of the same method on the board and asks whether they
are equal. They are — the compiler silently fills in whatever `public` /
`abstract` you left out.

| Written as | Compiler sees |
|---|---|
| `void m1();` | `public abstract void m1();` |
| `public void m1();` | `public abstract void m1();` |
| `abstract void m1();` | `public abstract void m1();` |
| `public abstract void m1();` | `public abstract void m1();` |

**Board:** *Hence inside interface the following method declarations are
equal.*

### 07:55 — Which modifiers become illegal, and why

If the method is always **public**, `private` and `protected` can never join
it — public and private/protected on the same member is a contradiction. If
the method is always **abstract**, none of the implementation-flavoured
modifiers can join it either: `static`, `final`, `synchronized`, `strictfp`,
`native`.

**Board:**

> As every interface method is always public and abstract, we can't declare
> interface method with the following modifiers: `private`, `protected`,
> `static`, `final`, `synchronized`, `strictfp`, `native`.

```java
interface Inter  { private void m1(); }       // CE: modifier private not allowed here
interface Inter2 { protected void m1(); }     // CE: modifier protected not allowed here
interface Inter3 { static void m1(); }        // CE: method m1() is missing a method body, or should be declared abstract
interface Inter4 { final void m1(); }         // CE: modifier final not allowed here
interface Inter5 { synchronized void m1(); }  // CE: modifier synchronized not allowed here
interface Inter6 { strictfp void m1(); }      // CE: modifier strictfp not allowed here
interface Inter7 { native void m1(); }        // CE: modifier native not allowed here

interface Inter8 {
    public abstract void m1(); // only this family is legal, Java 6/7 rules
}
```

> ⚠️ **Modern Java — three of these seven bans have real exceptions today.**
> This list is exactly right for the Java 1.4–7 interface Sir is teaching, and
> it is still the OCJP answer. Since then:
>
> - **`static`** — legal from **Java 8**, but only with a body (it is a
>   utility method callable as `Inter.m1()`, not inherited by implementers):
>   `static void m1() { }` compiles; `static void m1();` still fails with
>   *"missing a method body, or should be declared abstract"* — the modifier
>   itself is no longer the problem, the missing body is.
> - **`private`** — legal from **Java 9**, again only with a body. It is a
>   helper callable only from other methods in the same interface, used to
>   share code between `default` methods without exposing it:
>   `private void m1() { }` compiles.
> - **`strictfp`** — since **Java 17** it is a no-op on any method that *has*
>   a body (`javac` just warns: *"all floating-point expressions are evaluated
>   strictly and 'strictfp' is not required"*). On a bare abstract method with
>   no body it is still a flat compile error, same as Sir shows.
>
> Verified with `javac 26 --release` across versions. **`protected`,
> `final`, `synchronized`, and `native` are unaffected** — they are illegal on
> an interface method in Java 6/7 and remain illegal on every kind of
> interface method (abstract, default, static, or private) today. Only
> `static` and `private` moved from "always illegal" to "illegal only without
> a body."

### 11:09 — BIT: which method declarations are allowed inside an interface?

```java
interface Inter { public void m1() { } }               // (1)
interface Inter { private void m1(); }                  // (2)
interface Inter { protected void m1(); }                // (3)
interface Inter { static void m1(); }                   // (4)
interface Inter { public abstract native void m1(); }   // (5)
interface Inter { abstract public void m1(); }          // (6)
```

### 13:06 — Answers

| # | Declaration | Verdict | Why |
|---|---|---|---|
| 1 | `public void m1() { }` | ❌ invalid | an abstract method must end with `;` — no body allowed |
| 2 | `private void m1();` | ❌ invalid | `private` not allowed on a bare (no-body) method |
| 3 | `protected void m1();` | ❌ invalid | `protected` not allowed |
| 4 | `static void m1();` | ❌ invalid | `static` needs a body |
| 5 | `public abstract native void m1();` | ❌ invalid | `native` not allowed |
| 6 | `abstract public void m1();` | ✅ valid | modifier **order doesn't matter** — same as `public abstract` |

That finishes interface methods.

---

## 13:39 — Board heading: interface variables

An interface **can contain variables** — the next question is why it would
need to.

### 14:01 — Why: requirement-level constants (college automation example)

Sir's running example: a requirement spec says *"implement a College
Automation system — wherever college name is needed, use `DurgaSoft`;
wherever location is needed, use `Hyderabad`."* Those are values the
requirement itself fixes, independent of who implements it. The way to pin
them down is to declare them as **interface variables**.

```java
interface CollegeAutomation {
    String COLLEGE_NAME = "DurgaSoft";
    String LOCATION = "Hyderabad";

    void m1();
    void m2();
    void m3();
    void m4();
}

class CollegeAutomationImpl implements CollegeAutomation {
    public void m1() {
        System.out.println(COLLEGE_NAME); // prints DurgaSoft
    }

    public void m2() {
        System.out.println(LOCATION); // prints Hyderabad
    }

    public void m3() { }
    public void m4() { }
}
```

**Board:**

> An interface can contain variables. The main purpose of interface variable
> is to define requirement-level constants.

### 16:58 — Every interface variable is always public static final

Whether declared with those modifiers or not.

### 17:18 — Why always public

Who uses the variable? The **implementation class**, which may sit in any
package. So, exactly as with methods, it must be public to reach all of them.

```java
package p1;

public interface Inter {
    int x = 10; // public so every impl can see it
}

package p2;

class Test implements p1.Inter {
    public static void main(String[] args) {
        System.out.println(x); // prints 10
    }
}
```

**Board:** *To make this variable available to every implementation class,
this variable is always public.*

### 18:29 — Why always static

You cannot create an object for an interface. Without an object, the
implementation class still needs to reach the variable — and accessing
something with no object in hand is exactly what `static` is for.

```java
interface Inter { int x = 10; }

class Test implements Inter {
    public static void main(String[] args) {
        // Inter i = new Inter();
        // CE: Inter is abstract; cannot be instantiated

        System.out.println(Inter.x); // static access, no object — prints 10
        System.out.println(x);       // inherited static final — prints 10
    }
}
```

**Board:** *Without existing object, implementation class can access this
variable. That's why it should be static.*

### 19:39 — Why always final (the JDBC angle)

Not the simple why — the real one. JDBC's API is defined once, but
**multiple vendors** (IBM, MySQL, and others) each ship an implementation. If
one vendor's implementation class could change a shared constant, every other
vendor's class — for whom the variable is the same static field — would feel
the change. `final` is what stops that.

```java
interface Driver {
    int x = 10; // public static final — common to every vendor impl
}

class IbmDriver implements Driver {
    public static void main(String[] args) {
        // x = 20;
        // CE: cannot assign a value to final variable x
        System.out.println(x); // prints 10
    }
}

class MySqlDriver implements Driver {
    public static void main(String[] args) {
        System.out.println(x); // prints 10 — one vendor can't change it for the rest
    }
}
```

**Board:** *If one implementation class changes value, then remaining
implementation classes will be affected. To restrict this, every interface
variable is always final.*

### 22:23 — Recap: `int x = 10` with all three reasons

```java
interface Inter {
    int x = 10;
    // public  — to make this variable available to every implementation class
    // static  — without existing object also, implementation class has to access this variable
    // final   — if one implementation class changes value, remaining implementation
    //           classes will be affected; to restrict this, always final
}
```

Implementation classes **access**, never **modify**.

### 25:54 — Are all these variable declarations equal?

Same drill as the method version — eight ways to write the same field, all
equivalent once the compiler fills in what's missing:

| Written as | Compiler sees |
|---|---|
| `int x = 10;` | `public static final int x = 10;` |
| `public int x = 10;` | same |
| `static int x = 10;` | same |
| `final int x = 10;` | same |
| `public static int x = 10;` | same |
| `public final int x = 10;` | same |
| `static final int x = 10;` | same |
| `public static final int x = 10;` | same |

**Board:** *Hence within the interface the following variable declarations
are equal.*

### 28:21 — Which modifiers are not applicable, and why

Since the variable is always public, static, and final:

- **`private` / `protected`** — contradict "always public"; not applicable.

### 29:06 — Why `transient` doesn't apply

You cannot instantiate an interface. No object means no state to save, and
`transient` exists to exclude a field from **serialization** of an object's
state. No object, no serialization, no need for `transient`.

```java
interface Inter {
    transient int x = 10;
    // CE: modifier transient not allowed here
}
```

### 29:43 — Why `volatile` doesn't apply

`final` + `volatile` is already an illegal combination for *any* variable
(covered in an earlier session on variable types) — one guarantees the value
never changes, the other exists to manage changing values across threads.
Since every interface variable is implicitly `final`, `volatile` is
automatically out.

```java
interface Inter {
    volatile int x = 10;
    // CE: modifier volatile not allowed here
    // (also: illegal combination with implicit final)
}
```

**Board:**

> As every interface variable is always public static final, we can't declare
> with the following modifiers: `private`, `protected`, `transient`,
> `volatile`.

```java
interface Inter  { private int x = 10; }    // CE: modifier private not allowed here
interface Inter2 { protected int x = 10; }  // CE: modifier protected not allowed here
interface Inter3 { transient int x = 10; }  // CE: modifier transient not allowed here
interface Inter4 { volatile int x = 10; }   // CE: modifier volatile not allowed here
```

### 31:54 — Final-static initialization, and interfaces have no static block

Recap of the general rule for `final static` fields: initialization must
happen **before class-loading completes**, and there are exactly two places
that can happen — at the point of declaration, or inside a `static` block:

```java
class Demo {
    static final int x = 10; // option 1: at declaration

    static final int y;
    static {
        y = 20; // option 2: static block, before class-loading completes
    }
}
```

An **interface cannot have a static block** — no static block, no instance
block, no constructor. That removes option 2 entirely, so for interface
variables option 1 is the *only* option: initialize at declaration or don't
compile.

```java
interface Inter {
    int x = 10;

    // static { x = 10; }
    // CE: initializers not allowed in interfaces
}
```

### 34:26 — Demo: `int x;` with no initializer

```java
interface Inter {
    int x;
    // CE: '=' expected
}
```

The compiler stops right after `x`, expecting `=`. Writing just the `=` with
nothing after it fails differently:

```java
interface Inter {
    int x =;
    // CE: illegal start of expression
}
```

Only `int x = 10;` compiles.

**Board:** *For interface variables, compulsory we should perform
initialization at the time of declaration. Otherwise we will get
compile-time error.*

### 37:36 — BIT: which variable declarations are allowed inside an interface?

```java
interface Inter { int x; }                          // (1)
interface Inter { private int x = 10; }              // (2)
interface Inter { protected int x = 10; }            // (3)
interface Inter { volatile transient int x = 10; }   // (4)
interface Inter { public static int x = 10; }        // (5)
```

### 39:06 — Answers

| # | Declaration | Verdict | Why |
|---|---|---|---|
| 1 | `int x;` | ❌ invalid | no initializer — `=` expected |
| 2 | `private int x = 10;` | ❌ invalid | `private` not allowed |
| 3 | `protected int x = 10;` | ❌ invalid | `protected` not allowed |
| 4 | `volatile transient int x = 10;` | ❌ invalid | neither modifier is allowed |
| 5 | `public static int x = 10;` | ✅ valid | implicitly `final` too — same as `public static final int x = 10;` |

### 39:39 — Access vs. modify in the implementation class

Two versions of `class Test implements Inter`, side by side.

**Case A — assigning to the inherited `x` fails:**

```java
interface Inter { int x = 10; }

class Test implements Inter {
    public static void main(String[] args) {
        x = 777;
        System.out.println(x);
        // CE: cannot assign a value to final variable x
    }
}
```

**Case B — declaring a *new local* `x` succeeds, and prints 777:**

```java
interface Inter { int x = 10; }

class Test implements Inter {
    public static void main(String[] args) {
        int x = 777; // a fresh local variable, unrelated to Inter.x
        System.out.println(x); // prints 777
    }
}
```

The two `x`s are unrelated: Case A reassigns the inherited interface constant
(illegal — it's `final`), Case B *shadows* it with a brand-new local variable
(legal — locals aren't constants).

**Board:** *Inside implementation class we can access interface variables,
but we can't modify values.*

---

## 45:24 — Bridge: recap of video 040, and what's left

Video 040 covered: what an interface is, how to declare one, how to provide
an implementation, `extends` vs `implements`, syntax issues, then this
video's postmortem on methods and variables. Still to come in this session:
**interface naming conflicts** (method-level, then variable-level) — after
that, later videos take on marker interfaces, adapter classes, and
interface-vs-abstract-class-vs-concrete-class.

## 46:24 — Interface naming conflicts: method naming conflicts

Before starting, Sir plants a claim to test later: **a Java class can
implement any number of interfaces.** True — hold that answer, it's about to
get a wrinkle.

### 47:28 — Case 1: same signature, same return type — one method is enough

```java
interface Left  { public void m1(); }
interface Right { public void m1(); }

class Test implements Left, Right {
    public void m1() {
        System.out.println("one implementation serves both");
    }

    public static void main(String[] args) {
        Test t = new Test();
        Left l = t;
        Right r = t;
        l.m1(); // prints one implementation serves both
        r.m1(); // prints one implementation serves both
    }
}
```

Both interfaces ask for the identical `public void m1()`. One implementation
satisfies both requirements — there is no conflict to resolve. If the two
callers actually wanted *different* behavior, the fix is different classes,
not one class trying to be two things:

```java
class LeftImpl implements Left {
    public void m1() { System.out.println("left only"); }
}

class RightImpl implements Right {
    public void m1() { System.out.println("right only"); }
}
```

**Board:** *If two interfaces contain a method with the same signature and
the same return type, then in the implementation class we have to provide
implementation for only one method.*

> ⚠️ **Modern Java — this exact case gets harder if the methods are `default`.**
> Sir's `m1()` here is a plain abstract method, so "one implementation is
> enough" is correct and unaffected by anything since. But if `Left.m1()` and
> `Right.m1()` were both **Java 8 `default` methods** with the *same*
> signature, the compiler refuses to pick one for you:
>
> ```java
> interface Left  { default void m1() { System.out.println("left"); } }
> interface Right { default void m1() { System.out.println("right"); } }
>
> class Test implements Left, Right { }
> // CE: types Left and Right are incompatible;
> //     class Test inherits unrelated defaults for m1() from types Left and Right
> ```
>
> This is the classic "diamond problem" for default methods: Java requires
> `Test` to override `m1()` itself and explicitly say which (or write new
> behavior), e.g. `public void m1() { Left.super.m1(); }`. Verified with
> `javac 26`. The lecture's abstract-method version has no such ambiguity —
> only default methods can collide this way.

### 52:46 — Case 2: same name, different argument types — both are kept, as overloads

```java
interface Left  { public void m1(); }
interface Right { public void m1(int i); }

class Test implements Left, Right {
    public void m1() {
        System.out.println("no-arg");
    }

    public void m1(int i) {
        System.out.println(i);
    }

    public static void main(String[] args) {
        Test t = new Test();
        t.m1();   // prints no-arg
        t.m1(10); // prints 10
    }
}
```

Different argument types mean these are different methods by signature, so
both need an implementation — and the pair is, by definition, **overloaded**.

**Board:** *If two interfaces contain a method with the same name but
different argument types, then in the implementation class we have to
provide implementation for both methods, and these methods act as overloaded
methods.*

### 57:42 — Case 3: same signature, different return types — impossible

```java
interface Left  { public void m1(); }
interface Right { public int m1(); }

class Test implements Left, Right {
    public void m1() { }
    public int m1() { return 10; }
    // CE: m1() is already defined in Test
}
```

`void` and `int` are not covariant, and within one class two methods can't
share a signature — the second declaration collides with the first outright.

Splitting the two implementations across a parent/child pair doesn't rescue
it either:

```java
abstract class Test implements Left, Right {
    public void m1() { }
}

class SubTest extends Test {
    public int m1() { return 10; }
    // CE: m1() in SubTest cannot override m1() in Test
    //   attempting to assign incompatible return type
    //   found: int, required: void
}
```

Parent and child sharing a signature is **overriding**, and overriding
requires the same return type — `void` in the parent forces `void` in the
child, so this fails too. Nor does moving one implementation into an inner
class help; that's just two separate classes again, not one class
implementing both interfaces simultaneously.

**The real answer:** it is impossible to implement both interfaces at once —
*unless* the return types are **covariant** (Java 5+). `Object` in one and
`String` in the other works, because `String` can stand in for `Object`:

```java
interface Left  { public Object m1(); }
interface Right { public String m1(); }

class Test implements Left, Right {
    public String m1() { return "durga"; }

    public static void main(String[] args) {
        System.out.println(new Test().m1()); // prints durga
    }
}
```

`void` vs. `int` have no such relationship, so that pair stays impossible.

**Board (interview form):**

> Is a Java class can implement any number of interfaces simultaneously?
> **Answer: Yes, except a particular case** — if two interfaces contain a
> method with the same signature but different (non-covariant) return types,
> it is impossible to implement both simultaneously. (Covariant returns:
> Java 1.5 onwards.)

Interface **method** naming conflicts: done.

---

## 1:08:56 — Interface variable naming conflicts

### 1:09:32 — Two interfaces, same variable name, different value

```java
interface Left  { int x = 777; }
interface Right { int x = 888; }

class Test implements Left, Right {
    public static void main(String[] args) {
        System.out.println(x);
        // CE: reference to x is ambiguous
    }
}
```

Unqualified `x` could mean either interface's constant — the compiler refuses
to guess.

### 1:11:25 — Fix: qualify with the interface name

Every interface variable is `static`, so it's reachable by name the way any
static field is — through the type that declares it:

```java
interface Left  { int x = 777; }
interface Right { int x = 888; }

class Test implements Left, Right {
    public static void main(String[] args) {
        System.out.println(Left.x);  // prints 777
        System.out.println(Right.x); // prints 888
    }
}
```

**Board:** *Two interfaces can contain a variable with the same name, and
there may be a chance of variable naming conflicts, but we can solve this
problem by using interface names.*

### 1:13:52 — Method conflicts vs. variable conflicts

The asymmetry to remember: **method** naming conflict Case 3 (same signature,
non-covariant return types) has **no solution** — the class genuinely cannot
be written. **Variable** naming conflicts always have a solution — qualify
with the interface name.

---

## Exam and interview points

1. **Interface methods are always `public abstract`**, whether written that
   way or not; order of modifiers never matters (`abstract public` ==
   `public abstract`). Illegal companions: `private`, `protected`, `static`,
   `final`, `synchronized`, `strictfp`, `native` — for the *pre-Java-8, no-body*
   method this lecture teaches. Modern Java lets `static` (8) and `private` (9)
   join once the method has a body; `protected`, `final`, `synchronized`,
   `native` never do.
2. **Interface variables are always `public static final`**, must be
   initialized at declaration (interfaces have no static block), and an
   implementation class can access but never reassign one.
3. **`transient` and `volatile` never apply to interface variables** — no
   object means no serialization to exclude from, and `final` already rules
   out `volatile`.
4. **Method naming conflict, same signature + same return type:** one shared
   implementation covers both interfaces. (Only true for abstract methods —
   two colliding Java 8 `default` methods force an explicit override instead.)
5. **Method naming conflict, same name + different arguments:** both methods
   must be implemented; they become overloads.
6. **Method naming conflict, same signature + different return types:**
   impossible to implement both interfaces at once, unless the return types
   are covariant (Java 5+). This one case has no workaround.
7. **Variable naming conflict, same name in two interfaces:** always
   resolvable — qualify with `InterfaceName.field`.
8. **A class can implement any number of interfaces** — true as a general
   rule, with exactly the one exception above (method Case 3).

---

**Next:** Video 042 — Marker interface (and related board work)
