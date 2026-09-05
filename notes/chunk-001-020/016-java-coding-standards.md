# Video 016 — Java Coding Standards

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-16 || Java Coding Standards

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 16 of 203 |
| Series | Language Fundamentals · Part 16 of 16 (this part closes Language Fundamentals) |
| Topic | Java coding standards / naming conventions (classes, interfaces, methods, variables, constants, packages, JavaBeans getXxx/setXxx/isXxx, listeners addXxx/removeXxx) plus the interview-story framing |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 08m 38s (4118 seconds) |
| Video ID | -w4QphWnlZo |
| Watch | https://www.youtube.com/watch?v=-w4QphWnlZo |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

This upload is one file, two classroom sittings: an interview-story
introduction (~19 minutes), then a recap and the per-component rules through
listeners.

## What this lecture covers

1. Why coding standards exist (readability + maintainability)
2. The interview story: 3.6 years "experience," the two-integer-sum class,
   Ameerpet vs Hi-Tech City
3. Package-first rule and reverse-domain package names
4. Public class, `static` when there is no instance state, meaningful names
5. `Math.sqrt` / `Math.max` as the payoff of meaningful names
6. Board rules for **classes, interfaces, methods, variables, constants**
7. How constants are declared (`public static final`)
8. JavaBean definition, getter/setter syntax, and why "ends with `Bean`" is
   **not** an official Sun convention
9. **Exam twist:** for a boolean property, both `getEmpty` and `isEmpty` are
   valid; `is` is only the recommendation
10. Listener coding standards: register with `add`, unregister with
    `remove`, and the type named after the prefix must match the argument type
11. Close of Language Fundamentals

---

## 00:03 — Why coding standards exist

Whenever we write code — a class, a method, anything — we **must** follow
coding conventions. Readability and maintainability improve by default when
we do. Sir builds the case with a long interview story first (the *need*),
then gives the official-style rule for each component.

## 01:05 — Interview framing: checking your "original color"

You walk into the interview room with **2+ or 3+ years** of experience.
Assume **3.6 years**. The interviewer asks a couple of questions that feel
irritating or silly, but they decide whether you are coming from
**Ameerpet** (the Hyderabad institute / fake-project culture), from a real
software company, or whether the experience is original or fabricated.
Sir's framing: these two minutes decide your **original color**.

Script:

1. "How much experience do you have?" → "3.6 years."
2. "Is your total experience Java experience?" → "Yes, entirely Java."
3. Then, to check the color: "You have 3.6 years — do you know how to write
   a Java program, how to write a Java class?"

The requirement is tiny: write a **class**, with one **method**, that takes
**two `int` arguments** and **returns their sum**. Nothing more. Irritated at
being asked something so basic, you want to show caliber and slap something
on the board in two or three seconds.

**Telugu proverb he uses:** to check whether rice is cooked
(*anna manta udikindo ledo chudali*), you do not inspect the whole pot —
**one grain** (*oka metuku*) is enough. Same here: checking your original
color does not need a two-hour interview. One minute of code is enough.

### 03:14 — What most people write (the "Ameerpet" version)

```java
class A {
    public int m1(int x, int y) {
        return x + y;
    }
}
```

You show it — "here's your requirement, have a look" — and without waiting a
nanosecond the interviewer says, very politely: *"Can you please go out? If
there is a requirement, I will let you know."* A person with real 3.6 years
of experience never writes code that looks like this, and that is enough for
the interviewer to have already decided your color.

## 05:20 — How a real 3.6-year developer writes it: seven red flags

Sir now rebuilds the same class piece by piece. Every defect in
`class A { int m1(int x, int y) }` is its own red flag.

### Flag 1 — no package statement

Every Java source file must, as a rule, open with a `package` statement.
Comments can appear anywhere; other than comments, the **first real
statement must be `package`**. The Java API has 5,000+ classes, and not one
of them lacks a package:

| Class | Package |
|---|---|
| `String` | `java.lang` |
| `File` | `java.io` |
| `ArrayList` | `java.util` |

Every class belongs to some package — yours should too. If a candidate's
code doesn't start with `package`, that alone is enough to flag "no
real-time experience."

### Flag 2 — dummy package names

