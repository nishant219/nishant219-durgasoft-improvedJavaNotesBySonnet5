# Video 003 — Data Types Part 2

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part- 3 || Data Types part-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 3 of 203 |
| Series | Language Fundamentals · Part 3 of 16 |
| Topic | Data types part 2 — long, float, double, boolean, char, primitive summary table, null |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 55m 07s (3307 seconds) |
| Video ID | HYAosZptldA |
| Watch | https://www.youtube.com/watch?v=HYAosZptldA |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Video 002 ended on `byte`, `short` and `int`. This session finishes the eight
primitives and closes the topic:

1. When the **`int` range is not enough** → `long`
2. `long` — the two "why long?" examples, size, range
3. `byte`/`short`/`int`/`long` are for **integral values only**
4. **`float` vs `double`** — chosen by *accuracy*, not by "small vs big number"
5. **`boolean`** — no size, no range, no C-style 0/1
6. **`if` / `while` with integers** — legal in C, illegal in Java
7. **`char`** — why Java's is 2 bytes when C's is 1
8. The **summary table** of all 8 primitives: size, range, wrapper, default
9. **`null`** is for object references only — never for primitives

---

## 00:04 — When `int` is not enough: the `long` type

Sir opens by asking the class to recite the `int` range:

**`int` range:** −2,147,483,648 to 2,147,483,647

A ten-digit number. "Seems to be a big range" — and it is. But *sometimes it is
still not enough*, and that is when you reach for `long`.

### 00:58 — Example 1: distance travelled by light in 1,000 days

The setup: speed of light is 3 × 10⁸ m/s (3 × 10¹⁰ cm/s), which Sir converts to
**126,000 miles per second**. Multiply out — × 60 for a minute, × 60 for an
hour, × 24 for a day, × 1,000 for a thousand days — and the result blows past
`int`.

> **Board:** Sometimes `int` may not be enough to hold big values. Then we
> should go for `long` type.
>
> Example 1: the amount of distance travelled by light in 1,000 days — to hold
> this value `int` may not be enough; we should go for `long`.

> ❗ **Correction — light travels about 186,000 miles per second, not 126,000.**
> 299,792,458 m/s ÷ 1,609.344 m per mile ≈ **186,282 miles/s**. Sir's own metric
> figure (3 × 10⁸ m/s) is right; only the mile conversion slipped. The teaching
> point is untouched — either number overflows `int` once you multiply by
> 86,400,000 — but do not quote 126,000 in an interview.

> ❗ **Correction — the code as written silently overflows. `long` on the left does not help.**
> This is the single most valuable trap in the whole lecture, and it is easy to
> miss because it **compiles cleanly** — no error, no warning, not even with
> `-Xlint:all`:
>
> ```java
> long l = 126000 * 60 * 60 * 24 * 1000;
> System.out.println(l);   // prints -1342095360  (!)
> ```
>
> Every operand is an `int` literal, so the whole expression is evaluated in
> **32-bit `int` arithmetic** and wraps around. Widening to `long` happens at
> the assignment — *after* the damage is done. The fix is to make one operand a
> `long` so the promotion happens during the multiply:
>
> ```java
> long l = 126000L * 60 * 60 * 24 * 1000;
> System.out.println(l);   // 10886400000000  — correct
> ```
>
> Declaring the variable `long` is necessary but not sufficient. The *expression*
> has to be `long` too.

### 05:01 — Example 2: the size of a big file

A file with lakhs of pages, hundreds of lines per page, hundreds of characters
per line. To hold that count, `int` may not be enough — which is why the JDK
itself declares it as `long`:

```java
import java.io.File;

class Test {
    public static void main(String[] args) {
        File f = new File("report.txt");
        long l = f.length();          // length() returns long, not int
        System.out.println(l);
    }
}
```

Sir's emphasis: *"it's not my own creation, it's a part of the API."* The
library designers hit the same wall you would.

> **Board:** Example 2: the number of characters present in a big file may
> exceed `int` range. Hence the return type of `length()` is **`long` but not
> `int`**.

