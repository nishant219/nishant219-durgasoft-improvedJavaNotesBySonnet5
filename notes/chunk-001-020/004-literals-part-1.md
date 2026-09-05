# Video 004 — Literals, part 1

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-4 || Literals Part-1

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 4 of 203 |
| Series | Language Fundamentals · Part 4 of 16 |
| Topic | Literals (part 1): integral, floating-point, boolean |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 22m 19s (4939 seconds) |
| Video ID | Eng8Oi-p2r4 |
| Watch | https://www.youtube.com/watch?v=Eng8Oi-p2r4 |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Two kinds of callout interrupt the lecture where
> it needs it: **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and
> has since changed. **❗ Correction** — what was stated is not accurate, then or
> now. Everything else is Sir's teaching, cleaned up.
>
> *This upload has captions disabled, so these sections carry no timestamps.
> The ordering follows the board work: video 003 closes data types with "how we
> provide values, we discuss in literals", and video 005 opens on char literals.*

## What this lecture covers

1. What a literal is
2. Integral literals — decimal, octal, hexadecimal, binary
3. Underscores in numeric literals
4. Default type of an integral literal (`int`) and the `L` suffix
5. Assigning integral literals to `byte` / `short` / `int` / `long` (range checks)
6. Floating-point literals — default `double`, `F`/`D` suffixes, scientific notation
7. Boolean literals — only `true` and `false`
8. Exam "valid or invalid" drills

Char and string literals are **next video**.

Every code sample and every compile error below was checked against `javac` 26.

---

## What is a literal?

> A **literal** is any constant value that can be assigned to a variable.

The left-hand side of an assignment is a variable. The right-hand side, when it
is a value typed straight into the source, is a literal.

```java
int x = 10;          // 10       — integral literal
float f = 10.5f;     // 10.5f    — floating-point literal
boolean b = true;    // true     — boolean literal
char ch = 'a';       // 'a'      — char literal   (part 2)
String s = "durga";  // "durga"  — String literal (part 2)
```

> ⚠️ **Modern Java — two more literal forms exist now.**
> The list Sir works through is complete for Java 6. Since then the language has
> added:
>
> | Form | Release | Example |
> |---|---|---|
> | Binary literals | **Java 7** | `0b1010` |
> | Underscores in numeric literals | **Java 7** | `1_000_000` |
> | Text blocks | **Java 15** | `"""` … `"""` (a String literal — part 2) |
>
> Both Java 7 additions are already in this note, because the recording sits on
> the 6→7 boundary. Worth knowing: the JDK itself has moved on far enough that
> Java 6 is not even a compilation target any more — `javac 26` accepts
> `--release 8` through `--release 26` and rejects `--release 6` outright. Every
> compiler you will meet in an interview already supports binary literals and
> underscores.

---

## Integral literals

Integral types are `byte`, `short`, `int`, `long` — and `char`.

> ❗ **Correction — `char` is an integral type.**
> The board list of "integral types" usually stops at four. The JLS lists
> **five**: `byte`, `short`, `int`, `long`, **`char`** (JLS §4.2.1). `char` is
> the unsigned 16-bit member of the family, and it behaves like one in exactly
> the place this lecture cares about — assigning constants:
>
> ```java
> char c = 65;      // valid — int constant in char range, prints 'A'
> byte b = 'a';     // valid — char constant 97 is in byte range
> char bad = 70000; // CE: possible lossy conversion from int to char (max 65535)
> ```
>
> The floating-point types are `float` and `double`; integral + floating-point
> together are the *numeric* types, and `boolean` is the odd one out. Getting
> `char` into the right bucket is a routine exam question.

An integral value can be written in four forms. Sir drills the conversion in
both directions — form → decimal, and "how do I write 10 in octal / hex".

### 1. Decimal (base 10) — the default

Digits `0`–`9`, no prefix.

```java
int x = 10;
int y = 100;
```

### 2. Octal (base 8)

Prefix **`0`** — a leading zero. Allowed digits `0`–`7`.

