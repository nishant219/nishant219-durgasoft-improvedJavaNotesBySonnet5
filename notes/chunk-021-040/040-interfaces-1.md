# Video 040 — Interfaces Part 1

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-11|| interfaces-1

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 40 of 203 |
| Series | Declarations and Access Modifiers · Part 11 |
| Topic | interfaces-1 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 11m 33s |
| Video ID | sEH6BDCS3do |
| Watch | https://www.youtube.com/watch?v=sEH6BDCS3do |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (YouTube had no usable auto-captions) |

> **How to read these notes.** This upload had no usable YouTube captions, so
> the transcript is a local Whisper pass on the audio — noisier than the
> auto-captions used elsewhere, and timestamps are approximate. Sections
> follow Durga Sir's board order. Two kinds of callout interrupt the lecture
> where it needs it: **⚠️ Modern Java** — what Sir taught was right for Java
> 6/7, and has since changed. **❗ Correction** — what was stated is not
> accurate, then or now. Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Interfaces is a big enough topic that Sir splits it across several videos.
The full plan, as he boards it:

1. Introduction — what is an interface? ← *this video*
2. Interface declaration and implementation ← *this video*
3. `extends` versus `implements` ← *this video*
4. Interface methods (detailed discussion)
5. Interface variables (purpose, applicable modifiers)
6. Interface naming conflicts (method conflicts, variable conflicts)
7. Marker interfaces — "very important for interview"
8. Adapter classes
9. Interface vs abstract class vs concrete class
10. Differences between interface and abstract class
11. Conclusions

Items 4–11 continue in Video 041 onward. This video's own centre of gravity is
the interview question "can you define what is an interface?" — Sir gives
three definitions plus a summary answer, then the mechanical rules for
declaring, implementing, extending, and combining interfaces.

---

## 00:02 — Agenda

Sir frames marker interfaces and "interface vs abstract class" as the two
highest-value interview topics in the whole block, and promises to build up to
them across the coming videos.

## 05:17 — Introduction: "Can you define what is an interface?"

Sir's interview trap: candidates give *one* correct definition, but the
interviewer had a different one in mind and isn't satisfied. He lists the
definitions people reach for — "collection of only abstract methods,"
"requirement specification," "contract between client and service provider,"
"100% pure abstract class" — and says all of them are valid, just from
different angles. His plan: cover all of them, then give one summary
definition that always contains whatever the interviewer expected.

## 07:25 — Definition 1: Service requirement specification (SRS)

> Any **service requirement specification** is, by default, considered an
> **interface**.

**Example — JDBC API.** The JDBC API is a requirement specification for a
database driver; database vendors implement it.

```java
interface Connection {
    void close();   // one of the methods JDBC's spec requires
}

class OracleConnection implements Connection {
    public void close() { /* Oracle-specific */ }
}

class MysqlConnection implements Connection {
    public void close() { /* MySQL-specific */ }
}

class Db2Connection implements Connection {
    public void close() { /* DB2-specific */ }
}
```

The Java community defines the JDBC API; each database vendor implements it to
produce its own driver. "API" is literally *Application Programming
**Interface***.

## 13:25 — Example 2: Servlet API

Same pattern, one level up: the **Servlet API** is a requirement specification
for a web server, and the **web server vendor** implements it.

```java
interface Servlet {
    void service();
}

class TomcatServletContainer implements Servlet {
    public void service() { /* Apache Tomcat */ }
}

class WeblogicServletContainer implements Servlet {
    public void service() { /* BEA, later Oracle */ }
}

class WebsphereServletContainer implements Servlet {
    public void service() { /* IBM */ }
}
```

Sir's portability story: deploy a web app on Tomcat, it works; redeploy the
same app, unchanged, on WebLogic, then WebSphere — both work. Every vendor
implemented the same Servlet API, so client code that depends only on the
interface never cares which one is underneath:

```java
class MyWebApp {
    void handle(Servlet container) {
        container.service();
    }
}
```

**Definition 1, restated:** any requirement specification is, by default, an
interface.

## 18:33 — Definition 2: Contract between client and service provider

