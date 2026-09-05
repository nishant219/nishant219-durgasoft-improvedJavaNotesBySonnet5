# Video 012 — var-arg methods

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-12 || var-arg methods

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 12 of 203 |
| Series | Language Fundamentals · Part 12 of 16 |
| Topic | var-arg methods (int... x) — syntax, restrictions, vs arrays, overloading |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 20m 36s |
| Video ID | sjsq5UL5oFs |
| Watch | https://www.youtube.com/watch?v=sjsq5UL5oFs |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. What **var-arg** means: **variable number of argument** methods
2. Why 1.5 added them: `sum(int,int)`, `sum(int,int,int)`, … explodes length and kills readability
3. Declaration: `m1(int... x)` — **exactly three dots**
4. Calls with 0, 1, 2, 4, … arguments (including zero)
5. Internally a **1-D array**; differentiate values by **index**; `x.length`
6. Meaningful `sum` example with **for-each** (also 1.5)
7. SCJP loopholes / cases:
   - Case 1 — which declarations are valid (`int... x` vs `int x...`; spaces; three dots are "best friends")
   - Case 2 — mix var-arg with a normal parameter
   - Case 3 — var-arg **must be last**
   - Case 4 — **only one** var-arg parameter
   - Case 5 — cannot declare var-arg **and** the matching 1-D array method in the same class
   - Case 6 — overload var-arg vs general method; **least priority** (like `default` in `switch`); old concept wins
8. Equivalence with 1-D arrays: array → var-arg **is** a valid replacement (including `main(String... args)`); **reverse is not**
9. `int[]... x` means a group of 1-D arrays → `x` is 2-D; exam program printing `a[0]` and `b[0]`

Next topics he announces: postmortem on `main` (about two sessions), command-line arguments, Java coding standards.

---

## 00:06 — Name and version

Important for the **interview room** and the **exam** — it gives **more flexibility** to the programmer.

**var-arg methods** = **variable number of argument** methods. In speech he says "where-are methods"; on the board it is **var-arg**. New concept in **Java 1.5**.

---

## 01:13 — The problem until 1.4: too many `sum` methods

Requirement: find the sum of two numbers.

```java
public static void sum(int a, int b) {
    System.out.println(a + b);
}
sum(10, 20);
```

Later: sum of three numbers, `sum(10, 20, 30)`. Can you reuse the two-argument method? **No** — it takes two values, you are passing three. New method:

```java
public static void sum(int a, int b, int c) {
    System.out.println(a + b + c);
}
```

Four numbers, then five, then six — each time, another `sum` overload. The *requirement* never changes (sum some `int`s); only the **count of arguments** changes, and until 1.4 that alone forces a **new method**. Result: **length of the code increases, readability drops.**

---

## 04:36 — The 1.5 fix

In 1.5 you no longer need a `sum` method per arity. **One** `sum` method can be called with **any number of `int` values** — 2, 3, 4, 10, a lakh — no problem. Methods that accept a **variable number of arguments** are **var-arg methods**.

Declaration:

```java
public static void sum(int... a) {
    // ...
}
```

**Exactly three dots.** A fourth dot is a compile error. From 1.5 you can call this one method with two values, three, four, any number — **including zero**.

---

## 06:01 — Board theory: until 1.4 vs 1.5

**Until 1.4:** we **can't** declare a method with a variable number of arguments. A change in arity forces a **new method** — more code, less readability.

**From 1.5:** var-arg methods let one method take a variable number of arguments.

---

## 09:03 — How to declare and how to call

```java
m1(int... x)
```

Call it with **any number of `int` values, including zero**:

| Call | Valid? |
|---|---|
| `m1()` | yes (zero ints) |
| `m1(10)` | yes |
| `m1(10, 20)` | yes |
| `m1(10, 20, 30, 40)` | yes |