> ❗ **Correction — `File.length()` returns a size in *bytes*, not a count of characters.**
> The javadoc is explicit: "the length, in bytes, of the file". For a pure-ASCII
> file the two numbers coincide, which is why the confusion survives. For
> anything else they do not:
>
> ```java
> // u.txt contains the 8 Telugu characters నమస్కారం, saved as UTF-8
> new File("u.txt").length()                        // 24  — bytes on disk
> Files.readString(Path.of("u.txt")).length()       //  8  — characters
> ```
>
> Same file, three-to-one difference. The *reason* the return type is `long` is
> exactly as Sir says — file sizes exceed `int` — so the exam answer is safe.
> Just say "size in bytes" rather than "number of characters."

> ⚠️ **Modern Java — `java.io.File` is the legacy API; NIO.2 replaced it in Java 7.**
> `File.length()` still works and still returns `long`, but it reports `0` for a
> missing file — you cannot tell "empty" from "does not exist." The NIO.2
> replacement throws instead:
>
> ```java
> import java.nio.file.*;
>
> long size = Files.size(Path.of("report.txt"));   // throws IOException if absent
> ```
>
> Both return `long`, so the lecture's point stands. `Path` + `Files` (JSR 203,
> Java 7) is what new code should use; `File` is what you will meet in every
> codebase written before 2011.

### 07:49 — `long`: size and range

| | |
|---|---|
| Size | 8 bytes (64 bits) |
| Range | −2⁶³ to 2⁶³ − 1 |

Sir's advice: do not memorise the expanded decimal. *"Don't worry about that
value — even I don't know it."* The formula is the answer. (For the record it is
−9,223,372,036,854,775,808 to 9,223,372,036,854,775,807, and
`Long.MIN_VALUE` / `Long.MAX_VALUE` will print it for you.)

> ⚠️ **Modern Java — two tools that did not exist when this was recorded.**
>
> **Underscores in numeric literals (Java 7, JSR 334)** make big constants
> readable, and the compiler strips them:
>
> ```java
> long l = 126_000L * 60 * 60 * 24 * 1_000;
> int  max = 2_147_483_647;
> ```
>
> **`Math.*Exact` (Java 8)** turns the silent overflow from the correction above
> into a loud one — use it whenever a wrap-around would be a bug rather than a
> feature:
>
> ```java
> Math.multiplyExact(1_000_000, 1_000_000);   // throws ArithmeticException: integer overflow
> Math.multiplyExact(1_000_000, 1_000_000L);  // 1000000000000 — long overload, fine
> ```
>
> Also available: `addExact`, `subtractExact`, `incrementExact`, `negateExact`,
> `toIntExact`. Java 18 added `Math.divideExact`.

### 08:53 — Everything so far is integral only

Four types down: `byte`, `short`, `int`, `long`.

> **Board:** All the above data types (`byte`, `short`, `int`, `long`) are for
> representing **integral values**.
>
> If we want to represent **floating-point values** (a number *with* a decimal
> point), we cannot use these. We should go for **floating-point data types**.

---

## 10:52 — Floating-point types: `float` and `double`

Two of them: **`float`** and **`double`**.

### 12:03 — The wrong criterion (most people fail this)

The instinct, carried over from the integral types, is:

- small floating-point value → `float`
- big floating-point value → `double`

Sir is blunt: *"No, it is not the criteria — most of the people are going to
fail."* For `byte`/`short`/`int`/`long`, "smaller value, smaller type" genuinely
*is* the rule. Do not copy that reasoning across to `float` and `double`.

### 12:31 — The right criterion: accuracy

Take `10.0 / 3` → 3.3333…, a number that never terminates. How many digits do
you actually need?

| Requirement | Choose |
|---|---|
| 5 to 6 decimal places of accuracy | `float` |
| 14 to 15 decimal places of accuracy | `double` |

So `float` = less accuracy, `double` = more accuracy. In the formal vocabulary:

| Type | Follows | Meaning |
|---|---|---|
| `float` | single precision | less accuracy |
| `double` | double precision | more accuracy |

*"Precision is nothing but accuracy."*

> ❗ **Correction — those are *significant digits*, not *decimal places*.**
> The distinction matters as soon as the number is not close to 1. IEEE 754
> `binary32` carries a 24-bit significand ≈ **7 significant decimal digits**;
> `binary64` carries 53 bits ≈ **15 to 17 significant digits**. Run it:
>
> ```java
> System.out.println(10.0f / 3);   // 3.3333333          — 8 digits total, 7 significant
> System.out.println(10.0  / 3);   // 3.3333333333333335 — 17 significant
> ```
>
> For 3.33… the two phrasings happen to agree, which is why the lecture's
> version survives. But a `float` holding 12,345,678.9 has **zero** correct
> decimal places — it cannot even represent the integer part exactly. Sir's
> 5–6 / 14–15 split is the right *ranking* and the expected OCJP answer; the
> accurate wording is "significant digits."

