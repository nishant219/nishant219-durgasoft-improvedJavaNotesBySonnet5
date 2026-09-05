# Video 009 — Arrays, Part 4

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-9 || Arrays Part-4

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 9 of 203 |
| Series | Language Fundamentals · Part 9 of 16 |
| Topic | Arrays (part 4): array variable assignments |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 54m 23s (3263 seconds) |
| Video ID | mkQsfdMITM8 |
| Watch | https://www.youtube.com/watch?v=mkQsfdMITM8 |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** No transcript survives for this upload, so
> sections below follow the note's own structure rather than the lecture's
> timestamps. Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

Part 3 (video 008) closed by naming the next heading — **array variable
assignments** — and stopping. This lecture is that heading: not "what can go
in `a[i]`" (that was part 3), but "when can I write `left = right` for two
array names?" Every claim below has been checked against the JLS and
compiled on JDK 26.

## What this lecture covers

1. Element assignment vs. variable assignment
2. Assigning one array reference to another (same type, same dimension)
3. What happens to the old array object (GC)
4. Dimension mismatch (`int[]` vs. `int[][]`)
5. Child-type arrays assigned to parent-type arrays (`String[]` → `Object[]`)
6. Why `char[]` cannot be assigned to `int[]` (promotion is for *elements*, not for the array type)
7. 3-D / jagged leftovers and exam patterns
8. Close of the arrays topic

---

## Two different "assignments"

Durga keeps these on two boards:

| Kind | Meaning | Example |
|---|---|---|
| Element assignment (parts 3–4 start) | What may go inside `a[i]` | `a[0] = 10;` / `a[0] = new Thread();` |
| Variable assignment (this lecture) | What may go into the array name itself | `a = b;` |

Element rules, recapped from part 3 and still in force:

- Primitive array: any type that can be **implicitly promoted** to the declared element type (`byte` into `int[]`, etc.).
- Object array: declared type **or child** objects.
- Abstract-class array: **child** objects (`Number[]` can hold `Integer`, `Double`, …).
- Interface array: **implementation** objects (`Runnable[]` can hold `Thread`).

This lecture is not "what goes in the slot." It is "when can I write
`leftArray = rightArray`?"

## Same type, same dimension — always allowed

```java
int[] a = {10, 20, 30, 40, 50};
int[] b = {60, 70};
a = b;
```

Both are `int[]` (one-dimensional). Assignment is valid — verified on JDK 26.

**After `a = b`:**

- `a` and `b` point to the **same** array object `{60, 70}`.
- `a.length` is now **2**, not 5.
- The old `{10, 20, 30, 40, 50}` object has no reference → eligible for **GC**.

```java
System.out.println(a[0]); // 60
b[0] = 99;
System.out.println(a[0]); // 99 — same object
```

Sizes do **not** have to match. Only the **type and dimension** have to match.
`{10, 20, 30, 40, 50}` and `{60, 70}` have different lengths; the assignment
is still legal because both are `int[]`.

## Dimension must match

```java
int[] a = new int[3];
int[][] b = new int[2][3];

a = b;      // CE: incompatible types: int[][] cannot be converted to int[]
b = a;      // CE: incompatible types: int[] cannot be converted to int[][]
a = b[0];   // valid — b[0] is int[]
b[0] = a;   // valid
```

How to see it: `b` is an array of `int[]`. So `b[0]` has type `int[]`, which
matches `a`.

Three-dimensional:

```java
int[][][] x = new int[2][3][4];
int[][] y;
int[] z;

y = x[0];    // valid — x[0] is int[][]
z = x[0][0]; // valid — x[0][0] is int[]
z = x[0];    // CE: incompatible types: int[][] cannot be converted to int[]
```

Exam pattern: "which assignments compile?" with a mix of `a`, `a[0]`, `a[0][0]`.

## Element-level promotion does not apply to the array variable

This is the trap Durga builds toward.

At **element** level, `char` promotes to `int`:

```java
int[] a = new int[3];
a[0] = 'a';   // valid — char → int, stores 97
```

At **variable** level, `char[]` is **not** a subtype of `int[]`:

```java
char[] ch = {'a', 'b', 'c'};
int[] i = {10, 20, 30};
i = ch;   // CE: incompatible types: char[] cannot be converted to int[]
ch = i;   // CE: incompatible types: int[] cannot be converted to char[]
```

Why: an array's type is `char[]` or `int[]`. Those are different types in the
type system. Promotion rules are for **values**, not for **array types**.

Same idea:

```java
byte[] b = {10, 20};
int[] i = {30, 40};
i = b;    // CE: incompatible types: byte[] cannot be converted to int[]
```

Even though `byte` promotes to `int` at the element level.

## Object arrays and children — variable assignment is allowed

Arrays are objects. For **reference** element types, Java allows:

**child-type array → parent-type array variable**

```java
String[] s = {"A", "B", "C"};
Object[] o = s;     // valid
```

`String` is a child of `Object`, so `String[]` may be assigned to `Object[]`.

Without a cast, the reverse is a compile error:

```java
Object[] o = s;
String[] back = o;  // CE: incompatible types: Object[] cannot be converted to String[]
```

The reverse *with* a cast compiles, but whether it survives at runtime
depends on something narrower than "are the elements Strings":

```java
String[] real = {"A", "B"};
Object[] o = real;               // upcast — o still refers to the same String[] object
String[] back = (String[]) o;    // valid — the object's real type IS String[]
```

> ❗ **Correction — a cast to `String[]` does not succeed just because every
> element happens to be a `String`.**
> The array's own runtime type is fixed by how it was **created**, not by what
> is stored in it. `new Object[]{...}` is an `Object[]` object forever, even
> if every slot holds a `String`:
>
> ```java
> Object[] o2 = new Object[]{"A", "B"};
> String[] s2 = (String[]) o2;   // compiles; throws at runtime
> ```
>
> ```text
> Exception in thread "main" java.lang.ClassCastException: class [Ljava.lang.Object;
> cannot be cast to class [Ljava.lang.String; ([Ljava.lang.Object; and
> [Ljava.lang.String; are in module java.base of loader 'bootstrap')
> ```
>
> That is a **`ClassCastException`, thrown immediately on the cast** — it does
> not matter that both elements are Strings, because the check is on the array
> object's own component type, not on its contents. Contrast with the case
> above: `back = (String[]) o` succeeds only because `o` was never anything
> but a reference to the original `String[]` object — the cast is undoing an
> earlier upcast of that *same object*, not converting an `Object[]` into
> something it never was. Verified on JDK 26; the mechanism has not changed
> since Java 5, when array covariance and `ClassCastException` semantics were
> fixed by JLS §10.10.

More Durga examples:

```java
Runnable[] r = new Runnable[5];
r[0] = new Thread();
Object[] o = r;     // valid — Runnable[] to Object[]

Number[] n = new Number[3];
n[0] = new Integer(10);
n[1] = new Double(10.5);
Object[] o2 = n;    // valid
```

> ⚠️ **Modern Java — `new Integer(10)` and `new Double(10.5)` are deprecated.**
> Since **Java 9**, every boxed-primitive wrapper constructor —
> `new Integer(int)`, `new Double(double)`, `new Long(long)`, `new Boolean(boolean)`,
> … — carries `@Deprecated(since="9")` in the JDK source. `javac -Xlint:deprecation`
> flags both lines above:
>
> ```text
> warning: [deprecation] Integer(int) in Integer has been deprecated
> warning: [deprecation] Double(double) in Double has been deprecated
> ```
>
> They still compile and still behave exactly as taught here — this is a
> warning, not an error, and legacy code full of `new Integer(...)` keeps
> working. The reason for the deprecation: the constructor always allocates a
> **new** object, while autoboxing (`Integer n = 10;`) and `Integer.valueOf(10)`
> reuse a shared cache for values **−128 to 127** (JLS §5.1.7). Modern code
> writes `Number[] n = {10, 10.5};` or `Integer.valueOf(10)` and never calls
> `new Integer(...)` directly.

