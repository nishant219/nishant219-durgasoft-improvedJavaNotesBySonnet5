# Video 042 — Marker Interfaces and Adapter Classes

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-13|| interfaces-3

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 42 of 203 |
| Series | Declarations and Access Modifiers · Part 13 |
| Topic | interfaces-3 (marker interface and related) |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 04m 31s |
| Video ID | Kveg8HH2g9c |
| Watch | https://www.youtube.com/watch?v=Kveg8HH2g9c |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Marker interface is an **interview** topic — "empty interface" is only half
   the definition.
2. Full rule: no methods **and** implementing it gives the object some extra
   **ability**. Also called ability interface / tag interface.
3. Examples: `Serializable`, `Cloneable`, `RandomAccess`, `SingleThreadModel`.
4. `clone()` lives in `Object`, not in `Cloneable`. Missing `Cloneable` →
   `CloneNotSupportedException`.
5. Big doubt: no methods, so how does the object get the ability? Internally
   the **JVM** (or its runtime library) provides it.
6. Why does the JVM do it? To reduce the complexity of programming and keep
   Java simple.
7. Can we create our own marker (`Sleepable`, `Jumpable`)? Yes — but it needs
   **customization of the runtime**, or a JVM of your own.
8. Next topic: **adapter classes** — a programmer's trick, not a language
   feature.
9. Interface with 1000 methods; you need only `m3` → dummy methods vs. extend
   an adapter.
10. Declare the adapter **abstract** — creating an object of it and calling its
    dummy methods is waste.
11. Servlet example: three ways to build one; `GenericServlet` is *more or
    less* an adapter for `Servlet`.
12. Closing board: marker interfaces and adapter classes simplify programming
    — best utilities to the programmer.

---

## 00:04 — Marker interface: an interview staple

Board heading, written slowly so the room copies it: **marker interface**.
Sir opens with a challenge — spell out whatever you know, so he can correct
it live.

### 00:49 — Incomplete definition: "no methods" is not enough

A student offers: *the interface which doesn't contain any methods is a
marker interface.* Sir puts this on the board as rule one — **first half
only** — and tests it:

```java
interface X {
    // doesn't contain any method
}
```

Is `X` a marker interface? If "no methods" really were the whole definition,
`X` should qualify. Sir is confident no one will accept that. So the
one-line definition is incomplete.

### 01:47 — The full two-part definition

**Rule 1** (what the student said): the interface has no methods.
**Rule 2:** implementing that interface must give the object some **extra
ability**.

> *If an interface doesn't contain any methods **and** by implementing that
> interface our objects get some ability, such interfaces are called
> **marker interfaces**.*

```java
interface MarkerStyle {
    // no methods
}

class MyClass implements MarkerStyle {
    // objects of MyClass get some extra ability —
    // that ability does NOT come from a method inside MarkerStyle
}
```

An empty interface that grants **no** ability by being implemented is just
empty — not a marker. That is why a random `interface X` with nothing inside
does not count.

### 02:45 — Example: Serializable

Best example: **`Serializable`**. It has no methods. If a class's object does
not implement it, that object cannot be saved to a file and cannot be sent
across a network. Implement it, and the object gets **serializable
ability**.

```java
import java.io.Serializable;

class Student implements Serializable {
    String name;
    int rollNumber;
}

class Demo {
    public static void main(String[] args) {
        Student s = new Student();
        s.name = "Durga";
        s.rollNumber = 101;
        // s has serializable ability: can be saved to a file,
        // can travel across a network
    }
}
```

```java
class Employee {
    String name;
    int empId;
}
// Employee does NOT implement Serializable:
// cannot be saved to a file, cannot be sent across a network
```

### 03:56 — Example: Cloneable — `clone()` lives in `Object`, not in `Cloneable`

Same shape, different ability. If you want an exact duplicate of an object,
its class must implement `Cloneable`. Skip that and call `clone()` anyway,
and you get `CloneNotSupportedException` at runtime — not a compile error,
because the method exists on every object; it just refuses to run.

