# Video 039 — native, transient, volatile

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-10|| native,static,transient

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 39 of 203 |
| Series | Declarations and Access Modifiers · Part 10 |
| Topic | native, static, transient |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 27m 49s |
| Video ID | nJ8klW-SQXs |
| Watch | https://www.youtube.com/watch?v=nJ8klW-SQXs |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

`static` is in the title, but **not** on this board — `static` was covered in
video 038. This Part-10 session actually works through **`native` → `transient`
→ `volatile`**, then closes the "Declarations and Access Modifiers" block with
a summary table of all 12 modifiers and their applicability across classes,
methods, variables, blocks, interfaces, enums, and constructors.

## What this lecture covers

1. `native` — applicable only to methods; what a native method is and why it exists
2. Three objectives of `native`: performance, machine/memory-level access, reusing legacy C/C++ code (`hashCode()` as the running example)
3. Pseudocode for using `native` in Java: load the library, declare the method, invoke it
4. Native method declarations cannot have a body; `native abstract` and `native strictfp` are illegal combinations
5. Advantage of `native` (performance) vs. disadvantage (breaks platform independence)
6. `transient` — applicable only to variables; its role in serialization
7. Serialization/deserialization basics, and why a sensitive field (`password`) should be `transient`
8. What actually happens to a `transient` field's value during serialization
9. `volatile` — applicable only to variables; multi-threaded shared-variable problem it addresses
10. `final volatile` is an illegal combination
11. Full summary table: all 12 modifiers × classes / inner classes / methods / variables / blocks / interfaces / inner interfaces / enums / inner enums / constructors
12. Exam-style "only applicable for ..." conclusions drawn from the table

---

## 00:04 — Where can we apply `native`?

`native` is a **modifier**, applicable **only for methods**. It cannot be
applied to a class, a variable, a block, or anything else — it is a
method-specific modifier.

```java
// CE: modifier native not allowed here (class)
native class Test {
}
```

```java
class Test {
    // CE: modifier native not allowed here (variable)
    native int x = 10;
}
```

```java
class Test {
    // valid — method declaration
    public native void m1();
}
```

> **Board:** `native` is a modifier applicable only for methods and we can't
> apply it anywhere else.

## 01:55 — What is a native method?

Not "a method from our native place." A **native method** is one whose
**implementation is written in a non-Java language** — mostly C or C++. Sir
also calls these **foreign methods**: the functionality comes from another
language.

```java
class Demo {
    // declaration lives in Java; the body lives in native (C/C++) code
    public native int compute();
}
```

## 03:30 — Why depend on C/C++ at all?

Sir's setup (trimmed from a long "Java has every star" bit): Java advertises
itself as simple, robust, secure, object-oriented, multithreaded, platform
independent, architecture neutral — so why still reach for old C/C++ code?
Because **there are areas where Java genuinely is not up to the mark**, and
`native` is how you fill those gaps.

## 06:48 — Objective 1: performance

Wherever performance is **very critical**, Java is comparatively weaker than
C/C++. Sir's advice: as a Java programmer, don't casually claim "Java is the
fastest" in a room where performance is being discussed.

**The pattern:** design most of the application in Java; implement the
performance-critical slice in C/C++; bring that functionality into Java with
`native`. This is the **biggest, first objective** of the keyword — improve
the performance of the system.

## 09:05 — Objective 2: machine-level / memory-level communication

Java is **programmer-friendly**, not **machine-friendly** — it cannot talk
directly to the machine or to memory the way C can, which is why device
drivers and OS-level work are typically written in C, not Java. Wherever
machine-level or memory-level communication is required, that part is
implemented in C/C++ and exposed to Java through `native`.

**Sir's example: `hashCode()`.** His claim — hash code is generated based on
an object's **address**, and pure Java has no way to read that address, so
the method has to be native:

```java
public class Object {
    // conceptual signature, as on the board (this is Object's real API)
    public native int hashCode();
}
```

