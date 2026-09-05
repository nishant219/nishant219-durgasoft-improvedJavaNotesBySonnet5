# Video 001 — Identifiers and Reserved Words

## Video info

| Field | Detail |
|---|---|
| Playlist | Core Java with OCJP/SCJP — Durga Sir |
| Position | Video 1 of 203 |
| Series | Language Fundamentals · Part 1 of 16 |
| Topic | Identifiers and reserved words |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 16m 59s |
| Watch | https://www.youtube.com/watch?v=eTXd89t8ngI |
| Playlist | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Language Fundamentals is the first block of OCJP, roughly ten sessions:

1. Identifiers ← *this video*
2. Reserved words ← *this video*
3. Data types
4. Literals
5. Arrays
6. Types of variables
7. Var-arg methods
8. `main` method
9. Command-line arguments
10. Java coding standards

The material is basic, but Sir's point is that OCJP tests the edges of it — the
loopholes, not the headline rule.

---

## 03:38 — What an identifier is

> An identifier is a **name in a Java program used for identification purposes**.

Sir's analogy: in a class of 100 students you identify each person by name. A
program is the same — every thing you declare needs a name to refer to it.

An identifier can be a:

- class name
- interface name
- method name
- variable name
- label name

```java
class Test {
    public static void main(String[] args) {
        l1: {
            l2: {
                int x = 10;   // l1 and l2 are label names — also identifiers
            }
        }
    }
}
```

