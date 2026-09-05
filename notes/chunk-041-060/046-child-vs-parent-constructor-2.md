# Video 046 — Child Object vs Parent Constructor (Part 2)

## Video info

**Title:** Java -  Interface and Abstract class Loopholes Part-3 || Child Object Vs Parent Constructor-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | 46 of 203 |
| Series | Interface and Abstract class Loopholes · Part 3 |
| Topic | Child Object Vs Parent Constructor-2 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 14m 08s |
| Video ID | o-naZqPsO9U |
| Watch | https://www.youtube.com/watch?v=o-naZqPsO9U |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is Part 3 of a three-part loophole on one question: when you create a
child class object, does a parent object get created too? Video 044 drew the
line between `new` and a constructor call; Video 045 (no usable YouTube
captions, so skipped in this note set) built a `Person`/`Student` example
arguing *why* the parent constructor has to run. This video is the
**empirical proof**: print `this.hashCode()` from inside both constructors
and from the child reference in `main`, and show all three prints match —
which is only possible if one object exists, not two.

1. The common (and wrong) textbook claim about child/parent object creation
2. A `hashCode()` experiment that would show *two* different values if the
   claim were true
3. The actual output — one value, three times
4. Why the misconception exists: confusing "constructor executed" with
   "object created"

---

## 00:32 — The doubt: does a child object also create a parent object?

Sir calls this "a bit dangerous" — a statement that shows up in classrooms and
textbooks everywhere: *whenever we create a child class object, a parent
object is automatically created too.* True or false?

He polls the room — a couple of hands for yes, most unsure — then asks
everyone to hold that answer and check it against a program instead of a
guess.

## 01:35 — Assume "yes," then test it with code

Assume the claim is true for now. Don't settle it by belief; settle it by
writing the program and reading the output.

## 01:53 — Board: build the experiment, piece by piece

`P`'s constructor prints its own hash code:

```java
class P {
    P() {
        System.out.println(this.hashCode());
    }
}
```

`C extends P`, with the identical print in the child constructor:

```java
class C extends P {
    C() {
        System.out.println(this.hashCode());
    }
}
```

`Test` creates one child object and prints its hash code too:

```java
class Test {
    public static void main(String[] args) {
        C c = new C();
        System.out.println(c.hashCode());
    }
}
```

Every object gets an identifying number from `hashCode()`. Print it from all
three places — `P`'s constructor, `C`'s constructor, and `main` — and compare.

> ❗ **Correction — "unique number" overstates the `hashCode()` contract.**
> `Object.hashCode()`'s only real guarantee (per its Javadoc) is that
> **equal objects return equal hash codes.** The reverse is never promised —
> two distinct, unequal objects are legally allowed to share a hash code (a
> collision). In this demo, three prints matching is evidence they are the
> *same* object, not proof by definition that unequal objects must differ.

## 03:28 — Both constructors run — the tempting wrong inference

Which object did we create? The **child** object. Creating it runs the child
constructor — yes — and it also runs the parent constructor — yes. Both
execute.

The wrong chain of logic that follows: child constructor ran, so a child
object exists; parent constructor ran, so a *parent* object exists too.
Assume that for the next step.

## 04:05 — If it were true, the two `this.hashCode()` prints should differ

Follow the assumption through. Inside `C`'s constructor, `this` is the object
under construction — the child object, say hash value **100**. `c.hashCode()`
in `main` refers to that same object, so it should also print **100**.

But inside `P`'s constructor, if a *separate* parent object had really been
created, `this` there would point to that separate object — with its own,
different hash code. So if the claim were true, the program should print
**two distinct values**, not one repeated three times.

## 05:31 — Typed live, compiled, and run

Same three classes, typed fresh in the editor, then compiled and executed:

```java
class P {
    P() {
        System.out.println(this.hashCode());
    }
}

class C extends P {
    C() {
        System.out.println(this.hashCode());
    }
}

class Test {
    public static void main(String[] args) {
        C c = new C();
        System.out.println(c.hashCode());
    }
}
```

```text
$ javac Test.java
$ java Test
2060468723
2060468723
2060468723
```

(Sir's board number is **100** as a stand-in for whatever large int the JVM
actually assigns — confirmed above by compiling and running this exact
program: the value repeats, whatever it is.)