Most people, if they remember `package` at all, write `pack1`, `pack2`,
`packX`. The universally accepted convention is the **client's internet
domain name, reversed, plus a module name**:

```java
package com.durgasoft.scjp;
```

`com.durgasoft` reverses `durgasoft.com`; `scjp` names the module.

> ⚠️ **Modern Java — packages now nest inside modules, but the naming rule is unchanged.**
> Since **Java 9** (the Java Platform Module System, JPMS), a project can add
> a `module-info.java` that declares which packages it `exports` and which
> modules it `requires`. That is a layer on top of packages, not a
> replacement for them — the reverse-domain naming convention for the
> package itself is exactly what Sir teaches here, module system or not.

### Flag 3 — class not `public`

Code that several people need to use should be reachable by them —
`public class`, not `class A`.

### Flag 4 — meaningless class name

`class A`, `class B`, `class X`, `class Y` are what Sir calls "Ameerpet
colors" — do not show these in an interview room. The rule: a class name
should represent the component's purpose. This class does arithmetic, so it
becomes:

```java
public class Calculator
```

"Sir, I have a `Calculator` class" tells the listener something real; "Sir,
I have an `A` class" tells them nothing.

### Flag 5 — instance method with no instance state

The method takes two `int`s and returns their sum — it uses no instance
variable. An instance method that touches no instance state has no reason to
require an object; calling it would mean creating an object purely to reach
a method that is "nowhere related to any object." Declare it `static`:
`public static`.

### Flag 6 — meaningless method name

`m1` tells you nothing; the method returns a sum, so name it `add` (or
`sum`) — whichever is more meaningful.

### Flag 7 — meaningless parameter names

Even `x, y` is not recommended. Use full words: `number1, number2`, or
`firstNumber, secondNumber`.

```java
return number1 + number2;
```

## 10:31 — Side-by-side: Ameerpet standard vs Hi-Tech City standard

