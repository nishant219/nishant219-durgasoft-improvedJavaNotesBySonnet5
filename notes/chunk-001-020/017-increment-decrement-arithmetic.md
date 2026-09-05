# Video 017 — Increment, decrement, and arithmetic operators

## Video info

**Title:** Core Java with OCJP/SCJP: Operators & Assignments Part-1  || Increment & Decrement , Arithmetic

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 17 of 203 |
| Series | Operators & Assignments · Part 1 of 7 |
| Topic | Increment / decrement (++ --) and arithmetic (+ - * / %) |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 37m 49s (5869 seconds) |
| Video ID | 1JGOPhIyhAM |
| Watch | https://www.youtube.com/watch?v=1JGOPhIyhAM |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Two kinds of callout interrupt the lecture where
> it needs it: **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and
> has since changed. **❗ Correction** — what was stated is not accurate, then or
> now. Everything else is Sir's teaching, cleaned up.
>
> *No English captions exist for this upload — YouTube only offers Hindi
> auto-captions, which do not track the lecture — so these sections carry no
> timestamps. Video 016 closed Language Fundamentals; video 018 opens with
> "last session we covered arithmetic operators and increment and decrement;
> now string concatenation `+`." These notes are that Part-1 operators lecture,
> rebuilt from the board work and worked examples rather than a transcript.*

## What this lecture covers

1. Operators & Assignments module opens
2. Increment and decrement: pre vs post
3. What `++` / `--` may be applied to — and what is a compile error
4. The `byte b++` vs `b = b + 1` split — the most-asked question from this lecture
5. Arithmetic operators and the result-type rule: `max(int, type of a, type of b)`
6. `/` and `%` on integers vs floating point — `ArithmeticException`, `Infinity`, `NaN`
7. String `+` is **next** lecture — a teaser only, no content here

---

## Increment and decrement

Two operators: `++` (add one) and `--` (subtract one). Each comes in a pre and
a post form, and the difference between them is entirely about *when* the
change happens relative to when the value is used:

| Form | Name | Meaning |
|---|---|---|
| `++x` | pre-increment | increment first, then use the new value |
| `x++` | post-increment | use the old value first, then increment |
| `--x` | pre-decrement | decrement first, then use the new value |
| `x--` | post-decrement | use the old value first, then decrement |

```java
int x = 10;
int y = ++x;   // y = 11, x = 11 — value used is the incremented one

int x2 = 10;
int y2 = x2++; // y2 = 10, x2 = 11 — value used is the old one
```

```java
int x = 10;
System.out.println(++x); // 11 — x is now 11
int a = 10;
System.out.println(a++); // 10 — printed before the increment
System.out.println(a);   // 11 — the increment has now happened
```

Durga's spoken shortcut for telling them apart under exam pressure: **pre**
means "change first, then do the remaining operation"; **post** means "do the
remaining operation first, then change."

---

## What `++` / `--` may be applied to

The operand must be a **variable** — something a new value can be stored back
into. A literal, an expression, or anything not addressable is rejected:

```java
int x = 10;
x++;             // valid
++x;             // valid

final int y = 10;
y++;              // CE: cannot assign a value to final variable y

10++;             // CE: unexpected type — required: variable, found: value
(x + 1)++;        // CE: unexpected type — (x + 1) is a computed value, not a variable
```

Nesting is also rejected, for the same reason: `++x` is a value, and `++`
cannot be reapplied to a value.

```java
int x = 10;
++(++x);          // CE: unexpected type — required: variable, found: value
```

`boolean` has no `++`/`--` at all — there is no "one more than true":

```java
boolean b = true;
b++;              // CE: bad operand type boolean for unary operator '++'
```

Floating types are **not** on the forbidden list. `float` and `double`
variables accept `++`/`--` exactly like the integral types — the compiler
treats it as "add one, keeping the same type":

```java
double d = 5.0;
d++;              // valid — d becomes 6.0
```

So the full invalid list is short and specific: literals, non-variable
expressions, `final` variables, `boolean`, and a nested `++`/`--`. Everything
else that is a variable — every numeric primitive, `char` included — is fair
game.

---

## The `byte` puzzle (memorize cold)

This is the single most-tested contrast in the whole operators module.

```java
byte b = 10;
b++;              // valid — b becomes 11
```

```java
byte b = 10;
b = b + 1;        // CE: incompatible types: possible lossy conversion from int to byte
```

Both lines look like "add one to b." Only one compiles. The reason is that
`++` and plain addition go through different type rules:

- **`b + 1`** follows the ordinary arithmetic result-type rule (below):
  `byte + int` promotes to `int`. Assigning that `int` back into a `byte`
  variable is a narrowing conversion, and narrowing is never implicit — hence
  the compile error.
