# Video 018 — Concatenation, Relational, and Equality Operators

## Video info

**Title:** Core Java with OCJP/SCJP: Operators & Assignments Part-2  || Concatenation,Relational,equality

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 18 of 203 |
| Series | Operators & Assignments · Part 2 of 7 |
| Topic | String concatenation (+), relational operators, equality operators (== / !=) vs equals() |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 09m 31s (4171 seconds) |
| Video ID | D7deFmjJBfs |
| Watch | https://www.youtube.com/watch?v=D7deFmjJBfs |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Recap of last session (increment / decrement / arithmetic) and today's three operator groups
2. `+` as the **only overloaded operator** in Java: arithmetic addition vs string concatenation
3. When `+` is addition vs concatenation (at-least-one-String rule)
4. Left-to-right evaluation of a chain of `+` operators (same precedence)
5. Exam example 1: `a + b + c + d` in four orders, with `String a = "durga"` and ints
6. Exam example 2: which assignments are valid (`a = b + c + d` vs `a = a + b + c`, etc.)
7. Relational operators: `<` `<=` `>` `>=`
8. Relational operators on every primitive **except** `boolean`
9. Relational operators **cannot** be applied to object types
10. Nesting of relational operators is **not allowed** (`10 < 20 < 30`)
11. Equality operators: `==` and `!=`
12. Equality on every primitive **including** `boolean`
13. Equality on object types = **reference / address comparison**
14. Object `==` requires a type relation (child↔parent or same type); else *incomparable types*
15. Interview one-liner: `==` vs `equals()`
16. `r == null` and `null == null`

## Detailed notes

### 00:06 — Recap and agenda

Last session (video 017, Operators & Assignments Part-1) covered **increment / decrement** and **arithmetic** operators. Today's three topics, in board order: the string concatenation operator (`+`), relational operators, and equality operators.

---

## 00:17 — String concatenation operator (`+`) — the only overloaded operator in Java

Warm-up the class already knows:

| Expression | Result | Why |
|---|---|---|
| 10 + 20 | 30 | both operands are numbers → arithmetic addition |
| "ab" + "cd" | "abcd" | at least one operand is a String → string concatenation |

Sometimes `+` is addition. Sometimes `+` is concatenation. That is **operator overloading**.

Durga's exam-level wording (he dictates this several times — memorize it):

> **The only overloaded operator in Java is the plus operator.**
>
> *Sometimes it acts as arithmetic addition operator. Sometimes it acts as string concatenation operator.*

**Operator overloading at language level:** Java does **not** let you overload operators in general (you cannot define `+` for your own class the way C++ does). Method overloading you can apply everywhere; operator overloading you cannot. **One exceptional case** is `+` on `String`.

Exam trap: do **not** answer "Java supports operator overloading" as a blanket yes. The safe answer is: **at language level Java does not provide operator overloading, except `+` for String concatenation.**

The exam will not stop at "plus is overloaded." The hard part is **deciding, in a mixed expression, which `+` is addition and which is concatenation.**

> ⚠️ **Modern Java — how `+` concatenation is compiled changed in Java 9.**
> Through Java 8, `javac` compiled a chain of String `+` into explicit
> `StringBuilder` calls: `new StringBuilder().append(a).append(b)....toString()`.
> Since **Java 9** (JEP 280), `javac` instead emits a single `invokedynamic`
> call to `java.lang.invoke.StringConcatFactory`, and the JVM picks the actual
> concatenation strategy at link time (it can change strategy in a later JVM
> release without anyone recompiling application code). The result and the
> rules Sir teaches here — at-least-one-String, left-to-right, every `+` after
> the first String concatenates — are completely unchanged. Only the bytecode
> under the hood is different, which is why this is a fair "how does the JVM
> actually do this" follow-up question in a modern interview.

### 04:40 — Example 1: four `println`s, left-to-right evaluation

Board declarations (ASR says "DGA" / "dura"; the string is **`"durga"`**):

```java
String a = "durga";
int b = 10;
int c = 20;
int d = 30;
```

Four statements:

```java
System.out.println(a + b + c + d);
System.out.println(b + c + d + a);
System.out.println(b + c + a + d);
System.out.println(b + a + c + d);
```

Class guesses that collide:

| Line | Wrong guess A | Wrong guess B | Actual |
|---|---|---|---|
| a + b + c + d | "durga60" | "durga102030" | "durga102030" |
| b + c + d + a | "102030durga" | "60durga" | "60durga" |
| b + c + a + d | "30durga30" or "1020durga30" |  | "30durga30" |
| b + a + c + d | "10durga2030" |  | "10durga2030" |

**Why left-to-right (not "add the numbers then glue the string")**

`a + b + c + d` contains **three** `+` operators. When more than one operator is present, evaluation uses **precedence**. Here **all three have the same precedence**, so the order of evaluation is **always left to right**.

So the compiler does **not** treat it as `a + (b + c + d)`. It treats it as `((a + b) + c) + d`.

**Rule that decides each `+`**

For **one** `+` with two operands:

1. If **at least one argument is String type**, `+` acts as **concatenation**.
2. If **both arguments are number type**, `+` acts as **arithmetic addition**.

After concatenation, the result is a `String`. That `String` then infects every `+` to its right.

**Walkthrough of all four**

**1. `a + b + c + d` → `"durga102030"`**

```java
a + b     →  "durga" + 10     → at least one String → "durga10"
"durga10" + c → "durga10" + 20 → concatenation      → "durga1020"
"durga1020" + d → concatenation                     → "durga102030"
```

People who print `"durga60"` added `10+20+30` first. That is **wrong evaluation order**.

**2. `b + c + d + a` → `"60durga"`**

```java
b + c     →  10 + 20          → both numbers → 30
30 + d    →  30 + 30          → both numbers → 60
60 + a    →  60 + "durga"     → concatenation → "60durga"
```

**3. `b + c + a + d` → `"30durga30"`**

```java
b + c     →  10 + 20          → 30
30 + a    →  30 + "durga"     → "30durga"
"30durga" + d → concatenation → "30durga30"
```

**4. `b + a + c + d` → `"10durga2030"`**

```java
b + a     →  10 + "durga"     → "10durga"
"10durga" + c → concatenation → "10durga20"
"10durga20" + d → concatenation → "10durga2030"
```

Once a `String` appears, **every later `+` in that left-to-right chain is concatenation**. Numbers after the first String are **not** added together.

Durga flags this as **maximum chance for SCJP/OCJP**. Write the four outputs until they are automatic.

### 14:42 — Example 2: which assignments are valid

Same variables: `String a = "durga"`, `int b = 10`, `int c = 20`, `int d = 30`.

Consider these **four assignments**. Which compile?

```java
a = b + c + d;   // (1)
a = a + b + c;   // (2)
b = a + c + d;   // (3)
b = b + c + d;   // (4)
```

Board answers (he asks the class before explaining):

| # | Expression | Valid? | Type of RHS | Assigned to | Result |
|---|---|---|---|---|---|
| 1 | a = b + c + d | invalid | int (10+20+30 → 60) | String a | compile-time error |
| 2 | a = a + b + c | valid | String (concatenation) | String a | OK |
| 3 | b = a + c + d | invalid | String | int b | compile-time error |
| 4 | b = b + c + d | valid | int | int b | OK |

If (1) is invalid, (2) is the "string version" and is valid. If (3) is invalid, (4) is the "int version" and is valid. That pairing is how he wants you to check quickly, then prove with types.

**Compiler messages (write these; exam options quote them)**

**(1)** `b + c + d` is `int`. You cannot assign `int` to `String`:

```text
incompatible types
found   : int
required: java.lang.String
```

**(2)** `a + b + c`: `a` is `String`, so the whole RHS is `String`. `String` into `String` — fine.

**(3)** `a + c + d` is `String`. You cannot assign `String` to `int`:

```text
incompatible types
found   : java.lang.String
required: int
```

**(4)** `b + c + d` is `int`. `int` into `int` — fine.

> ⚠️ **Modern Java — this exact wording is from the Java 6/7-era `javac`.**
> Verified on a current JDK (26): `javac` no longer prints the two-line
> `found:` / `required:` block, and it drops the `java.lang.` package prefix.
> Compiling statement (1) today gives one line instead:
>
> ```text
> incompatible types: int cannot be converted to String
> ```
>
> and statement (3) gives:
>
> ```text
> incompatible types: String cannot be converted to int
> ```
>
> `javac`'s diagnostic formatter was rewritten around the JDK 8/9 era; the
> *rule* — you cannot assign an `int`-typed expression to a `String` variable
> or vice versa — has never changed, only the sentence the compiler prints.
> OCJP-era exam options still quote the old two-line form; a modern terminal
> will show the new one-liner. The same swap applies to every other compiler
> message quoted later in this lecture (`operator > cannot be applied to …`
> becomes `bad operand types for binary operator '>'` with separate
> `first type:` / `second type:` lines, and `incomparable types: java.lang.X
> and java.lang.Y` drops its `java.lang.` prefix too).

