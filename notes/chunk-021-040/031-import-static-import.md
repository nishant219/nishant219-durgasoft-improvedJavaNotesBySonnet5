# Video 031 — import and static import

## Video info

| Field | Detail |
|---|---|
| Playlist | Core Java with OCJP/SCJP — Durga Sir |
| Position | Video 31 of 203 |
| Series | Declarations and Access Modifiers · Part 2 of 11 |
| Topic | Types of import; nine exam cases; `#include` vs `import`; 1.5 features; static import |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 39m 31s |
| Watch | https://www.youtube.com/watch?v=aXA59eIWkw0 |
| Playlist | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Last session covered why `import` exists: it lets you write short names
(`ArrayList`, `LinkedList`) instead of typing the fully qualified name every
time — a typing shortcut, nothing more.

This video works through **nine exam-style cases** about `import`, then
introduces **static import** — new in 1.5, and, in Sir's verdict, the one
1.5 feature that flopped.

1. Two types of import — explicit vs implicit — and why explicit wins
2. Which import statements are actually meaningful
3. A fully qualified name makes `import` unnecessary
4. The `Date` / `List` ambiguity trap
5. Resolution order: explicit → current working directory → implicit
6. Importing a package does not import its subpackages
7. The two packages you never need to import
8. Import is a compile-time-only concept
9. C's `#include` vs Java's `import` (a favourite interview question)
10. Static import: the syntax, Sun's pitch, and the community's verdict

---

## 00:05 — Recap

One agreement at the top of the file — the import statement — means that
wherever `ArrayList` appears in the code, it stands for `java.util.ArrayList`.

## 00:45 — Case 1: types of import statements

Two kinds:

```java
import java.util.ArrayList; // explicit — import this one particular class
```

```java
import java.util.*; // implicit — import every class and interface in util
```

Is explicit or implicit recommended? The classroom's answer is "it depends" —
one or two classes, go explicit; twenty classes from the same package, go
implicit. Sir overrules that: **even for a hundred classes from the same
package, use explicit class import.** Implicit is never recommended — he
calls it "almost a banned terminology."

### 04:39 — Why implicit hurts: the HDFC / ICICI story

```java
// illustrative — com.hdfc and com.icici are not real Java packages
import com.hdfc.*;
import com.icici.*;

class Test {
    void m1() {
        Account a = new Account();
        a.getInfo();
        Loan l = new Loan();
        l.getInterestRate();
    }
}
```

Sir is handed this code and asked to review it. Where is `Account.getInfo()`
implemented? He opens `com.hdfc` — fifteen minutes, no `Account` there. He
opens `com.icici` — found it. Then `Loan.getInterestRate()`: not in `com.icici`,
found in `com.hdfc` after half an hour. Two classes, half an hour lost, because
the `*` import hides which package each class actually comes from.

Swap to explicit imports and the same code tells you immediately:

```java
import com.hdfc.Account;
import com.icici.Loan;

class Test {
    void m1() {
        Account a = new Account();
        a.getInfo();
        Loan l = new Loan();
        l.getInterestRate();
    }
}
```

`Loan` is from ICICI, `Account` is from HDFC — readable at a glance. Sir's
framing: **typing is a one-time activity; reading and analysing code is a
many-times activity.** Optimise for the many, not the one. His shorthand for
the two audiences: **Hi-tech City** (professional delivery — readability
matters, go explicit) versus **Ameerpet** (typing-speed training centres —
typing matters, and you're not shipping the code to anyone, so implicit is
tolerated there).

> **Board:**
> *Explicit class import — highly recommended, because it improves
> readability. Best suited for Hi-tech City, where readability is important.*
> *Implicit class import — not recommended, because it reduces readability.
> Best suited for Ameerpet, where typing is important.*

## 12:44 — Case 2: which import statements are meaningful?

```java
import java.util.ArrayList;   // 1 — meaningful: explicit class import
import java.util.ArrayList.*; // 2 — meaningless: nothing to import here
import java.util.*;           // 3 — meaningful: implicit class import
import java.util;             // 4 — CE: cannot find symbol (java.util is a package, not a type)
```

1. `java.util.ArrayList` — explicit, meaningful.
2. A `.*` **after a class name** asks for the member types nested *inside*
   that class. `ArrayList` declares none, so this import brings in nothing —
   pointless, but not an error.
