# Video 056 — Overriding and access modifiers

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-6 ||overriding ||access modifiers

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 56 of 203 |
| Series | OOPs · Part 6 |
| Topic | overriding, access modifiers |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 23m 45s |
| Video ID | 1By_hC3ONt8 |
| Watch | https://www.youtube.com/watch?v=1By_hC3ONt8 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is OOPs Part 6, continuing straight from Part 5's overriding rules. Sir
covers, in order: **why** you can't reduce an overridden method's access
scope (the previous video only stated the rule), the **checked-exception
overriding rule** (seven board cases plus a live `javac` run), a recap of
**every overriding rule so far**, then **static methods** — you cannot mix
static and non-static across an override, both-static compiles but is
**method hiding** rather than overriding, and a hiding-vs-overriding demo
(`parent child parent` vs `parent child child`) with a comparison table. The
video closes with the board-vs-chart story for why the two behaviours got
different names, and a heading-only preview of the next topic: overriding
with respect to var-arg methods.

---

## 00:05 — Recap: last session ended on the access-modifier rule

Part 5 ended with the rule: while overriding, **you cannot reduce the scope
of the access modifier**. If the parent method is `public`, the child
override must be `public` too.

```java
class P {
    public void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    // child MUST stay public if this is an override
    public void m1() {
        System.out.println("child");
    }
}

class AccessRecapOk {
    public static void main(String[] args) {
        P p = new C();
        p.m1();
        // prints child
    }
}
```

Reducing `public` to default is the illegal move Sir is about to motivate:

```java
class P {
    public void m1() { }
}

class C extends P {
    void m1() { } // default — weaker than public
}
// CE: m1() in C cannot override m1() in P
// attempting to assign weaker access privileges; was public
```

### 01:00 — Internal reason: parent `public void m1()`, child does not override yet

A parent reference can hold a child object:

```java
class P {
    public void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    // did not override
}

class OutsideCaller {
    public static void main(String[] args) {
        P p = new C(); // parent reference, child object
        p.m1();
        // prints parent — child did not override, so parent method executes
    }
}
```

`m1` is `public`, so outside callers — in this package and in others — can
already call it through exactly this pattern. Sir's number for the size of
that crowd: **about 100 outside people** are calling `m1` this way.

### 02:38 — Tomorrow you override and reduce the modifier to default

Those 100 callers are already using `p.m1()`. Now suppose you override in
the child and drop `public` to default:

```java
class P {
    public void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    void m1() { // default — reduced
        System.out.println("child");
    }
}
// CE: m1() in C cannot override m1() in P
// attempting to assign weaker access privileges; was public
```

If Java allowed this, the runtime object behind every one of those 100
`P p = new C()` callers is `C`, so the **child** method would now run for
all of them — and the child method is default: current-package only.
Everyone calling from outside the package would break, with a compile error
or a runtime access failure depending on how they wrote the call.

**Minimum thumb rule: our overriding must not affect outside people.**
Without the override, several outside callers could reach the method; after
overriding, that same set must still be able to reach it. Gaining *more*
callers is fine — a bonus. Losing any of the callers who already worked is
not. Reducing `public` to default loses callers, so it's invalid.

### 05:47 — Parent default: same default is OK; increasing to public is OK

If the parent `m1` is default, only same-package callers exist in the first
place. A default override keeps that same set — fine. A `public` override
keeps that set **and** adds outside-package callers — also fine, because
that's strictly more access, never less.

```java
class P {
    void m1() { // default
        System.out.println("parent");
    }
}

class C extends P {
    void m1() { // same default — same callers still work
        System.out.println("child");
    }
}

class SamePackageOk {
    public static void main(String[] args) {
        P p = new C();
        p.m1();
        // prints child
    }
}
```

```java
class P {
    void m1() { // default
        System.out.println("parent");
    }
}

class C extends P {
    public void m1() { // increased to public — extra callers allowed
        System.out.println("child");
    }
}

class IncreaseScopeOk {
    public static void main(String[] args) {
        P p = new C();
        p.m1();
        // prints child
    }
}
```