```java
class Test implements Cloneable {
    int x = 10;

    public static void main(String[] args) throws CloneNotSupportedException {
        Test t1 = new Test();
        Test t2 = (Test) t1.clone();
        System.out.println(t2.x);   // 10
    }
}
```

```java
class Test {
    int x = 10;

    public static void main(String[] args) throws CloneNotSupportedException {
        Test t1 = new Test();
        Test t2 = (Test) t1.clone();
        // RE: java.lang.CloneNotSupportedException: Test
        //   at java.base/java.lang.Object.clone(Native Method)
        // class does not implement Cloneable → no clonable ability
    }
}
```

Verified: compiling and running both versions reproduces exactly this —
`10` for the first, `CloneNotSupportedException` thrown from
`Object.clone()` (a native method) for the second.

**Don't miss this:** `clone()` is declared in `Object`, not in `Cloneable`.

```java
package java.lang;

public class Object {
    protected native Object clone() throws CloneNotSupportedException;
    // clone() lives here
}

public interface Cloneable {
    // no methods — marker/tag only
}
```

### 05:01 — RandomAccess, SingleThreadModel, and the two other names for this idea

More marker interfaces, same shape — no methods, but tagged with an ability:

| Marker interface | Package | Ability the object gets |
|---|---|---|
| `Serializable` | `java.io` | can be written to a stream / sent over a network |
| `Cloneable` | `java.lang` | `Object.clone()` succeeds instead of throwing `CloneNotSupportedException` |
| `RandomAccess` | `java.util` | list algorithms (e.g. `Collections.binarySearch`) switch to index-based access instead of iterator-based |
| `SingleThreadModel` | `javax.servlet` | (historic) guarantees only one thread touches a given servlet instance at a time |

Because they are "marked" for an ability, Sir also calls this idea **ability
interface** or **tag interface** (tagged with an ability) — three names, one
concept.

> ❗ **Correction — `SingleThreadModel` was already obsolete when this was recorded.**
> The Servlet spec deprecated `SingleThreadModel` in **Servlet 2.4 (2003)** —
> years before this lecture — because "one thread per instance" does not
> actually make a servlet thread-safe (its fields could still be shared with
> other objects), and containers were free to implement it by pooling
> instances, which is expensive and misleading. It is legacy-taught-as-current
> here; do not reach for it in real code.

> ⚠️ **Modern Java — marker interfaces got a sibling: marker annotations.**
> Since **Java 5** you can also "tag" a type with a **marker annotation** —
> an annotation with no elements, like `@Deprecated` or `@FunctionalInterface`
> — instead of an empty interface:
>
> ```java
> @interface MyMarker { }   // marker annotation: zero elements
>
> @MyMarker
> class Widget { }
> ```
>
> So why do `Serializable`, `Cloneable`, and `RandomAccess` still exist as
> *interfaces* instead of being converted to annotations? Because their check
> has to run as an `instanceof` test inside ordinary method dispatch —
> `ObjectOutputStream.writeObject` and `Object.clone()` both do
> `obj instanceof Serializable` / `this instanceof Cloneable` — and only an
> interface participates in Java's type system that way. An annotation is
> metadata you inspect through reflection; it cannot appear on the right side
> of `instanceof` or change what a variable can be assigned to. Rule of thumb
> for an interview: reach for a marker **interface** when the marker must
> affect the type system or a runtime `instanceof` check; reach for a marker
> **annotation** when the marker is purely informational (a compiler hint, a
> tool hint, documentation).

### 11:15 — Interview doubt: no methods, so how does the ability appear?

The big doubt, "expected even in the interview room": marker interfaces
declare zero methods, so where does the ability actually come from?

```java
interface Serializable {
    // no methods at all
}

class Student implements Serializable {
    // this object gets "save to file / send on network" ability —
    // but Serializable itself declares nothing that could grant it
}
```

### 12:36 — Analogy: why nobody starts their job hunt in New York

