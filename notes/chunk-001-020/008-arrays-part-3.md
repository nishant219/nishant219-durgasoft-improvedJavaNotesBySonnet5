# Video 008 — Arrays part 3

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-8 || Arrays Part-3

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 8 of 203 |
| Series | Language Fundamentals · Part 8 of 16 |
| Topic | Arrays part 3 |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 38m 56s (5936 seconds) |
| Video ID | I_aJgAmDYPk |
| Watch | https://www.youtube.com/watch?v=I_aJgAmDYPk |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Last session (video 007) finished array **initialization** — default values,
overriding those defaults, and `ArrayIndexOutOfBoundsException`. This session
works through the next items on the board:

1. Array **declaration, creation, and initialization in a single line** — the `{…}` shortcut
2. Extending the shortcut to **multi-dimensional arrays**, plus an exam-style 3-D indexing drill
3. Why the shortcut **cannot be split across two statements** (`illegal start of expression`)
4. **`length` versus `length()`** — array final variable vs `String` final method; multi-dimensional `length` is the **base size only**
5. **Anonymous arrays** — nameless, one-time use; `new int[]{10, 20, 30}`; no size in that form; naming one later means it is no longer anonymous
6. **Array element assignments** in four flavours — primitive arrays (implicit promotion), object-type arrays (declared type or child), abstract-class arrays (`Number`), interface-type arrays (`Runnable[]` + `Thread`)
7. A summary table of which element types each array kind allows

The lecture ends mid-sentence on **array variable assignments** — assigning one
array reference to another, as opposed to assigning one element. Sir names
that topic and stops; it is taught in full next video, so it is not written up
below.

---

## 00:05 — Declaration, creation, and initialization in one line

The long form of building an array is five lines:

```java
int[] x;                 // declare
x = new int[3];          // create
x[0] = 10;                // initialize
x[1] = 20;
x[2] = 30;
```

There is a shortcut that folds all five into **one line**:

```java
int[] x = {10, 20, 30};
```

Internally the same work happens — the same object gets created and the same
three slots get filled. There is **no performance difference**; the shortcut
exists purely for the programmer's convenience.

The same shortcut works for any element type:

```java
char[] ch = {'a', 'e', 'i', 'o', 'u'};    // vowels
String[] names = {"A", "AA", "AAA"};     // a group of String objects
```

You never write the size in this form. Listing the elements **is** the size —
that is the whole point of "you are not required to specify it separately."

### 05:36 — Heap vs SCP: where the pieces of a `String[]` shortcut live

Every Java object is created on the **heap** — the array object itself is no
exception. But `"A"`, `"AA"`, and `"AAA"` are **string literals**, and every
literal gets one object in the **SCP** (string constant pool). The array's
slots do not hold the characters directly; they hold **references** to the
SCP objects.

- Array object → heap
- String literals → SCP
- Array slots → references pointing at those SCP objects

This is the same SCP idea covered in the literals lectures — Sir repeats it
here only so you do not picture the strings as sitting *inside* the array
object.

