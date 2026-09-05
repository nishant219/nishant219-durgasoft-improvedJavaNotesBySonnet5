# Video 019 — instanceof and bitwise operators

## Video info

**Title:** Core Java with OCJP/SCJP: Operators & Assignments Part-3 || instanceof, bitwise operator

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 19 of 203 |
| Series | Operators & Assignments · Part 3 of 7 |
| Topic | `instanceof`; bitwise `&` `\|` `^`; bitwise complement `~`; boolean complement `!` |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 55m 14s (3314 seconds) |
| Video ID | dW_yjiVRlqQ |
| Watch | https://www.youtube.com/watch?v=dW_yjiVRlqQ |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

## What this lecture covers

1. Recap (equality / concatenation / arithmetic) and today's two topics
2. Why `instanceof` exists — a mixed collection whose `get()` returns `Object`
3. The keyword is **all lowercase** (`instanceof`, not `instanceOf`)
4. Syntax: `r instanceof X` — object reference vs. class/interface name
5. Example 1: `Thread` vs. `Thread` / `Object` / `Runnable` — all `true`
6. Example 2: `Thread` vs. `String` → compile error, a relation is required
7. `null instanceof X` is **always `false`**, for any class or interface `X`
8. Bitwise `&` `|` `^` on **boolean** — when each returns `true`
9. Same operators on **integrals**: `4 & 5`, `4 | 5`, `4 ^ 5` → `4`, `5`, `1` (not `true`/`false`)
10. Why 3-bit board math is enough for `&` `|` `^` here, but `~` needs the full 32 bits
11. Bitwise complement `~` (tilde): integrals only; `~true` is a CE; `~4` is **`-5`**, not `3`
12. Sign bit, two's complement, and why `~4 == -5`
13. Boolean complement `!`: boolean only; `!4` is a CE; `!false` is `true`
14. Summary table — which operators apply to boolean, which to integral
15. Q&A: bitwise on a negative number still runs on the full 32-bit two's-complement pattern

---

## 00:11 — Recap and agenda

Already covered: arithmetic, concatenation, equality. Next up: **`instanceof`**, then the bitwise family.

## 00:21 — `instanceof`: spelling and purpose

The keyword is **all lowercase**: `instanceof`. Write `instanceOf` (capital `O`) and it is a compile-time error — it is a keyword, not a camelCase method name.

**Purpose:** check whether a **given object is of a particular type or not**. "I have an object — is it a `Student`? A `Customer`? A `String`?" That is what `instanceof` answers.

### Why you would not already know the type

Typical scenario: a collection holding mixed objects.

```java
list:  [ obj0, obj1, obj2, obj3, ... ]
```

You cannot assume index 0 is always `String` or always `Student` — it might be anything. `List.get(int)` is declared to return **`Object`** (this is OCJP-era collections, before generics are the main story), so the parent type can hold any object:

```java
Object o = l.get(0);
```

Now you must **test the runtime type** before casting and calling type-specific methods:

```java
if (o instanceof Student) {
    Student s = (Student) o;
    // perform student-specific functionality
} else if (o instanceof Customer) {
    Customer c = (Customer) o;
    // perform customer-specific functionality
}
```

Without `instanceof`, a blind cast (`(Student) o`) throws `ClassCastException` the moment the object turns out to be a `Customer`.

> **Board:** We can use the `instanceof` operator to check whether the given object is of a particular type or not.

> ⚠️ **Modern Java — pattern matching folds the test and the cast into one step.**
> Since **Java 16** (JEP 394), `instanceof` can bind a **pattern variable** that is
> already cast and in scope wherever the compiler can prove the check succeeded:
>
> ```java
> if (o instanceof Student s) {
>     // s is already a Student here — no separate (Student) o needed
> } else if (o instanceof Customer c) {
>     // c is already a Customer here
> }
> ```
>
> **Java 21** (JEP 441) extends the same idea to `switch`, which is the natural
> modern shape of exactly this dispatch:
>
> ```java
> switch (o) {
>     case Student  s -> System.out.println("student: " + s);
>     case Customer c -> System.out.println("customer: " + c);
>     case null, default -> System.out.println("other");
> }
> ```
>
> Generics (Java 5) also shrink the problem at the source: a `List<Student>`
> never needs `instanceof` at all. The pattern here — a heterogeneous
> `List<Object>` — is exactly the case generics cannot help with, and it is why
> `instanceof` (now with pattern matching) is still current, not legacy, Java.