```java
int x = 010;    // octal 10 → decimal 8
int y = 0777;   // → 511
int z = 0786;   // CE: illegal digit in an octal literal ('8')
```

Conversion, on the board: `010` = 1×8¹ + 0×8⁰ = **8**.

So `System.out.println(010);` prints **8**, not 10. The exam loves this, and so
does every code review that has ever seen a zero-padded date constant.

### 3. Hexadecimal (base 16)

Prefix **`0x`** or **`0X`**. Digits `0`–`9` and `a`–`f` / `A`–`F`.

```java
int x = 0x10;      // hex 10 → decimal 16
int y = 0xFace;    // → 64206
int z = 0XBeef;    // → 48879
int bad = 0xBeer;  // CE: ';' expected — the literal ends at 0xBee, then 'r' is junk
```

`0x10` = 1×16¹ + 0×16⁰ = **16**, so `System.out.println(0x10);` prints **16**.

Letter case is irrelevant to the value: `0xFace`, `0xFACE` and `0xfaCE` are the
same number. Case matters only to your reader.

Note the error message on `0xBeer`: javac does **not** say "r is not a hex
digit". The lexer happily reads `0xBee`, stops, and then trips over a stray
identifier — hence `';' expected`. Same outcome, different wording than most
notes claim.

### 4. Binary (base 2) — from Java 7

Prefix **`0b`** or **`0B`**. Digits `0` and `1` only.

```java
int x = 0b1111;   // 15
int y = 0B1010;   // 10
int z = 0b201;    // CE: illegal digit in a binary literal
```

### The bases are not just decoration

| Written | Base | Decimal value |
|---|---|---|
| `10` | 10 | 10 |
| `010` | 8 | 8 |
| `0x10` | 16 | 16 |
| `0b10` | 2 | 2 |

> ❗ **Correction — the "int range" limit applies to decimal literals only.**
> It is commonly taught that any integral literal above `2147483647` is a
> compile error. That is true for **decimal**, but hex, octal and binary
> literals are allowed to specify the full 32-bit pattern, including patterns
> that denote negative numbers (JLS §3.10.1):
>
> ```java
> int a = 0xffffffff;                          // valid → -1
> int b = 0x80000000;                          // valid → -2147483648
> int c = 0b11111111111111111111111111111111;  // valid → -1
> int d = 017777777777;                        // valid → 2147483647
>
> int e = 4294967295;                          // CE: integer number too large
> int f = 0x100000000;                         // CE: integer number too large (33 bits)
> ```
>
> The real rule: a decimal literal may not exceed `2147483647` (unless it is
> exactly `2147483648` immediately after a unary minus); a hex/octal/binary
> literal may be anything that fits in 32 bits. Same rule one size up for `long`
> with the `L` suffix — `0xFFFFFFFFFFFFFFFFL` is a valid `long` equal to `-1`.

---

## Underscores in numeric literals (Java 7)

You may split groups of digits with `_` purely for readability. The compiler
throws them away.

```java
int   x = 1_00_000;      // 100000 — Indian grouping
int   y = 0b0111_1111;   // 127 — one underscore per nibble
long  z = 9_223_372_036_854_775_807L;
double d = 1_000.000_1;  // 1000.0001
```

> ❗ **Correction — state the underscore rule properly: a digit on both sides.**
> The rule is not "not next to a prefix" or "not next to a decimal point"; it is
> one rule that covers every case — **an underscore must have a digit
> immediately before it and a digit immediately after it** (JLS §3.10.1).
> Everything else falls out of that:
>
> ```java
> int a = 100_;        // CE: illegal underscore — nothing after it
> int b = 0x_10;       // CE: illegal underscore — 'x' before it is not a digit
> int c = 1_000_000_L; // CE: illegal underscore — 'L' after it is not a digit
> double e = 1_.5;     // CE: illegal underscore — '.' after it
> double f = 1._5;     // CE: illegal underscore — '.' before it
> int g = _100;        // NOT a literal error: _100 parses as an identifier,
>                      // so the error is "cannot find symbol"
> ```
>
> And the case that surprises people, which the "no underscore near a prefix"
> phrasing gets wrong:
>
> ```java
> int h = 0_10;   // VALID — the leading 0 is an octal digit, not a prefix.
>                 // Prints 8.
> ```

