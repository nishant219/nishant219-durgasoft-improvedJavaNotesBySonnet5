# Video 027 — while, do-while

## Video info

**Title:** Core Java with OCJP/SCJP: Flow-Control Part-4  || Iterative Statements: while,do-while

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 27 of 203 |
| Series | Flow-Control · Part 4 |
| Topic | Iterative statements: while, do-while |
| Instructor | Durga Sir |
| Duration | 1h 12m 39s |
| Video ID | dd9Epay1y6g |
| Watch | https://www.youtube.com/watch?v=dd9Epay1y6g |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. `while` — when to use it instead of `for`
2. Where `while` shows up in real code: `ResultSet`, `Enumeration`, `Iterator`
3. `while` syntax — the condition **must** be `boolean`
4. `while (1)` — a C/C++ habit that is a Java compile error
5. Curly braces are optional, same rule as `if`
6. The unreachability loophole — six `while` cases (`true` / `false` / normal
   variables / `final` variables)
7. Two compiler notes: a `final` variable is replaced by its value at compile
   time; an operation is folded at compile time when every operand is a
   compile-time constant
8. `do-while` — the body executes **at least once**; the trailing semicolon
   is mandatory
9. Curly braces between `do` and `while`
10. The "99% think it's a compile error" nested `do` / `while (true)` /
    `while (false)` case — it is actually valid
11. Unreachability again, for `do-while` — the same six cases, except
    `do { } while (false)` is valid where plain `while (false)` was not

---

## 00:07 — `while` vs `for`: when to reach for which

He starts from a `for` loop he already used:

```java
for (int i = 0; i < 10; i++) {
    System.out.println("hello");
}
```

`hello` prints 10 times. If the number of iterations is known in advance —
exactly 10, exactly 20 — `for` is the best choice.

Sometimes the count is **not** known up front:

- for every record in a `ResultSet`, do something — how many records? unknown
  until you've read them
- for every object in a collection, do something — how many objects? unknown

Board sentence:

> *If we don't know number of iterations in advance then we should go for
> while loop.*

## 02:21 — Where `while` shows up in real code

JDBC — draining a `ResultSet` one row at a time:

```java
while (rs.next()) {
    // for every record present in the ResultSet, do some activity
}
```

Collections cursor, `Enumeration`:

```java
while (e.hasMoreElements()) {
    // for every element present inside the Enumeration, do certain activity
}
```

`Iterator`:

```java
while (it.hasNext()) {
    // for every next object present inside the Iterator, do some activity
}
```

Rule of thumb: count known in advance → `for`; count unknown → `while`.

## 05:55 — Syntax: the condition must be `boolean`

```java
while (b) {
    // action / loop body
}
```

`b` must be `boolean`. The body executes as long as `b` is `true`; once `b`
is `false`, the loop stops.

Board:

> *The argument should be boolean type. If we are trying to provide any
> other type then we will get compile time error.*

### 08:06 — `while (1)` — a C/C++ habit that is a Java compile error

```java
while (1) {
    System.out.println("hello");
}
// CE: incompatible types: int cannot be converted to boolean
```

In C and C++, `1` means `true`, so `while (1)` loops forever. **Java has no
such coercion** — an `int` cannot stand in for a `boolean` anywhere,
including a loop condition.

> ⚠️ **Modern Java — the compiler's wording changed, the rule didn't.**
> This has always been a compile error; only how `javac` phrases it moved.
> Java 6/7-era `javac` (matching what Sir dictates on the board) reported it
> as a multi-line diagnostic:
>
> ```text
> incompatible types
> found   : int
> required: boolean
> ```
>
> Since Java 7, `javac` folds this into one line — verified on JDK 26:
>
> ```text
> error: incompatible types: int cannot be converted to boolean
> ```
>
> Same rule the whole time: no numeric type is ever accepted where a
> `boolean` is required. Only the printed shape of the error changed — the
> same wording change documented for narrowing casts in video 020.

## 09:45 — Curly braces are optional

Same rule as `if`/`else`. Without braces, `while` may take only **one**
statement, and that statement must not be a declaration.

```java
while (true)
    System.out.println("hello"); // valid — one non-declarative statement
```

```java
while (true)
    ; // valid — a bare semicolon is itself a valid Java statement
```

```java
while (true)
    int x = 10; // CE: variable declaration not allowed here
```

```java
while (true) {
    int x = 10;
} // valid — braces make a declaration fine
```

Board:

> *Curly braces are optional. Without curly braces we can take only one
> statement under while, which should not be declarative statement.*

## 13:08 — The unreachability loophole: six `while` cases

This loophole is not special to `while` — it applies to `for`, for-each,
every loop. Six shapes, and the pattern is: first two invalid, next two
valid, last two invalid.