### 14:22 — Size

| Type | Size |
|---|---|
| `float` | 4 bytes (32 bits) |
| `double` | 8 bytes (64 bits) |

### 14:42 — Range, and Sir's own correction

`E38` is **exponential form**: `3.4E38` means 3.4 × 10³⁸.

On the first pass Sir reads the two magnitudes in the wrong type-order — 1.7E38
against float, 3.4E38 against double. At **[18:05]** he stops and says *"range
wise, a small correction is there… reverse here"*, then fixes it. The value he
writes for `double` on that second pass is still `1.7E38`; the exponent is only
corrected to `E308` when he fills in the summary table at **[48:12]**.

**Take the summary table as the final board version:**

| Type | Range | Verified constant |
|---|---|---|
| `float` | −3.4E38 to 3.4E38 | `Float.MAX_VALUE` = `3.4028235E38` |
| `double` | −1.7E308 to 1.7E308 | `Double.MAX_VALUE` = `1.7976931348623157E308` |

A trap that follows directly from this and shows up in interviews:
`Float.MIN_VALUE` is **not** the most negative float. It is the smallest
*positive* non-zero value, `1.4E-45`. The most negative float is
`-Float.MAX_VALUE`. Same for `Double`. The integral wrappers do not behave this
way — `Integer.MIN_VALUE` really is the most negative `int`.

> ⚠️ **Modern Java — `strictfp` became a no-op in Java 17.**
> When this was recorded, floating-point results could differ across platforms
> unless a method or class was marked `strictfp`, which forced strict IEEE 754
> evaluation. **JEP 306 (Java 17)** made all floating-point expressions strict
> by default, so the keyword now changes nothing:
>
> ```text
> warning: [strictfp] as of release 17, all floating-point expressions are
> evaluated strictly and 'strictfp' is not required
> ```
>
> It still parses and still compiles — it is one of the 11 modifier keywords in
> video 001 — but writing it today is dead code.

---

## 19:44 — The `boolean` data type

### 19:51 — Size: not applicable

The class, arriving from C/C++, offers 1 bit, 1 byte, 2 bytes, "zero means
false, non-zero means true." Sir's response: *"that type of terminology is
applicable only for old languages, but not for Java."*

If someone with a C background asks you the size of a Java `boolean`:

- The correct answer is **not applicable**.
- The answer that earns marks is **"virtual machine dependent"** — Sir calls
  this phrasing *"really appreciable."*
- Depending on the JVM it may occupy one bit or one byte. You cannot state a
  fixed size.

The JLS backs this up: it defines `boolean` by its *values*, never by a width.
(For your own curiosity, HotSpot in practice gives a `boolean` field one byte,
a `boolean[]` element one byte, and a local variable a full 32-bit stack slot —
three different answers on one JVM, which is exactly why the language refuses to
promise a number.)

### 21:16 — Range: not applicable

You cannot say "true to false" or "false to true" — that would make one of them
the minimum and the other the maximum. **Both are at the same level.** There is
no ordering, so there is no range.

> **Board:**
>
> | | |
> |---|---|
> | Size | not applicable (virtual machine dependent) |
> | Range | not applicable, but allowed values are `true` or `false` |

Allowed values: `true` or `false`, **lowercase**, and nothing else.

Nothing in this section has changed since the recording. `boolean` is one of the
few corners of Java that has never moved.

### 22:50 — The four assignment quizzes

Sir compiles each of these live so the class sees four *different* outcomes.
Assume every line sits inside a class named `Test`.

| Code | Valid? | What the compiler says |
|---|---|---|
| `boolean b = true;` | ✅ valid | nothing — this is the only legal form |
| `boolean b = 0;` | ❌ CE | `incompatible types: int cannot be converted to boolean` |
| `boolean b = True;` | ❌ CE | `cannot find symbol — symbol: variable True, location: class Test` |
| `boolean b = "true";` | ❌ CE | `incompatible types: String cannot be converted to boolean` |

