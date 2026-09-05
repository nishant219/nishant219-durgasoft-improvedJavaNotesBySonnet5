# Video 025 — Selection Statements: if-else

## Video info

**Title:** Core Java with OCJP/SCJP: Flow-Control Part-2  || Selection Statements : if-else

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 25 of 203 |
| Series | Flow-Control · Part 2 of 6 |
| Topic | if-else: boolean argument, = vs ==, braces, empty statement, dangling else |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 32m 21s (1941 seconds) |
| Video ID | FnnJkV1Euxk |
| Watch | https://www.youtube.com/watch?v=FnnJkV1Euxk |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Two exam-sized conclusions about `if-else`, plus a small bonus at the end.

1. Syntax: `if (b)` / `else` — **`b` must be boolean**. Any other type is a
   compile-time error (`incompatible types`, found `int`, required `boolean`).
   Exam options circle around `if (x)`, `if (x = 20)`, `if (x == 20)`,
   `if (b = false)`, `if (b == false)`.
2. **`else` is optional. Curly braces are optional.** Without braces, only
   **one** statement is allowed under `if`, and it **must not be a
   declarative statement**. The same rule applies wherever braces are
   optional (`while`, …). A bare semicolon is a valid **empty statement**.
3. Bonus: **there is no dangling-else problem in Java** — every `else` maps
   to the **nearest `if`**.

---

## 00:38 — Syntax: the boolean-only rule

```java
if (b) {          // b must be boolean type
    // action if b is true
} else {
    // action if b is false
}
```

The syntax itself is simple; the one compulsory rule is that the argument to
`if` must be **boolean type**. Provide anything else and it is a
compile-time error by default — a small point, Sir warns, but one the exam
loves to probe from every angle.

### 03:54 — Example 1: `if (x)` with `int x` — the C/C++ trap

```java
class Test {
    public static void main(String[] args) {
        int x = 0;
        if (x) {
            System.out.println("hello");
        } else {
            System.out.println("hi");
        }
    }
}
// CE: incompatible types
// found: int
// required: boolean
```

Most people fail this one: `x` is `0`, `0` means false in C/C++, so they
expect `hi`. **Java has no such terminology.** `if` always expects
`boolean`; here it was given `int`, so the compiler rejects the program
before it can run at all — there is no "high" to print, only a compile
error.

> ❗ **Correction — the exact compiler wording has changed.**
> The three-line message Sir dictates (`incompatible types` / `found: int`
> / `required: boolean`) is the **Java 6/7 javac** wording. A current javac
> (verified on 26) collapses it to one line:
>
> ```text
> error: incompatible types: int cannot be converted to boolean
> ```
>
> Same defect, same rule, tidier diagnostic. If you see the old three-line
> form in a textbook, it is not wrong — just dated output.

### 05:51 — Example 2: `if (x = 20)` — assignment, not comparison

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        if (x = 20) {
            System.out.println("hello");
        } else {
            System.out.println("hi");
        }
    }
}
// CE: incompatible types: int cannot be converted to boolean
```

Most people see `10` and `20`, decide they are unequal, and guess `hi`. But
`x = 20` is a **single `=`** — assignment, not comparison. `x` becomes `20`,
so the check is really `if (20)`, and `if` never accepts an `int`. Same
compile error as Example 1, for the same reason: know your `=` from your
`==` before you evaluate anything else.

### 07:23 — Example 3: `if (x == 20)` — comparison, prints `hi`

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        if (x == 20) {
            System.out.println("hello");
        } else {
            System.out.println("hi");
        }
    }
}
// prints hi
```

Now it really is comparison. `10 == 20` is `false`, the `else` branch runs,
and the output is `hi` — this time for the reason people guessed in
Example 2.

### 08:16 — Example 4: `boolean b = true; if (b = false)` — valid assignment

```java
class Test {
    public static void main(String[] args) {
        boolean b = true;
        if (b = false) {
            System.out.println("hello");
        } else {
            System.out.println("hi");
        }
    }
}
// prints hi
```

Assignment again — but this time it compiles. `b = false` assigns `false`
to `b` **and** the assignment expression's value is `false`, which is
already a `boolean`. `if` does not care whether the argument arrived by
comparison or by assignment; it only cares that the final value is
`boolean`. So `if (b)` becomes `if (false)`, the `else` branch runs, and the
output is `hi`.

