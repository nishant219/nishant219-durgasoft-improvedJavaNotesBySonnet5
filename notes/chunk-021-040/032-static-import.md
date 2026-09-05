# Video 032 — static import

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-3 || static import

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 32 of 203 |
| Series | Declarations and Access Modifiers · Part 3 |
| Topic | static import |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 13m 21s |
| Video ID | oYLGLVjckj8 |
| Watch | https://www.youtube.com/watch?v=oYLGLVjckj8 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Captions | None on YouTube. Notes reconstructed from this lecture topic as Durga Sir teaches it, with full Java board examples. |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Last video (031) finished the nine import cases, C `#include` vs Java `import`, the 1.5 feature list, Sun vs worldwide experts on static import, and the first Math demo (`sqrt` / `max` / `random`). This part is the **rest of static import** — the loopholes, the live compiles, and the exam bits.

1. Recap: we normally access static members by **class name**; static import lets us skip the class name.
2. Two types: **explicit static import** vs **implicit static import** (`import static java.lang.Math.sqrt;` vs `import static java.lang.Math.*;`).
3. `java.lang` already gives us the **Math class**, not unqualified `sqrt()`. That is the whole point of static import.
4. Full anatomy of `System.out.println` — System is a class, `out` is a static `PrintStream`, `println` is an instance method.
5. `System.out.println` via **static import of `out`**: `out.println("hello");`
6. You cannot static-import `println`. You cannot normal-import `out`.
7. Ambiguity: two static imports of the **same name** (`Integer.MAX_VALUE` and `Byte.MAX_VALUE`).
8. Precedence while resolving static members: **current class → explicit static import → implicit static import**.
9. Exam list: which import statements are valid.
10. **Normal import vs static import** (what each one brings into scope).
11. Sun's line vs experts' line: if there is no specific requirement, **never recommended**.

One spelling note: while **writing** code we write `import static`; while **pronouncing** it we say "static import." Don't let the word order confuse you.

---

## 00:04 — Last class recap — why static import exists

Board heading: static import (continued).

Usually we access static members (method or variable) by using the class name. Last session he already compiled this:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(4));
        System.out.println(Math.max(10, 20));
        System.out.println(Math.random());
    }
}
// prints 2.0
// prints 20
// prints a double in [0.0, 1.0)  (changes every run)
```

`sqrt`, `max`, `random` are static methods of `java.lang.Math`. If you want square root 20 times, you type `Math` 20 times — length of the code goes up. Sun's thought: remove the class name, length down, readability up. That thought introduced static import in **1.5**.

According to Sun: using static import reduces code length and improves readability. According to worldwide programming experts (like us): using static import creates confusion and reduces readability — hence if there is no specific requirement, it is **not recommended**. While releasing 1.6 they repeated the same line. For SCJP, know the advantage, disadvantage, syntax, ambiguity, and why it is considered a flop.

## 04:30 — Need of static import — the class name every time

Without static import, even a small Math program repeats the class name:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(4));
        System.out.println(Math.sqrt(9));
        System.out.println(Math.sqrt(16));
        System.out.println(Math.sqrt(25));
    }
}
// prints 2.0
// prints 3.0
// prints 4.0
// prints 5.0
```

Need of static import: *usually we access static members by class name; if we want to access them directly without the class name, static import is required.*

## 08:10 — Two types of static import

Board heading: types of static import. Exactly parallel to last video's two types of **class** import:

1. Explicit static import — import **one particular** static member.
2. Implicit static import — import **all** static members of that class.

```java
import static java.lang.Math.sqrt; // explicit static import — only sqrt

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
    }
}
// prints 2.0
```

```java
import static java.lang.Math.*; // implicit static import — all static members of Math

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
        System.out.println(max(10, 20));
        System.out.println(random());
    }
}
// prints 2.0
// prints 20
// prints a double in [0.0, 1.0)  (changes every run)
```

Syntax on the board — take special care of the word order:

```java
import static java.lang.Math.sqrt; // import static  <fully-qualified-class>  .  <member>
import static java.lang.Math.*;    // import static  <fully-qualified-class>  .  *
```

Wrong order is a favourite exam trap:

```java
static import java.lang.Math.sqrt; // CE: class, interface, or enum expected

class Test {
    public static void main(String[] args) {
        System.out.println("this line is never reached");
    }
}
```

Parentheses are not allowed in the import line — we are importing the **method name**, not calling it:

```java
import static java.lang.Math.sqrt(); // CE: ';' expected — parentheses are illegal here

class Test {
    public static void main(String[] args) {
        System.out.println("this line is never reached");
    }
}
```

Which type is recommended? Same story as last class: **explicit** is more readable. `Math.*` dumps every static name into your file — `sin`, `cos`, `tan`, `abs`, `floor`, `ceil`, `pow`, `PI`, `E`, … — and the reader cannot see *which* members you actually use.

## 12:45 — Live compile — explicit `sqrt` is not enough for `max` and `random`

He types the program **without** any static import first, using short names — three cannot-find-symbol errors. Then he adds only `sqrt`. Then he switches to `Math.*`.

```java
class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
        System.out.println(max(10, 20));
        System.out.println(random());
    }
}
// CE: cannot find symbol method sqrt(int)
// CE: cannot find symbol method max(int,int)
// CE: cannot find symbol method random()
```

```java
import static java.lang.Math.sqrt;

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
        System.out.println(max(10, 20));
        System.out.println(random());
    }
}
// sqrt is OK
// CE: cannot find symbol method max(int,int)
// CE: cannot find symbol method random()
```

If you already have `import static java.lang.Math.*;`, the extra line `import static java.lang.Math.sqrt;` is redundant — `sqrt` is already included. He deletes the explicit line and keeps only the star.

`sqrt` returns **double**, so `sqrt(4)` prints `2.0`, not `2`. Students who expect `2` lose an exam mark. `max(10, 20)` is overloaded; the `int` version returns `20` with no decimal.

## 20:00 — More static members of Math — `abs`, `min`, `pow`, `PI`, `E`

Once `Math.*` is there, any public static member of Math can be used as a short name:

```java
import static java.lang.Math.*;

class Test {
    public static void main(String[] args) {
        System.out.println(abs(-10));
        System.out.println(min(10, 20));
        System.out.println(pow(2, 3));
        System.out.println(PI);
        System.out.println(E);
    }
}
// prints 10
// prints 10
// prints 8.0
// prints 3.141592653589793
// prints 2.718281828459045
```

Explicit form for a **variable** (constant) is the same syntax as for a method — no parentheses:

```java
import static java.lang.Math.PI;

class Test {
    public static void main(String[] args) {
        System.out.println(PI);
        System.out.println(Math.E);
    }
}
// prints 3.141592653589793
// prints 2.718281828459045
```

`PI` came through static import. `E` still needs `Math.` because we did not import `E`.

## 24:30 — `java.lang` is already imported — then why static import Math?

Biggest student confusion of this video. Last class: two packages are default-available — `java.lang` and the default package. So `Math` is already there:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(4));
    }
}
// prints 2.0 — no import statement needed, Math is a class in java.lang
```

Now remove the class name:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
    }
}
// CE: cannot find symbol method sqrt(int)
```

**Default import of `java.lang` makes the class available. It does not make the static members available as unqualified names.** For the short name `sqrt` you still need static import.

Normal import of Math is legal but useless for this problem — Math is already in `java.lang`:

```java
import java.lang.Math; // valid normal import, but redundant (java.lang is default)

class Test {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(4));
        // System.out.println(sqrt(4));
        // CE if uncommented: cannot find symbol method sqrt(int)
    }
}
// prints 2.0
```

Board: *importing a class and importing static members of a class are two different things.*

## 28:40 — Anatomy of `System.out.println`

Board heading: explain about `System.out.println` statement. Until today we typed it like a slogan; today we break it into three pieces:

| Piece | What it is |
|---|---|
| System | a class in java.lang |
| out | a static variable in class System |
| println | an instance method in class PrintStream (java.io) |

Type of `out` is `PrintStream`. So `System.out` is a `PrintStream` object (already created for us, pointing at the console). On that object we call `println`. He proves the type live:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(System.out.getClass().getName());
    }
}
// prints java.io.PrintStream
```

`err` and `in` are the siblings, same idea:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(System.err.getClass().getName());
        System.out.println(System.in.getClass().getName());
    }
}
// prints java.io.PrintStream
// prints java.io.BufferedInputStream
```

So the one-liner we always write is just: take the static field `out`, call instance method `println` on it.

```java
class Test {
    public static void main(String[] args) {
        java.io.PrintStream out = System.out;
        out.println("hello");
        out.println("hi");
    }
}
// prints hello
// prints hi
```