```java
Thread[] t = new Thread[5];
Runnable[] r = t;   // valid — Thread implements Runnable
t = r;              // CE: incompatible types: Runnable[] cannot be converted to Thread[]
```

## After parent = child, be careful writing elements

```java
String[] s = new String[3];
Object[] o = s;
o[0] = new Integer(10);  // compiles (Object slot) — ArrayStoreException at runtime
```

```text
Exception in thread "main" java.lang.ArrayStoreException: java.lang.Integer
```

Because the **real** object is still a `String[]`. The compiler only sees
`Object[]`. The JVM checks the actual component type on every store.

This is the array version of polymorphism plus a heap-level safety check.
Durga uses it as an exam bomb.

## Jagged leftovers

Still legal after assignment:

```java
int[][] a = new int[3][];
a[0] = new int[2];
a[1] = new int[4];
a[0] = new int[]{10, 20, 30}; // replace entire row (anonymous array from part 3)
```

`a[0]` is an `int[]` variable. Assigning another `int[]` to it is variable
assignment at the row level.

## `null` assignment

```java
int[] a = {10, 20, 30};
a = null;   // valid — a is a reference
// a[0] = 10;  // NPE at runtime
```

Primitive arrays are still objects. The name `a` can hold `null`. You cannot
write `int x = null;`.

> ⚠️ **Modern Java — the NPE message got a lot more useful.**
> Since **Java 14** (JEP 358, opt-in) and default from **Java 15**, a
> `NullPointerException` names the exact failing expression:
>
> ```text
> Exception in thread "main" java.lang.NullPointerException:
> Cannot load from int array because "a" is null
> ```
>
> On Java 6/7 the same crash gave only `Exception in thread "main"
> java.lang.NullPointerException` with a stack trace and no detail message —
> you had to work out which reference was `null` from the line number alone.
> Reproduce the old behaviour on a current JDK with
> `java -XX:-ShowCodeDetailsInExceptionMessages`.

## What becomes eligible for GC

```java
int[] a = new int[3];
int[] b = new int[4];
a = b;
```

The `new int[3]` object is eligible for GC (unless some other name still
points to it).

```java
int[][] x = new int[2][3];
x[0] = null;
```

Only that inner `int[3]` row is dropped, not the whole 2-D object.

## One-slide summary

| Left | Right | Result |
|---|---|---|
| `int[] a` | `int[] b` | valid, even if lengths differ |
| `int[] a` | `int[][] b` | CE |
| `int[] a` | `b[0]` if `b` is `int[][]` | valid |
| `int[] a` | `char[] ch` | CE |
| `int[] a` | `byte[] b` | CE |
| `Object[] o` | `String[] s` | valid |
| `String[] s` | `Object[] o` | CE (cast possible, `ClassCastException` risk) |
| `Runnable[] r` | `Thread[] t` | valid |
| `int[] a` | `null` | valid |

## Complete program from the lecture

