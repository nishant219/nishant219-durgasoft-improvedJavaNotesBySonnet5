# Video 028 — for, for-each

## Video info

**Title:** Core Java with OCJP/SCJP: Flow-Control Part-5  || Iterative Statements : for, for-each Loops

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 28 of 203 |
| Series | Flow-Control · Part 5 |
| Topic | Iterative statements: for, for-each (enhanced for) |
| Instructor | Durga Sir |
| Duration | 1h 33m 09s |
| Video ID | ZfpvcmdOLOA |
| Watch | https://www.youtube.com/watch?v=ZfpvcmdOLOA |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. `for` — the most commonly used loop in Java; best choice when we **know** the iteration count in advance
2. Syntax and life cycle: init once → condition → body → increment → condition → …
3. Curly braces optional (same one-statement / not-declarative rule as `while`)
4. Initialization section — executes once; any number of locals **of the same type**; any valid Java statement, including a plain `System.out.println`
5. Conditional check — any boolean expression; **optional** (the compiler places `true` if omitted)
6. Increment/decrement section — any valid Java statement
7. All three parts are **independent** and **optional** (`for (;;)` is an infinite loop)
8. Unreachability loophole — **seven** `for` cases; only two compile
9. For-each / enhanced `for` (Java 1.5) — retrieves elements of arrays and collections
10. 1-D, 2-D, 3-D array examples, traditional `for` vs for-each
11. Limitations of for-each: not a general-purpose loop; original order only, never reverse
12. The target must be an **Iterable** object (`java.lang.Iterable`); interview table: Iterator vs Iterable

---

## 00:07 — `for`: the most commonly used loop

Board heading: **for loop**.

"Our hand is always going for `for`" — it's the most commonly used loop in Java. Sir's standing rule from earlier lectures: **`for` is the best choice when you know the number of iterations in advance** (exactly 10 times, exactly 20 times).

```java
for (int i = 0; i < 10; i++) {
    System.out.println("hello");
}
```

`hello` is printed **10 times**. Four named parts:

| Part | Name |
|---|---|
| `int i = 0` | initialization section |
| `i < 10` | condition check / conditional check |
| `i++` | increment or decrement section |
| `System.out.println("hello")` | loop body / action |

### 01:52 — Life cycle: which part runs first

1. **Initialization** — first, and only **once**
2. **Conditional check**
3. If true → **loop body**
4. **Increment or decrement**
5. Conditional check again → body → increment → …

Initialization is **not** repeated. After it, the cycle is: condition → body → increment → condition → body → … Pre-increment or post-increment both work fine here.

### 04:31 — Syntax on the board

```java
for (initialization; conditional_check; increment_or_decrement) {
    // loop body
}
```

Board points: *for loop is the most commonly used loop in Java*, and *if we know the number of iterations in advance, for loop is the best choice*.

---

## 06:56 — Curly braces optional

Same rule as `while` / `do-while`. Braces are **optional**; without them, exactly **one statement** is allowed, and it must **not** be declarative.

```java
for (int i = 0; true; i++)
    System.out.println("hello"); // valid — one non-declarative statement
```

```java
for (int i = 0; i < 10; i++)
    ;   // valid — a bare semicolon is a valid Java statement
```

```java
for (int i = 0; i < 10; i++)
    int x = 10;   // CE: without curly braces we can't take a declarative statement
```

---

## 10:57 — Initialization section

Board heading: **initialization section**. It executes **only once** in the loop's life cycle. Its usual job: declare and initialize the loop's local counter.

**Multiple variables? Yes — as long as they share a type:**

```java
for (int i = 0, j = 0; i < 10; i++) {
    // valid — two ints, same type
}
```

**One `int` and one `String`?**

```java
for (int i = 0, String s = "durga"; ; ) {
} // CE: ';' expected — can't mix types in the initialization section
```

**Repeating the type keyword is also invalid** — the parser treats the second `int` as starting a new statement, and the whole thing falls apart because a `for` init clause is a single declaration, not a statement list:

```java
for (int i = 0, int j = 0; ; ) {
} // CE: <identifier> expected
```

Board points, verified against a current `javac`:

1. This part executes **only once** in the loop's life cycle.
2. Here you can declare and initialize **local variables of the for loop**.
3. You can declare **any number of variables**, but they **must share one type**. Mixed types → compile-time error.

```java
for (int i = 0, j = 0; ; ) { }              // valid
// for (int i = 0, String s = "durga"; ; ) { } // CE
// for (int i = 0, int j = 0; ; ) { }          // CE
```