**You can increase the scope while overriding, but you cannot decrease it** —
because decreasing can strand outside callers who were already relying on
the wider parent-reference access.

That closes the access-modifier rule.

---

## 07:01 — Next rule needs checked vs unchecked exceptions

Sir assumes you already know checked vs unchecked exceptions (that's an
interview-room staple he'll cover properly in the exceptions chapter, not
here) — but the next overriding rule depends on being able to sort one from
the other on sight.

### 07:39 — Exception hierarchy on the board

`Throwable` is the root of the exception hierarchy, with two children:
`Exception` and `Error`.

```text
Throwable
├── Exception
│   ├── RuntimeException
│   │   ├── NullPointerException
│   │   ├── ClassCastException
│   │   ├── ArithmeticException
│   │   └── …
│   ├── IOException
│   │   ├── FileNotFoundException
│   │   ├── EOFException
│   │   └── …
│   ├── InterruptedException
│   ├── ServletException
│   └── …
└── Error
    └── VirtualMachineError
        ├── OutOfMemoryError
        ├── StackOverflowError
        └── …
```

> ❗ **Correction — `RemoteException` is not a direct child of `Exception`.**
> Sir lists `RemoteException` alongside `IOException` as if both sit directly
> under `Exception`. In the real JDK, `java.rmi.RemoteException` **extends
> `java.io.IOException`**, so it belongs one level deeper, under `IOException`,
> not beside it:
>
> ```text
> public class java.rmi.RemoteException extends java.io.IOException
> ```
>
> This doesn't change anything Sir concludes — `RemoteException` is still a
> checked exception either way, and it never appears in the seven worked
> cases below — but the diagram as drawn misplaces it.

### 09:57 — Thumb rule: what is unchecked; everything else is checked

**Unchecked:** `RuntimeException` and its subclasses, `Error` and its
subclasses. **Everything else is, by default, a checked exception.**

Sir quizzes the class through the list:

| Type | Checked or unchecked |
|---|---|
| `Throwable` | checked |
| `Exception` | checked |
| `IOException` | checked |
| `FileNotFoundException` | checked |
| `EOFException` | checked |
| `InterruptedException` | checked (parent is `Exception`) |
| `ArithmeticException` | unchecked |
| `NullPointerException` | unchecked |
| `ClassCastException` | unchecked |
| `RuntimeException` | unchecked |
| `Error` | unchecked |
| `VirtualMachineError` | unchecked |
| `OutOfMemoryError` | unchecked |

Two parent relationships worth pinning down, because the next rule leans on
them: `EOFException` and `FileNotFoundException` both descend from
`IOException`; `InterruptedException` descends from `Exception` directly —
**not** from `IOException`.

```java
class IdentifyChecked {
    void checked() throws Throwable, Exception, java.io.IOException,
            java.io.FileNotFoundException, java.io.EOFException,
            InterruptedException { }

    void unchecked() throws RuntimeException, ArithmeticException,
            NullPointerException, ClassCastException, Error,
            VirtualMachineError, OutOfMemoryError { }
}
```

---

## 12:11 — Seven board cases: decide valid or invalid before the rule

Sir gives seven examples before stating the rule, to test intuition first.
Every method is `public void m1()`; only the `throws` clause changes.

### 13:04 — Case 1: parent throws `Exception`, child throws nothing

```java
class P {
    public void m1() throws Exception { }
}

class C extends P {
    public void m1() { } // no throws
}
// valid
```

### 13:23 — Case 2: parent throws nothing, child throws `Exception`

```java
class P {
    public void m1() { }
}

class C extends P {
    public void m1() throws Exception { }
}
// CE: m1() in C cannot override m1() in P
// overridden method does not throw java.lang.Exception
```

### 13:50 — Case 3: parent throws `Exception`, child throws `IOException`

```java
import java.io.IOException;

class P {
    public void m1() throws Exception { }
}

class C extends P {
    public void m1() throws IOException { }
}
// valid
```

### 14:19 — Case 4: parent throws `IOException`, child throws `Exception`