Sir's setup: after finishing the Java course, everyone plans to job-hunt in
Hyderabad, Bangalore, Chennai, Pune — never New York, London, or California,
even in their dreams. Why not? The class lists the real blockers: money
(**"Vitamin M"**), passport/visa, a new environment with no one to guide you,
food, and homesickness. Every one of those is a genuine reason to stay close
to home.

Then the twist: if someone guarantees to handle every one of those problems —
money until your first paycheck, passport and visa contacts, a guest house
and local support, even bringing your parents along — suddenly everyone in
the room is willing to go. **Approach 1** (you handle everything yourself) is
paralysing; **approach 2** (someone else absorbs the hard parts) makes the
same opportunity usable.

### 23:38 — The same story, aimed at marker interfaces: sending an object to London

Someone in London asks Sir to send a `Student` object across the network. His
honest answer: he can't — not because he doesn't want to, but because turning
a live Java object into "network-supported form" and handling every
network-level failure would take, by his estimate, **around 70 lakh (7
million) lines of code across a dozen network-related languages**. No single
programmer is going to learn all of that just to send one object.

```java
class Student {
    String name;
    int rollNumber;
}
// to send a Student object Hyderabad → London, if the PROGRAMMER
// had to write the wire-format conversion and handle every network
// failure personally: ~70 lakh lines of code, a dozen protocols —
// no programmer is realistically going to do that
```

### 25:56 — Sun's answer: the JVM (really, the platform) does it for you

Sun's people saw this exact problem and provided an "assistant": if you want
an object to travel across a network, you are not required to write any of
that code. Mark the class `implements Serializable`, and the required
ability is provided **internally**. You never touch a network API yourself.

```java
import java.io.Serializable;

class Student implements Serializable {
    String name;
    int rollNumber;
}
// programmer writes zero lines of wire-format code —
// just "implements Serializable"; the platform provides the ability
```

> ❗ **Correction — it isn't literally "the JVM" that does the work in every case.**
> For **`Cloneable`**, "the JVM" is exactly right: `Object.clone()` is a
> **native method implemented inside the JVM**, and it is the JVM that checks
> `this instanceof Cloneable` before it will duplicate the object.
> For **`Serializable`**, the check runs in ordinary **class-library** code —
> `java.io.ObjectOutputStream` (via `ObjectStreamClass`) tests
> `obj instanceof Serializable` and throws `NotSerializableException` if it
> fails, entirely in Java code that ships with the JDK, not inside the JVM
> engine itself. "Internally the JVM is responsible" is the right OCJP
> answer and a fine mental model; "internally the platform — JVM or runtime
> library, depending on which marker — is responsible" is the precise one.

### 26:45 — Board Q&A: how, and why

```java
// Q: without having any methods, how do objects get ability?
// A: internally the JVM (or its runtime library) is responsible
//    for providing the required ability
//
// Q: why does the JVM/runtime provide that ability instead of
//    leaving it to the programmer?
// A: to reduce the complexity of programming and keep
//    Java language as simple as possible
```

If the platform did not provide this, the programmer would have to — and
"complexity of the programming is going to be increased" while "programmer
may not be at that level." Providing it through marker interfaces is part of
Java's "nursery standard, simple language" pitch.

### 30:44 — Can we create our own marker interface?

**Yes — 100% possible.** But here's the twist: whoever checks `instanceof
YourMarker` and acts on it has to already exist. The **existing** JVM already
knows to look for `Serializable` and `Cloneable` — that logic is built in.
It does **not** already know to look for a marker you invent.

```java
interface Sleepable { }
interface Jumpable { }

class Dog implements Sleepable, Jumpable { }