> ❗ **Correction — "hash code = the object's address" is a simplification, not the mechanism.**
> `Object`'s own Javadoc does say the default is "typically implemented by
> converting the internal address of the object into an integer" — so Sir's
> story matches the *documented* folklore. In practice, HotSpot's default
> identity-hash algorithm since long before this recording is **not** a live
> memory address: it is a value (commonly a per-thread pseudorandom number)
> computed once and cached in the object's header the first time
> `hashCode()` runs. It has to work this way, because a compacting or
> generational garbage collector **moves objects in memory** — if the hash
> really were the live address, it would change every time the GC relocated
> the object, breaking every `HashMap` bucket built from it. The part of
> Sir's claim that *is* exactly right and still true today: `hashCode()` on
> `Object` is genuinely `native` because plain Java has no portable way to
> read or derive this identity value itself.

So the two forces at play here: performance (objective 1) and machine/memory
communication (objective 2).

## 11:26 — Objective 3: reuse legacy non-Java code

Third reason: some functionality already exists in a C/C++ legacy library and
you are not interested in rewriting it in Java. `native` lets you call that
already-existing, non-Java code directly.

### Board: the three objectives of `native`

| # | Objective |
|---|---|
| 1 | Improve performance of the system |
| 2 | Achieve machine-level / memory-level communication |
| 3 | Use already-existing legacy non-Java code |

Even with three benefits listed, Sir's stress is on the single most important
practical one: fill Java's performance gap with C/C++, via `native`.

## 14:42 — Pseudocode for using `native` in Java (3 steps)

1. **Load** the native libraries
2. **Declare** the native method
3. **Invoke** the native method

### Step 1 — load native libraries, in a `static` block

Native libraries must be loaded at **class-loading time**. A `static` block
runs exactly then, so `System.loadLibrary(...)` belongs there:

```java
class NativeDemo {
    static {
        // load native libraries at class-loading time
        System.loadLibrary("nativeLibraryPath");
        // or: System.load("/absolute/path/to/lib.so");
    }
}
```

### Step 2 — declare the native method, ending with `;`

The implementation already exists in C/C++ — you are not responsible for a
Java body. Same shape as an `abstract` method declaration: it ends with a
semicolon, not `{ }`.

```java
class NativeDemo {
    static {
        System.loadLibrary("nativeLibraryPath");
    }

    // declare native method — ends with a semicolon
    public native void m1();
}
```

### Step 3 — invoke the native method from a client

An instance method still needs an object to call it on:

```java
class NativeDemo {
    static {
        System.loadLibrary("nativeLibraryPath");
    }

    public native void m1();
}

class Client {
    public static void main(String[] args) {
        NativeDemo n = new NativeDemo();
        n.m1(); // invoke the native method
    }
}
```

**JNI, at a glance:** internally, JNI (the Java Native Interface) and the
platform's DLL/shared-library mapping do the work of connecting the Java
declaration to the C/C++ implementation. For this OCJP chapter, the three
steps above are what matters — writing the JNI glue itself is out of scope
here.