A client (a college) wants a college automation system with ~100 expected
services — `getAttendance`, `getMarks`, `updateMarks`, and so on. That set of
expected services *is* the requirement specification, and from the client's
side it *is* the interface. A service provider agrees to implement all of it —
that agreement is the contract.

```java
interface CollegeAutomation {
    void getAttendance();
    void getMarks();
    void updateMarks();
    // ... the rest of the ~100 services in the SRS
}

class CollegeAutomationImpl implements CollegeAutomation {
    public void getAttendance() { /* ... */ }
    public void getMarks()      { /* ... */ }
    public void updateMarks()   { /* ... */ }
}
```

| Perspective | Interface means |
|---|---|
| Client | the set of services expected |
| Service provider | the set of services offered |

**Definition 2:** any contract between client and service provider is, by
default, an interface.

Sir's classroom analogy: paying course fee for an OCJP batch is a contract for
~20 topics. Teach only 10, and the contract is broken — a student can refuse
to accept it. The same idea, in code shape:

```java
interface OcjpCourse {
    void topic1();
    void topic2();
    // ... about 20 topics total, per the syllabus
}

class DurgaSoftBatch implements OcjpCourse {
    public void topic1() { /* covered */ }
    public void topic2() { /* covered */ }
    // leaving a topic unimplemented breaks the "contract"
}
```

## 24:15 — The ATM GUI screen (same Definition 2, a second angle)

A bank ATM's GUI shows Withdraw, Mini Statement, Balance Enquiry. That one
screen is simultaneously the set of services the **customer expects** and the
set of services the **bank offers** — which is exactly the contract idea.

```java
interface AtmServices {
    void withdraw();
    void miniStatement();
    void balanceEnquiry();
}

class BankAtm implements AtmServices {
    public void withdraw()       { /* debit, dispense cash */ }
    public void miniStatement()  { /* ... */ }
    public void balanceEnquiry() { /* ... */ }
}
```

Two stories illustrate where responsibility sits:

- **Withdraw fails mid-transaction, account already debited.** The bank is
  responsible — withdraw is a service it offers — and the standard response is
  a refund within 24 hours or a branch visit.
- **A customer leaves cash in an envelope for "deposit" at a no-deposit ATM.**
  The bank is *not* responsible — deposit was never an offered service, so it
  was never part of the contract.

```java
interface AtmServicesNoDeposit {
    void withdraw();
    void miniStatement();
    void balanceEnquiry();
    // no deposit() — a customer cannot claim a service that isn't offered
}
```

**Board conclusion:** the ATM GUI shows what the bank offers and what the
customer expects on one screen — that overlap is the contract, which is the
interface.

## 32:03 — Definition 3: 100% pure abstract class

> Inside an interface, every method is always abstract — whether you write
> `abstract` or not.

Hence an interface is also a **100% pure abstract class**; some textbooks
phrase it exactly that way round.

```java
interface Interf {
    void m1();   // implicitly public abstract
    void m2();   // implicitly public abstract
}

abstract class PureAbstract {   // the same idea, spelled out with abstract classes
    public abstract void m1();
    public abstract void m2();
}
```

> ❗ **Correction — "every method is always abstract" stopped being true in
> Java 8.**
> This was a completely accurate description of interfaces through Java 7,
> which is the version this lecture teaches. Since **Java 8**, an interface
> can declare **`default`** and **`static`** methods that carry a real body —
> not abstract at all — and since **Java 9**, **`private`** interface methods
> too (helpers for default methods to share code without exposing it):
>
> ```java
> interface Modern {
>     void m1();                  // still implicitly public abstract
>
>     default void m2() {         // Java 8 — has a body, not abstract
>         System.out.println("default body");
>     }
>
>     static void m3() {          // Java 8 — has a body, not abstract,
>         System.out.println("static body");   // and not inherited by implementers
>     }
>
>     private void helper() {     // Java 9 — body-only helper, interface-private
>         System.out.println("private helper");
>     }
>
>     default void m4() {
>         helper();
>     }
> }
>
> class Impl implements Modern {
>     public void m1() { }        // only the abstract method needs overriding
> }
> ```
>
> `new Impl().m2()` and `new Impl().m4()` both run without `Impl` overriding
> anything, and `Modern.m3()` is called on the interface itself, like a static
> method on a class. So "100% pure abstract class" is no longer literally true
> of every interface — it is exactly true of an interface that sticks to
> abstract methods only (the shape the OCJP exam this course targets cares
> about, and what a **functional interface** is). Video 041 in this series
> covers interface methods — including this default/static/private split — in
> depth.