> ⚠️ **Modern Java — declaring a var-arg over a generic type needs `@SafeVarargs` (Java 7).**
> Every example in this lecture varargs over `int`, `String`, `double` — concrete
> types, no problem. The trap arrives when the vararg element type is itself a
> **generic type parameter**: because arrays and generics don't mix cleanly, the
> compiler has to build the backing array as `Object[]` at runtime, which can let
> the wrong type sneak in (**heap pollution**) without any cast ever failing
> visibly at the call site:
>
> ```java
> static <T> T[] toArray(T... x) {   // compiles, but with a warning
>     return x;
> }
> ```
>
> ```text
> warning: [unchecked] Possible heap pollution from parameterized vararg type T
> ```
>
> Since **Java 7**, annotating the method `@SafeVarargs` tells the compiler
> "I checked, this method does nothing unsafe with the array" and suppresses the
> warning at every call site — but it is a promise, not a proof; the JDK itself
> uses it on `Arrays.asList`, `List.of`, and friends. Confirmed on JDK 26: the
> exact same warning still fires without the annotation.

---

## 11:50 — First runnable example

```java
class Test {
    public static void m1(int... x) {
        System.out.println("var-arg method");
    }

    public static void main(String[] args) {
        m1();
        m1(10);
        m1(10, 20);
        m1(10, 20, 30, 40);
    }
}
```

`javac Test.java` compiles; `java Test` prints:

```text
var-arg method
var-arg method
var-arg method
var-arg method
```

Four calls, four lines. How to declare a var-arg method and how to call it is now clear — a big convenience for the programmer.

---

## 16:32 — Internally a 1-D array — differentiate by index

You can pass zero, one, two, four, a lakh values. Inside the method, how do you tell the first value from the second from the third? A **group of `int` values** becomes a **one-dimensional array**: internally the var-arg parameter **is converted into a 1-D array**. Differentiate elements the only way arrays allow — **by index**.

Number of arguments:

```java
public static void m1(int... x) {
    System.out.println("Number of arguments: " + x.length);
}
```

`x.length` is the array property:

| Call | `x.length` |
|---|---|
| `m1()` | 0 |
| `m1(10)` | 1 |
| `m1(10, 20)` | 2 |
| `m1(10, 20, 30, 40)` | 4 |

**Board:**
- Internally the var-arg parameter will be converted into a **one-dimensional array**.
- Hence within the var-arg method we can differentiate values **by using index**.

---

## 20:26 — Meaningful example: one `sum` for 0, 2, 3, 4 arguments

```java
class Test {
    public static void main(String[] args) {
        sum();
        sum(10, 20);
        sum(10, 20, 30);
        sum(10, 20, 30, 40);
    }

    public static void sum(int... x) {
        int total = 0;
        for (int x1 : x) {          // for-each, also 1.5
            total = total + x1;
        }
        System.out.println("The sum: " + total);
    }
}
```

Expected output, written on the board before coding:

| Call | Expected |
|---|---|
| `sum()` | The sum: 0 (no values) |
| `sum(10, 20)` | The sum: 30 |
| `sum(10, 20, 30)` | The sum: 60 |
| `sum(10, 20, 30, 40)` | The sum: 100 |

Without var-arg you would need **four** `sum` methods; with var-arg, **one**. `x` is the var-arg parameter, internally a 1-D `int` array; **for-each** (`for (int x1 : x)`) is also a **1.5** feature — for every `int` value `x1` in `x`, `total = total + x1`.

Compiled and run: **0, 30, 60, 100** — verified. The clearest case yet for why var-arg is the right choice.

---

## 27:25 — SCJP loophole, case 1: valid declarations (syntax)

Array parameter styles, all valid, for comparison:

```java
m1(int[] x)     // valid
m1(int []x)     // valid — same method, space/bracket style
m1(int x[])     // valid for arrays (C-style)
```

People want the same freedom for the var-arg parameter. Which of these are valid **var-arg** declarations? A compulsory syntax-checking question.

**Valid** — spaces around the `...` token are ignored; the three dots must stay together as one token:

```java
m1(int... x)     // valid
m1(int ...x)     // valid — space ignored
m1(int...x)      // valid — no space needed
```

**Invalid:**

```java
m1(int x...)     // CE: ',', ')', or '[' expected — ... cannot follow the identifier
m1(int ..x)      // CE: illegal '.' — not three dots together
```