---

## Default type of an integral literal is `int`

Every integral literal is an **`int`** unless you suffix it with `L` or `l`.

```java
int  x  = 10;    // valid
long l1 = 10;    // valid — int literal widened to long
long l2 = 10L;   // valid — long literal
long l3 = 10l;   // valid — lowercase L, legal but unreadable
```

```java
int x = 10L;     // CE: incompatible types: possible lossy conversion from long to int
```

Use uppercase **`L`**. Lowercase `l` is indistinguishable from digit `1` in most
fonts — this is the one place where a style rule is a correctness rule.

When do you actually *need* the suffix? When the number does not fit in an
`int`:

```java
long a = 2147483647;    // valid — still an int literal, then widened
long b = 2147483648;    // CE: integer number too large
long c = 2147483648L;   // valid
```

`int` max is 2³¹−1 = **2147483647**. Note where the error comes from: `b` fails
in the **lexer**, before assignment is even considered. The compiler never gets
as far as "you are assigning to a `long`, so it would have fitted" — the token
itself is illegal. That is why the `L` is mandatory and not merely advisory.

> ⚠️ **Modern Java — `var` (Java 10) makes the default type visible.**
> With `var` there is no declared type to widen into, so the literal's own type
> is the variable's type — exactly the rule this section teaches, now with
> consequences:
>
> ```java
> var v1 = 10;     // int
> var v2 = 10L;    // long
> var v3 = 10.5;   // double
> var v4 = 10.5f;  // float
> ```
>
> (Verified by boxing each and printing `getClass()`: `Integer`, `Long`,
> `Double`, `Float`.) There is no literal suffix for `byte` or `short`, so
> `var b = 10;` gives you an `int` and always will — if you want a `byte`, you
> must write `byte b = 10;` the old way. `var` also cannot be used for fields,
> method parameters, or return types; it is for local variables only.

---

## Assigning to `byte` and `short`

The special rule Sir repeats until it sticks:

> If the right-hand side is an **`int` constant** and its value is **in the
> target type's range**, the assignment is allowed. The compiler performs an
> implicit narrowing.

```java
byte b1 = 10;      // valid — 10 is in byte range (-128 to 127)
byte b2 = 127;     // valid — the top of the range
byte b3 = 128;     // CE: possible lossy conversion from int to byte
byte b4 = -129;    // CE: below -128
short s1 = 32767;  // valid
short s2 = 32768;  // CE: possible lossy conversion from int to short
```

Ranges worth having memorised cold:

| Type | Bits | Range |
|---|---|---|
| `byte` | 8 | −128 … 127 |
| `short` | 16 | −32768 … 32767 |
| `char` | 16 (unsigned) | 0 … 65535 |
| `int` | 32 | −2147483648 … 2147483647 |
| `long` | 64 | −2⁶³ … 2⁶³−1 |

A `long` literal assigned to a `byte` is a compile error even when the value is
tiny, because the implicit narrowing is defined for `int` constants and not for
`long` ones:

```java
byte b = 10L;   // CE: possible lossy conversion from long to byte
byte c = (byte) 10L;  // valid — explicit cast
```

> ❗ **Correction — the rule is about *constant expressions*, not literals.**
> "It only works if the right-hand side is a literal, never a variable" is the
> version usually taught, and it is too narrow. JLS §5.2 allows implicit
> narrowing whenever the right-hand side is a **constant expression** of type
> `byte`, `short`, `char` or `int` whose value fits. A constant expression can
> be arithmetic on literals, and it can be a **constant variable** — a `final`
> variable initialised with a constant expression:
>
> ```java
> byte a = 10 + 20;            // valid — 30 is computed at compile time
> byte c = 'a';                // valid — char constant 97 fits in byte
>
> final int K = 10;
> byte d = K;                  // valid — K is a constant variable
>
> static final int FIELD = 10;
> byte e = FIELD;              // valid — same reason
> ```
>
> What genuinely fails is a value the compiler cannot pin down, and *that* is
> the real content of the "variable" rule:
>
> ```java
> int x = 10;
> byte f = x;                  // CE — x is not final, value not constant
> byte g = (byte) x;           // valid — explicit cast
>
> final int nc = compute();
> byte h = nc;                 // CE — final, but the initialiser is not constant
>
> byte i = 127 + 1;            // CE — constant expression, but 128 is out of range
> ```
>
> Note `h`: `final` alone is not enough. It has to be `final` **and**
> initialised with a compile-time constant. And note `i`: being a constant
> expression buys you the implicit narrowing, not an exemption from the range
> check. These four lines are the whole exam question.