Two exam *styles* for concatenation, same concept:

1. **What is printed?** (evaluation order, example 1)
2. **Which lines compile?** (assignment compatibility, example 2)

That closes concatenation.

---

## 21:26 — Relational operators

Operators on the board:

| Operator | Meaning |
|---|---|
| < | less than |
| <= | less than or equal to |
| > | greater than |
| >= | greater than or equal to |

Result of a relational operator is always `boolean` (`true` or `false`).

### Example set — primitives (including `char` promotion)

```java
System.out.println(10 < 20);        // true
System.out.println('a' < 10);       // false
System.out.println('a' < 97.6);     // true
System.out.println('a' > 'A');      // true
System.out.println(true > false);   // compile-time error
```

Walkthrough:

| Expression | What happens | Result |
|---|---|---|
| 10 < 20 | obvious | true |
| 'a' < 10 | char promoted to number. 'a' is Unicode/ASCII 97. 97 < 10 | false |
| 'a' < 97.6 | 'a' → 97 → 97.0 (int promoted to double). 97.0 < 97.6 | true |
| 'a' > 'A' | 97 > 65 ('A' is 65) | true |
| true > false | two booleans, no "bigger / smaller" | CE |

Compiler message for the boolean case (Java 6/7 wording; today's `javac` says
`bad operand types for binary operator '>'` with `first type: boolean` /
`second type: boolean` — see the callout above):

```text
operator > cannot be applied to boolean,boolean
```

(`true` and `false` are at the same "level"; there is no ordering.)

**Conclusion 1 — every primitive except `boolean`**

> *We can apply relational operators for **every primitive type except boolean**.*

Allowed: `byte`, `short`, `int`, `long`, `float`, `double`, `char` (char is compared via its numeric value).

Not allowed: `boolean`.

### 27:29 — Conclusion 2: relational operators cannot apply to object types

```java
System.out.println("durga123" > "durga");
```

**Invalid.** Compile-time error.

Why, even in English: "first student greater than second student" is meaningless. "First student's **marks** greater than second student's **marks**" is meaningful. Relational `<` `>` talk about **numeric order**, not objects.

Compiler message (Java 6/7 wording — today drops `java.lang.` and uses the
`bad operand types` form):

```text
operator > cannot be applied to java.lang.String,java.lang.String
```

Same idea for any two objects (`Student`, `Thread`, …). Relational operators are **not** for object types.

> *We **cannot** apply relational operators for object types. If we try, compile-time error.*

### 31:15 — Conclusion 3: nesting of relational operators is not allowed

```java
System.out.println(10 < 20);         // true — answer immediately
System.out.println(10 < 20 < 30);    // compile-time error
```

Looks like "10 is less than 20 and 20 is less than 30." That is **not** how Java parses it.

There are **two** `<` operators, same precedence → **left to right**:

```java
10 < 20     →  true
true < 30   →  operator < cannot be applied to boolean, int
```

Compiler message:

```text
operator < cannot be applied to boolean,int
```

Durga's wording (ASR says "nising / nting"; he means **nesting**):

> **Nesting of relational operators is not allowed.**
>
> *After applying a relational operator, you cannot apply another relational operator to that result. Otherwise compile-time error.*

Chaining like Python (`10 < 20 < 30`) does **not** exist in Java.

**Relational operators — three conclusions to recite**

1. Every primitive **except** `boolean`.
2. **Not** for object types.
3. **Nesting** not allowed.

Small topic; those three loopholes are the exam.

---

## 35:09 — Equality operators (`==` and `!=`)

Equality operators on the board: **`==`** (double equal) and **`!=`** (not equal).

**Example set — primitives including `boolean`**

```java
System.out.println(10 == 20);         // false
System.out.println('a' == 'b');       // false
System.out.println('a' == 97.0);      // true
System.out.println(false == false);   // true
```

Walkthrough:

| Expression | What happens | Result |
|---|---|---|
| 10 == 20 | 10 is not 20 | false |
| 'a' == 'b' | 97 vs 98 | false |
| 'a' == 97.0 | smaller type promoted to bigger: 'a' → 97 → 97.0. 97.0 == 97.0 | true |
| false == false | both false | true |