class Test {
    public static void main(String[] args) {
        Dog d = new Dog();
        // compiles and runs fine — but nothing in the existing JVM
        // treats "Sleepable" or "Jumpable" specially
    }
}
```

Verified: this compiles and runs — `Dog implements Sleepable, Jumpable` is
completely legal Java. The interfaces themselves are inert; nothing acts on
them unless something is written to look for them.

### 32:05 — Sleepable / Jumpable, and "your own JVM"

To give `Sleepable`/`Jumpable` a real effect, you would need to customize the
runtime — or design your own JVM (Sir's shorthand: **DJVM**) that knows to
check for them. This is not exotic: the JVM is not Sun/Oracle proprietary.
Different servers ship different JVMs — Sir names **JRockit** as WebLogic's
JVM, alongside Tomcat and WebSphere, each free to build their own runtime and
recognise whatever markers they choose.

> ❗ **Correction — JRockit's later history.**
> JRockit was built by **Appstream**, then developed by **BEA Systems** (the
> company behind WebLogic) — not by Sun. When **Oracle acquired BEA in 2008**
> and then **Sun in 2010**, Oracle ended up owning both JRockit and HotSpot.
> Rather than keep two JVMs, Oracle merged JRockit's stronger features (its
> flight-recorder diagnostics, in particular) into HotSpot and **discontinued
> JRockit** around 2013–2014. Every JVM sold today under the Oracle,
> OpenJDK, or Temurin name is HotSpot-derived, not JRockit.

**Answer to remember for the interview:** *Yes, you can build your own marker
interface — but customization of the JVM (or runtime) is required for it to
do anything.* Building that customization is not normal application-developer
scope; it's the kind of thing app-server vendors (WebLogic, Tomcat,
WebSphere) do.

---

## 34:57 — Next topic: adapter classes

A much simpler idea: **adapter classes are a programmer's trick, not a
language feature.**

### 35:30 — Setup: interface `X` with 1000 methods, needed only `m3`

```java
interface X {
    void m1();
    void m2();
    void m3();
    // ...
    void m1000();
}
```

Target: implement `X`, but provide real logic for only `m3`.

### 36:23 — Implementing `X` directly forces every method — dummy or not

```java
class TestBad implements X {
    public void m3() {
        System.out.println("m3");
    }
    // CE: TestBad is not abstract and does not override abstract method m2() in X
    //     (and m1(), m4(), ..., m1000() are missing too)
}
```

Verified: `javac` rejects a 3-method trimmed-down version of exactly this
with `TestBad is not abstract and does not override abstract method m2() in
X`. Implementing an interface directly means every single method needs a
body — required or not, interesting or not:

```java
class Test implements X {
    public void m1() { }      // empty / dummy
    public void m2() { }      // empty / dummy
    public void m3() {
        System.out.println("m3");   // the only real implementation
    }
    public void m4() { }
    // ...
    public void m1000() { }   // 999 dummy methods total
}
```

Ten lines of real code cost 999 lines of dummy padding. Length goes up,
readability goes down, and every implementer of `X` has to repeat this.

### 38:28 — The adapter class: empty implementations, written once

> **Adapter class** is a plain Java class that implements an interface with
> **only empty implementations** for every method. Any name is fine — Sir
> uses `AdapterX`.

```java
abstract class AdapterX implements X {
    public void m1() { }
    public void m2() { }
    public void m3() { }
    // ...
    public void m1000() { }
}
```

### 39:57 — Extend the adapter instead of implementing `X` directly

```java
class Test extends AdapterX {
    public void m3() {
        System.out.println("only m3");
    }
    // remaining 999 methods come from AdapterX through inheritance
}
```

`Test` extends `AdapterX`, and `AdapterX implements X` — so **indirectly**
`Test` also implements `X`. No rule is bent; a class satisfies an interface
through its superclass just as well as directly.

```java
interface X {
    void m1();
    void m2();
    void m3();
}

abstract class AdapterX implements X {
    public void m1() { }
    public void m2() { }
    public void m3() { }
}

class Test extends AdapterX {
    public void m3() {
        System.out.println("m3 only");
    }
}