---

## Floating-point literals

| Type | Bits | Precision | Approximate range |
|---|---|---|---|
| `float` | 32 | ~6–7 significant decimal digits | ±1.4e−45 … ±3.4028235e38 |
| `double` | 64 | ~15–17 significant decimal digits | ±4.9e−324 … ±1.7976931348623157e308 |

### Default type is `double`

```java
double d1 = 123.456;   // valid
float  f1 = 123.456;   // CE: possible lossy conversion from double to float
float  f2 = 123.456F;  // valid
float  f3 = 123.456f;  // valid
double d2 = 123.456D;  // valid — D is legal but redundant
double d3 = 123.456d;  // valid
```

The board line to recite: **every floating-point literal is a `double` unless it
ends in `F` or `f`.** `D`/`d` is permitted but says nothing new.

An integral literal widens into either floating type without a suffix, and a
`float` widens into a `double`:

```java
float  f = 10;      // valid — int → float
double d = 10;      // valid — int → double
double e = 10.5f;   // valid — float → double (widening, always safe)
```

Nothing widens *into* an integral type, so the traps in the other direction all
fail:

```java
int x = 10.5;    // CE: possible lossy conversion from double to int
int y = 10.5F;   // CE: possible lossy conversion from float to int
int z = (int) 10.5;  // valid — 10, the fraction is discarded, not rounded
```

A literal that is too large for its own type also fails at lexing, the same way
`2147483648` did:

```java
float  f = 3.5e40f;  // CE: floating-point number too large (float max ≈ 3.4e38)
double d = 1e400;    // CE: floating-point number too large
```

### Scientific / exponential form

```java
double d1 = 1.2e3;    // 1.2 × 10³ = 1200.0
double d2 = 1.2E3;    // same — case of e/E does not matter
float  f1 = 1.2e3F;   // valid — still a float because of the suffix
double d3 = 1.2e-3;   // 0.0012 — the exponent may be negative
```

`e` / `E` reads as "times ten to the power of". Note that an exponent alone
makes a literal floating-point even with no decimal point: `1e3` is a `double`.

### The forms of a floating literal

All of these are floating-point, and all are `double` unless suffixed `F`/`f`:

```java
double a = 123.456;  // digits . digits
double b = 123.;     // 123.0    — trailing dot is legal
double c = .456;     // 0.456    — leading dot is legal
double d = 1.2e3;    // exponent, no dot needed
double e = 1e3;      // 1000.0
```

The working rule: **a decimal point or an exponent makes it floating-point; a
plain run of digits is integral.**

> ❗ **Correction — `0x` does not automatically mean "integral".**
> Notes on this topic normally list `0x10` under the floating-point forms with
> the caveal "this one is integral hex, not float". `0x10` is indeed an `int`,
> but the implication that hex can only be integral is wrong. Java has had
> **hexadecimal floating-point literals** since **Java 5** (JLS §3.10.2). The
> exponent marker is `p`/`P` and is *mandatory*, and it means a power of **two**,
> not ten:
>
> ```java
> double a = 0x1.8p3;   // (1 + 8/16) × 2³ = 1.5 × 8  = 12.0
> double b = 0x1p-1;    // 1 × 2⁻¹                    = 0.5
> float  c = 0x1p4f;    //                            = 16.0
> ```
>
> You will almost never write one. They exist so that a `double` can be written
> down with its exact bit pattern, which decimal notation cannot always do —
> which is why `Double.toHexString` produces them. Nothing on the OCJP exam
> depends on writing one; recognising that `0x1.8p3` is a legal `double` and not
> a syntax error is the part that occasionally shows up.

