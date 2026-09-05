# Video 063 — Instance + static control flow (mixed)

## Video info

**Title:** Core Java With OCJP/SCJP: OOPs(Object Oriented Programming) Part-13 || instance, static control flow

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 63 of 203 |
| Series | OOPs · Part 13 |
| Topic | instance, static control flow (mixed) |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 45m 29s |
| Video ID | KFKQNiOEepo |
| Watch | https://www.youtube.com/watch?v=KFKQNiOEepo |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Notes source | Local Whisper STT (no YouTube auto-captions) |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is **OOPs Part 13**, and it does two things. First it merges the static
control flow (Video 60) and instance control flow (Video 62) rules into one
combined procedure, drilled on three board programs — a hand-mixed `Test`,
then `Initialization` and `Initialization2` — with live-compiled outputs
`2 3 1` and `1 3 2`. Then it explains, with the JVM's own reasoning, why a
static context can never read an instance member directly, and closes with
the interview standard: the **five ways to obtain an object in Java** (`new`,
reflection, factory method, `clone()`, deserialization), each with a
one-line code sample. All three worked examples and the compiler message
below were re-compiled on a current JDK for this note and match exactly.

---

## 00:04 — Goal: mix instance + static control flow

Sir wants one example that mixes **instance control flow** and **static
control flow** so the class shows both kinds of members, then asks: in what
order does it all run?

### 00:15 — Board: class `Test` with both kinds of members

He builds `class Test` top to bottom: an instance block, a static block, a
constructor, `main` (which creates two objects), then a *second* static
block and a *second* instance block placed after `main`.

```java
class Test {
    {
        System.out.println("First instance block");
    }

    static {
        System.out.println("First static block");
    }

    Test() {
        System.out.println("Constructor");
    }

    public static void main(String[] args) {
        Test t1 = new Test();
        System.out.println("main");
        Test t2 = new Test();
    }

    static {
        System.out.println("Second static block");
    }

    {
        System.out.println("Second instance block");
    }
}
```

His point in stressing the scattered layout: instance block, static block,
constructor, `main`, another static block, another instance block —
everything mixed, on purpose. Can you predict the output?

### 02:30 — Walk the static control flow first

Whenever the class runs, **static control flow always goes first** (already
taught in Video 60):

1. Identification of static members, top to bottom.
2. Execution of static variable assignments and static blocks, top to bottom.
3. Execution of `main`.

Two static blocks exist — first and second — so step 2 prints:

```text
First static block
Second static block
```

Then `main` executes.

### 03:36 — First `new Test()` → instance control flow

Inside `main`: `Test t1 = new Test();`. Whenever an object is created:

1. Identification of instance members, top to bottom.
2. Execution of instance variable assignments and instance blocks, top to bottom.
3. Execution of the constructor.

Two instance blocks run in order, then the constructor:

```text
First instance block
Second instance block
Constructor
```

Object created. `main` then prints `"main"`.

### 04:22 — Second `new Test()` → instance control flow again

After `main` prints, `Test t2 = new Test();` runs the exact same
three-step instance procedure again:

```text
First instance block
Second instance block
Constructor
```

Verified end-to-end on a current JDK — this compiles and runs unchanged:

```java
// javac Test.java && java Test
First static block
Second static block
First instance block
Second instance block
Constructor
main
First instance block
Second instance block
Constructor
```

### 05:06 — Critical observation: one-time vs per-object

Mix instance and static control flow and the combined order above falls out
naturally — but one observation is compulsory:

- **Static control flow is a one-time activity** — once per class, at load.
- **Instance control flow is *not* one-time** — it runs again for every
  object. The first `new Test()` produced the instance prints once; the
  second `new Test()` produced them again.

### 05:35 — Same example, redictated

Sir rewrites the identical `Test` class on the board a second time purely so
students can copy it down as clean notes, then re-derives the same output
(`First static block, Second static block, First instance block, Second
instance block, Constructor, main, First instance block, Second instance
block, Constructor`). No new information — just make sure your notes have
the example and its output, and that you can derive the order yourself.

