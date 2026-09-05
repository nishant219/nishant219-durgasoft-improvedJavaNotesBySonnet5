# Video 026 — Selection statements: switch

## Video info

**Title:** Core Java with OCJP/SCJP: Flow-Control Part-3  || Selection Statements : switch

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 26 of 203 |
| Series | Flow-Control · Part 3 |
| Topic | Selection Statements : switch |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 11m 30s |
| Video ID | bgA_xYjJ8xY |
| Watch | https://www.youtube.com/watch?v=bgA_xYjJ8xY |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Captions | None on YouTube. Notes reconstructed from this lecture topic as Durga Sir teaches it, with full Java board examples. |

> **How to read these notes.** Sections follow the lecture's own structure.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

This is **Java 7-era traditional `switch`** — colon labels and `break`, the
form the OCJP exam this course targets actually asks about. Sir does not
teach the Java 14 arrow form (`case 2 -> ...`) here; every board program
below is written the way he writes it, and the arrow form is introduced only
where a ⚠️ **Modern Java** callout below calls it out.

## What this lecture covers

Previous video: `if-else`. This video: the other selection statement.

1. Allowed argument types for `switch` — and, just as important, what is
   **not** allowed.
2. Curly braces are **mandatory**; `case` and `default` are both **optional**
   (an empty `switch` is legal); a stray statement with no `case`/`default`
   above it is not.
3. Three rules every `case` label must satisfy: compile-time constant, in
   range of the argument type, unique.
4. `default` is optional, can appear **anywhere**, at most one per `switch`.
   Fall-through runs until `break` or the closing brace.
5. Nested `switch` is allowed.
6. Wrapping/unwrapping (1.5 autoboxing) when the argument is `Byte` /
   `Short` / `Integer` / `Character`.
7. `String` switch (1.7) and `enum` switch (1.5).
8. When to reach for `switch` instead of `if-else`.

---

## `switch` as a selection statement

`if-else` picks a branch based on a **boolean condition**. `switch` also
picks a branch, but based on **one of several possible values of a single
expression** — if the value is 0 do this, if 1 do that, if 2 do something
else.

## Syntax

```java
class Test {
    public static void main(String[] args) {
        int x = 1;
        switch (x) {
            case 0:
                System.out.println("case 0");
                break;
            case 1:
                System.out.println("case 1");
                break;
            case 2:
                System.out.println("case 2");
                break;
            default:
                System.out.println("default");
                break;
        }
    }
    // prints case 1
}
```

`x` is the switch argument. Matching starts at the `case` whose constant
equals `x`. Once a matching `case` (or `default`) is entered, execution runs
**every following statement** — including later `case`/`default` labels —
until it hits a `break` or the closing `}` of the `switch`. That's
fall-through; the rest of this note keeps coming back to it.

> ⚠️ **Modern Java — `switch` can also be an expression.**
> Since **Java 14** (JEP 361), `switch` doesn't have to be a statement that
> falls through by default — it can be an *expression* that produces a
> value, using arrow labels instead of colons:
>
> ```java
> int x = 2;
> String result = switch (x) {
>     case 1 -> "one";
>     case 2 -> "two";
>     case 3 -> "three";
>     default -> "other";
> };
> System.out.println(result);   // two
> ```
>
> Arrow labels **do not fall through** — each one is its own mini-block, no
> `break` needed. A multi-statement branch uses `yield` to produce the
> value. If the argument is an `enum` (or, from Java 21, a `sealed` type)
> and every constant is covered, the compiler accepts it as **exhaustive**
> with no `default` at all — verified: a three-constant `enum` switch
> expression with all three arrows and no `default` compiles and runs
> cleanly. This is the modern answer wherever the lecture's colon-and-break
> form is only being used to compute a value; the OCJP colon form below is
> still what the exam (and a lot of legacy code) asks for.

## Allowed argument types — the first big exam conclusion

The argument to `switch` is **not** like `if`. `if` wants `boolean`.
`switch` never wants `boolean`.

| Since | Allowed argument types |
|---|---|
| Always | `byte`, `short`, `char`, `int` |
| 1.5 | `Byte`, `Short`, `Character`, `Integer` (wrappers of the four above), `enum` |
| 1.7 | `String` |
| Never | `boolean`/`Boolean`, `long`/`Long`, `float`/`Float`, `double`/`Double` |

