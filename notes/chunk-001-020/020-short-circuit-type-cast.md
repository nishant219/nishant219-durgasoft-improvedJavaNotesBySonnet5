# Video 020 — Short-Circuit Operators and Type Cast

## Video info

**Title:** Core Java with OCJP/SCJP: Operators & Assignments Part-4 || short-circuit,type cast operators

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 20 of 203 |
| Series | Operators & Assignments · Part 4 of 7 |
| Topic | Short-circuit `&&` `\|\|` vs bitwise `&` `\|`; implicit vs explicit type cast (widening / narrowing) |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 16m 01s (4561 seconds) |
| Video ID | 8xoqfIeBZ1g |
| Watch | https://www.youtube.com/watch?v=8xoqfIeBZ1g |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

Assignment, conditional (`?:`), and `new` are **not** covered in this video —
Sir defers all three to Part-5 (video 021).

## What this lecture covers

1. Recap of bitwise `&` `|` `^` and why `&&` `||` exist
2. Motivation: if the first operand of AND is already `false`, skip the expensive second check
3. Login analogy: username missing → do not bother checking the password
4. Difference table: bitwise `&` `|` vs short-circuit `&&` `||` (evaluation, performance, types)
5. When `y` is evaluated in `x && y` vs `x || y`
6. Exam example 1: `++x` / `++y` inside `if`, four operators (`&` `&&` `|` `||`) → four different `x, y` pairs
7. Exam example 2: `&&` vs `&` with `x / 0` — `Hi` vs `ArithmeticException`
8. Two kinds of type casting: **implicit** vs **explicit**
9. Implicit: compiler-driven, smaller→bigger, widening/upcasting, no loss of information; the conversion diagram
10. Examples: `int x = 'a'` → `97`; `double d = 10` → `10.0`
11. Explicit: programmer-driven `(type)`, bigger→smaller, narrowing/downcasting, possible loss; `possible loss of precision`
12. Example: `(byte) 130` → **`-126`**, with the 32-bit → last-8-bits → two's-complement derivation
13. Example: `(short) 150` stays `150`; `(byte) 150` → **`-106`**
14. Example: `(int) 130.456` → `130`; `(byte) 130.456` → `-126` (fraction digits dropped first)

---

## 00:07 — Recap, and the interview question that is *not* "one `&` vs two"

Last part covered bitwise operators. This part covers **short-circuit
operators** — `&&` and `||`.

Interview / exam framing: *we already have `&`. Why do we need `&&`?* The
wrong joke answer is "here we write `&` once, there we write it twice." That
is not the difference — and answering that way in an interview is the trap.

## 01:37 — Motivation: don't pay for the second operand if it can't change the answer

Sir's toy timing: a condition `bigX & bigY` where evaluating `bigX` takes 10
minutes, evaluating `bigY` takes another 10, and the `&` itself costs a
minute — 21 minutes before you even reach the `if`/`else`.

After the *first* 10 minutes you already know `bigX` is `false`. For AND, if
the first operand is `false`, the whole expression is `false` **no matter
what the second operand is**. Spending another 10 minutes on it is pure
waste.

- **Bitwise `&`** always evaluates both operands, even when the second
  cannot change the answer.
- **Short-circuit `&&`** evaluates the second operand **only if required**
  — only when the first operand is `true`.

**Performance:** `&&` is relatively better than `&` for exactly this reason
— it skips work that cannot affect the result.

### The login analogy

A user enters a username and password. The username is not in the database.
Is it worth comparing the password? No — that comparison can never change
the outcome. Use `&&`, not `&`.

## 06:10 — Difference table: bitwise vs short-circuit

`&&` and `||` behave **exactly like** `&` and `|`, except for three
differences:

|  | Bitwise `&` `\|` | Short-circuit `&&` `\|\|` |
|---|---|---|
| 1. Evaluation | Both operands are always evaluated, whether required or not | The second operand's evaluation is optional — evaluated only if required |
| 2. Performance | Relatively low | Relatively high |
| 3. Applicable types | Both `boolean` and integral types | `boolean` only, never integral types |

`4 & 5` is legal — bitwise AND of the bit patterns, value `4`. `4 && 5` is
not:

```java
// class Bad {
//     public static void main(String[] args) {
//         if (4 && 5) { }
//     }
// }
// error: bad operand types for binary operator '&&'
//   first type:  int
//   second type: int
```

Short-circuit operators only ever talk in `true`/`false`.

## 07:16 — When is `y` evaluated? `x && y` vs `x || y`

**`x && y`** — `y` is evaluated **if and only if `x` is `true`**. If `x` is
`false`, the whole AND is already `false`, so `y` is skipped.

**`x || y`** — `y` is evaluated **if and only if `x` is `false`**. If `x` is
`true`, the whole OR is already `true`, so `y` is skipped.

That asymmetry — "skip the second when the first already decided the
answer" — is why these operators exist only for `boolean`: there is no other
type where "already decided" is a meaningful, two-valued idea.

## 16:20 — Exam example 1: increment inside `if` (four operators, four outputs)

> The lecture board first writes `++y > 50`; when Sir actually works the
> example he uses `++y > 15` throughout (`16 > 15` is `true`). The worked
> numbers below use `15`, matching what he evaluates and what the compiler
> confirms.

```java
int x = 10;
int y = 15;
if (++x < 10 /* & or && or | or || */ ++y > 15) {
    x++;
} else {
    y++;
}
System.out.println(x + "........" + y);
```

Replace the operator with `&`, `&&`, `|`, or `||`. The exam question: **what
are `x` and `y` for each?** Start: `x = 10`, `y = 15`. Both branches use
pre-increment on `x` or `y`.

### Case A — bitwise `&` (both sides always run)

```text
++x → 11,  11 < 10 → false
++y → 16,  16 > 15 → true
false & true → false → else → y++
```

`x` is incremented once (in the condition); `y` is incremented twice
(condition, then `else`). **Result: `x = 11`, `y = 17`.**

### Case B — short-circuit `&&`

`++x` still runs → `11 < 10` → `false`. Because the first operand is
`false`, **`++y` is never evaluated** — `y` stays `15`. Control goes to
`else`: `y++`.

`x` incremented once, `y` incremented once. **Result: `x = 11`, `y = 16`.**
This is the entire `&` vs `&&` difference, visible only in the printed
numbers.

### Case C — bitwise `|` (both sides always run)

First operand is still `false`. Second still evaluated: `++y` → `16`,
`16 > 15` → `true`. `false | true` → `true` → **then**: `x++`.

`x` incremented twice (condition + then); `y` incremented once (condition
only). **Result: `x = 12`, `y = 16`.**

### Case D — short-circuit `||`

First operand is `false`, so OR **cannot** skip the second — a short-circuit
OR only skips when the first is already `true`. Same evaluation as `|`
here: second is `true`, then-branch `x++`.

**Result: `x = 12`, `y = 16`** — identical to `|` in this example, because
the first operand is `false`. The two operators would diverge only if the
first operand were `true` (`||` would then skip `++y` entirely; `|` never
would).

### Summary table for example 1

| Operator | `++y` runs? | Branch taken | `x` | `y` |
|---|---|---|---|---|
| `&` | yes | `else` | 11 | 17 |
| `&&` | no | `else` | 11 | 16 |
| `\|` | yes | `then` | 12 | 16 |
| `\|\|` | yes (first was `false`) | `then` | 12 | 16 |

Compiled and run on JDK 26, all four match exactly.

## 22:31 — Exam example 2: short-circuit can skip a `/ 0`

Same idea, a different multiple-choice trap.

```java
int x = 10;
if (++x < 10 && (x / 0 > 10)) {
    System.out.println("Hello");
} else {
    System.out.println("Hi");
}
```

Options offered in the lecture: (1) compile-time error, (2) runtime
`ArithmeticException: / by zero`, (3) `Hello`, (4) `Hi`.

Seeing `/ 0`, most people pick the runtime exception. **Wrong**, for `&&`:
`++x` → `11`, `11 < 10` → `false`. Short-circuit AND does **not** evaluate
`x / 0` — control goes straight to `else`. Output: **`Hi`**.

