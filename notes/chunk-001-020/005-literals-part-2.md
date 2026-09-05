# Video 005 — Literals Part 2

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-5 || Literals part-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 5 of 203 |
| Series | Language Fundamentals · Part 5 of 16 |
| Topic | Literals part 2 — char literals (four ways), escape characters, String literals, Java 1.7 binary literals and underscores, implicit conversion diagram |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 05m 28s (3928 seconds) |
| Video ID | IJ0xCDR_Dlw |
| Watch | https://www.youtube.com/watch?v=IJ0xCDR_Dlw |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

This lecture **starts at `char` literals**. Integral, floating-point and boolean
literals were part 1 (video 004). Decimal / octal / hexadecimal integer forms are
not re-explained here — they come back only as ways of writing a Unicode value.

## What this lecture covers

1. **Four ways** to specify a `char` literal
2. Way 1: a single character in **single quotes** — plus every invalid variant (`A` unquoted, `"A"`, `'AB'`)
3. Way 2: an **integral literal** standing for the Unicode value (decimal / octal / hex), range **0 to 65,535**
4. The twist: why some code points print as **`?`**
5. Way 3: **Unicode representation** `'\uXXXX'` — four hex digits
6. Way 4: every **escape character** is a valid `char` literal; the list of eight; `\'` `\"` `\\`; illegal escapes
7. Exam drill: which `char` assignments are valid?
8. **`String` literals**: any sequence of characters in double quotes
9. Java **1.7** enhancement 1: **binary literals** (`0b` / `0B`)
10. Java **1.7** enhancement 2: **underscores** between digits of numeric literals
11. The **implicit conversion / widening diagram** Sir reuses for the rest of the course
12. Why an 8-byte `long` can be assigned to a 4-byte `float`
13. Why `char` and `short` are not assignment-compatible despite both being 2 bytes

---

## 00:06 — `char` literals: how many ways?

> For the `char` data type, in how many ways can we specify a literal value?

Several. Sir teaches **four**, and the OCJP questions live in the gaps between
them.

### 00:22 — Way 1: a single character within single quotes

> **Board:** We can specify a `char` literal as a **single character within single quotes**.

```java
char ch = 'A';
System.out.println(ch);   // A
```

#### 01:40 — Quiz 1: quotes missing

```java
char ch = A;   // CE: cannot find symbol — symbol: variable A
```

Without the quotes this is not a `char` literal, not a `String` literal, and not
a valid value for any type. The compiler has only one reading left: `A` must be a
**variable**, and there is no such variable.

```text
error: cannot find symbol
  symbol:   variable A
  location: class Test
```

Same compiler reasoning as `boolean b = True;` in video 003.

#### 02:36 — Quiz 2: double quotes instead of single quotes

```java
char ch = "A";   // CE: incompatible types
```

Double quotes mean **`String`**, and a `String` cannot be assigned to a `char`.

> ⚠️ **Modern Java — the wording of this error changed.**
> Sir reads out the Java 6 diagnostic:
>
> ```text
> incompatible types
> found   : java.lang.String
> required: char
> ```
>
> From **Java 7** onwards `javac` prints the compressed one-line form, and that
> is what you will see today:
>
> ```text
> error: incompatible types: String cannot be converted to char
> ```
>
> Same error, same cause. The old `found:` / `required:` layout still turns up in
> OCJP question banks written against Java 6, so recognise both.

#### 03:28 — Quiz 3: two characters in single quotes

```java
char ch = 'AB';   // CE — and not the error you expect
```

The class guesses "it's a String." No — a `String` needs **double** quotes.

**Think the way the compiler thinks** (Sir insists this is mandatory):

1. First `'` — a character literal starts here. Fine.
2. `A` — one character. Fine.
3. After one character the compiler now **expects the closing `'`**. It finds `B`
   instead → **`unclosed character literal`**.
4. The second `'` opens a *new* character literal with no partner → a second
   **`unclosed character literal`**.
5. What is left over is not a Java statement → **`not a statement`**.

So one short line produces **three** compile errors. Verified on JDK 26:

```text
error: unclosed character literal      (at the first ')
error: unclosed character literal      (at the second ')
error: not a statement
3 errors
```

That count is itself an exam answer: the trap is answering "one error, String
cannot be converted to char."

---

## 08:41 — Way 2: an integral literal that *is* the Unicode value

Every character has a Unicode value, so you can write the number instead of the
character.

> **Board:** We can specify a `char` literal as an **integral literal** which
> represents the **Unicode value** of the character. That integral literal can be
> specified in **decimal, octal or hexadecimal** form. Allowed range is
> **0 to 65,535**.

```java
char ch = 97;
System.out.println(ch);   // a
```

