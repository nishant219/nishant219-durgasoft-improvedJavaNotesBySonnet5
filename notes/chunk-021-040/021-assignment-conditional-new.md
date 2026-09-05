# Video 021 — Assignment, Conditional, and New Operators

## Video info

**Title:** Core Java with OCJP/SCJP: Operators & Assignments Part-5  ||Assignment,conditional,new Operators

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 21 of 203 |
| Series | Operators & Assignments · Part 5 of 7 |
| Topic | Simple / chained / compound assignment; the conditional (`?:`) operator; `new` vs constructor vs garbage collector; `[]` for arrays |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 48m 30s (2910 seconds) |
| Video ID | _zZ2Eazelxc |
| Watch | https://www.youtube.com/watch?v=_zZ2Eazelxc |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Recap: the type-cast operator (implicit and explicit), finished in Part-4.
2. Three kinds of assignment: simple, chained, compound.
3. Chained assignment on the board — `a = b = c = d = 20`.
4. The twist: chained assignment written directly at declaration time is a compile error.
5. The fix: declare the other variables first, then chain.
6. Compound assignment operators — the complete list of 11.
7. `>>` vs `>>>` (sign-bit fill vs zero fill) — a basic idea only, not on the SCJP exam.
8. There is no unsigned left shift (`<<<` does not exist).
9. Loophole: `byte b = b + 1` is a CE, but `b++` and `b += 1` both compile — internal type casting.
10. Extra example: `byte` overflow via compound assignment wraps silently.
11. SCJP-style mix: chained assignment combined with compound assignment, evaluated right to left.
12. The conditional / ternary operator `?:` — Java's only ternary operator.
13. Nesting of `?:` is legal, to any depth.
14. `new` creates the object; the constructor only initializes it. No `delete` — the garbage collector destroys unreachable objects.
15. `[]` to declare and create arrays.

## Detailed notes

### 00:08 — Recap, then assignment operators

Last class finished the type-cast operator — implicit and explicit casting. Today's
topic: assignment operators — what one is, and how many kinds there are.

## 00:46 — Three kinds of assignment

Sir's classification, dictated with no further explanation offered — it's meant to
be memorized as-is:

**1. Simple assignment** — a value assigned straight to a variable.

```java
int x = 10;   // simple assignment
```

**2. Chained assignment** — a sequence, a chain, of `=` operators.

```java
a = b = c = d = 20;   // chained assignment
```

**3. Compound assignment** — assignment mixed with some other operator.

```java
a += 20;   // compound assignment: assignment mixed with +
```

Three types, full stop: simple, chained, compound.

> ⚠️ **Modern Java — `var` (Java 10) covers simple assignment, not chained.**
> `var x = 10;` compiles fine for Sir's first case — the compiler infers `int` from
> the initializer. It does **not** rescue the chained-declaration loophole below:
> `var a = b = c = 20;` fails with the exact same `cannot find symbol` error as
> `int a = b = c = 20;` (verified on `javac` 26), because `var` still declares only
> the one variable named on its left.

### 03:26 — Chained assignment on the board

```java
class Test {
    public static void main(String[] args) {
        int a, b, c, d;
        a = b = c = d = 20;
        System.out.println(a + "........" + b + "........" + c + "........" + d);
        // 20........20........20........20
    }
}
```

Assignment right-associates: `20` is assigned to `d` first, then `d`'s value to `c`,
then `c`'s to `b`, then `b`'s to `a`. All four end up `20`. A chain of assignment
operators is entirely legal.

### 05:21 — Twist: chained assignment at declaration time

Why not fold the two lines above into one?

```java
class Test {
    public static void main(String[] args) {
        int a = b = c = d = 20;
    }
}
```

```text
Test.java:3: error: cannot find symbol
        int a = b = c = d = 20;
                ^
  symbol:   variable b
  location: class Test
(same error repeats for c, then for d)
```

This single line declares exactly **one** variable — `a`. `b`, `c`, `d` are *used*
on the right of an `=`, but never *declared*, so the compiler has nowhere to look
them up: "you're using `b` — where did you declare it?" (Verified: this is exactly
the error `javac` gives, three times over, once per undeclared name.)