## 07:39 — Syntax: `r instanceof X`

```java
r instanceof X
```

| Token | Meaning |
|---|---|
| `r` | object reference |
| `X` | class name or interface name |

Result type: `boolean`.

## 08:56 — Example 1: `Thread`, `Object`, `Runnable` — all `true`

```java
Thread t = new Thread();

System.out.println(t instanceof Thread);    // true
System.out.println(t instanceof Object);    // true
System.out.println(t instanceof Runnable);  // true
```

Facts on the board (this is still **not** a multithreading chapter — `Thread` is just a convenient class):

- `Thread` is a **child class of `Object`**.
- `Thread` **implements `Runnable`**.

So: `t instanceof Thread` — the object *is* a `Thread` → `true`. `t instanceof Object` — every child object is-a parent type → `true`. `t instanceof Runnable` — every implementing-class object is-a that interface type → `true`. All three print `true`.

## 12:06 — Example 2: no relation, no verdict — a compile error

```java
Thread t = new Thread();
System.out.println(t instanceof String);
```

The obvious guess is `false` — a `Thread` is not a `String`, so surely the check just fails. **Wrong.** This does not compile.

> **Board:** To use `instanceof`, compulsory there should be some relation between the argument types — either child to parent, or parent to child, or same type. Otherwise, compile-time error: **inconvertible types**.

`Thread` and `String` have no such relation. The compiler asks "can this type ever be this other type?" and rejects the comparison outright rather than letting it run and answer `false`:

```text
inconvertible types
found   : java.lang.Thread
required: java.lang.String
```

Same rule for predefined and user-defined types alike. Contrast with the last video: equality (`==`) between unrelated types is a CE worded **incomparable types**; `instanceof` between unrelated types is a CE worded **inconvertible types**. Related idea, different wording — both are exam bait for exactly that reason.

> ⚠️ **Modern Java — the message itself has changed, and merged into a bigger family.**
> Compiled on **JDK 26** (verified, and identical via `--release 8/11/17/21/25` back
> to Java 8), the same code now produces:
>
> ```text
> error: incompatible types: Thread cannot be converted to String
> ```
>
> "Inconvertible types" is gone; instanceof mismatches now share the same
> `incompatible types: X cannot be converted to Y` wording used for narrowing
> assignments and bad casts. It is the same shift documented for `byte`/`int`
> assignments in video 002 — the old two-line `found:` / `required:` format
> collapsed into one line, and the vocabulary unified across error kinds. The
> **concept Sir teaches is unchanged**: no relation between the compile-time
> types, no compile.

> ❗ **Correction — "child, parent, or same type" is the class-to-class rule; interfaces are more permissive.**
> The three-way rule is right whenever **both** sides are classes. When one side
> is an interface, the compiler instead asks "is it *possible* for some future
> subclass to implement this?" — and for a non-final class, the answer is always
> yes, even with no declared relation:
>
> ```java
> interface Flyable {}
> class Bird {}                 // does not implement Flyable, and is not final
>
> Bird b = new Bird();
> System.out.println(b instanceof Flyable);   // valid — compiles, prints false
> ```
>
> Only a **`final`** class that provably cannot implement the interface is
> rejected at compile time. This has been true since `instanceof` was
> introduced — it is not a version change, just a sharper statement of "some
> relation" than the lecture's three bullet points give you.

## 18:10 — Last conclusion: `null instanceof X` is always `false`

For **any** class or interface `X`:

```java
null instanceof X   // always false
```

This **compiles**. It is not a CE, and the runtime result is always **`false`**:

```java
System.out.println(null instanceof Thread);    // false
System.out.println(null instanceof Object);    // false
System.out.println(null instanceof Runnable);  // false
```

