# Video 007 — Arrays part 2

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-7 || Arrays part-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 7 of 203 |
| Series | Language Fundamentals · Part 7 of 16 |
| Topic | Arrays part 2 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 48m 20s (2900 seconds) |
| Video ID | Qtw3nVWqf-w |
| Watch | https://www.youtube.com/watch?v=Qtw3nVWqf-w |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Continues the arrays agenda from video 006, moving from 1-D creation into
multi-dimensional arrays:

1. Two- and three-dimensional array **creation** — not a C/C++ matrix, an
   **array of arrays**
2. Exam drill: which of ten `new` expressions are valid
3. **Array initialization** — default values, printing a reference vs.
   printing an element
4. The `new int[2][]` case: a 1-D reference that stays `null`, and the
   `NullPointerException` that follows from using it
5. Overriding default values with customized ones
6. Out-of-range index (`ArrayIndexOutOfBoundsException`) vs. a non-`int`
   index (compile-time error)

The `{10, 20, 30}` shortcut, `length` vs `length()`, anonymous arrays, and
array **element** assignment are video 008's material, not this one's.

---

## 00:06 — Two-dimensional creation: not a matrix

Video 006 finished one-dimensional creation. Now: how to create
two-dimensional and three-dimensional arrays.

In C and C++ a two-dimensional array is called a **matrix** — a group of
rows and columns, first row/second row, first column/second column. Sir's
point is that this word does not carry over cleanly to Java, and forcing a
matrix shape onto real data wastes memory.

### 01:21 — Why a matrix wastes memory: the supplementary-marks example

Sir's example: four students' **supplementary** (not regular) marks, out of
100 per subject.

| Student | Marks | Subject count |
|---|---|---|
| S1 | 10, 12, 07, 09, 15 | 5 |
| S2 | 28, 67 | 2 |
| S3 | 80 | 1 |
| S4 | 40, 50, 28 | 3 |

Store this as a 4×5 **matrix** and only S1 fills every cell: S2 wastes 3
slots, S3 wastes 4, S4 wastes 2. Going for arrays at all is already a memory
trade-off (fixed size decided up front); stacking a matrix shape on top of
mismatched row lengths wastes even more.

### 03:16 — Java's approach: array of arrays

Java did not implement multi-dimensional arrays in matrix style. It follows
a different memory approach: **array of arrays** (and for 3-D, array of
array of arrays). Same four students, in Java:

- base array size **4** — one slot per student
- S1's slot → a 1-D array of size **5** → `{10, 12, 07, 09, 15}`
- S2's slot → size **2** → `{28, 67}`
- S3's slot → size **1** → `{80}`
- S4's slot → size **3** → `{40, 50, 28}`

Each slot of the base array is itself an array, and the inner lengths need
not match. No wasted cells.

> **Board:** In Java, two-dimensional arrays are not implemented using
> matrix style. Some people followed the array-of-arrays approach for
> multi-dimensional array creation. Main advantage of this approach: memory
> utilization will be improved.

A 2-D array is an array where each element is itself an array. A 3-D array
adds one more level: an array of array of arrays.

---

## 07:40 — Example 1: writing the Java for a jagged 2-D array

Memory structure Sir draws: base size **2**; first element a 1-D array of
size **2**; second element a 1-D array of size **3**. Overall dimension: 2
(array of arrays).

```java
int[][] x = new int[2][];   // base size fixed at 2; next-level size varies, so leave it
x[0] = new int[2];
x[1] = new int[3];
```

**At least the base size must be specified** in that `new`. The remaining
sizes are not required there — if the next level is sometimes 2 and
sometimes 3, it is not fixed, so leave it and fill it in on later lines.

## 10:43 — Example 2: writing the Java for a jagged 3-D array

Memory structure: base size **2** ("two wings"). First wing: a 2-D array
whose base size is **3**, with innermost arrays of size **1**, **2**, and
**3** (not fixed). Second wing: a 2-D array whose base size is **2**, where
**every** innermost array has size **2** (fixed). Dimension: array of array
of arrays → 3-D.

```java
int[][][] x = new int[2][][];   // only the base size, 2, is fixed

x[0] = new int[3][];            // first wing: 2-D, base 3, inner sizes vary
x[0][0] = new int[1];
x[0][1] = new int[2];
x[0][2] = new int[3];

x[1] = new int[2][2];           // second wing: inner size is always 2, so fix it here
```