### 17:31 — Init slot can hold any statement, including SOP

Counter declared **outside** the loop, so the init slot is free for something else:

```java
int i = 0;
for (System.out.println("hello boss you are sleeping"); i < 3; i++) {
    System.out.println("no boss you only sleeping");
}
```

Valid — **the initialization section can be any valid Java statement, including a `println`.** Trace:

1. Init runs once → prints `hello boss you are sleeping`; `i` is already `0`
2. `0 < 3` → prints `no boss you only sleeping` → `i++` → 1
3. `1 < 3` → prints again → `i++` → 2
4. `2 < 3` → prints again → `i++` → 3
5. `3 < 3` is false → stop

```text
hello boss you are sleeping
no boss you only sleeping
no boss you only sleeping
no boss you only sleeping
```

A student asks about `return` / `break` in that slot — `return` only belongs inside a method body and would end the method, and a statement placed after it would be unreachable, so those are ruled out by other rules, not by anything special about the init slot.

Sir also hits `cannot find symbol: i` when `i` is left as an uninitialized **local** inside the loop — the JVM supplies default values only for **instance and static** fields, never for locals. That's exactly why he moved the counter's declaration outside: to free up the init slot for the `println`.

---

## 24:41 — Conditional check

Board heading: **conditional check**.

```java
for (int i = 0; i < 3; i++) {
    // this slot: i < 3
}
```

**Point 1.** Any valid Java expression is allowed here, but the **result must be `boolean`** — `a < b && b > 30 || k < l`, anything, as long as the final type is boolean.

**Point 2.** This part is **optional**. Leave it empty and the compiler **inserts `true`**.

Dropping the condition from the sleeping example:

```java
int i = 0;
for (System.out.println("hello you are sleeping"); ; i++) {
    System.out.println("no boss you only sleeping");
    System.out.println(i);
}
```

Init prints `hello`, the empty condition becomes `true`, body runs, increment, `true` again — **infinite**. `hello` prints once, then the body runs forever.

---

## 28:58 — Increment/decrement section

Board heading: **increment or decrement section**. Writing `i++` / `i--` is not compulsory — **any valid Java statement, including SOP, is allowed.**

```java
int i = 0;
for (System.out.println("hello"); i < 3; System.out.println("hi"))
    i++;
```

Trace:

1. Init: prints `hello`; `i == 0`
2. `0 < 3` true → body `i++` → 1 → increment slot prints `hi`
3. `1 < 3` true → body `i++` → 2 → prints `hi`
4. `2 < 3` true → body `i++` → 3 → prints `hi`
5. `3 < 3` false → stop

**Output:** `hello` then `hi` `hi` `hi`.

---

## 33:40 — All three parts independent and optional

The three slots inside `for ( ; ; )` have **no dependency on each other** — init can be an SOP, the condition any boolean expression, the increment another SOP; they don't need to reference the same variable at all.

**All three are individually optional:**

```java
for (;;) {
    System.out.println("hello");
} // valid — infinite loop, hello forever
```

```java
for (;;)
    ;   // valid — infinite loop, no output at all
```

Both are infinite (empty condition becomes `true`); the second just has no visible output.

---

## 37:06 — Unreachability: seven `for` cases

Same loophole family as `while`. **Seven** shapes; only **two** compile.

**Case 1 — condition `true`**

```java
for (int i = 0; true; i++) {
    System.out.println("hello");
}
System.out.println("hi"); // CE: unreachable statement
```

**Case 2 — condition `false`**

```java
for (int i = 0; false; i++) {
    System.out.println("hello");
} // CE: unreachable statement — the loop body itself never runs
System.out.println("hi");
```

**Case 3 — empty condition (compiler inserts `true`)**

```java
for (int i = 0; ; i++) {
    System.out.println("hello");
}
System.out.println("hi"); // CE: unreachable statement
```

Same effect as Case 1 — the conditional expression is optional, and the compiler quietly places `true`.

**Case 4 — normal variables, `a < b`**

```java
int a = 10, b = 20;
for (int i = 0; a < b; i++) {
    System.out.println("hello");
}
System.out.println("hi");
```

Valid. `a` and `b` are ordinary variables; the compiler never evaluates their values, only that `a < b` is a legal boolean expression. At runtime it's `true` → **infinite `hello`**.

**Case 5 — normal variables, `a > b`**