> ⚠️ **Modern Java — the SCP has lived inside the main heap since Java 7.**
> Before **Java 7u40** (JDK-6962931, "Move interned strings out of the
> permanent generation"), the string pool sat in **PermGen** — a separate
> generation from the object heap, which is exactly why Sir draws it as its
> own box next to "the heap." From Java 7 onward the pool is just a table of
> references living *inside* the main heap, and PermGen itself disappeared in
> **Java 8**, replaced by **Metaspace** (which holds class metadata, not
> strings, and by default is not even part of the heap). The rule Sir
> teaches — array object on the heap, literal in the SCP, slot holds a
> reference — is still exactly right. Only the SCP's *address*, so to speak,
> moved from a side room into the same building.

## 06:53 — The shortcut also works for multi-dimensional arrays

Do not assume `{…}` is a one-dimensional trick. It extends cleanly to two and
three dimensions. A jagged 2-D example: first inner array `10, 20`, second
inner array `30, 40, 50`.

```java
int[][] x = {{10, 20}, {30, 40, 50}};
```

A 2-D array is, underneath, still "one dimension of arrays": the outer array
has two elements, and each element is itself a 1-D array — the first of size
2, the second of size 3. Draw that picture before you trust any answer about
what a given index returns.

## 09:51 — Exam drill: convert the 3-D shortcut to memory before answering

This is exactly the kind of thing OCJP asks: a nested brace initializer, and
several `x[i][j][k]` questions fired at it. **Do not answer by staring at the
braces** — most people guess wrong that way. Convert to a diagram first, then
read off indexes.

```java
int[][][] x = {
    { {10, 20, 30}, {40, 50, 60} },
    { {70, 80},     {90, 100, 110} }
};
```

Memory, read out loud:

- Dimension **3**. Top-level base size **2** — two 2-D arrays.
- `x[0]` is a 2-D array of base size 2: `x[0][0] = {10, 20, 30}`, `x[0][1] = {40, 50, 60}`.
- `x[1]` is a 2-D array too: `x[1][0] = {70, 80}` (length 2), `x[1][1] = {90, 100, 110}`.

| Expression | Result |
|---|---|
| `x[0][1][2]` | `60` |
| `x[1][0][1]` | `80` (not `70` — `70` is `x[1][0][0]`) |
| `x[2][0][0]` | **RE** `ArrayIndexOutOfBoundsException` — the top level has no index 2 |
| `x[1][2][0]` | **RE** `ArrayIndexOutOfBoundsException` — `x[1]` has no index 2 |
| `x[1][1][1]` | `100` |
| `x[2][1][0]` | **RE** `ArrayIndexOutOfBoundsException` — same reason as row 3 |

Students who answer without the diagram guess `70`, `60`, or `40` with no
confidence — and mostly land on the wrong row. Once the memory picture exists,
every one of these becomes mechanical, including the deeper indexes Sir keeps
firing at the class (`x[2][2][1][0]` and similar): the first out-of-range
index anywhere in the chain is where the exception fires, regardless of how
many indexes follow it.

## 17:15 — The shortcut must stay in one statement

Ordinary primitive assignment can be split across two lines with no penalty:

```java
int x = 10;   // valid — one line
int x;
x = 10;       // also valid — split into two lines
```

Applying the same instinct to the array shortcut looks reasonable, and is not:

```java
int[] x = {10, 20, 30};   // valid — one line

int[] x;
x = {10, 20, 30};         // INVALID — CE: illegal start of expression
```

The one-liner compiles cleanly. Splitting it produces:

```text
error: illegal start of expression
```

— and depending on the exact split, the compiler may also add `not a
statement` or `';' expected`. `{10, 20, 30}` is not a general-purpose
expression you can drop on the right of any `=`. It is legal only as part of
a **declaration** initializer (or, as the next section shows, inside `new
int[]{…}` — an anonymous array).

> **Board:** If we want to use this shortcut, compulsory we should perform all
> activities in a single line. If we try to divide into multiple statements,
> we get a compile-time error.

> ⚠️ **Modern Java — `var` does not get you around this either.**
> Java 10's `var` still requires an explicit target type before it will accept
> a bare `{…}` initializer, so the bare form is a compile error under `var`
> too, with a clearer message pointing at the actual problem:
>
> ```java
> var x = {10, 20, 30};        // CE: cannot infer type for local variable x
>                               //     (array initializer needs an explicit target-type)
> var x = new int[]{10, 20, 30};   // valid — the `new int[]` supplies the type
> ```
>
> Same underlying rule Sir teaches: the bare brace form only ever works where
> the compiler already knows the array's type from context. `var` removes the
> type from the left side of `=`, so it removes exactly the context the bare
> form needs.

## 22:07 — `length` versus `length()`

### 22:40 — Array `length`: a final variable, not a method

```java
int[] x = new int[6];
System.out.println(x.length());   // CE
System.out.println(x.length);     // 6
```

`x.length()` fails to compile:

```text
error: cannot find symbol
  symbol:   method length()
  location: variable x of type int[]
```

There is no `length` *method* on an array type. `x.length` — no parentheses —
prints `6`. `length` is a **variable** applicable to arrays, and it holds the
array's **size**.

Is it final? Yes: once an array is created, its size can never change, so
there is never a chance to reassign `length`. **`length` is a final variable
applicable for arrays.**

> **Board:** `length` is a final variable applicable for arrays. The `length`
> variable represents the size of the array.

### 27:02 — `String.length()`: a final method, not a variable

```java
String s = "durga";
System.out.println(s.length);     // CE
System.out.println(s.length());   // 5
```

`s.length` fails:

```text
error: cannot find symbol
  symbol:   variable length
  location: variable s of type String
```

`length` as a variable is **not applicable** to `String`. `s.length()` —
with parentheses — returns `5`: the number of characters (d-u-r-g-a).
**`length()` is a method applicable to `String` objects**, returning the
character count.

Sir's argument for why it counts as final, for exam purposes:

1. `length()` is declared in `String`.
2. `String` is a **final class**.
3. A final class cannot be subclassed.
4. Overriding requires a subclass. No subclass → no overriding.
5. Therefore every method inside a final class is, in effect, unoverridable —
   "final by default." He flags that he will restate this same conclusion
   when the course reaches OOP.

> ❗ **Correction — "final by default" describes behaviour, not the bytecode.**
> The reasoning above is correct about *outcome*: nobody can override
> `String.length()`, because nobody can subclass `String`. But the method
> itself does not carry the literal `final` modifier — `javap` shows it as
> plain `public int length()`, and reflection agrees:
>
> ```java
> java.lang.reflect.Method m = String.class.getMethod("length");
> System.out.println(java.lang.reflect.Modifier.isFinal(m.getModifiers()));
> // false — verified on JDK 26
> ```
> `Modifier.isFinal` returns `false`. Sir's exam answer — "unoverridable
> because the class is final" — is exactly the reasoning OCJP wants, and it
> has never been wrong about behaviour. Just do not repeat it as "the JVM
> marks it `final`," because that specific claim is checkable and false; the
> `final`-ness here is a **consequence of the class**, not a modifier on the
> method.

So: array `length` is a final **variable**; `String.length()` is an
effectively-final **method** — final in what it does, not in how the class
file spells it.

### 32:42 — The line that pairs them

> `length` — variable, applicable for arrays, not for `String` objects.
> `length()` — method, applicable for `String` objects, not for arrays.

### 34:06 — Exam combo: `String[]`

```java
String[] s = {"A", "AA", "AAA"};
System.out.println(s.length);      // ?
System.out.println(s.length());    // ?
System.out.println(s[0].length);   // ?
System.out.println(s[0].length()); // ?
```

| Code | Valid? | Result |
|---|---|---|
| `s.length` | yes | `3` — `s` is the array; three elements |
| `s.length()` | no | CE: cannot find symbol — method `length()`, location `String[]` |
| `s[0].length` | no | CE: cannot find symbol — variable `length`, location `String` |
| `s[0].length()` | yes | `1` — the first element is `"A"` |

The classic trap: `s` is an array (so use `.length`), but `s[0]` is a `String`
(so use `.length()`). Mixing the two in either direction is a compile error,
and the error message names exactly which one you got backwards.

### 40:05 — Multi-dimensional arrays: `length` is base size only

```java
int[][] x = new int[6][3];
System.out.println(x.length);      // ?
System.out.println(x[0].length);   // ?
```

The array can hold 18 `int`s total. Is `x.length` `6`, `18`, or `9`? It is
**6**. Even a 2-D array is basically one-dimensional: `x` has 6 elements, and
each element happens to be an array of size 3.

> **Board:** In multi-dimensional arrays, the `length` variable represents
> only the base size, not the total size.

`x[0].length` is `3`. There is **no direct way** to find the total element
count of a multi-dimensional array, because the size at the next level is not
guaranteed uniform — one row might be size 2, another size 4. Indirectly, you
sum the rows yourself:

```java
int total = x[0].length + x[1].length + x[2].length + x[3].length
          + x[4].length + x[5].length;
```

That finishes `length` versus `length()`.

## 46:30 — Anonymous arrays

### 46:36 — What an anonymous array is, and why

**Anonymous** means nameless. Sometimes an array is declared without a name;
such nameless arrays are, by definition, **anonymous arrays**. If an array
has a name, size is `x.length`, elements are `x[0]`, `x[1]`, … — every later
use goes through that name. So a nameless array is only useful for **instant,
one-time use**: if you will never touch it again after this line, it does not
need a name.

Sir's two analogies carry the same point. Someone on the road tells you where
a building is — you never take their contact details, because you will never
need to reach them again. A city-bus conductor sells you a ticket — you never
ask for their number either, because tomorrow's conductor will be someone
else. **Once you *would* contact someone again, they stop being anonymous** —
which is the hinge for the "naming it later" case below.

> **Board:** Sometimes we can declare an array without a name. Such nameless
> arrays are called anonymous arrays, and the main purpose of an anonymous
> array is just instant, one-time use.

### 53:36 — Writing one: the `sum` example

```java
class Test {
    public static void main(String[] args) {
        sum(new int[]{10, 20, 30, 40});
    }

    public static void sum(int[] x) {
        int total = 0;
        for (int x1 : x) {          // for-each loop
            total = total + x1;
        }
        System.out.println("The sum is " + total);
    }
}
```

`sum` expects an `int[]`. The values `10, 20, 30, 40` need an array only to
make this one call — after `sum` returns, that array is never touched again;
there is not even a way to print its first element, because it has no name.
The creation form:

```java
new int[]{10, 20, 30, 40}
```

`new`, then the element type, then the values in braces — no size. The same
form works for any element type (`char[]`, `String[]`, …).

### 58:56 — Trap: never give an anonymous array a size

Muscle memory after typing `new int` reaches for a size — `new int[3]`. Doing
that *and* listing values is a compile error:

```java
new int[3]{10, 20, 30};   // INVALID
new int[]{10, 20, 30};    // VALID
```

```text
error: array creation with both dimension expression and initialization is illegal
```

You are already telling the compiler the count by listing the values; adding
a size is redundant information the language refuses to accept.

> **Board:** While creating anonymous arrays, we cannot specify the size —
> because we are already providing the number of elements.

### 1:01:28 — Multi-dimensional anonymous arrays

The technique is not limited to one dimension:

```java
new int[][]{{10, 20}, {30, 40, 50}}
```

A valid 2-D anonymous array — an array of two 1-D arrays, `{10, 20}` and
`{30, 40, 50}`.

### 1:03:19 — Give it a name later, and it stops being anonymous

Back to the train-neighbour version of the same story: he starts as another
anonymous stranger, but once you take his card because you *will* be in touch
again, he is no longer anonymous. Same for arrays:

```java
int[] x = new int[]{10, 20, 30};
```

Created in anonymous *style*, then bound to `x` because it turns out you do
need it in later lines. **Based on the requirement, you may give an anonymous
array a name — at which point it simply is not anonymous any more.**
Perfectly valid; nothing exotic about it.

### 1:11:04 — Why anonymous was the right call for `sum`

In the `sum` example, an array was required purely to satisfy the method
signature; nothing after the call ever needed it again. For a one-time
requirement like that, anonymous is the right choice — a name would only add
a variable nobody reads.

## 1:12:55 — Array element assignments

This section is about **element** assignment (`a[i] = …`) — assigning one
array *variable* to another is the topic Sir opens at the very end and
defers to the next video.

### 1:13:14 — Case 1: primitive-type arrays

```java
int[] x = new int[6];

x[0] = 10;      // valid — int
x[1] = 'a';     // valid — char promoted to int; stores 97
byte b = 20;
x[2] = b;       // valid — byte promoted to int
short s = 30;
x[3] = s;       // valid — short promoted to int
x[4] = 10L;     // INVALID
```

```text
error: incompatible types: possible lossy conversion from long to int
```

> ⚠️ **Modern Java — the compiler's wording for this changed by JDK 8.**
> Sir dictates the Java 6-era shape of this message: `possible loss of
> precision`, `found: long`, `required: int`, printed across three lines.
> Every JDK from 8 onward (verified here on JDK 26) compresses it into the
> one-liner shown above. Same defect, same cause — only the diagnostic layout
> moved. (Video 002 covers the full before/after table for every narrowing
> message.)

This is the same promotion chart used for primitive assignment generally:
`byte → short → int ← char`, then `int → long → float → double`. Wherever
`int` is required, `byte`, `short`, `char`, and `int` are all accepted.

**In the case of primitive-type arrays, an array element may be any type
that can be implicitly promoted to the declared component type.**

- `int[]` accepts: `byte`, `short`, `char`, `int`.
- `float[]` accepts: `byte`, `short`, `char`, `int`, `long`, `float` — everything
  that promotes to `float`, i.e. everything except `double` (and `boolean`,
  which never promotes to anything numeric).

### 1:19:33 — Case 2: object-type arrays

`Object[]`, `String[]`, `Student[]`, `Customer[]` — arrays of reference types.

```java
Object[] a = new Object[10];
a[0] = new Object();           // valid — declared type
a[1] = new String("durga");    // valid — String is a child of Object
a[2] = new Integer(10);        // valid — Integer is a child of Object
```

A second example, using `Number` for its own case below:

```java
Number[] n = new Number[10];
n[0] = new Integer(10);        // valid — Integer is a child of Number
n[1] = new Double(10.5);       // valid — Double is a child of Number
n[2] = new String("durga");    // INVALID
```

```text
error: incompatible types: String cannot be converted to Number
```

`String` is not, and never has been, a child of `Number`.

**In the case of object-type arrays, an array element may be either the
declared type or any of its child-class objects.**

> ❗ **Correction — `Number`'s direct subclasses are not only the six numeric
> wrappers.** Sir names `Byte, Short, Integer, Long, Float, Double`, which is
> the right list for "which wrapper types can I store here" — but the
> `Number` hierarchy is older and wider than that even in Java 6. `BigInteger`
> and `BigDecimal` (`java.math`) and `AtomicInteger` and `AtomicLong`
> (`java.util.concurrent.atomic`, present since Java 5) also directly extend
> `Number` — verified here with `Class#getSuperclass()` on JDK 26. If an exam
> or interview question lists one of those four alongside the wrappers and
> calls it invalid for a `Number[]`, that question is wrong, not you.

> ⚠️ **Modern Java — `new Integer(10)` and `new Double(10.5)` are deprecated
> since Java 9.** They still compile — this is not a removal — but every
> single-argument constructor on a primitive wrapper (`Byte`, `Short`,
> `Integer`, `Long`, `Float`, `Double`, `Boolean`, `Character`) carries
> `@Deprecated(since="9")`, verified here by decompiling `java.lang.Integer`
> on JDK 26:
>
> ```text
> warning: [deprecation] Integer(int) in Integer has been deprecated
> ```
>
> The reason: autoboxing and the pooled `Integer.valueOf(int)` do the same
> job without guaranteeing a fresh object every time. Modern code writes
> `n[0] = 10;` (autoboxed) or `n[0] = Integer.valueOf(10);`. Sir's teaching
> point — "a child-class object is allowed here" — is unaffected either way;
> only the specific constructor call is now flagged.

### 1:34:36 — Abstract-class arrays are just object arrays with no direct instances

This case is the `Number[]` example already covered, looked at from a
different angle. `Number` is an **abstract class** — `new Number()` is
illegal — but a `Number[]` is perfectly legal, and its elements are the
concrete subclasses (`Integer`, `Double`, …).

**For abstract-class-type arrays, child-class objects are allowed as
elements** — exactly the same rule as Case 2, restated because the component
type happens to be abstract.

### 1:26:55 — Case 3: interface-type arrays

```java
Runnable[] r = new Runnable[10];
```

The instinctive answer is "invalid — `Runnable` is an interface, you cannot
instantiate an interface." That instinct is about the wrong object: **this
line does not create a `Runnable`; it creates a `Runnable[]`.** An array
object of interface-component type is perfectly legal — only an *instance* of
the interface itself is impossible.

What can occupy a slot? `Runnable`'s implementation class `Thread` — every
`Thread` object *is-a* `Runnable`:

```java
r[0] = new Thread();          // valid
r[1] = new String("durga");   // INVALID
```

```text
error: incompatible types: String cannot be converted to Runnable
```

A student in the room suggests `Throwable` as another candidate — rejected:
`Throwable` does not implement `Runnable`, directly or indirectly. It roots
the exception hierarchy, not the threading one.

**For interface-type arrays, an array element must be an object of an
implementation class.**

> ⚠️ **Modern Java — a lambda can fill this slot too.** Since **Java 8**,
> `Runnable` is a functional interface (one abstract method), so a lambda
> expression is a legal `Runnable` implementation with no named class at all:
>
> ```java
> r[1] = () -> System.out.println("lambda runnable");   // valid since Java 8
> r[1].run();                                             // prints the line
> ```
>
> Verified compiling and running on JDK 26. `new Thread()` is still exactly
> as valid as Sir teaches — nothing about `Thread` changed — this is simply a
> second, shorter way to produce an implementation-class object that did not
> exist when this was recorded.

### 1:32:26 — The summary table

| Array type | Allowed element types |
|---|---|
| Primitive arrays | Any type implicitly promotable to the declared component type |
| Object-type arrays | The declared type, or any of its child-class objects |
| Abstract-class-type arrays | Child-class objects |
| Interface-type arrays | Implementation-class objects |

That is array **element** assignments, complete.

## 1:38:31 — Bridge: array *variable* assignments

The last heading Sir puts on the board is **array variable assignments** —
assigning one array *reference* to another (`int[] a = b;`, mixing 1-D and
2-D references, and the compatibility rules that come with that). He names
the topic and the video ends there. That is arrays **part 4** — covered in
the next note, not here.

---

## Code from the lecture

Verified against `javac`/`java` on JDK 26; every line marked `CE` fails to
compile exactly as commented, and every printed value matches the run.

```java
class Test {
    public static void main(String[] args) {
        // shortcut: five lines become one
        int[] x = {10, 20, 30};
        char[] ch = {'a', 'e', 'i', 'o', 'u'};
        String[] names = {"A", "AA", "AAA"};

        int[][] two = {{10, 20}, {30, 40, 50}};

        int[][][] three = {
            { {10, 20, 30}, {40, 50, 60} },
            { {70, 80},     {90, 100, 110} }
        };
        System.out.println(three[0][1][2]); // 60
        System.out.println(three[1][0][1]); // 80
        System.out.println(three[1][1][1]); // 100
        // three[2][0][0]  → ArrayIndexOutOfBoundsException
        // three[1][2][0]  → ArrayIndexOutOfBoundsException

        // int[] split;
        // split = {10, 20, 30};   // CE: illegal start of expression

        int[] six = new int[6];
        // System.out.println(six.length());   // CE: cannot find symbol — method length()
        System.out.println(six.length);         // 6

        String s = "durga";
        // System.out.println(s.length);        // CE: cannot find symbol — variable length
        System.out.println(s.length());          // 5

        String[] arr = {"A", "AA", "AAA"};
        System.out.println(arr.length);           // 3
        // System.out.println(arr.length());      // CE
        // System.out.println(arr[0].length);     // CE
        System.out.println(arr[0].length());      // 1

        int[][] m = new int[6][3];
        System.out.println(m.length);       // 6  (base only, not 18)
        System.out.println(m[0].length);    // 3
        // total size indirectly: m[0].length + m[1].length + ...

        sum(new int[]{10, 20, 30, 40});
        // new int[3]{10, 20, 30};             // CE: dimension + initializer together
        int[] named = new int[]{10, 20, 30};    // no longer anonymous

        // Case 1 — primitive
        int[] p = new int[5];
        p[0] = 10;
        p[1] = 'a';          // 97
        byte b = 20;
        p[2] = b;
        short sh = 30;
        p[3] = sh;
        // p[4] = 10L;       // CE: incompatible types: possible lossy conversion from long to int

        // Case 2 — Object / Number
        Object[] o = new Object[10];
        o[0] = new Object();
        o[1] = new String("durga");
        o[2] = new Integer(10);   // compiles with a deprecation warning (Java 9+)

        Number[] n = new Number[10];
        n[0] = new Integer(10);   // deprecation warning (Java 9+)
        n[1] = new Double(10.5);  // deprecation warning (Java 9+)
        // n[2] = new String("durga");   // CE: incompatible types: String cannot be converted to Number

        // Case 3 — interface
        Runnable[] r = new Runnable[10];   // valid: array object, not a Runnable instance
        r[0] = new Thread();
        r[1] = () -> System.out.println("lambda runnable");   // valid since Java 8
        // r[1] = new String("durga");   // CE: incompatible types: String cannot be converted to Runnable
    }

    public static void sum(int[] x) {
        int total = 0;
        for (int x1 : x) {
            total = total + x1;
        }
        System.out.println("The sum is " + total);
    }
}
```

## Rules to memorize

1. Shortcut: `int[] x = {10, 20, 30};` — declare, create, and initialize in one
   line. Size is implied by the number of elements; no performance difference
   from the five-line form.
2. Same shortcut for `char[]`, `String[]`, and multi-dimensional arrays:
   `int[][] x = {{10, 20}, {30, 40, 50}}`.
3. `String[]` shortcut: array object on the heap; literals in the SCP (inside
   the heap since Java 7); array slots hold references.
4. The `{…}` shortcut **must** be on the declaration line. `int[] x; x =
   {10, 20, 30};` → `illegal start of expression`. `var` does not create a new
   loophole here — it needs the type from `new int[]{…}` just like everything
   else.
5. For 3-D brace nesting, draw the memory picture before answering `x[i][j][k]`.
6. **`length`**: final variable, arrays only, means size — in a
   multi-dimensional array, **base size only**, never the total cell count.
7. **`length()`**: method on `String` objects only, means character count.
   Unoverridable because `String` is final and has no subclass — but that is
   a consequence of the class, not a `final` modifier on the method itself.
8. `String[] s`: `s.length` OK; `s.length()` CE; `s[0].length` CE;
   `s[0].length()` OK.
9. No direct total-size API for a multi-dimensional array; sum the inner
   `.length` values yourself.
10. Anonymous array = nameless, one-time / instant use. Syntax `new
    int[]{10, 20, 30}` — never `new int[3]{…}`, which is a compile error
    because you would be specifying both a size and a count of elements.
11. `int[] x = new int[]{10, 20, 30};` is valid; the moment it has a name, it
    is no longer anonymous.
12. Primitive elements: any type implicitly promotable to the component type
    (`int[]` ← `byte`/`short`/`char`/`int`; `float[]` ← those plus
    `long`/`float`; never `double` into anything, never `long` into `int`).
13. Object elements: declared type or child. `Number[]` cannot hold a
    `String`. Modern code prefers autoboxing/`Integer.valueOf(...)` over
    `new Integer(...)` (deprecated since Java 9), but the array-element rule
    itself is unchanged.
14. Abstract component type (e.g. `Number`): child-class objects, same rule
    as any object-type array.
15. Interface component type: `new Runnable[10]` is valid (an array object),
    but its elements must be implementation-class objects — `Thread`, or (since
    Java 8) a lambda expression — never `String`, never `Throwable`.

## Exam and interview points

1. **The `{…}` shortcut is one statement, no exceptions.** Splitting
   `int[] x; x = {10, 20, 30};` looks like splitting `int x; x = 10;`, but it
   is a compile error either way you try it — `illegal start of expression`.
   The only legal two-step form is `x = new int[]{10, 20, 30};`.
2. **`x.length()` on an array is CE "method not found"; `s.length` on a
   `String` is CE "variable not found."** Which error *kind* — method vs.
   variable — is itself worth a mark; the compiler tells you exactly which
   half of the rule you broke.
3. **`new int[6][3]` then `x.length == 18` is the classic trap.** The answer
   is `6` — the base size — every time.
4. **`new int[3]{1, 2, 3}` is illegal; `new int[]{1, 2, 3}` is legal.** Giving
   both a size and an initializer list is a compile error, never a warning.
5. **"`Runnable[] r = new Runnable[10];` is invalid because you can't
   instantiate an interface" is false.** You instantiate an *array*, not a
   `Runnable`. `r[0] = new Thread();` is valid; `r[0] = new String("x");` is
   CE incompatible types. Since Java 8, `r[0] = () -> {};` (a lambda) is
   valid too.
6. **`Number` is abstract: `new Number()` is illegal, `new Number[10]` is
   legal, `n[0] = new Integer(10)` is legal.** `Number`'s known direct
   subclasses go beyond the six wrappers — `BigInteger`, `BigDecimal`,
   `AtomicInteger`, and `AtomicLong` are all direct children too.
7. **`x[1] = 'a'` in an `int[]` stores `97`**, the Unicode value, not the
   character `'a'` itself.
8. **`x[i] = 10L` in an `int[]` is CE possible-lossy-conversion** — the same
   underlying rule as `new int[10L]` in part 1, just triggered in a different
   place (an element assignment instead of a size expression).
9. **Element assignment (`a[i] = …`) is not variable assignment (`a = b`).**
   The second is arrays part 4 — do not conflate the two when a question asks
   which "assignment" rule applies.
10. **`new Integer(10)` and `new Double(10.5)` compile with a deprecation
    warning on Java 9+**, not an error. Autoboxing or `Integer.valueOf(...)`
    is the modern equivalent; the array-element rule they illustrate (child of
    `Number` is allowed) has not changed.

---

**Next:** Video 009 — Arrays, Part 4
