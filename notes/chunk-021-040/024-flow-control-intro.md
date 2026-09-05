# Video 024 — Flow-Control introduction

## Video info

**Title:** Core Java with OCJP/SCJP: Flow-Control Part-1  || Introduction

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 24 of 203 |
| Series | Flow-Control · Part 1 of 6 |
| Topic | What flow control is; selection / iterative / transfer map |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 10m 25s (625 seconds) |
| Video ID | X6rS9vD9-qM |
| Watch | https://www.youtube.com/watch?v=X6rS9vD9-qM |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Meaning of flow control: at **run time**, **in which order** statements execute.
2. Spoken sketches of `if`/`else` and of a loop.
3. All flow-control statements divided into **three** categories (he draws the diagram).
4. Selection: `if-else`, `switch`.
5. Iterative: `while`, `do-while`, `for`, `for-each` (came in **1.5**).
6. Transfer: `break`, `continue`, `return`, `try-catch-finally`, `assert` (came in **1.4**).
7. In **this class** he will explain up to **break and continue**. `assert` → assertions chapter. `try-catch-finally` and `return` → exception handling.
8. Dictated definition + the same diagram again. Next videos: **postmortem** on each statement; basics, but several loopholes waiting.

## Detailed notes

### 00:08 — Keep copying: Flow control

Board heading: **flow control**. A very basic concept, he says, but there are several new things waiting in it even so.

### 00:31 — What is flow control / control flow?

Students routinely show up with 20–30 lines of code and ask "sir, can you explain the flow?" His answer is the definition itself:

**What is flow control?** At **run time**, in which **order** the statements are going to **execute** — that order is decided by flow control.

### 01:09 — `if` — JVM checks true or false

Suppose an `if` statement is there. Immediately the **JVM** checks: is the condition true or false?

- If **true** → execute the if-part.
- If **false** → skip the if-part, control goes straight to the **else** part.

```java
int x = 10;
if (x > 5) {
    System.out.println("if-part");     // JVM: condition true → executes this part
} else {
    System.out.println("else-part");   // condition false → control comes here instead
}
```

### 01:30 — Loop — keep executing until the condition fails

A loop keeps executing **until the condition fails**. Once it fails, control comes out automatically.

```java
int i = 0;
while (i < 3) {
    System.out.println(i);   // keeps executing until the condition fails
    i++;
} // condition failed → control comes out here
```

So: in which order the statements are going to be executed is decided by flow control.

### 01:51 — How many flow-control statements? Three categories

All flow-control statements are divided into three categories.

### 02:14 — 1. Selection statements

When several alternatives are there, **one** of them is selected and executed — that is a selection statement.

**First:** `if-else`. Only **two** options are available — the if-part or the else-part.

```java
if (condition) {
    // option 1 — if-part
} else {
    // option 2 — else-part
}
```

**Second:** `switch`. Several options are there; **one case** is selected and that case is executed.

```java
switch (x) {
    case 1:
        break;   // one case selected and executed
    case 2:
        break;
    default:
        break;
}
```

In Java, how many selection statements are there? **`if-else` and `switch`.** Only those two.

> ⚠️ **Modern Java — `switch` gained a second form.**
> Since **Java 14** (JEP 361), `switch` can also be an **expression** that
> produces a value, using arrow (`->`) labels with no fall-through, and since
> **Java 21** (JEP 441) a `case` label can be a **type pattern** with an
> optional `when` guard:
>
> ```java
> String kind = switch (x) {          // switch EXPRESSION, not statement
>     case 1, 7 -> "weekend";
>     case 2, 3, 4, 5, 6 -> "weekday";
>     default -> "invalid";
> };
>
> Object o = 5;
> String desc = switch (o) {          // pattern matching for switch (21)
>     case Integer i when i > 0 -> "positive int " + i;
>     case Integer i -> "non-positive int " + i;
>     case String s -> "string " + s;
>     default -> "other";
> };
> ```
>
> The classic statement form Sir teaches here is still exactly correct and is
> still what the OCJP exam (and most legacy code) uses. "Selection: `if-else`
> and `switch`, only those two" still holds — `switch` just does more now.