```java
int a = 10, b = 20;
for (int i = 0; a > b; i++) {
    System.out.println("hello");
}
System.out.println("hi");
```

Valid. Runtime evaluates `10 > 20` as `false` → **output: `hi`**.

**Case 6 — `final` variables, `a < b`**

```java
final int a = 10, b = 20;
for (int i = 0; a < b; i++) {
    System.out.println("hello");
}
System.out.println("hi"); // CE: unreachable statement
```

`final` variables are compile-time constants, so the compiler substitutes their values and evaluates `10 < 20` itself — it *is* `true`, so the body never exits, and `hi` is unreachable.

**Case 7 — `final` variables, `a > b`**

```java
final int a = 10, b = 20;
for (int i = 0; a > b; i++) {
    System.out.println("hello");
} // CE: unreachable statement — the loop body is unreachable
System.out.println("hi");
```

Compiler evaluates `10 > 20` as `false` → the body itself is unreachable.

All seven verified against a current `javac` — same outcomes and same "unreachable statement" wording the lecture describes.

| Case | Compiles? | If valid |
|---|---|---|
| condition `true`, `hi` after | CE | — |
| condition `false` | CE | — |
| empty condition | CE | — |
| normal `a < b` | valid | infinite `hello` |
| normal `a > b` | valid | `hi` |
| `final` `a < b` | CE | — |
| `final` `a > b` | CE | — |

**Only the two "normal variable" cases compile.** Unreachability is the same trap in every loop construct — `while`, `do-while`, and `for` alike.

---

## 47:11 — For-each / enhanced `for`

Board heading: **for each loop**. Also called the **enhanced for loop**. Introduced in **Java 1.5**.

Purpose-built to **retrieve elements of arrays and collections** one at a time. An array is a group of elements; a collection is a group of objects — for-each is the best-suited loop for pulling them out one by one.

### 50:04 — Example 1: a 1-D array

```java
int[] x = {10, 20, 30, 40};
```

**Traditional `for`:**

```java
for (int i = 0; i < x.length; i++) {
    System.out.println(x[i]);
}
```

**Enhanced `for`:**

```java
for (int x1 : x) {
    System.out.println(x1);
}
```

Read it in English: *for each `int` value `x1` in `x`, print `x1`.* First value `10`, then `20`, `30`, `40`. Once you know for-each, going back to the index form feels unnecessary — Sir's recommendation: wherever the target is an array or collection, prefer for-each over the traditional `for`.

### 55:03 — Example 2: a 2-D array

```java
int[][] x = {{10, 20, 30}, {40, 50}};
```

Outer size **2** (two 1-D arrays): the first holds `10, 20, 30`, the second `40, 50`.

**Traditional `for`:**

```java
for (int i = 0; i < x.length; i++) {
    for (int j = 0; j < x[i].length; j++) {
        System.out.println(x[i][j]);
    }
}
```

**Enhanced `for`:**

```java
for (int[] x1 : x) {
    for (int x2 : x1) {
        System.out.println(x2);
    }
}
```

English reading: *for each 1-D array `x1` in `x`; for each `int` `x2` in `x1`; print `x2`.*

### 1:01:08 — Example 3: a 3-D array

```java
int[][][] x = {{{10, 20}, {30, 40}}, {{50, 60, 70}, {80, 90}}};
```

`x` is 3-D → contains 2-D arrays → each 2-D contains 1-D arrays → each 1-D contains `int` values.

```java
for (int[][] x1 : x) {          // each 2-D array in x
    for (int[] x2 : x1) {       // each 1-D array in that 2-D
        for (int x3 : x2) {     // each int in that 1-D
            System.out.println(x3);
        }
    }
}
```

Sir skips writing the traditional-`for` equivalent here as "unnecessary waste" — printing a 3-D array with index-based loops would be "very horrible." This is exactly the loop enhanced-`for` was built to remove.

---

## 1:05:37 — Limitation 1: not a general-purpose loop

"For-each is the best choice — don't change your answer" is the setup for a trap. Given:

```java
for (int i = 0; i < 10; i++) {
    System.out.println("hello");
}
```

**Write an equivalent for-each loop for this.** It cannot be done — there is no array or collection here, just a counter. For-each's job is narrowly **retrieving elements of arrays and collections**; with neither present, it does not apply. **It is not a general-purpose replacement for `for`.**

```java
for (int i = 0; i < 10; i++) {
    System.out.println("hello");
}
// no direct for-each equivalent exists for this — there is nothing to iterate
```