- **`b++`** is specified to behave as if the compiler inserted the narrowing
  cast for you: effectively `b = (byte) (b + 1)`. The increment operator does
  the promotion, the addition, *and* the cast back to `byte`, all in one step
  — which is exactly what plain assignment refuses to do silently.

```java
byte b = 10;
b = (byte) (b + 1);   // valid — spelling out what b++ does internally
```

The same split holds for `short` and `char`, because they hit the identical
result-type rule:

```java
char ch = 'a';
ch++;                  // valid — becomes 'b'
ch = ch + 1;           // CE: possible loss of precision — int to char

short s = 10;
s++;                   // valid
s = s + 1;             // CE: possible loss of precision — int to short
```

`int` and anything wider never hit this wall, because `int + int` is already
`int` — no narrowing is involved either way:

```java
int x = 10;
x = x + 1;   // valid
x++;         // valid
```

**Overflow is silent.** `++` on a `byte` at its maximum wraps around using
ordinary two's-complement arithmetic — no exception, no warning:

```java
byte b = 127;
b++;
System.out.println(b);   // -128
```

Exam questions on this lecture love to ask for the printed value after an
overflow, not just whether the code compiles.

---

## Expression questions: walking through pre/post chains

Durga spends real board time on expressions that mix pre- and post-increment
on the *same* variable, because the trap is always the same: people try to
remember one "magic total" instead of re-deriving it. The method is mechanical
— apply each operator exactly where it sits, left to right, updating the
variable as you go:

1. Track the current value of the variable.
2. For each occurrence: if it is **post** (`x++`/`x--`), use the current value,
   *then* apply the change; if it is **pre** (`++x`/`--x`), apply the change
   *first*, then use the new value.
3. Add up whatever was "used" at each step.

A short warm-up:

```java
int x = 10;
int y = x++;    // y = 10, x = 11 — post: use, then change
```

A two-term board sum:

```java
int x = 4;
int y = x++ + ++x;   // 4 + 6 = 10, final x = 6
```

Walking it: `x++` uses 4 and leaves `x` at 5; `++x` changes `x` to 6 first and
uses 6. Sum is `4 + 6 = 10`; `x` ends at 6.

The full three-term expression the note headline promises, worked the same way:

```java
int x = 10;
int y = x++ + ++x + x--;
```

- `x++` uses **10**, then `x` becomes 11.
- `++x` changes `x` to **12** first, then uses 12.
- `x--` uses the current value **12**, then `x` becomes 11.
- `y = 10 + 12 + 12 = 34`; final `x = 11`.

Always recompute term by term — there is no shortcut formula that survives a
new arrangement of `++`/`--` on the same variable.

---

## Arithmetic operators

Binary: `+` `-` `*` `/` `%`. Unary: `+x` `-x`.

`+` on two `String`s (or a `String` and anything else) is **concatenation** —
that is next lecture's topic. Everywhere in *this* lecture, `+` is plain
numeric addition, because no `String` appears in any expression here.

### Result type rule

For `a + b` (and the same for `-` `*` `/` `%` between numeric operands), the
rule Durga gives is:

**Result type = `max(int, type of a, type of b)`**

"Max," ordered from narrowest to widest: `byte`/`short`/`char` → `int` → `long`
→ `float` → `double`. In words: the two smaller integral types always widen up
to at least `int` before the operator runs; from there the wider of the two
operand types wins.

```java
byte a = 10, b = 20;
byte c = a + b;     // CE: possible lossy conversion from int to byte — a+b is int
int  i = a + b;      // valid — 30
```

```java
byte a = 10;
int  b = 20;
int  c = a + b;      // valid — 30
```

```java
int   a = 10;
float b = 20.5f;
float c = a + b;     // 30.5
```

```java
long   a = 10L;
double b = 2.0;
double c = a * b;    // 20.0
```

`char + char` also promotes to `int` — the Unicode code points are added, not
the characters:

```java
System.out.println('a' + 'b');   // 195 (97 + 98)
System.out.println('a' + 1);     // 98
```

### Division and remainder — integers

```java
System.out.println(10 / 2);   // 5
System.out.println(10 / 3);   // 3 — integer division truncates toward zero
System.out.println(10 % 3);   // 1
```

**Integer divide by zero throws:**

```java
System.out.println(10 / 0);   // Runtime: ArithmeticException: / by zero
System.out.println(10 % 0);   // ArithmeticException: / by zero
```

`ArithmeticException` is an **unchecked** exception — a subclass of
`RuntimeException`. No `throws` clause is required to compile, and no
`catch` is required either; if nothing catches it, the program simply crashes
with a stack trace. There is **no** integer "Infinity" — that concept only
exists for floating-point division.

### Division — floating point

```java
System.out.println(10.0 / 0);     // Infinity
System.out.println(-10.0 / 0);    // -Infinity
System.out.println(0.0 / 0.0);    // NaN
System.out.println(-0.0 / 0.0);   // NaN
```