## 33:54 — Why a summary definition? (the interview mismatch)

Answer only with Definition 1 when the interviewer expected Definition 3 (or
vice versa), and they may not be satisfied even though your answer was
correct. Sir's fix: fold all three into one sentence so the expected idea is
always present.

**Summary definition, worth memorising verbatim:**

> **Board:** Any service requirement specification, or any contract between
> client and service provider, or a 100% pure abstract class, is nothing but
> an interface.

```java
/*
 * Interface =
 *   SRS (service requirement specification)
 *   OR contract between client & service provider
 *   OR 100% pure abstract class
 */
interface SummaryMeaning {
    void service();
}
```

---

## 36:53 — Interface declaration and implementation

```java
interface Interf {
    void m1();
    void m2();
}
```

A client has two required services, `m1` and `m2`. First attempt at a service
provider class — deliberately wrong, so the mistakes can be counted:

```java
// FIRST ATTEMPT — wrong on two separate counts
class ServiceProvider implements Interf {
    void m1() {
        // only m1, and not public
    }
}
```

Sir's framing: **how many mistakes**, not just "is this wrong" — because each
mistake is its own exam-worthy conclusion. Answer: **two mistakes, two
compile-time errors.**

### 39:35 — Mistake 1: implement every method, or mark the class `abstract`

If a class `implements` an interface, it must implement **every** method of
that interface — or declare itself `abstract` and push the remaining methods
onto its child classes.

```java
interface Interf {
    void m1();
    void m2();
}

class ServiceProvider implements Interf {
    public void m1() {
    }
    // missing m2() —
    // CE: ServiceProvider is not abstract and does not override
    //     abstract method m2() in Interf
}
```

Fix, when only some methods are ready now:

```java
interface Interf {
    void m1();
    void m2();
}

abstract class ServiceProvider implements Interf {
    public void m1() {
    }
    // m2 stays abstract — a child class is responsible for it
}
```

### 40:45 — Mistake 2: an implementing method must be `public`

Every interface method is always `public` and `abstract`, whether you write
those words or not. Implementing it is **overriding**, and overriding can
never *reduce* the access modifier's scope — so the override must be `public`
too.

```java
interface Interf {
    void m1();   // public abstract by default
}

class ServiceProvider implements Interf {
    void m1() {
        // CE: m1() in ServiceProvider cannot implement m1() in Interf;
        //     attempting to assign weaker access privileges; was public
    }
}
```

Fix:

```java
interface Interf {
    void m1();
}

class ServiceProvider implements Interf {
    public void m1() {   // public is compulsory here
    }
}
```

Both mistakes were verified against `javac` — the errors above are the actual
compiler output, not paraphrase.

### 42:03 — Working through both errors together, then one at a time

Board sequence: start from the doubly-wrong class, fix one problem, watch the
other error remain, fix that too.

```java
interface Interf {
    void m1();
    void m2();
}

class ServiceProvider implements Interf {
    void m1() {
    }
}
// two errors: ServiceProvider is not abstract (missing m2), AND
//             m1() has weaker access than Interf's public m1()
```

Declare the class `abstract` — the "missing m2" error disappears, one error
remains:

```java
abstract class ServiceProvider implements Interf {
    void m1() {
    }
}
// one error left: m1() weaker access than public
```

Make `m1` public — compiles clean. `m2` is now some child class's problem:

```java
abstract class ServiceProvider implements Interf {
    public void m1() {
    }
}
```

### 44:01 — The child class must implement what's left