**Why `0` fails:** an integral literal is `int` by default. In C, `0` means
false. Java has no such rule — there is no conversion, implicit or explicit,
between `int` and `boolean`.

**Why `True` gives a *different* error — think like the compiler:**

1. Is `True` a boolean value? No — `true` is lowercase.
2. Is it an `int`? No.
3. Is it a `String`? No — a `String` needs double quotes.

It is not a valid literal for **any** type, so the compiler's only remaining
interpretation is that it must be a **variable name**. You never declared a
variable called `True`, so: `cannot find symbol`. The same happens for `TRUE`,
`FALSE`, or any other miscased spelling.

**Why `"true"` fails:** double quotes make it a `String`. *"String and boolean —
there is no compatibility."* Note this is a **compile** error, not a silent
conversion; Java will not parse the text for you. If you actually want that
conversion you must ask for it: `boolean b = Boolean.parseBoolean("true");`.

> ⚠️ **Modern Java — the error messages were reworded, and one of these lines is no longer an error.**
>
> **1. Message format.** Sir reads out the Java 6 wording, `incompatible types
> — found: int, required: boolean`. Modern javac (verified on JDK 26) says:
>
> ```text
> error: incompatible types: int cannot be converted to boolean
> ```
>
> Same error, one sentence instead of two lines. The `cannot find symbol /
> symbol: variable True / location: class Test` message is **unchanged** —
> word for word what Sir predicts.
>
> **2. Autoboxing.** Since **Java 5** this compiles, because `Boolean.TRUE` is a
> `Boolean` object and unboxing inserts the `.booleanValue()` call for you:
>
> ```java
> boolean b = Boolean.TRUE;   // valid — unboxing, Java 5+
> ```
>
> Sir's `True` is still a compile error because it is a bare undeclared
> identifier. But if an interviewer writes `Boolean.TRUE`, the answer flips.
> Watch for the null case: `Boolean flag = null; if (flag)` compiles and throws
> `NullPointerException` at runtime.

### 29:47 — `if` and `while` with numbers: C versus Java

The second exam pattern that comes out of `boolean`.

#### Example A — `if (x)` where `x` is an `int`

```java
class Test {
    public static void main(String[] args) {
        int x = 0;
        if (x) {                             // CE: incompatible types: int cannot be converted to boolean
            System.out.println("hello");
        } else {
            System.out.println("hi");
        }
    }
}
```

| Language | Result |
|---|---|
| C / C++ | valid — `0` is false, so it prints `hi` |
| Java | **compile error** — `if` always expects a `boolean`, you supplied an `int` |

The wrong answer here is "it prints hi." The program never runs.

#### Example B — `while (1)`

```java
class Test {
    public static void main(String[] args) {
        while (1) {                          // CE: incompatible types: int cannot be converted to boolean
            System.out.println("hello");
        }
    }
}
```

Sir: *"Don't tell infinite number of times."* That is the C answer, where `1` is
true. In Java, `while` expects `true`/`false` and `1` is an `int` — compile
error. If you want the infinite loop, you write `while (true)`.

Both snippets are valid C and invalid Java *"because the Java compiler is very
strong"* — the same strong-typing theme as video 002.

---

## 33:28 — The `char` data type: why 2 bytes?

A standing fresher-interview question: **what is the size of `char` in Java, and
why is it 2 bytes instead of 1?**

| Language | Size of `char` |
|---|---|
| C / C++ | 1 byte (8 bits) |
| Java | 2 bytes (16 bits) |

The one-line answer Sir wants you to have ready: **Java is Unicode based, old
languages are ASCII based.** Then be ready to explain it.

### 34:38 — Old languages are ASCII based

Characters you can use in a C program: `a–z`, `A–Z`, `0–9`, `$`, `#`, `+`, `-`,
and the other specials. The number of distinct allowed characters is **≤ 256**.

Why 8 bits cover that — Sir counts the powers of two on the board:

| Bits | Distinct values |
|---|---|
| 1 | 2 |
| 2 | 4 |
| 3 | 8 |
| 4 | 16 |
| 5 | 32 |
| 6 | 64 |
| 7 | 128 |
| 8 | 256 |

≤ 256 characters → 8 bits are enough → `char` is **1 byte**.