> ❗ **Correction — 97 is `'a'`, not `'A'`.**
> Sir says "`A`, what is the corresponding Unicode value? 97," and then reads the
> output as `A`. The program prints lowercase **`a`**. The real values are:
>
> | Character | Decimal | Hex |
> |---|---|---|
> | `'A'` | 65 | `0x41` |
> | `'Z'` | 90 | `0x5A` |
> | `'a'` | **97** | `0x61` |
> | `'z'` | 122 | `0x7A` |
> | `'0'` | 48 | `0x30` |
>
> The rest of the lecture is internally consistent — he later converts 97 to hex
> `0061` and calls `'\u0061'` an `A` as well. Everywhere he says "A" for 97, read
> **`a`**. Memorise the anchors: **65 = `A`, 97 = `a`, 48 = `'0'`**, and note that
> `'a' - 'A' == 32`.

#### 11:51 — Examples

| Code | Valid? | Why |
|---|---|---|
| `char ch = 97;` | ✅ valid | decimal — prints `a` |
| `char ch = 0xFACE;` | ✅ valid | hex; 64,206 — inside 0–65,535 |
| `char ch = 0777;` | ✅ valid | octal; 511 |
| `char ch = 65535;` | ✅ valid | the maximum `char` |
| `char ch = 65536;` | ❌ CE | one past the maximum |

The `0xFACE` case is the one Sir dictates as "0 x of f"; the value he reads out,
**64,206**, confirms it is `0xFACE`.

For `65536`:

```java
char ch = 65536;   // CE: incompatible types: possible lossy conversion from int to char
```

> ⚠️ **Modern Java — "possible loss of precision" is now "possible lossy conversion".**
> Java 6 said `possible loss of precision / found: int / required: char`. From
> **Java 7** the message is:
>
> ```text
> error: incompatible types: possible lossy conversion from int to char
> ```
>
> Worth knowing because the same phrase shows up for every failed narrowing later
> in the course (`char` → `short`, `long` → `int`, and so on).

Note the mechanism behind why 65,535 compiles at all: `65535` is an `int`
literal, and assigning an `int` to a `char` is a *narrowing* conversion. Java
permits it only because the value is a **compile-time constant that fits** in the
target range (JLS §5.2, implicit narrowing for constant expressions). Change it to
a variable and even a legal value is rejected:

```java
int i = 97;
char ok  = 97;   // valid — constant expression, fits
char bad = i;    // CE: possible lossy conversion from int to char
```

> ❗ **Correction — `char` holds a *code unit*, not "any character".**
> "Every character has a Unicode value, and `char` covers 0 to 65,535" was already
> only half true when this was recorded. Since **Java 5**, `char` is a **UTF-16
> code unit**, and Unicode code points run to **U+10FFFF** (1,114,111). Anything
> above U+FFFF — emoji, many CJK extensions, most historic scripts — does not fit
> in one `char` and is stored as a **surrogate pair** of two `char`s:
>
> ```java
> String smile = "😀";
> System.out.println(smile.codePointAt(0));   // 128512  — the real code point
> System.out.println(smile.length());         // 2       — two chars, not one
> System.out.println(smile.charAt(0));        // half a character (a lone surrogate)
> ```
>
> The exam answer stays **0 to 65,535** for the `char` *type*. But "one `char` =
> one character" is false, and the API that gets it right is the `int` code-point
> family: `String.codePointAt`, `codePoints()`, `Character.toChars(int)`,
> `Character.charCount(int)`.

### 14:19 — The twist: why some code points print as `?`

```java
char a = 97;    System.out.println(a);   // a
char b = 197;   System.out.println(b);   // a special character
char c = 1970;  System.out.println(c);   // ?
char d = 1971;  System.out.println(d);   // ?
char e = 19710; System.out.println(e);   // ?
```

"Our favourite symbol will come," says Sir — the question mark. He puts two
explanations to the class:

1. **Option 1** — there is no character defined for 1970, 1971, …
2. **Option 2** — the character exists, but this system lacks the **font**, so it
   cannot be drawn.

Sir picks **option 2**, with the analogy that you can only type Telugu or Hindi on
a machine once the font is installed, and points at
**https://www.unicode.org** to look the code point up.

> ❗ **Correction — the `?` comes from the output *charset*, not the font, and for
> 1970 option 1 was the right answer anyway.**
>
> Two separate things get conflated here. Take them apart:
>
> **(a) What actually produces the `?`.** `System.out` is a `PrintStream` wrapping
> a **charset encoder**. When a `char` has no representation in that charset, the
> encoder substitutes `?` — before any font is consulted. Proof, same JVM, same
> terminal, same font, only the charset changed:
>
> ```java
> char c = 1970;
> System.out.println(System.getProperty("stdout.encoding"));
> System.out.println(c);
> ```
>
> ```text
> $ java Q                              $ java -Dstdout.encoding=US-ASCII Q
> UTF-8                                 US-ASCII
> ޲                                      ?
> ```
>
> A missing *font* gives you a blank box or `▯` (the "tofu" glyph) — rendered by
> the terminal. A missing *charset mapping* gives you `?` — produced inside Java.
> Sir's machine was a Windows console on a legacy code page, so almost everything
> outside Latin-1 became `?`.
>
> **(b) The specific code points he chose.** Checked against JDK 26:
>
> | Code point | Hex | Defined in Unicode? | What it really is |
> |---|---|---|---|
> | 97 | U+0061 | yes | LATIN SMALL LETTER A |
> | 197 | U+00C5 | yes | LATIN CAPITAL LETTER A WITH RING ABOVE — **Å** |
> | 1970 | U+07B2 | **no** | unassigned, Thaana block |
> | 1971 | U+07B3 | **no** | unassigned, Thaana block |
> | 19710 | U+4CFE | yes | CJK UNIFIED IDEOGRAPH-4CFE |
>
> So for **1970 and 1971 option 1 was correct** — those code points have no
> character, and `Character.isDefined(1970)` returns `false` to this day. For
> **19710** the character exists and option 2's *mechanism* (the output cannot
> represent it) applies. Sir declared option 2 the universal answer; the honest
> answer is "it depends which code point, and the `?` itself is an encoder
> substitution either way."
>
> **(c) Why 197 looked like a plus sign.** Sir reads it as "plus symbol". In Java
> `char 197` is **Å**. On the old Windows console code page 437, byte 197 is the
> box-drawing character **┼**, which does look like a plus — the console was
> showing its own code page's glyph, not Unicode's. It is the same charset
> mismatch, caught in the act.

