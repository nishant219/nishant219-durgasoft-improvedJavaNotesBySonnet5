# Video 029 — Transfer Statements: break and continue

## Video info

**Title:** Core Java with OCJP/SCJP: Flow-Control Part-6  || Transfer statements : break and continue

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 29 of 203 |
| Series | Flow-Control · Part 6 of 6 |
| Topic | Transfer statements: break, continue, labeled break/continue, do-while vs continue |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 50m 59s |
| Video ID | 90DPWIfbPiY |
| Watch | https://www.youtube.com/watch?v=90DPWIfbPiY |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Last Flow-Control session. Transfer statements move control from one place
to another.

1. `break` — three legal places (switch, loops, labeled blocks)
2. `continue` — only inside loops
3. Labeled `break` / `continue` in nested loops (exam favourite)
4. `do-while` versus `continue` — a dangerous combination; output is
   `1 4 6 8 10`

---

## 00:07 — Transfer statements

Board heading: **transfer statements**. We use them to transfer control from
one place in a program to another. First transfer statement: **`break`**.

## 00:43 — Where `break` can be used: three places

### 00:43 — Place 1: inside `switch`

```java
int x = 0;
switch (x) {
    case 0:
        System.out.println(0);
    case 1:
        System.out.println(1);
        break;
    case 2:
        System.out.println(2);
    default:
        System.out.println("def");
}
// prints 0
// 1
```

`case 0` matches. From that point **every statement runs until `break` or
the end of the switch** — fall-through. So `0` then `1`. Delete the `break`
entirely and it falls all the way through to `def`, printing `0 1 2 def`.
Inside `switch`, `break` exists to **stop fall-through**.

### 03:00 — Place 2: inside loops

```java
for (int i = 0; i < 10; i++) {
    if (i == 5)
        break;
    System.out.println(i);
}
// prints 0 1 2 3 4
```

`i` counts up; the moment it hits `5`, `break` exits the loop outright.
`break` inside a loop **ends the loop based on a condition**, rather than
waiting for the loop's own test to fail.

### 04:27 — Place 3: inside labeled blocks

A rarely used third possibility, but a valid one: **inside labeled blocks**.
A labeled block is just a block with a name in front of it, and the name
buys you nothing beyond readability — "this block does database work," "this
block does printing." `break <label>` is the one thing a label lets you do
that a plain block can't: exit early.

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        l1: {
            System.out.println("begin");
            if (x == 10)
                break l1;
            System.out.println("end");
        }
        System.out.println("hello");
    }
}
// prints begin
// hello
```

`begin` prints. `x == 10`, so `break l1` exits the labeled block immediately
— `end` never runs. Control resumes after the block, so `hello` prints
next. Verified: **`begin` followed by `hello`**.

> ⚠️ **Modern Java — `switch` can skip `break` altogether.**
> Since **Java 14** (JEP 361), an arrow-labeled `switch` (`case 0 -> ...`)
> never falls through — each arrow is its own self-contained branch, so
> `break` is not needed to stop fall-through the way it is above:
>
> ```java
> switch (x) {
>     case 0 -> System.out.println(0);
>     case 1 -> System.out.println(1);
>     default -> System.out.println("def");
> }
> ```
>
> `break` is still legal syntax inside an arrow-form `switch` statement —
> it just has nothing to stop, since arrow branches don't fall through
> anyway (verified: `case 0 -> { ...; break; }` compiles and runs
> identically with or without the `break`). And when `switch` is used as an
> *expression* that produces a value, `yield` takes over the job `break`
> used to do for value-returning switches. Video 026 covers arrow-switch
> and `yield` in full — the fall-through rule taught here is unchanged for
> the classic colon form, which is still what the OCJP exam and most
> legacy code use.

## 06:49 — Only three places for `break`

1. Inside **switch** — to stop fall-through
2. Inside **loops** — to end the loop on a condition
3. Inside **labeled blocks** — to end the block on a condition

Anywhere else, `break` is a **compile-time error**.

## 12:40 — `break` anywhere else is a compile-time error

Innocent-looking code:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        if (x == 10)
            break;   // CE: break outside switch or loop
        System.out.println("hello");
    }
}
```

The instinct is: `x == 10`, so `break` the `main` method, and `hello` never
prints. Wrong — there is no "break the method." To use `break` you need one
of a loop, a switch, or a labeled block; here there is none of the three, so
`javac` refuses: `break outside switch or loop`.

