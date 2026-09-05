# Video 006 — Arrays part 1

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-6 || Arrays Part-1

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 6 of 203 |
| Series | Language Fundamentals · Part 6 of 16 |
| Topic | Arrays part 1 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 15m 24s (4524 seconds) |
| Video ID | HSp0UX9Z8Zw |
| Watch | https://www.youtube.com/watch?v=HSp0UX9Z8Zw |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Arrays is a big topic. Durga budgets two or three sessions and starts with a nine-item agenda that spans this video and the next array videos.

1. Introduction (need, advantage, limitation, definition)
2. Array declaration (1-D, 2-D, 3-D, plus two declaration conclusions)
3. Array creation (every array is an object; language-level class names; 1-D creation loopholes)
4. Array initialization *(starts in video 007)*
5. Array declaration, creation and initialization in a single line *(video 008)*
6. `length` versus `length()` *(video 008)*
7. Anonymous arrays *(video 008)*
8. Array **element** assignments *(video 008)*
9. Array **variable** assignments *(introduced at the end of video 008; taught in part 4)*

This video finishes introduction, declaration, and **one-dimensional** creation (including the creation loopholes). Two-dimensional / three-dimensional *creation* continues in video 007.

## 00:06 — Agenda

Nine subtopics, written on the board before touching code: declaration, creation, and initialization are three separate stages, and element assignment is not the same thing as variable assignment. Keeping those apart is the point of the whole unit.

## 02:44 — Why arrays exist

### The individual-variable problem

```java
int x = 10;
```

That represents **one** `int` value. Two values need two variables (`x` and `y`). Three values need three (`x`, `y`, `z`). Ten thousand values would need ten thousand variables — the worst kind of programming practice: ten thousand lines, unreadable, and you cannot remember which name holds which value.

### Advantage — huge number of values, one variable

If you want to represent a huge number of values by using a **single** variable, go for arrays:

```java
int[] x = new int[10000];
```

`x` now represents 10,000 `int` slots. You distinguish them by **index**: `x[0]` is the first, `x[1]` the second, `x[2]` the third, … up to `x[9999]`.

**Advantage of an array:** we can represent a huge number of values by using a single variable, so **readability of the code will be improved**.

### 05:09 — Limitation 1: fixed in size

For every advantage there is a disadvantage.

If you create the array with size 10,000 and at runtime even **one extra** element arrives, the array cannot grow to hold it. Arrays are **fixed in size**. Once you create an array with some size, there is **no chance of increasing or decreasing** the size based on requirement.

Classroom analogy Durga uses: he expected the SCJP batch to be a "big hit," so he arranged a hall of **10,000 chairs** and multiple projectors — but only **two** students showed up, wasting 9,998 seats for two months. Next time he booked a **small room** with five chairs, and **10,000** people showed up, with no way to seat them.

**To use arrays you must know the size in advance.** If you do not know the size in advance, you cannot use arrays.

Biggest limitation, in his words: **arrays are fixed in size**.

### 07:27 — Limitation 2: homogeneous elements only

An array can hold only **homogeneous** (similar type) data-type elements. An `int[]` can store only `int` (and values that promote to `int` — that promotion rule is taught later). If you try to add a `boolean` or a `String` into an `int[]`, you get a compile-time error.

### 07:58 — Next level: collections

To overcome these problems, the next level is the **collections** concept: collections are not fixed in size, and they can accept both homogeneous and heterogeneous elements. That is a later module. For now we stay at the array level.

The ladder he draws: individual variables → arrays → collections.

> ⚠️ **Modern Java — "collections are not fixed in size" now has an exception.**
> `ArrayList`, `HashMap`, and the rest of the classic collections are still
> growable, exactly as taught. But **Java 9** added factory methods that hand
> back a genuinely **fixed-size, immutable** collection — closer to an array's
> size discipline than to a growable list:
>
> ```java
> List<Integer> nums = List.of(1, 2, 3);
> nums.add(4);        // RE: UnsupportedOperationException
> ```
>
> So the ladder gains a rung: individual variables → arrays → **fixed
> collections (`List.of`, `Set.of`, `Map.of`)** → growable collections. The
> exam-era claim that "collections are never fixed in size" is no longer
> universally true; it is true of `ArrayList`/`HashMap`, not of `List.of`.

### 08:20 — Definition to memorize

> *An array is an ***indexed collection of a fixed number of homogeneous data elements***.*

Every word is load-bearing:

| Word | Meaning |
|---|---|
| indexed | you reach an element by index (x[0], x[1], …) |
| collection | many values under one name |
| fixed number | size decided at creation; cannot grow/shrink |
| homogeneous | one element type |