> ⚠️ **Modern Java — writing raw JNI is no longer the only door into C/C++.**
> Since **Java 22** (JEP 454, finalized after previews starting in Java 17),
> the **Foreign Function & Memory API** (`java.lang.foreign`, the "Project
> Panama" work) lets you call a C library and read/write off-heap native
> memory **without** writing a single `native` method, a `.c` glue file, or
> touching JNI at all — you look up a native symbol with `Linker` and
> `SymbolLookup` and call it through a `MethodHandle`. This targets exactly
> objectives 2 and 3 above (machine-level access, reusing existing C
> libraries) more safely than hand-written JNI. Calling into native code —
> the classic way or the new way — is also now treated as a **restricted
> operation**: without `--enable-native-access` granted to your module, the
> JVM prints a runtime warning. `native` methods and JNI still work exactly
> as Sir teaches them here; they are simply no longer the *only* tool for
> the job, and the platform is nudging native interop from "silent" to
> "opt-in."

## 21:48 — Native methods cannot have a body

Because the implementation already lives in C/C++, the declaration **must
end with `;`**. Writing `{ }` is a compile-time error.

```java
class Test {
    // valid
    public native void m1();
}
```

```java
class Test {
    // CE: native methods cannot have a body
    public native void m1() {
    }
}
```

| Declaration | Valid? | Reason |
|---|---|---|
| `public native void m1();` | Yes | Ends with `;` — no Java body |
| `public native void m1() { }` | No | Native methods cannot have a body |

## 25:10 — Illegal combo: `abstract` + `native`

| Kind | Implementation |
|---|---|
| native method | Implementation already available (in C/C++) |
| abstract method | Implementation must **not** be available (must be overridden later) |

The two ideas contradict each other, so `native abstract` (in either order)
is an illegal combination for methods:

```java
abstract class Test {
    // CE: illegal combination of modifiers: abstract and native
    public abstract native void m1();
}
```

Verified on JDK 26 — the compiler rejects both `abstract native` and
`native abstract` with the same message, order-independent.

## 27:54 — Illegal combo: `native` + `strictfp`

Recap of `strictfp`: a method marked `strictfp` must perform all
floating-point arithmetic to the **IEEE 754** standard, for
platform-independent results — a Java-language guarantee. But a `native`
method's body is C/C++, a platform-dependent language with no guarantee of
following IEEE 754. So a native method cannot be `strictfp`:

```java
class Test {
    // CE: illegal combination of modifiers: native and strictfp
    public native strictfp void m1();
}
```

> ⚠️ **Modern Java — `strictfp` itself is a no-op since Java 17** (JEP 306):
> all floating-point expressions are strict by default now, so the keyword
> changes nothing wherever it *is* still legal. That does not make this
> combination legal, though — verified on JDK 26, `native strictfp` still
> fails to compile with the same "illegal combination of modifiers" error,
> alongside a separate warning that `strictfp` itself is redundant. The
> reasoning Sir gives has been moot since Java 17 (there is no longer any
> IEEE-754 promise for `strictfp` to conflict with), but the syntax rule
> forbidding the pairing was never removed from the language.

## 31:16 — Advantage vs. disadvantage of `native`

**Advantage:** performance of the application improves — the critical parts
run as compiled C/C++.

**Disadvantage:** it breaks Java's **platform-independent** nature. Depending
on C/C++ — both platform-dependent languages — can make your Java program
platform-dependent too. Sir's example: `hashCode()` may produce one number on
one system and a different number after you change systems, precisely
because the method isn't pure Java.

```java
class HashDemo {
    public static void main(String[] args) {
        Object o = new Object();
        System.out.println(o.hashCode());
        // the printed number is not guaranteed to repeat across
        // JVMs, platforms, or even separate runs
    }
}
```

### Board summary for `native`

| | |
|---|---|
| Applicable | methods only |
| Meaning | implemented in non-Java (foreign methods) |
| Advantage | performance improves |
| Disadvantage | breaks platform independence |
| Illegal with | `abstract`, `strictfp` |
| Declaration | must end with `;` (no body) |

---

## 35:10 — Where can we apply `transient`?

`transient` is a modifier, applicable **only for variables** — it cannot be
applied to a method or anything else.

```java
class Test {
    // CE: modifier transient not allowed here
    transient void m1() {
    }
}
```

```java
class Account {
    // valid — variable
    transient String password;
}
```

`transient` plays its role in the **serialization** concept. (Full
serialization programs come 6–7 hours later in the course; this is the basic
idea only.)

## 37:26 — Serialization / deserialization, the basic idea

**Serialization:** saving (or sending) the **state of an object** — to a
file, or across a network. **Deserialization:** the reverse — reading an
object's state back from where it was saved.

Sir's sketch: an `Account` object, saved to `abc.ser` (the `.ser` extension is
just a convention; any extension works). Saving that object's state to the
file is serialization; reading it back is deserialization. A file lives on
the hard disk — **permanent** storage.

## 39:05 — Why `transient`? Security while serializing

Some fields are sensitive. Sir's example:

```java
username = "Durga"
password = "Anushka"
```

Saving both `username` and `password` **permanently** to a file is not
recommended — a security risk if the file is misused. His classroom analogy:
people readily share an email address, almost nobody shares a password, and
saving both together compounds the risk.

**The rule:** if you don't want to save a particular variable's value, to
meet a security constraint, declare that variable `transient`:

```java
class Account {
    String username = "Durga";
    transient String password = "Anushka";
}
```

## 41:26 — What happens to a `transient` variable at serialization time?

The JVM **ignores the original value** of a transient variable and saves its
**default value** to the file instead — `null` for a `String`.