### Why floating-point results look wrong

```java
System.out.println(0.1 + 0.2);   // 0.30000000000000004  — not 0.3
System.out.println(10 / 3);      // 3    — int division, fraction discarded
System.out.println(10.0 / 3);    // 3.3333333333333335
System.out.println(1.0 / 0.0);   // Infinity  — no exception
System.out.println(0.0 / 0.0);   // NaN       — no exception
System.out.println((float) 123.456789012);  // 123.45679 — float runs out of digits
```

Binary floating-point cannot represent 0.1 or 0.2 exactly, so their sum is not
exactly 0.3. Integer division by zero throws `ArithmeticException`; floating
division by zero does not — it produces `Infinity` or `NaN`. For money, use
`BigDecimal`, never `double`.

> ⚠️ **Modern Java — `strictfp` is now a no-op (Java 17).**
> When this was recorded, floating-point arithmetic could differ slightly
> between platforms unless a class or method was marked `strictfp`, which forced
> exact IEEE 754 semantics. Since **Java 17** (JEP 306) **all** floating-point
> expressions are evaluated strictly, everywhere, and `strictfp` changes
> nothing. It still parses and still compiles — `javac -Xlint:strictfp` warns
> that "as of release 17, all floating-point expressions are evaluated strictly
> and 'strictfp' is not required". It remains a reserved word (see video 001),
> so it still counts in the keyword list; it is simply dead code if you write it.

---

## Boolean literals

There are exactly two: **`true`** and **`false`**.

```java
boolean b1 = true;
boolean b2 = false;
```

Everything else is a compile error, and this is where C and C++ programmers
walk straight into the wall:

```java
boolean a = 0;        // CE: incompatible types: int cannot be converted to boolean
boolean b = 1;        // CE: same
boolean c = True;     // CE: cannot find symbol — True is an identifier, not a literal
boolean d = "true";   // CE: incompatible types: String cannot be converted to boolean
```

In C, `0` is false and anything non-zero is true. In Java there is **no
conversion at all** between `boolean` and the numeric types, in either
direction. This is the strong-typing point from video 002 — `int x = 10.5;` and
`boolean b = 0;` are rejected for the same underlying reason.

Note also what it costs you: `if (x = 5)` — the classic C typo of `=` for `==` —
does not compile in Java, because the assignment yields an `int` and `if`
demands a `boolean`. The rule you are complaining about is the rule catching
your bug.

`true`, `false` and `null` are **reserved literals**, not keywords (video 001):
they carry a value but no functionality. Reserved either way — you cannot use
them as identifiers.

---

## Which literal belongs to which type — board summary

| Literal kind | How you write it | Default type | Prefix / suffix |
|---|---|---|---|
| Decimal integral | `10` | `int` | none |
| Octal integral | `010` | `int` | leading `0` |
| Hex integral | `0x10` | `int` | `0x` / `0X` |
| Binary integral | `0b1010` | `int` | `0b` / `0B` (Java 7+) |
| Long integral | `10L` | `long` | `L` / `l` |
| Decimal floating | `10.5` | `double` | optional `D` / `d` |
| Float | `10.5F` | `float` | `F` / `f` required |
| Exponential | `1.2e3` | `double` | `e` / `E`; add `F` for float |
| Hex floating | `0x1.8p3` | `double` | `0x` … `p` / `P` (Java 5+) |
| Boolean | `true` `false` | `boolean` | — |
| Char | `'a'` | `char` | quotes (part 2) |
| String | `"durga"` | `String` | double quotes (part 2) |

There is **no suffix for `byte` or `short`.** That is not an oversight in your
memory — the language simply has none, which is exactly why the implicit
narrowing rule above has to exist.

---

## Classic print questions

```java
System.out.println(10);     // 10
System.out.println(010);    // 8
System.out.println(0x10);   // 16
System.out.println(0b10);   // 2
```

