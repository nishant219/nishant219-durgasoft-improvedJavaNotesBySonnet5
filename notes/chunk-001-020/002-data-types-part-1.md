# Video 002 — Data Types Part 1

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-2 || Data Types part-1

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 2 of 203 |
| Series | Language Fundamentals · Part 2 of 16 |
| Topic | Data types part 1 — strongly typed Java, eight primitives, signed types, byte, short, int |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 06m 48s (4008 seconds) |
| Video ID | njy7NGYzsvM |
| Watch | https://www.youtube.com/watch?v=njy7NGYzsvM |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Why Java is a **strongly typed** language — four board conclusions
2. Interview question: **Is Java a pure object-oriented language?** — recommended answer, and why
3. The **eight primitive data types**, split numeric / non-numeric and integral / floating-point
4. **Signed** types: everything except `boolean` and `char`
5. **`byte`** — size, sign bit, range, two's complement, the two compile-error families, when it is the right choice
6. **`short`** — the most rarely used type, size and range, why it exists and why it is obsolete
7. **`int`** — the most commonly used type, size and range, `integer number too large` vs `possible loss of precision`, the `L` suffix

`long`, `float`, `double`, `boolean` and `char` appear in the classification here
but are taught in detail in video 003.

---

## 00:05 — Recap and agenda

Last session covered identifiers and reserved words. This session is **data
types**, and Sir's framing is that we are going to perform a **postmortem** on
them — not a one-line definition, a full dissection.

---

## 00:41 — Why Java is strongly typed

Four conclusions, then the slogan.

### Conclusion 1 — every variable has a type

You cannot declare a variable in Java without a type. Whatever name you pick, it
must be attached to one.

```java
class Test {
    public static void main(String[] args) {
        int x;
        boolean b;
        double y;
        // z = 10;   // CE: cannot find symbol — there is no untyped declaration
    }
}
```

`x` is `int`, `b` is `boolean`, `y` is `double`. Without a type there is no
chance of even a single variable existing.

> ⚠️ **Modern Java — `var` (Java 10) does not break this rule.**
> Since **Java 10** (JEP 286) a local variable can be declared with `var` and the
> compiler infers the type from the initialiser:
>
> ```java
> var v = 10;      // v is int   — inferred, not untyped
> var d = 10.5;    // d is double
> var s = "durga"; // s is String
> // var u;        // CE: cannot infer type — 'var' needs an initializer
> ```
>
> This is **inference, not dynamic typing**. `v` is an `int` forever; `v = "x";`
> is still a compile error. Sir's conclusion survives intact — every variable
> still has exactly one static type, you just stopped typing it out. `var` is
> restricted to local variables, `for` indexes and lambda parameters; fields,
> method parameters and return types still need a written type.

### Conclusion 2 — every expression has a type

The same rule applies to expressions. Take `a + b + c`:

| If a, b, c are | then `a + b + c` is |
|---|---|
| `String` | `String` |
| `int` | `int` |

There is no untyped expression either.

> ❗ **Correction — the result type is not always the operand type.**
> "If a, b, c are `int`, then `a + b + c` is `int`" is true, but the general rule
> is **binary numeric promotion** (JLS §5.6): operands narrower than `int` are
> promoted to `int` before the operation. So the small types do *not* preserve
> themselves:
>
> ```java
> byte p = 10, q = 20;
> // byte r = p + q;   // CE: incompatible types: possible lossy conversion from int to byte
> int  r = p + q;      // 30 — byte + byte is an int expression
> ```
>
> Promotion order: if either operand is `double` → `double`; else `float`; else
> `long`; else **both are promoted to `int`**. This is why `byte`, `short` and
> `char` arithmetic always lands in `int`, and it is one of the most reliable
> OCJP traps in the whole syllabus.

### Conclusion 3 — each type is strictly defined

`byte` is the example:

| Property | Value |
|---|---|
| Size | 1 byte = 8 bits |
| Range | −128 to +127 |

Nothing here is "implementation-defined" the way `int` is in C, where the width
depends on the platform. In Java every primitive's size and range are fixed by
the specification and are the same on every JVM on every machine.

### Conclusion 4 — every assignment is checked for type compatibility

The compiler compares the **provided value** against the **expected type**:

| Assignment | Valid in Java? | Why |
|---|---|---|
| `int x = 10.5;` | invalid | `10.5` is a `double`, not an `int` |
| `boolean b = 0;` | invalid | `0` is a number, not a boolean |

Both of these are accepted by C. Java rejects both.

> ❗ **Correction — "both are valid in C" needs one qualifier.**
> `int x = 10.5;` is genuinely valid C — it silently truncates to `10`. But
> `boolean b = 0;` was not valid C either, because **C had no boolean type at all
> until C99**; you wrote `int b = 0;` and relied on 0/non-zero being read as
> false/true. The teaching point is right and is the real difference: C converts
> freely between numbers and truth values, Java refuses. Just do not repeat "C
> has a `boolean` that accepts 0" in an interview.