> ⚠️ **Modern Java — this is exactly the error you hit converting a
> loop's `break` into `Stream.forEach`.**
> Java 8 lambdas don't count as "inside a loop" for `break`/`continue`
> purposes — a lambda body compiles to its own method, not to loop body
> code:
>
> ```java
> import java.util.List;
>
> List.of(1, 2, 3, 4, 5).forEach(i -> {
>     if (i == 3) break;   // CE: break outside switch or loop
>     System.out.println(i);
> });
> ```
>
> This hits the identical `break outside switch or loop` diagnostic as the
> example above, even though there is visibly a loop-like traversal one
> line up the call chain — verified. `break`/`continue` only reach an
> *actual* enclosing `for`/`while`/`do-while`, and a lambda body is never
> one. Need early exit while iterating a stream? Keep a plain `for` loop,
> or reach for `Stream.anyMatch` / `takeWhile` (Java 9), or an `Iterator`.

## 16:41 — `continue`

Where can `break` go? Three places: switch, loops, labeled block. Does
`continue` get the same three? **No** — and this is the important loophole.
`continue` is never valid inside a `switch` on its own. First, its
functionality; then, where it's legal.

### 18:53 — What `continue` does, inside a loop

```java
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0)
        continue;
    System.out.println(i);
}
// prints 1 3 5 7 9
```

`i == 0`: `0 % 2 == 0` → `continue` — skip the rest of this iteration and go
straight to the next one. `i == 1`: condition false → print `1`. Same
pattern for `3 5 7 9`. `continue` means: **skip the current iteration,
continue with the next one.**

### 20:51 — Why not switch, why not a labeled block?

A `switch`'s matched branch runs exactly **once** — it isn't a loop, so
"skip this iteration and continue to the next one" has no next iteration to
mean anything. Same for a labeled block: it also runs once. So `continue` is
legal in exactly **one** place — loops. Anywhere else, compile-time error.

> ❗ **Correction — "you never use `continue` inside switch" is stated too
> broadly.**
> It's true that `continue` is meaningless when a `switch` is the *nearest*
> enclosing loop-or-switch construct with nothing wrapping it — standing
> directly inside a bare `switch` is a compile error, exactly like standing
> outside any loop at all. But `continue` always targets the nearest
> enclosing **loop**, not the nearest enclosing `switch`, so a `switch`
> nested inside a loop is no obstacle:
>
> ```java
> for (int i = 0; i < 10; i++) {
>     switch (i) {
>         case 5:
>             continue;      // continues the enclosing for loop
>         default:
>             System.out.println(i);
>     }
> }
> // prints 0 1 2 3 4 6 7 8 9
> ```
>
> This compiles and runs exactly as shown — verified; `i == 5` is skipped,
> every other value prints. The exam-safe version of the rule: `continue`
> cannot appear where the *only* thing wrapping it is a `switch`; it has no
> trouble reaching past a `switch` to an outer loop.

## 22:42 — `continue` only inside loops

```java
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0)
        continue;
    System.out.println(i);
}
// prints 1 3 5 7 9
```