3. `java.util.*` — implicit, meaningful: every class and interface in `util`.
4. A package name followed directly by a semicolon is not a legal import at
   all; after a package name you must write `.*` or `.ClassName`.

> ❗ **Correction — line 2 does not fail to compile.**
> Sir's verdict was "not meaningful," and that's right about its usefulness —
> but it can read as "this won't compile," which is wrong. `import
> TypeName.*;` is legal Java (JLS §7.5.2): it imports the accessible *member
> types* of a class (its `public`/`protected` nested classes, interfaces, and
> enums). `ArrayList` has none, so the statement compiles cleanly and simply
> imports nothing — confirmed with `javac`. Contrast a class that *does* have
> nested types, e.g. `import java.util.Map.*;` legitimately pulls in
> `Map.Entry`.

## 16:52 — Case 3: a fully qualified name makes import unnecessary

```java
class MyObject extends java.rmi.server.UnicastRemoteObject {
    protected MyObject() throws java.rmi.RemoteException {
        super();
    }
}
```

No `import` anywhere, yet this compiles. Why? Because the superclass is
referenced by its **fully qualified name** (FQN) — `java.rmi.server` is
spelled out in full. Sir's rule: whenever you use an FQN, `import` is not required;
whenever you write `import`, the FQN is not required. **Import and fully
qualified names are alternatives, not partners** — you only ever need one of
the two for a given class reference.

> **Board:** *The code compiles fine even though we are not writing an import
> statement, because we used a fully qualified name. Whenever we use a fully
> qualified name it is not required to write an import statement; whenever we
> write an import statement it is not required to use a fully qualified name.*

## 22:00 — Case 4: `Date` is ambiguous (a dangerous case)

```java
import java.util.*;
import java.sql.*;

class Test {
    public static void main(String[] args) {
        Date d = new Date();
        // CE: reference to Date is ambiguous
        //   both class java.sql.Date in java.sql and
        //   class java.util.Date in java.util match
    }
}
```

`Date` exists in **both** `java.util` and `java.sql`. Sir's story: he tells the
compiler to just pick one, the compiler picks `util.Date`, he wanted `sql.Date`
this time — "left and right," don't decide on your own. Next run he wants
`util`, the compiler (having learned its lesson) picks `sql`. Third time the
compiler refuses outright: tell me which `Date` you mean, or I'm not
compiling. That refusal is the real compiler error, reproduced above.

If the ambiguous name is never actually *used*, there's no error — the clash
only bites the moment you reference the bare name.

The same trap catches **`List`**: it exists in `java.util` (the collection)
and in `java.awt` (a GUI list-of-options component).

```java
import java.util.*;
import java.awt.*;

class Test {
    public static void main(String[] args) {
        List l = null;
        // CE: reference to List is ambiguous
        //   both class java.awt.List in java.awt and
        //   interface java.util.List in java.util match
    }
}
```

> **Board:** *Even in the case of `List`, we may get the same ambiguity
> problem, because it is available in both `util` and `awt` packages.*

### 32:33 — Explicit beats implicit

Same `Date` clash, but make one of the two imports explicit:

```java
import java.util.Date; // explicit
import java.sql.*;     // implicit

class Test {
    public static void main(String[] args) {
        Date d = new Date(); // compiles — the explicit import wins
    }
}
```

This compiles. The compiler gives **explicit class import more priority than
implicit**, so `util.Date` is chosen without a fight.

## 33:35 — Case 5: the order the compiler resolves class names in

The thumb rule, highest priority first:

1. **Explicit class import**
2. **Classes in the current working directory** (the default package)
3. **Implicit class import**

```java
import java.util.Date;
import java.sql.*;

class Test {
    public static void main(String[] args) {
        Date d = new Date();
        System.out.println(d.getClass().getName());
        // prints java.util.Date — the explicit import won
    }
}
```

Comment out the explicit line and only `import java.sql.*;` remains: even
then, a `Date` class sitting in the **current working directory** (default
package) is chosen ahead of `java.sql.Date`. Only if the CWD has no `Date` at
all does the implicit `java.sql.*` finally get considered. Verified by
compiling a bare `class Date {}` alongside the test class: the CWD version
wins, printing the unqualified name `Date`.