> ⚠️ **Modern Java — the default charset is UTF-8 now, so this demo mostly stopped happening.**
>
> | Release | Behaviour |
> |---|---|
> | Java 6–17 | default charset came from the OS locale — `windows-1252`, `cp437`, `MS932`, … Non-Latin output degraded to `?` |
> | **Java 18** | **JEP 400** — `file.encoding` defaults to **UTF-8** on every platform |
> | **Java 19** | `stdout.encoding` / `stderr.encoding` added, so console encoding is separately controllable |
>
> On a current JDK with a UTF-8 terminal, `char c = 19710;` prints the actual CJK
> ideograph. Reproduce Sir's `?` on purpose with
> `java -Dstdout.encoding=US-ASCII`. And the Unicode standard has kept growing —
> Java 6 shipped Unicode 4.0, current JDKs ship Unicode 16 — so code points that
> were genuinely unassigned in 2013 may be real characters today. 1970 is not one
> of them; it is still unassigned.

---

## 17:34 — Way 3: Unicode representation `'\uXXXX'`

**Form:** single quote, backslash, `u`, **exactly four hexadecimal digits**,
single quote.

Sir works the conversion live for `'a'` = 97:

- 16 × 6 = 96, remainder **1** → hex **61**
- four digits are required → pad to **`0061`**

```java
char ch = '\u0061';
System.out.println(ch);   // a

char ch2 = '\u0062';
System.out.println(ch2);  // b   — 0x62 = 98
```

> **Board:** We can represent a `char` literal in **Unicode representation**,
> which is nothing but `'\uXXXX'`, where XXXX is a **four-digit hexadecimal number**.

> ❗ **Correction — `\uXXXX` is not part of the character literal. It is preprocessed before the compiler ever sees a literal.**
> This is the single most misunderstood thing about `\u` in Java, and it changes
> the answer to one of the drill questions below.
>
> `javac` runs Unicode escape translation as **step 1 of lexical translation**
> (JLS §3.3), before tokenising. Every `\uXXXX` anywhere in the source file — in
> code, in a `String`, **in a comment** — is replaced by the character it names,
> and only then is the result parsed as Java. Three consequences you can test:
>
> ```java
> // NOTE: this block is a demonstration, not a compilable file — lines 2 and 3
> // are precisely the cases that break compilation.
> // 1. Multiple u's are legal: \uuu0061 is still 'a'
> char ch = '\uuu0061';
> System.out.println(ch);            // a
>
> // 2. '\u000A' is a compile error — the escape becomes a REAL newline,
> //    so the character literal is left hanging open:
> //    char nl = '\u000A';          // CE: illegal line end in character literal
> //    You must write '\n' instead.
>
> // 3. A \u000A inside a // comment ends the comment and breaks the file:
> //    this comment ends with \u000A and the rest becomes code
> ```
>
> So `\u` is a **source-file encoding mechanism**, not an escape sequence like
> `\n`. `\n` is understood by the *character-literal* grammar; `\u0061` is gone
> before that grammar runs. Sir teaching it as "the third way to write a `char`
> literal" is fine as a memory aid, but it is why the next section's `\uface`
> question has a surprising error message.

---

## 22:02 — Way 4: every escape character is a valid `char` literal

```java
char nl  = '\n';   // valid — new line
char tab = '\t';   // valid — horizontal tab
char bad = '\m';   // CE: illegal escape character
```

"`m` means mute character?" — no. To answer this class of question you must know
the list by heart.

> **Board:** Every escape character is a valid `char` literal.

### 24:43 — How many escape characters? Eight

| Escape | Meaning |
|---|---|
| `\n` | new line |
| `\t` | horizontal tab |
| `\r` | carriage return — move to the first cell of the next line, like hitting return while typing |
| `\b` | **backspace**, not blank space — the keyboard key that moves one cell back and deletes the character there |
| `\f` | form feed ("check your C books; as a programmer you are not required to worry") |
| `\'` | single quote as a symbol |
| `\"` | double quote as a symbol |
| `\\` | backslash as a symbol |