### 06:13 — Count the identifiers

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
    }
}
```

The classroom guesses three or four. The answer is **five**:

| # | Identifier | Why it counts |
|---|---|---|
| 1 | `Test` | class name |
| 2 | `main` | method name |
| 3 | `String` | a predefined class name — still a name |
| 4 | `args` | name of the array parameter |
| 5 | `x` | variable name |

`class`, `public`, `static`, `void` and `int` are **reserved words**, not
identifiers. That distinction is the whole point of the exercise.

---

## 10:01 — The six rules

Sir's framing: naming a child follows rules in every family; naming things in
Java follows rules too, and breaking them is a compile-time error.

### 11:46 — Rule 1: allowed characters

An identifier may contain **letters, digits, `$` and `_`**.

```java
int total_number = 10;   // valid
int total# = 10;         // CE: '#' is not allowed
int all@hands = 10;      // CE: '@' is not allowed
```

> ❗ **Correction — "only `a–z`, `A–Z`, `0–9`, `$`, `_`" is the ASCII subset, not the rule.**
> Java identifiers are defined over **Unicode**, not ASCII (JLS §3.8). The real
> test is `Character.isJavaIdentifierStart` for the first character and
> `Character.isJavaIdentifierPart` for the rest — which accepts letters from any
> script, currency symbols, and connecting punctuation:
>
> ```java
> int café    = 10;   // valid — é is a Unicode letter
> int π       = 3;    // valid — Greek letter
> int числа   = 5;    // valid — Cyrillic
> int €rate   = 7;    // valid — € is a currency symbol
> ```
>
> Sir's ASCII list is the practical rule for readable code and it is what the
> OCJP exam asks about. But "any character other than these five groups is a
> compile error" is false — memorise it as *the recommended set*, not the legal set.

### 14:58 — Rule 2: cannot start with a digit

```java
int total123 = 10;   // valid — digit not at the start
int 123total = 10;   // CE: identifier cannot begin with a digit
```

Same rule as C and C++.

### 16:26 — Rule 3: identifiers are case sensitive

```java
class Test {
    int number = 10;   // three genuinely different variables
    int Number = 20;
    int NUMBER = 30;
}
```

Java as a language is case sensitive, so identifiers inherit that.

### 19:19 — Rule 4: no length limit

The classroom guesses 32, 64, 128, 256. The answer is that the **language
specifies no limit**:

```java
class Test {
    public static void main(String[] args) {
        int xxxxxxyyyyyyjjjjjjxxxxxxxxxyyyyyyyjjjjjj = 10;
        System.out.println(xxxxxxyyyyyyjjjjjjxxxxxxxxxyyyyyyyjjjjjj);   // 10
    }
}
```

This compiles. Sir's verdict on whether you should: an expert seeing this would
give you "left and right" — all that length to declare one variable and print
it. Readability collapses.

> **Board:** There is no length limit for Java identifiers, but it is not
> recommended to use excessively long identifiers.

> ❗ **Correction — there is a hard ceiling in practice.**
> The *language* imposes no limit, but the *class file format* does: every name
> is stored as a `CONSTANT_Utf8` entry, capped at **65,535 bytes** (JVMS §4.4.7).
> Sir's "you can take a one-crore-length identifier" would fail at class-file
> generation, not at parsing. Unlimited in the JLS, 64 KB in reality.

### 23:28 — Rule 5: reserved words cannot be identifiers

```java
int x  = 10;   // valid
int if = 20;   // CE: 'if' is a reserved word
```

`if` already carries meaning; you cannot repurpose it.

### 25:11 — Rule 6: predefined class and interface names *are* allowed

The classroom is certain this is invalid. It is not:

```java
class Test {
    public static void main(String[] args) {
        int String = 38;
        System.out.println(String);     // 38

        int Runnable = 39;
        System.out.println(Runnable);   // 39
    }
}
```

Rule 5 said *reserved words* cannot be identifiers. `String` and `Runnable` are
class and interface names — they were never reserved words. This compiles and
prints 38 then 39.

Is it recommended? No. Readability drops and it actively confuses: your IDE
colours `String` as a type while you are using it as an `int`.

> **Board:** Even though it is valid, it is not good programming practice,
> because it reduces readability and creates confusion.

> ⚠️ **Modern Java — a few names have since become off-limits.**
> Rule 6 still holds for library classes, but Java has added *contextual*
> keywords that are restricted in specific positions:
>
> ```java
> int var = 10;        // still valid — var is fine as a variable name
> class var    { }     // CE: 'var' not allowed here
> class record { }     // CE: 'record' not allowed here
> class yield  { }     // CE: 'yield' not allowed here
> class sealed { }     // CE: 'sealed' not allowed here
> class permits{ }     // CE: 'permits' not allowed here
> ```
>
> So the modern rule is: predefined **library** names are fair game; a handful of
> **contextual keywords** are rejected, but only in the position where they would
> be ambiguous — which is why `var` may still name a variable but never a type.

### 31:13 — The six rules, recapped

1. The only allowed characters are letters, digits, `$` and `_`.
2. An identifier must not start with a digit.
3. Identifiers are case sensitive.
4. There is no length limit.
5. Reserved words cannot be used as identifiers.
6. All predefined Java class and interface names can be used as identifiers.

### 31:51 — Exam drill: which are valid?

| Identifier | Valid? | Reason |
|---|---|---|
| `total_number` | ✅ valid | allowed characters only |
| `total#` | ❌ CE | `#` not allowed |
| `123total` | ❌ CE | starts with a digit |
| `total123` | ✅ valid | digit is not first |
| `ca$h` | ✅ valid | `$` is allowed |
| `_$_` | ✅ valid | `$` and `_` only |
| `all@hands` | ❌ CE | `@` not allowed |
| `Java2Share` | ✅ valid | letters and digits |
| `Integer` | ✅ valid | predefined class name is fine |
| `Int` | ✅ valid | capital `I` — not a reserved word |
| `int` | ❌ CE | reserved word |

> ⚠️ **Modern Java — one entry on this list has changed.**
> A **bare `_`** was a legal identifier when this was recorded. It is not any more:
>
> | Version | `int _ = 10;` |
> |---|---|
> | Java 8 and earlier | valid (warning from Java 8) |
> | Java 9 – 21 | **compile error** — `_` became a keyword (JEP 213) |
> | Java 22+ | valid again, but as an **unnamed variable** (JEP 456) — you cannot read it back |
>
> `_$_` from the drill above is unaffected — the restriction is only on `_`
> standing completely alone.

---

## 35:48 — Reserved words

> In any language — spoken or programming — some words are reserved to represent
> a particular meaning or functionality.

English reserves *cat*, *dog*, *apple*, *eat*, *sleep* — you cannot redefine
them mid-sentence. English has an Oxford dictionary's worth. Java has 53.

### 39:11 — The breakdown

```text
reserved words (53)
├── keywords (50)
│   ├── used keywords (48)     if, else, switch, …
│   └── unused keywords (2)    goto, const
└── reserved literals (3)      true, false, null
```

The keyword / reserved-literal split turns on **functionality**:

- carries functionality → **keyword**
- carries only a value → **reserved literal**

`true` and `false` denote boolean values and do nothing else; `null` denotes the
default reference value. Hence three reserved literals.