### 09:38 — Board recap of introduction

- **Main advantage:** we can represent a huge number of values by using a single variable, so that readability of the code will be improved.
- **Main disadvantage:** fixed in size — once we create an array there is no chance of increasing or decreasing the size based on our requirement. Hence to use arrays we **compulsory should know the size in advance**, which may not be possible always.

That is the whole introduction.

## 12:56 — Array declaration

### 13:10 — One-dimensional declaration

Three ways to declare a 1-D `int` array. **All three are valid:**

```java
int[] x;    // 1 — recommended
int []x;    // 2
int x[];    // 3  (C / C++ style; still legal in Java)
```

Dimension symbols `[]` may sit:

- after the type (`int[] x`)
- before the variable (`int []x`)
- after the variable (`int x[]`)

**Recommended:** the first form, `int[] x`.

Not because "first impression is the best impression" — Durga tells two personality-development stories here (a treacherous minister who backfires into a royal marriage, and the wooden-horse-style gift full of soldiers) to make the point stick. The **Java** reason is narrower:

- In `int[] x`, **the name is clearly separated from the type**. You read: `x` is a one-dimensional `int` array.
- In `int x[]` you read "one-dimensional array `x` is of `int` type" — type is mixed with the name.
- `int []x` has the same mixing problem.

So: all valid; **first is recommended because the name is clearly separated from the type**.

> ⚠️ **Modern Java — `var` cannot stand where these brackets stand.**
> `var` (Java 10) infers `int[]` fine on the *right*-hand side, but it can
> never carry a dimension itself:
>
> ```java
> var x = new int[10];   // valid — infers int[]
> var y[] = new int[10]; // CE: 'var' is not allowed as an element type of an array
> var[] z = new int[10]; // CE: 'var' is not allowed as an element type of an array
> ```
>
> So `var` does not add a fourth declaration style — it only ever replaces
> the explicit type name (`int[]`), never the brackets. The three forms above
> remain the complete set for a 1-D array declaration.

### 21:18 — Declaration conclusion 1: no size at declaration

Requirement: represent six `int` values, so someone writes:

```java
int[6] x;   // CE: ']' expected
int[] x;    // VALID
```

**At the time of declaration we cannot specify the size.** Size is required at the time of **creation**. If you specify size in the declaration, compile-time error.

This is a very important exam conclusion.

### 24:02 — Two-dimensional declaration

Six styles. **All six are valid** two-dimensional array declarations (first three valid, next three also valid — "don't keep any doubt"):

```java
int[][] a;
int [][]a;
int a[][];
int[] []a;
int[] a[];
int []a[];
```

Wherever you place the two pairs of `[]` — both after the type, both after the name, or split between type and name — it is still a 2-D `int` array.

### 26:34 — Declaration conclusion 2: dimensions before the variable, first variable only

This is the second declaration conclusion and a favourite OCJP trap. Several variables in one statement:

| Declaration | a dimension | b dimension | Valid? |
|---|---|---|---|
| int[] a, b; | 1 | 1 | yes |
| int[] a[], b; | 2 | 1 | yes |
| int[] a[], b[]; | 2 | 2 | yes |
| int[][] a, b; | 2 | 2 | yes — the space is ignored; [][] is part of the type, so both a and b are 2-D |
| int[][] a, b[]; | 2 | 3 | yes |
| int[] a, []b; | — | — | no — CE: `<identifier> expected` |

Why the last one fails: if you want to specify a dimension **before the variable**, that facility is applicable **only for the first variable** in the declaration. The compiler treats `[]` attached to the type as part of the type for every name in the list, but `[]` written *before a later name* (`[]b`) is illegal — the parser expects an identifier there, not a bracket.

Same rule with three names:

```java
int[] a, b, c;     // valid — all 1-D
int[] a, []b, c;   // CE: <identifier> expected — dimension before the second variable
```

After the variable you may add `[]` on any name (`b[]`, `c[][]`, …) with no problem. The restriction is only **dimension before the variable**, and only the first name may use that.

He also drills "which of the following are valid" on this family and says he will give notes for the last (invalid) form.

### 35:48 — Three-dimensional declaration

He does not go to a fourth dimension — once you see 3-D you can generalise.

All of these are **valid** 3-D declarations (every way of distributing three `[]` pairs between type and name):

```java
int[][][] a;
int [][][]a;
int a[][][];
int[] [][]a;
int[][] []a;
int[] a[][];
int[][] a[];
int [][]a[];
int []a[][];
int[] []a[];
```