class Demo {
    public static void main(String[] args) {
        X x = new Test();   // valid — Test indirectly implements X
        x.m3();              // m3 only
        x.m1();               // empty from AdapterX — no output
    }
}
```

Verified: this compiles and prints `m3 only`, confirming that extending the
adapter and calling `m3()` on it through the `X` reference works exactly as
described.

### 41:15 — Write the adapter once, reuse it many times

```java
class Sample extends AdapterX {
    public void m7() { System.out.println("m7"); }
}

class DemoUser extends AdapterX {
    public void m1000() { System.out.println("m1000"); }
}
```

The adapter is **written once** and **used three times** here (`Test`,
`Sample`, `DemoUser`), each overriding only the one method it needs. Without
the trick, every one of those three classes would have to implement all
1000 methods of `X` itself — three times the dummy-method tax. This is a
programmer's design pattern, not something the Java language enforces.

### 42:39 — Declare the adapter `abstract`

Every method in the adapter is a dummy — calling any of them on an adapter
instance does nothing, so creating one is waste. That is why an adapter
class is almost always declared `abstract`:

```java
class AdapterXBad implements X {
    public void m1() { }
    public void m2() { }
    public void m3() { }
}

class UseIt {
    public static void main(String[] args) {
        AdapterXBad a = new AdapterXBad();
        a.m1();   // nothing happens — dummy implementation, wasted object
    }
}
```

```java
abstract class AdapterX2 implements X {
    public void m1() { }   // concrete, but dummy
    public void m2() { }   // concrete, but dummy
    public void m3() { }   // concrete, but dummy
}

class UseIt2 {
    public static void main(String[] args) {
        AdapterX2 a = new AdapterX2();
        // CE: AdapterX2 is abstract; cannot be instantiated
    }
}
```

As covered earlier in the course: an abstract class may legally contain
**zero abstract methods** — every method here is concrete, just uselessly
so. Declaring the class `abstract` anyway is what stops a wasted object from
ever being created.

> ⚠️ **Modern Java — for a single-method interface, you often don't need an adapter at all.**
> Adapter classes solve the "implement N methods, care about 1" problem.
> Since **Java 8**, if the interface you actually need has exactly **one**
> abstract method (a *functional interface*), a **lambda** replaces the whole
> dummy-subclass dance:
>
> ```java
> interface OneMethod { void m3(); }
>
> // pre-lambda: needed an adapter or an anonymous class
> // Java 8+:
> OneMethod r = () -> System.out.println("m3 only");
> ```
>
> This doesn't retire the adapter-class pattern — `X` in this lecture has
> 1000 methods, and multi-method interfaces still need it. The textbook real
> examples in the JDK are `java.awt.event.WindowAdapter`, `MouseAdapter`, and
> `KeyAdapter` (all present since Java 1.1) — each implements a listener
> interface with 5–7 methods using empty bodies, exactly so you can override
> only the one event you care about. Lambdas only replace the pattern where
> the interface has a single abstract method.

---

## 44:01 — Where this is used: Servlet programming

Sir asks whether the room knows Servlet programming, then walks through the
real-world instance of this exact trick.

### 53:37 — Three ways to develop a servlet

`Servlet` is an interface. `GenericServlet` implements it and is `abstract`
because it provides real implementations for every method **except**
`service`. `HttpServlet` extends `GenericServlet` and is also `abstract` —
not because it has any abstract method left, but because its own
implementation of `service` just sends a "method not supported" error for
whatever HTTP verb you didn't override.

```java
interface Servlet {
    void init();
    void service();
    void destroy();
    void getServletConfig();
    void getServletInfo();
}

abstract class GenericServlet implements Servlet {
    public void init() { }
    public void destroy() { }
    public void getServletConfig() { }
    public void getServletInfo() { }
    public abstract void service();   // the one method left to the subclass
}

abstract class HttpServlet extends GenericServlet {
    // no abstract method of its own — but still abstract:
    // its service() implementation is a dummy that sends an error
    // for whichever HTTP method the subclass didn't override
    public void service() {
        // dummy implementation / "method not allowed" style response
    }
}