Without an enclosing loop:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        if (x == 10)
            continue;   // CE: continue outside of loop
        System.out.println("hello");
    }
}
```

`javac` rejects this with `continue outside of loop` — verified.

## 27:26 — Labeled `break` and `continue`

In nested loops, a plain `break` or `continue` only ever acts on the
**innermost** loop. To act on an outer loop, label it:

```java
l1: for (...) {
    for (...) {
        break;       // breaks the innermost loop only
        // break l1;    // breaks the l1 loop; control resumes after l1
        // continue;    // continues the innermost loop
        // continue l1; // continues the l1 loop
    }
}
```

Labeled `break`/`continue` let you target **a specific loop in a nest**,
rather than always the closest one.

### 32:31 — Exam example: four variants, four different outputs

```java
class Test {
    public static void main(String[] args) {
        l1:
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (i == j)
                    break;   // swap this line per variant below
                System.out.println(i + "..." + j);
            }
        }
    }
}
```

This looks simple; most people still get it wrong. All four variants below
were compiled and run to confirm the output.

**1. Plain `break`** — breaks only the inner loop:

| `i` | `j` | `i == j`? | Action |
|---|---|---|---|
| 0 | 0 | yes | `break` inner, move to `i=1` |
| 1 | 0 | no | print `1...0` |
| 1 | 1 | yes | `break` inner, move to `i=2` |
| 2 | 0 | no | print `2...0` |
| 2 | 1 | no | print `2...1` |
| 2 | 2 | yes | `break` inner, `i=3` ends the outer loop |

```text
1...0
2...0
2...1
```

**2. `break l1`** — breaks straight out of both loops, no output at all:
`i=0, j=0` are equal immediately, `break l1` exits everything before a
single `println` runs.

**3. Plain `continue`** — continues the **inner** loop (skips just the
matching `j`, keeps looping `j`):

```text
0...1
0...2
1...0
1...2
2...0
2...1
```

**4. `continue l1`** — continues the **outer** loop (abandons the rest of
`j` for that `i` and jumps straight to the next `i`):

```text
1...0
2...0
2...1
```

## 41:55 — `do-while` versus `continue` — a dangerous combination

Take special care here for the exam — this is the trap.

```java
class Test {
    public static void main(String[] args) {
        int x = 0;
        do {
            x++;
            System.out.println(x);
            if (++x < 5)
                continue;
            x++;
            System.out.println(x);
        } while (++x < 10);
    }
}
```

The wrong instinct: `continue` inside a `do-while` jumps back to the top of
the `do` block, so it must skip the `while` test. **It does not.** `continue`
inside a `do-while` always jumps to the **condition check** — if that
condition is true, the body runs again from the top; there is nowhere else
for it to go.

Walk-through (`x` starts at `0`):

| Step | Expression | `x` after | Printed |
|---|---|---|---|
| `x++; println(x)` | | 1 | `1` |
| `if (++x < 5) continue` | `x` → 2, `2 < 5` true | 2 | |
| `while (++x < 10)` | `x` → 3, `3 < 10` true → body again | 3 | |
| `x++; println(x)` | | 4 | `4` |
| `if (++x < 5)` | `x` → 5, `5 < 5` false — falls through | 5 | |
| `x++; println(x)` | | 6 | `6` |
| `while (++x < 10)` | `x` → 7, true | 7 | |
| `x++; println(x)` | | 8 | `8` |
| `if (++x < 5)` | `x` → 9, false — falls through | 9 | |
| `x++; println(x)` | | 10 | `10` |
| `while (++x < 10)` | `x` → 11, `11 < 10` false → stop | 11 | |

```text
1
4
6
8
10
```

Compiled and run — output confirmed: **`1 4 6 8 10`**. Any answer of the
shape `1 2 3`, `1 3 5`, or `1 2 3 4 5 6` comes from assuming `continue`
restarts the loop body; it doesn't, in a `do-while`.

---

## Exam and interview points

1. **`break` has exactly three legal homes**: switch (stops fall-through),
   loops (ends the loop), labeled blocks (ends the block). Anywhere else:
   `break outside switch or loop`.
2. **`continue` has exactly one legal home**: loops. It is never valid
   directly inside a `switch` or a labeled block with nothing enclosing it —
   but a `switch` *nested inside a loop* is not a barrier, since `continue`
   always targets the nearest **loop**, not the nearest switch. Anywhere
   truly outside a loop: `continue outside of loop`.
3. **Labeled `break`/`continue` target a specific loop in a nest** —
   `break l1` exits that loop entirely; `continue l1` skips to that loop's
   next iteration. Unlabeled versions always act on the *innermost*
   enclosing loop or switch.
4. **The classic four-way exam trap**: given nested loops with
   `if (i == j)`, swapping `break` → `break l1` → `continue` →
   `continue l1` produces four completely different outputs. Trace each one
   by hand rather than guessing from the shape of the code.
5. **`continue` inside `do-while` jumps to the condition check, not to the
   top of the loop body.** This is the single most misjudged case in this
   lecture — verified output for the walkthrough example is `1 4 6 8 10`.
6. **Java 8 lambdas silently break this whole toolkit**: `break`/`continue`
   inside a `Stream.forEach` lambda are compile errors, because a lambda
   body is not a loop body — even one line below an obvious iteration.
7. **Java 14's arrow `switch`** never falls through, so `break` is no longer
   needed to stop it; `yield` replaces `break`'s old job of producing a
   value from a `switch` expression. See Video 026 for the full treatment.

**Next:** Video 030 — Java source file structure