The rule to internalise while writing this:

- Specify sizes from the **left** (the base) as far as they are **fixed**.
- If a later size **varies**, omit it in that `new` and assign the inner
  arrays on later lines.
- If a later size is **always the same**, you may specify it in the same
  `new` (`new int[2][2]`).

### 17:09 — Exam drill: which of ten array creations are valid?

Ten lines. The pattern: **you may omit trailing sizes, but you must never
skip a size and then specify a later one.** At least the **base** size is
always required.

| # | Code | Valid? | Why |
|---|---|---|---|
| 1 | `int[] a = new int[];` | ❌ no | at least the base size must be specified |
| 2 | `int[] a = new int[3];` | ✅ yes | base size given |
| 3 | `int[][] a = new int[][];` | ❌ no | at least the base size must be specified |
| 4 | `int[][] a = new int[3][];` | ✅ yes | base given; second dimension left for later |
| 5 | `int[][] a = new int[][4];` | ❌ no | can't specify a later size without the base |
| 6 | `int[][] a = new int[3][4];` | ✅ yes | both sizes given |
| 7 | `int[][][] a = new int[3][4][5];` | ✅ yes | all three sizes given |
| 8 | `int[][][] a = new int[3][4][];` | ✅ yes | first two given; last left open |
| 9 | `int[][][] a = new int[3][][5];` | ❌ no | second dimension skipped, third specified |
| 10 | `int[][][] a = new int[][4][5];` | ❌ no | first (base) dimension skipped |

All ten verified against `javac` on JDK 26 — every "no" row is a
`array dimension missing` or `']' expected` compile error, exactly as Sir
predicts. Recite the key: **1 invalid, 2 valid, 3 invalid, 4 valid, 5
invalid, 6 valid, 7 valid, 8 valid, 9 and 10 invalid.**

That closes array creation. 1-D loopholes (size compulsory, zero legal,
negative size, allowed size types, max size) were video 006's territory;
this drill is the 2-D/3-D `new` rules layered on top of them.

---

## 21:35 — Array initialization

### 21:51 — Example 1: printing a reference vs. printing an element

```java
int[] x = new int[3];
System.out.println(x);      // [I@d0c6   (your hex will differ)
System.out.println(x[0]);   // 0
```

`x` is a **reference variable**. Whenever you print a reference variable,
`toString()` is called internally — and the default `Object.toString()`
returns `classname@hashcode_in_hexadecimal`. For `int[]` the class name is
`[I` (that language-level naming was covered in video 006), so the output
looks like `[I@d0c6`. The hex digits are **not fixed** — they vary from run
to run and machine to machine; do not memorise the number, only the shape.

Once you create an array, **every element is default-initialized**. For
`int` that default is `0`, so `x[0]` prints `0`.

> **Board:** Once we create an array, every array element is by default
> initialized with default values.

### 26:13 — Note: printing any reference calls `toString()`

> Whenever we try to print any reference variable, internally `toString()`
> will be called, which is implemented by default to return the string in
> the form **`classname@hashcode_in_hexadecimal`**.

Arrays prove the rule because every array is an object (video 006). The
`java.lang.Object` mechanics behind `toString()` are covered properly later
in the course.

### 28:06 — Example 2: a fully sized 2-D array

```java
int[][] x = new int[2][3];
System.out.println(x);
System.out.println(x[0]);
System.out.println(x[0][0]);
```

| Expression | What it is | Output |
|---|---|---|
| `x` | reference to the 2-D array object | `[[I@…` |
| `x[0]` | reference to a 1-D array object (this row does exist) | `[I@…` |
| `x[0][0]` | an `int` element | `0` (default) |

Terminology to recite: `x` is a two-dimensional array reference, `x[0]` is a
one-dimensional array reference, and `x[0][0]` is `0`. Every inner `int` is
default `0`; the inner array objects exist because the second dimension was
specified in the same `new`.

### 33:25 — Example 3: only the base size specified — `null`, then `NullPointerException`

Same shape, one change: drop the second dimension.

```java
int[][] x = new int[2][];
System.out.println(x);         // [[I@…    — x is still a 2-D array object
System.out.println(x[0]);      // null     — no 1-D object was ever created for this slot
System.out.println(x[0][0]);   // NullPointerException
```