| Field | Transient? | Value saved / restored |
|---|---|---|
| `username` | no | `"Durga"` |
| `password` | yes | `null` (default) |

```java
import java.io.*;

class Account implements Serializable {
    String username = "Durga";
    transient String password = "Anushka";
}

class SerializeDemo {
    public static void main(String[] args) throws Exception {
        Account a1 = new Account();

        ObjectOutputStream oos =
            new ObjectOutputStream(new FileOutputStream("abc.ser"));
        oos.writeObject(a1);
        oos.close();

        ObjectInputStream ois =
            new ObjectInputStream(new FileInputStream("abc.ser"));
        Account a2 = (Account) ois.readObject();
        ois.close();

        System.out.println(a2.username + "---" + a2.password);
        // prints Durga---null
        // username survives; transient password comes back as its default, null
    }
}
```

> **Board:** `transient` means "not to serialize" — at serialization time,
> the JVM ignores the original value of a transient variable and saves the
> default value to the file.

> ⚠️ **Modern Java — a record cannot mark one of its components `transient` at all.**
> ```java
> // CE: record components cannot have modifiers
> record Account(String username, transient String password) { }
> ```
> Verified on JDK 21 and JDK 26. A record's components are not ordinary field
> declarations you can annotate one by one — every component flows through
> the canonical constructor, so there is no per-component "skip me" hook the
> way there is on a plain class's field. If you need transient-style
> selective serialization on a record, you write a custom `writeObject`/
> `readObject` pair (or, more idiomatically today, don't serialize the record
> with Java serialization at all — reach for a `record`-friendly format like
> JSON instead).

## 47:38 — Wrap-up; next modifier is `volatile`

Serialization detail is deferred to its own block later in the course. Next
modifier: `volatile`.

## 48:00 — Where can we apply `volatile`?

`volatile` is a modifier, applicable **only for variables** — same shape as
`transient`, not applicable to methods or classes.

```java
class Test {
    // CE: modifier volatile not allowed here
    volatile void m1() {
    }
}
```

```java
class Test {
    // valid
    volatile int x;
}
```

## 49:11 — What "volatile" means: the memory analogy

Everyday sense: volatile = keeps changing, no stable behaviour. Sir's
hardware analogy: **volatile memory** is RAM — data is lost on shutdown;
**non-volatile** is the hard disk — data survives a restart. The thread
applies the same "keeps changing" idea to a variable's value.

## 50:32 — When do we need `volatile`? Multiple threads, one variable

Suppose `x` is read and written by several threads — `T1` sets it to `20`,
`T3` to `30`, `T4` to `-10`, and so on. A value that keeps changing under
concurrent access risks **data inconsistency**. Sir's fix, as taught in this
lecture: declare the variable `volatile`.

```java
class Shared {
    // value may be written by multiple threads
    volatile int x;
}
```

## 51:37 — The kids-and-ball story, and what `volatile` actually does

Sir's long analogy: kids at a festival fight over one shared ball; buying a
**separate ball for every kid** ends the fighting. His mapping onto threads,
as taught: if a variable is `volatile`, the JVM gives **every thread its own
separate local copy** — each thread's writes land only in its own copy, with
no effect on any other thread, and the inconsistency problem is "solved."

```java
class Counter {
    volatile int x = 0;

    // NOT how volatile actually works — see the correction below
    public void update(int value) {
        x = value;
    }
}
```

> ❗ **Correction — this is `volatile`'s actual behaviour turned inside out.**
> `volatile` does **not** give each thread its own private copy of the
> variable — that would make the inconsistency *worse*, not better, since
> then no thread could ever see another thread's update. The truth is closer
> to the opposite of the story:
>
> - **Without `volatile`**, a thread is *allowed* to keep a cached copy of the
>   variable — in a CPU register or core-local cache — and the Java Memory
>   Model does not promise that a write by one thread becomes visible to
>   another thread in any particular timeframe. *That* caching, not sharing,
>   is the real source of the "some thread sees a stale value" problem.
> - **With `volatile`**, every read goes to the single shared value and every
>   write is flushed straight back to it — the JVM is instructed to skip
>   thread-local caching and instruction reordering around that variable, so
>   all threads observe the same, most-recently-written value. `volatile`
>   also establishes a **happens-before** relationship (JLS §17.4.5): a write
>   to a volatile field happens-before every subsequent read of that same
>   field by another thread.
>
> The right story is "give every kid a window onto the *same* ball, always
> updated the instant anyone touches it" — not "give every kid a private
> ball." `volatile` solves *visibility*, not per-thread isolation; it does
> **not** by itself make compound operations like `x++` atomic (two threads
> can still race on a read-modify-write), which is exactly why
> `java.util.concurrent.atomic.AtomicInteger` and friends exist on top of it.

