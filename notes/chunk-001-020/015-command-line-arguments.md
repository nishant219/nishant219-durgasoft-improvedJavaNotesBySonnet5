# Video 015 — Command Line Arguments

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-15|| Command Line Arguments

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 15 of 203 |
| Series | Language Fundamentals · Part 15 of 16 |
| Topic | Command line arguments (args array, java Test A B C, length, index, space as separator, String[] vs usage inside main) |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 38m 34s (2314 seconds) |
| Video ID | w9BrD4eanxQ |
| Watch | https://www.youtube.com/watch?v=w9BrD4eanxQ |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This follows directly on from the two `main()` lectures (Parts 13–14), which
covered the *signature* of `main`. This one covers the *argument* that
signature receives:

1. What a command line argument is, and what the JVM does with one
2. Reading values inside `main`: `args[0]`, `args[1]`, `args.length`
3. Java vs C: the class name is **not** `args[0]`
4. Why we need them at all — the lab-exam story and the file-merge story
5. Why the type is always `String[]`
6. **Case 1 (SCJP trap):** `i <= args.length` → `ArrayIndexOutOfBoundsException` on every run
7. **Case 2 (SCJP trap):** reassigning `args` to another array discards the command-line values
8. **Case 3 (SCJP trap):** `args[0] + args[1]` is concatenation, not addition
9. **Case 4:** space is the separator; double quotes make one argument out of several words

---

## 00:18 — What is a command line argument?

> The arguments which are passed from the command prompt are called command
> line arguments.

```text
java Test A B C
```

| Token | Meaning |
|---|---|
| `java` | the JVM launcher |
| `Test` | the class whose `main` will run |
| `A` | first command line argument |
| `B` | second command line argument |
| `C` | third command line argument |

`A`, `B`, `C` are arguments **to `main`**, not to the class name.

### 00:50 — What the JVM does with those tokens

Whenever you run `java Test A B C`, the JVM does three things, in order:

1. Creates one `String` array holding the tokens: `{"A", "B", "C"}`.
2. Passes that array as the argument to `main`.
3. Invokes `main`.

`main` never "reads the command prompt" itself — the JVM has already packaged
the tokens into a `String[]` before `main` starts running.

```text
java Test A B C
        │
        ▼
   JVM builds:  String[] { "A", "B", "C" }
        │
        ▼
   Test.main( that array )
```

### 02:11 — Reading the values inside `main`

```java
class Test {
    public static void main(String[] args) {
        // args[0], args[1], args[2]  and  args.length
    }
}
```

| Expression | Value for `java Test A B C` |
|---|---|
| `args[0]` | `"A"` |
| `args[1]` | `"B"` |
| `args[2]` | `"C"` |
| `args.length` | `3` — how many command line arguments were passed |

Indexing is **zero-based**; `length` is a count, not the last index. The last
valid index is always `args.length - 1`.

The parameter *name* on the board doesn't matter — Sir's board sometimes reads
as `ax` rather than `args` (an auto-caption artifact of the recording, not a
second identifier). What matters is the *type*: a one-dimensional `String`
array. You could legally name the parameter `x` or `argh`; the JVM still
passes the same array, and usage inside `main` is always index-into-array plus
`.length`.

A related interview question this lecture sets up: `main` can equally be
written with varargs syntax, `public static void main(String... args)`. It is
the same signature as far as the JVM is concerned — `String...` is just
`String[]` with call-site sugar — so `args[0]` and `args.length` behave
identically either way. Verified: both forms compile and run the same for
`java Test A B C`.

### 02:52 — Java vs C: `args[0]` is not the class name

Sir flags this as one small thing to be aware of if you already know C.

In **C**, the program name itself becomes the first command line argument —
`argv[0]` is the executable name, and the real user tokens start at `argv[1]`.

In **Java**, the first command line argument is the first token *after* the
class name. `Test` is never stored anywhere in `args`:

```text
java Test A B C
```

- `args[0]` is `"A"` — **not** `"Test"`.
- There is no extra slot reserved for the class name.