| # | Condition | Valid? |
|---|---|---|
| 1 | `while (true)` then a statement after the loop | invalid |
| 2 | `while (false)` | invalid |
| 3 | normal `int a, b` and `a < b` | valid |
| 4 | normal `int a, b` and `a > b` | valid |
| 5 | `final int a, b` and `a < b` | invalid |
| 6 | `final int a, b` and `a > b` | invalid |

### 18:46 — Case 1 — `while (true)` then `hi`

```java
while (true) {
    System.out.println("hello");
}
System.out.println("hi"); // CE: unreachable statement
```

If the condition is `true`, `hello` executes forever — `hi` never gets a
turn. Unreachable statements are a compile-time error, and the compiler can
prove this one is unreachable because `true` is a literal, not a variable.

### 19:42 — Case 2 — `while (false)`

```java
while (false) {
    System.out.println("hello");
} // CE: unreachable statement (pointing at the opening curly brace)
System.out.println("hi");
```

The condition is `false`, so the loop body never runs even once — the
**entire body** is unreachable. `javac` points the error at the loop's
opening `{`.

### 20:35 — Case 3 — normal variables, `a < b`

```java
int a = 10, b = 20;
while (a < b) {
    System.out.println("hello");
}
System.out.println("hi");
```

Valid — compiles clean. `a` and `b` are ordinary local variables; the
compiler never looks at their *values*, only that `a < b` is a legal
`boolean` expression. Whether it's `true` or `false` is a runtime question.
At runtime `10 < 20` is `true`, so this prints `hello` forever.

Who checks unreachability? The **compiler**. The JVM's job is only to
execute — Sir's analogy: the person checking ID cards at the door is the
compiler; once you're inside, the class continues regardless of whether the
door-check happened correctly. If the compiler can't *prove* something is
unreachable, the JVM will happily run it, endlessly if need be.

### 24:12 — Case 4 — normal variables, `a > b`

```java
int a = 10, b = 20;
while (a > b) {
    System.out.println("hello");
}
System.out.println("hi");
```

Valid, for the same reason as Case 3 — the compiler still doesn't evaluate
`a > b`. At runtime `10 > 20` is `false`, so the body never runs.
**Output: `hi`.**

### 24:56 — Case 5 — `final` variables, `a < b`

```java
final int a = 10, b = 20;
while (a < b) {
    System.out.println("hello");
}
System.out.println("hi"); // CE: unreachable statement
```

`a` and `b` are `final`, so their values can never change after
initialization — the compiler *does* evaluate `a < b`, gets `true`, and
treats this exactly like `while (true)`. `hi` is unreachable.

### 26:29 — Case 6 — `final` variables, `a > b`

```java
final int a = 10, b = 20;
while (a > b) {
    System.out.println("hello");
} // CE: unreachable statement (pointing at the opening curly brace)
System.out.println("hi");
```

The compiler folds `a > b` to `10 > 20`, i.e. `false` — same as
`while (false)`, so the entire loop body is unreachable.

| Case | Compiles? | Runtime output if it compiled |
|---|---|---|
| `while (true)` + `hi` after | CE (`hi` unreachable) | — |
| `while (false)` | CE (body unreachable) | — |
| normal `a < b` | valid | infinite `hello` |
| normal `a > b` | valid | `hi` |
| `final a < b` | CE (`hi` unreachable) | — |
| `final a > b` | CE (body unreachable) | — |

All six verified on JDK 26 — every compile/CE result and every printed line
matches. Every loop construct in Java shares this same unreachability rule.

## 33:26 — Note 1: a `final` variable is replaced by its value at compile time

Board:

> *Every final variable will be replaced by the value at compile time only.*

```java
final int a = 10;
int b = 20;
System.out.println(a);
System.out.println(b);
```

`a` can never be anything but `10`, so the compiler substitutes it directly.
After compilation, conceptually:

```java
System.out.println(10);
System.out.println(b);
```

`b` is a normal variable — its value is only known at runtime, so it stays
`b` in the generated code.

Board:

> *If it is a normal variable, its value will be considered only at run
> time. If it is a final variable, its value will be considered at compile
> time.*

## 35:48 — Note 2: compile-time constant folding

> *If every argument is a final variable (compile-time constant), then that
> operation should be performed at compile time only.*

```java
final int a = 10, b = 20;
int c = 20;
System.out.println(a + b);   // both final → folded to 30
System.out.println(a + c);   // c is normal → stays as 10 + c
System.out.println(a < b);   // both final → folded to true
System.out.println(a < c);   // c is normal → stays as 10 < c
```

Verified on JDK 26: prints `30`, `30`, `true`, `true` — the last two lines
compute their runtime-evaluated form to the same values, since `c` happens
to equal `20`.