```java
import java.io.IOException;

class P {
    public void m1() throws IOException { }
}

class C extends P {
    public void m1() throws Exception { }
}
// CE: m1() in C cannot override m1() in P
// overridden method does not throw java.lang.Exception
```

`IOException` is the child type here, `Exception` the parent — the reverse
of case 3.

### 14:52 — Case 5: parent throws `IOException`, child throws `FileNotFoundException`, `EOFException`

```java
import java.io.EOFException;
import java.io.FileNotFoundException;
import java.io.IOException;

class P {
    public void m1() throws IOException { }
}

class C extends P {
    public void m1() throws FileNotFoundException, EOFException { }
}
// valid — both are children of IOException
```

### 15:50 — Case 6: parent throws `IOException`, child throws `EOFException`, `InterruptedException`

```java
import java.io.EOFException;
import java.io.IOException;

class P {
    public void m1() throws IOException { }
}

class C extends P {
    public void m1() throws EOFException, InterruptedException { }
}
// CE: m1() in C cannot override m1() in P
// overridden method does not throw java.lang.InterruptedException
```

`EOFException` sits under `IOException`, so that half is fine.
`InterruptedException` does not, so this half breaks the override.

### 16:49 — Case 7: parent throws `IOException`, child throws three unchecked types

```java
import java.io.IOException;

class P {
    public void m1() throws IOException { }
}

class C extends P {
    public void m1() throws ArithmeticException, NullPointerException, ClassCastException { }
}
// valid — unchecked; no comparison required
```

### 17:32 — The board answers, given before the rule

| Case | Parent throws | Child throws | Valid? |
|---|---|---|---|
| 1 | `Exception` | (none) | valid |
| 2 | (none) | `Exception` | invalid |
| 3 | `Exception` | `IOException` | valid |
| 4 | `IOException` | `Exception` | invalid |
| 5 | `IOException` | `FileNotFoundException`, `EOFException` | valid |
| 6 | `IOException` | `EOFException`, `InterruptedException` | invalid |
| 7 | `IOException` | `ArithmeticException`, `NullPointerException`, `ClassCastException` | valid |

Sir writes all seven verdicts on the board before explaining why, deliberately
alternating valid/invalid/valid/invalid/valid/invalid/valid — and confirms
every one is correct as written, resisting the class's guesses that 4 or 7
might be typos.

### 20:55 — The rule

**If the child method throws any checked exception, the parent method must
throw that same checked exception or one of its parents — otherwise it's a
compile-time error.** If the parent throws nothing at all but the child
throws a checked exception, that alone is enough for the error.

**Unchecked exceptions carry no restriction at all.** Parent and child can
each throw any number of unchecked types; there's no comparison to make. The
rule exists only for checked exceptions.

### 24:22 — Applying the rule to all seven

- **Case 1:** child throws no checked exception at all. Nothing to check. Valid.
- **Case 2:** child throws checked `Exception`; parent throws nothing. Invalid.
- **Case 3:** child throws `IOException`; parent throws `Exception`, which is
  `IOException`'s parent. Valid.
- **Case 4:** child throws `Exception`; parent throws `IOException`, which is
  `Exception`'s **child**, not its parent or itself. Invalid.
- **Case 5:** child throws `FileNotFoundException`; parent throws `IOException`,
  its parent. Valid.
- **Case 6:** child's `EOFException` is fine against parent `IOException`, but
  child's `InterruptedException` has no matching parent throw. Invalid.
- **Case 7:** all three child exceptions are unchecked. Nothing to check. Valid.

### 27:01 — Live compile of case 6; exact compiler message

Terminology Sir wants copied down: the **parent** method is the **overridden**
method; the **child** method is the **overriding** method.

```java
import java.io.*;

class P {
    public void m1() throws IOException { }
}

class C extends P {
    public void m1() throws EOFException, InterruptedException { }
}
// CE: m1() in C cannot override m1() in P
// overridden method does not throw java.lang.InterruptedException
```

### 30:29 — Same case 6, three follow-up tweaks

**Fix 1:** parent also throws `InterruptedException` → valid.

```java
import java.io.*;

class P {
    public void m1() throws IOException, InterruptedException { }
}

class C extends P {
    public void m1() throws EOFException, InterruptedException { }
}
// valid
```