`null` is not an instance of anything. Comparing `null` against any class or interface via `instanceof` is always `false` — this still holds unchanged with pattern-matching `instanceof` (Java 16+): `null instanceof String s` is `false` and never binds `s`.

That closes `instanceof`.

---

## 21:07 — Bitwise operators `&` `|` `^`

Board names: **and**, **or**, **xor** (exclusive or).

| Symbol | Name |
|---|---|
| `&` | AND |
| `\|` | OR |
| `^` | XOR / exclusive OR |

### Boolean meaning, first

**`&` (AND)** returns `true` **if and only if both arguments are `true`**.

**`|` (OR)** returns `true` **if and only if at least one argument is `true`** — "either this or this," including both.

**`^` (XOR)** — contrast with normal OR: normal OR is *first, or second, or both*; exclusive OR is *first but not second, or second but not first* — either one, but not both. Sir's book analogy: an animal can be a dog or a cat, never both at once. So XOR returns `true` **if and only if both arguments are different**.

| Pair | `&` | `\|` | `^` |
|---|---|---|---|
| different (`true`/`false` or `false`/`true`) | `false` | `true` | **`true`** |
| same (`true`/`true` or `false`/`false`) | depends | depends | `false` |

### Boolean examples on the board

```java
System.out.println(true & false);  // false — not both true
System.out.println(true | false);  // true  — at least one true
System.out.println(true ^ false);  // true  — arguments differ
```

Sir's note: interviews rarely ask these, but OCJP/SCJP does.

## 27:29 — Same operators on integral types — not `true`/`false`

```java
System.out.println(4 & 5);
System.out.println(4 | 5);
System.out.println(4 ^ 5);
```

First question is not "what number" — it is **valid or invalid?** It is **valid**; do not mark it a CE. And the wrong instinct is to answer `true`/`false` for each line — the actual results are **numbers**:

| Expression | Result |
|---|---|
| `4 & 5` | `4` |
| `4 \| 5` | `5` |
| `4 ^ 5` | `1` |

> **Board:** If we apply these operators to `boolean`, the result is `boolean`. If we apply them to a number/integral type, the result is a number. We can apply `&` `|` `^` to integral types too — `byte`, `short`, `int`, `long`.

### Why 4, 5, 1 — bitwise on the bits

These are **bitwise** operators — they work bit by bit. Using the low three bits of `4` and `5`:

```text
4  →  1 0 0
5  →  1 0 1
```

**AND** (`1` only if both are `1`):

```text
1 0 0
1 0 1
-----
1 0 0   →  4
```

**OR** (`1` if at least one is `1`):

```text
1 0 0
1 0 1
-----
1 0 1   →  5
```

**XOR** (`1` if the bits differ, `0` if they match):

```text
1 0 0
1 0 1
-----
0 0 1   →  1
```

So: **4, 5, 1** — not `true`/`false`, and not `3` (a common wrong instinct for the next operator).

---

## 33:51 — Bitwise complement operator `~` (tilde)

A unary operator, spoken "tilde."

### Not for boolean

```java
System.out.println(~true);
```

Looks like "negation of `true` → `false`." **Wrong** — this is a compile-time error.

> **Board:** the bitwise complement operator is applicable only for integral types, not for `boolean`.

```text
operator ~ cannot be applied to boolean
```

### For integrals it compiles — but the result is not "flip three bits"

```java
System.out.println(~4);
```

**Valid** — integral. The instinctive wrong answer: `4` is `100`, flip the three bits → `011` → `3`. The **actual output is `-5`**. (Sir compiles it live specifically because the class does not believe him.)

## 39:03 — Why `~4` is `-5` (32-bit, sign bit, two's complement)

`4` is an `int` literal, and every integral literal is `int` by default. `int` is **4 bytes = 32 bits** — so complement runs over **32 bits**, not 3.

### How `4` sits in memory

The most significant bit (MSB) is the **sign bit**: `0` means positive, `1` means negative. The remaining 31 bits carry magnitude.

```text
sign = 0,  remaining bits = ...0000 0100
```

### Apply `~` to all 32 bits

Every `0` becomes `1`, every `1` becomes `0`:

```text
1111 ... 1011
```

The MSB is now `1` → the result is negative.