Because of all four points:

> **Board:** Java language is considered as a strongly typed programming language.

"Strongly typed" does **not** mean you have to hit the keyboard very hard. It
means **type checking is strong** — type matters, and the compiler enforces it.

**Board recap, as dictated:**

1. Every variable and every expression in Java has some type.
2. Each and every data type is clearly defined.
3. Every assignment should be checked by the compiler for type compatibility.
4. Because of the above reasons, Java is a strongly typed programming language.

---

## 06:19 — Is Java a pure object-oriented language?

The second big conclusion. Sir spends real time here because both classroom
answers are defensible — it depends on the perspective you are arguing from.

### 08:00 — The "two marks extra" analogy

School-age Durga brings his progress report to his father and announces: "Dad, I
am the too-intelligent person when compared with **Ravi** — I got **two marks
extra**." Father is delighted, good, keep it up. Five minutes later he asks how
many marks Ravi got. Ravi got **0 out of 100**. Which makes Durga **2 out of 100**.

- **Relative comparison:** yes, 2 > 0, he is the intelligent one.
- **Consider Durga alone:** no. Two marks out of a hundred is not intelligence.

The answer flips the moment you stop comparing and start judging on its own.

### Apply it to Java

- **Compared with older languages like C++**, Java has *more* object-oriented
  nature. In that relative perspective people call it pure OOP.
- **Consider Java alone**, without the comparison, and several OOP features are
  simply missing — so you cannot call it pure.

Features Sir names as missing: **operator overloading**, **multiple
inheritance**, and others.

> ❗ **Correction — both examples need a footnote.**
> **Operator overloading:** Java does not let *you* overload operators, but the
> language itself ships one overloaded operator — `+` is arithmetic addition for
> numbers and concatenation for `String`. The accurate claim is "Java has no
> **user-defined** operator overloading."
>
> **Multiple inheritance:** Java has always supported multiple inheritance **of
> type** — a class may implement any number of interfaces. What it forbids is
> multiple inheritance **of state** (a class has exactly one superclass), which
> is what avoids the C++ diamond problem. Say "no multiple inheritance of
> classes," not "no multiple inheritance."

> ⚠️ **Modern Java — interfaces now inherit behaviour too.**
> Since **Java 8**, `default` methods give interfaces real implementations, so a
> class genuinely inherits *behaviour* from several supertypes. The compiler
> forces you to disambiguate a clash rather than guessing:
>
> ```java
> interface A { default String who() { return "A"; } }
> interface B { default String who() { return "B"; } }
>
> class C implements A, B {
>     // without this override: CE: class C inherits unrelated defaults for who()
>     public String who() { return A.super.who() + B.super.who(); }  // "AB"
> }
> ```
>
> Java 8 also added `static` methods on interfaces, and **Java 9** added
> `private` interface methods. "Interfaces are only contracts" stopped being true
> in 2014 — the surviving restriction is on inherited *state*, not behaviour.

### 13:22 — The interview-room answer

Pick the answer that will **not create a problem for you**.

| If you answer | The interviewer's next question | Are you safe? |
|---|---|---|
| Yes | "Several features are not supported by Java. How is that pure?" | Your face becomes a question mark. Bad. |
| No | "Why not?" | You have the reasons ready. |

Reasons for **no**:

1. Several OOP features are not satisfied by Java — user-defined operator
   overloading, multiple inheritance of classes, and others.
2. **We depend on primitive data types, which are non-objects.** `int x = 10;` is
   not an object. In a genuinely pure OOP language everything would be an object.
   Wrapper conversion is a different story — you are *still* depending on
   primitives underneath.

> **Board:** Java is not considered as a pure object-oriented programming
> language, because several OOP features are not satisfied by Java (like operator
> overloading and multiple inheritance etc.). Moreover we are depending on
> primitive data types which are non-objects.

> ⚠️ **Modern Java — autoboxing softened it, Valhalla has not landed.**
> **Java 5** added autoboxing, so `Integer i = 10;` compiles and generics let you
> write `List<Integer>` — you can go a long way without naming a primitive. But
> Sir's reason still holds exactly as stated: boxing *converts* a primitive, it
> does not remove it, and `int` remains a non-object with no methods and no
> `null`.
>
> **Project Valhalla** (value classes / primitive classes) aims to close the gap
> between primitives and objects, but as of **Java 25 it has not shipped** — only
> preview pieces. So in 2026 the recommended interview answer is still **no**,
> with exactly these reasons.

**Two conclusions so far:** Java is a **strongly typed** language, and Java is
**not** a pure object-oriented language.

---

## 17:27 — How many primitive data types? Eight

Java has **eight** primitive data types. Split them the way the board splits
them.

**Numeric vs non-numeric.** Some types talk about numbers; some do not.