To show the *shape* of System (not the real JDK source — a teaching model), he draws:

```java
class PrintStreamDemo {
    public void println(String s) {
        System.out.println(s);
    }
}

class SystemDemo {
    static PrintStreamDemo out = new PrintStreamDemo();

    public static void main(String[] args) {
        SystemDemo.out.println("hello");
    }
}
// prints hello
```

`SystemDemo.out.println("hello")` is the same shape as `System.out.println("hello")`: class → static field → instance method.

## 43:50 — `System.out.println` via static import of `out`

If `out` is a static member of `System`, we can static-import **that member** and drop the `System.`:

```java
import static java.lang.System.out;

class Test {
    public static void main(String[] args) {
        out.println("hello");
        out.println("hi");
    }
}
// prints hello
// prints hi
```

Implicit form also works — all static members of `System` (`out`, `err`, `in`, `gc`, `exit`, …):

```java
import static java.lang.System.*;

class Test {
    public static void main(String[] args) {
        out.println("hello");
        err.println("this goes to error stream");
    }
}
// prints hello
// prints this goes to error stream  (on stderr)
```

You can still write the long form even after static import. Static import is only a **compile-time shortcut**, same philosophy as last video's import:

```java
import static java.lang.System.out;

class Test {
    public static void main(String[] args) {
        out.println("short");
        System.out.println("long form still valid");
    }
}
// prints short
// prints long form still valid
```

## 48:20 — What we cannot import — `println` is not a static member of System

Favourite wrong attempt: "sir, I want only `println();` on its own."

```java
import static java.lang.System.out.println; // CE: cannot find symbol (out is not a class of System)

class Test {
    public static void main(String[] args) {
        println("hello");
    }
}
```

`println` lives in `PrintStream`. It is an **instance** method. Static import can import only **static** members of a type, and there is no `System.println`. Same failure if you star-import everything from System and then call `println()` as if it were a static method of System:

```java
import static java.lang.System.*;

class Test {
    public static void main(String[] args) {
        println("hello"); // CE: cannot find symbol method println(String)
        out.println("hello");
    }
}
```

If the second line is kept and the first is commented, it compiles and prints `hello` — the star imported `out`, not `println`.

Normal import cannot import a field or a method either:

```java
import java.lang.System.out; // CE: cannot find symbol class out (normal import is only for types)

class Test {
    public static void main(String[] args) {
        System.out.println("never reached");
    }
}
```

```java
import java.lang.Math.sqrt; // CE: cannot find symbol class sqrt (sqrt is a method, not a type)

class Test {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(4));
    }
}
```

```java
import static java.lang.Math; // CE: static import only from classes and interfaces (must be Math.member or Math.*)

class Test {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(4));
    }
}
```

And you cannot static-import a **class** as if it were a static member:

```java
import static java.util.ArrayList; // CE: static import only from classes and interfaces (ArrayList is a type, not a static member)

class Test {
    public static void main(String[] args) {
        System.out.println("never reached");
    }
}
```

Normal import is the tool for classes:

```java
import java.util.ArrayList;

class Test {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        System.out.println(l.size());
    }
}
// prints 0
```

## 52:40 — Combining `Math.*` and `System.out`

Now the "short program" Sun advertised: no `Math.`, no `System.`.

```java
import static java.lang.Math.*;
import static java.lang.System.out;

class Test {
    public static void main(String[] args) {
        out.println(sqrt(4));
        out.println(max(10, 20));
        out.println(PI);
    }
}
// prints 2.0
// prints 20
// prints 3.141592653589793
```

Looks cute. Next topic is why worldwide experts still say *don't*.

## 56:10 — Ambiguity — two static imports of the same name

Board heading: ambiguity problem in static import.

`MAX_VALUE` is a public static final variable in **Integer** and also in **Byte** (and Short, Long, …) — two classes, same member name, very common. Without static import there is no fight, because the class name is the identity:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(Integer.MAX_VALUE);
        System.out.println(Byte.MAX_VALUE);
        System.out.println(Integer.MIN_VALUE);
        System.out.println(Byte.MIN_VALUE);
    }
}
// prints 2147483647
// prints 127
// prints -2147483648
// prints -128
```

Now hide the class names with two implicit static imports:

```java
import static java.lang.Integer.*;
import static java.lang.Byte.*;