Base size is still 2, so `x` still prints `[[I@…`. But the next-level size
was never specified, so each slot of `x` is supposed to point at a 1-D array
object — and no such object exists. The default value of an **object
reference** is `null`, so `x[0]` prints `null`.

`x[0][0]` means "take `null` and ask for its first element." You cannot
perform any operation on `null`; the JVM throws a runtime
`NullPointerException`.

> **Board:** If we try to perform any operation on `null`, we will get a
> runtime exception saying `NullPointerException`.

> ⚠️ **Modern Java — the `NullPointerException` message got specific in Java 14.**
> The classic exception here carries no detail at all — you have to reason
> out for yourself that `x[0]` was the `null` in question. **JEP 358**
> ("Helpful NullPointerExceptions", opt-in in 14, default from **Java 15**)
> names the exact failing expression:
>
> ```text
> Exception in thread "main" java.lang.NullPointerException:
>     Cannot load from int array because "x[0]" is null
>         at Test.main(Test.java:4)
> ```
>
> Verified on JDK 26, compiled with debug info (`javac -g`) — that is the
> literal text `x[0][0]` throws today. The underlying rule Sir teaches is
> unchanged: indexing through a `null` reference is still a runtime
> `NullPointerException`. Only the diagnostic improved.

### 38:40 — Overriding default values

```java
int[] x = new int[6];   // size 6; every element defaults to 0
```

If you are not satisfied with the defaults, override them with customized
values:

```java
x[0] = 10;
x[1] = 20;
x[2] = 30;
x[3] = 40;
x[4] = 50;
x[5] = 60;
```

> **Board:** Once we create an array, every array element is by default
> initialized with default values. If we are not satisfied with the default
> values, then we can override these values with our customized values.

### 42:35 — Out-of-range index vs. an illegal index type

Valid indexes for size 6 are **0 to 5**.

```java
int[] w = new int[6];
w[6] = 70;     // runtime: ArrayIndexOutOfBoundsException
w[-6] = 80;    // runtime: ArrayIndexOutOfBoundsException  — same, still out of range
w[2.5] = 90;   // compile-time error, not runtime
```

`w[6]` and `w[-6]`: whether +6 or −6, both fall outside the valid range 0…5,
and both throw the same runtime `ArrayIndexOutOfBoundsException` — the sign
of an out-of-range index does not change which exception you get.

`w[2.5]`: the **compiler** checks only whether the index is a valid `int`
value. Plus/minus and in-range/out-of-range are the **JVM**'s job, decided at
run time. `2.5` is a `double`, not an `int`, so this fails as a syntactical
mistake, at compile time:

```java
error: incompatible types: possible lossy conversion from double to int
```

A logical mistake (a wrong index that is still an `int`) fails at run time.
A syntactical mistake (an index that is not an `int` at all) fails at
compile time.

> **Board:** If we try to access an array element with an out-of-range index
> (either a positive or a negative `int` value), we will get a runtime
> exception saying `ArrayIndexOutOfBoundsException`.

> ⚠️ **Modern Java — the compiler's wording for this changed by Java 7.**
> Sir dictates the Java 6-era message, "possible loss of precision / found:
> double / required: int." `javac` on any JDK you will actually use today
> (verified here on JDK 26) prints the compressed one-line form instead:
>
> ```text
> error: incompatible types: possible lossy conversion from double to int
> ```
>
> Same defect, same cause — a `double` cannot narrow to an `int` index
> without an explicit cast. Only the message layout changed. (Video 005 covers
> the same wording change for `char` narrowing, in more depth.)

---

## Complete program from the lecture