Sir's mnemonic for the first five is **n t r b f** — hung on the Telugu film
*Badshah* starring N. T. Rama Rao Jr., which he grades "average". Then three
more: quote, double quote, backslash. **5 + 3 = 8.**

> ❗ **Correction — eight is the count of *named* escapes; Java also has octal escapes.**
> JLS §3.10.6 defines an `EscapeSequence` as the named list **plus an
> `OctalEscape`**: a backslash followed by one to three octal digits, covering
> `\0` through `\377` (0–255). This has been in the language since Java 1.0 and
> still works:
>
> ```java
> char c = '\101';   System.out.println(c);        // A   — octal 101 = 65
> char z = '\0';     System.out.println((int) z);  // 0   — the NUL character
> char m = '\377';   System.out.println((int) m);  // 255 — the maximum octal escape
> // char x = '\400';                              // CE — 400 octal = 256, out of range
> ```
>
> `'\0'` in particular shows up constantly in real code and in C-derived exam
> questions. Answer "eight" if the question says "escape characters" and lists the
> table; know that the complete grammar has nine categories once `OctalEscape` is
> counted.

> ⚠️ **Modern Java — a ninth named escape, `\s`, arrived in Java 15.**
> **JEP 378** (text blocks) added `\s`, which is a plain **space** (U+0020), and
> the line-continuation escape `\` at end of line.
>
> ```java
> char sp = '\s';                     // valid from Java 15 — a space
> System.out.println("a\sb");         // a b
> ```
>
> Compiling the same line with `--release 11` fails: *"text blocks are not
> supported in -source 11"*. `\s` exists because trailing spaces are stripped
> from text-block lines, and `\s` is how you protect one. The current named list
> is therefore **`\b \t \n \f \r \s \" \' \\`** — nine.

#### 27:18 — Why `\'`, `\"` and `\\` exist

**A single quote you want to print:**

```java
// System.out.println(''');       // CE: unclosed character literal
System.out.println('\'');          // ' — tell the compiler: treat ' as a symbol
System.out.println("this is \' symbol");
```

**A double quote inside a String:**

```java
// System.out.println("this is " symbol");   // CE: unclosed string literal
System.out.println("this is \" symbol");     // this is " symbol
```