```java
interface Interf {
    void m1();
    void m2();
}

abstract class ServiceProvider implements Interf {
    public void m1() {
    }
}

class SubServiceProvider extends ServiceProvider {
}
// CE: SubServiceProvider is not abstract and does not override
//     abstract method m2() in Interf
```

Fix:

```java
class SubServiceProvider extends ServiceProvider {
    public void m2() {
    }
}
```

Compiles — no problem.

### 45:26 — The two rules, repeated for memory

1. Implementing an interface means implementing **every** method, or the
   class must be declared `abstract` so a subclass can finish the job.
2. Every interface method is `public abstract` by default; an overriding
   method must be declared `public` explicitly, or the compiler rejects it as
   a scope reduction.

```java
interface Interf {
    void m1();
    void m2();
}

abstract class ServiceProvider implements Interf {
    public void m1() { }
}

class SubServiceProvider extends ServiceProvider {
    public void m2() { }
}
```

---

## 51:42 — `extends` versus `implements`

Sir's warning: this looks simple, and yet most people still get it wrong —
worth extra care.

### 1) A class can extend only one class at a time

```java
class A { }
class B { }

class C extends A { }   // valid — one superclass

// class D extends A, B { }
// CE (syntax): '{' expected — a class cannot list two superclasses
```

### 2) An interface can extend any number of interfaces at once

This is *why* Java supports multiple inheritance for interfaces:

```java
interface A { }
interface B { }
interface D { }

interface C extends A, B, D { }   // perfectly valid
```

### 3) A class can implement any number of interfaces at once

```java
interface A { }
interface B { }
interface C { }

class Test implements A, B, C {
}
```

### 4) A class can extend a class *and* implement interfaces, together

```java
class Parent { }
interface I1 { }
interface I2 { }

class Child extends Parent implements I1, I2 {
}
```

### 54:29 — The four valid combinations, boarded together

1. A class can extend **only one** class at a time.
2. An interface can extend **any number** of interfaces at once.
3. A class can implement **any number** of interfaces at once.
4. A class can extend one class **and** implement any number of interfaces, at
   the same time.

## 58:03 — BIT/MCQ drill: which claim is valid?

Sir flips the framing to false statements — every one of these is invalid:

| # | Claim | Verdict | Why |
|---|---|---|---|
| 1 | A class can extend any number of classes at a time | ❌ Invalid | only one superclass allowed |
| 2 | A class can implement only one interface at a time | ❌ Invalid | a class can implement any number |
| 3 | An interface can extend only one interface at a time | ❌ Invalid | an interface can extend any number |
| 4 | An interface can implement another interface | ❌ Invalid | interfaces *extend* interfaces; they never `implement` |
| 5 | A class can extend a class *or* implement an interface, but never both | ❌ Invalid | both together are allowed |
| 6 | None of the above | ✅ **Correct** | every prior claim was false |

```java
// counters to claims 2–4, in order
interface I1 { }
interface I2 { }
class Test implements I1, I2 { }        // counters claim 2

interface A { }
interface B { }
interface C extends A, B { }            // counters claim 3

// interface B2 implements A { }
// CE (syntax): '{' expected — an interface cannot implement, only extend

class X extends Object implements I1 { } // counters claim 5 (implicit — extends + implements together)
```

## 1:01:42 — Exam pattern: `X extends Y`

For which X and Y is `X extends Y` valid?

| Option | Claim | Verdict |
|---|---|---|
| 1 | Both X and Y must be classes | Incomplete — interfaces work too |
| 2 | Both X and Y must be interfaces | Incomplete — classes work too |
| 3 | Both X and Y can be either classes or interfaces (matching kind) | ✅ Correct |
| 4 | No restriction at all | Wrong |

```java
class Y { }
class X extends Y { }        // both classes — valid

interface Y2 { }
interface X2 extends Y2 { }  // both interfaces — valid

// interface X3 extends Y { }
// CE (syntax): interface expected here — an interface cannot extend a class

// class X4 extends Y2 { }
// CE (syntax): no interface expected here — a class cannot extend an interface
```

Mixing kinds always fails — X and Y must be the same kind of thing.

## 1:06:30 — More `extends` / `implements` combinations