### 03:25 — 2. Iterative statements

Statements executed **repeatedly / iteratively** — he stresses the word is **iterative**, not "irritative."

1. `while` loop
2. `do-while`
3. `for` loop
4. `for-each` loop

```java
int n = 3;
while (n > 0) { n--; }

do { n++; } while (n < 3);

for (int i = 0; i < n; i++) { }

int[] arr = {1, 2, 3};
for (int e : arr) { }   // for-each
```

**`for-each` is the new loop which came in the 1.5 version.**

### 04:28 — 3. Transfer statements

Last category: to **transfer control from one place to another**.

Best example: he is in a `while` loop; `break` appears in the middle; control is immediately transferred **outside the loop**.

```java
int i = 0;
while (i < 5) {
    if (i == 3) break;   // control transferred outside the loop
    i++;
}
```

How many transfer statements are there?

**First:** `break`. **Second:** `continue`. **Third:** `return`.

```java
break;     // transfer out of a loop / switch
continue;  // transfer to the next iteration
return;    // transfer out of the method
```

### 05:24 — `try-catch-finally` is also a transfer statement

`try-catch-finally` is **also a transfer statement only**, he says — because if an exception is raised inside the `try` block, control is **transferred to the catch block**; if that catch is **not matching**, control is transferred on to the **finally** block.

```java
try {
    throw new RuntimeException("boom");   // exception raised → control transfers to catch
} catch (RuntimeException e) {
    System.out.println("caught: " + e.getMessage());
} finally {
    System.out.println("finally runs");   // reached whether or not catch matched
}
```

> ⚠️ **Modern Java — the `try` he's about to teach in exception handling gained two new forms.**
> **Java 7** added **multi-catch** (one `catch` for several unrelated exception
> types) and **try-with-resources** (a resource declared in the `try(...)`
> header is closed automatically); **Java 9** relaxed try-with-resources so an
> **effectively-final** existing variable can be used directly, no re-declaration
> needed:
>
> ```java
> try (var sr = new java.io.StringReader("hi")) {   // Java 7 try-with-resources
>     System.out.println((char) sr.read());
> } catch (IllegalStateException | IllegalArgumentException e) {  // Java 7 multi-catch
>     System.out.println(e.getMessage());
> }
>
> java.io.StringReader sr2 = new java.io.StringReader("hi");
> try (sr2) {   // Java 9: effectively-final variable, no re-declaration
>     System.out.println((char) sr2.read());
> }
> ```
>
> None of this changes what Sir is teaching *here* — this video only classifies
> `try-catch-finally` as a transfer statement, and that classification is
> untouched. The full mechanics wait for the exception-handling chapter, same
> as he says below.

### 06:14 — `assert` is also a transfer statement (1.4)

Fifth one: `assert`. If its condition fails, the program is stopped by raising `AssertionError` — this is covered properly in the assertions chapter.

```java
int x = 10;
assert x > 100 : "x too small";
```

> ❗ **Correction — assertions do not run "immediately" by default.**
> `assert` statements are **disabled at run time unless the JVM is started
> with `-ea`** (`-enableassertions`), a rule unchanged since Java 1.4. Without
> that flag the line above is a no-op; with it, it throws `AssertionError:
> x too small` and the program terminates (unless something catches
> `AssertionError`, which is rarely correct to do). Sir's "if this condition
> fails the program will be stopped" is the *intended* behaviour once
> assertions are switched on — worth remembering because forgetting `-ea` is
> exactly why a broken `assert` can silently do nothing in production.

These are the various transfer statements: `break`, `continue`, `return`, `try-catch-finally`, `assert`.

### 06:41 — What he will explain in this class vs later chapters