This is exactly why `final int a = 10, b = 20; while (a < b)` behaves as
`while (true)` in the compiler's eyes: both operands are compile-time
constants, so the comparison is folded before the program ever runs.

## 43:37 — `do-while`: the body executes at least once

Board heading: **do while**.

The real difference from `while` is not "one has `do`" — it's that a plain
`while` body may run **zero** times, but sometimes the requirement is that
the body must run **at least once**. That's what `do-while` is for.

```java
do {
    // loop body
} while (b);
```

`b` must be `boolean`, same as `while`. Flow: run the body → check `b` → if
`true`, run again → if `false`, stop. Either way, the body has already run
once before the condition is even checked.

Board:

> *If we want to execute loop body at least once then we should go for
> do-while.*

> ❗ **Correction — the mandatory trailing semicolon is not a Java-vs-C++ difference.**
> Sir says the semicolon after `while (b)` is optional in C/C++ but mandatory
> in Java. The conclusion for Java is right — `do { } while (b)` without the
> `;` is a syntax error — but the contrast is invented: in C and C++, the
> `do` statement's grammar (`do statement while ( expression ) ;`) requires
> that trailing `;` too. It's the one iteration form in the C family whose
> closing token is a semicolon rather than a block or a bare statement, and
> that's true in C, C++, *and* Java alike. The exam-relevant fact — never
> forget the semicolon after a `do-while` — stands regardless.

## 47:48 — `do-while` curly braces

Curly braces are optional everywhere except `switch`. Without braces,
between `do` and `while` there may be only **one** statement, and it must
not be a declaration.

```java
do
    System.out.println("hello");
while (true); // valid — one non-declarative statement
```

```java
do
    ;
while (true); // valid — a bare semicolon is a valid statement
```

```java
do
    int x = 10;
while (true); // CE: variable declaration not allowed here
```

```java
do {
    int x = 10;
} while (true); // valid — braces make a declaration fine
```

```java
do
while (true); // CE — see correction below
```

Board:

> *Curly braces are optional. Without curly braces we can take only one
> statement between do and while, which should not be declarative
> statement.*

> ❗ **Correction — the last example does not fail because "the body is missing."**
> Sir reads this as "between `do` and `while`, there is no body." Compiling
> it on JDK 26 shows the real story is almost the opposite:
>
> ```text
> error: while expected
>         while (true);
>                      ^
> error: illegal start of expression
>     }
>     ^
> ```
>
> `while (true);` **is** a complete, legal statement on its own — a nested
> `while` loop with an empty body. The parser greedily consumes it *as the
> `do`'s body*. That leaves nothing to serve as the outer `do-while`'s own
> required `while ( … ) ;` clause, so the compiler runs out of tokens and
> reports `while expected` at the closing brace. The body isn't missing —
> the outer loop's condition clause is, because the inner `while` ate it.
> The teaching point survives either way: this exact two-line shape does not
> compile, and the fix is braces or a distinguishing statement — but the
> mechanism is a parsing ambiguity, not an empty body.

## 53:03 — The case 99% call invalid — it's actually valid

```java
do
    while (true)
        System.out.println("hello");
while (false);
```

Shown to a room, most people call this invalid for two reasons: "there are
two statements between `do` and `while`," and "the inner `while (true)` is
missing its semicolon." **Pakka valid** — both objections dissolve once you
read it by grammar, not by line count.

Physically there are two lines; logically the statement between `do` and the
outer `while (false)` is **one** `while` statement —
`while (true) System.out.println("hello");` — with the `println` as its
body. That's why it doesn't need its own semicolon: a `while` loop with a
block or single-statement body was never terminated by one. Sir's analogy:
a `try`/`catch`/`finally` with a hundred thousand lines in each block is
still, physically enormous but **logically one statement** — Java's grammar
counts statements, not lines.

The second objection — "`while (true)` runs forever, so the outer
`while (false)` becomes unreachable" — also fails: you have already
**entered** the `do`. The first half of a `do-while` is always reachable by
definition, so the compiler doesn't get to call any of it unreachable; it
checks reachability statement-by-statement, not by whether a nested loop
happens to run forever.

Verified on JDK 26: this compiles. Running it prints `hello` forever, as
expected from the nested `while (true)`.

## 1:00:59 — Unreachability in `do-while`: same six cases, one difference

Same six shapes as for `while`, but because the body always runs at least
once, `do { } while (false)` is **valid** — the mirror image of plain
`while (false)`, which was not.

**Case 1 — `while (true)` then `hi`**

```java
do {
    System.out.println("hello");
} while (true);
System.out.println("hi"); // CE: unreachable statement
```

Invalid — `hello` runs forever, so `hi` is unreachable.

**Case 2 — `while (false)` then `hi`**

```java
do {
    System.out.println("hello");
} while (false);
System.out.println("hi");
```