**The three dots are best friends. You cannot separate them.** He compares them to **three stars in the sky that are always together** — a childhood navigation story (look up, those three stars are always there, wherever you go). The technical point underneath the story: `...` is a single token, attached to the **type**, never to the name.

Why `int x...` fails where `int x[]` succeeds: array syntax allows brackets after the identifier; var-arg does not mirror that. Do not copy `int x[]` style onto var-arg.

Verified on JDK 26 — `javac` rejects `int x...` with `',', ')', or '[' expected` and rejects `int ..x` with `illegal '.'`; `int... x`, `int ...x`, and `int...x` all compile identically.

---

## 32:33 — Case 2: mix var-arg with a normal parameter

```java
m1(int x, int... y)           // VALID
m1(String s, double... y)     // VALID
```

First method: **one `int` is compulsory**, then any number of extra `int`s (including zero extra). Second: **one `String` is mandatory**, then any number of `double`s.

**We can mix a var-arg parameter with a normal parameter.** A method is not required to take *only* a var-arg parameter.

---

## 35:01 — Case 3: if you mix them, var-arg must be **last**

If case 2 is valid, the reverse is invalid:

```java
m1(double... d, String s)     // CE: varargs parameter must be the last parameter
```

"Any number of `double`s, but compulsory the last one should be `String`" — invalid, because the var-arg parameter is placed **first**.

```java
m1(String s, double... d)     // VALID — var-arg is last
```

**If we mix a normal parameter with a var-arg parameter, the var-arg parameter must be the last parameter.** Verified: JDK 26 reports exactly `varargs parameter must be the last parameter`.

---

## 38:03 — Case 4: only **one** var-arg parameter

```java
m1(int... x, double... d)     // CE: varargs parameter must be the last parameter
```

Classroom joke: "both are last only, one by one last only" — still **invalid**. Inside a method you can take **only one** var-arg parameter.

```java
m1(int x, double... d)        // VALID — one normal + one var-arg, var-arg last
m1(int... x, double... d)     // INVALID — two var-args
```

Verified: `javac` reports the same `varargs parameter must be the last parameter` message here as in case 3 — the compiler treats "var-arg not in the last slot" as one error, whether the thing pushed past it is a normal parameter or a second var-arg.

---

## 40:36 — Case 5: var-arg vs the matching 1-D array method

Warm-up (an overloading rule, ahead of the dedicated lecture on it): **inside a class, two methods with the same signature are not allowed. Return type is not part of the signature.**

```java
class Test {
    public void m1(int i) { }
    public int m1(int i) { return 10; }   // CE: m1(int) is already defined
}
```

Signature of both is `m1(int)`. If you call `m1(10)`, which one runs? The compiler rejects it before that question can arise.

**Same rule applies to var-arg**, because internally `int... x` **is** `int[] x`:

```java
class Test {
    public static void m1(int... x) {
        System.out.println("var-arg");
    }

    public static void m1(int[] x) {
        System.out.println("int[]");
    }
}
```

Signature of the first is `m1(int[])`. Signature of the second is `m1(int[])`. **Same signature** → compile-time error:

```text
error: cannot declare both m1(int[]) and m1(int...) in Test
```

**Inside a class we cannot declare a var-arg method and the corresponding one-dimensional array method simultaneously.** Verified — that exact message, byte for byte, comes back from JDK 26.

---

## 47:35 — Case 6: overloading — general method vs var-arg (least priority)

These two **are** allowed together, because signatures differ (`m1(int)` vs `m1(int[])`):

```java
class Test {
    public static void m1(int... x) {
        System.out.println("var-arg method");
    }

    public static void m1(int x) {
        System.out.println("general method");
    }

    public static void main(String[] args) {
        m1();
        m1(10, 20);
        m1(10);
    }
}
```

| Call | Which method runs? | Why |
|---|---|---|
| `m1()` | var-arg | general method expects one `int`; you passed zero. Var-arg accepts any count, including zero |
| `m1(10, 20)` | var-arg | general method does not match two `int`s |
| `m1(10)` | general method | both match — general wins |