```java
class ArrayVarAssign {
    public static void main(String[] args) {
        int[] a = {10, 20, 30, 40, 50};
        int[] b = {60, 70};
        a = b;
        System.out.println(a.length); // 2

        int[][] m = new int[2][3];
        a = m[0];                     // valid
        // a = m;                     // CE: incompatible types: int[][] cannot be converted to int[]

        char[] ch = {'a', 'b'};
        // a = ch;                    // CE: incompatible types: char[] cannot be converted to int[]

        String[] s = {"durga", "soft"};
        Object[] o = s;               // valid
        System.out.println(o[0]);     // durga
        // o[0] = 10;                 // compiles (autoboxed to Integer) — ArrayStoreException at runtime

        Object[] o2 = new Object[]{"A", "B"};
        // String[] wrong = (String[]) o2;  // compiles — ClassCastException at runtime:
        // elements being Strings does not matter; o2's real type is Object[]

        Number[] n = new Number[3];
        n[0] = new Integer(10);       // deprecated since Java 9 — still legal
        n[1] = new Double(10.5);      // same
        Object[] onums = n;           // valid

        Thread[] t = new Thread[5];
        Runnable[] r = t;              // valid — Thread implements Runnable
        // t = r;                      // CE: incompatible types: Runnable[] cannot be converted to Thread[]

        int[][] jag = new int[3][];
        jag[0] = new int[2];
        jag[1] = new int[4];
        jag[0] = new int[]{10, 20, 30}; // replace entire row

        a = null;                      // valid — a is a reference
        // System.out.println(a[0]);   // NullPointerException at runtime
    }
}
```

## Rules to memorize

1. Array **variable** assignment requires matching **type + dimension**, not matching length.
2. `a = b` makes both names point to the same object; the old object may be GC'd.
3. `int[]` and `int[][]` never assign to each other; use `b[0]` to drop one dimension.
4. Primitive promotion (`char` → `int`) does **not** make `char[]` assignable to `int[]`.
5. Child `[]` **is** assignable to parent `[]` (`String[]` → `Object[]`, `Thread[]` → `Runnable[]`).
6. Storing the wrong runtime element into that parent view throws `ArrayStoreException` — at the store, not at the cast.
7. Casting a reference **down** to `String[]` only survives if the object's own runtime type is (a subtype of) `String[]` — element contents never override that check.

## Exam and interview points

1. **Lengths do not have to match** for `a = b` to compile — only type and dimension do. `int[5]` and `int[2]` assign to each other freely.
2. **`char[]` to `int[]` is a compile error**, even though a single `char` promotes to `int` at the element level. Promotion is for values inside the array, never for the array's own type.
3. **`int[]` and `int[][]` are unrelated types.** `b[0]` (where `b` is `int[][]`) drops one dimension and is assignable to `int[]`; `b` itself never is.
4. **`String[]` assigns to `Object[]`** without a cast (array covariance); the reverse needs a cast and can fail at runtime.
5. **A cast to `String[]` throws `ClassCastException` whenever the array's real type is not `String[]`, regardless of what is stored in it.** `new Object[]{"A","B"}` cast to `String[]` fails even though both elements are Strings — the check is on the array object's own component type (JLS §10.10), not on element contents.
6. **`ArrayStoreException` is a runtime check, not a compile check.** `Object[] o = new String[3]; o[0] = Integer.valueOf(10);` compiles because the compiler only sees `Object[]`; the JVM rejects the store because the real array is `String[]`.
7. **`Thread[]` assigns to `Runnable[]`** because `Thread implements Runnable`; the reverse needs a cast and is exactly the same `ArrayStoreException`/`ClassCastException` trap as `String[]`/`Object[]`.
8. **Arrays are objects, so array variables accept `null`.** `int[] a = null;` compiles; `int x = null;` does not — that is the line between a reference type and a primitive.
9. **`new Integer(10)` and every other boxed-wrapper constructor have been deprecated since Java 9** (`@Deprecated`, not yet removed). They still work as taught; prefer autoboxing or `Integer.valueOf(int)`.
10. **NullPointerException messages got a detail line in Java 14/15** (JEP 358, "helpful NPEs") — `Cannot load from int array because "a" is null` instead of a bare exception with no explanation.
11. **The classic exam bomb sequence:** declare `Object[] o = someStringArray;`, store any non-`String`, and the trap is that it *compiles* — the failure only shows up when the line actually runs.
12. **This closes the arrays topic**: declaration → creation → initialization → `length` vs. `length()` → anonymous arrays → element assignments → variable assignments. Next up: types of variables.

---

**Next:** Video 010 — Types of Variables Part 1