Replace `&&` with `&`: both sides now evaluate, `x / 0` runs, and the
program throws `ArithmeticException: / by zero`. Verified on JDK 26 — with
`&&` the program prints `Hi`; with `&` it throws. Single `&` vs double
`&&` here is a difference in **behaviour**, not just speed.

That closes short-circuit operators. Sir's note: these two styles — the
increment drill and the `/ 0` trap — are the only shapes this topic takes on
the exam.

---

## 27:21 — Type cast operator: two kinds

Two types of type casting: **implicit** and **explicit**.

## 28:56 — Implicit type casting

### Example 1 — `char` into `int`

```java
int x = 'a';
System.out.println(x);   // 97
```

You provided a `char`. The output is `97` — something converted `char` to
`int` automatically. That conversion is **implicit type casting**, and the
**compiler** performs it.

### Example 2 — `int` into `double`

```java
double d = 10;
System.out.println(d);   // 10.0
```

The compiler converts `int` to `double` automatically; the print shows
`10.0`, not `10`.

### Four conclusions

1. The **compiler** is responsible for implicit type casting.
2. It happens whenever a **smaller data type value** is assigned to a
   **bigger data type variable** — `char` (2 bytes) into `int` (4 bytes),
   `int` (4 bytes) into `double` (8 bytes). "Keeping a small value in a big
   container."
3. Also known as **widening** or **upcasting**.
4. There is **no loss of information**. If there were, the compiler would
   refuse to do it automatically — `10` becomes `10.0` and `'a'` becomes
   `97` without losing the value.

### Where implicit conversion happens

Moving left to right (smaller → bigger), the compiler inserts the
conversion automatically:

```text
byte  →  short  →  int  →  long  →  float  →  double
                      ↑
                     char
```

`byte→short`, `short→int`, `int→long`, `long→float`, `float→double`, and
`char→int` are all acceptable without a cast. The programmer is not
responsible; it happens internally.

`long → float` sits on this same arrow even though `float` is only 4 bytes
against `long`'s 8 — the story here is **range**, not byte count, and it can
in fact lose precision (a `float` has only 24 significand bits). That
derivation belongs to video 005's implicit-conversion diagram; this lecture
reuses the same diagram without repeating it.

## 41:33 — Explicit type casting

Now the conversion the **programmer** must write.

### Compiler refuses `int` → `byte` without a cast

```java
int x = 130;
// byte b = x;
// CE: incompatible types: possible lossy conversion from int to byte
```

`int` is 4 bytes, `byte` is 1 byte. Putting a 4-byte value into a 1-byte
hole risks losing information, so the compiler refuses — decently, with a
warning rather than a silent guess.

You must tell the compiler you accept the risk:

```java
byte b = (byte) x;   // compiles
```

This programmer-written conversion is **explicit type casting**, required
whenever a **bigger data type value** is assigned to a **smaller data type
variable**.

### The shocking output

```java
int x = 130;
byte b = (byte) x;
System.out.println(b);   // -126
```

You assigned `130`. You get `-126`. The programmer is shocked; the compiler
is not — it already warned about possible loss of information. In explicit
type casting there **may be** loss of information, and it will not always
be a value as memorable as `130 → -126` — the exam is just as likely to ask
about `150`.

### Four conclusions

1. The **programmer** is responsible for explicit type casting.
2. It is required whenever a **bigger data type value** is assigned to a
   **smaller data type variable**.
3. Also known as **narrowing** or **downcasting**. "Keeping a big value in a
   small place."
4. There **may be a chance of loss of information** (`130` became `-126`).

### Same diagram, opposite direction

- Left → right: implicit (smaller → bigger).
- Right → left: explicit (bigger → smaller) — `double → float → long → int
  → short → byte`, and `int → char`.

> ⚠️ **Modern Java — the diagnostic wording changed twice since this recording.**
> Sir dictates and reads out the JDK 6 message:
>
> ```text
> possible loss of precision
> found   : int
> required: byte
> ```
>
> From **Java 7** onward, `javac` collapses this to a single line, and both
> the "numeric but out of range" family and the "different kind entirely"
> family (`boolean`, `String`, …) now share the same `incompatible types:`
> prefix:
>
> ```text
> error: incompatible types: possible lossy conversion from int to byte
> ```
>
> Verified byte-for-byte on JDK 26. The **concept** Sir teaches —
> "loss-of-precision" numeric narrowing vs. "incompatible types" for
> unrelated kinds — is unchanged and is still the right way to *think*
> about the two error families; only the printed wording moved into the
> second half of the sentence. This exact wording history is covered in
> more depth in video 002 (the `byte` assignment drills), which this
> lecture's cast errors match precisely.