**Valid.** The body runs once regardless, prints `hello`, the condition is
`false` so the loop stops, then `hi`. **Output: `hello` then `hi`.** This is
the direct contrast with plain `while (false)`, which was a compile error.

**Case 3 — normal variables, `a < b`**

```java
int a = 10, b = 20;
do {
    System.out.println("hello");
} while (a < b);
System.out.println("hi");
```

Valid — the compiler doesn't evaluate normal variables. At runtime,
`10 < 20` is `true`, so this compiles fine and prints `hello` forever.

**Case 4 — normal variables, `a > b`**

```java
int a = 10, b = 20;
do {
    System.out.println("hello");
} while (a > b);
System.out.println("hi");
```

Valid. Body runs once (`hello`), then `10 > 20` is `false`, loop stops, then
`hi`. **Output: `hello` then `hi`.**

**Case 5 — `final` variables, `a < b`**

```java
final int a = 10, b = 20;
do {
    System.out.println("hello");
} while (a < b);
System.out.println("hi"); // CE: unreachable statement
```

The compiler folds `a < b` to `true`, so the loop never ends — `hi` is
unreachable.

**Case 6 — `final` variables, `a > b`**

```java
final int a = 10, b = 20;
do {
    System.out.println("hello");
} while (a > b);
System.out.println("hi");
```

**Valid.** The compiler folds `a > b` to `false`, but that only stops the
loop *after* its one guaranteed run — the body already executed once, so
`hi` is perfectly reachable. **Output: `hello` then `hi`.**

| Case | Compiles? | Output if valid |
|---|---|---|
| `do … while (true)` + `hi` after | CE (`hi` unreachable) | — |
| `do … while (false)` + `hi` after | valid | `hello` then `hi` |
| normal `a < b` | valid | infinite `hello` |
| normal `a > b` | valid | `hello` then `hi` |
| `final a < b` | CE (`hi` unreachable) | — |
| `final a > b` | valid | `hello` then `hi` |

All six verified on JDK 26. Remove every unreachable statement and the rest
compiles; that is the whole loophole, for every loop construct in the
language.

## 1:11:14 — Close

That closes `while` and `do-while`. The unreachability loophole is not
specific to this lecture — it recurs in every loop shape Java has, and it's
worth being able to spot on sight: literal condition vs. variable condition,
`final` vs. normal.

---

## Exam and interview points

1. **Known iteration count → `for`; unknown count → `while`.** The canonical
   `while` sites are `rs.next()`, `Enumeration.hasMoreElements()`, and
   `Iterator.hasNext()`.
2. **The condition of `while` and `do-while` must be `boolean`** — no other
   type is accepted, unlike C/C++ where any non-zero `int` means `true`.
   `while (1)` is a Java compile error, full stop.
3. **Curly braces are optional** for `while`, `do-while`, and `if`, but never
   for `switch`. Without braces, exactly one non-declarative statement is
   allowed; a bare `;` counts as that one statement.
4. **The six-case unreachability loophole applies to every loop**: literal
   `true`/`false` conditions are checked at compile time (CE if unreachable
   code follows); conditions built from plain variables are never evaluated
   by the compiler (checked only at runtime, however long that takes);
   conditions built entirely from `final` variables *are* folded at compile
   time, because a `final` variable's value can never change after
   initialization.
5. **A `final` local variable initialized with a constant is replaced by its
   value at compile time**, and an operation is folded to a compile-time
   constant when every operand is such a value. This is why
   `final int a = 10, b = 20; while (a < b)` compiles exactly like
   `while (true)`.
6. **`do-while` guarantees the body runs at least once**, because the
   condition is checked *after* the first pass — the one real behavioral
   difference from `while`, not merely the keyword.
7. **The trailing `;` after `do { … } while (cond)` is mandatory** — in
   Java, and, contrary to what's sometimes taught, in C/C++ too; it's part
   of the `do-while` grammar in all three languages, not a Java-only rule.
8. **`do { } while (false)` is valid; plain `while (false)` is not.** That
   asymmetry — body-runs-once vs. body-may-run-zero-times — is the cleanest
   one-line way to state the difference between the two loops.
9. **`do \n while (cond);` on two lines with nothing else is a compile
   error**, but not because "the body is missing" — `while (cond);` is
   itself swallowed as the `do`'s body (a legal nested `while`), leaving the
   outer `do-while`'s own condition clause absent. Braces avoid the
   ambiguity entirely.
10. **A nested `do / while (true) SOP / while (false);` is valid**, though
    99% of a room calls it a compile error on sight. Java's grammar counts
    logical statements, not physical lines, and the first half of a
    `do-while` is always reachable once you've entered it — a nested
    infinite `while (true)` inside does not retroactively make the outer
    loop's condition unreachable.

---

**Next:** Video 028 — for, for-each