> **Board:** the most significant bit acts as the sign bit. `0` means positive, `1` means negative. Positive numbers are represented directly in memory. Negative numbers are represented indirectly, in two's complement form.

Two's complement = one's complement, then add 1. Working the value: one's complement of the remaining bits gives a magnitude of 4, add 1 → magnitude 5, and the sign is negative → **`-5`**.

Thumb formula (same result, useful as a shortcut): `~x == -x - 1`, so `~4 == -5`.

## 46:08 — Twist: why `&` `|` `^` used 3 bits, but `~` needs 32

Student objection: the `4 & 5` board used three bits; the `~4` board suddenly used 32. Inconsistent?

**Strictly, `&` `|` `^` are also 32-bit operations.** The leading bits of positive `4` and `5` are all zeros:

```text
4  →  000...0100
5  →  000...0101
```

`0 & 0 = 0`, `0 | 0 = 0`, `0 ^ 0 = 0` — the extra high-order zero bits do not change the numeric result, which is why the 3-bit board was enough **for these particular positive operands**. For `~`, those high zeros flip to ones, the MSB becomes `1`, and the result *does* change — you get a negative number. Complement genuinely requires the full 32-bit picture; `&`/`|`/`^` only look that way in this specific example because both operands were small and positive.

## 48:18 — Boolean complement operator `!`

The opposite specialization of `~`: boolean-only, not integral.

```java
System.out.println(!4);      // CE
System.out.println(!false);  // true
```

`!4` looks like it should answer `true`/`false` — it is instead a compile-time error:

```text
operator ! cannot be applied to int
```

`!false` → `true`, no further explanation needed.

> **Board:** we can apply `!` only to `boolean` types, not to integral types.

## 51:27 — Summary of the bitwise-family operators

| Operator(s) | Boolean? | Integral? |
|---|---|---|
| `&` `\|` `^` | yes | yes (result is a number) |
| `~` (bitwise complement) | no — CE | yes, only |
| `!` (boolean complement) | yes, only | no — CE |

Recite: `&` `|` `^` apply to **both** boolean and integral; `~` applies **only to integral**; `!` applies **only to boolean**.

> ⚠️ **Modern Java — both compiler messages above have since changed wording.**
> Compiled on **JDK 26** (identical since at least JDK 8 via `--release`), the two
> boarded messages now read:
>
> ```text
> ~true   →  error: bad operand type boolean for unary operator '~'
> !4      →  error: bad operand type int for unary operator '!'
> ```
>
> Sir's `operator X cannot be applied to Y` phrasing was the wording of the era's
> compiler (the same family as `operator > cannot be applied to boolean,boolean`
> for relational operators, and `inconvertible types` for `instanceof` above);
> current javac's unary-operator diagnostic is `bad operand type <type> for
> unary operator '<op>'`, and its binary form is `bad operand types for binary
> operator '<op>'` with separate `first type:`/`second type:` lines. The rule
> being reported — `~` and `!` are mutually exclusive over boolean vs. integral —
> has not moved at all; only the sentence describing the violation has.

## 54:19 — Classroom Q&A: bitwise with a negative operand (e.g. `4 & -5`, `4 | -5`)

Someone asks what happens mixing `4` with a negative number. Sir does not run a full worked example; the point is procedural, not a specific answer to memorize:

- `-5` is stored in **32-bit two's complement** (sign bit `1`).
- `4` has sign bit `0`.
- `&` `|` `^` still run across all 32 bits.
- For **OR** specifically, `0 | 1` on the sign bit yields `1` → the result is a negative number.

Do not fall back to 3-bit arithmetic once a negative operand is involved — use the full 32-bit picture from the `~` section above.

---

## Code from the lecture

```java
import java.util.ArrayList;
import java.util.List;

class Student {}
class Customer {}

class InstanceofDemo {
    public static void main(String[] args) {
        Thread t = new Thread();
        System.out.println(t instanceof Thread);    // true
        System.out.println(t instanceof Object);    // true
        System.out.println(t instanceof Runnable);  // true
        // System.out.println(t instanceof String);
        // CE: incompatible types: Thread cannot be converted to String
        // (Sir's JDK 6/7 wording: "inconvertible types found: Thread required: String")

        System.out.println(null instanceof Thread);    // false
        System.out.println(null instanceof Object);    // false
        System.out.println(null instanceof Runnable);  // false
    }
}