**Inside numeric, integral vs floating-point.** A number *with* a decimal point
(`123.456`) is floating-point. A number *without* one is integral.

```text
primitive data types (8)
├── numeric
│   ├── integral          → byte, short, int, long
│   └── floating-point    → float, double
└── non-numeric
    ├── char              → characters (not a number)
    └── boolean           → true / false
```

Count: **4 + 2 + 2 = 8**.

| Category | Types | Used to represent |
|---|---|---|
| Integral | `byte`, `short`, `int`, `long` | numbers without a decimal point |
| Floating-point | `float`, `double` | numbers with a decimal point |
| Non-numeric | `char`, `boolean` | a character; a truth value |

> ❗ **Correction — `char` is a number underneath.**
> Putting `char` under "non-numeric" is the exam's classification and you should
> reproduce it, but do not carry the literal belief into code. A `char` **is** an
> integral type in the JLS (§4.2.1): it is an unsigned 16-bit integer, it takes
> part in arithmetic, and it promotes to `int` like `byte` and `short` do.
>
> ```java
> char c = 'a';
> int  n = c + 1;              // 98
> System.out.println((char) n); // b
> byte b = 'a';                 // valid — 'a' is the constant 97, which fits
> ```
>
> The real non-numeric type is `boolean`, and it is the only primitive with no
> numeric conversion at all. `char` is classified apart because *signedness* is
> meaningless for it, which is exactly the point of the next section.

Two of the eight are left as headline facts here and taught properly in video
003: `long` (8 bytes), `float`/`double` (4 and 8 bytes), `boolean` and `char`.

---

## 21:42 — Common point: signed data types

For numbers, a leading `+` or `−` has meaning:

```java
int    x = +10;     // valid
int    y = -10;     // valid
double d = -10.5;   // valid
```

For the non-numeric types it does not:

```java
// char    ch = -'a';    // CE: incompatible types: possible lossy conversion from int to char
// boolean b  = -false;  // CE: bad operand type boolean for unary operator '-'
```

> **Board:** Except `boolean` and `char`, the remaining data types are considered
> as **signed data types**, because we can represent both positive and negative
> numbers.

| Type | Signed? |
|---|---|
| `byte`, `short`, `int`, `long`, `float`, `double` | yes — signed |
| `boolean`, `char` | no |

Worth noting the two exclusions are excluded for *different* reasons. `boolean`
is not a number at all. `char` **is** a number, but an **unsigned** one — its
range is `0` to `65535`, verified by `Character.MIN_VALUE` and
`Character.MAX_VALUE`. `char` is in fact the only unsigned primitive in Java.

> ⚠️ **Modern Java — unsigned *operations* exist, unsigned *types* still do not.**
> Java never added `unsigned int`, and it still has not. But since **Java 8** the
> wrapper classes carry static methods that let you treat an `int` or `long` as
> unsigned when you need to:
>
> ```java
> int  raw = -1;
> System.out.println(Integer.toUnsignedString(raw));   // 4294967295
> System.out.println(Integer.divideUnsigned(raw, 2));  // 2147483647
> System.out.println(Integer.compareUnsigned(raw, 1)); // 1  (as unsigned, -1 > 1)
> System.out.println(Byte.toUnsignedInt((byte) -1));   // 255
> ```
>
> The *type* is still signed; only the interpretation changes. Sir's rule is
> unaffected — this is the escape hatch for protocol and file-format code that
> used to force people into `long`.

---

## 24:32 — The `byte` data type

The first primitive discussed in detail.

### Size and the sign bit

|  |  |
|---|---|
| Size | 1 byte (8 bits) |

Draw the eight bits. `byte` is a **signed** type, so:

- The first bit is the **MSB** — Most Significant Bit — and acts as the **sign bit**.
- **0** → positive, **1** → negative.
- One bit is reserved for the sign; the **remaining 7 bits** carry the value.

### Maximum value from 7 value bits

All seven value bits set to 1:

```text
2^0 + 2^1 + 2^2 + 2^3 + 2^4 + 2^5 + 2^6
=  1  +  2  +  4  +  8  + 16  + 32  + 64
= 127
```

Sign bit 0 → **maximum = +127**.

### The "how is −128 possible?" doubt

Sir raises the student objection himself: seven bits top out at 127, and seven
zeros are just zero — so where does **−128** come from?

His answer on the board:

1. The most significant bit acts as the **sign bit**.
2. **0** means positive number, **1** means negative number.
3. Positive numbers are represented **directly** in memory.
4. Negative numbers are represented in **two's complement form**.

He defers the actual bit pattern to a later session and tells the class to
memorise the range for now.