**Fix 2:** parent throws `Exception`, the parent of both checked types → valid.

```java
import java.io.*;

class P {
    public void m1() throws Exception { }
}

class C extends P {
    public void m1() throws EOFException, InterruptedException { }
}
// valid
```

**Still invalid:** parent throws nothing at all, child still throws a checked type.

```java
import java.io.*;

class P {
    public void m1() { }
}

class C extends P {
    public void m1() throws EOFException, InterruptedException { }
}
// CE: m1() in C cannot override m1() in P
// overridden method does not throw java.io.EOFException
```

---

## 38:51 — Internal reason for the exception rule

Same shape of argument as the access-modifier reason. If a method throws a
checked exception, its **caller is responsible for handling it** — `try`/
`catch`, or propagating with `throws`. Skip that and it's a compile error.

```java
import java.io.IOException;

class P {
    public void m1() throws IOException { }
}

class C extends P { }

class CallerHandlesIo {
    public static void main(String[] args) {
        P p = new C();
        try {
            p.m1();
        } catch (IOException e) {
            // thousands of outside people already catch IOException
        }
    }
}
```

Thousands of outside callers of this public `m1` already handle
`IOException`, because that's what the parent method throws. Override with
the same `IOException` and nothing changes for them:

```java
import java.io.IOException;

class P {
    public void m1() throws IOException { }
}

class C extends P {
    public void m1() throws IOException { } // same checked — callers already catch IOException
}

class StillOk {
    public static void main(String[] args) throws IOException {
        P p = new C();
        p.m1();
    }
}
```

But override with the broader `Exception` instead, and the method that now
actually runs for those callers throws something they never wrote a `catch`
for. Their code stops compiling — the override reached outside its own
class and broke callers it had no business touching:

```java
import java.io.IOException;

class P {
    public void m1() throws IOException { }
}

class C extends P {
    public void m1() throws Exception { } // raised checked level
}
// CE: m1() in C cannot override m1() in P
// overridden method does not throw java.lang.Exception
```

So if the parent throws `IOException`, the child at override time may take:
the **same** `IOException`, **a child of it** (`EOFException`,
`FileNotFoundException`, …), or **no `throws` at all**. What it may never do
is **raise** the checked level — existing callers only prepared to handle up
to the parent's declared exception.

```java
import java.io.EOFException;
import java.io.FileNotFoundException;
import java.io.IOException;

class P {
    public void m1() throws IOException { }
}

class C1 extends P {
    public void m1() throws IOException { } // same — OK
}

class C2 extends P {
    public void m1() throws EOFException { } // child of IOException — OK
}

class C3 extends P {
    public void m1() throws FileNotFoundException { } // child of IOException — OK
}

class C4 extends P {
    public void m1() { } // no throws — OK
}
```

**Conclusion, same rule:** if the child throws any checked exception, the
parent must throw that same checked exception or its parent, or it's a
compile error. No restriction for unchecked exceptions.

---

## 44:48 — Recap: all overriding rules covered so far

1. **Signatures must match.** Same method name, same argument types.

   ```java
   class P {
       public void m1(int x) { }
   }

   class C extends P {
       public void m1(int x) { } // same name + same args = override
   }

   class NotOverride {
       public void m1(int x) { }
   }

   class OverloadInstead extends NotOverride {
       public void m1(String s) { } // different args — overloading, not overriding
   }
   ```

2. **Return types must match — until 1.4.** From **1.5 onward, covariant
   return types** are allowed.

   ```java
   class P {
       public Object m1() {
           return null;
       }
   }

   class C extends P {
       public String m1() { // covariant return (1.5+)
           return "child";
       }
   }

   class CovariantDemo {
       public static void main(String[] args) {
           P p = new C();
           System.out.println(p.m1());
           // prints child
       }
   }
   ```