**A backslash as a symbol.** Wherever the compiler sees `\`, its habit is
"escape sequence follows." `\c` is not an escape → `illegal escape character`.

```java
System.out.println("this is \\ character");   // this is \ character
```

**The file-path example** (a preview of the File I/O topic):

```java
// File f = new File("C:\Durga classes");    // CE: illegal escape character — \D
File f = new File("C:\\Durga classes");      // one real backslash in the path
```

`\\` in source becomes one `\` at runtime.

---

## 32:08 — The four ways, and the valid/invalid drill

1. A single character within single quotes
2. An integral literal = the Unicode value (decimal / octal / hex, 0–65,535)
3. Unicode representation `'\uXXXX'`
4. An escape character

### 32:37 — Which of the following are valid?

| Code | Sir's verdict | Verified on JDK 26 |
|---|---|---|
| `char ch = 65536;` | ❌ invalid | ❌ `incompatible types: possible lossy conversion from int to char` |
| `char ch = 0xBeer;` | ❌ invalid — `R` is not a hex digit | ❌ but the error is `';' expected` — see below |
| `char ch = \uface;` | ❌ invalid — single quotes missing | ❌ but the error is `cannot find symbol` — see below |
| `char ch = '\ubeef';` | ✅ valid | ✅ `0xBEEF` = 48,879, a Hangul syllable |
| `char ch = '\m';` | ❌ invalid | ❌ `illegal escape character` |
| `char ch = '\iface';` | ❌ invalid — `\i` is not an escape | ❌ `illegal escape character` |

Two of those need the real story, because the *reason* is an exam answer in
itself:

> ❗ **Correction — `0xBeer` fails as a syntax error, not a "bad hex digit" error.**
> The lexer is greedy: it reads `0xBee` as a perfectly good hex literal (3,054),
> then hits `r`, which starts a new identifier token. The result is two tokens
> where one was expected:
>
> ```text
> error: ';' expected
> class Bad { char ch = 0xBeer; }
>                            ^
> ```
>
> Sir's point stands — `0xBEEF` is a legal literal and `0xBeer` is not, because
> hex digits are `0–9` and `A–F` in either case. But do not expect the compiler to
> say "invalid hexadecimal digit"; it never gets that far.

> ❗ **Correction — `char ch = \uface;` fails because U+FACE is substituted into the source, not because quotes are missing.**
> Remember §3.3 from the Way 3 correction: `\uface` is translated **before**
> parsing. What the compiler actually parses is:
>
> ```java
> char ch = 龜;   // U+FACE, CJK COMPATIBILITY IDEOGRAPH-FACE
> ```
>
> and since that ideograph is a legal Java identifier character, the compiler
> reads it as a **variable name**:
>
> ```text
> error: cannot find symbol
>   symbol:   variable 龜
>   location: class Test
> ```
>
> Exactly the `char ch = A;` error from Quiz 1, in a different alphabet. Sir's
> verdict (invalid) is right and his fix (add the quotes) is right; the diagnostic
> is not the one he predicts.

Loopholes worth memorising from this drill: the **range**, the **hex alphabet**,
the **quotes** around a `\u` form, and **which escapes are legal**.

---

## 35:42 — `String` literals

`String` is not a primitive type, but it has a literal form, and Sir dispatches
it in one line.

> **Board:** Any sequence of characters within **double quotes** is treated as a
> **string literal**.

```java
String s = "Durga";
```

That closes the literals topic as a set: integral, floating-point, boolean,
`char`, and `String`.

> ⚠️ **Modern Java — text blocks are a second String literal form (Java 15).**
> **JEP 378** added the triple-quoted **text block**, so "any sequence of
> characters within double quotes" is no longer the whole rule:
>
> ```java
> String json = """
>     {
>       "name": "Durga",
>       "topic": "literals"
>     }""";
> ```
>
> Inside a text block you write `"` with no escaping at all, incidental leading
> whitespace is stripped based on the closing delimiter's indentation, and the
> trailing `\` joins lines. Available from **Java 15** (previewed in 13 and 14).

> ⚠️ **Modern Java — what a `String` is made of, and what it can do, both changed.**
>
> | Change | Release | What it means |
> |---|---|---|
> | **Compact strings** (JEP 254) | **Java 9** | A `String` is backed by `byte[]` plus a coder flag, not `char[]`. Pure Latin-1 strings take **half** the memory. Invisible to your code, large in a heap dump. |
> | `isBlank()`, `strip()`, `stripLeading/Trailing()`, `lines()`, `repeat(n)` | **Java 11** | `strip()` is Unicode-aware where `trim()` only cuts characters ≤ U+0020 |
> | `formatted()`, `stripIndent()`, `translateEscapes()` | **Java 15** | text-block companions |
>
> ```java
> System.out.println("  hi  ".strip());   // "hi"
> System.out.println("x".repeat(3));      // xxx
> System.out.println("".isBlank());       // true
> ```
>
> String *literal interning* is unchanged: identical literals still share one
> object in the string pool, which is video 004's material and remains an exam
> favourite.

---

## 37:14 — Java 1.7 enhancements to literals

Two new things arrived in 1.7.

> ⚠️ **Modern Java — "1.7" is now just Java 7, and both features are baseline.**
> Java 7 shipped in **2011**; these two came from **Project Coin (JSR 334)**.
> Nothing about them has changed since, but the framing has: no current codebase
> treats binary literals or underscores as "new". Read every "from 1.7 onwards"
> below as "always available".

### 38:01 — Enhancement 1: binary literals

Until 1.6, an integral literal (`byte`, `short`, `int`, `long`) could be written
three ways: **decimal, octal, hexadecimal**. From 1.7 there is a fourth,
**binary**.

- Allowed digits: **0 and 1** only
- Prefix: **`0b`** or **`0B`** — zero followed by lower- or upper-case `b`
- Compare: `0x` / `0X` is hexadecimal, `0b` / `0B` is binary

```java
int x = 0b1111;
System.out.println(x);   // 15
```

Four 1-bits = decimal 15. Printing always shows the **decimal** value — the
binary form exists only in the source.

> **Board:** For integral data types, until 1.6 we can specify a literal value in
> decimal, octal or hexadecimal form. But from **1.7 version onwards** we can
> specify even in **binary form**. Allowed digits: 0 and 1. The literal should be
> prefixed with **`0b` or `0B`**.

Binary literals earn their keep for bitmasks and flags, where the decimal
equivalent tells you nothing:

```java
int READ    = 0b0000_0100;   // 4
int WRITE   = 0b0000_0010;   // 2
int EXECUTE = 0b0000_0001;   // 1
System.out.println(READ | WRITE);   // 6
```

### 42:57 — Enhancement 2: underscores in numeric literals

This one applies to **all numeric literals** — integral *and* floating-point.

The problem is a plain digit dump:

```text
101101101
```

Thousands? Lakhs? Crores? Nobody can read it at a glance. From 1.7, Sun allowed
`_` **between digits**:

```java
double d1 = 123456.789;      // original
double d2 = 1_23_456.789;    // Indian grouping: 1 lakh 23 thousand 456.789
double d3 = 123_456.789;     // US grouping:     123 thousand 456.789
```

> **Board:** From **1.7 version onwards** we can use the underscore symbol
> **between digits** of a numeric literal. **Main advantage: readability of the
> code will be improved.**

### 48:28 — Underscores live only in the `.java` file

The doubt from the class: one person writes one underscore, another writes two —
how does the JVM know these are the same number?

Readability is needed in the **`.java`** file, not the `.class` file; nobody
opens a `.class` to read code. At **compile time** the underscores are simply
**removed**. After compilation these are the same instruction:

```java
double d = 1_23_456.789;
double d = 123456.789;
```

The JVM never sees an underscore. Zero runtime cost.

> **Board:** At the time of compilation these underscore symbols will be removed
> automatically. Hence after compilation the above lines will become
> `double d = 123456.789;`.

### 51:00 — Two conclusions about underscores

#### Conclusion 1 — more than one underscore between digits is fine

```java
double d = 1__23_4_56.789;
System.out.println(d);   // 123456.789
```

Every `_` is deleted anyway, so use as many as you find comfortable — as long as
they sit **between digits**.

> **Board:** We can use **more than one** underscore symbol also **between the digits**.

#### Conclusion 2 — anywhere other than between digits is a compile error

```java
double a = _1_23_456.789;    // CE
double b = 1_23_456_.789;    // CE: illegal underscore
double c = 1_23_456._789;    // CE: illegal underscore
double d = 1_23_456.789_;    // CE: illegal underscore
```

The *purpose* of `_` is to separate place values between digits. At the start it
does nothing, beside the decimal point it does nothing, at the end it is waste —
you are misusing the syntax.

> **Board:** We can use the underscore symbol **only between the digits**. If we
> use it **anywhere else**, we will get a **compile-time error**.

> ❗ **Correction — the leading-underscore case fails for a different reason, and the full rule has more edges than "between digits".**
> `_1_23_456.789` does **not** report `illegal underscore`. `_1_23_456` is a
> perfectly legal *identifier*, so the compiler reads a variable name followed by
> `.789` and gives up with `';' expected`. The other three do say
> `illegal underscore`.
>
> The complete rule (JLS §3.10.1) is that an underscore must have a **digit on
> both sides**, which also rules out positions Sir does not mention. All verified
> on JDK 26:
>
> | Literal | Result | Why |
> |---|---|---|
> | `1_000_000` | ✅ valid | between digits |
> | `0xFF_FF` | ✅ valid | between digits — works in hex and binary too |
> | `0b1010_1010` | ✅ valid | the idiomatic use for bitmasks |
> | `9_999_999_999L` | ✅ valid | suffix is outside the digits |
> | `1_0e1_0` | ✅ valid | both exponent digits are separated legally |
> | `_123` | ❌ CE `';' expected` | parsed as an identifier |
> | `123_` | ❌ CE `illegal underscore` | nothing to the right |
> | `0x_FF` | ❌ CE `illegal underscore` | adjacent to the `0x` prefix |
> | `0b_11` | ❌ CE `illegal underscore` | adjacent to the `0b` prefix |
> | `10_L` | ❌ CE `illegal underscore` | adjacent to the `L` suffix |
> | `1_e5` | ❌ CE `illegal underscore` | adjacent to the `e` exponent marker |
> | `1_.0` / `1._0` | ❌ CE `illegal underscore` | adjacent to the decimal point |
>
> Sir's "only between digits" is the right slogan; these are the cases an exam
> writer picks from.

That closes the 1.7 literal enhancements: **binary literals** and **underscores**.

---

## 56:56 — The implicit assignment (widening) diagram

Take this one seriously. Sir says he will come back to it "minimum twenty times"
in later classes — assignment, type casting, operators, overloading.

Assigning a **lower type value to a higher type variable** is always allowed:

```text
byte  →  short  →  int  →  long  →  float  →  double
                    ↑
                   char