Mixing an integer with a floating operand is enough to switch the whole
expression to floating rules — the exception disappears and `Infinity` takes
its place:

```java
System.out.println(10 / 0.0);    // Infinity — one operand is double
System.out.println(10.0 / 0);    // Infinity — same reason
```

Named constants for both cases exist on the wrapper classes:

- `Float.POSITIVE_INFINITY` / `Double.POSITIVE_INFINITY`
- `Float.NEGATIVE_INFINITY` / `Double.NEGATIVE_INFINITY`
- `Float.NaN` / `Double.NaN`

**`NaN` is never equal to itself** — by IEEE 754 definition, `NaN` compares
unequal to every value, including another `NaN`. Testing for it needs the
dedicated method, not `==`:

```java
System.out.println(Float.NaN == Float.NaN);   // false
System.out.println(Float.isNaN(0.0f / 0.0f)); // true
```

### `%` with floating point

Java allows `%` on floating operands too, which surprises anyone coming from a
C mental model where remainder is integer-only:

```java
System.out.println(10.0 % 0.0);   // NaN
System.out.println(10.5 % 3);     // 1.5
```

### Unary minus

```java
int x = 10;
System.out.println(-x);   // -10
```

`-10` written directly is unary minus applied to the literal `10`; the result
is still an `int`, not a separate "negative literal" form.

---

## What this lecture is not

Deliberately deferred to keep this session to increment/decrement and
arithmetic only:

- `+` on `"durga" + 10` (concatenation) → video 018
- `==` vs `.equals()` → video 018
- `instanceof`, bitwise operators → video 019
- `&&` vs `&` (short-circuit vs non-short-circuit) → video 020

---

## Code from the lecture

```java
class Operators1 {
    public static void main(String[] args) {
        byte b = 10;
        b++;
        // b = b + 1; // CE: possible lossy conversion from int to byte

        int x = 10;
        System.out.println(x++); // 10
        System.out.println(++x); // 12

        System.out.println('a' + 1);     // 98
        System.out.println(10 / 0.0);    // Infinity
        System.out.println(0.0 / 0.0);   // NaN
        try {
            System.out.println(10 / 0);
        } catch (ArithmeticException e) {
            System.out.println("int / 0 -> " + e);
        }
    }
}
```

Verified against `javac`/`java` 26: prints `10`, `12`, `98`, `Infinity`, `NaN`,
then `int / 0 -> java.lang.ArithmeticException: / by zero`.

---

## Rules to memorize

1. `++`/`--` need a non-final variable as their operand — no literals, no
   parenthesized expressions, no nested `++`, and no `boolean`.
2. `b++` is valid for `byte`/`short`/`char`; `b = b + 1` on the same variable
   is a compile error, because `++` inserts the narrowing cast and plain
   assignment does not.
3. Arithmetic result type is `max(int, type of a, type of b)`.
4. `byte + byte` (and `short + short`, `char + char`) is `int`, not the
   original narrower type.
5. `int / 0` throws `ArithmeticException`; floating `/ 0` produces
   `Infinity`, `-Infinity`, or `NaN` — never an exception.
6. `NaN == NaN` is `false`; use `Float.isNaN`/`Double.isNaN` to test for it.

---

## Exam and interview points

1. **`byte b = 10; b = b + 1;` is a compile error; `b++;` on the same variable
   is valid.** This is the most-asked question from the lecture — know *why*
   (`++` inserts an implicit narrowing cast; plain addition promotes to `int`
   and stops there).
2. **`byte b = 127; b++;` prints `-128`.** Overflow on `++` wraps silently
   with no exception — expect the exam to ask for the printed value, not just
   whether it compiles.
3. **`10 / 0` throws `ArithmeticException`; `10.0 / 0` evaluates to
   `Infinity`.** The presence of even one floating operand switches the whole
   expression from integer to floating division rules.
4. **`'a' + 'b'` prints `195`, not `"ab"`.** No `String` is involved, so `+` is
   numeric addition on the Unicode code points, and the result type is `int`.
5. **`final int x = 10; x++;` is a compile error** — `++` still needs to write
   a new value back, and a `final` variable cannot be reassigned.
6. **`NaN == NaN` is `false`.** Any comparison involving `NaN` — `<`, `>`,
   `==` — is `false` except `!=`, which is always `true`. Only
   `Float.isNaN`/`Double.isNaN` reliably detects it.
7. **Re-derive pre/post chains term by term.** `x++ + ++x + x--` starting from
   `x = 10` evaluates to `34` with `x` ending at `11` — there is no shortcut
   formula that survives a different starting value or a different
   arrangement of operators.

---

**Next:** Video 018 — Concatenation, relational, and equality operators