## 07:21 — Same value, three times → only one object

One value, printed three times: from `P`'s constructor, from `C`'s
constructor, and from `main`. Same object, same hash, every time — not the
two different values the "parent object also gets created" theory predicted.

## 07:47 — Verdict: parent constructor executed, parent object never created

**Parent constructor executed. Parent object not created.** The parent
constructor ran, but it ran *for the child object* — there was never a second
object for it to belong to. Total objects created: one. Which one: the
child object.

> ⚠️ **Modern Java — this exact experiment does not port to a `record`.**
> `Object.hashCode()`'s identity-based default is unchanged since Java 1.0,
> so the proof itself is timeless. But since **Java 16**, a `record`
> auto-generates `hashCode()` from its **field values**, not identity, and a
> `record` implicitly extends the `final` class `java.lang.Record` — so it
> cannot `extends` another class at all. The `class C extends P` shape this
> proof depends on only exists for ordinary classes.

## 08:16 — Why the misconception persists

The root cause: people conflate "constructor runs" with "constructor creates
the object." It doesn't — `new` allocates the object; the constructor chain
only *initializes* it. Both parent and child constructors run for the sake of
the one child object, not because each constructor stamps out an object of
its own.

> ❗ **Correction — sharpen "constructor creates the object."**
> Allocation and initialization are two separate steps. `new C()` first
> allocates memory for one object and zero-fills its fields — identity, and
> therefore `hashCode()`, are already fixed at that point — and only *then*
> does the constructor chain run to assign field values. A constructor never
> allocates; it only initializes.
>
> It is also worth naming precisely why the parent constructor runs at all
> here: neither `C()` nor `P()` above writes `super(...)`. Every constructor's
> first statement is either an explicit `this(...)`/`super(...)` call or an
> implicit **no-arg `super()`** the compiler inserts automatically — which is
> why `P`'s print always executes before `C`'s, with no `super(...)` visible
> anywhere in this source.

## 08:48 — Conclusion, dictated to the board

> **Board:** Whenever we are creating a child class object, the parent
> constructor will be executed, but the parent object won't be created.

Some argue there's "no such terminology" as a constructor running without
creating its own object — the counter is simply this proof: the parent
constructor executes **for the child object's purpose only**.

## 10:13 — Recap with the board's own numbers

```java
class P {
    P() {
        System.out.println(this.hashCode()); // 100
    }
}

class C extends P {
    C() {
        System.out.println(this.hashCode()); // 100
    }
}

class Test {
    public static void main(String[] args) {
        C c = new C();
        System.out.println(c.hashCode()); // 100
    }
}
```

Whatever the number, it repeats in every case, because only one object was
ever created.

## 11:53 — One object, two constructors, restated

How many objects: **one**. How many constructors ran: **two** — parent and
child. Both ran **for that one child object.**

---

## Exam and interview points

1. **"Creating a child object also creates a parent object" is false.** `new
   C()` allocates exactly **one** object; the parent constructor runs against
   that same object, never a second one.
2. **The proof pattern**: print `this.hashCode()` from every constructor in
   the chain, plus from the reference in `main`. Identical values across all
   of them is the standard way to demonstrate "only one object exists."
3. **Constructor executed ≠ object created.** `new` allocates; the
   constructor chain (parent first, via explicit or implicit `super()`, then
   child) only initializes. This is the interview-ready phrasing of the rule.
4. **Every constructor's first statement is `this(...)`, `super(...)`, or a
   compiler-inserted no-arg `super()`.** That is the actual mechanism behind
   "the parent constructor always runs before the child constructor's body" —
   it is not special-cased for hash codes or object creation, it is how
   constructor chaining always works.
5. **`hashCode()` guarantees "equal objects → equal hash," never the
   reverse.** Do not describe it on an exam as a guaranteed-unique identifier;
   two unequal objects sharing a hash code is a legal collision, not a bug.
6. **A `record` cannot reproduce this demo.** It cannot `extends` another
   class (Java 16+), and its `hashCode()` is derived from field values, not
   identity — know this distinction if asked to contrast legacy classes with
   records.

---

**Next:** Video 047 — Need of Abstract Class Constructor