> ⚠️ **Modern Java — a stream can fake this, but it's still not for-each.**
> Since **Java 8**, `IntStream` gets you the same ten iterations without a
> classic counter:
>
> ```java
> java.util.stream.IntStream.range(0, 10)
>     .forEach(i -> System.out.println("hello"));
> ```
>
> This is a genuinely different construct (a stream pipeline calling
> `Iterable`'s cousin, `forEach`, not the `for (x : y)` syntax) — it doesn't
> overturn the lecture's point. For-each the *language keyword* still only
> ever targets an array or something `Iterable`; a bare counter is still not
> a legal for-each target.

## 1:10:04 — Limitation 2: original order only

```java
int[] x = {10, 20, 30, 40, 50};
for (int i = x.length - 1; i >= 0; i--) {
    System.out.println(x[i]);
}
```

`x.length` is 5, so `i` starts at 4. Output: **50 40 30 20 10** — reverse order, using the traditional `for`.

**There is no equivalent for-each for this.** A traditional `for` can print an array forward or backward; for-each can only ever walk it in its **original** order.

> ⚠️ **Modern Java — `List`, but not a raw array, can now hand you a reverse view.**
> **Java 21**'s `SequencedCollection` interface (JEP 431) added `reversed()` to
> every ordered collection, which *can* be driven with for-each:
>
> ```java
> import java.util.*;
>
> List<Integer> list = new ArrayList<>(List.of(10, 20, 30, 40, 50));
> for (int v : list.reversed()) {   // Java 21 — SequencedCollection::reversed
>     System.out.println(v);       // 50 40 30 20 10
> }
> ```
>
> `reversed()` returns a live reversed **view**, not a copy — mutating one
> side mutates the other. It exists on `List`, `Deque`, and `LinkedHashSet` /
> `LinkedHashMap`'s keySet/entrySet, because those already have a defined
> order. It does **not** exist on a plain array or on `int[]` — arrays never
> implemented `Iterable` in a way that gained this method, so Sir's exact
> array example is still exactly as limited as taught. The workaround only
> narrows the collections half of the gap.

---

## 1:14:33 — Iterable: the interview topic

Not something new invented "just for for-each" — a pre-existing concept the loop depends on. Syntax:

```java
for (Item x : target) {
    // for every element x in this array or collection
}
```

`target` can be **either an array or a collection**. The target of a for-each loop **must be an `Iterable` object.**

An object is Iterable **if and only if** its class implements **`java.lang.Iterable`**.

As a programmer you're **not required to do anything** about this — every array-related type and every `Collection` implementation already satisfies it. Collection framework sketch: `Collection` is the root interface → `List`, `Set`, `Queue` extend it. **Since 1.5, `Collection` itself extends `Iterable`**, so every collection implementation is automatically Iterable.

`Iterable` arrived in **1.5** — the same release as for-each and generics. Sir's board version of the method it declares:

```java
public Iterator iterator();
```

> ❗ **Correction — the real declaration is generic, not raw.**
> `Iterable` was introduced generic from day one (Java 5 shipped generics and
> `Iterable` in the same release):
>
> ```java
> public interface Iterable<T> {
>     Iterator<T> iterator();
> }
> ```
>
> Sir's `public Iterator iterator();` is the pre-generics, raw-type shorthand
> — it still compiles (raw types remain legal for backward compatibility) but
> it was never the actual signature on the board. The correct memorised
> version is `Iterator<T> iterator()`.

> ⚠️ **Modern Java — `Iterable` gained two more methods in Java 8.**
> "It contains only one method" was true in 1.5–7. Since **Java 8**, default
> methods added two more:
>
> ```java
> public interface Iterable<T> {
>     Iterator<T> iterator();                                  // abstract — unchanged
>     default void forEach(Consumer<? super T> action) { … }   // Java 8
>     default Spliterator<T> spliterator() { … }                // Java 8
> }
> ```
>
> `forEach` is why `list.forEach(System.out::println)` compiles directly on
> any `Iterable` — no loop needed. `spliterator()` backs parallel stream
> processing. Neither is *abstract*, so implementing classes still only have
> to write one method (`iterator()`) to satisfy the interface — Sir's "you
> don't have to do anything extra" survives untouched. It's specifically the
> *count* of methods *declared on the interface* that moved from one to
> three.

---

## 1:24:24 — Iterator vs Iterable

Board heading: **differences between iterator and iterable**. The similar spelling makes this a favourite interview question.

| | Iterator | Iterable |
|---|---|---|
| Related to | collections — it's the cursor | the for-each loop |
| Purpose | retrieve elements of a collection one by one (cursor family: `Enumeration`, `Iterator`, `ListIterator`) | the target type a for-each loop requires |
| Package | `java.util` | `java.lang` |
| Methods | three: `hasNext()`, `next()`, `remove()` | one: `iterator()` |

`hasNext()` — is the next element there? `next()` — hand it over. `remove()` — this current element isn't wanted, drop it. (Full collections treatment comes later; for now, remember the three names.)

Quick answer if asked: Iterator is the collection-framework cursor; Iterable is the for-each target type. `java.util` vs `java.lang`. Three methods vs one.

> ⚠️ **Modern Java — the method count on both sides moved, but the abstract core didn't.**
> Java 8 added default methods to `Iterator` too:
>
> ```java
> public interface Iterator<E> {
>     boolean hasNext();                                        // abstract — unchanged
>     E next();                                                 // abstract — unchanged
>     default void remove() { throw new UnsupportedOperationException(); } // Java 8
>     default void forEachRemaining(Consumer<? super E> action) { … }      // Java 8
> }
> ```
>
> Before Java 8, `remove()` was **abstract** — every `Iterator` implementation
> had to supply it, even a no-op that threw. Since Java 8 it's a **default**
> method that throws `UnsupportedOperationException` unless overridden, and
> `forEachRemaining` was added alongside it. So the honest current count is
> **four methods declared, two of them abstract** — the interview-table "three
> methods" is the pre-8 count. Symmetrically, `Iterable` moved from one method
> to three (see the callout above) but kept exactly one abstract method. The
> table's *shape* (Iterator has more machinery than Iterable) is still the
> right thing to remember; the raw numbers in each cell are Java 7-and-earlier
> numbers.

That's the full for-each and Iterable/Iterator picture for this lecture.

---

## Exam and interview points

1. **`for` is preferred when the iteration count is known in advance**; `while` is preferred when it isn't (JDBC `ResultSet`, `Enumeration`/`Iterator` cursors) — a distinction carried over from the previous lecture.
2. **Multiple variables in the init slot must share exactly one type** — `int i = 0, j = 0` compiles; `int i = 0, String s = "durga"` and `int i = 0, int j = 0` are both compile errors.
3. **Any slot in `for ( ; ; )` can hold an arbitrary statement**, not just a counter update — a bare `System.out.println(...)` is legal in the init slot and in the increment slot.
4. **All three slots are individually optional.** `for (;;)` is an infinite loop; the compiler inserts `true` for a missing condition.
5. **Unreachability is a compile-time check, not a runtime one** — `final` variables get folded to their compile-time-constant values and checked; ordinary variables don't, even with the exact same value, so `for (int i=0; a<b; i++)` compiles while `for (int i=0; true; i++)` followed by unreachable code does not. Only 2 of the classic 7 `for`-loop shapes compile.
6. **For-each (Java 1.5) targets arrays and `Iterable`s only** — it has no equivalent for a plain counted loop with no collection or array behind it, and it can only walk elements in their **original** order, never reverse.
7. **`Iterable` (`java.lang`, Java 1.5) declares `iterator()`**, and since **Java 8** also carries default `forEach()` and `spliterator()` — three methods on the interface, but only one (`iterator()`) is abstract, so implementing it is exactly as much work as it always was.
8. **`Iterator` (`java.util`) declares `hasNext()`/`next()`**, and since **Java 8** also carries a default `remove()` (throws `UnsupportedOperationException` unless overridden) and `forEachRemaining()` — four methods, two abstract.
9. **`Collection` has extended `Iterable` since 1.5**, which is why every `List`/`Set`/`Queue` implementation is automatically usable in a for-each loop with no extra work from the programmer.
10. **Modern interview angle on Limitation 2:** `List`/`Deque` gained a genuine reverse **view** via `SequencedCollection::reversed()` in **Java 21** — usable with for-each — but plain arrays still have no such method, so the array example from this lecture is unaffected.
11. **Modern interview angle on Limitation 1:** `IntStream.range(...).forEach(...)` (Java 8) can reproduce a counted loop's *effect*, but it is a stream pipeline, not the `for (x : y)` syntax — it does not make for-each a general-purpose loop.

**Next:** Video 029 — Transfer statements: break and continue