> ❗ **Correction — two's complement does not "reserve" a sign bit.**
> The mental model of "1 bit for sign, 7 bits for magnitude" is
> **sign-and-magnitude**, which is a *different* encoding that Java does not use.
> It is a useful first approximation, but it cannot explain −128, which is why the
> class got stuck.
>
> In **two's complement** all 8 bits are value bits; the top bit simply carries a
> **negative weight** of −2⁷:
>
> ```text
> value = -128·b7 + 64·b6 + 32·b5 + 16·b4 + 8·b3 + 4·b2 + 2·b1 + 1·b0
>
> 0111 1111  =        64+32+16+8+4+2+1  =  +127   (Byte.MAX_VALUE)
> 0000 0000  =                          =     0
> 1111 1111  = -128 + 64+32+16+8+4+2+1  =    -1
> 1000 0000  = -128                     =  -128   (Byte.MIN_VALUE)
> ```
>
> Verified: `Integer.toBinaryString((byte) -128 & 0xFF)` prints `10000000`, and
> `(byte) -1` prints `11111111`.
>
> This also explains the **asymmetry** that "one bit for sign" cannot: the range
> is −128 to +127, not −127 to +127, because two's complement has exactly one
> representation of zero and therefore one spare slot on the negative side. The
> same asymmetry is why `Math.abs(Byte.MIN_VALUE)` cannot be represented and why
> `Math.abs(Integer.MIN_VALUE)` famously returns a negative number.
>
> Sir's sentence "in two's complement, 7 bits are enough to represent 128" is the
> part to unlearn. It is 8 bits, one of which is worth −128.

### Range (memorise)

|  |  |
|---|---|
| Size | 1 byte (8 bits) |
| Max value | +127 (`Byte.MAX_VALUE`) |
| Min value | −128 (`Byte.MIN_VALUE`) |
| Range | −128 to +127, i.e. −2⁷ to 2⁷ − 1 |

---

## 33:26 — `byte`: valid and invalid assignments (exam gold)

Sir drills these until you can recite both the verdict and the exact compile-error
family. The demo shape:

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        System.out.println(b);   // 10
    }
}
```

`javac Test.java` then `java Test` prints `10`. He deliberately switches his
`PATH` to **JDK 1.6** mid-lecture so the error wording matches his slides.

| Code | Valid? | Compile error (Sir's JDK 1.6 wording) |
|---|---|---|
| `byte b = 10;` | valid | — prints 10 |
| `byte b = -127;` | valid | in range |
| `byte b = 127;` | valid | max byte |
| `byte b = 128;` | invalid | `possible loss of precision — found: int, required: byte` |
| `byte b = 10.5;` | invalid | `possible loss of precision — found: double, required: byte` |
| `byte b = true;` | invalid | `incompatible types — found: boolean, required: byte` |
| `byte b = "durga";` | invalid | `incompatible types — found: java.lang.String, required: byte` |

### The two error families

**1. `possible loss of precision`** — there *is* numeric compatibility, but the
value may not fit or may lose accuracy.

- `128` is a number, so this is a **range** problem, not a kind-of-thing problem.
- Every integral literal is `int` by default → *found `int`, required `byte`*.
- `10.5` is `double` by default → *found `double`, required `byte`*.

**2. `incompatible types`** — completely different kinds of value, no numeric
story at all.

- `true` is `boolean`. → *found `boolean`, required `byte`*.
- `"durga"` is `java.lang.String`. → *found `java.lang.String`, required `byte`*.

This is Conclusion 4 in action: every assignment is checked by the compiler for
type compatibility.

> ⚠️ **Modern Java — the wording changed, and the two families now share a prefix.**
> Compiled on **JDK 26** (and identically on every JDK from 8 onward), the exact
> messages are:
>
> ```text
> byte b = 128;       error: incompatible types: possible lossy conversion from int to byte
> byte b = 10.5;      error: incompatible types: possible lossy conversion from double to byte
> byte b = true;      error: incompatible types: boolean cannot be converted to byte
> byte b = "durga";   error: incompatible types: String cannot be converted to byte
> ```
>
> Three things moved since 1.6:
>
> | 1.6 wording | Current wording |
> |---|---|
> | `possible loss of precision` | `possible lossy conversion` |
> | `found: X / required: Y` on separate lines | `from X to Y` inline |
> | only the second family said `incompatible types` | **both** families are prefixed `incompatible types:` |
> | `java.lang.String` | `String` (simple name) |
>
> That third row matters for the exam. Sir teaches "know when it is *incompatible
> types* and when it is *possible loss of precision*" — on a modern compiler
> **every one of them says `incompatible types`**, and the distinction has moved
> into the second half of the sentence: `possible lossy conversion from …` for the
> numeric-range family, `X cannot be converted to Y` for the different-kind
> family. The **concept is unchanged**; only the diagnostic text moved. Answer the
> OCJP question with Sir's two families, and recognise the new phrasing at a
> terminal.

> ⚠️ **Modern Java — literal syntax gained two conveniences in Java 7.**
> Neither changes the rules above, but both show up in current code and in newer
> exam questions:
>
> ```java
> byte b   = 0b0111_1111;    // binary literal (Java 7)  = 127
> int  max = 2_147_483_647;  // underscore separators (Java 7) — same value, readable
> ```
>
> Underscores are ignored by the compiler and may not sit at the start or end of a
> literal or next to the decimal point.

### Why does `byte b = 10;` compile at all?

Sir does not raise this, but the exam does. `10` is an `int` literal, and `int`
to `byte` is a narrowing conversion — so by Conclusion 4 it should be rejected,
exactly as `byte b = 128;` is. The reason it is accepted is a special rule in
**JLS §5.2**: in an *assignment* context, an implicit narrowing conversion is
allowed when the right-hand side is a **compile-time constant expression** whose
value actually fits the target type.

```java
final int c = 127;
byte ok  = c;      // valid — c is a constant variable, 127 fits