**Conclusion:** we can perform chained assignment. We cannot perform chained
assignment directly at the point of declaration, because the declaration
statement introduces only the one variable it names.

### 09:08 — Fix: declare the others first, then chain

```java
class Test {
    public static void main(String[] args) {
        int b, c, d;
        int a = b = c = d = 20;   // valid — b, c, d are already declared
        System.out.println(a + "........" + b + "........" + c + "........" + d);
        // 20........20........20........20
    }
}
```

Once `b`, `c`, `d` already exist, the single-line chain for `a` is fine — the
earlier complaint was only ever "you never declared `b`, `c`, `d`," and that
complaint is gone.

## 10:18 — Compound assignment operators

Sometimes the assignment operator is mixed with some other operator:

```java
class Test {
    public static void main(String[] args) {
        int a = 10;
        a += 20;   // means a = a + 20
        System.out.println(a);   // 30
    }
}
```

### 11:36 — The full list: 11 operators

| Group | Operators | Count |
|---|---|---|
| Arithmetic | `+=` `-=` `*=` `/=` `%=` | 5 |
| Bitwise | `&=` `\|=` `^=` | 3 |
| Shift | `>>=` `>>>=` `<<=` | 3 |

5 + 3 + 3 = **11** — the complete list of compound assignment operators in Java,
then and now. Nothing has been added to it.

### 12:21 — `>>` vs `>>>` (basic idea only, not on the SCJP)

Not exam material, and rare even in real code, but the underlying idea: shifting
`x`'s bits right by two leaves two vacant bits on the left.

- Fill the vacant bits with the **sign bit** (`0` for positive, `1` for negative)
  → ordinary right shift, `>>`.
- Always fill with **zero**, ignoring the sign entirely → unsigned / zero-filling
  right shift, `>>>`.

The same idea for filling vacated bits applies conceptually on the left side too
— which sets up the next point.

### 15:24 — There is no unsigned left shift

Students guess `<<<` ought to exist by symmetry with `>>>`. It does not. Java has
exactly **three** shift operators: `>>`, unsigned right shift `>>>`, and left
shift `<<`. There is no unsigned/zero-filling left shift and no such
terminology — which is why the compound-assignment list above stops at 11, with
no `<<<=`. This has never changed.

## 19:24 — Loophole: `b = b + 1` vs `b++` vs `b += 1`

Three cases, all starting from `byte b = 10`.

**Case 1 — plain arithmetic (invalid):**

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        b = b + 1;
        System.out.println(b);
    }
}
```

```text
error: incompatible types: possible lossy conversion from int to byte
        b = b + 1;
              ^
```

Any arithmetic operator promotes its operands to `max(int, type of first operand,
type of second operand)`. `b` is `byte`, `1` is `int`, so `b + 1` is an `int` —
and an `int` cannot be assigned straight back into a `byte` variable without an
explicit cast.

> ⚠️ **Modern Java — same rule, clearer wording.**
> Sir dictates the compiler's message as `possible loss of precision / found: int
> / required: byte`, which was `javac`'s exact wording in the Java 6/7 era this
> lecture is from. Current `javac` (verified here on JDK 26) phrases the identical
> failure as `incompatible types: possible lossy conversion from int to byte` — the
> rule that fails is unchanged, only the diagnostic text got more explicit.

**Case 2 — increment (valid):**

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        b++;
        System.out.println(b);   // 11
    }
}
```

`b++` really means `b = (byte)(b + 1)` — `++` and `--` perform the narrowing cast
back to `byte` automatically. Already covered in the increment/decrement lecture;
the answer is **11**.