`m1(10)`: both methods match, but there is **no ambiguity error**. Only one gets the call. Story: the two methods meet at a common place to fight, and the **general method always wins** — "19+ years of industry experience" beats the newcomer. General-method overloading exists from **Java 1.0**; var-arg arrived in **1.5**. Experienced vs. fresher — experience wins.

**Two rules to remember:**

1. If there is a fight between an **old concept and a new concept**, the **old concept wins** — for compatibility with old code. "Old is gold."
2. **Var-arg gets the least priority.** If **no other method matches**, only then does the var-arg method get the chance — exactly like **`default` inside a `switch`**: several `case`s, then `default` runs only **if no case matched**.

Output, compiled and run:

```text
var-arg method
var-arg method
general method
```

**Board:** in general, var-arg gets **least priority** — if no other method matched, only then does the var-arg method get the chance. Same idea as `default` inside a `switch`.

> This is not folklore dressed up — it is how the JLS actually resolves an
> overloaded call (§15.12.2), in three fixed phases: **phase 1** tries every
> applicable method *without* boxing or var-arg (this is where `m1(int)` wins
> `m1(10)`); only if phase 1 finds nothing does **phase 2** allow boxing/unboxing;
> only if phase 2 also finds nothing does **phase 3** allow variable-arity
> invocation. A var-arg method is only ever picked in phase 3 — Sir's "least
> priority" is the accurate, one-sentence version of that three-phase search, and
> it has been unchanged since var-arg itself arrived in 1.5.

This is case 6 of var-arg methods.

---

## 57:31 — Equivalence between var-arg parameter and 1-D array

Question: you have a method taking a 1-D array — can you replace it with a var-arg parameter? You have a var-arg method — can you replace it with a 1-D array method? What is the equivalence?

### Case A — 1-D array **can** be replaced with var-arg (valid replacement)

```java
m1(int[] x)
```

Call style for an array parameter:

```java
m1(new int[]{10});
m1(new int[]{10, 20});
m1(new int[]{10, 20, 30});
```

Replace with var-arg:

```java
m1(int... x)
```

Now **all** of these work:

```java
m1(new int[]{10});      // still valid — an array is a legal var-arg call too
m1();                   // NEW — zero arguments
m1(10);                 // NEW
m1(10, 20, 30);         // NEW
```

Existing array-passing calls still work, **plus** new combinations appear. **Wherever a one-dimensional array parameter is present, we can replace it with a var-arg parameter. This replacement is valid.**

### `main` itself — `String... args`

`main`'s parameter is `String[]`. By the same rule, replace it with var-arg:

```java
class Test {
    public static void main(String... args) {
        System.out.println("var-arg main");
    }
}
```

**Perfectly valid from 1.5 onwards** — verified: compiles and runs on JDK 26, and `java Test` finds and launches it as the entry point exactly as it would `String[] args`. (`Stringer` in the auto-captions is **`String`**.)

**Board:**
- Wherever a one-dimensional array is present, we can replace it with a var-arg parameter.
- `m1(int[] x)` → `m1(int... x)` — valid.
- `main(String[] args)` → `main(String... args)` — valid.

### Case B — the reverse is **not** possible (invalid replacement)

Start with var-arg:

```java
m1(int... x)
```

Valid calls: `m1()`, `m1(10)`, `m1(10, 20, 30)`, and also `m1(new int[]{...})`. Now replace it with a plain array:

```java
m1(int[] x)
```

| Call that used to work | After the replacement |
|---|---|
| `m1()` | CE — method expects a 1-D array; you passed no arguments |
| `m1(10)` | CE — `int` cannot be converted to `int[]` |
| `m1(10, 20, 30)` | CE |
| `m1(new int[]{10, 20})` | still valid — you are passing an actual array |

Some combinations **stop compiling** once the parameter goes back to a plain array. Verified: JDK 26 rejects the bare `m1()` call with `actual and formal argument lists differ in length` and rejects `m1(10)` with `incompatible types: int cannot be converted to int[]`. Therefore:

**Wherever a var-arg parameter is present, we cannot replace it with a one-dimensional array. The reverse is not possible.**

| Direction | Valid replacement? |
|---|---|
| 1-D array → var-arg | yes (old calls still work, new calls appear) |
| var-arg → 1-D array | no (zero-arg and loose-argument calls break) |

---

## 1:08:47 — Exam bit: var-arg of arrays (1-D, 2-D, 3-D)

Var-arg is not always `int...` — purely an SCJP point of view.

```java
m1(int... x)
```

Call by passing any number of `int` values; **`x` becomes a 1-D `int` array**.

```java
m1(String... x)
```

Call by passing any number of `String` values; **`x` becomes a 1-D `String` array**.

```java
m1(int[]... x)
```

Call by passing a **group of one-dimensional `int` arrays**. A group of 1-D arrays **is a 2-D array** — **`x` becomes a 2-D `int` array.**

```java
m1(int[][]... x)
```

A group of 2-D arrays → **`x` becomes a 3-D `int` array**.

**Board:**

| Declaration | We can call by passing | `x` becomes |
|---|---|---|
| `m1(int... x)` | a group of `int` values | 1-D `int` array |
| `m1(int[]... x)` | a group of 1-D `int` arrays | 2-D `int` array |
| `m1(int[][]... x)` | a group of 2-D `int` arrays | 3-D `int` array |

Sometimes you need `m1(int[]... x)`, not only `m1(int... x)`.

---

## 1:14:36 — Last exam program: `int[]... x`, print first elements

```java
class Test {
    public static void main(String[] args) {
        int[] a = {10, 20, 30};    // 1-D array
        int[] b = {40, 50, 60};    // 1-D array
        m1(a, b);
    }

    public static void m1(int[]... x) {
        for (int[] x1 : x) {
            System.out.println(x1[0]);
        }
    }
}
```

Is `m1(int[]... x)` valid for this call? Yes — we pass a **group of 1-D arrays** (`a` and `b`), so **`x` becomes a 2-D array**. Base size of that 2-D structure: **2** (two 1-D arrays inside). First element: `{10, 20, 30}`. Second: `{40, 50, 60}`.

for-each: for every 1-D array `x1` in `x` — the loop runs **twice**. Each time it prints `x1[0]`, the first element of that 1-D array.

| Iteration | `x1` | `x1[0]` |
|---|---|---|
| 1 | `{10, 20, 30}` | 10 |
| 2 | `{40, 50, 60}` | 40 |

**Output**, compiled and run — verified:

```text
10
40
```

Chance this appears on the exam. Do not read "var-arg" as always meaning `int...`; work out what `x` actually becomes.

---

## 1:18:47 — What comes next in Language Fundamentals

Last example related to var-arg. Next up: a **postmortem on the `main` method** — about two sessions — then **command-line arguments**, then **Java coding standards**.

---

## Code from the lecture

Everything Sir compiles, consolidated. Every block below was compiled and run on JDK 26 for this note; invalid lines are commented with the exact modern error.

```java
class Test {
    public static void m1(int... x) {
        System.out.println("var-arg method");
        System.out.println("Number of arguments: " + x.length);
    }

    public static void main(String[] args) {
        m1();                // Number of arguments: 0
        m1(10);              // Number of arguments: 1
        m1(10, 20);          // Number of arguments: 2
        m1(10, 20, 30, 40);  // Number of arguments: 4
    }
}
```

```java
class Test {
    public static void sum(int... x) {
        int total = 0;
        for (int x1 : x) {
            total = total + x1;
        }
        System.out.println("The sum: " + total);
    }

    public static void main(String[] args) {
        sum();                      // The sum: 0
        sum(10, 20);                // The sum: 30
        sum(10, 20, 30);            // The sum: 60
        sum(10, 20, 30, 40);        // The sum: 100
    }
}
```