#### `X extends Y, Z`

Valid only when X, Y, and Z are all interfaces (a class can never list two
things after `extends`):

```java
interface Y { }
interface Z { }
interface X extends Y, Z { }   // valid — all interfaces
```

#### `X implements Y, Z`

X must be a class; Y and Z must be interfaces:

```java
interface Y { }
interface Z { }
class X implements Y, Z {
}
```

#### `X extends Y implements Z`

X and Y must be classes; Z must be an interface:

```java
class Y { }
interface Z { }
class X extends Y implements Z {
}
```

#### `X implements Y extends Z` — always invalid

`extends` must come before `implements` in a class header — there is no
ordering under which this compiles:

```java
interface Y { }
class Z { }

// class X implements Y extends Z { }
// CE (syntax): '{' expected — implements cannot precede extends
```

### 1:09:36 — The full recap

| Expression | What X / Y / Z must be |
|---|---|
| `X extends Y` | both classes, or both interfaces |
| `X extends Y, Z` | all interfaces |
| `X implements Y, Z` | X a class; Y, Z interfaces |
| `X extends Y implements Z` | X, Y classes; Z an interface |
| `X implements Y extends Z` | always a syntax error — wrong keyword order |

```java
interface I1 { }
interface I2 { }
interface I3 extends I1, I2 { }

class C1 { }
class C2 extends C1 { }
class C3 extends C1 implements I1, I2 { }
```

## 1:10:18 — Closing

This video completes: what an interface is (three definitions plus a summary),
declaration and implementation (the two rules), and `extends` versus
`implements` (valid forms, invalid forms, and the exam-style `X extends Y`
questions). Interface methods in depth, interface variables, naming
conflicts, marker interfaces, adapter classes, and interface-vs-abstract-class
continue in later videos.

---

## Quick revision sheet

**Definition (say all three, or the summary):**

| # | Definition | Angle |
|---|---|---|
| 1 | Any service requirement specification (SRS) | how a spec becomes an interface (JDBC, Servlet API) |
| 2 | Any contract between client and service provider | what the client expects = what the provider offers |
| 3 | 100% pure abstract class | true for Java 6/7; only partly true from Java 8 onward |

**Implementing an interface — two rules:**

1. Implement **every** method, or declare the class `abstract`.
2. Every implemented method must be **`public`** — interface methods are
   `public abstract` by default, and overriding can't narrow that.

**`extends` / `implements` — four valid shapes:**

| Shape | Rule |
|---|---|
| `class extends class` | at most **one** superclass |
| `interface extends interface, …` | **any number** of interfaces |
| `class implements interface, …` | **any number** of interfaces |
| `class extends class implements interface, …` | both together, `extends` first |

**Order rule:** `extends` always precedes `implements` in a class header —
`implements X extends Y` never compiles, in any context.

---

## Exam and interview points

1. **Give the summary definition, not just one of the three.** SRS, or a
   contract between client and service provider, or a 100% pure abstract
   class — say all of it, so whichever the interviewer expects is covered.
2. **Implementing an interface: implement every method, or go `abstract`.**
   Skipping a method without marking the class `abstract` is a compile error
   naming the exact missing method.
3. **Every abstract interface method is `public` by default — the override
   must say `public` explicitly**, or it is rejected as reducing access from
   `public` to default.
4. **A class extends at most one class, but can implement any number of
   interfaces** — this asymmetry is why Java gets multiple inheritance
   through interfaces, not classes.
5. **An interface extends any number of interfaces — it never `implements`.**
   Only classes use `implements`.
6. **When a class header uses both, `extends` must come before
   `implements`** — the reverse order is a syntax error, not a semantic one.
7. **`X extends Y` needs matching kinds** — both classes, or both interfaces,
   never mixed; use `implements` to connect a class to an interface.
8. **"100% pure abstract class" was exactly true through Java 7.** Since
   Java 8, interfaces can carry `default` and `static` methods with real
   bodies, and since Java 9, `private` helper methods too — know this before
   an interviewer follows up with "so can an interface have a method body?"

---

**Next:** Video 041 — Interface methods (and related board work)