```

The valid steps he reads out:

| Assignment | Sizes | OK? |
|---|---|---|
| `byte` → `short` | 1 → 2 | ✅ |
| `short` → `int` | 2 → 4 | ✅ |
| `char` → `int` | 2 → 4 | ✅ |
| `int` → `long` | 4 → 8 | ✅ |
| `long` → `float` | 8 → 4 | ✅ |
| `float` → `double` | 4 → 8 | ✅ |

Left to right is always acceptable. Read against the arrows and you need an
explicit cast.

Two things the arrows say that people miss, both compiler-verified:

```java
byte b = 10;
char c = b;      // CE: possible lossy conversion from byte to char
                 // there is NO byte → char arrow: byte is signed, char is not

final short s = 10;
char c2 = s;     // valid! constant expression in range — the §5.2 exception again
```

### 58:51 — The doubt: how does an 8-byte `long` fit in a 4-byte `float`?

The chain looks orderly until the fifth step:

- 1 byte → 2 bytes: fine
- 2 → 4: fine
- 4 → 8 (`int` → `long`): fine
- 4 → 8 (`float` → `double`): fine
- **8 → 4 (`long` → `float`): allowed?**

It is:

```java
float f = 10L;
System.out.println(f);   // 10.0
```

The left-hand types are **integral**; `float` and `double` are **floating-point**,
and their memory representation is completely different.

**Sir's classroom analogy:** Room 1 has 100 chairs, one person per chair — 100
students. Room 2 has only 50 chairs, but they are big enough for two people each
— still 100 people. Different number of chairs, same capacity, because the
internal arrangement differs.

> **Board:** An 8-byte `long` value can be assigned to a 4-byte `float` variable
> because **both follow different memory representations internally**.

> ❗ **Correction — `long` → `float` is a widening conversion that *can lose precision*. The chairs analogy says the capacity is equal; it is not.**
> "Different representation" is the right instinct, but the analogy implies both
> rooms hold the same 100 people. What actually happens is a trade: a `float`
> (IEEE 754 binary32) spends 8 bits on an exponent and only **24 bits on the
> significand**, so it covers a far wider **range** than a `long` while carrying
> far fewer **significant digits**.
>
> | Type | Bits | Range | Exactly representable integers |
> |---|---|---|---|
> | `long` | 64 | ±9.22 × 10¹⁸ | every integer in range |
> | `float` | 32 | ±3.40 × 10³⁸ | only up to **2²⁴ = 16,777,216** |
> | `double` | 64 | ±1.80 × 10³⁰⁸ | only up to **2⁵³ ≈ 9.0 × 10¹⁵** |
>
> Run it:
>
> ```java
> long   L = 123456789123456789L;
> float  f = L;                        // widening — no cast needed
> System.out.println(L);               // 123456789123456789
> System.out.println((long) f);        // 123456790519087104   <- 337 million off
>
> int i = 16777217;                    // 2^24 + 1
> float g = i;
> System.out.println((int) g);         // 16777216             <- the 1 is gone
> ```
>
> JLS §5.1.2 names exactly three widening primitive conversions that **may lose
> precision**: `int → float`, `long → float`, and `long → double`. Java still
> calls them widening — no cast, no warning — because the **magnitude** is
> preserved even when the digits are not. That distinction is the exam answer:
> **widening is about range, not about exactness.**

### 1:03:28 — Why `char` and `short` are not assignment-compatible

Both are 2 bytes. Neither can be assigned to the other:

```java
char  c = 'a';
short s = c;    // CE: possible lossy conversion from char to short