> **Board:** *While resolving class names, the compiler always gives
> precedence in this order: (1) explicit class import, (2) classes present in
> the current working directory (default package), (3) implicit class
> import.*

## 40:23 — Case 6: importing a package does not import its subpackages

`Pattern` (regular expressions) lives in `java.util.regex` — a *subpackage*
of `util`. Which import actually brings it in?

```java
import java.*;              // 1 — not enough
import java.util.*;         // 2 — not enough
import java.util.regex.*;   // 3 — correct
// 4 — "no import required"  — wrong
```

Whenever you import a package, every class and interface **directly inside**
that package becomes available — **but not the classes of any subpackage**.
To reach a subpackage class you must write the import all the way down to
that subpackage. Answer: **3**.

```java
import java.util.*;

class Pat1 {
    public static void main(String[] args) {
        Pattern p = Pattern.compile("a+");
        // CE: cannot find symbol — Pattern lives in java.util.regex,
        // not java.util, so import java.util.*; does not reach it
    }
}
```

```java
import java.util.regex.*; // or: import java.util.regex.Pattern;

class Pat2 {
    public static void main(String[] args) {
        Pattern p = Pattern.compile("a+");
        System.out.println(p.matcher("aaa").matches()); // true
    }
}
```

Sir's proof-by-contradiction: if subpackages loaded automatically, a single
`import java.*;` would be enough for everything under `java` — nobody would
ever need to write `import java.util.*;` or `import java.sql.*;` separately.
The fact that those separate imports are necessary shows subpackages are not
included for free.

Second proof: `java.lang` classes are available with no import at all, yet
`Method` (in `java.lang.reflect`, a subpackage of `lang`) still needs its own
import:

```java
import java.lang.reflect.Method;
// or: import java.lang.reflect.*;

class Refl {
    public static void main(String[] args) throws Exception {
        Method m = String.class.getMethod("length");
        System.out.println(m.getName()); // length
    }
}
```

> **Board:** *Whenever we import a Java package, all classes and interfaces
> present in that package are, by default, available — but not subpackage
> classes. To use a subpackage class we must compulsorily write the import
> statement until the subpackage level.*
>
> Diagram: `java` → `util` → `regex` → `Pattern`.

## 50:05 — Case 7: the two packages you never need to import

All classes and interfaces in these two are available to every Java program
without any `import`:

1. **`java.lang`**
2. **The default package** — classes in the current working directory

```java
class Test {
    public static void main(String[] args) {
        String s = new String("Durga"); // String is in java.lang — no import
        System.out.println(s);
    }
}
```

```java
// Student.java — same folder, default package
class Student {
    String name;
    int rollNo;
    Student(String name, int rollNo) {
        this.name = name;
        this.rollNo = rollNo;
    }
}
```

```java
// Test.java — same folder as Student.java, no import needed
class Test {
    public static void main(String[] args) {
        Student s1 = new Student("Durga", 101);
        System.out.println(s1.name + "..." + s1.rollNo); // Durga...101
    }
}
```

`Student.java` sits in the same current working directory, so `Test.java`
compiles against it with zero imports.

> **Board:** *All classes and interfaces present in the following packages
> are, by default, available to every Java program — hence we are not
> required to write an import statement: (1) `java.lang` package, (2) default
> package (current working directory).*

## 56:02 — Case 8: import is a compile-time concept

Two programs doing identical work:

```java
// Program 1 — fully qualified names, no import
class Test {
    public static void main(String[] args) {
        java.util.ArrayList l = new java.util.ArrayList();
    }
}
```

```java
// Program 2 — short names + import
import java.util.ArrayList;

class Test {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
    }
}
```

**Which compiles slower?** Program 2. With the FQN, the compiler already has
everything it needs. With the short name `ArrayList`, the compiler must first
scan the import statements to work out that `ArrayList` means
`java.util.ArrayList` — extra work, extra compile time.

**Which runs slower?** Neither — they run at the same speed. Sir flags the
common misconception ("more compile time must mean more execution time") and
rejects it directly: if using an FQN genuinely cost execution time, it would
be forbidden outright — "we can compromise on anything except performance."
Import resolution is purely a **compile-time** activity; it has zero effect
at runtime.

> **Board:** *Import statements are a totally compile-time-related concept.
> More imports means more compile time, but there is no effect on execution
> time (run time).*