**Case 3 — compound assignment (valid — this lecture's loophole):**

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        b += 1;                  // equivalent to: b = (byte)(b + 1);
        System.out.println(b);   // 11
    }
}
```

`b += 1` is **not** shorthand for `b = b + 1` — that would not compile, per Case
1. It is shorthand for `b = (byte)(b + 1)`. Compound assignment operators perform
the same automatic internal (narrowing) type cast as `++`/`--`, which is why this
compiles and prints **11** where the spelled-out arithmetic form does not.

### 24:11 — Extra example for clarity: `byte` overflow

```java
class Test {
    public static void main(String[] args) {
        byte b = 127;   // max value of byte
        b += 3;
        System.out.println(b);   // -126
    }
}
```

`127 + 3 = 130`, an `int` value well outside `byte`'s range (`-128..127`).
Compound assignment casts it anyway: `(byte) 130` wraps around to **`-126`**
(verified). No compile error, no runtime exception — just silent wraparound. The
biggest advantage of compound assignment (automatic internal type casting) is
also its biggest trap: it will compile things the spelled-out arithmetic form
would correctly reject.

## 28:03 — SCJP mix: chained assignment + compound assignment

A style worth recognizing for the exam: chained assignment and compound
assignment mixed in one statement. Not having seen this kind of code before does
not make it invalid — it is perfectly legal:

```java
class Test {
    public static void main(String[] args) {
        int a, b, c, d;
        a = b = c = d = 20;
        a += b -= c *= d /= 2;
        System.out.println(a + "........" + b + "........" + c + "........" + d);
        // -160........-180........200........10
    }
}
```

After the first line, `a`, `b`, `c`, `d` are all `20`. **Assignment always
evaluates right to left:**

| Step | Expression | Computation | Result |
|---|---|---|---|
| 1 | `d /= 2` | `d = d / 2 = 20 / 2` | `d = 10` |
| 2 | `c *= d` | `c = c * d = 20 * 10` | `c = 200` |
| 3 | `b -= c` | `b = b - c = 20 - 200` | `b = -180` |
| 4 | `a += b` | `a = a + b = 20 + (-180)` | `a = -160` |

Output: `-160........-180........200........10` (verified). Memorize the pattern
— right to left, one step at a time — rather than just the final numbers.

## 32:36 — Conditional operator `?:` — Java's only ternary operator

First, the vocabulary of "how many operands":

- **Unary** — one operand: `a++`, `++a`.
  ```java
  a++;
  ++a;   // unary: one operand
  ```
- **Binary** — two operands: `a + b`.
  ```java
  int sum = a + b;   // binary: two operands
  ```
- **Ternary** — three operands: the conditional operator.
  ```java
  int x = (10 < 20) ? 30 : 40;
  // 10 < 20 → the condition   (argument 1)
  // 30      → value if true   (argument 2)
  // 40      → value if false  (argument 3)
  System.out.println(x);   // 30
  ```

**Conclusion:** the only possible ternary operator in Java — and in most
programming languages — is the conditional operator, so "conditional operator"
and "ternary operator" name the same thing and can be used interchangeably.

### 36:08 — Nesting of the conditional operator is legal

```java
class Test {
    public static void main(String[] args) {
        int x = (10 > 20) ? 30 : ((40 > 50) ? 60 : 70);
        System.out.println(x);   // 70
    }
}
```

`?:` is right-associative, so the "false" branch of one conditional expression
can itself be another conditional expression. Walking it: `10 > 20` is false →
take the colon side, `(40 > 50) ? 60 : 70`; `40 > 50` is also false → **70**.
Nesting to `n` levels is no problem at all.

Sir notes the older version of this course spent close to an hour on further
loopholes of this operator — none of which are required for the exam, or for
day-to-day coding.

> ⚠️ **Modern Java — switch expressions (Java 14) are the idiomatic tool for
> multi-branch logic now.**
> Nested `?:` is still perfectly legal, and the conditional operator is still the
> only ternary operator in the language — nothing about that claim has changed.
> But the kind of logic that used to force deep `?: … : …` nesting (three, four,
> five possible outcomes) now has a cleaner home: the switch **expression** form
> added in Java 14, which yields a value directly with no `break` and no
> fall-through:
> ```java
> int x = switch (score) {
>     case 100    -> 30;
>     case 40, 41 -> 70;
>     default     -> 0;
> };
> ```
> Reach for nested `?:` for one quick either/or; reach for a switch expression once
> there are more than two outcomes to choose between.

## 40:37 — The `new` operator

`new`'s job — its only job — is to **create** the object:

```java
class Test { }