short t = 10;
char  d = t;    // CE: possible lossy conversion from short to char
```

The reason is the **sign bit**.

|  | `char` | `short` |
|---|---|---|
| Size | 2 bytes / 16 bits | 2 bytes / 16 bits |
| Signed? | **unsigned** — all 16 bits carry value | **signed** — 1 sign bit, 15 value bits |
| Range | 0 to 65,535 | −32,768 to 32,767 |

- A `char` of **65,535** is legal as a `char` but is far outside `short`'s range —
  16 value bits will not go into 15.
- A `short` of **−32,768** cannot become a `char`, because `char` has no way to
  represent a negative value.

Neither range contains the other, so neither direction is safe, and the compiler
refuses both. `char` is in fact Java's **only unsigned primitive type**.

Both still widen to `int` without complaint, which is why `char` → `int` is on
the diagram and why arithmetic on `char` silently produces an `int`:

```java
char x = 'a';
int  y = x + 1;                    // 98 — an int, not a char
System.out.println((char) y);      // b  — cast back to see the character
// char z = x + 1;                 // CE: possible lossy conversion from int to char
```

---

## Complete program from the lecture

```java
import java.io.File;

class Test {
    public static void main(String[] args) {
        // --- Way 1: single character in single quotes ---
        char ch1 = 'A';
        System.out.println(ch1);          // A
        // char bad1 = A;                 // CE: cannot find symbol — variable A
        // char bad2 = "A";               // CE: incompatible types: String cannot be converted to char
        // char bad3 = 'AB';              // CE: unclosed character literal x2, not a statement

        // --- Way 2: integral literal = Unicode value, 0..65535 ---
        char ch2 = 97;
        System.out.println(ch2);          // a   (NOT A — see the correction)
        char hex = 0xFACE;                // 64206 — valid
        char oct = 0777;                  // 511   — valid
        char max = 65535;                 // valid
        // char tooBig = 65536;           // CE: possible lossy conversion from int to char
        System.out.println((int) hex + " " + (int) oct + " " + (int) max);

        char undefined = 1970;            // U+07B2 — unassigned code point
        System.out.println(Character.isDefined(undefined));   // false

        // --- Way 3: Unicode representation ---
        char u1 = '\u0061';
        System.out.println(u1);           // a
        char u2 = '\u0062';
        System.out.println(u2);           // b
        char u3 = '\uuu0061';             // extra u's are legal (JLS 3.3)
        System.out.println(u3);           // a
        // A backslash-u escape for 000A cannot even be written here: the escape is
        // expanded before parsing, so it would end this comment line. See JLS 3.3.

        // --- Way 4: escape characters ---
        char nl  = '\n';
        char tab = '\t';
        char oct2 = '\101';               // octal escape — 'A'
        char sp   = '\s';                 // Java 15+ — a space
        System.out.println(oct2 + "" + tab + "[" + sp + "]");
        // char mute = '\m';              // CE: illegal escape character

        System.out.println('\'');                     // '
        System.out.println("this is \" symbol");      // this is " symbol
        System.out.println("this is \\ character");   // this is \ character
        File f = new File("C:\\Durga classes");
        System.out.println(f.getPath());              // C:\Durga classes

        // --- String literals ---
        String s = "Durga";
        System.out.println(s + " " + s.repeat(2) + " " + "  x  ".strip());

        // --- Java 7 literal enhancements ---
        int bin = 0b1111;
        System.out.println(bin);          // 15
        int mask = 0b0000_1111;
        System.out.println(mask);         // 15
        double d1 = 1_23_456.789;         // underscores stripped at compile time
        double d2 = 1__23_4_56.789;       // multiple underscores are fine
        System.out.println(d1 + " " + d2);// 123456.789 123456.789
        // double e1 = _123.45;           // CE: ';' expected — _123 is an identifier
        // double e2 = 123_.45;           // CE: illegal underscore
        // double e3 = 123._45;           // CE: illegal underscore
        // double e4 = 123.45_;           // CE: illegal underscore
        // int    e5 = 0x_FF;             // CE: illegal underscore — next to the prefix

        // --- Widening ---
        float wide = 10L;
        System.out.println(wide);         // 10.0
        long big = 123456789123456789L;
        System.out.println((long) (float) big);   // 123456790519087104 — lossy widening
        // short sh = ch1;                // CE: possible lossy conversion from char to short
        // char  cc = (short) 10;         // CE: possible lossy conversion from short to char
    }
}
```

---

## Exam and interview points

1. **Four ways to write a `char` literal**: `'X'`; an integral Unicode value in
   decimal / octal / hex within **0–65,535**; `'\uXXXX'`; an escape character.
2. **97 is `'a'`, 65 is `'A'`.** Sir says "A" for 97 throughout; the program prints
   `a`. Anchors worth memorising: 48 = `'0'`, 65 = `'A'`, 97 = `'a'`, and
   `'a' - 'A' == 32`.
3. **`char ch = 'AB';` produces three errors**, not one: `unclosed character
   literal` twice plus `not a statement`. Answering "String cannot be converted to
   char" is the trap.
4. **The modern narrowing error is `incompatible types: possible lossy conversion
   from int to char`.** Java 6 said `possible loss of precision / found: int /
   required: char`. Recognise both wordings.
5. **`char ch = 65535;` compiles only because the literal is a constant expression
   in range** (JLS §5.2). Put the same value in an `int` variable and it becomes a
   compile error.
6. **A `char` is a UTF-16 code unit, not a character.** Code points above U+FFFF
   take two `char`s; use the `int` code-point APIs for real text.
7. **`?` on the console is the charset encoder substituting**, not a missing font.
   A missing font gives you a blank box. Since **Java 18** (JEP 400) the default
   charset is UTF-8, so the classic `?` demo needs
   `-Dstdout.encoding=US-ASCII` to reproduce.
8. **1970 (U+07B2) and 1971 (U+07B3) are genuinely unassigned code points** — for
   those two examples Sir's rejected "option 1" was the correct answer.
9. **`\uXXXX` is preprocessed before lexing** (JLS §3.3). It works inside comments,
   accepts extra `u`s (`\uuu0061`), and `'\u000A'` is a compile error because it
   becomes a real newline. Write `'\n'`.
10. **Eight named escapes in Sir's table** — `\n \t \r \b \f \' \" \\` — but the
    grammar also has **octal escapes** (`'\0'`, `'\101'`, up to `'\377'`), and
    **`\s`** was added in **Java 15**, making nine named escapes today.