## 1:02:49 — Case 9: C's `#include` vs Java's `import` (an interview favourite)

A common (and wrong) claim, repeated by faculty and textbooks alike: Java's
`import` is "the same as" C's `#include`. Functionally, it is not.

```c
/* C — not Java: loads every declared header at translation time */
#include <stdio.h>
```

```java
import java.io.*;
```

In C, `#include` performs a **static include**: every header you name is
loaded up front, at translation time, whether or not you end up using
anything in it.

In Java, the `import` line loads **nothing**. A class's `.class` file is
loaded only when that class is first *used*, at runtime — **load on demand**
(also called load on the fly, or dynamic include).

Java's approach is the better one: loading all ~5,000 JDK classes at startup,
whether used or not, would waste memory and hurt performance for no benefit —
you don't know in advance which I/O classes (or any classes) a given run will
actually touch.

> **Board:** *In C, `#include` loads all header files at the beginning
> (translation time) — a static include. In Java, no `.class` file loads at
> the beginning; whenever a class is first used, only then is its `.class`
> file loaded. This is a dynamic include / load-on-demand / load-on-the-fly.*

Nine cases down. Recap: two types of import, explicit strongly preferred; FQN
and import are interchangeable alternatives.

Sir adds one absolute claim while wrapping up: "no IDE in the universe
generates implicit import statements" — since Eclipse/MyEclipse write out
imports for you, and they always write explicit ones.

> ❗ **Correction — some IDEs do generate `*` imports, by design.**
> Eclipse and MyEclipse default to explicit, matching what Sir says. But
> **IntelliJ IDEA** ships with "Class count to use import with `*`" set to
> **5** (Settings → Editor → Code Style → Java → Imports): use five or more
> classes from one package and IDEA collapses them into a single `import
> pkg.*;` automatically, with a matching threshold for static imports.
> Eclipse offers the same behaviour as an opt-in ("Number of imports needed
> for `.*`" under Organize Imports). "No IDE" was never literally true; the
> defensible claim is narrower: *your* IDE's default, and most shops' style
> guides, favour explicit.

## 1:12:41 — 1.5's new features, and the static-import tease

Sir's analogy: a movie's producers always promise a blockbuster before
release — pre-release hype is no guarantee of a hit, and audiences alone
decide (his example: *Orange*, hyped hard, flopped). Java 1.5 got the same
treatment: a "press meet" declaring it would "pack all other languages,"
and this time the hype mostly held up — worldwide programmers judged most
1.5 features genuinely simplified the language:

```text
for-each loop
var-arg methods
autoboxing and auto-unboxing
generics
covariant return types
Queue (collections)
annotations
enum
static import
```

Every feature on that list was a hit except one: **static import** — Sir
calls it the one "flop" of the 1.5 release, and the next section explains why.

## 1:22:06 — Static import: Sun's pitch vs the world's verdict

Static import arrived in **1.5**.

**Sun's position:** static import reduces code length and improves
readability.

**Sir's position (shared with "worldwide programming experts"):** static
import creates confusion and *reduces* readability. Verdict: **if there is no
specific requirement, do not use static import.** For the exam, know what it
is, its stated advantage, and why it's discouraged in practice.

### 1:26:37 — Without static import vs with static import

Static members are normally accessed through their class name:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(Math.sqrt(4));
        System.out.println(Math.max(10, 20));
        System.out.println(Math.random());
    }
}
```

Static import lets you drop the class name entirely, member by member:

```java
import static java.lang.Math.sqrt;

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
        System.out.println(max(10, 20));   // CE: cannot find symbol
        System.out.println(random());      // CE: cannot find symbol
    }
}
```

This does **not** compile — only `sqrt` was statically imported; `max` and
`random` still need either their class name or their own static import. Use
the on-demand form to pull in every static member at once:

```java
import static java.lang.Math.*;

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
        System.out.println(max(10, 20));
        System.out.println(random());
    }
}
```

Now it compiles and runs. The need for static import in one line: you access
static members through the class name *unless* you specifically want to
reach them without it — that's what static import is for.

One spelling note Sir flags directly: **while writing it, the keyword order
is `import static`; while pronouncing the concept, everyone says "static
import."** Don't let the reversed word order in speech throw off the syntax.

### 1:33:22 — Live compile: three errors, then two, then none

```java
class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));
        System.out.println(max(10, 20));
        System.out.println(random());
    }
}
// CE: cannot find symbol method sqrt
// CE: cannot find symbol method max
// CE: cannot find symbol method random
```

Three errors with no static import at all.

```java
import static java.lang.Math.sqrt;

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));     // OK now
        System.out.println(max(10, 20)); // CE: cannot find symbol
        System.out.println(random());    // CE: cannot find symbol
    }
}
```

Down to two errors — `sqrt` resolves, `max` and `random` still don't.

```java
import static java.lang.Math.*;