## 56:54 — Board conclusions for `volatile` (and correcting "almost deprecated")

Sir's board conclusion, as taught: advantage is overcoming data
inconsistency; disadvantage is that maintaining a separate copy per thread
(10,000 threads → 10,000 copies, in his framing) adds complexity and hurts
performance — so his verdict is that `volatile` is "almost deprecated," rarely
needed, and barely known by most Java programmers.

| | |
|---|---|
| Advantage (as taught) | overcomes data inconsistency |
| Disadvantage (as taught) | per-thread copies increase complexity and hurt performance |
| Advice (as taught) | without a specific need, never recommended; almost deprecated |

> ❗ **Correction — `volatile` was never deprecated, and it is not obscure.**
> Two things follow directly from the correction above. First, since there
> is no per-thread copy to create or maintain, the stated "disadvantage" and
> its performance story do not apply the way described — the real cost of
> `volatile` is much smaller (it forbids certain compiler/CPU reorderings and
> disables register caching for that field), not "one copy per live thread."
> Second, far from being deprecated or rarely used, `volatile` is a
> foundational building block of Java concurrency, then and now:
> `java.util.concurrent`'s atomic classes and locks are built on
> volatile-backed fields, the classic double-checked-locking singleton
> pattern requires a volatile field to be correct, and `java.lang.invoke.VarHandle`
> (Java 9) added even finer-grained volatile-style access modes
> (`acquire`/`release`/`opaque`). It remains exactly as relevant under
> virtual threads (Java 21, JEP 444) as under platform threads — visibility
> semantics are unchanged either way. Treat `volatile` as a precise,
> narrow-purpose tool worth understanding correctly, not as legacy syntax to
> avoid.

```java
class SharedData {
    volatile int x = 10;

    public void m1() {
        x = 20; // visible to every other thread as soon as this write completes
    }
}
```

## 1:03:04 — Illegal combo: `final` + `volatile`

Sir's reasoning (correct on its own terms, even once the mental model above
is fixed): `final` means the value is fixed and never changes, so there is
nothing whose visibility across threads needs to be kept up to date —
`volatile` on a variable that can never change again is unnecessary. The
compiler rejects the pairing:

```java
class Test {
    // CE: illegal combination of modifiers: final and volatile
    final volatile int x = 10;
}
```

```java
class Test {
    // CE: illegal combination of modifiers: volatile and final
    volatile final int y = 20;
}
```

Verified on JDK 26 — both orderings fail to compile with the same message.

| Modifier | Meaning for the value |
|---|---|
| `final` | never changes |
| `volatile` | may be read/written by multiple threads and must stay visible |

A value that can never change again has nothing left for `volatile` to keep
visible — hence the two are incompatible.

---

## 1:06:38 — All 12 modifiers — the summary table begins

The twelve modifiers covered across this series: `public`, default (no
modifier), `protected`, `private`, `final`, `abstract`, `static`,
`synchronized`, `strictfp`, `native`, `transient`, `volatile`.

The board's table asks, for each modifier: is it applicable to outer classes?
Inner classes? Methods? Variables? Blocks? Outer interfaces? Inner
interfaces? Outer enums? Inner enums? Constructors? A blank cell means "not
applicable."

## 1:12:03 — Filling the table

### Outer classes

Applicable: `public`, default, `final`, `abstract`, `strictfp`.

```java
public final class OuterAllowed {
}

class OuterDefault {
}

abstract class OuterAbstract {
}

strictfp class OuterStrict {
}
```

### Inner classes

Those same five, plus three more that only make sense once a class is
nested: `private`, `protected`, `static`.