11. **`\b` is backspace, not blank space.** A perennial one-mark question.
12. **`\m`, `\i`, `\D` → `illegal escape character`**, not "incompatible types".
13. **`0b`/`0B` is binary, `0x`/`0X` is hex.** `0b1111` prints **15**, never `1111`.
    Both binary literals and underscores arrived in **Java 7 (Project Coin, JSR 334)**.
14. **Underscores must have a digit on both sides.** Legal in hex and binary
    (`0xFF_FF`, `0b1010_1010`); illegal next to a prefix (`0x_FF`), a suffix
    (`10_L`), an exponent marker (`1_e5`), or a decimal point. `_123` fails as
    `';' expected` because it parses as an identifier, not as `illegal underscore`.
15. **The compiler strips underscores; the JVM never sees them.** `1_23_456.789`
    and `123456.789` compile to the identical constant.
16. **Widening order:** `byte → short → int → long → float → double`, plus
    `char → int`. There is **no `byte → char`** and **no `char ↔ short`**.
17. **`long` → `float` is legal but lossy.** JLS §5.1.2 lists exactly three lossy
    widening conversions: `int → float`, `long → float`, `long → double`. Widening
    guarantees magnitude, not exactness — a `float` holds only 24 significand bits,
    so integers above 2²⁴ start rounding.
18. **`char` and `short` are both 2 bytes and still incompatible in both
    directions**, because `char` is unsigned (0–65,535) and `short` is signed
    (−32,768–32,767). Neither range contains the other. `char` is Java's only
    unsigned primitive.
19. **Text blocks (Java 15) are a second String literal form**, and since Java 9 a
    `String` is backed by `byte[]` (compact strings, JEP 254), not `char[]`.
20. **Copy the widening diagram into your own notes.** It is reused for assignment,
    casting, operators and overload resolution for the rest of this course.

---

**Next:** Video 006 — Arrays Part 1