Read them as "three-dimensional `int` array `a`" no matter where the brackets sit.

### 38:34 — Declaration wrap-up

Only **two** declaration conclusions:

1. At the time of array declaration we cannot specify the size.
2. If we want to specify a dimension before the variable, that facility is applicable only for the **first** variable; applying it to remaining variables is a compile-time error.

Then the lecture moves to creation.

## 38:52 — Array creation

### Every array in Java is an object

```java
int[] a = new int[3];
```

Objects are created with the `new` operator. Arrays are also created with `new`. Therefore **every array in Java is an object**. `a` is a reference variable pointing at that array object.

Feel it as an object; draw the diagram: heap object of length 3, reference `a` pointing to it.

### 41:41 — Corresponding classes exist, but not at programmer level

Usually we create objects of classes. If every array is an object, a corresponding class must exist. Those classes **are part of the Java language** and are **not available at the programmer level** (you do not write `class [I { … }`). Naming conventions of those classes are internal; you are not expected to declare them.

**Proof** — ask the runtime class name:

```java
int[] x = new int[3];
System.out.println(x.getClass().getName());
```

Compiles and runs. Output:

```text
[I
```

Meaning: one `[` = one dimension, `I` = `int`.

For a two-dimensional `int` array (`new int[3][2]` or similar):

```text
[[I
```

Two `[` = two dimensions, then `I`.

He compiles `Test.java`, runs `java Test`, shows `[I`, then changes to 2-D and shows `[[I`.

### 46:44 — Table: array type → class name