- **`assert`** → the assertions concept.
- **`try-catch-finally`** and **`return`** → exception handling.
- **In this class**, up to `break` and `continue`.

Recap of the three categories:

1. **Selection statement** — among several options, one is selected and executed.
2. **Iterative statement** — a group of statements executed iteratively. Four of them: `while`, `do-while`, `for`, `for-each`.
3. **Transfer statement** — control moves from one place to another: `break`, `continue`, `return`, and the rest on the diagram.

### 07:31 — Board sentence (dictation)

He repeats it until the class copies it down:

> **Flow control describes the order in which the statements will be executed at run time.**

### 08:13 — Same diagram again (copy it directly)

Better to keep this diagram directly. Three types of flow-control statements:

**First — selection statements.** Among several options, one is selected and executed.

**Second — iterative statements.** `while`, `do-while`, `for`, `for-each`. **`for-each` came in the 1.5 version.**

**Third — transfer statements.** `break`, `continue`, `return`, `try-catch-finally`, `assert`. **`assert` came in the 1.4 version.**

```java
// selection
if (condition) { } else { }
switch (x) { case 1: break; }

// iterative (for-each: 1.5)
while (condition) { }
do { } while (condition);
for (;;) { }
for (int e : arr) { }

// transfer (assert: 1.4)
break;
continue;
return;
try { } catch (Exception e) { } finally { }
assert condition;
```

That's all for the map. Now they perform **postmortem** on each of these — very basic, but with several loopholes waiting.

He recites the transfer list once more at the end: `break`, `continue`, `return`, `try-catch-finally`, `assert`. Completed.

## Rules (as he states them)

1. Flow control = order of statement execution at run time.
2. **Three** boxes only: selection, iterative, transfer — not a fourth top-level box for exceptions.
3. Selection in Java: only `if-else` (two options) and `switch` (several cases, one selected).
4. Iterative: four — `while`, `do-while`, `for`, `for-each` (**1.5**).
5. Transfer: `break`, `continue`, `return`, `try-catch-finally`, `assert` (**1.4**).
6. `break` in the middle of a loop transfers control **outside** the loop.
7. Exception in `try` → control to `catch`; if catch does not match → `finally`.
8. Failed `assert` (with assertions enabled) → program stopped by raising `AssertionError`.
9. This class's scope: **break and continue**. `assert` later (assertions). `try-catch-finally` and `return` later (exception handling).

## Exam / interview traps (from this lecture)

- **`for-each` is 1.5**, not "always existed."
- **`assert` is 1.4** and sits in his **transfer** list, not in a separate "assertions" box on this diagram.
- **`assert` is disabled by default** — the exam loves testing whether you remember `-ea` is required.
- **`try-catch-finally` is classified here as transfer**, not as a fourth top-level category — this is Sir's teaching classification, useful for the exam, though the JLS itself only names `break`/`continue`/`return`/`throw` as the statements that cause abrupt completion.
- Iterative, **not** "irritative" — he corrects the pronunciation on purpose.
- Students asking "explain the flow" of 20–30 lines: the answer is this map, not a mystery.

## Exam and interview points

1. **Three categories only**: selection, iterative, transfer — memorise the map before the postmortem videos start filling in loopholes.
2. **Selection = `if-else` + `switch`**, nothing else. `switch` gained an expression form (14) and pattern matching (21), but it is still one of exactly two selection statements.
3. **Iterative = four**: `while`, `do-while`, `for`, `for-each` — `for-each` is version **1.5**, a favourite exam date to misremember.
4. **Transfer = `break`, `continue`, `return`, `try-catch-finally`, `assert`** — `assert` is version **1.4**.
5. **`assert` only fires with `-ea`.** Without it, every `assert` in the program is a no-op — a very common gotcha in both the exam and real deployments.
6. **This video is scope-setting only.** `break`/`continue` come next in this course's sequence; `assert`, `try-catch-finally`, and `return` are deliberately deferred to their own chapters.

**Next:** Video 025 — Selection statements: if-else