Ameerpet code (`class A`, `m1`) exists because it is never delivered to a
client — if it ever had to ship, every one of these names would be replaced
first. **Hi-Tech City standard** is the style used where the software
companies actually sit (Hyderabad's Hi-Tech City): meaningful names,
`public`, `static` where appropriate, a package. Whenever you write a Java
class — compulsory: follow naming conventions.

## 11:34 — Why meaningful names matter: `Math.sqrt`, `Math.max`

```java
Math.sqrt(4);
Math.max(10, 20);   // 20
```

Almost nobody has opened `java.lang.Math` to see how `sqrt` is implemented,
yet everyone in the room can say its purpose: square root of the given
number. Same for `max`. That ease comes entirely from the name. If Sun had
instead called them `m1`, `m2`, `m3`, … across 1,000 methods, there would be
no way to guess which one does what. Meaningful names are what make
readability and maintainability possible at all.

## 14:06 — "Durga bar and restaurant": the name must match the product

"Durga Software Solutions — best for our Java training" is a meaningful,
relevant name. "Durga bar and restaurant — best for our Java training" gets
a laugh — the name promises one thing and delivers another. Code with names
that don't match what the component does gets the same laugh.

## 17:07 — The two programs, board version

**Ameerpet standard** — never delivered, so conventions never matter:

```java
class A {
    public int m1(int x, int y) {
        return x + y;
    }
}
```

**Hi-Tech City standard** — what actually ships:

```java
package com.durgasoft.scjp;

public class Calculator {
    public static int add(int number1, int number2) {
        return number1 + number2;
    }
}
```

(Auto-captions later render the package as `com.durgasoft.ejp` in one pass —
same example; the module name Sir actually says is `scjp`.)

## 18:30 — Utility classes don't need `main`

`Calculator` above is a normal **utility class**, and it correctly has no
`main`. Don't assume every Java class needs one:

- **Servlets** are never invoked from the command prompt — the web container
  does that. No `main`.
- **EJB** classes don't need `main` either.
- A **standalone application** you launch from the command prompt is the one
  case where you keep `main`.

## 20:25 — Coding standards for classes

Class names such as `String`, `StringBuffer`, `Account`, `Dog` are all
**nouns** in English. The rule:

1. Usually, class names are **nouns**.
2. Should start with an **uppercase** character.
3. If it contains multiple words, **every inner word** starts with
   uppercase too (PascalCase / UpperCamelCase — Sir describes the shape
   without naming it "camel case," a term he reserves for names that start
   lowercase).

## 23:25 — Coding standards for interfaces

Interface names such as `Runnable`, `Serializable`, `Comparable`, and
`RandomAccess` are, in English, **adjectives** rather than nouns — Sir
starts to say "nouns," then catches himself. Same capitalization rule as
classes: start uppercase, capitalize every inner word.

1. Usually, interface names are **adjectives**.
2. Should start with an **uppercase** character.
3. If it contains multiple words, every inner word starts with uppercase.

> ❗ **Correction — "usually adjectives" overstates the rule.**
> It's true for the *-able*-style capability interfaces this lecture picks —
> `Runnable`, `Comparable`, `Serializable`, `Cloneable`, `Iterable` all read
> as adjectives. But a large share of the JDK's most-used interfaces are
> plain **nouns**: `List`, `Map`, `Set`, `Queue`, `Deque`, `Collection`,
> `Iterator`, `Comparator`. Oracle's actual naming-convention document never
> mandates a part of speech for interfaces — only the same capitalization
> style as classes. Treat "interfaces are adjectives" as *a pattern you'll
> see often*, not a rule the compiler or Sun ever enforced.

## 26:20 — Coding standards for methods

`print`, `sleep`, `run`, `eat`, `start` are method names, and in English
they are **verbs** — a method represents an action. `getName`, `setSalary`
split into a verb (`get`/`set`) plus a noun (`Name`/`Salary`):

1. Usually, method names are either **verbs** or a **verb–noun combination**.
2. Should start with a **lowercase** alphabet character.
3. If multiple words, every inner word starts with uppercase — this
   lower-start, upper-inner shape is **camel case convention**.

| Name | Kind |
|---|---|
| `print`, `sleep`, `run`, `eat`, `start` | verbs |
| `getName`, `setSalary` | verb–noun combinations |

## 31:31 — Coding standards for variables

`name`, `age`, `salary`, `mobileNumber` are variable names, and in English
they are **nouns** — every variable holds some value.

1. Usually, variable names are **nouns**.
2. Should start with a **lowercase** alphabet character.
3. If multiple words, every inner word starts with uppercase (camel case,
   same shape as methods).

## 34:44 — Coding standards for constants

`MAX_VALUE`/`MIN_VALUE` (every numeric wrapper class), `Thread.MAX_PRIORITY`
/`NORMAL_PRIORITY`/`MIN_PRIORITY`, and `Math.PI` are constants — a constant
is just a variable whose value is fixed. Still nouns in English; the only
difference from an ordinary variable is that the value never changes.

1. Usually, constant names are **nouns**.
2. Should **contain** only uppercase characters (Sir starts to write
   "should *start* with," catches the mistake mid-sentence, and corrects it
   to "should *contain* only uppercase" — the whole name is capitals, not
   just the first letter).
3. If multiple words, they're separated by an **underscore** `_`.

### 38:20 — How constants are declared

Constants are usually declared with the **`public static final`**
modifiers:

```java
public static final int MAX_VALUE = ...;
```

## 39:34 — JavaBean coding standards

A JavaBean is a **simple Java class** with **private properties** and
**public getter/setter methods** — nothing more is required for something
to count as a Bean. Every variable gets both accessors:

```java
public class StudentBean {
    private String name;

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

Every rule in this example is itself a coding standard: the field is
private; every property gets a setter and a getter; the setter is `public`,
returns `void`, and must take an argument; the getter is `public`, takes no
argument, and its return type must not be `void`. This is also why IDEs can
right-click-generate getters and setters automatically — the syntax is
fixed, so 100 developers (or 100 IDEs) asked to write a getter for
`String name` all produce the same shape.

**"Ends with `Bean`" is not an official Sun convention.** `StudentBean`,
`FormBean` are common, but Sun never required a Bean class name to end in
`Bean` — it's allowed, just not mandated.

> ⚠️ **Modern Java — records (16) cover the same idea for immutable data, with different accessor names.**
> A `record` gives you a constructor, `equals`/`hashCode`/`toString`, and
> read accessors in one line — but the accessor for field `name` is
> `name()`, not `getName()`, and there is no setter at all because the
> instance is immutable:
>
> ```java
> record Student(String name) { }
>
> Student s = new Student("Durga");
> s.name();   // canonical accessor — verified: no "get" prefix
> ```
>
> This is a genuinely different naming convention, not a violation of the
> JavaBean rule — records were never meant to be Beans. The classic
> `private` field + `getXxx`/`setXxx`/`isXxx` pattern this lecture teaches
> is still exactly what frameworks that expect JavaBeans (JSP EL, many
> serialization and binding libraries, JPA entities) require, and it is
> still what you write for any type that needs to be mutable.

### 47:36 — Setter method syntax

1. Must be a **`public`** method.
2. Return type must be **`void`** — you're updating a value, not expecting
   one back.
3. Method name must be **prefixed with `set`**.
4. Must **take an argument** — you have to pass the value to set.

### 50:00 — Getter method syntax

1. Must be a **`public`** method.
2. Return type must **not** be `void` — you're expecting a value back.
3. Method name must be **prefixed with `get`**.
4. Must **not take any argument** — you're only asking, not supplying.

## 51:55 — Exam twist: boolean getter — `getXxx` or `isXxx`

For a property `private boolean empty;`, the getter rules above give:

```java
public boolean getEmpty() {
    return empty;
}
```

This is **100% valid** — no doubt about it. But for boolean properties
specifically, the method name can also be prefixed with **`is`** instead of
`get`. Since `empty` can only be `true` or `false`, "is empty or not?" is the
more natural phrasing:

```java
public boolean isEmpty() {   // valid, and the recommended style
    return empty;
}
```

**Both are valid.** The collections framework uses `isEmpty()`, not
`getEmpty()`, precisely because it reads better — that doesn't make
`getEmpty` wrong, only less idiomatic. The exam version of this question
gives both spellings as options and expects you to mark **both** valid,
with `is` as the recommended one.

> **Board note (star):** For boolean properties, the getter method name can
> be prefixed with either `get` or `is`, but `is` is recommended.

> ⚠️ **Modern Java — a record's boolean accessor uses neither prefix.**
> `record Box(boolean empty) { }` generates the accessor `empty()` —
> verified by compiling it — not `isEmpty()` or `getEmpty()`. The
> `get`/`is` choice above is specific to the classic mutable-JavaBean
> pattern; a record's canonical accessor is always just the field name.

## 56:56 — Listener coding standards

GUI/AWT event handling is where most people first meet the word
**listener** — `MouseMotionListener`, a mouse-click listener, and so on.
Servlets have their own listener interfaces too. A listener **listens for
events** and **performs an appropriate action** whenever that event occurs
— Sir's classroom example: a "sleeping listener" posted at the door that
watches for a sleeping student and acts (gives "left and right") until the
sleeping stops.

Sir names eight servlet-related listeners:

- `ServletRequestListener`
- `ServletRequestAttributeListener`
- `ServletContextListener`
- `ServletContextAttributeListener`
- `HttpSessionListener`
- `HttpSessionActivationListener`
- `HttpSessionBindingListener`

> ❗ **Correction — that's seven names, not the eight he says.**
> The Servlet API of this era (2.5/3.0) defines exactly eight listener
> interfaces; the one missing from the list above is
> **`HttpSessionAttributeListener`** (fires when an attribute is added,
> removed, or replaced on a session — distinct from
> `HttpSessionBindingListener`, which the *attribute value itself*
> implements to be notified when it is bound to or unbound from a session).

> ⚠️ **Modern Java — the package changed name in 2020, and lambdas cover the single-method case.**
> Starting with **Jakarta EE 9**, the servlet API moved from `javax.servlet.*`
> to `jakarta.servlet.*` (Oracle's trademark on `javax` forced the rename
> when the spec moved to the Eclipse Foundation) — same interfaces, same
> method signatures, new package. Separately, since **Java 8**, any listener
> interface with a single abstract method (`ActionListener`,
> `Runnable`-shaped listeners) can be implemented with a **lambda** instead
> of an anonymous inner class — that changes how you *implement* a listener,
> not the `addXxx`/`removeXxx` naming standard a class exposes it under,
> which is exactly what the next two sections cover.

### 59:38 — Case 1: registering a listener (`add`)

The standard: the method is `public void`, its name is prefixed with `add`,
and the listener type named after `add` must match the argument's type.

```java
public void addMyActionListener(MyActionListener l) { }           // valid
public void registerMyActionListener(MyActionListener l) { }      // invalid: prefix must be add, not register
public void addMyActionListener(ActionListener l) { }              // invalid: name says MyActionListener, argument is ActionListener
```

| Method | Valid? | Why |
|---|---|---|
| `addMyActionListener(MyActionListener l)` | valid | `add` prefix + matching type |
| `registerMyActionListener(MyActionListener l)` | invalid | prefix must be `add`, not `register` |
| `addMyActionListener(ActionListener l)` | invalid | type after `add` ≠ argument type |

### 1:03:52 — Case 2: unregistering a listener (`remove`)

`add`'s counterpart for unregistering is **`remove`**. Same matching rule:
the type named after `remove` and the argument type must be identical, and
the method is `public void`.

```java
public void removeMyActionListener(MyActionListener l) { }        // valid
public void unregisterMyActionListener(MyActionListener l) { }    // invalid: not "remove"
public void removeMyActionListener(ActionListener l) { }          // invalid: type mismatch
public void deleteMyActionListener(MyActionListener l) { }        // invalid: not "remove"
```

| Method | Valid? | Why |
|---|---|---|
| `removeMyActionListener(MyActionListener l)` | valid | `remove` prefix + matching type |
| `unregisterMyActionListener(MyActionListener l)` | invalid | not `remove` |
| `removeMyActionListener(ActionListener l)` | invalid | type mismatch |
| `deleteMyActionListener(MyActionListener l)` | invalid | not `remove` (not `delete`) |

## 1:08:12 — Close: Language Fundamentals completed

That closes what you should know about Java coding standards — and with it,
**Language Fundamentals is complete**. The next playlist block is
Operators & Assignments.

---

## Exam and interview points

1. A "silly" write-a-class interview question is really checking for
   package, `public`, meaningful names, `static`, and camel case — not
   whether you can add two `int`s.
2. `class A` / `m1` / `x, y` / a missing package are the classic "Ameerpet"
   tells; a package statement must be the first real statement in a `.java`
   file.
3. Classes are nouns in UpperCamelCase; interfaces follow the same
   capitalization, and are *often* — not by any enforced rule — adjectives
   like `Runnable` and `Comparable`, while core interfaces such as `List`
   and `Map` are nouns.
4. Methods and variables are lowerCamelCase; methods are verbs or
   verb+noun (`getName`), variables are nouns.
5. Constants are nouns, `ALL_CAPS` with underscores, usually declared
   `public static final`.
6. A JavaBean is a simple class with private fields plus public
   getters/setters — the class name ending in `Bean` is common but never an
   official Sun rule.
7. Setter: `public`, `void`, `set` prefix, must take an argument. Getter:
   `public`, non-`void`, `get` prefix, must take no argument.
8. **Boolean getter twist:** both `getEmpty()` and `isEmpty()` are valid for
   `private boolean empty` — an exam question expects you to mark **both**
   valid, with `is` only as the recommendation.
9. Listener registration is prefixed `add`; unregistration is prefixed
   `remove` — never `register`/`unregister`/`delete` — and the listener type
   named after the prefix must match the parameter's type exactly.
10. The Servlet API defines **eight** listener interfaces, not the seven
    usually recited from memory; the easy one to forget is
    `HttpSessionAttributeListener`. Its package is `jakarta.servlet.*` in
    current specs, `javax.servlet.*` in this lecture's era.
11. Not every class needs `main` — servlets, EJB classes, and plain utility
    classes like `Calculator` don't have one.
12. Records (Java 16) give immutable data a getter-free naming convention
    of their own — `name()`, not `getName()`; `empty()`, not `isEmpty()` —
    which sits alongside the JavaBean convention rather than replacing it.

---

**Next:** Video 017 — Increment, Decrement, and Arithmetic Operators