class Demo {
    public static void main(String[] args) {
        Test t = new Test();
        // 1. new Test() allocates and creates the object
        // 2. Test's (default) constructor then runs, to initialize it
    }
}
```

The common misconception: "we use the constructor to create an object." That is
wrong. `new` creates the object; the constructor's role is purely
**initialization**, executed automatically immediately after `new` has done the
creating. Sir's phrasing for the notebook: *a constructor is not for creation of
an object; it is for initialization of an object.*

Is there a `delete` operator in Java? No. Destroying an unreachable object is the
**garbage collector's** responsibility, not the programmer's. Contrast with
C++, where `new` and `delete` are a matched pair, because in C++ the programmer
is responsible for both creating *and* destroying the object.

> ⚠️ **Modern Java — the GC's cleanup hook has moved away from `finalize()`.**
> Sir's "the GC destroys the object, not you" is still exactly correct today. What
> has changed is the mechanism a class could use to run code *during* that
> destruction: `Object.finalize()` was deprecated in **Java 9**, and since
> **Java 18** (JEP 421) is disabled by default at runtime — overriding it no
> longer reliably runs at all. The modern replacements are `java.lang.ref.Cleaner`
> (Java 9) for GC-triggered cleanup, and — far more commonly used — `try`-with-
> resources / `AutoCloseable` for deterministic cleanup you don't want to leave to
> the GC's schedule in the first place.

## 46:30 — `[]` — declare and create arrays

Not much depth needed here, and barely tested beyond this:

```java
class Test {
    public static void main(String[] args) {
        int[] x = new int[10];
        System.out.println(x.length);   // 10
    }
}
```

`[]` — square bracket open and close — is used for exactly one purpose in Java:
declaring and creating arrays. Outside of arrays, this operator has no other use.

---

## Exam and interview points

1. **Three kinds of assignment** — simple, chained, compound. That is the whole
   classification; nothing else qualifies.
2. **Chained assignment is legal, but not directly at declaration time.**
   `int a = b = c = d = 20;` fails with `cannot find symbol` for `b`, `c`, and
   `d`, because that line declares only `a`. Declare `b`, `c`, `d` first and the
   same chain compiles.
3. **Exactly 11 compound assignment operators**: 5 arithmetic + 3 bitwise + 3
   shift. There is no `<<<` — Java has never had an unsigned left shift.
4. **The `byte` + compound-assignment loophole.** `byte b = 10; b = b + 1;` is a
   CE (`int` can't narrow into `byte` implicitly); `b++` and `b += 1` both
   compile to `11`, because `++`/`--` and every compound assignment operator
   perform the narrowing cast automatically. `byte b = 127; b += 3;` compiles and
   silently wraps to `-126` — not a compile error, not `130`.
5. **Chained + compound mixed in one statement evaluates strictly right to
   left.** From `a = b = c = d = 20`, the statement `a += b -= c *= d /= 2`
   yields `a=-160, b=-180, c=200, d=10`. Memorize the right-to-left walk, not
   just the final numbers — "never seen this before" does not mean invalid.
6. **`?:` is the only ternary operator in Java** — and in most languages.
   Nesting is legal to any depth.
7. **`new` creates the object; the constructor only initializes it.** "The
   constructor creates the object" is the standard wrong answer to plant as a
   trap.
8. **Java has `new` but no `delete`.** The garbage collector destroys
   unreachable objects; the programmer never does. Unlike C++, where `new` and
   `delete` are both the programmer's job.
9. **`[]` has exactly one job**: declaring and creating arrays.
10. **Version awareness beyond the OCJP exam**: `var` (Java 10) covers simple
    assignment but not the chained-declaration case; switch expressions (Java 14)
    are the modern tool for multi-branch logic that used to mean nested `?:`;
    `finalize()` is deprecated (9) and disabled by default (18), so lean on
    `try`-with-resources or `Cleaner` instead of relying on GC-triggered cleanup;
    and today's `javac` reports the classic byte-narrowing error as "possible
    lossy conversion," not "possible loss of precision."

---

**Next:** Video 022 — Operator & Operand Precedence