int  n   = 127;
// byte bad = n;   // CE: incompatible types: possible lossy conversion from int to byte
```

Same value, same types — the only difference is that `c` is `final` and therefore
a constant expression the compiler can evaluate. Drop the `final` and it fails.
This single rule explains the whole `byte b = 10;` / `byte b = 128;` split: the
compiler evaluates the constant and checks the range.

---

## 43:03 — When is `byte` the best choice?

Not "whenever the number happens to be between −128 and +127." The classroom
offers that and Sir rejects it as the *reason `byte` exists*.

> **Board:** `byte` is the best choice if we want to handle data **in terms of
> streams**, either from the **file** or from the **network**.
> (File supported form or network supported form is **byte**.)

There are two kinds of streams: **character streams** and **byte streams**. A
file, and a network connection, are fundamentally a **sequence of bytes** — so
that is the form you handle stream data in.

His API example: `FileOutputStream` writes binary data to a file, and its `write`
method takes a **`byte[]`**, never a `short[]`.

```java
import java.io.FileOutputStream;

class Demo {
    public static void main(String[] args) throws Exception {
        byte[] data = "durga".getBytes();     // String -> byte[]
        try (FileOutputStream fos = new FileOutputStream("out.bin")) {
            fos.write(data);                  // write(byte[]) — always byte
        }
    }
}
```

> ⚠️ **Modern Java — the same reason, far less plumbing.**
> `byte[]` is still the currency of I/O, which is exactly Sir's point, but you
> rarely hand-roll the loop any more:
>
> ```java
> import java.nio.file.*;
>
> byte[] data = Files.readAllBytes(Path.of("in.bin"));   // Java 7 NIO.2
> Files.write(Path.of("out.bin"), data);                 // Java 7
> byte[] all = someInputStream.readAllBytes();           // Java 9
> someInputStream.transferTo(someOutputStream);          // Java 9
> ```
>
> Also worth knowing: `String.getBytes()` uses the platform default charset, which
> is why you should pass one explicitly — and since **Java 18** (JEP 400) the
> default for the JDK's own APIs is **UTF-8** everywhere rather than
> platform-dependent, which quietly fixed a decade of cross-platform bugs.
>
> The `try (...)` above is **try-with-resources**, added in **Java 7**; before
> that you closed the stream in a `finally` block by hand.

---

## 47:07 — The `short` data type

### The most rarely used type in Java

Sir's running joke: ask someone who has been learning Java for a year how often
they used `short` — "I never used it." Ask someone with seven or eight years in
industry — "I never used it." Out of his own two-month SCJP course, `short`
appears in **this class only**.

### Size and range

Same sign-bit story as `byte`, scaled up: 1 bit for sign, **15 bits** for value.

|  |  |
|---|---|
| Size | 2 bytes (16 bits) |
| Range (formula) | −2¹⁵ to 2¹⁵ − 1 |
| Range (numbers) | −32,768 to 32,767 |

2¹⁵ = 32,768. (`Short.MIN_VALUE` and `Short.MAX_VALUE` confirm both.) The two's
complement correction from the `byte` section applies here unchanged: it is 16
value bits with the top one weighted −32,768, not 15 bits plus a sign flag.

### `short` assignment quizzes — same pattern

| Code | Valid? | Error (1.6 wording) | Current wording |
|---|---|---|---|
| `short s = 32767;` | valid | — | — |
| `short s = 32768;` | invalid | `possible loss of precision — found int, required short` | `incompatible types: possible lossy conversion from int to short` |
| `short s = 10.5;` | invalid | `possible loss of precision — found double, required short` | `incompatible types: possible lossy conversion from double to short` |
| `short s = true;` | invalid | `incompatible types — found boolean, required short` | `incompatible types: boolean cannot be converted to short` |

Sir does not re-run the `String` case; it behaves exactly as it did for `byte`.

---

## 53:55 — When is `short` the best choice?

Rarely used now, but there was a historical reason.

- Java arrived in **1995**.
- Popular processors then, per the lecture: **8085 / 8086**, described as **16-bit
  processors**.
- A 16-bit processor means the instruction length is 16 bits and data is handled
  in 16-bit form.
- `short` is 16 bits. Expected form and provided form match, so read and write
  operations become very efficient.

> **Board:** `short` data type is best suitable for **16-bit processors** like
> **8085**. But these processors are completely **outdated**. Hence the
> corresponding `short` data type is also an **outdated** data type.

> ❗ **Correction — the 8085 is an 8-bit processor, and 1995 was not the 16-bit era.**
> Two factual slips inside a conclusion that is nevertheless correct:
>
> | Chip | Year | Data width |
> |---|---|---|
> | Intel **8085** | 1976 | **8-bit** data bus (16-bit *address* bus) |
> | Intel **8086** | 1978 | **16-bit** — this is the 16-bit example |
> | Intel 80386 | 1985 | 32-bit |
> | Intel Pentium | 1993 | 32-bit |
>
> So the 16-bit example should be the **8086**, not the 8085 — the 8085's 16 bits
> are its address bus, which is probably where the confusion comes from. And by
> **1995** the mainstream desktop had been 32-bit for a decade; Java was not born
> into a 16-bit world.
>
> The conclusion still stands, for the reason Sir gives one line earlier: `short`
> pays off only when the machine word matches, and no mainstream machine has a
> 16-bit word any more. `short` really is close to obsolete — just do not cite the
> 8085 as your 16-bit processor in an interview.

Today 32-bit and 64-bit processors are the norm, so `short` buys nothing.

> ⚠️ **Modern Java — `short` is not only unused, it is often slower.**
> On a modern 64-bit JVM, `short` and `byte` locals are stored in a full 32-bit
> stack slot anyway, and arithmetic on them promotes to `int` and then narrows
> back — so a `short` counter is never faster than an `int` counter and can be
> marginally slower. The one place the small types still genuinely pay is **large
> arrays**, where `byte[]` and `short[]` really do use 1 and 2 bytes per element
> and the memory saving is real.
>
> Two related modern facts: **compact strings** (Java 9, JEP 254) store Latin-1
> text as a `byte[]` rather than a `char[]`, halving the footprint of most
> strings; and the **Vector API** (incubating since Java 16) works over `byte[]`
> and `short[]` lanes. So the *small array* case matured while the *small scalar*
> case stayed dead.

---

## 57:39 — The `int` data type

### The most commonly used type in Java

Even to represent the value 10, the hand always goes to `int x = 10;` — `byte`
would do, but nobody reaches for it.

### Size and range

|  |  |
|---|---|
| Size | 4 bytes (32 bits) |
| Range (formula) | −2³¹ to 2³¹ − 1 |
| Range (numbers) | −2,147,483,648 to 2,147,483,647 |

(`Integer.MIN_VALUE` and `Integer.MAX_VALUE` confirm both.)

---

## 1:00:31 — `int` quizzes, and a brand-new compile error

```java
int x = 2147483647;      // valid — the max value
System.out.println(x);   // 2147483647
```

```java
// int x = 2147483648;   // invalid
```

Students predict `possible loss of precision, found long, required int`.
**Wrong** — that is not the error you get.

### The rule

Every **integral literal** (a number without a decimal point) is by default an
**`int`**. The compiler requires that literal to be **within the `int` range**
before it even considers the assignment. If it is not:

> **`integer number too large`**

`2147483648` is still being read as an `int` literal, and it does not fit. The
failure happens at the literal, not at the assignment — which is why the
found/required wording never appears.

### The `L` suffix changes which error you get

Suffix the literal with a lowercase `l` or an uppercase `L` and it becomes a
`long` literal. Now the literal itself is legal, and the *assignment* is what
fails:

```java
// int x = 2147483648L;   // CE: incompatible types: possible lossy conversion from long to int
long y = 2147483648L;     // valid — this is what L is actually for
```

| Code | Error (1.6 wording) | Current wording |
|---|---|---|
| `int x = 2147483647;` | none — valid | — |
| `int x = 2147483648;` | `integer number too large` | `integer number too large` (unchanged) |
| `int x = 2147483648L;` | `possible loss of precision, found long, required int` | `incompatible types: possible lossy conversion from long to int` |
| `int x = true;` | `incompatible types, found boolean, required int` | `incompatible types: boolean cannot be converted to int` |

Sir compiles all three live: `2147483647` runs and prints; changing the last
digit gives `integer number too large`; adding the `l`/`L` **changes the error**
to the loss-of-precision one.

The `L` does **not** solve anything. You still cannot store that magnitude in an
`int` — it exceeds the range. All the suffix does is change *how the compiler
classifies the literal*, and therefore which of the two errors you see. That is
the entire point of the exercise.

> **Note:** `integer number too large` is the one message in this whole lecture
> that is **byte-for-byte identical on JDK 1.6 and JDK 26** — verified. It is a
> lexical error raised while reading the literal, not a type error, which is why
> it escaped the JDK 7 diagnostic rewrite.

Prefer capital **`L`** in real code. Sir allows either, but a lowercase `l` is
almost indistinguishable from the digit `1` in most fonts — `1l` versus `11` is a
real bug source.

> ⚠️ **Modern Java — the arithmetic traps around `int` overflow got real support.**
> Sir's point is about *literals*; the same range limit bites at *runtime*, where
> Java silently wraps around instead of failing:
>
> ```java
> System.out.println(Integer.MAX_VALUE + 1);   // -2147483648 — silent wraparound
> ```
>
> **Java 8** added `Math` methods that throw instead of wrapping, plus exact-width
> helpers:
>
> ```java
> Math.addExact(Integer.MAX_VALUE, 1);      // throws ArithmeticException: integer overflow
> Math.multiplyExact(100000, 100000);       // throws ArithmeticException
> Math.toIntExact(3_000_000_000L);          // throws ArithmeticException
> Math.floorDiv(-7, 2);                     // -4  (int division would give -3)
> ```
>
> Silent wraparound is still the default for `+`, `-` and `*` and always will be —
> that is specified behaviour, not a bug. But money, sizes and counters should use
> the `*Exact` methods (or `long`, or `BigInteger`). This is a very common
> follow-up in interviews that start from "what is the range of `int`."

`long` continues in the next lecture.

---

## Code from the lecture

Everything Sir compiles, in one file. The invalid lines are commented with the
error each one actually produces on a current JDK.

```java
class Test {
    public static void main(String[] args) {
        // --- strongly typed: legal in C, rejected by Java ---
        // int x = 10.5;           // CE: incompatible types: possible lossy conversion from double to int
        // boolean b = 0;          // CE: incompatible types: int cannot be converted to boolean

        // --- signed types ---
        int    p1 = +10;
        int    p2 = -10;
        double p3 = -10.5;
        // char    ch = -'a';      // CE: incompatible types: possible lossy conversion from int to char
        // boolean bb = -false;    // CE: bad operand type boolean for unary operator '-'

        // --- byte ---
        byte b1 = 10;              // OK, prints 10
        byte b2 = -127;            // OK
        byte b3 = 127;             // OK, Byte.MAX_VALUE
        // byte b4 = 128;          // CE: incompatible types: possible lossy conversion from int to byte
        // byte b5 = 10.5;         // CE: incompatible types: possible lossy conversion from double to byte
        // byte b6 = true;         // CE: incompatible types: boolean cannot be converted to byte
        // byte b7 = "durga";      // CE: incompatible types: String cannot be converted to byte

        // why b1 compiles at all: constant expression that fits (JLS 5.2)
        final int c = 127;
        byte b8 = c;               // OK — c is a constant variable
        int  n  = 127;
        // byte b9 = n;            // CE: incompatible types: possible lossy conversion from int to byte

        // --- short ---
        short s1 = 32767;          // OK, Short.MAX_VALUE
        // short s2 = 32768;       // CE: incompatible types: possible lossy conversion from int to short
        // short s3 = 10.5;        // CE: incompatible types: possible lossy conversion from double to short
        // short s4 = true;        // CE: incompatible types: boolean cannot be converted to short

        // --- int ---
        int x1 = 2147483647;       // OK, Integer.MAX_VALUE
        // int x2 = 2147483648;    // CE: integer number too large   (lexical, not a type error)
        // int x3 = 2147483648L;   // CE: incompatible types: possible lossy conversion from long to int
        // int x4 = true;          // CE: incompatible types: boolean cannot be converted to int
        long x5 = 2147483648L;     // OK — this is what the L suffix is for

        System.out.println(b1 + " " + b3 + " " + b8 + " " + s1 + " " + x1 + " " + x5);
        System.out.println(p1 + " " + p2 + " " + p3);
    }
}
```

---

## Rules to memorize

1. Every variable and every expression has a type; every assignment is checked
   for type compatibility. → Java is **strongly typed**. `var` (Java 10) infers a
   type, it does not remove one.
2. Interview: Java is **not** a pure OOP language — missing OOP features plus
   primitives are non-objects. Answer **no**, and have both reasons ready.
3. **8 primitives:** `byte`, `short`, `int`, `long`, `float`, `double`, `boolean`,
   `char`.
4. Integral = `byte short int long`; floating-point = `float double`;
   non-numeric = `boolean char` (with `char` really being an unsigned integral
   type).
5. Except `boolean` and `char`, all types are **signed**. `char` is the only
   **unsigned** primitive: `0` to `65535`.
6. **`byte`:** 1 byte / 8 bits; **−128 to +127**; MSB is the sign bit (0 = +,
   1 = −); positives direct, negatives in **two's complement** — where all 8 bits
   are value bits and the top one is worth −128.
7. Out-of-range but numerically compatible → **possible loss of precision**
   (`possible lossy conversion` on modern javac). Completely different kind →
   **incompatible types**.
8. Integral literals are **`int` by default**; `10.5` is **`double` by default**.
9. `byte b = 10;` compiles because a **constant expression that fits** may narrow
   implicitly (JLS §5.2). `int n = 10; byte b = n;` does not.
10. `byte + byte` is an **`int`** expression — binary numeric promotion.
11. **`byte` best choice:** stream data from a file or a network.
    `FileOutputStream.write` takes a `byte[]`.
12. **`short`:** 2 bytes / 16 bits; **−32,768 to 32,767**; most rarely used; meant
    for 16-bit processors; effectively obsolete.
13. **`int`:** 4 bytes / 32 bits; **−2,147,483,648 to 2,147,483,647**; most
    commonly used.
14. An unsuffixed integral literal outside the `int` range → **integer number too
    large** (not "found long").
15. Suffix `l` / `L` makes a **`long`** literal; assigning it to an `int` → the
    lossy-conversion error instead. The `L` changes the *error*, not the outcome.

---

## Exam and interview points

1. **`int x = 10.5;` and `boolean b = 0;` are illegal in Java.** The classic
   strongly-typed demonstration. `int x = 10.5;` is legal C; `boolean b = 0;` is
   not legal C either, because pre-C99 C had no boolean at all.
2. **"Strongly typed" means type checking is strong** — not that you type hard on
   the keyboard, and not that you must write every type out (`var` still infers a
   fixed static type).
3. **"Is Java pure OOP?" → No**, with two reasons: several OOP features are
   unsupported, and we depend on primitives, which are non-objects. Say
   "user-defined operator overloading" and "multiple inheritance **of classes**"
   — Java has always had multiple inheritance of type, and since Java 8, of
   behaviour via `default` methods.
4. **`byte b = 128;` is NOT `incompatible types` in Sir's taxonomy** — it is
   `possible loss of precision` (found `int`). On JDK 8+ the printed message
   begins `incompatible types:` for *both* families, so read the second half of
   the sentence: `possible lossy conversion from X to Y` versus `X cannot be
   converted to Y`.
5. **`byte b = true;` and `byte b = "durga";` are the genuine incompatible-types
   cases.** The found type for the second is `java.lang.String`, not any string
   primitive — Java has none.
6. **Two's complement, properly.** All 8 bits are value bits with the MSB weighted
   −2⁷. That, not "one bit for sign", is what explains −128 and the −128/+127
   asymmetry. `Byte.MIN_VALUE` is `1000 0000`.
7. **"Use `byte` because the number is small" is the wrong answer.** The intended
   answer is **streams** — file and network data is a sequence of bytes, which is
   why `FileOutputStream.write` takes `byte[]`.
8. **Do not claim you use `short` regularly.** The expected answer is "most rarely
   used, meant for 16-bit processors, now outdated." If you name the chip, name
   the **8086** — the 8085 is an 8-bit processor.
9. **`int x = 2147483648;` → `integer number too large`**, not a loss-of-precision
   error. It is a *lexical* error on the literal, which is also why this one
   message is unchanged from JDK 1.6 to JDK 26.
10. **`int x = 2147483648L;` → lossy conversion from `long` to `int`.** The `L`
    suffix is the entire difference between points 9 and 10, and it fixes neither
    assignment. Prefer capital `L` so it is not read as digit `1`.
11. **`byte + byte` is `int`.** Binary numeric promotion pushes everything narrower
    than `int` up to `int`, so `byte r = p + q;` does not compile.
12. **`byte b = 10;` compiles only because `10` is a constant expression that
    fits.** Make it a non-`final` `int` variable and the same assignment fails —
    this is JLS §5.2, and it is a favourite trick question.
13. **`char` is unsigned, `0`–`65535`,** and is the only unsigned primitive. Java
    has no unsigned *types*, but since Java 8 it has unsigned *operations*
    (`Integer.toUnsignedString`, `divideUnsigned`, `Byte.toUnsignedInt`).
14. **`int` arithmetic wraps silently on overflow.** `Integer.MAX_VALUE + 1` is
    `Integer.MIN_VALUE`. Since Java 8, `Math.addExact` / `multiplyExact` /
    `toIntExact` throw `ArithmeticException` instead — the expected answer when an
    interviewer follows "what is the range of `int`" with "so what happens if you
    exceed it".
15. **Error wording is version-dependent, error *meaning* is not.** Sir compiles on
    JDK 1.6 (`possible loss of precision`, `found:` / `required:`); JDK 8 through
    26 say `incompatible types: possible lossy conversion from X to Y`. Know both
    phrasings and which compiler produces which.

---

**Next:** Video 003 — Data Types Part 2