## 54:43 — Internal analysis: why `(byte) 130` is `-126`

`130` as an `int` occupies 4 bytes = 32 bits. It is positive, so the sign
bit is `0`, and the remaining bits store `130` directly. `130 = 128 + 2`, so
the low byte is `10000010`:

```text
32-bit 130:  00000000 00000000 00000000 10000010
```

**The rule:** whenever a bigger data type value is assigned to a smaller
data type variable by explicit type casting, the **most significant bits
are dropped** — only the **least significant bits** survive.

`byte` is 8 bits, so keep the last 8: `10000010`. Its MSB is `1` →
negative. The magnitude comes from **two's complement**:

- Invert `0000010` (the value bits) → `1111101`
- Add 1 → `1111110` = `126`
- Sign negative → **`-126`**

Cross-check with the full byte: `10000010` as a signed 8-bit value is
`-128 + 2 = -126`. Verified: `Integer.toBinaryString((byte) 130 & 0xFF)`
prints `10000010`, and `(byte) 130` prints `-126`.

## 1:03:11 — Example 2: `(short) 150` vs `(byte) 150`

```java
int x = 150;
short s = (short) x;
byte b = (byte) x;
System.out.println(s);   // 150
System.out.println(b);   // -106
```

`150` is well inside `short`'s range, so expect no loss there. `150` in
binary, built the successive-÷2 way: remainders bottom-up give
`10010110`.

**`(short) x`:** `short` is 16 bits. Padded to 16 bits the value is
`0000000010010110` — MSB `0`, positive, remaining bits represent `150`
directly. Output **`150`**, no loss.

**`(byte) x`:** last 8 bits are `10010110`. MSB `1` → negative. Two's
complement of the value bits: `0010110` inverted is `1101001`, plus 1 is
`1101010` = `64 + 32 + 8 + 2 = 106`. Negative → **`-106`**.

Sir first guesses `-108` out loud while narrating, then corrects to `-106`
once he actually computes it — the calculation and the compiled run both
give `-106`. Verified: `Integer.toBinaryString((byte) 150 & 0xFF)` prints
`10010110`, and `(byte) 150` prints `-106`.

## 1:11:32 — Example 3: floating point into an integral type

```java
double d = 130.456;
int x = (int) d;
byte b = (byte) d;
System.out.println(x);   // 130
System.out.println(b);   // -126
```

**The rule:** casting a floating-point value to an integral type by
explicit type casting drops the **digits after the decimal point** first.

`(int) 130.456` → `130` (`.456` is simply gone — truncation toward zero, as
taught here). Then `(byte) d` narrows the already-truncated `130` the same
way `(byte) 130` did above, giving the same **`-126`**. Verified on JDK 26.

> This truncates *toward zero*, not toward negative infinity — `(int)
> (-130.456)` gives `-130`, not `-131`. Sir's examples are all positive, so
> the distinction never comes up here, but it is a real interview follow-up
> once negative values enter the picture.

## 1:15:24 — Close of type cast; remaining operators later

Two kinds, recapped: implicit (compiler, smaller→bigger, no loss) and
explicit (programmer, bigger→smaller, possible loss).

Assignment, conditional (`?:`), and `new` are the next Operators &
Assignments video (Part-5, video 021), not this one.

---

## Code from the lecture

### Short-circuit example 1 (four operators, run independently)