| Array type | getClass().getName() |
|---|---|
| int[] | [I |
| int[][] | [[I |
| int[][][] | [[[I |
| double[] | [D |
| short[] | [S |
| byte[] | [B |
| boolean[] | [Z |

He runs:

```java
byte[] x = new byte[3];
System.out.println(x.getClass().getName());   // [B
```

Then the same with `boolean[]` of size 3. Boolean's encoding is `[Z` (students also guess `[B`, which is already used for `byte`). These names start with `[` precisely so they do not look like programmer-level class names.

A `boolean[]` stores `true`/`false` in each slot — that is the only extra remark he makes on the boolean diagram.

**Conclusion to copy:** for every array type, corresponding classes are available, and these classes are part of the Java language and not available to the programmer level.

> ⚠️ **Modern Java — you rarely need to decode `[I` by hand any more.**
> `getClass().getName()` still returns the same descriptor-style names Sir
> shows (`[I`, `[[I`, `[Z`, …) — that has not changed. But two additions make
> the *readable* answer easier to reach without memorising the code table:
>
> ```java
> int[] x = new int[3];
> x.getClass().getCanonicalName();   // "int[]" — human-readable
> x.getClass().componentType();      // Class<Integer.TYPE> — Java 12, java.lang.Class::componentType
> ```
>
> `componentType()` (Java 12) hands back the element type directly instead of
> making you string-parse `[I`. The internal name in the table above is still
> the one JVM tooling (stack traces, `instanceof` messages, bytecode) shows
> you, so it is still worth knowing — `getCanonicalName()` is the shortcut for
> printing something a person can read.

### 50:18 — Creation loophole 1: size is compulsory at creation

```java
int[] x = new int[];     // CE: array dimension missing
int[] x = new int[6];    // VALID
```

At declaration we **cannot** specify size. At creation we **must** specify size. The JVM reserves memory from the size. If you omit the size, the compiler reports it.

**Rule:** at the time of array creation, compulsory we should specify the size; otherwise compile-time error.

### 53:06 — Creation loophole 2: size zero is legal

```java
int[] x = new int[0];    // VALID
```

It is **legal to have an array with size zero** in Java.

Best example: `main`'s parameter is `String[] args` (command-line arguments). If you run the class 100 times you may pass arguments once or twice. If you pass **no** command-line arguments, `args.length` is **0**. If you pass `a b c d`, `args.length` is **4**.

He prints `args.length`: no args → `0`; four tokens → `4`.

### 56:00 — Creation loophole 3: negative size compiles, blows up at runtime

```java
int[] x = new int[-3];
```

**Invalid at runtime, not at compile time.**

There is **no compile-time error**. The compiler only checks: did you specify *some* size, and is it an `int` value? Positive vs negative is **not** the compiler's job.

At runtime the JVM tries to reserve memory, sees a negative size, and throws a runtime exception:

**`NegativeArraySizeException`**

He compiles: fine. He runs:

```text
Exception in thread "main" java.lang.NegativeArraySizeException: -3
```

**Rule:** if we try to specify array size with some negative `int` value, we get a runtime exception saying `NegativeArraySizeException`. No compile-time error.

(It is **size**, not index — students say "negative index"; he corrects them.)

### 1:00:52 — Creation loophole 4: which types may be used as size

The size expression must be `int` (or a type that promotes to `int`).

Promotion chart from the data-types lectures: `byte` → `short` → `int` ← `char`, then `int` → `long` → `float` → `double`.

Allowed for array size: **`byte`, `short`, `char`, `int`**.

```java
int[] x = new int['a'];   // VALID — char promotes to int; size is 97 (Unicode of 'a')

byte b = 20;
int[] x = new int[b];     // VALID

short s = 30;
int[] x = new int[s];     // VALID

int[] x = new int[10L];   // CE: incompatible types: possible lossy conversion from long to int
```

`long` is not allowed as size. Any other type (`long`, `float`, `double`, `boolean`, …) → compile-time error.

**Rule:** to specify array size, the allowed data types are `byte`, `short`, `char`, `int`. If we specify any other type, compile-time error.

*(Sir quotes the older three-line form of this message — `possible loss of precision` / `found: long` / `required: int`. Current javac folds it into the single line shown above; the rule it enforces has not moved.)*

### 1:06:44 — Creation loophole 5: maximum allowed size

There must be an upper bound: the size type is `int`, and the maximum `int` value is **2147483647**.

So the **maximum allowed array size in Java is 2147483647**, which is the maximum value of the `int` data type.

```java
int[] x = new int[2147483647];   // compiles (size is a valid int)
int[] x = new int[2147483648];   // CE: integer number too large
```

`2147483648` is outside the `int` range. Any integral literal that is not in the `int` range is a compile error **integer number too large** (from the literals lectures: an integral literal is `int` unless it ends with `L`). Adding `L` would make it `long`, which is then illegal as an array size for loophole 4.

**Even the first line can fail at runtime.** 2,147,483,647 `int` values × 4 bytes each is a huge heap request. That much memory may not be available. Then you get:

```text
Exception in thread "main" java.lang.OutOfMemoryError: Requested array size exceeds VM limit
```

He compiles `new int[2147483647]`: fine. He runs it and — unless the JVM has an enormous heap available — gets the `OutOfMemoryError` above.

That is **not a program logic mistake**; it is lack of system / heap resources. Provide enough heap and it can run. He still calls it a runtime problem you should be aware of: even in the first (compiling) case we **may** get a runtime failure if sufficient heap memory is not available.

### 1:14:20 — One-dimensional creation: five conclusions he recites at the end

1. At the time of array creation we must specify the size (else compile-time error).
2. It is legal to have an array with size zero.
3. Negative `int` size → runtime `NegativeArraySizeException` (no compile error).
4. Allowed size types: `byte`, `short`, `char`, `int` (else compile-time error).
5. Maximum allowed size is 2147483647 (`int` max). Bigger literal → `integer number too large`. Even max size may throw `OutOfMemoryError` if the heap cannot hold it.

The video ends here. Two-dimensional creation (array-of-arrays, not matrix) is the opening of part 2.

## Code from the lecture

Every line below was compiled against a current JDK; the commented-out lines carry the exact message that JDK produces.

```java
class Test {
    public static void main(String[] args) {
        // declaration styles (1-D) — all valid; first recommended
        int[] a;
        int []b;
        int c[];

        // int[6] d;          // CE: ']' expected

        // 2-D — all valid
        int[][] e;
        int [][]f;
        int g[][];
        int[] []h;
        int[] i[];
        int []j[];

        // comma declarations
        int[] k, l;           // both 1-D
        int[] m[], n;         // m is 2-D, n is 1-D
        int[] o[], p[];       // both 2-D
        int[][] q, r;         // both 2-D (space ignored)
        int[][] s, t[];       // s is 2-D, t is 3-D
        // int[] u, []v;      // CE: <identifier> expected

        // creation
        int[] x = new int[3];
        System.out.println(x.getClass().getName()); // [I

        int[][] y = new int[3][2];
        System.out.println(y.getClass().getName()); // [[I

        byte[] z = new byte[3];
        System.out.println(z.getClass().getName()); // [B

        // int[] bad = new int[];          // CE: array dimension missing
        int[] zero = new int[0];           // legal
        // int[] neg = new int[-3];        // compiles; RE: NegativeArraySizeException: -3

        int[] fromChar = new int['a'];     // size 97
        byte bb = 20;
        int[] fromByte = new int[bb];
        short ss = 30;
        int[] fromShort = new int[ss];
        // int[] fromLong = new int[10L];  // CE: incompatible types: possible lossy conversion from long to int

        // int[] huge = new int[2147483647]; // compiles; may OOME at runtime
        // int[] tooBig = new int[2147483648]; // CE: integer number too large

        System.out.println(args.length);   // 0 if no command-line args
    }
}
```

## Rules to memorize

1. Array = indexed collection of a fixed number of homogeneous data elements.
2. Advantage: huge number of values, one variable → better readability.
3. Disadvantage: fixed size; you must know the size in advance (not always possible). Also homogeneous only. Next level: growable collections (`ArrayList`, `HashMap`, …) — and, since Java 9, fixed-size immutable ones too (`List.of`, `Set.of`, `Map.of`).
4. 1-D: `int[] x`, `int []x`, `int x[]` all valid; **`int[] x` recommended** (name clearly separated from type). `var` (Java 10) never adds a fourth form — it replaces the type name, not the brackets.
5. **No size at declaration** (`int[6] x` is CE). **Size compulsory at creation** (`new int[]` is CE).
6. 2-D: all six bracket placements valid. 3-D: all ten bracket placements valid.
7. `int[] a, b` → both 1-D. `int[][] a, b` → both 2-D (brackets on the type apply to every name). `int[] a[], b` → `a` is 2-D, `b` is 1-D. `int[][] a, b[]` → `a` is 2-D, `b` is 3-D. `int[] a, []b` → **CE**.
8. Dimension **before** a name: only the **first** variable in the declaration.
9. Every array is an object (`new`). Corresponding classes exist at language level (`[I`, `[[I`, `[D`, `[S`, `[B`, `[Z`, …), not as types you declare. `getClass().getCanonicalName()` and `Class::componentType()` (Java 12) give the readable form without decoding the descriptor by hand.
10. `new int[0]` is legal. `main`'s `args` has length 0 when no command-line arguments are passed.
11. `new int[-3]` compiles; runtime **`NegativeArraySizeException`**.
12. Size types: **byte, short, char, int** only. `new int[10L]` → CE, reported today as `incompatible types: possible lossy conversion from long to int`.
13. Max size **2147483647**. Literal `2147483648` → CE **integer number too large**. Max size may still throw **`OutOfMemoryError: Requested array size exceeds VM limit`**.

## Exam and interview points

1. `int[] x` vs `int x[]` — both compile; only the first is recommended, because the name stays visually separated from the type.
2. `int[6] x` looks like C-style sizing; it is a **compile-time error** in Java (`']' expected`) — size belongs at creation, never at declaration.
3. `int[] a, []b` looks symmetric with `int[] a[], b`; it is **illegal**, because a dimension written *before* a name is only legal on the *first* variable in the declaration. `int[] a[], b` is legal and `b` is only 1-D.
4. `int[][] a, b` — both names are 2-D, not "`a` is 2-D and `b` is 1-D"; brackets attached to the type belong to every name in the list.
5. "Is an array an object?" — **Yes.** Proof: created with `new`; `getClass().getName()` works and returns a real (if unwritable) class name.
6. Class names like `[I`, `[[I`, `[Z` are not programmer-level types; do not try to write `new [I()`. Use `getClass().getCanonicalName()` or `Class::componentType()` (Java 12) when you want the readable form instead.
7. A **zero-length array is legal**, not a trick invalid case — it is exactly what `args` is when no command-line arguments are passed.
8. Negative size is **not** a compile error. Do not write "CE" for `new int[-1]`; it is a **`NegativeArraySizeException`** at runtime.
9. `char` as an array size is legal (`'a'` promotes to `97`). `long` is not — it is a compile error even though `long` is "bigger" than `int`, because array size must be exactly `int` or something that promotes to it.
10. `2147483647` compiles; "so it always runs" is false — heap may throw `OutOfMemoryError: Requested array size exceeds VM limit`. That is an **Error**, not a logic-bug exception, but the exam still expects you to know the message.
11. **Modern interview angle:** `var` cannot appear where an array's `[]` appears (`var x[]` and `var[] x` both fail to compile) — it only ever stands in for the type name. And "collections are never fixed size" needs a caveat since Java 9: `List.of(...)` is deliberately fixed and immutable, closer to array discipline than to `ArrayList`.
12. Two-dimensional arrays in Java are **not** a C-style matrix — the next lecture (video 007) opens with the fact that Java implements them as an **array of arrays**, so inner rows can have different lengths.

**Next:** Video 007 — Arrays part 2