Class joke: some people say `false == false` is "a false statement." It is **true**. Two `false` values **are** equal.

**Promotion reminder:** whenever you compare a smaller numeric type with a bigger one, the smaller is promoted (same idea as arithmetic).

Difference vs relational: `<` `>` are **illegal** on `boolean`. `==` `!=` are **legal** on `boolean`.

**Conclusion 1 — every primitive including `boolean`**

> *We can apply equality operators for **every primitive type including boolean**.*

Durga calls equality operators **universal** at the primitive level: numbers, chars, booleans — all fine.

### 39:40 — Equality operators on object types — reference / address comparison

Yes, you **can** apply `==` / `!=` to object types. That is a major difference from relational operators.

If you apply equality operators to object references `r1` and `r2`:

> `r1 == r2` returns *true if and only if both references point to the same object*.

That is **reference comparison** (also called **address comparison**). Not content comparison.

Diagram he draws: two arrows into **one** heap object → `==` is `true`. Two arrows into **two** objects → `==` is `false`, even if the objects "look" the same.

### 43:47 — Example 1: Thread references (not a multithreading lecture)

```java
Thread t1 = new Thread();
Thread t2 = new Thread();
Thread t3 = t1;

System.out.println(t1 == t2);
System.out.println(t1 == t3);
```

How many objects? **Two** (`new Thread()` twice).

How many reference variables? **Three** (`t1`, `t2`, `t3`).

```text
t1 ──► [ Thread object A ]
t3 ──┘
t2 ──► [ Thread object B ]
```

| Expression | Same object? | Result |
|---|---|---|
| t1 == t2 | no | false |
| t1 == t3 | yes (t3 = t1) | true |

He stresses: this is **not** a threads chapter. `Thread` is just a convenient class. The same picture works with any class.

### 46:37 — Example 2: there must be a relation between argument types

```java
Thread t = new Thread();
Object o = new Object();
String s = new String("durga");

System.out.println(t == o);
System.out.println(o == s);
System.out.println(s == t);
```

Three objects, three types.

| Expression | Compiles? | Runtime if it compiles |
|---|---|---|
| t == o | yes (Thread is a child of Object) | false (different objects) |
| o == s | yes (String is a child of Object) | false |
| s == t | no | compile-time error |

The first two are `false` because the references do **not** point to the same object. That is the same rule as example 1.

The **loophole** is the third line. If it were simply `false`, there would be no reason for a new example. Instead:

```text
incomparable types: java.lang.String and java.lang.Thread
```

(ASR: "in comparable types." Compiler wording is **incomparable types**.)

He compiles `Test.java` with the third line commented: `t == o` and `o == s` print `false` `false`. Uncomment `s == t` → compile error.

**Analogy he uses**

- Two software engineers — comparable (skill, etc.)
- Two auto drivers — comparable (speed, experience)
- One software engineer and one auto driver — **not** comparable
- One animal and one human — **not** comparable

To use `==` between object types, the types must be in the **same inheritance line**.

**Rule (dictate this)**

> *If we apply equality operators for object types, **compulsory there should be some relation between argument types**
> (either **child to parent**, or **parent to child**, or **same type**).*
>
> *Otherwise compile-time error: **incomparable types**.*

`Thread` and `Object`: parent–child → OK.

`String` and `Object`: parent–child → OK.

`String` and `Thread`: siblings under `Object`, **no** direct relation for `==` → CE.

Same-type (`Thread` vs `Thread`) is obviously allowed (example 1).

> ❗ **Correction — "child-to-parent, parent-to-child, or same type" is not quite the complete rule.**
> The actual JLS rule (§15.21) for reference `==`/`!=` is **castability**, not
> strictly inheritance: one operand's compile-time type must be convertible to
> the other's by a cast. Sir's three cases are exactly right for two **classes**.
> But if either side's compile-time type is an **interface**, the comparison
> compiles even with no class relationship at all — *unless* the other side is
> a `final` class that provably does not implement it:
>
> ```java
> interface Foo {}
> class B {}                    // does NOT implement Foo, and is not final
>
> Foo f = null;
> B b = new B();
> System.out.println(f == b);   // compiles (verified on JDK 26) — some future
>                                // subclass of B could implement Foo, so the
>                                // compiler can't rule it out
>
> final class C {}              // final AND does not implement Foo
> // System.out.println(f == (C) null == ...); // f == c would be a CE:
> // incomparable types: Foo and C — now provably impossible, since C can
> // never be subclassed to add Foo
> ```
>
> `String` vs `Thread` fails because **neither is an interface** and neither
> extends the other — Sir's rule gives the right answer for every OCJP
> question on this topic. The interface exception above is the natural
> interviewer follow-up once you've given the thumb-rule answer.