```java
class ShortCircuitEx1 {
    public static void main(String[] args) {
        {
            int x = 10, y = 15;
            if (++x < 10 & ++y > 15) { x++; } else { y++; }
            System.out.println("&  -> " + x + "........" + y);   // 11........17
        }
        {
            int x = 10, y = 15;
            if (++x < 10 && ++y > 15) { x++; } else { y++; }
            System.out.println("&& -> " + x + "........" + y);   // 11........16
        }
        {
            int x = 10, y = 15;
            if (++x < 10 | ++y > 15) { x++; } else { y++; }
            System.out.println("|  -> " + x + "........" + y);   // 12........16
        }
        {
            int x = 10, y = 15;
            if (++x < 10 || ++y > 15) { x++; } else { y++; }
            System.out.println("|| -> " + x + "........" + y);   // 12........16
        }
    }
}
```

### Short-circuit example 2 (`/ 0`)

```java
class ShortCircuitEx2 {
    public static void main(String[] args) {
        int x = 10;
        if (++x < 10 && x / 0 > 10) {
            System.out.println("Hello");
        } else {
            System.out.println("Hi");   // this prints — && skips x / 0
        }
        // if (++x < 10 & x / 0 > 10)  →  ArithmeticException: / by zero
    }
}
```

### Implicit type cast

```java
class ImplicitCast {
    public static void main(String[] args) {
        int x = 'a';
        System.out.println(x);   // 97  (compiler: char → int)

        double d = 10;
        System.out.println(d);   // 10.0  (compiler: int → double)
    }
}
```

### Explicit type cast — 130, 150, 130.456

```java
class ExplicitCast {
    public static void main(String[] args) {
        int x = 130;
        // byte b = x;
        // CE: incompatible types: possible lossy conversion from int to byte
        byte b = (byte) x;
        System.out.println(b);   // -126

        int n = 150;
        short s = (short) n;
        byte b2 = (byte) n;
        System.out.println(s);   // 150
        System.out.println(b2);  // -106

        double d = 130.456;
        int i = (int) d;
        byte b3 = (byte) d;
        System.out.println(i);   // 130   (fraction gone)
        System.out.println(b3);  // -126
    }
}
```

All four files compile and run on JDK 26 with exactly these outputs.

---

## Exam and interview points

1. **The `&` vs `&&` difference is not "one character vs two."** It is
   always-evaluate vs. optional-second-operand, a performance difference,
   and boolean-only vs. boolean-**and**-integral.
2. **`x && y`** evaluates `y` iff `x` is `true`. **`x || y`** evaluates `y`
   iff `x` is `false`. Memorise the direction, not just the fact that one
   operand can be skipped.
3. **Classic increment drill:** `&` → `11, 17`; `&&` → `11, 16`; `|` and
   `||` (with a `false` first operand) → `12, 16`. `|` and `||` only
   diverge when the first operand is `true`.
4. **`&&` with `x / 0` after a `false` first operand prints `Hi`**, not
   `ArithmeticException`. Replace `&&` with `&` and it throws — proof that
   short-circuit changes *behaviour*, not merely speed.
5. **`4 && 5` is a compile error** (`bad operand types for binary operator
   '&&'`) — short-circuit operators never accept `int` operands, unlike `&`
   and `|`, which do.
6. **Implicit casting:** compiler-driven, widening/upcasting,
   smaller→bigger, **no** loss. `int x = 'a'` is `97`; `double d = 10` is
   `10.0`.
7. **Explicit casting:** programmer-driven `(type)`, narrowing/downcasting,
   bigger→smaller, **possible** loss. The historical message was `possible
   loss of precision`; the modern one (Java 7+) is `incompatible types:
   possible lossy conversion from X to Y`.
8. **`(byte) 130` is `-126`**, not `130`, not `-130`. The MSB of the 8 bits
   you keep becomes the new sign bit; the magnitude comes from two's
   complement.
9. **`(short) 150` stays `150`; `(byte) 150` is `-106`** (not `-108` —
   that number only ever appears as a slip of the tongue mid-derivation,
   never as the answer).
10. **Float/double → int/byte drops the fractional digits first**, then
    narrows what's left: `130.456 → 130 → -126` as a `byte`. Truncation is
    toward zero, so a negative fractional value truncates up, not down
    (`(int) -130.456` is `-130`).
11. **Assignment operators, the conditional `?:`, and `new` are next
    lecture** (Part-5, video 021), not this one.

---

**Next:** Video 021 — Operators & Assignments Part 5 (Assignment, Conditional, and `new`)