> ❗ **Correction — ASCII itself is 128 characters, not 256.**
> ASCII is a **7-bit** encoding: code points 0–127, and that is the entire
> standard. The 256 figure comes from the 8-bit *extensions* built on top of it
> — Latin-1 / ISO-8859-1, Windows-1252, the old DOS code pages — which fill
> 128–255 with a region-specific second half. Those are not ASCII, and they do
> not agree with each other, which is precisely the mess Unicode was invented to
> end. Sir's arithmetic still works (a C `char` is one byte and can hold 256
> distinct values); the label "256 ASCII characters" is what is inaccurate.

### 36:48 — Java is Unicode based

In a Java program you can use all of those characters **plus** the alphabet of
any language you like. Sir writes Telugu (అ …) and Hindi (अ …) on the board and
mentions Tamil and Chinese:

```java
class Test {
    public static void main(String[] args) {
        char telugu  = 'అ';
        char hindi   = 'अ';
        char chinese = '中';
        System.out.println("" + telugu + hindi + chinese);
    }
}
```

That set is **definitely greater than 256** and **≤ 65,536**. 8 bits are not
enough; you need **16 bits**. Hence Java's `char` is **2 bytes**.

> **Board (two columns):**
>
> **Old languages (C / C++):** ASCII based. The number of different ASCII
> characters is ≤ 256. To represent them, 8 bits are enough. Hence the size of
> `char` is **1 byte**.
>
> **Java:** Unicode based. The number of different Unicode characters is
> **> 256 and ≤ 65,536**. 8 bits may not be enough; compulsory **16 bits**.
> Hence the size of `char` in Java is **2 bytes**.

### 38:59 — The overlap with ASCII

*"The first 256 Unicode characters are nothing but the ASCII characters."*
Example — lowercase `'a'`:

| | Value |
|---|---|
| ASCII of `'a'` | 97 |
| Unicode of `'a'` | 97 (the same) |

For the overlapping block the numbers are identical; beyond it, characters have
a Unicode code point and no ASCII value at all.

> ❗ **Correction — the ASCII overlap is the first 128, not the first 256.**
> Unicode's first **128** code points (U+0000–U+007F) are ASCII exactly. Code
> points U+0080–U+00FF match **Latin-1 / ISO-8859-1**, which Unicode also
> adopted wholesale — that is where the 256 comes from. The headline claim is
> untouched: `'a'` is 97 in both, and every ASCII character keeps its number in
> Unicode.

> ❗ **Correction — Unicode is not capped at 65,536, and a `char` is not a character.**
> This is the biggest thing the lecture gets wrong, and it was already wrong in
> 2004. Unicode 2.0 (1996) broke the 16-bit ceiling. Today the codespace is
> **U+0000 to U+10FFFF — 1,114,112 code points**, of which roughly 155,000 are
> assigned:
>
> ```java
> System.out.println(Character.MAX_CODE_POINT);   // 1114111  (0x10FFFF)
> System.out.println((int) Character.MAX_VALUE);  //   65535  (0xFFFF)
> ```
>
> Those two numbers are different for a reason. Since **Java 5**, a `char` is
> defined as a **UTF-16 code unit**, not a character. Anything above U+FFFF (a
> *supplementary* character — emoji, historic scripts, rarer CJK) does not fit
> in one `char` and is stored as a **surrogate pair** of two `char`s:
>
> ```java
> String s = "😀";                                  // U+1F600
> s.length();                                       // 2  — two char code units
> s.codePointCount(0, s.length());                  // 1  — one actual character
> s.charAt(0);                                      // '\uD83D' — a lone high surrogate, meaningless alone
> ```
>
> So the exam answer stays: **`char` is 2 bytes because Java is Unicode based.**
> The accurate sentence to add in an interview is: *"a `char` holds one UTF-16
> code unit; characters outside the Basic Multilingual Plane need two."* That
> one line separates people who read the spec from people who memorised a slide.

### 43:29 — `char`: size and range

Sir first says "0 to 65530", then corrects himself: there are 65,536
representable values in total, and zero is included, so the top is 65,535.

| | |
|---|---|
| Size | 2 bytes |
| Range | 0 to 65,535 |

`char` is the only **unsigned** primitive in Java — there is no negative `char`,
which is why the range starts at 0 rather than at −2¹⁵. Confirmed by
`Character.MIN_VALUE` (0) and `Character.MAX_VALUE` (65535).