class Test {
    public static void main(String[] args) {
        System.out.println(MAX_VALUE);
    }
}
// CE: reference to MAX_VALUE is ambiguous
//     both variable MAX_VALUE in Byte and variable MAX_VALUE in Integer match
```

Same story with two **explicit** static imports of the same name — explicit vs explicit is still a tie, and the compiler will not pick for you:

```java
import static java.lang.Integer.MAX_VALUE;
import static java.lang.Byte.MAX_VALUE;

class Test {
    public static void main(String[] args) {
        System.out.println(MAX_VALUE);
    }
}
// CE: reference to MAX_VALUE is ambiguous
```

`MIN_VALUE` has the same fight:

```java
import static java.lang.Integer.*;
import static java.lang.Byte.*;

class Test {
    public static void main(String[] args) {
        System.out.println(MIN_VALUE);
    }
}
// CE: reference to MIN_VALUE is ambiguous
```

If you never **use** the name, there is no ambiguity — imports are checked when the simple name actually appears. Parallel to last video's `Date` case (util + sql): the problem comes from writing `Date d`, not from merely importing both packages.

```java
import static java.lang.Integer.*;
import static java.lang.Byte.*;

class Test {
    public static void main(String[] args) {
        System.out.println("no MAX_VALUE used");
    }
}
// prints no MAX_VALUE used
```

Names that do **not** clash are fine even with both stars. `Integer` has `MAX_VALUE`; `Thread` has `MAX_PRIORITY` — different simple names, no fight:

```java
import static java.lang.Integer.*;
import static java.lang.Thread.*;

class Test {
    public static void main(String[] args) {
        System.out.println(MAX_VALUE);
        System.out.println(MAX_PRIORITY);
    }
}
// prints 2147483647
// prints 10
```

## 1:00:10 — Why ambiguity is rare in normal import, common in static import

Board note (write this; exam paragraph):

Two packages containing a **class or interface with the same name** is very rare (`Date` in util and sql, `List` in util and awt) — hence ambiguity in **normal import** is rare. Two classes containing a **method or variable with the same name** is very common (`MAX_VALUE`, `MIN_VALUE`, `MAX_PRIORITY` vs somebody's own `max`, …) — hence ambiguity in **static import** is also very common. That is one more reason it is considered a flop feature.

Resolve it the honest way — put the class name back. Then static import was a waste:

```java
import static java.lang.Integer.*;
import static java.lang.Byte.*;

class Test {
    public static void main(String[] args) {
        System.out.println(Integer.MAX_VALUE);
        System.out.println(Byte.MAX_VALUE);
    }
}
// prints 2147483647
// prints 127
```

## 1:04:20 — Precedence while resolving static members

Board heading: while resolving static members. Compiler gives precedence in this order (highest first):

1. **Current class static members**
2. **Explicit static import**
3. **Implicit static import**

Compare with last video's class-name order: explicit class import → current working directory → implicit class import. Same *explicit beats implicit* idea, plus "our own class wins everything."

He writes three lines and comments them one by one. All three present — current class wins:

```java
import static java.lang.Integer.MAX_VALUE;
import static java.lang.Byte.*;

class Test {
    static int MAX_VALUE = 999;

    public static void main(String[] args) {
        System.out.println(MAX_VALUE);
    }
}
// prints 999
```

Comment out the field — explicit Integer beats implicit Byte:

```java
import static java.lang.Integer.MAX_VALUE;
import static java.lang.Byte.*;

class Test {
    public static void main(String[] args) {
        System.out.println(MAX_VALUE);
    }
}
// prints 2147483647
```

Comment out the explicit import too — only implicit Byte remains:

```java
import static java.lang.Byte.*;

class Test {
    public static void main(String[] args) {
        System.out.println(MAX_VALUE);
    }
}
// prints 127
```

Only explicit Byte (no Integer, no current class):

```java
import static java.lang.Byte.MAX_VALUE;

class Test {
    public static void main(String[] args) {
        System.out.println(MAX_VALUE);
    }
}
// prints 127
```

Implicit Integer vs implicit Byte — both same level — ambiguous (already seen). Explicit Integer vs explicit Byte — both same level — also ambiguous.

Current class **method** with the same name also wins over static-imported methods:

```java
import static java.lang.Math.max;

class Test {
    static int max(int a, int b) {
        return a + b; // our own method, not Math.max
    }