### 08:00 — Next board example: `Initialization.java`

A second, tighter example, written on the board as `Initialization.java`:

```java
public class Initialization {
    private static String m1(String msg) {
        System.out.println(msg);
        return msg;
    }

    public Initialization() {
        m = m1("1");
    }

    {
        m = m1("2");
    }

    String m = m1("3");

    public static void main(String[] args) {
        Object obj = new Initialization();
    }
}
```

`m1` is a **static** helper: called with a string, it prints that string and
returns it unchanged — a way to make the execution order visible on screen.

### 10:55 — Static steps for `Initialization`

Step 1, identification of static members, top to bottom: only **two** exist
— `m1` and `main`.

Step 2, execution of static variable assignments and static blocks: nothing
here — no static variables, no static blocks.

Step 3: execute `main`. Inside it, `new Initialization()` starts instance
control flow.

### 11:29 — Instance control flow for `Initialization`

Identification of instance members, top to bottom — **three**:

1. The constructor.
2. The instance block (`m = m1("2")`).
3. The instance variable `String m = m1("3")`.

Execution of instance variable assignments and instance blocks, top to
bottom (not counting the constructor yet):

- `m` is a `String`, so its JVM default is **`null`** before anything runs.
- The instance block comes first in source order → `m = m1("2")` prints
  **`2`**, returns `"2"`, `m` becomes `"2"`.
- Then the instance variable assignment → `m = m1("3")` prints **`3`**, `m`
  becomes `"3"`.

Last step, the constructor: `m = m1("1")` prints **`1`**.

**Output: `2`, `3`, `1`.** Order: instance block → instance variable
initializer → constructor, always in that fixed sequence regardless of how
they're arranged on the page.

```java
// javac Initialization.java && java Initialization
2
3
1
```

Sir compiles and runs it live; the terminal agrees — `2 3 1`. Re-verified on
a current JDK for this note: identical output.

### 15:39 — Pause: mixed flows drive the order

One line of recap before moving on: when instance and static control flow
mix, you drive the execution order yourself using the two three-step
procedures above. Output for this demo: **2, 3, 1**.

### 17:02 — Next example: `Initialization2.java`

Same idea, different mix — this time a static variable, an instance block,
and a static block are interleaved.

```java
public class Initialization2 {
    private static String m1(String msg) {
        System.out.println(msg);
        return msg;
    }

    static String m = m1("1");

    {
        m = m1("2");
    }

    static {
        m = m1("3");
    }

    public static void main(String[] args) {
        Object obj = new Initialization2();
    }
}
```

### 19:53 — Static control flow for `Initialization2`

Identification of static members, top to bottom — **four**: `m1`, the
static variable `m`, the static block, `main`.

Execution of static variable assignments and static blocks, top to bottom —
note this step **skips the instance block sitting between them**:

- `static String m = m1("1")` → prints **`1`**, `m` becomes `"1"`.
- `static { m = m1("3"); }` → prints **`3`**, `m` becomes `"3"`.

Then `main` executes.

### 21:10 — Object creation → only one instance member

Inside `main`, `new Initialization2()` starts instance control flow.
Identification of instance members: only **one** — the instance block (there
is no explicit constructor, no instance variable).

Execution: `m = m1("2")` prints **`2`**, `m` becomes `"2"`.

Then the (default, silent) constructor executes.

**Output: `1`, `3`, `2`.** The static phase — variable *and* block — always
finishes completely before the instance phase begins, no matter how the two
kinds of member are interleaved in the source.

```java
// javac Initialization2.java && java Initialization2
1
3
2
```

Sir compiles and runs it live — same answer, `1 3 2`. Re-verified on a
current JDK: identical.

### 23:03 — Dictation wrap on mixed flows

One more pass making sure the `Initialization2` shape and its `1, 3, 2`
output are written down correctly before moving to the next topic.

### 25:05 — Important conclusion: why static cannot touch instance directly

A very important internal-reasoning question:

```java
class Test {
    int x = 10;

    public static void main(String[] args) {
        System.out.println(x);
    }
}
```