```java
class Test {
    public static void main(String[] args) {
        // Example 1 — jagged 2-D
        int[][] x2 = new int[2][];
        x2[0] = new int[2];
        x2[1] = new int[3];

        // Example 2 — jagged 3-D
        int[][][] x3 = new int[2][][];
        x3[0] = new int[3][];
        x3[0][0] = new int[1];
        x3[0][1] = new int[2];
        x3[0][2] = new int[3];
        x3[1] = new int[2][2];

        // Exam drill — the ten new-expressions (invalid ones commented out)
        // int[] a = new int[];               // CE: array dimension missing
        int[] a = new int[3];                 // OK
        // int[][] b = new int[][];           // CE: array dimension missing
        int[][] b = new int[3][];             // OK
        // int[][] c = new int[][4];          // CE: ']' expected
        int[][] d = new int[3][4];            // OK
        int[][][] e = new int[3][4][5];       // OK
        int[][][] f = new int[3][4][];        // OK
        // int[][][] g = new int[3][][5];     // CE: ']' expected
        // int[][][] h = new int[][4][5];     // CE: ']' expected

        // Initialization — Example 1
        int[] x = new int[3];
        System.out.println(x);       // [I@<hex>
        System.out.println(x[0]);    // 0

        // Initialization — Example 2
        int[][] y = new int[2][3];
        System.out.println(y);          // [[I@<hex>
        System.out.println(y[0]);       // [I@<hex>
        System.out.println(y[0][0]);    // 0

        // Initialization — Example 3
        int[][] z = new int[2][];
        System.out.println(z);          // [[I@<hex>
        System.out.println(z[0]);       // null
        // System.out.println(z[0][0]); // RE: NullPointerException
        //     "Cannot load from int array because "z[0]" is null" (JDK 14+)

        // Overriding default values
        int[] w = new int[6];
        w[0] = 10; w[1] = 20; w[2] = 30;
        w[3] = 40; w[4] = 50; w[5] = 60;
        // w[6] = 70;     // RE: ArrayIndexOutOfBoundsException
        // w[-6] = 80;    // RE: ArrayIndexOutOfBoundsException
        // w[2.5] = 90;   // CE: incompatible types: possible lossy conversion from double to int
    }
}
```

Every line above (including every commented-out one) was compiled against
JDK 26 while writing this note; the messages shown are the real ones, not
recollections.

---

## Exam and interview points

1. **Java arrays are not matrices.** A 2-D array is an **array of arrays**;
   inner rows can have different lengths, and that is the whole memory
   advantage over the C-style matrix layout.
2. **3-D is array of array of arrays** — one more level of indirection than
   2-D, no new concept.
3. In a `new` expression, **specify sizes left to right as far as they are
   fixed; the base size is always required.** `new int[3][]` and
   `new int[3][4][]` are valid. `new int[][4]`, `new int[3][][5]`, and
   `new int[][4][5]` are all invalid — you cannot skip a dimension and then
   fill a later one.
4. **`new int[3][]` is valid; `new int[][3]` is invalid.** This pair is the
   most commonly asked variant of the rule.
5. **`new int[3][][5]` is invalid even though the base (3) is present** —
   the missing dimension is in the middle, and that is enough to fail.
6. **Creating an array default-initializes every element**: `int` → `0`,
   any reference type → `null`.
7. **Printing a reference variable calls `toString()`**, which by default
   returns `classname@hashCode-in-hex`. For arrays that is `[I@…` (1-D
   `int[]`) or `[[I@…` (2-D `int[]`). The hex digits are not fixed —
   never memorise them.
8. **`x` is a 2-D reference, `x[0]` is a 1-D reference, `x[0][0]` is the
   `int` element** (or a `NullPointerException` if `x[0]` is `null`).
   `println(x)` never prints the elements themselves.
9. **`new int[2][]` leaves every `x[i]` as `null`.** Accessing `x[0][0]`
   after that is a runtime `NullPointerException`, not an
   `ArrayIndexOutOfBoundsException` — do not confuse the two.
10. **Default values can be overridden** with ordinary assignment,
    `x[i] = value`; nothing special is required.
11. **Index must be an `int`** (or a type that promotes to `int`).
    `x[2.5]` fails to *compile* — `incompatible types: possible lossy
    conversion from double to int` — because the mistake is syntactical.
12. **Out-of-range `int` index → `ArrayIndexOutOfBoundsException` at run
    time**, whether the index is too large (`x[6]` for size 6) or negative
    (`x[-6]`). Sign does not change the exception.
13. **Syntactical mistake (wrong index type) → compile time. Logical
    mistake (wrong index value, still an `int`) → run time.** That
    distinction is itself an exam answer.
14. **Since Java 14/15 (JEP 358), a `NullPointerException` names the
    failing expression** — e.g. `Cannot load from int array because "x[0]"
    is null` — instead of the bare, detail-free exception the lecture's
    Java 6/7 JVM produced.
15. **The compiler's narrowing-conversion wording changed by Java 7**: the
    lecture's "possible loss of precision / found / required" block became
    the one-line `incompatible types: possible lossy conversion from X to
    Y`. Same defect, different message layout — recognise both if you are
    working from an older question bank.

---

**Next:** Video 008 — Arrays part 3