    public static void main(String[] args) {
        System.out.println(max(10, 20));
    }
}
// prints 30
```

Reader sees `max(10, 20)` and thinks Math. Output is `30`. *This is the confusion* the experts point at, live on the board.

## 1:08:40 — Which of the following import statements are valid?

Board heading: which of the following import statements are valid? Exam style — each shown as its own tiny program so the CE reason is attached to real Java.

**(1) Normal explicit class import — valid** (redundant for `java.lang`, but valid):

```java
import java.lang.Math;

class Test {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(4));
    }
}
// prints 2.0
```

**(2) `.*` after a class name as a normal import — not meaningful.** Math has no nested type we use — after a class, `.*` imports nested types, not static methods:

```java
import java.lang.Math.*; // not meaningful as a way to get sqrt

class Test {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(4));
        // System.out.println(sqrt(4));
        // CE if uncommented: cannot find symbol method sqrt(int)
    }
}
// prints 2.0
```

**(3) Normal import of a method — invalid:**

```java
import java.lang.Math.sqrt; // CE: cannot find symbol class sqrt

class Test {
    public static void main(String[] args) {
        System.out.println("never reached");
    }
}
```

**(4) Static import of the class itself — invalid:**

```java
import static java.lang.Math; // CE: static import only from classes and interfaces

class Test {
    public static void main(String[] args) {
        System.out.println("never reached");
    }
}
```

**(5) Implicit static import — valid:**

```java
import static java.lang.Math.*;

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
    }
}
// prints 2.0
```

**(6) Explicit static import — valid:**

```java
import static java.lang.Math.sqrt;

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
    }
}
// prints 2.0
```

**(7) Static import of `out` — valid:**

```java
import static java.lang.System.out;

class Test {
    public static void main(String[] args) {
        out.println("ok");
    }
}
// prints ok
```

**(8) Static import of `Integer.MAX_VALUE` — valid:**

```java
import static java.lang.Integer.MAX_VALUE;

class Test {
    public static void main(String[] args) {
        System.out.println(MAX_VALUE);
    }
}
// prints 2147483647
```

**(9) `import static java.lang.Integer.*_VALUE` — invalid** (no wildcard in the middle of a name; SCJP-style distractor):

```java
import static java.lang.Integer.*_VALUE; // CE: ';' expected — malformed import

class Test {
    public static void main(String[] args) {
        System.out.println("never reached");
    }
}
```

Quick scoreboard he wants in memory:

| Statement | Valid? |
|---|---|
| `import java.lang.Math;` | yes (normal class import) |
| `import java.lang.Math.sqrt;` | no |
| `import static java.lang.Math;` | no |
| `import static java.lang.Math.*;` | yes |
| `import static java.lang.Math.sqrt;` | yes |
| `import static java.lang.Math.sqrt();` | no |
| `static import java.lang.Math.sqrt;` | no |
| `import java.lang.System.out;` | no |
| `import static java.lang.System.out;` | yes |
| `import static java.lang.System.out.println;` | no |
| `import static java.lang.Integer.MAX_VALUE;` | yes |
| `import java.lang.Integer.MAX_VALUE;` | no |

## 1:11:20 — Difference between general import and static import

Board heading: what is the difference between general import and static import?

**General / normal import**
- Purpose: import **classes and interfaces** of a package.
- After writing it we can use **short names** of those types — fully qualified name is not required.
- Example: `import java.util.ArrayList;` then `ArrayList l = new ArrayList();`

**Static import**
- Purpose: import **static members** (methods and variables) of a particular class.
- After writing it we can access those members **without the class name**.
- Example: `import static java.lang.Math.sqrt;` then `sqrt(4)` instead of `Math.sqrt(4)`.

Side by side:

```java
import java.util.ArrayList; // general import — type ArrayList

class Test {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        System.out.println(l.getClass().getName());
    }
}
// prints java.util.ArrayList
```

```java
import static java.lang.Math.sqrt; // static import — member sqrt

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(16));
    }
}
// prints 4.0
```

We can use **both** in the same source file — they solve different problems, and neither replaces the other:

```java
import java.util.ArrayList;
import static java.lang.Math.sqrt;
import static java.lang.System.out;

class Test {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
        l.add("durga");
        out.println(sqrt(4));
        out.println(l.size());
    }
}
// prints 2.0
// prints 1
```

General import cannot pull in `sqrt`. Static import cannot pull in `ArrayList`. `Integer.parseInt` is another static method people static-import in exam code:

```java
import static java.lang.Integer.parseInt;
import static java.lang.System.out;