class InstanceofUse {
    public static void main(String[] args) {
        List<Object> l = new ArrayList<>();
        l.add(new Student());
        l.add(new Customer());

        Object o = l.get(0);
        if (o instanceof Student) {
            Student s = (Student) o;
            // perform student-specific functionality
        } else if (o instanceof Customer) {
            Customer c = (Customer) o;
            // perform customer-specific functionality
        }

        // Java 16+: pattern matching folds the test and the cast into one step
        if (o instanceof Student s2) {
            // s2 is already a Student here — no separate cast needed
        }
    }
}

class BitwiseDemo {
    public static void main(String[] args) {
        System.out.println(true & false);  // false
        System.out.println(true | false);  // true
        System.out.println(true ^ false);  // true

        System.out.println(4 & 5);  // 4
        System.out.println(4 | 5);  // 5
        System.out.println(4 ^ 5);  // 1

        // System.out.println(~true);
        // CE: bad operand type boolean for unary operator '~'
        // (Sir's JDK 6/7 wording: "operator ~ cannot be applied to boolean")
        System.out.println(~4);     // -5

        // System.out.println(!4);
        // CE: bad operand type int for unary operator '!'
        // (Sir's JDK 6/7 wording: "operator ! cannot be applied to int")
        System.out.println(!false); // true
    }
}
```

All four classes compile and run as commented above (verified on JDK 26; the CE lines are commented out because they are, correctly, compile errors).

---

## Exam and interview points

1. **`instanceof` is a keyword, entirely lowercase.** `instanceOf` (capital `O`) does not compile — it is not a method name.
2. **Its job is a runtime type check before a cast**, typically on values that arrive as `Object` (a mixed collection, `List.get()`), so a blind cast cannot throw `ClassCastException`.
3. **`t instanceof Thread` / `Object` / `Runnable` are all `true`** for a plain `Thread` — child-to-parent and implementing-class-to-interface are both `true` by definition.
4. **`t instanceof String` is a compile error, not `false`**, because `Thread` and `String` share no type relation. The exam wording is *inconvertible types*; on a modern compiler the same error reads `incompatible types: Thread cannot be converted to String`. Compare with `==`'s *incomparable types* from the previous lecture — same idea, different keyword, different wording.
5. **The three-way relation rule (child/parent/same type) is for two classes.** Against an interface, a non-final class compiles even with no declared relation — only a `final` class that cannot possibly implement the interface is rejected.
6. **`null instanceof X` always compiles and is always `false`**, for any class or interface `X` — even after Java 16 pattern matching, `null instanceof String s` is `false` and never binds `s`.
7. **`&` `|` `^` apply to both `boolean` and integral types.** On `boolean` they return `boolean`; on integral types (`byte`, `short`, `int`, `long`) they return a **number**, computed bit by bit. `4 & 5` is **not** `true` or `false` — it is `4`.
8. **`~` (bitwise complement) is integral-only; `!` (boolean complement) is boolean-only.** `~true` and `!4` are both compile errors, for opposite reasons.
9. **`~4` is `-5`, not `3`.** The complement runs over all 32 bits of the `int`, not just the 3 bits that show the value — flipping the leading zero bits sets the sign bit and forces a two's-complement negative result.
10. **MSB is the sign bit: `0` positive, `1` negative.** Positive values are stored directly; negative values are stored in two's complement (one's complement, then add 1).
11. **`&` `|` `^` on small positive operands look like 3-bit math only because the high bits are all zero on both sides** — they are 32-bit operations too; it just does not show for `4` and `5`.
12. **Modern equivalents worth naming in an interview:** pattern-matching `instanceof` (Java 16) and pattern matching for `switch` (Java 21) both replace the classic "`instanceof` then cast" dance for exactly this Student/Customer-style dispatch — know that `instanceof` did not become obsolete, it grew a binding form.

---

**Next:** Video 020 — Short-circuit operators and type cast