How to *write* `char` values — quotes, escapes, `'A'`, integer forms — is
deferred to the **literals** session.

> ⚠️ **Modern Java — the code-point APIs, and where `char` went inside `String`.**
>
> **Code-point APIs.** Because a `char` cannot hold every character, iterate by
> code point rather than by index whenever text may be non-BMP:
>
> ```java
> "😀abc".codePoints().forEach(cp -> System.out.println(Integer.toHexString(cp)));
> // 1f600, 61, 62, 63  — four characters, even though length() is 5
> ```
>
> `String.codePoints()` and `String.chars()` arrived in **Java 8**;
> `Character.codePointAt`, `.toChars`, `.isSupplementaryCodePoint` in Java 5.
>
> **Compact strings (Java 9, JEP 254).** Sir's mental model — a `String` is a
> `char[]`, two bytes per character — was true through Java 8. Since Java 9 a
> `String` holds a `byte[]` plus a one-byte coder flag, and a string whose
> characters all fit in Latin-1 is stored at **one byte per character**. Java
> programs got measurably smaller heaps for free. The `char` *type* is still two
> bytes; the *storage inside `String`* is not.
>
> **Unicode version.** Each JDK ships the `Character` tables for a particular
> Unicode release (Java 8 → Unicode 6.2, Java 17 → 13.0, Java 21 → 15.0), so
> `Character.isLetter` can answer differently across JDKs for newly added
> characters.

---

## 44:22 — Summary of Java's primitive data types

*"Let me keep one small summary table, so that you can be aware of all the
things at a single slap."* Five columns: data type, size, range, corresponding
wrapper class, and default value — *"if you are not providing any value, then
the JVM is always going to provide a default value."*

| Data type | Size | Range | Wrapper class | Default value |
|---|---|---|---|---|
| `byte` | 1 byte | −2⁷ to 2⁷−1 = −128 to 127 | `Byte` | `0` |
| `short` | 2 bytes | −2¹⁵ to 2¹⁵−1 = −32,768 to 32,767 | `Short` | `0` |
| `int` | 4 bytes | −2³¹ to 2³¹−1 = −2,147,483,648 to 2,147,483,647 | `Integer` | `0` |
| `long` | 8 bytes | −2⁶³ to 2⁶³−1 | `Long` | `0L` |
| `float` | 4 bytes | −3.4E38 to 3.4E38 | `Float` | `0.0f` |
| `double` | 8 bytes | −1.7E308 to 1.7E308 | `Double` | `0.0d` |
| `boolean` | not applicable (JVM dependent) | not applicable (allowed: `true` / `false`) | `Boolean` | `false` |
| `char` | 2 bytes | 0 to 65,535 | `Character` | `' '` |

### 49:17 — The default-value points Sir stresses

- Integral types (`byte`, `short`, `int`, `long`) default to **`0`**.
- `float` and `double` default to **`0.0`**.
- **`boolean` defaults to `false`** in Java.
- **`char` defaults to `0`** — Sir adds *"zero represents a space character,
  remember this one."*

Defaults apply to **fields and array elements only**. A local variable has no
default — reading one before you assign it is a compile error
(`variable x might not have been initialized`). That distinction is worth more
exam marks than the default values themselves.

> ❗ **Correction — `char`'s default `' '` is NUL, not a space character.**
> The space character is **32** (`' '`). Code point **0** is **NUL**, a
> non-printing control character. Verify it:
>
> ```java
> char c = 0;
> System.out.println(c == ' ');                  // false
> System.out.println(Character.isSpaceChar(c));  // false
> System.out.println(Character.getName(c));      // NULL
> ```
>
> The confusion is a display artefact: printing `' '` to a terminal usually
> produces nothing visible, which *looks* like a blank. The value is 0 — say
> "the null character" or "`' '`", never "space."

> ❗ **Correction — C++ does not default `bool` to `true`.**
> Sir contrasts Java's `false` with *"in C++ the default value for boolean is
> true."* No C++ standard has ever said that. A C++ `bool` with static storage
> duration zero-initialises to **`false`**; an uninitialised automatic (local)
> `bool` holds an **indeterminate** value, and reading it is undefined
> behaviour. The Java half of the sentence is correct and is what the exam
> tests: **Java's `boolean` default is `false`.** There is no C++ contrast to
> draw.