class Test {
    public static void main(String[] args) {
        int x = parseInt("10");
        out.println(x);
    }
}
// prints 10
```

Without that static import:

```java
class Test {
    public static void main(String[] args) {
        int x = Integer.parseInt("10");
        System.out.println(x);
    }
}
// prints 10
```

## 1:12:40 — Why never recommended — closing the topic

He returns to `MAX_VALUE` without a class name. Open a 2000-line file, see `MAX_VALUE` — whose? Integer? Byte? Short? Our own class? You cannot say until you scroll to the import section, and even then it might lose to a current-class field. **Readability down, confusion up.**

Sun said the opposite; experts (and later Sun's own 1.6 advice) said: if there is no specific requirement, never recommended. Specific requirement they have in mind: you are hammering constants from **one** class (lots of `Math.PI` / `Math.sin` in a scientific class) and not mixing two classes that share names. Even then, explicit static import of the two or three names you need is less dirty than `*`.

Static import is a **compile-time** shortcut, like normal import. More static imports can mean marginally more compile work, but **no change in execution time** — at runtime the bytecode still refers to `Math.sqrt` / `System.out`. Don't tell an interviewer that static import makes the program faster.

> ⚠️ **Modern Java — the "never recommended" verdict has softened for specific vocabularies.**
> Sir's advice is still correct for hiding arbitrary constants from two unrelated classes — the `MAX_VALUE` ambiguity trap above is exactly as real today. But modern idiomatic Java leans on static import constantly in two settings this course predates: test assertions (`import static org.junit.jupiter.api.Assertions.*;` → `assertEquals(...)`, `assertThrows(...)`) and stream/collector code (`import static java.util.stream.Collectors.toList;`, `import static java.util.Map.entry;`). In both cases the imported names read as a small, well-known vocabulary rather than an arbitrary grab-bag — which is precisely the "specific requirement" exception Sir already carves out, just wider in practice than 2008-era Java code suggested. The mechanics (explicit vs implicit, precedence, ambiguity) have not changed since Java 5.

Board recap he wants you to photocopy:

- Came in 1.5. Considered a flop feature by experts, still asked about on the exam.
- Writing: `import static`. Speaking: static import.
- Two types: explicit (`Class.member`) and implicit (`Class.*`).
- `java.lang.Math` is already available; `sqrt()` still needs static import.
- `System` = class, `out` = static `PrintStream`, `println` = instance method. Static-import `out`, then `out.println(...)`.
- Cannot static-import `println`. Cannot normal-import `out`.
- Two static imports of the same simple name → `reference to X is ambiguous`.
- Precedence: current class static members → explicit static import → implicit static import.
- Normal import → types. Static import → static members.
- If no specific requirement, **not recommended**.

## Exam and interview points

1. **Static import removes the class name for static members only** — it cannot pull in instance methods (`println`), and normal import cannot pull in fields or methods (`out`, `sqrt`) — each tool has one job.
2. **Wrong syntax is a classic distractor**: `static import ...` (word order swapped) and `import static ...sqrt();` (parentheses added) are both compile errors, not valid alternate forms.
3. **`java.lang` being default-imported only makes the class available, not its members unqualified.** `Math.sqrt(4)` compiles with zero imports; `sqrt(4)` still needs `import static java.lang.Math.sqrt;` or `.*`.
4. **`System.out.println` is class → static field → instance method** — `System` (class), `out` (static `PrintStream`), `println` (instance method on `PrintStream`). Static-importing `out` gets you `out.println(...)`; there is no way to static-import `println` itself.
5. **Ambiguity is the #1 gotcha**: two static imports exposing the same simple name (`Integer.MAX_VALUE` and `Byte.MAX_VALUE`) compile fine until you actually *use* that name — then it's `reference to X is ambiguous`, whether both imports are implicit, both explicit, or one of each.
6. **Precedence order, memorise exactly**: current class's own static member → explicit static import → implicit static import. A field in your own class always wins, even over an explicit static import of the same name.
7. **Static import is compile-time only** — it changes nothing about the generated bytecode or runtime speed; the long form (`System.out.println(...)`) always remains valid even after a static import of `out`.
8. **The official verdict, then and now**: valid, occasionally useful for one class's constants, but not recommended as a default habit — hiding where a name comes from costs more readability than it saves in typing.

---

**Next:** Video 033 — package statement