class MyServlet extends HttpServlet {
    // the everyday way to write a servlet
}
```

**Three ways to develop a servlet:**

1. **Implement `Servlet`** directly.
2. **Extend `GenericServlet`.**
3. **Extend `HttpServlet`.**

```java
class MyServlet1 implements Servlet {   // way 1
    public void init() { }
    public void service() { }
    public void destroy() { }
    public void getServletConfig() { }
    public void getServletInfo() { }
}

class MyServlet2 extends GenericServlet {   // way 2
    public void service() { }
}

class MyServlet3 extends HttpServlet { }    // way 3 — most common
```

### 54:23 — Implementing `Servlet` directly needs all five methods

`javax.servlet.Servlet` has **five** methods: `init`, `service`, `destroy`,
`getServletConfig`, `getServletInfo`. Implement it directly, and every one
of the five is mandatory whether you need it or not — "no initialization
activity" still forces an `init()` body, "no cleanup" still forces a
`destroy()` body. Nobody actually builds servlets this way.

```java
class MyServletDirect implements Servlet {
    public void service() {
        System.out.println("service");
    }
    // CE: MyServletDirect is not abstract and does not override
    //     abstract method init() in Servlet
    //     (destroy(), getServletConfig(), getServletInfo() missing too)
}
```

> ❗ **Correction — the real `Servlet` interface's methods carry parameters, checked exceptions, and non-`void` returns.**
> The board version above is simplified for teaching. The actual
> `javax.servlet.Servlet` interface is:
>
> ```java
> import java.io.IOException;
>
> interface Servlet {
>     void init(ServletConfig config) throws ServletException;
>     ServletConfig getServletConfig();
>     void service(ServletRequest req, ServletResponse res)
>             throws ServletException, IOException;
>     String getServletInfo();
>     void destroy();
> }
> ```
>
> `getServletConfig()` returns a `ServletConfig`, `getServletInfo()` returns a
> `String` — neither is `void` — and `init`/`service` declare checked
> exceptions. Verified: a mock `GenericServlet` built against this exact
> shape (with stand-in `ServletConfig`/`ServletRequest`/`ServletResponse`/
> `ServletException` types) compiles cleanly, leaving only `service` abstract
> — matching what Sir teaches, just with the real signatures.

> ⚠️ **Modern Java — `javax.servlet` became `jakarta.servlet`.**
> None of `Servlet`, `GenericServlet`, or `HttpServlet` are part of Java SE —
> they belong to the separate Servlet specification (Java EE, then Jakarta
> EE). When Oracle transferred Java EE to the Eclipse Foundation, trademark
> restrictions on the `javax.*` name forced a rename: as of **Jakarta EE 9
> (2020)**, the entire API moved to the **`jakarta.servlet`** package.
> Containers from Tomcat 10 / Jetty 11 onward ship the `jakarta.*` classes;
> anything still importing `javax.servlet.*` is running the pre-2020 API
> (still valid, e.g. on Tomcat 9).

### 55:28 — Extending `GenericServlet` needs only `service`

`GenericServlet` already implements all methods of `Servlet` except
`service`. Extend it, and only `service` is your responsibility — the
other four arrive from the parent through inheritance.

```java
class MyServlet extends GenericServlet {
    public void service() {
        System.out.println("only service");
        // init, destroy, getServletConfig, getServletInfo come from GenericServlet
    }
}
```

### 56:20 — "More or less" an adapter — but not 100%

Because extending `GenericServlet` means providing an implementation for
only one method out of several, Sir wants to call `GenericServlet` an
adapter class for `Servlet`. But he immediately qualifies it: a strict
adapter class contains **only empty** implementations. `GenericServlet`'s
`init`, `destroy`, `getServletConfig`, and `getServletInfo` are not empty —
they carry real, useful logic (tracking the `ServletConfig`, etc.). So it's
**more or less** an adapter, not a textbook one.

```java
abstract class StrictAdapterServlet implements Servlet {
    public void init() { }              // EMPTY — strict adapter style
    public void destroy() { }
    public void getServletConfig() { }
    public void getServletInfo() { }
    public abstract void service();
}