3. **Private methods are not overridden.** A parent's private methods aren't
   visible to the child, so overriding doesn't apply to them. Defining the
   same private method in the child compiles fine — it's just a separate,
   unrelated private method.

   ```java
   class P {
       private void m1() {
           System.out.println("parent private");
       }
   }

   class C extends P {
       private void m1() { // not overriding — just another private method
           System.out.println("child private");
       }
   }

   class PrivateNotOverride {
       public static void main(String[] args) {
           C c = new C();
           // c.m1();
           // CE: m1() has private access in C
       }
   }
   ```

4. **`final` methods cannot be overridden.**

   ```java
   class P {
       public final void m1() { }
   }

   class C extends P {
       public void m1() { }
   }
   // CE: m1() in C cannot override m1() in P
   // overridden method is final
   ```

5. **Abstract methods can be overridden** (that's how they get implemented).

   ```java
   abstract class P {
       public abstract void m1();
   }

   class C extends P {
       public void m1() {
           System.out.println("implemented");
       }
   }

   class AbstractOverrideDemo {
       public static void main(String[] args) {
           P p = new C();
           p.m1();
           // prints implemented
       }
   }
   ```

6. **`synchronized`, `strictfp`, `native` keep no restriction** on overriding
   either way.

   ```java
   class P {
       public synchronized void m1() { }
   }

   class C extends P {
       public void m1() { } // synchronized not required on the child
   }

   class StrictFpOk {
       public strictfp void m1() { }
   }

   class StrictFpChild extends StrictFpOk {
       public void m1() { } // strictfp not required
   }
   ```

   > ⚠️ **Modern Java — `strictfp` is now a no-op.**
   > Since **Java 17** (JEP 306) all floating-point arithmetic is strict by
   > default, which is what `strictfp` used to opt into. It still parses and
   > still compiles here, but changes nothing, and `javac` says so directly:
   >
   > ```text
   > warning: [strictfp] as of release 17, all floating-point expressions are
   > evaluated strictly and 'strictfp' is not required
   > ```
   >
   > Sir's point — that it imposes no override restriction — is still true.
   > It's just that today the keyword itself does nothing.

7. **Access modifiers cannot be reduced, only increased.** `public` → `public`;
   `protected` → `protected` or `public`. (This video's first half.)

   ```java
   class P {
       protected void m1() { }
   }

   class C extends P {
       public void m1() { } // protected → public: increased — OK
   }

   class IncreaseProtected {
       public static void main(String[] args) {
           P p = new C();
           p.m1();
       }
   }
   ```

   ```java
   class P {
       protected void m1() { }
   }

   class C extends P {
       void m1() { } // protected → default: reduced
   }
   // CE: m1() in C cannot override m1() in P
   // attempting to assign weaker access privileges; was protected
   ```

8. **Checked exceptions cannot be raised.** If the child throws any checked
   exception, the parent must throw that same checked exception or its
   parent. No restriction for unchecked exceptions. (This video's second
   half.)

> ⚠️ **Modern Java — default and static interface methods add two more
> corners to this list.**
> None of the eight rules above changed, but Java 8 added method bodies to
> interfaces, which interact with overriding in ways worth knowing:
>
> - A **default method** (`default void m2() { … }`) behaves like any other
>   inherited instance method for these purposes — a class can override it,
>   and the usual rules apply.
> - A **static interface method** cannot be overridden or hidden at all —
>   it isn't even inherited by implementing classes. `I.m1()` must be called
>   through the interface name; `C.m1()` fails to resolve even when `C
>   implements I`:
>
>   ```java
>   interface I {
>       static void m1() { System.out.println("interface static"); }
>       default void m2() { System.out.println("interface default"); }
>   }
>   class C implements I { }
>   class Demo {
>       public static void main(String[] args) {
>           new C().m2();  // OK — default methods are inherited
>           I.m1();        // must call through the interface
>           // C.m1();     // CE: cannot find symbol — static methods are not inherited
>       }
>   }
>   ```

---

## 46:39 — Overriding with respect to static methods

Sir flagged the `static` modifier as deferred from the modifier summary in
the last video, because — unlike `synchronized`, `native`, and `strictfp` —
it comes with real rules.

### 47:15 — Case 1: parent `static`, child non-static — invalid

```java
class P {
    public static void m1() { }
}

class C extends P {
    public void m1() { } // static overridden as non-static
}
// CE: m1() in C cannot override m1() in P
// overridden method is static
```

**Why:** a static method is a **class-level** method; an instance method is
an **object-level** method. You can't override one with the other. Sir's
analogy: a faculty member leaves, so you look for another faculty member to
fill the seat — you don't recruit a student for a faculty role. Different
levels, not interchangeable.

### 52:46 — Case 2: parent non-static, child static — also invalid

```java
class P {
    public void m1() { }
}

class C extends P {
    public static void m1() { }
}
// CE: m1() in C cannot override m1() in P
// overriding method is static
```

Same mismatch, reversed. Note which half of the message changes: the first
case says the **overridden** (parent) method is static; this case says the
**overriding** (child) method is static.

### 56:33 — Case 3: both static — compiles, but it's method hiding, not overriding

```java
class P {
    public static void m1() { }
}

class C extends P {
    public static void m1() { }
}
// compiles — method hiding, but not overriding
```

No compile error here. It looks like overriding works for static methods —
it doesn't. **This is method hiding.**

---

## 1:01:29 — Method hiding: all overriding rules apply, except one

Every rule already covered for overriding — same name, same arguments, same
return type, access scope only increases, never decreases — applies
identically to hiding. The one difference is **who resolves the call, and
when.**

### 1:03:34 — Three calls: parent/parent, child/child, parent-ref/child-object

```java
class P {
    public static void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    public static void m1() {
        System.out.println("child");
    }
}

class Test {
    public static void main(String[] args) {
        P p = new P();
        p.m1();
        // prints parent — parent reference, parent object

        C c = new C();
        c.m1();
        // prints child — child reference, child object (exact match)

        P p1 = new C();
        p1.m1();
        // prints parent — parent reference can hold child object
    }
}
```

The first two calls are unsurprising. The third is the whole point: **if
this were overriding**, `p1.m1()` would run the child method, because
overriding resolves on the runtime object. It doesn't here — it prints
`parent`, because `p1`'s **reference type** is `P`.

**In method hiding, resolution is done by the compiler, from the reference
type, and the runtime object plays no part.** In overriding, resolution is
done by the JVM, from the runtime object.

### 1:06:30 — Static (hiding) vs non-static (overriding), side by side

Static — hiding, resolved by reference type:

```java
class P {
    public static void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    public static void m1() {
        System.out.println("child");
    }
}

class Test {
    public static void main(String[] args) {
        P p = new P();
        p.m1();
        C c = new C();
        c.m1();
        P p1 = new C();
        p1.m1();
        // prints parent
        // prints child
        // prints parent
    }
}
```

Remove `static` from both — now it's overriding, resolved by runtime object:

```java
class P {
    public void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    public void m1() {
        System.out.println("child");
    }
}

class Test {
    public static void main(String[] args) {
        P p = new P();
        p.m1();
        C c = new C();
        c.m1();
        P p1 = new C();
        p1.m1();
        // prints parent
        // prints child
        // prints child
    }
}
```

Only the third line changes: `parent` for hiding, `child` for overriding.
That single line is the entire practical difference.

### 1:08:20 — Comparison table

| Method hiding | Overriding |
|---|---|
| Both parent and child class methods must be **static** | Both parent and child class methods must be **non-static** |
| **Compiler** resolves the call, based on **reference type** | **JVM** resolves the call, based on **runtime object** |
| Also known as compile-time polymorphism, static polymorphism, early binding | Also known as runtime polymorphism, dynamic polymorphism, late binding |

Because the compiler settles hiding from the declared reference type before
the program ever runs, it earns the "compile-time / static / early binding"
names. Because the JVM settles overriding from the actual object at the
moment of the call, it earns "runtime / dynamic / late binding."

### 1:13:53 — Same program, dictated again with the comment attached

Sir has the class copy the static (hiding) demo from 1:06:30 a second time,
this time with the explanatory comment attached directly to the code, and
gets the room to say the output aloud: **parent, child, parent**. Then he
flips the same program to non-static — **parent, child, child** — as one
more pass to lock in the single line that differs between the two.

```java
// both parent and child class methods are static → method hiding, not overriding
// output: parent, child, parent

// both parent and child class methods are non-static → overriding
// output: parent, child, child
```

---

## 1:17:40 — Why the words "overriding" and "hiding"

A short aside on the vocabulary itself, offered as optional: skip it if the
etymology doesn't interest you.

**Overriding, board analogy:** write something on a whiteboard, then rub it
out and write new data over it. The old data is simply gone — only the new
data is available.

**Hiding, chart analogy:** pin a chart, explain it, then pin a *second*
chart on top of the first. If a student asks to see the old chart again, you
can unpin the new one and show it — **both copies still exist**; the old one
is only hidden behind the new one, not destroyed.

### 1:20:12 — Mapping the metaphor onto parent/child methods

**Overriding:** once `m1` is overridden in the child, the parent's version is
gone for that object — for a child object, whether you call through a
parent reference or a child reference, the **child** method is what runs in
both cases.

```java
class P {
    public void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    public void m1() {
        System.out.println("child");
    }
}

class OverridingOnlyNewCopy {
    public static void main(String[] args) {
        P p = new C();
        p.m1();
        // prints child — parent reference, child object

        C c = new C();
        c.m1();
        // prints child — child reference, child object
        // for the child object, parent method already gone
    }
}
```

**Hiding:** with both methods static, both copies stay available for a child
object. A parent reference reaches the parent's copy; a child reference
reaches the child's copy — nothing was ever destroyed, only hidden depending
on which reference you use.

```java
class P {
    public static void m1() {
        System.out.println("parent");
    }
}

class C extends P {
    public static void m1() {
        System.out.println("child");
    }
}

class HidingBothCopies {
    public static void main(String[] args) {
        P p = new C();
        p.m1();
        // prints parent — parent reference on child object

        C c = new C();
        c.m1();
        // prints child — child reference on child object
        // both methods still available; old copy is only hidden
    }
}
```

That's the source of the names: hiding keeps both copies reachable, just one
behind the other; overriding replaces the old copy outright.

---

## 1:23:05 — Next heading (video ends): overriding with respect to var-arg methods

Sir writes only the heading here — the var-arg special case is the next
session.

## Exam and interview points

1. **Access modifiers can only widen, never narrow, on override** — `public`
   → `public` only; `protected` → `protected` or `public`; default → default,
   protected, or public. Reducing scope breaks callers who reach the object
   through a wider parent-typed reference.
2. **The checked-exception override rule**: if the child throws a checked
   exception, the parent must throw that same checked exception or one of
   its parents, or it's a compile error — `overridden method does not throw
   <type>`. **Unchecked exceptions have no such restriction** in either
   direction.
3. **`EOFException`/`FileNotFoundException` are children of `IOException`;
   `InterruptedException` is a child of `Exception` directly** — memorize
   this pairing, it's exactly what the seven-case drill turns on.
4. **A static method cannot be overridden as non-static, and a non-static
   method cannot be overridden as static** — both are immediate compile
   errors, distinguished only by which half of the message says
   `overridden`/`overriding method is static`.
5. **Both-static "overriding" compiles but is method hiding, not
   overriding.** The tell: does the call resolve by **reference type**
   (hiding, compiler, static/early binding) or by **runtime object**
   (overriding, JVM, dynamic/late binding)? Test it with
   `P p1 = new C(); p1.m1();` — hiding prints the parent's output, overriding
   prints the child's.
6. **`synchronized`, `native`, `strictfp` impose no restriction on
   overriding** in either direction — but `strictfp` itself is a no-op since
   Java 17 (JEP 306), because all floating-point math is strict by default
   now.
7. **Static interface methods (Java 8+) are never inherited or overridden**
   at all — call them through the interface name. Default methods, by
   contrast, behave like ordinary inherited instance methods and follow the
   normal override rules.
8. **`RemoteException` extends `IOException`**, not `Exception` directly —
   worth knowing precisely if a diagram (or your own memory of this lecture)
   puts it at the wrong level.

**Next:** Video 057 — Overriding and var-arg methods