### 10:05 — Example 5: `boolean b = false; if (b == false)` — comparison, prints `hello`

```java
class Test {
    public static void main(String[] args) {
        boolean b = false;
        if (b == false) {
            System.out.println("hello");
        } else {
            System.out.println("hi");
        }
    }
}
// prints hello
```

`false == false` is `true`, so `hello` prints. Sir's warning: people who
learned the "assignment inside `if` never compiles" reflex from other
languages will misjudge Examples 2 and 4 in opposite directions — the only
fix is to actually check whether the operator is `=` or `==` and what type
results.

### 11:26 — The five, side by side

| Code | What most people guess | Actual result |
|---|---|---|
| `int x = 0; if (x)` | `hi` (0 is false) | **CE** — incompatible types |
| `int x = 10; if (x = 20)` | `hi` (10 ≠ 20) | **CE** — it's assignment, then `if (20)` |
| `int x = 10; if (x == 20)` | confused with `=` | `hi` (valid comparison, 10 ≠ 20) |
| `boolean b = true; if (b = false)` | CE, because it's assignment | valid, prints `hi` |
| `boolean b = false; if (b == false)` | `hi` / CE | `hello` |

---

## 14:53 — `else` and braces are optional — but only one statement

Is `else` mandatory? No — optional. Are curly braces mandatory? No —
optional too. Sir flags this as the twist most people miss: **without
braces, only one statement is allowed under `if`.**

### 15:55 — One statement, no braces — valid

```java
class Test {
    public static void main(String[] args) {
        if (true)
            System.out.println("hello");
    }
}
// compiles; prints hello
```

### 16:18 — `if (true);` — the empty statement

```java
if (true);
```

A bare semicolon is a valid Java statement — the **empty statement**. You
can stack any number of them. `if (true);` compiles cleanly and produces no
output at all; the `if` simply has nothing to do when it's true.

```java
class Test {
    public static void main(String[] args) {
        if (true);
        ;;;   // more empty statements — still fine, still no output
    }
}
```

### 17:02 — `if (true) int x = 10;` without braces — invalid

Sir has the class guess before showing it. Without braces it looks like one
statement, same as the `println` version above — but it is not allowed:

```java
class Test {
    public static void main(String[] args) {
        if (true)
            int x = 10;   // CE
    }
}
```

Wrap the same declaration in braces and it compiles without complaint:

```java
class Test {
    public static void main(String[] args) {
        if (true) {
            int x = 10;   // valid — braces present
        }
    }
}
// compiles; no output (nothing is printed either way)
```

So bracing the identical line is the only difference between a compile
error and a clean compile. On javac 6/7 this single line produced a
cascade Sir reads out loud on the recording — `;` expected, not a
statement, illegal start of expression, up to four errors for one bad line,
"even the compiler is getting shocked."

> ❗ **Correction — the "four errors" claim is compiler-version-specific,
> and the modern message is different (and singular).**
> Verified on javac 26, the same code produces exactly **one** clear
> diagnostic:
>
> ```text
> error: variable declaration not allowed here
> ```
>
> Old javac's error recovery re-parsed the same bad token several times and
> reported each mis-parse separately, which is where the "four errors"
> came from. Modern javac recognizes the specific mistake — a local
> variable declaration where only an expression statement is legal — and
> names it in one line. Same rule, much friendlier diagnostic.

### 21:26 — The rule generalizes beyond `if`

This is not an `if`-only quirk. `while` follows the identical rule: without
braces, only one statement is allowed under `while`, and it must not be
declarative.

```java
while (condition)
    int x = 10;   // CE — same rule, same reason, no braces

while (condition) {
    int x = 10;   // fine — braces present
}
```

Sir's framing: **wherever curly braces are optional in Java, this rule
applies.**

### 21:56 — Why: `x` is scoped to a block that no longer exists

The internal reason, in Sir's words: `x` in `if (true) int x = 10;` is a
**local variable of the `if` block**. It can only be used *inside* that
block. Without braces, the `if` block is exactly one statement long — the
moment that statement's semicolon completes, the `if` block is over, and
`x` is already out of scope in every line that follows. You would be
declaring and assigning a variable you are structurally forbidden from
ever reading — so the compiler refuses to let you declare it there at all.