**Wrapper names to match exactly:** `Byte`, `Short`, **`Integer`** (not `Int`),
`Long`, `Float`, `Double`, `Boolean`, **`Character`** (not `Char`). Six of the
eight are just the primitive with a capital letter; the two exceptions are
exactly the two that get asked.

> ⚠️ **Modern Java — never construct a wrapper with `new`.**
> Every wrapper constructor (`new Integer(5)`, `new Boolean(true)`, …) was
> **deprecated in Java 9** and **deprecated for removal in Java 16** (JEP 390,
> value-based classes). Use the factory instead:
>
> ```java
> Integer bad  = new Integer(5);      // warning: [deprecation] Integer(int) has been deprecated
> Integer good = Integer.valueOf(5);  // preferred — and cached for −128..127
> Integer best = 5;                   // autoboxing calls valueOf for you (Java 5+)
> ```
>
> `valueOf` returns shared instances for small values, which is the whole reason
> the `Integer a = 127, b = 127; a == b` (true) versus `a = 128, b = 128; a == b`
> (false) interview puzzle works. `new` would defeat the cache and allocate every
> time.

> ⚠️ **Modern Java — `var` (Java 10) for local variables.**
> Local declarations can infer their type, including primitives. It does **not**
> make Java dynamically typed — `x` below is an `int`, permanently:
>
> ```java
> var x = 10;          // int
> var d = 10.0;        // double  — NOT float; floating literals default to double
> var c = 'a';         // char
> var f = 0.0f;        // float   — the f suffix is what makes it a float
> ```
>
> `var` is a **contextual keyword** (see video 001), not a reserved word, so
> `int var = 10;` still compiles. Fields, parameters and return types cannot use
> it.

---

## 51:54 — `null` is for object references, never primitives

One clarification to close the topic. **`null` is the default value for any
object reference** — `String`, `Student`, `Customer`, any class or interface
type, and arrays.

**You cannot apply `null` to a primitive.** Sir stresses this even for `char`,
because `char`'s default of 0 tempts people into thinking it might accept one:

```java
class Test {
    public static void main(String[] args) {
        String s  = null;   // valid — object reference
        // char ch = null;  // CE: incompatible types: <null> cannot be converted to char
    }
}
```

> **Board:** `null` is the default value for **object references**, and we can't
> apply it to **primitives**. If we are trying to use it for a primitive, then we
> will get a **compile-time error**.
>
> Example: `char ch = null;` → `incompatible types`, found null type, required
> `char`.

The exam point is that this is a **compile-time** error, not a
`NullPointerException`. The program never gets far enough to run.

> ⚠️ **Modern Java — the wrapper detour, and helpful NPEs (Java 14).**
> Autoboxing (Java 5) creates a path from `null` to a primitive that did not
> exist when the "primitives can never be null" rule was formulated. This
> compiles perfectly and fails at runtime:
>
> ```java
> Integer count = null;
> int n = count;       // compiles — unboxes via count.intValue() → NullPointerException
> ```
>
> So the precise modern statement is: *a primitive variable can never **hold**
> null, but unboxing a null wrapper throws NPE.* This is the single most common
> real-world NPE in Java code.
>
> **JEP 358 (Java 14)** made the diagnosis trivial — helpful NullPointerException
> messages are on by default since Java 15:
>
> ```text
> Exception in thread "main" java.lang.NullPointerException: Cannot invoke
> "java.lang.Integer.intValue()" because "count" is null
> ```
>
> Before Java 14 you got a bare stack trace and a line number. Since **Java 8**,
> `Optional<T>` is the intended way to model "a value that may be absent"
> without reaching for `null` at all.

That closes the primitive data types. The next topic in the series is
**literals** — how you actually write the values these types hold.

---

## Rules to memorise

1. When `int` is not enough → **`long`**. Examples: the light-distance product;
   `File.length()` returns `long`.
2. `long`: **8 bytes / 64 bits**, range **−2⁶³ to 2⁶³−1**.
3. `byte`, `short`, `int`, `long` are integral only. A decimal point means
   **`float` / `double`**.
4. `float` vs `double` is decided by **accuracy**, not by "small vs big":
   **5–6 digits → `float`**, **14–15 digits → `double`**.