class Test {
    public static void main(String[] args) {
        System.out.println(sqrt(4));       // 2.0 — sqrt returns double
        System.out.println(max(10, 20));   // 20
        System.out.println(random());      // a different double each run
    }
}
```

Zero errors. `sqrt(4)` prints `2.0` (`Math.sqrt` returns `double`), `max(10,
20)` prints `20`, and `random()` prints a fresh value between 0 and 1 on every
run — Sir runs it three times live and gets three different numbers.

> **Board:** *Usually we access static members by using the class name; but
> whenever we write static import, we can access static members directly
> without the class name.*

> ⚠️ **Modern Java — static import is no longer purely a "flop."**
> The 1.6-era advice ("avoid unless there's a specific requirement") is still
> the safe default for arbitrary business classes. But idiomatic modern Java
> leans on static import routinely for a short list of very well-known,
> unambiguous APIs, where it's now the expected style rather than a red
> flag:
>
> - `import static java.util.stream.Collectors.*;` in stream pipelines
>   (`.collect(toList())`, `.collect(groupingBy(...))`)
> - `import static org.junit.jupiter.api.Assertions.*;` in JUnit 5 tests
>   (`assertEquals(...)`, `assertThrows(...)`)
> - `import static java.util.Map.entry;` when building small maps
>   (`Map.ofEntries(entry("a", 1), entry("b", 2))`)
>
> Google's Java Style Guide (widely followed today) explicitly permits static
> import for constants and for methods with clear, self-documenting names.
> The rule of thumb hasn't reversed — it has sharpened: static-import a
> handful of very familiar names, never a whole unfamiliar API.

Sir's final line for this session: take special care with the ordering —
`import static` on paper, "static import" out loud. More static-import
loopholes continue in the next video.

---

## Exam and interview points

1. **Explicit class import is always the recommended answer** — even for a
   hundred classes from one package. "Depends on requirement" is the
   classroom's instinct; "always explicit" is Sir's correction to it.
2. **A fully qualified name and `import` are alternatives**, never both
   required together — use one or the other for any given class reference.
3. **`Date` and `List` are the two classic ambiguous-class exam traps** —
   `Date` in `java.util` vs `java.sql`; `List` in `java.util` vs `java.awt`.
   Both produce `reference to X is ambiguous`, and only when the ambiguous
   name is actually referenced.
4. **Resolution order when names could clash**: explicit class import →
   classes in the current working directory (default package) → implicit
   class import. Explicit always wins over implicit.
5. **Importing a package never pulls in its subpackages.** `import
   java.util.*;` does not give you `java.util.regex.Pattern` or
   `java.lang.reflect.Method` — you must import down to the subpackage that
   actually declares the class.
6. **Only two packages need zero import ever**: `java.lang`, and the default
   package (current working directory).
7. **Import is compile-time only.** More imports can slow compilation
   slightly; nothing about imports affects runtime performance.
8. **`import` is not `#include`.** C's `#include` is a static, translation-time
   load of everything named; Java's `import` loads nothing until the class is
   first used — load-on-demand.
9. **Static import syntax is `import static`; the concept is pronounced
   "static import."** `import static java.lang.Math.*;` is required before
   `sqrt(4)`, `max(10, 20)`, or `random()` can be called unqualified — a
   partial static import (just `sqrt`) still leaves the other members
   needing the class name or their own explicit static import.
10. **Static import's official line, 1.6 onward: not recommended without a
    specific requirement.** Know Sun's stated rationale (shorter, more
    readable code) and the community's counter (confusing, less readable) —
    both are fair game for SCJP.

---

**Next:** Video 032 — static import