> ⚠️ **Modern Java — the count is no longer 53.**
>
> | | Java 5–8 | Java 21 / 25 |
> |---|---|---|
> | Keywords | 50 | **51** (`_` added in Java 9) |
> | Reserved literals | 3 | 3 |
> | **Reserved words** | **53** | **54** |
> | Contextual keywords | — | **17** |
>
> The 17 **contextual keywords** (JLS §3.9) are reserved only in the positions
> where they are meaningful, and remain usable as ordinary identifiers elsewhere:
>
> `exports`, `module`, `non-sealed`, `open`, `opens`, `permits`, `provides`,
> `record`, `requires`, `sealed`, `to`, `transitive`, `uses`, `var`, `when`,
> `with`, `yield`
>
> This is why `var` can still name a variable but not a class. If an interviewer
> asks "how many keywords does Java have," the complete answer is **51 keywords
> + 3 reserved literals, plus 17 contextual keywords** — and saying so signals
> you have tracked the language past Java 8.

### 43:17 — Keywords for data types (8)

```text
byte   short   char   int   long   float   double   boolean
```

### 44:42 — Keywords for flow control (11)

```text
if   else   switch   case   default   while   do   for   break   continue   return
```

### 46:19 — Keywords for modifiers (11)

```text
public   private   protected   static   final   abstract
synchronized   native   strictfp   transient   volatile
```

Java has twelve modifiers, but *default* access is expressed by writing nothing
at all — there is no `default` access modifier keyword to write. So eleven
appear on this list.

> ❗ **Careful — `default` IS a keyword, just not here.**
> It appears in this lecture's flow-control group (`switch` … `default`), and
> since Java 8 it also marks default methods in interfaces
> (`default void m() { }`). What Sir means is narrower and correct: there is no
> `default` **access modifier** you can type.

> ⚠️ **Modern Java — `strictfp` is now a no-op.**
> Since **Java 17** (JEP 306) all floating-point arithmetic is strict by default,
> which is what `strictfp` used to opt into. The keyword still parses and still
> compiles, but now changes nothing — and `javac -Xlint:strictfp` says so:
>
> ```text
> warning: [strictfp] as of release 17, all floating-point expressions are
> evaluated strictly and 'strictfp' is not required
> ```
>
> Historically it was worth marks. Today, writing it is dead code.

### 48:24 — Keywords for exception handling (6)

```text
try   catch   finally   throw   throws   assert
```

`assert` arrived in **Java 1.4**, for debugging.

### 49:33 — Class-related keywords (6)

```text
class   interface   extends   implements   package   import
```

Note `import`, **not** `imports`. `enum` is counted separately below.

### 50:42 — Object-related keywords (4)

```text
new   instanceof   super   this
```

`instanceof` is all lowercase — not `instanceOf`.

There is **no `delete` keyword** in Java: destroying unreachable objects is the
garbage collector's job, not yours.

### 51:51 — The `void` return type keyword (1)

```java
class Test {
    public m1() { }        // CE: invalid method declaration — return type required
}

class Test {
    public void m1() { }   // valid — declares that m1 returns nothing
}
```

In C the return type is optional and defaults to `int`. In Java the return type
is **mandatory**; a method that returns nothing must say `void`.

### 54:31 — Unused keywords (2)

`goto` and `const` are reserved but have **no use in Java**.

- **`goto`** — its use caused enough damage in other languages that Java's
  designers reserved the word and then refused to implement it.
- **`const`** — its job is defining constants, which `final` already does.

They are reserved precisely so you cannot use them, and so a C programmer's
`goto` produces a clear error rather than a confusing one:

```java
class Test {
    int goto  = 10;   // CE: <identifier> expected — 'goto' is a reserved word
    int const = 20;   // CE: <identifier> expected — 'const' is a reserved word
}
```

> **Board:** `goto` and `const` are unused keywords, and if we try to use them we
> get a compile-time error.

Both remain reserved and unused in current Java — nothing here has changed.

### 58:25 — Reserved literals (3)

```java
class Test {
    boolean flag  = true;    // boolean value
    boolean flag2 = false;   // boolean value
    String  ref   = null;    // default value for any object reference
}
```

### 1:00:08 — The `enum` keyword (Java 1.5)

Use `enum` when you want to define a **group of named constants**:

```java
enum Month {
    JAN, FEB, MAR, APR, MAY, JUN,
    JUL, AUG, SEP, OCT, NOV, DEC
}

enum Beer {
    KF, KO, RC, FO   // Kingfisher, Knock Out, Royal Challenge, Foster's
}
```

Sir defers the full `enum` treatment to a later session.

### 1:02:29 — The count, added up

| Group | Count | Running total |
|---|---|---|
| Data types | 8 | 8 |
| Flow control | 11 | 19 |
| Modifiers | 11 | 30 |
| Exception handling | 6 | 36 |
| Class related | 6 | 42 |
| Object related | 4 | 46 |
| `void` | 1 | 47 |
| Unused (`goto`, `const`) | 2 | 49 |
| `enum` | 1 | 50 |
| Reserved literals | 3 | **53** |

---

## 1:02:50 — Conclusions

**1. Every reserved word is entirely lowercase.** No uppercase letters, no
special characters. The ones people get wrong:

| Correct | Common mistake | What is wrong |
|---|---|---|
| `instanceof` | `instanceOf` | the `o` is lowercase |
| `strictfp` | `strictFp` | the `f` is lowercase |
| `null` | `NULL`, `Nul` | Java has no uppercase `NULL`; that is C |
| `synchronized` | `synchronize` | needs the `d` |
| `extends` | `extend` | plural |
| `implements` | `implement` | plural |
| `import` | `imports` | singular |
| `const` | `constant` | the reserved word is `const` |

> ⚠️ **Modern Java — one exception to "all lowercase."**
> `non-sealed` (Java 17) contains a **hyphen** — the only reserved word in the
> language that is not a plain run of lowercase letters. It is a contextual
> keyword, so the conclusion holds for the 54 true reserved words.

**2. Java has `new` but no `delete`,** because destroying unreachable objects is
the garbage collector's responsibility.

**3. Keywords added after Java 1.0:**

| Keyword | Version |
|---|---|
| `strictfp` | 1.2 |
| `assert` | 1.4 |
| `enum` | 1.5 |
| `_` | 9 |

---

## 1:10:47 — Exam drill: which list contains *only* reserved words?

| List | Problem |
|---|---|
| `new`, `delete` | `delete` does not exist in Java |
| `goto`, `constant` | the keyword is `const`, not `constant` |
| `break`, `continue`, `return`, `exit` | `exit` is a method (`System.exit`) |
| `final`, `finally`, `finalize` | `finalize` is a method on `Object` |
| `throw`, `throws`, `thrown` | `thrown` is not a Java word at all |
| `notify`, `notifyAll` | both are methods on `Object` |
| `implements`, `extends`, `imports` | the keyword is `import` |
| `sizeof`, `instanceof` | `sizeof` does not exist in Java |
| `Byte`, `short`, `Int` | `Byte` is a class; `Int` is not a keyword (`int` is) |
| **none of the above** | ✅ **correct answer** |

Sir's practical trick: in any IDE, a reserved word renders in the keyword colour
(blue in most themes). No colour change means it is not reserved. `delete`,
`exit`, `finalize`, `thrown`, `notify`, `sizeof` all stay plain.

### 1:15:23 — The same test, on the program you already know

```java
class Test {
    public static void main(String[] args) {
    }
}
```

| Token | Reserved word? |
|---|---|
| `class` | ✅ yes |
| `public` | ✅ yes |
| `static` | ✅ yes |
| `void` | ✅ yes |
| `main` | ❌ no — just a method name |
| `String` | ❌ no — a predefined class (your IDE colours it as a type) |
| `args` | ❌ no — a variable name |

---

## Exam and interview points

1. **Five identifiers** in the minimal `main` program — `String` and `args` are
   the two people miss.
2. **Predefined class names are legal identifiers.** `int String = 38;` compiles.
   Valid, never recommended.
3. **`goto` and `const` are reserved but unused** — using either is a compile
   error, and that is the whole reason they are reserved.
4. **All reserved words are lowercase.** `instanceOf`, `strictFp`, `NULL` are the
   planted traps.
5. **`exit`, `finalize`, `notify`, `notifyAll`, `sizeof`, `delete`, `thrown`,
   `constant`, `imports` are not reserved words** — most are methods, the rest
   do not exist.
6. **The count**: 53 for the OCJP exam this course targets; **54 keywords +
   literals, plus 17 contextual keywords** for a current interview. Know both,
   and know which one you are being asked for.

---

**Next:** Video 002 — Data Types Part 1