When a question mixes bases in one expression, convert each token to decimal
first, then evaluate — all four are just `int` values by the time the `+` runs:

```java
System.out.println(010 + 0x10 + 0b10);
// 8 + 16 + 2 = 26
```

The trap is assuming the base survives into the arithmetic. It does not. A base
is a **notation for writing the literal in source**, nothing more; there is no
"octal int" at runtime.

---

## Code from the lecture

```java
class LiteralDemo {
    public static void main(String[] args) {
        int decimal = 10;
        int octal   = 010;      // 8
        int hex     = 0x10;     // 16
        int binary  = 0b1010;   // 10
        long big    = 2147483648L;
        byte b      = 127;
        // byte bad = 128;      // CE: possible lossy conversion from int to byte
        float  f    = 12.34F;
        double d    = 12.34;
        double sci  = 1.2e3;    // 1200.0
        boolean flag = true;

        System.out.println(decimal + " " + octal + " " + hex + " " + binary);
        System.out.println(big);
        System.out.println(f + " " + d + " " + sci + " " + flag);
    }
}
```

Output:

```text
10 8 16 10
2147483648
12.34 12.34 1200.0 true
```

---

## Rules to memorise

1. A literal is a constant value written directly in source and assigned to a
   variable.
2. An integral literal is an `int` by default; suffix `L` when the value needs
   to be a `long`.
3. `010` is octal eight, `0x10` is hex sixteen, `0b10` is binary two.
4. Octal digits `0`–`7`; hex `0`–`9` `a`–`f`; binary `0`–`1`.
5. A decimal literal may not exceed `2147483647`; hex/octal/binary literals may
   use the full 32 bits, so `0xffffffff` is a legal `int` (−1).
6. An underscore in a numeric literal needs a digit on both sides — that single
   rule covers every illegal-underscore case.
7. `byte b = 10;` is valid because the right-hand side is a **constant
   expression** in range; `byte b = x;` for a non-final `int x` is a compile
   error.
8. A floating-point literal is a `double` unless suffixed `F`/`f`; `float f =
   10.5;` is a compile error.
9. Boolean literals are only `true` and `false` — never `0`, `1`, `True`, or
   `"true"`.
10. `char` is an integral type, and `char c = 65;` compiles.

---

## Exam and interview points

1. **`System.out.println(010)` prints 8, not 10.** The single most-asked
   question from this lecture. `0x10` prints 16, `0b10` prints 2, and
   `010 + 0x10 + 0b10` is 26.
2. **`int x = 10L;` is a compile error** — possible lossy conversion from `long`
   to `int` — while `long l = 10;` is fine. Widening is automatic, narrowing
   never is.
3. **`long l = 2147483648;` is a compile error** without the `L`, and the error
   is "integer number too large", raised at the token, not at the assignment.
4. **The narrowing rule is about constant expressions, not literals.**
   `byte b = 10 + 20;` and `final int K = 10; byte b = K;` both compile;
   `int x = 10; byte b = x;` does not. Expect the `final` variant on the paper.
5. **`byte b = 10L;` is a compile error** even though 10 fits — the implicit
   narrowing is defined for `int` constants, not `long` ones.
6. **`float f = 123.456;` is a compile error**; write `123.456F`. Every
   floating-point literal is a `double` by default.
7. **`boolean b = 0;` is a compile error.** There is no conversion between
   `boolean` and any numeric type, in either direction. `True` is not a literal.
8. **Malformed literals**: `0786` (illegal digit in an octal literal), `0b201`
   (illegal digit in a binary literal), `100_` and `0x_10` (illegal underscore),
   `0xBeer` (the literal stops at `0xBee`, so the error is `';' expected`).
9. **`char` is the fifth integral type.** Range 0–65535, so `char c = 65;`
   compiles and `char c = 70000;` does not.
10. **Modern additions worth naming in an interview**: binary literals and
    underscores in **Java 7**, `var` in **Java 10** (which makes a literal's
    default type the variable's type), text blocks in **Java 15**, and
    `strictfp` reduced to a no-op in **Java 17**.

---

**Next:** Video 005 — Literals Part 2