```java
class Test {
    public static void m1(int... x) {
        System.out.println("var-arg method");
    }

    public static void m1(int x) {
        System.out.println("general method");
    }

    public static void main(String[] args) {
        m1();          // var-arg method
        m1(10, 20);    // var-arg method
        m1(10);        // general method  (old concept wins; var-arg has least priority)
    }
}
```

```java
class Test {
    public static void main(String... args) {   // valid from 1.5 — an accepted entry point too
        System.out.println("var-arg main");
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int[] a = {10, 20, 30};
        int[] b = {40, 50, 60};
        m1(a, b);                   // prints 10 then 40
    }

    public static void m1(int[]... x) {
        for (int[] x1 : x) {
            System.out.println(x1[0]);
        }
    }
}
```

```java
// Case 5 — cannot coexist:
class Test {
    public static void m1(int... x) { }
    // public static void m1(int[] x) { }
    // CE: cannot declare both m1(int[]) and m1(int...) in Test
}

// Case 3 / Case 4 — var-arg must be last, and only one is allowed:
class Test2 {
    // static void m1(double... d, String s) { }        // CE: varargs parameter must be the last parameter
    // static void m1(int... x, double... d) { }         // CE: varargs parameter must be the last parameter
    static void m1(String s, double... d) { }            // valid — var-arg last
}
```

---

## Exam and interview points

1. **Var-arg (`int... x`) is a Java 1.5 feature.** Until 1.4, a change in the
   number of arguments compulsorily needed a new overload — that is the entire
   motivation.
2. **Exactly three dots, attached to the type, never the name.** `int ...x`
   and `int...x` are valid (spaces around the token don't matter); `int x...`
   and `int ..x` are compile errors. Verified: `',', ')', or '[' expected` and
   `illegal '.'` respectively.
3. **Zero arguments is a legal call.** `m1()` is valid for `m1(int... x)`; the
   `sum` example prints `The sum: 0` for exactly that reason.
4. **Internally `int... x` is `int[] x`.** Use `x.length` and index/for-each
   to work with it — there is no other way to tell the values apart.
5. **for-each (`for (T t : arr)`) is also a Java 1.5 feature**, same release as
   var-arg — the `sum` example uses both together.
6. **At most one var-arg parameter, and it must be the last parameter.**
   `m1(double... d, String s)` and `m1(int... x, double... d)` both fail with
   the identical message, `varargs parameter must be the last parameter`.
7. **A var-arg method and the matching 1-D array method cannot coexist** in one
   class — `m1(int... x)` and `m1(int[] x)` share the signature `m1(int[])`.
   Exact error: `cannot declare both m1(int[]) and m1(int...) in Test`.
8. **`m1(int... x)` and `m1(int x)` together is legal overloading**, and calling
   `m1(10)` picks the **general (fixed-arity) method**, not the var-arg one, and
   is not an ambiguity error. Var-arg is chosen only when nothing else matches —
   formally, JLS §15.12.2's phase 3 (variable-arity invocation), which is tried
   only after phases 1 and 2 both fail.
9. **1-D array → var-arg is a safe upgrade** (old array-passing calls keep
   working, new zero/loose-argument calls become legal) — this is exactly why
   `main(String... args)` is a valid, launchable entry point from Java 1.5
   onward. **Var-arg → 1-D array is not safe**: `m1()` and `m1(10)` calls that
   worked against the var-arg version break with `actual and formal argument
   lists differ in length` and `incompatible types` respectively.
10. **`T[]... x` is a var-arg of arrays**, not a var-arg of `T`. `int[]... x`
    makes `x` a **2-D** `int` array; `int[][]... x` makes it **3-D**. Passing
    two 1-D arrays and printing `x1[0]` in a for-each over `x` gives `10` then
    `40` — not the six elements laid flat.
11. **Watch for heap pollution on generic var-arg methods** (`<T> void m1(T...
    x)`): the JVM backs it with an `Object[]`, so the compiler warns
    `[unchecked] Possible heap pollution from parameterized vararg type T`.
    Since **Java 7**, `@SafeVarargs` on the method suppresses that warning —
    it is a promise the method is safe, not a guarantee enforced by the
    compiler.

---

**Next:** Video 013 — main() method, part 1