abstract class GenericServletReal implements Servlet {
    public void init() {
        // NOT empty — real bookkeeping happens here in the actual API
    }
    public void destroy() { /* real cleanup hook */ }
    public void getServletConfig() { /* real accessor */ }
    public void getServletInfo() { /* real accessor */ }
    public abstract void service();
    // "more or less" an adapter — but not 100% one
}
```

Either way, the effect for the servlet author is the same: implementing
`Servlet` directly "increases length of the code and reduces readability";
extending `GenericServlet` means providing implementation "only for the
service method," and everything else is inherited for free.

---

## 1:02:45 — Closing note

> **Marker interfaces and adapter classes simplify the complexity of
> programming and are the best utilities to the programmer** — the
> programmer's life becomes simpler because of both.

```java
// marker interface — the platform provides the ability; the programmer writes only:
class Student implements java.io.Serializable { }

// adapter class — the programmer implements only the required method:
abstract class AdapterX implements X {
    public void m1() { }
    public void m2() { }
    public void m3() { }
}

class Test extends AdapterX {
    public void m3() {
        System.out.println("only what I need");
    }
}
```

---

## Exam and interview points

1. **The complete marker-interface definition has two parts:** no methods
   *and* implementing it grants the object an extra ability. Either half
   alone is not enough — an empty interface that grants nothing is just
   empty.
2. **Standard exam examples:** `Serializable` (`java.io`), `Cloneable`
   (`java.lang`), `RandomAccess` (`java.util`) — and, historically,
   `SingleThreadModel` (`javax.servlet`, deprecated since Servlet 2.4).
3. **`clone()` lives in `Object`** (`protected native Object clone()`), not in
   `Cloneable`. Missing `Cloneable` → `CloneNotSupportedException` thrown
   from `Object.clone()` at runtime, not a compile error.
4. **The ability comes from an `instanceof` check written elsewhere** — in
   `Object.clone()` (the JVM itself, since it's native) for `Cloneable`, or
   in `ObjectOutputStream`/`ObjectStreamClass` (ordinary library code) for
   `Serializable` — never from a method the marker interface declares.
5. **You can write your own marker interface** (`Sleepable`, `Jumpable`, …),
   and it compiles and runs fine — but nothing acts on it unless some part
   of the runtime is written to check `instanceof YourMarker`. The
   interview answer is *"yes, but it requires customization of the JVM/runtime."*
6. **Marker annotations (Java 5+) are the modern alternative** for markers
   that are purely informational (`@Deprecated`, `@FunctionalInterface`).
   Markers that must affect `instanceof` checks or method dispatch —
   `Serializable`, `Cloneable`, `RandomAccess` — stay interfaces because
   annotations aren't part of the type system.
7. **Adapter class** = an (ideally `abstract`) class implementing a
   multi-method interface with empty bodies for every method, so a subclass
   overrides only what it needs. It is a **design pattern**, not a Java
   language feature.
8. **Real JDK adapters:** `java.awt.event.WindowAdapter` / `MouseAdapter` /
   `KeyAdapter` (since Java 1.1), and `GenericServlet` / `HttpServlet` in the
   Servlet API. Since Java 8, a **lambda** replaces the adapter pattern only
   when the target interface has a single abstract method; multi-method
   interfaces still need an adapter.
9. **Three ways to write a servlet:** implement `Servlet` (all five methods
   mandatory), extend `GenericServlet` (override only `service`), or extend
   `HttpServlet` (override `doGet`/`doPost`, not `service`) — the last is the
   everyday choice.
10. **`GenericServlet` is "more or less," not 100%, an adapter for
    `Servlet`** — a strict adapter's methods are all empty; several of
    `GenericServlet`'s carry real logic.

---

**Next:** Video 043 — Interface vs abstract class vs concrete class