Coming from C and reaching for `args[1]` expecting `"A"` is already the wrong
index in Java.

> ⚠️ **Modern Java — `main` no longer has to look like this at all.**
> Everything above assumes the classic signature from Parts 13–14:
> `public static void main(String[] args)` inside an explicit class. Starting
> with **Java 11** (JEP 330) you can run a `.java` file directly —
> `java Test.java A B C` — without a separate `javac` step, though the class
> and the full signature were still required. **Java 25** (JEP 512, final,
> after previewing since 21) goes further: a top-level file needs no
> `class Test { }` wrapper, no `public`, no `static`, and — the part that
> matters for this lecture — **no `args` parameter at all if you don't use
> command line arguments**:
>
> ```java
> // Hello.java — compiles and runs with `java Hello.java`, no class needed
> void main() {
>     System.out.println("no args needed here");
> }
> ```
>
> ```java
> // Hello.java — declare args only when you actually read the command line
> void main(String[] args) {
>     System.out.println("first arg: " + args[0]);
>     System.out.println("count: " + args.length);
> }
> ```
> Both compiled and ran unchanged on JDK 26 for this note. The classic
> `class Test { public static void main(String[] args) { ... } }` form Sir
> teaches still compiles and still works exactly as described — this is an
> additional, simpler entry point for small programs, not a replacement.

---

## 05:31 — Why do we need them? The lab-exam story

Sir's setup: academic lab exams. Most students bring slips, pen drives, or a
Bluetooth transfer from a phone, and copy a dumped solution. Some "smart"
students skip the props but still cheat the intent: they write code that only
*looks* like it solves the problem.

Question on the slip: *write a program to find the square of a given number.*

**Wrong "smart" version — hardcoded:**

```java
class Test {
    public static void main(String[] args) {
        System.out.println("the square of 4 is 16");
    }
}
```

They stall until the last five minutes, then call the lecturer over. He types:

```text
java Test 4
```

Output looks perfect: `the square of 4 is 16`. But run it with a different
number and the illusion breaks:

```text
java Test 5   →   the square of 4 is 16   (still)
```

It is not a square program — it is a `println` program that only survives one
specific test.

**Correct version — read the number from the command line:**

```java
class Test {
    public static void main(String[] args) {
        int n = Integer.parseInt(args[0]);
        System.out.println("the square of " + n + " is " + (n * n));
    }
}
```

| Invocation | Output |
|---|---|
| `java Test 4` | `the square of 4 is 16` |
| `java Test 5` | `the square of 5 is 25` |

`args[0]` arrives as the **String** `"4"`, not the `int` `4`. `Integer.parseInt`
converts it, and only then does `n * n` do real arithmetic. That conversion —
and the fact the program now works for any number you pass — is the whole
point:

> The main objective of command line arguments is **customization of the
> `main` method**: you pass values, and based on those values `main` behaves
> differently.

### 12:05 — Same idea, different data: merging files

Sir's second story: a program that merges `a.txt` and `b.txt` into `c.txt`.
It works — until tomorrow the input is `x.txt` and `y.txt`, and the output
should go to `j.txt`. If the file names are hardcoded inside `main`, the
program is welded to the A/B/C files and has to be rewritten.

Fix: don't hardcode — take the names as arguments.

```java
// args[0] = first input file, args[1] = second input file, args[2] = output file
// java Test a.txt b.txt c.txt
// java Test x.txt y.txt j.txt
```

Same compiled class, any file names, no recompilation. Passing arguments is
not compulsory, though — if `main` has nothing that needs to vary per run,
hardcoding is fine. Command line arguments are the tool for when the
interesting part of `main` should change between runs.

### 15:11 — Why is the type always `String[]`?

Sir gives two reasons the language designers picked `String` over, say,
`int[]` or `double[]`.