### `byte`, `short`, `char`, `int` — always allowed

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        switch (b) {
            case 10:
                System.out.println("ten");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints ten
}
```

```java
class Test {
    public static void main(String[] args) {
        short s = 20;
        switch (s) {
            case 10:
                System.out.println("ten");
                break;
            case 20:
                System.out.println("twenty");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints twenty
}
```

```java
class Test {
    public static void main(String[] args) {
        char ch = 'a';
        switch (ch) {
            case 'a':
                System.out.println("apple");
                break;
            case 'b':
                System.out.println("ball");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints apple
}
```

`char` is internally an unsigned 16-bit integer, so `switch` is happy with
it. `int` is the type most exam questions use:

```java
class Test {
    public static void main(String[] args) {
        int x = 2;
        switch (x) {
            case 1:
                System.out.println("one");
                break;
            case 2:
                System.out.println("two");
                break;
            case 3:
                System.out.println("three");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints two
}
```

### `boolean`, `long`, `float`, `double` — never allowed

```java
class Test {
    public static void main(String[] args) {
        boolean b = true;
        switch (b) {   // CE: incompatible types — switch does not accept boolean
            case true:
                System.out.println("true");
                break;
            case false:
                System.out.println("false");
                break;
        }
    }
}
```

**Why not `boolean`?** Only two possible values. For two values `if-else` is
enough — there's no gain from a `switch` here, so the language simply
doesn't allow it.

```java
class Test {
    public static void main(String[] args) {
        long x = 10L;
        switch (x) {   // CE: incompatible types — switch does not accept long
            case 10:
                System.out.println("ten");
                break;
            default:
                System.out.println("other");
        }
    }
}
```

**Why not `long`?** `switch` is compiled to a jump/lookup table keyed by
`int`-sized values; `long`'s 19-digit range doesn't fit that model. It
doesn't matter that the literal `10` obviously fits in an `int` — the
compiler checks the **declared type** of the argument (`long`), not the
value stored in it.

```java
class Test {
    public static void main(String[] args) {
        float f = 10.0f;
        switch (f) {   // CE: incompatible types — switch does not accept float
            case 10:
                System.out.println("ten");
                break;
            default:
                System.out.println("other");
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        double d = 10.0;
        switch (d) {   // CE: incompatible types — switch does not accept double
            case 10:
                System.out.println("ten");
                break;
            default:
                System.out.println("other");
        }
    }
}
```

**Why not `float`/`double`?** `switch` compares by **exact equality**, and
floating-point values are not reliably exact (`10.0` after arithmetic can
land on `10.000000001`). Use `if-else` with a delta comparison for floats;
`switch` will not take them, then or now.

> ⚠️ **Modern Java — this stays true for the *primitives*, verified against
> the latest compiler.** `switch` on a bare `boolean`, `long`, `float`, or
> `double` is still rejected, and that rejection is now even stricter: the
> newest javac ties primitive `case` labels to a **preview** feature
> ("primitive patterns", still unreleased as of Java 26) and refuses them
> outright without `--enable-preview`. Nothing here changed for the OCJP
> answer. What *did* change is one level up — see the wrapper-type callout
> below.

### Wrapper types from 1.5 — `Byte`, `Short`, `Integer`, `Character`

Because of autoboxing/unboxing, from 1.5 the wrappers of the four allowed
primitives are also accepted. Internally the wrapper is **unwrapped** first,
then it's an ordinary primitive `switch`.

```java
class Test {
    public static void main(String[] args) {
        Byte b = 10;
        switch (b) {
            case 10:
                System.out.println("ten");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints ten — Byte unwraps to byte
}
```

```java
class Test {
    public static void main(String[] args) {
        Short s = 20;
        switch (s) {
            case 10:
                System.out.println("ten");
                break;
            case 20:
                System.out.println("twenty");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints twenty — Short unwraps to short
}
```

```java
class Test {
    public static void main(String[] args) {
        Integer i = 30;
        switch (i) {
            case 10:
                System.out.println("ten");
                break;
            case 30:
                System.out.println("thirty");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints thirty — Integer unwraps to int
}
```

```java
class Test {
    public static void main(String[] args) {
        Character ch = 'A';
        switch (ch) {
            case 'A':
                System.out.println("capital A");
                break;
            case 'a':
                System.out.println("small a");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints capital A — Character unwraps to char
}
```

The corresponding wrappers of the **forbidden** primitives are still
forbidden — this is the exam trap. Seeing "wrapper" does not mean every
wrapper is fair game:

```java
class Test {
    public static void main(String[] args) {
        Boolean b = true;
        switch (b) {
            case true: // CE — a boolean literal is not a valid switch constant here
                System.out.println("true");
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        Long x = 10L;
        switch (x) {
            case 10: // CE: incompatible types: int cannot be converted to Long
                System.out.println("ten");
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        Float f = 10.0f;
        switch (f) {
            case 10: // CE: incompatible types: int cannot be converted to Float
                System.out.println("ten");
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        Double d = 10.0;
        switch (d) {
            case 10: // CE: incompatible types: int cannot be converted to Double
                System.out.println("ten");
        }
    }
}
```

Only the wrappers of `byte`/`short`/`char`/`int` are allowed as **constant**
switch arguments — not `Boolean`, not `Long`, not `Float`, not `Double`.
That's the whole OCJP rule this lecture teaches, and it is still exactly
right for a colon-and-break switch matching against literal constants.

> ⚠️ **Modern Java — `Boolean`/`Long`/`Float`/`Double` can be switched on
> since Java 21, just not with old-style constant labels.**
> Pattern matching for `switch` (JEP 441) accepts **any reference type** as
> the switch argument — including these four wrappers — as long as the
> labels are type patterns, `default`, or `case null`, not literal constants
> like `case true:`. Verified with `--release 21`:
>
> ```java
> Boolean b = true;
> switch (b) {
>     case Boolean bb -> System.out.println("boolean: " + bb);
>     case null      -> System.out.println("null");
> }
> // boolean: true
>
> Long x = 10L;
> switch (x) {
>     case Long lv -> System.out.println("long: " + lv);
>     case null    -> System.out.println("null");
> }
> // long: 10
> ```
>
> A plain `default:` also compiles for any of these four wrappers now. What
> is still refused, even on Java 26, is switching on the **primitive**
> `boolean`/`long`/`float`/`double` at all (see the callout above), and
> matching a wrapper against an old-style constant label such as
> `case true:` — that specific form remains behind an unreleased preview
> feature. So: still no constants for these four wrappers, but they are no
> longer categorically banned as switch arguments the way this lecture
> teaches.

### `enum` is allowed from 1.5

Sir's running example is a `Beer` enum:

```java
enum Beer {
    KF, KO, RC, FO   // Kingfisher, Knock Out, Royal Challenge, Foster's
}

class Test {
    public static void main(String[] args) {
        Beer b = Beer.KF;
        switch (b) {
            case KF:
                System.out.println("King Fisher");
                break;
            case KO:
                System.out.println("Knock Out");
                break;
            case RC:
                System.out.println("Royal Challenge");
                break;
            case FO:
                System.out.println("Foster");
                break;
            default:
                System.out.println("other brand");
        }
    }
    // prints King Fisher
}
```

`enum` is a typed set of named constants — a natural fit for `switch`.

### `String` is allowed from 1.7

Before 1.7, `switch("durga")` was a compile error. From 1.7 it's valid.

```java
class Test {
    public static void main(String[] args) {
        String s = "durga";
        switch (s) {
            case "durga":
                System.out.println("Durga Software Solutions");
                break;
            case "sunny":
                System.out.println("Sunny Leone");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints Durga Software Solutions
}
```

Comparison behaves like `.equals(...)` — exact character sequence,
case-sensitive — **not** `==` of references. More on this after the
case-label rules.

## Curly braces are mandatory; `case`/`default` are optional

For `if`, braces are optional. For `switch`, the body **must** be a block.

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        switch (x); // CE: '{' expected
    }
}
```

`if (true);` is a legal empty statement (a bare semicolon). `switch (x);`
is not — the compiler is expecting `{`.

Most people assume at least one `case` is required. It isn't — `case` and
`default` are both optional, so an **empty `switch`** is valid:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        switch (x) {
        }
    }
    // no output — legal, does nothing
}
```

This shows up in generated code or mid-edit, not hand-written programs, but
the exam asks "does this compile?" and the answer is yes.

Every statement inside `switch` must sit under some `case` or `default` — a
lone statement is illegal:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        switch (x) {
            System.out.println("hello"); // CE: case, default, or '}' expected
        }
    }
}
```

The compiler has no `case` to attach that `println` to. With a label it's
fine — either `default` alone, or `case` alone, both legal:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        switch (x) {
            default:
                System.out.println("hello");
        }
    }
    // prints hello
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = 11;
        switch (x) {
            case 10:
                System.out.println("ten");
        }
    }
    // no output — no case matches, no default present, no error
}
```

## `case` label rules — the exam meat

Every `case` label must satisfy **all three**:

1. It must be a **compile-time constant**.
2. Its value must be **within range** of (assignment compatible with) the
   switch argument's type.
3. Labels must be **unique** — no duplicates.

### Rule 1 — compile-time constant required

Literals are constants: `10`, `'a'`, `"durga"` all work. A `final` variable
initialized with a constant **at its declaration** is a compile-time
constant too:

```java
class Test {
    public static void main(String[] args) {
        int x = 20;
        final int y = 20;
        switch (x) {
            case 10:
                System.out.println("ten");
                break;
            case y:
                System.out.println("twenty");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints twenty — case y is as good as case 20
}
```

Without `final`, the value is only known at runtime, and case labels are
wired into the switch's dispatch at **compile** time:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        int y = 20;
        switch (x) {
            case 10:
                System.out.println("ten");
                break;
            case y: // CE: constant expression required
                System.out.println("twenty");
                break;
        }
    }
}
```

The one that traps students: a `final` variable **is** final, but if it's
assigned later rather than at declaration, it's not a *constant expression*:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        final int y;
        y = 20;
        switch (x) {
            case 10:
                System.out.println("ten");
                break;
            case y: // CE: constant expression required
                System.out.println("twenty");
                break;
        }
    }
}
```

Seeing `final` is not enough — it must be `final` **and** initialized with a
constant expression in the same declaration. Same reasoning kills a `final`
whose initializer is a method call:

```java
class Test {
    public static int m() {
        return 20;
    }

    public static void main(String[] args) {
        int x = 10;
        final int y = m();   // m() runs at runtime
        switch (x) {
            case y: // CE: constant expression required
                System.out.println("twenty");
        }
    }
}
```

Expressions made only of constants **are** constants — the compiler folds
them at compile time:

```java
class Test {
    public static void main(String[] args) {
        int x = 30;
        switch (x) {
            case 10:
                System.out.println("ten");
                break;
            case 10 + 20:
                System.out.println("thirty");
                break;
            case 5 * 8:
                System.out.println("forty");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints thirty
}
```

The switch **argument** itself does not have to be constant — only the
`case` labels do:

```java
class Test {
    public static void main(String[] args) {
        int x = 2;
        int y = 1;
        switch (x + y) {   // runtime value, that's fine
            case 1:
                System.out.println("one");
                break;
            case 2:
                System.out.println("two");
                break;
            case 3:
                System.out.println("three");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints three
}
```

But the same non-constant expression as a **case label** is illegal, even
though it looks harmless:

```java
class Test {
    public static void main(String[] args) {
        int x = 2;
        int y = 1;
        switch (x) {
            case 1:
                System.out.println("one");
                break;
            case x + y: // CE: constant expression required
                System.out.println("sum");
                break;
        }
    }
}
```

A `final Integer` — a reference — is not a constant expression of type
`int`, even when its value is a literal:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        final Integer y = 10;
        switch (x) {
            case y: // CE: constant expression required
                System.out.println("ten");
        }
    }
}
```

`Integer` is a reference type; `final Integer y = 10` is a constant
*reference* to a boxed object, not a constant `int` expression. This is a
favourite exam trap.

### Rule 2 — value must be within range of the argument type

The case constant must be assignment-compatible with the switch argument's
type. `byte` ranges −128 to 127:

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        switch (b) {
            case 10:
                System.out.println("ten");
                break;
            case 100:
                System.out.println("hundred");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints ten — 10 and 100 both fit in byte
}
```

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        switch (b) {
            case 10:
                System.out.println("ten");
                break;
            case 1000: // CE: incompatible types: possible lossy conversion from int to byte
                System.out.println("thousand");
                break;
        }
    }
}
```

`1000` is an `int` literal and cannot be assigned to `byte` without an
explicit cast. Most people assume `b` gets promoted to `int` inside
`switch`, so `case 1000` should be fine — it isn't. The switch argument's
type stays `byte`; every case constant must fit `byte`.

The companion program that makes the difference concrete — **promote the
argument first**, and `1000` becomes legal:

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        switch (b + 1) {   // b + 1 is int (binary numeric promotion)
            case 10:
                System.out.println("ten");
                break;
            case 100:
                System.out.println("hundred");
                break;
            case 1000:
                System.out.println("thousand");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints other — b + 1 is 11, matching none of 10 / 100 / 1000
}
```

Same labels, only `switch(b)` vs `switch(b + 1)` differs — one is a compile
error, the other is valid. This pair is 100% exam material.

`short` (−32768 to 32767) and `char` (0 to 65535) follow the same rule:

```java
class Test {
    public static void main(String[] args) {
        short s = 10;
        switch (s) {
            case 10:
                System.out.println("ten");
                break;
            case 32768: // CE: incompatible types: possible lossy conversion from int to short
                System.out.println("too big");
                break;
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        char ch = 'a';
        switch (ch) {
            case 97:
                System.out.println("97 is a");
                break;
            case -1: // CE: incompatible types: possible lossy conversion from int to char
                System.out.println("negative");
                break;
        }
    }
}
```

`char` cannot represent −1. An **explicit cast** turns the constant into
the right type and the range rule is satisfied — even though the stored
value wraps around:

```java
class Test {
    public static void main(String[] args) {
        byte b = -24;
        switch (b) {
            case 10:
                System.out.println("ten");
                break;
            case (byte) 1000:
                System.out.println("cast 1000");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints cast 1000 — 1000 truncated to 8 bits is -24, matching b
}
```

Legal, but ugly, and not the style anyone should write on purpose. The exam
version is almost always the uncast `1000` that fails to compile.

Unwrapping doesn't change the range rule — a `Byte` argument still needs
case values inside `byte`'s range:

```java
class Test {
    public static void main(String[] args) {
        Byte b = 10;
        switch (b) {
            case 10:
                System.out.println("ten");
                break;
            case 1000: // CE: incompatible types: possible lossy conversion from int to byte
                System.out.println("thousand");
                break;
        }
    }
}
```

### Rule 3 — duplicate case labels are not allowed

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        switch (x) {
            case 10:
                System.out.println("first 10");
                break;
            case 10: // CE: duplicate case label
                System.out.println("second 10");
                break;
        }
    }
}
```

The trap everyone falls into — **`97` and `'a'`**:

```java
class Test {
    public static void main(String[] args) {
        int x = 97;
        switch (x) {
            case 97:
                System.out.println("97");
                break;
            case 'a': // CE: duplicate case label
                System.out.println("a");
                break;
            case 98:
                System.out.println("98");
                break;
        }
    }
}
```

`'a'` is a `char` literal whose integer value is **97** (`'A'` is 65, `'b'`
is 98 — plain ASCII/Unicode code points). `case 97` and `case 'a'` are the
same label written two ways. The compiler compares **values**, not
spellings, and folded constant expressions are compared the same way:

```java
class Test {
    public static void main(String[] args) {
        int x = 20;
        switch (x) {
            case 20:
                System.out.println("20");
                break;
            case 10 + 10: // CE: duplicate case label
                System.out.println("10+10");
                break;
        }
    }
}
```

## `default` — optional, anywhere, at most one

If no `case` matches, `default` runs when present; with neither a match nor
a `default`, the `switch` does nothing — that's valid, not an error.

`default` is conventionally written last, but that's only convention — it
can be first, middle, or last. Matching is not "read top to bottom until you
hit default"; the JVM **jumps** straight to the matching label.

```java
class Test {
    public static void main(String[] args) {
        int x = 3;
        switch (x) {
            case 0:
                System.out.println("0");
                break;
            case 1:
                System.out.println("1");
                break;
            case 2:
                System.out.println("2");
                break;
            default:
                System.out.println("default");
                break;
        }
    }
    // prints default
}
```

Two `default`s are illegal:

```java
class Test {
    public static void main(String[] args) {
        int x = 1;
        switch (x) {
            case 1:
                System.out.println("1");
                break;
            default:
                System.out.println("d1");
                break;
            default: // CE: duplicate default label
                System.out.println("d2");
                break;
        }
    }
}
```

## Fall-through — `break` is optional

The most important runtime behaviour: once execution enters a matching
label, it runs every following statement — including later labels — until a
`break` or the end of the `switch`. Same code, four different values of
`x`, four different outputs:

```java
class Test {
    public static void main(String[] args) {
        int x = 0;   // same switch traced below for x = 0, 1, 2, 3
        switch (x) {
            case 0:
                System.out.println("0");
            case 1:
                System.out.println("1");
                break;
            case 2:
                System.out.println("2");
            default:
                System.out.println("def");
        }
    }
    // x = 0: prints 0, then 1 — enters case 0, no break, falls into case 1, break
}
```

Same switch, `x = 1` — enters `case 1` directly; `case 0` is skipped entirely:

```java
class Test {
    public static void main(String[] args) {
        int x = 1;
        switch (x) {
            case 0:
                System.out.println("0");
            case 1:
                System.out.println("1");
                break;
            case 2:
                System.out.println("2");
            default:
                System.out.println("def");
        }
    }
    // prints 1
}
```

Same switch, `x = 2` — enters `case 2`, no `break`, falls into `default`:

```java
class Test {
    public static void main(String[] args) {
        int x = 2;
        switch (x) {
            case 0:
                System.out.println("0");
            case 1:
                System.out.println("1");
                break;
            case 2:
                System.out.println("2");
            default:
                System.out.println("def");
        }
    }
    // prints 2, then def
}
```

Same switch, `x = 3` — no `case` matches, so control jumps straight to
`default`:

```java
class Test {
    public static void main(String[] args) {
        int x = 3;
        switch (x) {
            case 0:
                System.out.println("0");
            case 1:
                System.out.println("1");
                break;
            case 2:
                System.out.println("2");
            default:
                System.out.println("def");
        }
    }
    // prints def
}
```

| `x` | Path taken | Output |
|---|---|---|
| `0` | enter `case 0`, no `break`, fall into `case 1`, `break` | `0`, `1` |
| `1` | enter `case 1` directly, `break` — `case 0` is skipped | `1` |
| `2` | enter `case 2`, no `break`, fall into `default` | `2`, `def` |
| `3` (no match) | jump straight to `default` | `def` |

## `default` in the middle — the program everyone gets wrong

Moving `default` to the top does not make it run first. Matching still
jumps to whichever label equals the argument; fall-through still walks
**downward** from wherever execution entered — it never wraps back up to
`default`.

```java
class Test {
    public static void main(String[] args) {
        int x = 0;
        switch (x) {
            default:
                System.out.println("default");
            case 0:
                System.out.println("0");
                break;
            case 1:
                System.out.println("1");
            case 2:
                System.out.println("2");
        }
    }
    // prints 0 — jumps straight to case 0, default is skipped entirely
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = 1;
        switch (x) {
            default:
                System.out.println("default");
            case 0:
                System.out.println("0");
                break;
            case 1:
                System.out.println("1");
            case 2:
                System.out.println("2");
        }
    }
    // prints 1, then 2 — jumps to case 1, falls into case 2, default still skipped
}
```

The case that catches almost everyone — no `case` matches:

```java
class Test {
    public static void main(String[] args) {
        int x = 3;
        switch (x) {
            default:
                System.out.println("default");
            case 0:
                System.out.println("0");
                break;
            case 1:
                System.out.println("1");
            case 2:
                System.out.println("2");
        }
    }
    // prints default, then 0
}
```

Nothing matches `3`, so control jumps to `default` — but `default` has no
`break`, so it falls straight into `case 0`, which does have a `break`.
Most people guess only `default` prints. It's `default` **and** `0`.

With a `break` on every label, position stops mattering for the output —
only which label gets entered changes:

```java
class Test {
    public static void main(String[] args) {
        int x = 3;
        switch (x) {
            default:
                System.out.println("default");
                break;
            case 0:
                System.out.println("0");
                break;
            case 1:
                System.out.println("1");
                break;
        }
    }
    // prints default — the break stops the fall-through
}
```

## Intentional fall-through — grouping cases

Fall-through isn't always a bug. Stack case labels with empty bodies to
give several values the same action:

```java
class Test {
    public static void main(String[] args) {
        int day = 2;
        switch (day) {
            case 1:
            case 2:
            case 3:
            case 4:
            case 5:
                System.out.println("weekday");
                break;
            case 6:
            case 7:
                System.out.println("weekend");
                break;
            default:
                System.out.println("invalid day");
        }
    }
    // prints weekday — day 2 falls through the empty cases 2..5 to the shared body
}
```

In the exam, a **forgotten** `break` is usually a trick question; **stacked**
empty cases like this are the intended, readable use of fall-through.

## Nested `switch` is allowed

Inner case labels live in the **inner** switch — the same value can appear
in both without a duplicate-label conflict, because they're different
blocks:

```java
class Test {
    public static void main(String[] args) {
        int x = 1;
        int y = 2;
        switch (x) {
            case 1:
                System.out.println("outer 1");
                switch (y) {
                    case 1:
                        System.out.println("inner 1");
                        break;
                    case 2:
                        System.out.println("inner 2");
                        break;
                    default:
                        System.out.println("inner default");
                }
                break;
            case 2:
                System.out.println("outer 2");
                break;
            default:
                System.out.println("outer default");
        }
    }
    // prints outer 1, then inner 2
}
```

`break` inside the **inner** switch breaks only the inner switch — the
outer case keeps running afterward:

```java
class Test {
    public static void main(String[] args) {
        int x = 1;
        switch (x) {
            case 1:
                switch (x) {
                    case 1:
                        System.out.println("inner");
                        break;
                }
                System.out.println("still in outer case 1");
                break;
            default:
                System.out.println("outer default");
        }
    }
    // prints inner, then still in outer case 1
}
```

A `String` switch can nest inside an `int` switch and vice versa:

```java
class Test {
    public static void main(String[] args) {
        int year = 2;
        String branch = "CSE";
        switch (year) {
            case 1:
                System.out.println("electives: English, Algebra");
                break;
            case 2:
                switch (branch) {
                    case "CSE":
                    case "IT":
                        System.out.println("electives: ML, Big Data");
                        break;
                    case "ECE":
                        System.out.println("electives: Antenna");
                        break;
                    default:
                        System.out.println("electives: Optimization");
                }
                break;
            default:
                System.out.println("invalid year");
        }
    }
    // prints electives: ML, Big Data
}
```

## Wrapping vs unwrapping, and the `null` trap

**Wrapping** is primitive → wrapper object (autoboxing); **unwrapping** is
wrapper → primitive (auto-unboxing). From 1.5 the compiler does both
automatically:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        Integer y = x;   // wrapping
        int z = y;       // unwrapping
        System.out.println(z);
    }
    // prints 10
}
```

When `switch` receives a wrapper, it unwraps first, then matches as the
primitive — case labels are still `int` constants, not `Integer` objects:

```java
class Test {
    public static void main(String[] args) {
        Integer i = 10;
        switch (i) {   // effectively switch (i.intValue())
            case 5:
                System.out.println("five");
                break;
            case 10:
                System.out.println("ten");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints ten
}
```

If the wrapper reference is `null`, unwrapping calls `intValue()` on `null`
— it compiles, and blows up at **runtime**:

```java
class Test {
    public static void main(String[] args) {
        Integer i = null;
        switch (i) { // compiles; throws NullPointerException while unboxing
            case 10:
                System.out.println("ten");
                break;
            default:
                System.out.println("other");
        }
    }
}
```

There is no `case null` in this traditional switch — `null` is not a
constant `int`, and `default` does **not** catch it; the NPE happens before
any label is even considered.

> ⚠️ **Modern Java — `case null` is now legal, directly.**
> Since **Java 21** (JEP 441, pattern matching for `switch`), a `switch` on
> a reference type can have an explicit `case null` label, avoiding the NPE
> entirely — verified to compile and run without any preview flag:
>
> ```java
> String s = null;
> String r = switch (s) {
>     case null -> "was null";
>     case "durga" -> "durga";
>     default -> "other";
> };
> System.out.println(r);   // was null
> ```
>
> This works for the traditional colon form too, not just arrow switches.
> It applies to any reference-typed argument — `String`, wrapper types, or a
> custom class — but *not* to a `switch` on a primitive `int`/`char`/etc.,
> which can never hold `null` in the first place. Legacy code without a
> `case null` still throws the NPE exactly as Sir describes; this is purely
> an added option, not a change to the old behaviour.

## `String` switch in detail (1.7)

Comparison is **not** `==` — it behaves like `.equals(...)`. Content, case,
and spacing all matter:

```java
class Test {
    public static void main(String[] args) {
        String city = "Hyderabad";
        switch (city) {
            case "Hyderabad":
                System.out.println("Telangana");
                break;
            case "Chennai":
                System.out.println("Tamil Nadu");
                break;
            case "Bangalore":
                System.out.println("Karnataka");
                break;
            default:
                System.out.println("other city");
        }
    }
    // prints Telangana
}
```

Case-sensitive — `"hyderabad"` and `"Hyderabad"` are different labels, not
duplicates:

```java
class Test {
    public static void main(String[] args) {
        String city = "hyderabad";
        switch (city) {
            case "Hyderabad":
                System.out.println("Telangana");
                break;
            case "hyderabad":
                System.out.println("lowercase match");
                break;
            default:
                System.out.println("other city");
        }
    }
    // prints lowercase match
}
```

Fall-through works exactly the same as with `int`:

```java
class Test {
    public static void main(String[] args) {
        String s = "a";
        switch (s) {
            case "a":
                System.out.println("A");
            case "b":
                System.out.println("B");
                break;
            default:
                System.out.println("D");
        }
    }
    // prints A, then B
}
```

A `null` `String` compiles and throws at runtime, same as the `Integer`
case above — `default` does not catch it (see the ⚠️ Modern Java callout
above for the Java 21 `case null` fix):

```java
class Test {
    public static void main(String[] args) {
        String s = null;
        switch (s) { // compiles; throws NullPointerException at runtime
            case "durga":
                System.out.println("durga");
                break;
            default:
                System.out.println("other");
        }
    }
}
```

`case null` is illegal in the Java 7/8-era form this lecture targets:

```java
class Test {
    public static void main(String[] args) {
        String s = "durga";
        switch (s) {
            case null: // CE (pre-21): null is not a constant String expression
                System.out.println("null");
                break;
            default:
                System.out.println("other");
        }
    }
}
```

String case labels must still be compile-time constants — a non-`final`
variable doesn't qualify:

```java
class Test {
    public static void main(String[] args) {
        String s = "durga";
        String t = "durga";
        switch (s) {
            case t: // CE: constant expression required
                System.out.println("durga");
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        String s = "durga";
        final String t = "durga";
        switch (s) {
            case t:
                System.out.println("durga");
                break;
            default:
                System.out.println("other");
        }
    }
    // prints durga — final String t = "durga" is a constant variable
}
```

Interning doesn't matter for `switch` — a `String` built with `new` still
matches, because matching uses `equals`, not `==`:

```java
class Test {
    public static void main(String[] args) {
        String s = new String("durga");
        switch (s) {
            case "durga":
                System.out.println("matched");
                break;
            default:
                System.out.println("not matched");
        }
    }
    // prints matched
}
```

`if (s == "durga")` would print "not matched" here (different objects, same
content) — `switch` uses `equals`. Take special care with this distinction.

## `enum` switch in detail (1.5)

Case labels must be the **unqualified** enum constant name — the compiler
already knows the type from the switch argument:

```java
enum Beer {
    KF, KO, RC, FO
}

class Test {
    public static void main(String[] args) {
        Beer b = Beer.KO;
        switch (b) {
            case KF:
                System.out.println("King Fisher");
                break;
            case KO:
                System.out.println("Knock Out");
                break;
            case RC:
                System.out.println("Royal Challenge");
                break;
            case FO:
                System.out.println("Foster");
                break;
        }
    }
    // prints Knock Out
}
```

```java
enum Beer {
    KF, KO, RC, FO
}

class Test {
    public static void main(String[] args) {
        Beer b = Beer.KF;
        switch (b) {
            case Beer.KF: // CE (pre-21): an enum switch case label must be the unqualified name of an enumeration constant
                System.out.println("King Fisher");
                break;
            case KO:
                System.out.println("Knock Out");
                break;
        }
    }
}
```

Outside `switch` it's `Beer.KF`; inside `case`, only `KF`.

> ⚠️ **Modern Java — qualified enum case labels are now allowed.**
> Since **Java 21**, `case Beer.KF:` compiles — verified with `--release 21`
> and later; the same program with `--release 17` or earlier still gives
> the "unqualified name" error above. The unqualified form (`case KF:`)
> still works and is what most existing code (and the exam) uses, so both
> are worth recognising; the qualified form exists mainly to disambiguate
> when a switch is written generically over more than one enum type.

Mixing in a constant from a **different** enum is still illegal, unchanged:

```java
enum Color {
    RED, GREEN, BLUE
}

enum Beer {
    KF, KO
}

class Test {
    public static void main(String[] args) {
        Beer b = Beer.KF;
        switch (b) {
            case KF:
                System.out.println("KF");
                break;
            case RED: // CE: RED is not a constant of enum Beer
                System.out.println("red");
                break;
        }
    }
}
```

If every constant is listed, `default` is optional — but a constant added
to the `enum` later means old switches silently do nothing for it unless
they have a `default`. A `default` is the safer habit:

```java
enum Season {
    SUMMER, WINTER, RAINY
}

class Test {
    public static void main(String[] args) {
        Season s = Season.RAINY;
        switch (s) {
            case SUMMER:
                System.out.println("hot");
                break;
            case WINTER:
                System.out.println("cold");
                break;
            case RAINY:
                System.out.println("wet");
                break;
        }
    }
    // prints wet — valid without default because RAINY is listed
}
```

## Local variables inside `switch` — scope is the whole block

A variable declared in one `case` is in scope for the **entire** switch
block until its closing `}`, not just that case — `case` labels are jump
targets, not scopes.

```java
class Test {
    public static void main(String[] args) {
        int x = 1;
        switch (x) {
            case 1:
                int y = 10;
                System.out.println(y);
                break;
            case 2:
                int y = 20; // CE: variable y is already defined in this switch block
                System.out.println(y);
                break;
        }
    }
}
```

One `y` for the whole switch. Extra braces per case give each `case` its
own scope, if two independent locals with the same name are wanted:

```java
class Test {
    public static void main(String[] args) {
        int x = 2;
        switch (x) {
            case 1: {
                int y = 10;
                System.out.println(y);
                break;
            }
            case 2: {
                int y = 20;
                System.out.println(y);
                break;
            }
        }
    }
    // prints 20 — each { } block has its own y
}
```

Without extra braces, a later case can still **assign** (not redeclare) the
earlier declaration:

```java
class Test {
    public static void main(String[] args) {
        int x = 2;
        switch (x) {
            case 1:
                int y = 10;
                System.out.println(y);
                break;
            case 2:
                y = 20;
                System.out.println(y);
                break;
        }
    }
    // prints 20
}
```

If `case 2` were reached without ever going through `case 1`'s declaration
and tried to **read** `y` before assigning it, that's a "variable y might
not have been initialized" error — the compiler's definite-assignment check
still applies across the whole block.

## `switch` vs `if-else`

`switch` tests only **equality** of one expression against compile-time
constants (or enum/string constants) — it cannot test `x > 10`, ranges,
`&&`, `!=` of two variables, or anything beyond "equals this constant".
`if-else` can test any boolean condition.

A range needs `if-else` — faking it with 100 `switch` cases is the wrong
tool:

```java
class Test {
    public static void main(String[] args) {
        int x = 75;
        if (x < 0) {
            System.out.println("negative");
        } else if (x < 50) {
            System.out.println("small");
        } else if (x < 100) {
            System.out.println("medium");
        } else {
            System.out.println("large");
        }
    }
    // prints medium
}
```

`switch` has no `case x > 50` — that's not a constant:

```java
class Test {
    public static void main(String[] args) {
        int x = 75;
        switch (x) {
            case 75:
                System.out.println("exactly 75");
                break;
            default:
                System.out.println("not 75");
        }
    }
    // prints exactly 75
}
```

Where the same action applies to many discrete values, `switch`'s
fall-through grouping is shorter than the equivalent `if-else`:

```java
class Test {
    public static void main(String[] args) {
        char grade = 'B';
        switch (grade) {
            case 'A':
            case 'B':
            case 'C':
                System.out.println("pass");
                break;
            case 'D':
            case 'F':
                System.out.println("fail");
                break;
            default:
                System.out.println("invalid");
        }
    }
    // prints pass
}
```

```java
class Test {
    public static void main(String[] args) {
        char grade = 'B';
        if (grade == 'A' || grade == 'B' || grade == 'C') {
            System.out.println("pass");
        } else if (grade == 'D' || grade == 'F') {
            System.out.println("fail");
        } else {
            System.out.println("invalid");
        }
    }
    // prints pass — valid, just noisier
}
```

Both solve equality; `switch` is more convenient against many known
constants, `if-else` is the only option for anything else. And the two
never overlap on argument type: `if` always wants `boolean`; `switch` never
does.

## Empty `switch` vs empty `if`

`if (true);` is valid (empty statement via a bare `;`). `switch(x);` is
invalid — braces are mandatory. An empty **block**, `switch (x) {}`, is
valid:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        if (true)
            ;
        switch (x) {
        }
        System.out.println("reached");
    }
    // prints reached
}
```

## One more complete trace — all the rules at once

```java
class Test {
    public static void main(String[] args) {
        byte b = 2;
        switch (b) {
            default:
                System.out.println("def");
            case 0:
                System.out.println("0");
            case 1:
                System.out.println("1");
                break;
            case 2:
                System.out.println("2");
        }
    }
    // prints 2 — jumps straight to case 2, default never runs
}
```

Change only the value to `3`:

```java
class Test {
    public static void main(String[] args) {
        byte b = 3;
        switch (b) {
            default:
                System.out.println("def");
            case 0:
                System.out.println("0");
            case 1:
                System.out.println("1");
                break;
            case 2:
                System.out.println("2");
        }
    }
    // prints def, then 0, then 1 — no case matches, jump to default, fall through to break
}
```

Same switch, same labels — only the entry point changes, and that alone
changes everything that follows.

## Rules, all in one place

- Allowed `switch` arguments: `byte`, `short`, `char`, `int`; from 1.5 also
  `Byte`, `Short`, `Character`, `Integer`, and `enum`; from 1.7 also `String`.
- **Not** allowed as constants: `boolean`, `long`, `float`, `double`, and
  their wrappers `Boolean`, `Long`, `Float`, `Double` — though since Java 21
  the four wrappers can be switch arguments when matched with type patterns,
  `default`, or `case null` (not with old-style constant labels).
- Why not `boolean`: only two values; `if-else` is enough.
- Why not `long`: range too big for a jump table; the compiler checks the
  declared *type*, not the value, so `long x = 10L;` still fails even though
  `10` obviously fits an `int`.
- Why not `float`/`double`: exact equality on floating-point values is not
  reliable.
- `switch`'s curly braces are **mandatory**. `switch(x);` is a CE;
  `switch(x) {}` is valid.
- `case` and `default` are both optional → an empty switch is valid.
- Independent statements inside `switch`, outside any `case`/`default`, are
  a CE.
- A case label must be a **compile-time constant**: `final int y = 20;` is
  fine; `int y = 20;` is a CE; a blank `final` assigned later is a CE; a
  `final Integer` is a CE (it's a reference, not an `int` constant).
- A case value must be **within range** of (assignment-compatible with) the
  argument's type: `byte b; case 1000` is a CE ("possible lossy
  conversion"); `switch(b + 1) { case 1000 }` is valid because `b + 1` is
  `int`.
- Duplicate case labels are illegal, compared by **value**: `case 97` and
  `case 'a'` are duplicates.
- `default` is optional, can be anywhere, at most one. With no match: run
  `default` if present, else do nothing.
- `break` is optional; without it, fall-through continues until `break` or
  the end of the switch — even from a `default` that isn't written last.
- Nested `switch` is allowed; an inner `break` leaves only the inner switch.
- A wrapper argument unwraps to its primitive; a `null` wrapper or `null`
  String compiles and throws `NullPointerException` at runtime in this
  Java 7-style switch (fixable with `case null`, Java 21+).
- `String` switch (1.7) compares like `.equals(...)`, case-sensitive.
  `enum` switch (1.5) requires unqualified case labels in this lecture's
  era (`case KF`, not `case Beer.KF`) — Java 21 allows the qualified form
  too.
- A variable declared in one case is in scope for the whole switch block
  unless extra `{ }` are added per case.
- `switch` tests equality against constants (or, since Java 21, an
  argument's type via pattern matching); `if-else` tests any boolean
  condition. Prefer `switch` for many discrete values; use `if-else` when
  `switch` can't express the condition.

## Exam traps at a glance

| Code | What most people say | Actual |
|---|---|---|
| `switch` on `boolean`/`long`/`float`/`double` | valid | CE — incompatible types |
| `switch` on `Boolean`/`Long`/`Float`/`Double` with a **constant** case label | wrappers are allowed from 1.5 | CE — only `Byte`/`Short`/`Character`/`Integer` accept constants (these four are switchable via type patterns/`default` since Java 21 — see callout above) |
| `switch(x);` | valid empty, like `if (true);` | CE — `{` expected |
| `switch(x) {}` | CE — empty | valid, no output |
| statement inside `switch` with no `case`/`default` | valid | CE |
| `case y` with `int y = 20;` | valid | CE — constant expression required |
| `case y` with `final int y;` then `y = 20;` | valid because `final` | CE — not a compile-time constant |
| `case y` with `final Integer y = 10;` | valid | CE — constant expression required |
| `byte b; case 1000` | valid (promoted to `int`) | CE — possible lossy conversion |
| `switch(b + 1) { case 1000 }` | same CE | valid — argument is `int` |
| `case 97` and `case 'a'` | both valid | CE — duplicate case label |
| `default` first, `x` matches a later case | `default` always runs | jump to the matching case; `default` skipped |
| `default` first, no match, no `break` | only `default` prints | `default` **and** the cases it falls into |
| `Integer i = null; switch(i)` | `default` runs, or CE | compiles; NPE (fixable with `case null` since Java 21) |
| `String s = null; switch(s)` | `default` runs | compiles; NPE (same Java 21 fix applies) |
| `case Beer.KF` | valid | CE before Java 21; **valid from Java 21** |
| `new String("durga")` vs `case "durga"` | not matched (`==`) | matched (`equals`) |
| `"Hyderabad"` vs `"hyderabad"` | same label | different labels — case-sensitive |
| two `int y` in two cases | valid | CE — `y` already defined in this switch |

## Exam and interview points

1. **Allowed types with constant labels**: `byte`, `short`, `char`, `int`
   always; their four wrappers plus `enum` from 1.5; `String` from 1.7.
   Never `boolean`, `long`, `float`, `double`, or their wrappers as
   *constants* — that hasn't changed. Java 21 did add one exception, but
   only for pattern-matching labels: `Boolean`/`Long`/`Float`/`Double` can
   now be switch arguments if matched with type patterns, `default`, or
   `case null` (see the callout above) — the four primitives themselves
   still cannot be switched on at all outside an unreleased preview.
2. **Braces are mandatory** for `switch`; `case` and `default` are both
   optional, so an empty `switch (x) {}` is legal. A statement with no
   `case`/`default` above it is not.
3. **Every case label needs all three**: compile-time constant, in range of
   the argument type, unique. A `final` variable is a constant only if
   initialized with a constant expression at its own declaration; a
   `final Integer` never qualifies because it's a reference, not an `int`.
4. **Fall-through is the default**, not the exception — `break` is what
   stops it, `default` can sit anywhere and still falls into whatever
   follows it if it has no `break` of its own.
5. **Wrapper arguments unwrap**, and a `null` wrapper or `null` String
   compiles fine but throws `NullPointerException` at runtime in this
   Java 7-style switch — `default` does not catch a `null` argument.
6. **`enum` case labels are unqualified** (`case KF`, not `case Beer.KF`) in
   the OCJP-era form this lecture teaches — Java 21 relaxed this, see the
   ⚠️ Modern Java callout above.
7. **`String` switch matches like `equals`**, case-sensitive, works even on
   a `new String(...)` instance — it is never reference (`==`) comparison.
8. **Nested `switch` is fine**; an inner `break` only exits the inner
   switch, never the outer one.
9. Since **Java 14**, `switch` can be an **expression** with arrow labels
   and no fall-through (`yield` for multi-statement branches); since
   **Java 21**, `case null` is legal directly, and pattern matching for
   `switch` (JEP 441) extends matching to an argument's *type*, not just
   its value. All of this sits on top of — not instead of — the colon/break
   form covered here, which is what the exam and most legacy code use.

---

**Next:** Video 027 — while, do-while