"Don't overthink it" — this is a compile error, already covered several
times: **from a static area you cannot access an instance member
directly.**

The internal reason, in control-flow terms:

1. Identification of static members — here, only `main`.
2. Execution of static assignments/blocks — none.
3. Execute `main` → `System.out.println(x)`.

At that moment the JVM has not identified instance member `x` yet — `x` is
only identified **when an object is created**, and none has been. Hence the
compile error:

```java
class Test {
    int x = 10;

    public static void main(String[] args) {
        System.out.println(x);
    }
}
// CE: non-static variable x cannot be referenced from a static context
```

Verified verbatim against `javac` today — this is the exact message,
unchanged across every Java version tested.

### 27:53 — Fix: create the object, then access via reference

```java
class Test {
    int x = 10;

    public static void main(String[] args) {
        Test t = new Test();
        System.out.println(t.x);
    }
}
// java Test
// prints 10
```

Perfectly valid: creating the object makes the JVM identify instance
members, so `t.x` is `10`.

**Note (dictation):** from a static area you cannot access instance members
**directly**, because while a static area is executing, the JVM may not yet
have identified instance members — those are identified only when an object
is created.

---

## 31:04 — Interview bit: in how many ways can we get an object in Java?

A very important interview question, phrased carefully: **in how many ways
can we *create* / *get* an object in Java?** ("Get" is more accurate than
"create" — some of the ways below don't run `new` at all.) There are
**standard** ways — Sir commits to five; some books pad the count to six,
seven, or eight purely for variety, which he calls out and rejects below.

### 32:42 — Way 1: `new` operator

The best-known approach:

```java
Test t = new Test();
```

### 33:13 — Way 2: `newInstance()` (Reflection API)

```java
Test t = (Test) Class.forName("Test").newInstance();
```

What happens: `Class.forName("Test")` loads the `Test` class and produces a
`Class` object; calling `newInstance()` on *that* object (a method declared
in class `Class`) returns a new `Test` instance — typed as `Object`, so a
cast is required. (The difference between `new` and `newInstance()` was
covered back in the operators chapter.)

> ⚠️ **Modern Java — `Class.newInstance()` is deprecated.**
> Since **Java 9**, `Class.newInstance()` carries `@Deprecated`. Its flaw:
> it rethrows any exception the constructor throws — checked or not —
> without wrapping it, silently breaking the checked-exception contract the
> compiler is supposed to enforce. The replacement goes through
> `Constructor` instead, which wraps constructor failures in
> `InvocationTargetException`:
> ```java
> Test t = (Test) Class.forName("Test")
>                       .getDeclaredConstructor()
>                       .newInstance();
> ```
> Sir's form still compiles and still runs (with a deprecation warning) —
> the "get an object via reflection" idea he's teaching hasn't changed,
> only the recommended entry point has.

### 34:36 — Way 3: factory methods

A **factory method**: call a method by class name, and it returns an object
of that same class, without the caller writing `new` or `newInstance()`.
Programmer-friendly.

```java
Runtime r = Runtime.getRuntime();
```

`Runtime.getRuntime()` returns a `Runtime` object. It may use `new`
internally, but from the caller's point of view you got the object through
a method call — that's what makes it a factory method.

```java
DateFormat df = DateFormat.getInstance();
```

Same shape: call `DateFormat.getInstance()` by class name, get back a
`DateFormat` object.

> ⚠️ **Modern Java — prefer `java.time` for new date/time code.**
> `DateFormat`/`SimpleDateFormat` still compile and run exactly as shown —
> this example is only illustrating "factory method," not endorsing the
> API. Since **Java 8**, `java.time` (JSR-310) — `DateTimeFormatter`,
> `LocalDate`, `LocalDateTime` — is the recommended, thread-safe
> replacement for new date-handling code; `DateFormat` is not deprecated,
> but it is legacy.

### 36:14 — Way 4: `clone()` method

Given an existing `Test` object, `clone()` produces an exact duplicate:

```java
Test t1 = new Test();
Test t2 = (Test) t1.clone();
// only compiles if Test implements Cloneable and overrides
// clone() as public (Object.clone() itself is protected)
```

### 37:13 — Way 5: deserialization

**Deserialization** also gets you an object. Full mechanics are a later
chapter (streams: an output stream to *write* an object, an input stream to
*read* one) — this is only a sketch, not a complete compiling example:

```java
FileInputStream fis = new FileInputStream("abc.ser");
ObjectInputStream ois = new ObjectInputStream(fis);
Dog d2 = (Dog) ois.readObject();
```

Calling `readObject()` reconstitutes the object from the stream.

> ⚠️ **Modern Java — deserialization gained a security gate.**
> Since **Java 9** (JEP 290), `ObjectInputStream` supports
> `ObjectInputFilter`, which can restrict which classes a stream is allowed
> to reconstitute. The mechanism Sir shows is unchanged — `readObject()`
> still works exactly like this — but unrestricted deserialization of
> untrusted input is a well-known remote-code-execution vector, and
> production code reading data it doesn't fully control should configure a
> filter (or avoid Java serialization for that data entirely).

### 39:09 — Standard five; ignore non-standard "extra" counts

The standard five:

1. `new` operator
2. `newInstance()` method
3. Factory method
4. `clone()` method
5. Deserialization

Sir explicitly rejects padding the count with non-general tricks:

- A special `String` literal style is not a general way — it applies only
  to `String`.
- `Integer i = 10;` (autoboxing) is not a sixth way — internally it's
  `Integer.valueOf(10)`, which is already the factory-method idea, not a
  new concept.

`new`, `newInstance()`, `clone()`, and deserialization all apply across
classes generally, which is why they make the standard list and the other
two don't.

**Interview answer: 5 ways**, and sample code is expected for each.

### 41:12 — Final dictation of the five ways

| # | Way | Sample |
|---|---|---|
| 1 | `new` operator | `Test t = new Test();` |
| 2 | `newInstance()` method | `Test t = (Test) Class.forName("Test").newInstance();` |
| 3 | Factory method | `Runtime r = Runtime.getRuntime();` |
| 4 | `clone()` method | `Test t2 = (Test) t1.clone();` |
| 5 | Deserialization | `Dog d2 = (Dog) ois.readObject();` |

### 45:06 — Close

What to take from this session: the mixed instance + static control-flow
order, the `Initialization` / `Initialization2` output questions (`2 3 1`
and `1 3 2`), why static code can't see instance members without an object,
and the five standard ways to obtain an object in Java.

---

## Exam and interview points

1. **Static control flow always runs before instance control flow, and
   always completes fully first** — even when static and instance members
   are physically interleaved in the source, as in `Initialization2`.
2. **Static control flow is one-time** (once per class, at load); **instance
   control flow is not** — it repeats, in full, on every `new`.
3. Both procedures are three steps: identify members top to bottom → run
   variable assignments and blocks top to bottom → run `main` (static) or
   the constructor (instance).
4. **`Initialization` → `2, 3, 1`**: instance block, then instance-variable
   initializer, then constructor — that fixed order, regardless of their
   order on the page.
5. **`Initialization2` → `1, 3, 2`**: static variable, then static block
   (both during the one static phase) — the instance block sitting between
   them in the source does not run until an object is later created.
6. **A static context cannot read an instance member directly** —
   `non-static variable x cannot be referenced from a static context` —
   because instance members aren't identified until an object exists.
   Through an object reference (`t.x`), it's completely valid.
7. **Five standard ways to obtain an object in Java**: `new`, reflection
   (`newInstance()`), factory method, `clone()`, deserialization.
   Autoboxing and String-literal syntax are not extra ways — they route
   through the factory-method idea or are String-only, respectively.
8. **`Class.newInstance()` has been deprecated since Java 9** — modern code
   uses `Class.getDeclaredConstructor().newInstance()`, which correctly
   wraps constructor exceptions instead of rethrowing them unchecked.

---

**Next:** Video 064 — Constructors