**Reason 1 — String is (by Sir's estimate) the most-used type in Java code**,
roughly 70% String objects to 30% everything else. That ratio isn't a
documented language statistic — it's Sir's teaching shorthand for "you'll use
String far more than any other type" — but the conclusion holds regardless of
the exact number.

**Reason 2 — from a String you can convert to anything else.** String → number
(`Integer.parseInt`), String → boolean, String → whatever you need. Had `main`
taken `int[]`, you could never pass a file name through it. Because it takes
`String[]`, you can pass `"4"` and parse it, `"true"` and parse it, or
`"a.txt"` and use it as-is.

In the square example the value passed *looks* like a number, but it arrives
as a String; converting is always your job, never the JVM's.

---

## 17:37 — Case 1: `<=` vs `<` (SCJP trap)

```java
class Test {
    public static void main(String[] args) {
        for (int i = 0; i <= args.length; i++) {   // BUG: should be i < args.length
            System.out.println(args[i]);
        }
    }
}
```

| # | Command | Guess | Actual result |
|---|---|---|---|
| 1 | `java Test A B C` | prints `A B C` | prints `A`, `B`, `C`, then `ArrayIndexOutOfBoundsException` |
| 2 | `java Test A B` | prints `A B` | prints `A`, `B`, then `ArrayIndexOutOfBoundsException` |
| 3 | `java Test` (no args) | no output | `ArrayIndexOutOfBoundsException` immediately |

Verified by compiling and running: all three throw. Walking through invocation
1 — `args.length` is `3`, and the loop condition is `i <= 3`:

- `i = 0, 1, 2` → prints `args[0]`, `args[1]`, `args[2]` → `A`, `B`, `C`
- `i = 3` → `3 <= 3` is **true**, so the body runs once more → `args[3]`
- There is no index `3`; valid indexes are only `0, 1, 2` → `ArrayIndexOutOfBoundsException`

Invocation 2 (`java Test A B`) runs the same walkthrough one step shorter:
`args.length` is `2`, so the loop prints `args[0]` and `args[1]` (`A`, `B`),
then `i = 2` satisfies `2 <= 2` and `args[2]` doesn't exist — same exception,
different index in the message.

Invocation 3 (`java Test`, no arguments at all) is the case people get wrong
most often: **`args` is never `null`** — it is a zero-length array. `length`
is `0`, the condition `0 <= 0` is true, and `args[0]` fails before printing
anything.

**Fix — `<` instead of `<=`:**

```java
for (int i = 0; i < args.length; i++) {
    System.out.println(args[i]);
}
```

| Command | Output |
|---|---|
| `java Test A B C` | `A` / `B` / `C` |
| `java Test A B` | `A` / `B` |
| `java Test` | no output — loop body never runs |

The exam point Sir wants kept: know `<` vs `<=` against `args.length` cold —
it's a realistic SCJP question, and the failure mode is a runtime exception,
not "wrong output."

---

## 25:45 — Case 2: reassigning `args` (SCJP trap)

Sir calls this one out specifically as important for the exam.

```java
class Test {
    public static void main(String[] args) {
        String[] argh = {"X", "Y", "Z"};
        args = argh;
        for (String s : args) {
            System.out.println(s);
        }
    }
}
```

`args` and `argh` are both `String[]`, so `args = argh;` is a legal reference
assignment. From that line on, `args` points at `{"X", "Y", "Z"}` — the array
the JVM originally built from the command line is simply abandoned (eligible
for GC; nothing in `main` still refers to it).

Verified by compiling and running with three different invocations — the
output is identical every time:

```text
java Test A B C
java Test A
java Test
```

```text
X
Y
Z
```

...regardless of whether you passed any command line arguments at all. The
for-each loop always walks whatever `args` *currently* points to, not what it
originally pointed to.

**Exam takeaway:** `args` is an ordinary local parameter — a reference you're
free to re-point. Command line arguments are only what the JVM initially
assigns to it; reassign `args` and `main` stops looking at the command line
from that point on.

---

## 31:02 — Case 3: `args[0] + args[1]` is concatenation, not addition

```java
class Test {
    public static void main(String[] args) {
        System.out.println(args[0] + args[1]);
    }
}
```

```text
java Test 10 20
```

The trap: most people answer `30`. The verified answer is `1020`.

> Within `main`, command line arguments are available in String form.

`args[0]` is the String `"10"`, `args[1]` is the String `"20"`, and `+`
between two Strings is concatenation — `"10" + "20"` is `"1020"` — not
arithmetic, because no arithmetic ever happens unless you convert first.

**If you want actual addition:**

```java
int n1 = Integer.parseInt(args[0]);
int n2 = Integer.parseInt(args[1]);
System.out.println(n1 + n2);   // 30
```

Same two tokens, `10` and `20` — but parsed into `int` first, `+` becomes
arithmetic, and the result is `30`.

---

## 34:18 — Case 4: space is the separator; quotes glue words into one argument

```java
class Test {
    public static void main(String[] args) {
        System.out.println(args[0]);
    }
}
```

```text
java Test note book
```

`args[0]` is `"note"` — space splits tokens, so `note` is the first argument
and `book` is a separate second argument (`args[1]`), not part of the first.

To make the whole phrase `note book` land in `args[0]` as one argument,
enclose it in double quotes:

```text
java Test "note book"
```

Now there is exactly one command line argument. `args[0]` is `"note book"`
and `args.length` is `1`. Verified both ways by compiling and running.

> Usually space itself is the separator between command line arguments. If a
> command line argument itself contains a space, enclose it in double quotes.

---

## `String[]` vs usage inside `main`

A compact reference pulling the four cases together:

| Piece | Meaning |
|---|---|
| `String[]` | the type of `main`'s parameter — always an array of Strings |
| Parameter name (`args`, `x`, …) | just a local name; the JVM doesn't care what you call it |
| `args.length` | how many tokens were passed — `0` if you typed only `java Test` |
| `args[i]` | the *i*-th token, as a String, even if it looks like a number |
| Empty invocation | `args` is a length-0 array, never `null` |
| `+` on two slots | concatenation, not arithmetic |
| Need a number | `Integer.parseInt(args[i])` (or the matching wrapper method) |
| Need a space inside one token | wrap it in `"double quotes"` on the command line |

The declaration `String[] args` is the contract; everything else in this
lecture — indexing, length, parsing, never assuming `args` still points at the
JVM's original array once you've reassigned it — is usage.

## Exam and interview points

1. **`java Test A B C` → `args[0]` is `"A"`, never `"Test"`.** Unlike C's
   `argv[0]`, Java never stores the class name in `args`.
2. **`args` is never `null`** — running with zero command line arguments gives
   a zero-length array, so `args.length` is `0`, not a `NullPointerException`.
3. **`i <= args.length` in a loop always overruns by one** and throws
   `ArrayIndexOutOfBoundsException` — verified on every one of three
   invocations, including the zero-argument case, which fails on the very
   first line.
4. **Reassigning `args` inside `main` is legal** and silently discards the
   command-line values for the rest of the method — verified: the same
   for-each output prints for every invocation once `args = argh;` runs.
5. **`args[0] + args[1]` concatenates**, because command line arguments are
   always Strings inside `main`. `"10" + "20"` is `"1020"`; only
   `Integer.parseInt` (or similar) followed by `+` gives `30`.
6. **Space separates arguments; double quotes make one argument** out of a
   phrase that contains spaces.
7. **The objective of command line arguments is customizing `main`'s
   behavior** at launch time, not passing the class name and not compulsory
   when nothing needs to vary between runs.
8. **`main`'s parameter is `String[]` because String converts to anything**,
   not because of some fixed rule about ratios — the exact "70% String"
   figure is Sir's teaching estimate, not a specification.
9. **Since Java 25** (JEP 512, previewed from 21), a top-level `.java` file no
   longer needs a wrapping class or `public static`, and the `args`
   parameter itself is optional if the program never reads the command line
   — the classic signature this lecture teaches is still exactly what you
   write the moment you *do* need arguments.

---

**Next:** Video 016 — Java Coding Standards