### 57:24 — Interview FAQ: difference between `==` and `equals()`

**Maximum chance in the interview room** because the words look similar: double-equal **operator** vs `equals` **method**.

**One-line answer the interviewer wants:**

|  | Meant for |
|---|---|
| == operator | reference comparison (address comparison). true only if both references point to the same object. |
| equals() method | content comparison. Objects may be different objects; we care whether content is the same. |

Internal loopholes exist (he flags them: in one particular case `equals()` is also reference comparison — `Object`'s default `equals` — **later advanced topic**). At thumb-rule / top level, say: `==` → reference, `equals()` → content.

**Example to explain in the interview (recommended)**

```java
String s1 = new String("durga");
String s2 = new String("durga");

System.out.println(s1 == s2);        // false
System.out.println(s1.equals(s2));   // true
```

Heap picture:

```text
s1 ──► [ "durga" ]     // object 1
s2 ──► [ "durga" ]     // object 2, same content
```

Two objects, same content.

- `s1 == s2` → reference comparison → different objects → **`false`**
- `s1.equals(s2)` → content comparison → both `"durga"` → **`true`**

He tells you to **draw the diagram** in the interview.

Note he will return to: `equals()` is **not** always content comparison for every class (depends on override). Top-level answer still stands for `String`.

> ⚠️ **Modern Java — records (Java 16) give you content-comparing `equals()` for free.**
> Sir's `Object`'s-default-is-reference-comparison point is unchanged for
> ordinary classes. But a `record` auto-generates `equals()`, `hashCode()`,
> and `toString()` from its fields, so the "compare content, not address"
> behavior he's teaching happens automatically for a plain data carrier:
>
> ```java
> record Point(int x, int y) {}
>
> Point p1 = new Point(1, 2);
> Point p2 = new Point(1, 2);
> System.out.println(p1 == p2);        // false — different objects (verified)
> System.out.println(p1.equals(p2));   // true  — auto-generated, compares x and y
> ```
>
> Nothing here contradicts the lecture — it's the same `==`-vs-`equals()`
> split, just with the content-comparison method written for you instead of
> overridden by hand.

### 1:04:07 — Last point: comparing references with `null`

First dictation (then he immediately qualifies it):

> *For any object reference `r`, `r == null` is always `false`.*

Then the full picture:

| Expression | Result | Why |
|---|---|---|
| living reference == null | false | r points at an object, not null |
| null == null | `true` | both are null |

```java
String s = new String("durga");
System.out.println(s == null);     // false  — s points to an object

String s2 = null;
System.out.println(s2 == null);    // true   — s2 holds null

System.out.println(null == null);  // true
```

Do **not** blindly recite "any reference `== null` is false." If the reference **itself** is `null`, then `s == null` is **`true`**. `s` is still a reference variable; its **value** is `null` (not pointing to any object).

**Local vs "global" (instance / static)**

If `s` is a **local** variable and you never assign it, `s == null` is a compile-time error (local not initialized).

If `s` is an **instance or static** `String` (he says "global"), the default value is `null`, so `s == null` is **`true`** without an explicit assignment.

**Equality operators — closing recap from the lecture**

- You can apply equality operators **everywhere**: primitives, `boolean`, object types.
- On object types there is a **restriction**: relation between argument types, or CE *incomparable types* (with the interface nuance from the ❗ correction above).
- For a non-null object reference `r`, `r == null` is `false`. `null == null` is `true`.
- Interview: `==` vs `equals()` — reference vs content.

---

## Code from the lecture

### Concatenation — evaluation order

```java
class ConcatDemo {
    public static void main(String[] args) {
        String a = "durga";
        int b = 10, c = 20, d = 30;

        System.out.println(a + b + c + d); // durga102030
        System.out.println(b + c + d + a); // 60durga
        System.out.println(b + c + a + d); // 30durga30
        System.out.println(b + a + c + d); // 10durga2030
    }
}
```

### Concatenation — which assignments compile

```java
class ConcatAssign {
    public static void main(String[] args) {
        String a = "durga";
        int b = 10, c = 20, d = 30;

        // a = b + c + d; // CE: incompatible types: int cannot be converted to String
        a = a + b + c;      // OK  (String)
        // b = a + c + d;  // CE: incompatible types: String cannot be converted to int
        b = b + c + d;      // OK  (int)
    }
}
```

### Relational operators

```java
class RelationalDemo {
    public static void main(String[] args) {
        System.out.println(10 < 20);      // true
        System.out.println('a' < 10);     // false  (97 < 10)
        System.out.println('a' < 97.6);   // true   (97.0 < 97.6)
        System.out.println('a' > 'A');    // true   (97 > 65)
        // System.out.println(true > false);
        // CE: bad operand types for binary operator '>' (boolean, boolean)

        // System.out.println("durga123" > "durga");
        // CE: bad operand types for binary operator '>' (String, String)

        System.out.println(10 < 20);      // true
        // System.out.println(10 < 20 < 30);
        // CE: bad operand types for binary operator '<' (boolean, int)
    }
}
```

### Equality — primitives and Thread references

```java
class EqualityDemo {
    public static void main(String[] args) {
        System.out.println(10 == 20);       // false
        System.out.println('a' == 'b');     // false
        System.out.println('a' == 97.0);    // true
        System.out.println(false == false); // true

        Thread t1 = new Thread();
        Thread t2 = new Thread();
        Thread t3 = t1;
        System.out.println(t1 == t2); // false
        System.out.println(t1 == t3); // true
    }
}
```

### Equality — incomparable types, equals(), null

```java
class EqualityObjects {
    public static void main(String[] args) {
        Thread t = new Thread();
        Object o = new Object();
        String s = new String("durga");
        System.out.println(t == o); // false (compiles)
        System.out.println(o == s); // false (compiles)
        // System.out.println(s == t);
        // CE: incomparable types: String and Thread

        String s1 = new String("durga");
        String s2 = new String("durga");
        System.out.println(s1 == s2);        // false
        System.out.println(s1.equals(s2));   // true

        String live = new String("durga");
        System.out.println(live == null);    // false

        String n = null;
        System.out.println(n == null);       // true
        System.out.println(null == null);    // true
    }
}
```

All four classes above compile clean (verified with `javac` on JDK 26) once the commented compile-error lines stay commented.

---

## Exam and interview points

1. `+` is the **only** overloaded operator in Java; the language does **not** generally support operator overloading. Since Java 9, `+`-chains compile to an `invokedynamic` call into `StringConcatFactory` rather than explicit `StringBuilder` calls, but the concatenation rules themselves are untouched.
2. `a + b + c + d` with `a` a String is **`"durga102030"`**, not `"durga60"`. Left to right, same precedence. The first String in the chain "poisons" every `+` to its right.
3. `b + c + d + a` **is** `"60durga"` because the numbers are added **before** the String appears.
4. `a = b + c + d` does not concatenate; RHS is `int` → compile-time error (`incompatible types: int cannot be converted to String` on modern `javac`; the older `found:`/`required:` two-line form is what the exam quotes).
5. Relational operators: every primitive **except boolean**; **never** objects; **no nesting**. `'a' < 10` is `false` (97), not a CE. `true > false` is a CE; `10 < 20 < 30` is a CE (`true < 30`), not `true`.
6. `false == false` is `true` — two `false` values are equal; do not be talked into "false statement."
7. Object `==` is **reference** comparison, never content. `new String("durga") == new String("durga")` is `false` even though the content matches.
8. `String` `==` `Thread` is a compile-time error, **`incomparable types`**, not `false` — because neither type is an interface and neither extends the other. If either side's type *is* an interface, `==` against an unrelated non-final class still compiles (JLS §15.21 castability, not strict inheritance).
9. Interview one-liner: `==` is reference comparison; `equals()` is content comparison — demonstrate with the `new String("durga")` pair. `record` classes (Java 16+) generate a content-comparing `equals()` automatically, which is a clean modern illustration of the same split.
10. `null == null` is **`true`**. A reference that actually points to an object compared with `null` is `false`. An uninitialized **local** reference cannot be compared at all (definite-assignment CE); an uninitialized instance/static reference defaults to `null`.

---

**Next:** Video 019 — `instanceof` and Bitwise Operators