```java
class Outer {
    private class InnerPrivate {
    }

    protected class InnerProtected {
    }

    static class NestedStatic {
    }
}
```

### Methods

Almost everything applies here — access modifiers, `final`, `abstract`,
`static`, `synchronized`, `native`, `strictfp`. The two that do **not**:
`transient`, `volatile`.

```java
class MethodMods {
    public final synchronized void m1() {
    }

    public static strictfp void m2() {
    }

    public native void m3();

    // CE: modifier transient not allowed here
    // transient void bad1() { }

    // CE: modifier volatile not allowed here
    // volatile void bad2() { }
}
```

### Variables

Applicable: access modifiers, `final`, `static`, `transient`, `volatile`. Not
applicable: `abstract`, `synchronized`, `native`, `strictfp`.

```java
class VarMods {
    public static final int MAX = 100;
    private transient String secret;
    volatile int flag;

    // CE: abstract not allowed on variables
    // abstract int x;

    // CE: synchronized not allowed on variables
    // synchronized int y;

    // CE: native not allowed on variables
    // native int z;

    // CE: strictfp not allowed on variables
    // strictfp double d;
}
```

### Blocks

Only two block kinds carry a modifier: `static` blocks and `synchronized`
blocks. Every other modifier is not applicable to a block.

```java
class BlockMods {
    static {
        System.out.println("static block");
    }

    void m() {
        synchronized (this) {
            System.out.println("synchronized block");
        }
    }
}
```

### Interfaces (outer)

Like classes, with one exception: every interface is **abstract by
default**, so `final` — which means "can never be extended/overridden" — is
a direct contradiction and is **not** allowed on an interface.

```java
public interface I1 {
}

// CE: illegal combination of modifiers: interface and final
// final interface I2 { }

strictfp interface I3 {
}
```

Verified on JDK 26: `final interface` fails to compile.

### Inner interfaces

Same rule as outer interfaces (still no `final`), plus the same extras inner
classes get: `private`, `protected`, `static`.

```java
class Outer {
    private interface InnerI {
    }

    protected static interface NestedI {
    }
}
```

### Enums

An enum behaves like a class, with a twist: every enum is **always final
implicitly** (the full reasoning belongs to the enum chapter). Because it is
already final, you cannot write `final` on it explicitly either — and you
cannot declare an enum `abstract`. So the modifiers applicable to a class but
**not** to an enum are `final` and `abstract`. `public`, default, and
`strictfp` remain fine on an outer enum; an inner enum additionally allows
`private`, `protected`, `static`, matching inner classes.

```java
public enum Color {
    RED, GREEN, BLUE
}

// CE: modifier final not allowed here (already final implicitly)
// final enum Bad1 { A }

// CE: modifier abstract not allowed here
// abstract enum Bad2 { A }
```

Verified on JDK 26 — both fail with "modifier ... not allowed here."

```java
class Outer {
    private enum InnerEnum {
        A, B
    }

    static enum NestedEnum {
        X, Y
    }
}
```

> ⚠️ **Modern Java — two newer class-level modifiers joined this table.**
> **Records** (Java 16) are, like enums, always implicitly `final` — but
> unlike enums, writing `final` on a record explicitly compiles fine (it's
> merely redundant, verified on JDK 26); `abstract record` is still rejected
> the same way `abstract enum` is. **Sealed classes and interfaces** (Java
> 17, JEP 409) added two more modifiers to this same family: `sealed`
> restricts which classes may extend it to a declared `permits` list, and
> `non-sealed` reopens a branch of a sealed hierarchy to unrestricted
> extension. Both apply to classes and interfaces only — the same "not for
> variables, not for methods" shape every modifier in this table already
> follows.
> ```java
> sealed interface Shape permits Circle { }
> final class Circle implements Shape { }
> ```

### Constructors

Only access modifiers apply: `public`, `private`, `protected`, default. Any
other modifier on a constructor is a compile-time error.

```java
class Test {
    public Test() {
    }

    private Test(int x) {
    }

    protected Test(String s) {
    }

    Test(double d) { // default access
    }

    // CE: modifier final not allowed here
    // final Test(boolean b) { }

    // CE: modifier static not allowed here
    // static Test(char c) { }

    // CE: modifier synchronized not allowed here
    // synchronized Test(long n) { }
}
```