With braces, the block can hold "thousands of lines," and every one of
them is a place `x` could legitimately be read — so the declaration is
allowed, whether or not any later line actually uses it. The compiler is
reasoning about *possibility of use*, not about whether you happen to use
it.

> ⚠️ **Modern Java — a related but different variable-scoping rule inside
> `if` arrived in Java 16.**
> Pattern matching for `instanceof` (JEP 394) lets a variable come out of
> a condition test:
>
> ```java
> if (obj instanceof String s) {
>     System.out.println(s.length());   // s is in scope here
> }
> // s is NOT in scope out here — same lexical-scope rule Sir describes
> ```
>
> But if the `if` branch always exits — `return`, `throw`, `break`,
> `continue` — the compiler's **flow scoping** carries the pattern variable
> *past* the closing brace, into the code that follows:
>
> ```java
> void print(Object obj) {
>     if (!(obj instanceof String s)) {
>         return;
>     }
>     System.out.println(s.length());   // s IS in scope here — flow scoping
> }
> ```
>
> This is new territory Sir's lecture never touches: unlike the plain
> local variable in his example, a pattern variable's scope is no longer
> just "the braces it was declared in" — it depends on how the branch
> exits. Java 21 extends the same pattern syntax to `switch`.

---

## 28:23 — Bonus: no dangling else in Java

One more point — small, but a student had asked about it the day before.
Consider two `if`s and a single `else`:

```java
class Test {
    public static void main(String[] args) {
        boolean outer = true, inner = true;
        if (outer)
            if (inner)
                System.out.println("hello");
            else
                System.out.println("hi");
    }
}
```

Two `if` statements, only one `else`. Which `if` does it belong to — the
first, the second, or both? Sir's rule: **every `else` binds to the
nearest `if`**, so here it belongs to the inner `if`, even though
indentation makes it look like it hangs off the outer one. There is no
"dangling else problem" in Java — the compiler always resolves it the same
way, unambiguously.

> ❗ **Correction — this isn't a Java-vs-weak-compiler story; C and C++
> resolve it exactly the same way.**
> Sir frames this as Java's compiler being "strong" where old C/C++
> compilers "get left and right" over an ambiguous `else`. In fact the C
> grammar (and C++'s, and Java's) all specify the identical disambiguation
> rule: **an `else` binds to the nearest preceding, still-unmatched `if`.**
> This has been a spelled-out grammar rule in C since the original K&R
> language, not something later compilers had to get "strong enough" to
> handle. "Dangling else" names an ambiguity in how a *human reader* parses
> the indentation, not a compiler limitation — no C, C++, or Java compiler
> has ever rejected or misresolved this code. The teaching point that
> survives intact: **in Java, `else` always maps to the nearest `if`** — just
> don't repeat the claim that other compilers can't cope with it.

---

## Exam and interview points

1. **The argument to `if` must be `boolean`.** No C-style `0`/`1`
   truthiness in Java — providing an `int` (or anything non-boolean) is a
   compile-time error, not a runtime `false`.
2. **Check `=` vs `==` before you evaluate anything else.** `if (x = 20)`
   on an `int x` is a compile error (result is `int`); `if (b = false)` on
   a `boolean b` is valid (result is already `boolean`) and uses the
   value *after* the assignment.
3. **`else` is optional; curly braces are optional** — but without braces,
   `if` (and `while`, and anywhere else braces are optional) accepts
   **exactly one** statement, and that statement **must not be a
   declarative statement**.
4. **Why:** a variable declared without braces is scoped to a one-statement
   block that ends at the very next semicolon — it could never legally be
   read, so the compiler refuses to let you declare it there.
5. **A bare `;` is a valid Java statement** — the empty statement.
   `if (true);` compiles and produces no output; you may stack any number
   of extra semicolons.
6. **There is no dangling-else problem in Java** (or in C/C++, despite the
   lecture's framing) — an `else` always binds to the **nearest** unmatched
   `if`.
7. **Modern-Java footnote:** compiler diagnostics for these exact mistakes
   are cleaner today (one message instead of Sir's three- or four-line
   cascades) — same rules, better error text. Pattern matching for
   `instanceof` (Java 16) adds a second, *flow-sensitive* kind of variable
   scoping inside `if` that this lecture's simple lexical-scope story does
   not cover.

**Next:** Video 026 — switch