5. `float` = **single precision** (4 bytes, ±3.4E38). `double` = **double
   precision** (8 bytes, ±1.7E308).
6. `boolean`: size **not applicable** (JVM dependent), range **not applicable**,
   values **`true` / `false`** only.
7. `boolean b = 0;` → incompatible types. `boolean b = True;` → **cannot find
   symbol**. `boolean b = "true";` → found `String`.
8. `if (someInt)` and `while (1)` compile in C, **not** in Java.
9. Java `char` is **2 bytes** because Java is **Unicode** based; C `char` is
   1 byte because C is ASCII based. `'a'` is 97 in both.
10. `char` range **0 to 65,535** — the only unsigned primitive.
11. Defaults: integrals `0`; `float`/`double` `0.0`; `boolean` **`false`**;
    `char` `' '`. Fields and array elements only, never locals.
12. Wrappers: `Byte`, `Short`, **`Integer`**, `Long`, `Float`, `Double`,
    `Boolean`, **`Character`**.
13. **`null` is only for object references**, never for primitives.

---

## Exam and interview points

1. **`long l = 126000 * 60 * 60 * 24 * 1000;` compiles and prints
   `-1342095360`.** The expression is evaluated in `int` arithmetic and
   overflows before the widening assignment. One `L` suffix fixes it. No warning
   is issued, even at `-Xlint:all`.
2. **"Small float, big double" is the wrong criterion.** Accuracy is the
   criterion — and strictly, it is *significant digits* (≈7 for `float`, ≈15–17
   for `double`), not decimal places.
3. **`Float.MIN_VALUE` is the smallest positive float (`1.4E-45`), not the most
   negative.** The most negative is `-Float.MAX_VALUE`. `Integer.MIN_VALUE` does
   not behave this way — know which family you are being asked about.
4. **Size of `boolean` is "not applicable / JVM dependent."** Not 1 bit, not
   1 byte. Range is not applicable either, because `true` and `false` are at the
   same level.
5. **`boolean b = True;` is `cannot find symbol`, not `incompatible types`.**
   The compiler falls back to reading `True` as an undeclared variable. The
   other three quizzes give `incompatible types`. Four lines, three distinct
   errors — that is the whole point of the drill.
6. **`if (x)` with an `int` is a compile error, not "prints hi."** `while (1)`
   is a compile error, not an infinite loop. Both are valid C.
7. **`char` is 2 bytes because Java is Unicode based.** Be ready with 256 vs
   65,536 and 8 vs 16 bits — and add that a `char` is really a **UTF-16 code
   unit**, so supplementary characters (emoji, U+10000 and above) take two
   `char`s. Unicode has 1,114,112 code points, not 65,536.
8. **`'a'` is 97 in both ASCII and Unicode.** The overlap is the first **128**
   code points (ASCII); 128–255 is Latin-1, which Unicode also adopted.
9. **`char`'s default is `' '` (NUL), not a space.** Space is 32. This is
   the one place the lecture's board note is factually wrong.
10. **Java's `boolean` default is `false`.** Do not repeat the "C++ defaults to
    true" contrast — an uninitialised C++ `bool` is indeterminate, and a static
    one is `false`.
11. **The wrapper for `int` is `Integer`, for `char` is `Character`.** Those two
    are the planted traps; the other six are just capitalised.
12. **`char ch = null;` is a compile error** (`<null> cannot be converted to
    char`), not a `NullPointerException`. But `Integer n = null; int x = n;`
    *compiles* and throws NPE at runtime — that is the unboxing trap.
13. **`File.length()` returns bytes, and its return type is `long`, not `int`**
    — because file sizes exceed `int` range. Modern equivalent:
    `Files.size(Path)` (Java 7).
14. **Defaults apply to fields and array elements only.** A local variable read
    before assignment is a compile error: `variable x might not have been
    initialized`.
15. **Version markers worth knowing:** autoboxing and supplementary-character
    support (5), NIO.2 `Files.size` and literal underscores (7), `codePoints()`
    and `Math.*Exact` (8), compact strings and wrapper-constructor deprecation
    (9), `var` (10), helpful NPEs on by default (15), wrapper constructors
    deprecated for removal (16), `strictfp` a no-op (17).

---

**Next:** Video 004 — Literals Part 1