## 1:19:34 — Table complete; a gap means "not applicable"

Wherever the table's cell is empty, that modifier is simply not applicable
for that member kind — cross it out or leave it blank, whichever notation
you prefer.

## 1:22:36 — Extra conclusions under the table (exam favourites)

### 1) The only applicable modifier for a local variable

Already covered earlier in the course: **only `final`**.

```java
class Test {
    public void m1() {
        final int x = 10; // only applicable modifier for a local variable

        // CE: public not allowed for local variable
        // public int y = 20;

        // CE: static not allowed for local variable
        // static int z = 30;

        // CE: transient not allowed for local variable
        // transient int t = 40;
    }
}
```

### 2) The only applicable modifiers for a constructor

`public`, `private`, `protected`, default — nothing else.

```java
class C {
    public C() {
    }

    private C(int a) {
    }

    protected C(String s) {
    }

    C(byte b) {
    }
}
```

### 3) The modifier applicable only for methods, nowhere else

From the table, **`native`** is the clean method-only tick — every other
column crosses it out.

```java
class OnlyMethod {
    public native void m1(); // only for methods
}
```

(`synchronized` also concentrates on methods and blocks, but Sir's spoken
punchline for "only for methods" here is `native`.)

### 4) The modifiers applicable only for variables

**`transient`** and **`volatile`**.

```java
class OnlyVars {
    transient int a;
    volatile int b;
}
```

### 5) Applicable for classes but not interfaces

**`final`**.

```java
final class OkClass {
}

// CE: final interface not allowed
// final interface BadInterface { }
```

### 6) Applicable for classes but not enums

**`final`** and **`abstract`**.

```java
abstract class OkAbstractClass {
}

final class OkFinalClass {
}

// not applicable to enum (explicit final / abstract) — see the enum rules above
```

## 1:27:14 — Closing

That closes the modifiers block. **Next topic:** interfaces — Sir calls it
the "most valuable concept" for interviews and the OCJP track.

---

## Exam and interview points

1. **`native` is method-only.** Its three objectives are performance,
   machine/memory-level access, and reusing legacy non-Java code —
   `Object.hashCode()` is the canonical example and is genuinely `native` in
   the real JDK, though the "hash = literal memory address" story is folklore
   more than mechanism (HotSpot's default is a cached pseudorandom value, so
   it survives a compacting GC moving the object).
2. **A native method declaration ends with `;`, never `{ }`** — same shape as
   an abstract method, for the same reason: no Java body is provided.
3. **`abstract native` and `native strictfp` are illegal combinations for
   methods**, both verified on JDK 26. The `strictfp` reasoning ("no IEEE 754
   guarantee in old languages") has been moot since `strictfp` itself became
   a no-op in Java 17, but the syntax restriction on the pairing was never
   lifted.
4. **`transient` is variable-only**, and matters at serialization time: the
   JVM writes the field's **default value**, not its actual value, to the
   stream. A record cannot mark any single component `transient` — record
   components carry no modifiers at all.
5. **`volatile` is variable-only and its real job is cross-thread
   visibility, not per-thread copies.** The correct mental model: without
   `volatile`, a thread may cache a stale value; with it, every read/write
   goes through one shared, up-to-date value, and a write happens-before a
   later read by any other thread (JLS §17.4.5). It is a live, load-bearing
   part of `java.util.concurrent`, `VarHandle`, and double-checked locking —
   not "almost deprecated."
6. **`final volatile` is illegal** — verified on JDK 26 — because a value
   that can never change again has no visibility problem left for `volatile`
   to solve.
7. **The applicability table's stand-out rows:** `native` — methods only;
   `transient`/`volatile` — variables only; `final` — classes but not
   interfaces or enums; `abstract` — classes but not enums; local variables —
   `final` only; constructors — access modifiers only.
8. **Since this recording, two modifiers joined the class/interface family**:
   `sealed` and `non-sealed` (Java 17), restricting or reopening who may
   extend a type via a `permits` clause. Records (Java 16) behave like an
   enum's "always final" cousin, except an explicit `final record` compiles
   (merely redundant), while `final enum` does not.

---

**Next:** Video 040 — Interfaces Part 1
