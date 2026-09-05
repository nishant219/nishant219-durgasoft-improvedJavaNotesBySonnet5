# Video 033 — The package Statement

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-4 || package statement

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 33 of 203 |
| Series | Declarations and Access Modifiers · Part 4 |
| Topic | package statement, javac -d, at most one package, source-file order, empty file |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 10m 32s |
| Video ID | KHsAkh_JFw0 |
| Watch | https://www.youtube.com/watch?v=KHsAkh_JFw0 |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. What a package is — a grouping / encapsulation mechanism.
2. Examples: `java.sql`, `java.io`, plus `java.rmi`, `java.net`, `java.util`.
3. Four advantages: naming conflicts, modularity, maintainability, security (package as a wall).
4. The universally accepted naming convention — internet domain name in reverse.
5. How to write `package com.durgasoft.scjp;`.
6. `javac Test.java` vs `javac -d . Test.java` — what `-d` actually does.
7. `-d` creates missing package folders; whether the destination itself must already exist.
8. Running with the fully qualified name: `java com.durgasoft.scjp.Test`.
9. Conclusion 1 — **at most one** package statement per source file.
10. Conclusion 2 — the **first non-comment statement** must be `package` (if one is present).
11. The valid source-file structure: package (0–1) → imports (any number) → class/interface/enum (any number).
12. An **empty source file is a valid Java program.**

---

## 00:04 — What a package is

> A package is a group of related things.

Sir's analogy: a South India tour package, a North India tour package, a
Europe tour package — nobody overthinks the word "package" outside
programming, and the Java meaning is the same idea. Core Java, Advanced Java,
and Oracle are related courses grouped as a "basic package"; Struts,
Hibernate, and Spring are a "Frameworks package."

> A package is an **encapsulation mechanism** — a grouping mechanism — to
> group related classes and interfaces into a single unit.

### 02:01 — Example 1: `java.sql`

All classes and interfaces used for **database operations** — `Connection`,
`DriverManager`, `Statement` — are grouped into the `java.sql` package.

```java
class SqlPackageExamples {
    public static void main(String[] args) {
        java.sql.Connection con = null;
        java.sql.Statement st = null;
        System.out.println(con);
        System.out.println(st);
    }
}
```

### 02:26 — Example 2: `java.io`

All classes and interfaces for **file I/O** — `FileWriter`, `BufferedWriter`,
`PrintWriter`, `FileReader`, `BufferedReader` — live inside `java.io`.

```java
class IoPackageExamples {
    public static void main(String[] args) {
        java.io.FileWriter fw = null;
        java.io.BufferedWriter bw = null;
        java.io.PrintWriter pw = null;
        java.io.FileReader fr = null;
        java.io.BufferedReader br = null;
        System.out.println("java.io holds file IO types");
    }
}
```

Sir also names `java.rmi` (remote method invocation), `java.net`
(networking), and `java.util` (general utilities) — "about 11 or 12
packages" in the standard library of that era. Whatever you group for a
particular purpose becomes a package.

---

## 07:30 — Advantage 1: resolve naming conflicts

The **biggest advantage** of a package statement: it resolves naming
conflicts. Sir's analogy — one Chief Minister for Telangana, one for Andhra
Pradesh, one for Tamil Nadu, one for Karnataka. Without states, only one CM
could exist anywhere. Without packages, only one `Date` class could exist
anywhere — but `java.util.Date` and `java.sql.Date` both exist, because the
package gives each one a unique identity.

```java
class TwoDateClasses {
    public static void main(String[] args) {
        java.util.Date utilDate = new java.util.Date();
        java.sql.Date sqlDate = new java.sql.Date(0L);
        // unique identification because of the package
        System.out.println(utilDate);
        System.out.println(sqlDate);
    }
}
```

## 09:00 — Advantages 2 and 3: modularity and maintainability

Grouping order-processing classes into one package and order-delivery classes
into another package improves **modularity** — and dividing an application
module by module (order, payment, transaction, …) improves
**maintainability**, because managing small grouped units beats managing one
clumsy pile of classes.

```java
package com.xyz.order.process;

class ProcessOrder {
    public static void main(String[] args) {
        System.out.println("order processing module");
    }
}
```

```java
package com.xyz.order.delivery;

class DeliverOrder {
    public static void main(String[] args) {
        System.out.println("order delivery module");
    }
}
```

```java
package com.xyz.order;

class OrderModule {
    public static void main(String[] args) {
        System.out.println("order module");
    }
}
```

## 11:22 — Advantage 4: security — the package as a wall

A class with **default** access (no modifier written) can be used only
**within its own package**. An outside package cannot reach it at all — the
package acts as a wall around the class, which is why Sir counts this as a
security advantage: without packages, there would be no way to restrict an
outside class from touching yours.

```java
package pack1;

class Test {
    // default / package-private class
    void m1() {
        System.out.println("only pack1 can see Test");
    }
}
```

```java
package pack2;

class Outside {
    public static void main(String[] args) {
        // Test t = new Test();
        // CE: pack1.Test is not public; cannot be accessed from outside its package
        System.out.println("package acts as a wall");
    }
}
```

### 12:53 — The four advantages, on the board

1. To resolve **naming conflicts** — unique identification of components.
2. Improves **modularity** of the application.
3. Improves **maintainability** of the application.
4. Provides **security** for components.

---

## 15:14 — Naming convention: internet domain name in reverse

Since a package's purpose is unique identification, the language needed a
naming scheme that is unique by construction. A company name is not unique —
several small companies can share "Infosys" in their name. An internet
domain name is: only one website is `gmail.com`, only one is `yahoo.com`.
Programming convention therefore uses the **domain name in reverse** as the
package prefix.

```java
package com.icicibank.loan.housing;

public class Account {
    public static void main(String[] args) {
        System.out.println("com.icicibank = domain reverse");
        System.out.println("loan = module");
        System.out.println("housing = sub-module");
        System.out.println("Account = class");
    }
}
```

| Segment | Meaning |
|---|---|
| `com.icicibank` | client's internet domain name, reversed |
| `loan` | module name |
| `housing` | sub-module name |
| `Account` | class name |

Sir's point: find this fully qualified name on a piece of paper anywhere, and
you instantly know it's an ICICI Bank component, in the loan module, housing
sub-module — no further reading required. That is what the naming convention
buys you. He also warns against classroom-style names like `pack1`, `pack2`,
`packX` in real code — those exist here purely as short exam-style demo
names.

---

## 22:08 — Writing the package statement

`package` is a Java keyword, written as the very first thing in the file:

```java
package com.durgasoft.scjp;

public class Test {
    public static void main(String[] args) {
        System.out.println("package demo");
    }
}
```

### 23:40 — Compiling without `-d`: `javac Test.java`

Does this compile even though the file declares a package? **Yes** — a
package statement never blocks a normal compile. But the generated
`Test.class` is placed in the **current working directory**, not inside a
`com/durgasoft/scjp/` structure — which is meaningless once you actually try
to organize a project by package.

```java
class CompileWithoutDashD {
    public static void main(String[] args) {
        // javac Test.java
        // compiles fine
        // Test.class ends up in the current working directory, not in a package tree
        System.out.println("legal but class file not in package folders");
    }
}
```

### 25:17 — Compiling with `-d`: `javac -d . Test.java`

`-d` = destination: where to place the generated class files. `.` = the
current working directory. With `-d`, javac places `Test.class` inside the
**package-shaped folder structure** under that destination:
`./com/durgasoft/scjp/Test.class`.

```java
class CompileWithDashD {
    public static void main(String[] args) {
        // javac -d . Test.java
        // Test.class lands under CWD/com/durgasoft/scjp/
        System.out.println("place Test.class under CWD package folders");
    }
}
```

Verified: `javac -d . Test.java` on a class declaring `package
com.durgasoft.scjp;` produces `./com/durgasoft/scjp/Test.class` — exactly as
taught, on current `javac` too.

### 35:01 — Variation 1: missing package folders are created

If `com`, `com/durgasoft`, or `com/durgasoft/scjp` do not already exist,
`-d` creates them itself. There is **no compile error** for missing package
folders — javac builds the whole chain of subdirectories under the
destination.

```java
class DashDCreatesFolders {
    public static void main(String[] args) {
        // javac -d . Test.java
        // if com/durgasoft/scjp does not exist, javac creates it
        System.out.println("package folders created by -d if missing");
    }
}
```

### 37:55 — Variation 2: the destination can be any valid directory

Instead of `.`, Sir uses any existing drive — `C:`, `D:`, `E:`, `F:` on his
Windows machine — and the same package tree gets created under it:
`F:\com\durgasoft\scjp\Test.class`.

```java
class DashDToFColon {
    public static void main(String[] args) {
        // javac -d F: Test.java   (Windows-era demo; F: already existed)
        // F:\com\durgasoft\scjp\Test.class
        System.out.println("destination instead of dot: any valid directory");
    }
}
```

### 42:10 — Variation 3: what if the destination itself is missing?

Sir's live demo: `javac -d J: Test.java`, where `J:` is not a drive present
on his machine, fails with `directory not found: J:`. His conclusion: **if
the specified destination is not already available, `-d` will not create it
— you get a compile-time error.**

```java
class DashDMissingDrive {
    public static void main(String[] args) {
        // javac -d J: Test.java   (no J: drive on this Windows machine)
        // CE: directory not found: J:
        System.out.println("a missing drive letter cannot be created by -d");
    }
}
```

> ❗ **Correction — the rule is "javac cannot create a drive/mount," not "javac cannot create a missing folder."**
> Tested on JDK 26 (macOS): `javac -d some/deeply/nested/newpath Test.java`
> **creates every missing directory level**, not just the package
> subfolders under an existing destination:
>
> ```text
> $ javac -d nosuchdir Test.java     # nosuchdir does not exist yet
> $ find . -name '*.class'
> ./nosuchdir/pack1/Test.class       # -d created nosuchdir itself, then the package tree
> ```
>
> The only thing `-d` genuinely cannot manufacture is a filesystem object the
> OS itself must provide — a drive letter like `J:` that Windows has never
> mounted, or an unmounted volume. That was true then and is true now; it
> was never about ordinary folders. So Sir's demo is accurate for the
> specific case he ran (a nonexistent drive), but "the destination itself
> must already exist" over-generalizes it — an ordinary missing path under an
> existing drive is created just like the package subfolders are.

---

## 45:23 — Running: the fully qualified name is compulsory

`Test.class` lives at `CWD/com/durgasoft/scjp/Test.class`. To run it, you
**must** give the fully qualified name — you cannot `cd` into `com` and run
a short name from there.

```java
class RunPackagedClass {
    public static void main(String[] args) {
        // java com.durgasoft.scjp.Test
        // prints: package demo
        System.out.println("run with the fully qualified name");
    }
}
```

Verified: `java com.durgasoft.scjp.Test` (run from the directory that
contains `com/`) prints `package demo`; `java Test` from inside
`com/durgasoft/scjp/` fails with `ClassNotFoundException`.

> ⚠️ **Modern Java — you can skip the separate `javac` step entirely for a quick file.**
> Since **Java 11** (JEP 330, the single-file source-code launcher), `java
> Test.java` compiles the file in memory and runs it directly — handy for
> the kind of one-off demo this whole video is built around. It respects
> packages exactly the way the compiler does: the file's own **path** must
> match its package.
>
> ```text
> $ java Test.java
> error: end of path to source file does not match its package name
>        com.durgasoft.scjp: Test.java
>
> $ java com/durgasoft/scjp/Test.java
> package demo via source launcher
> ```
>
> Both verified on JDK 26. Java 22 (JEP 458) extended the same launcher to
> multi-file source programs. None of this replaces `javac -d` for a real
> build — it is a script-runner convenience, not a packaging tool.

---

## 48:25 — Two SCJP conclusions

### 48:36 — Conclusion 1: at most one package statement

```java
package pack1;
package pack2;

public class A {
}
```

The natural guess is "one class file, placed in whichever package came
first" — wrong framing entirely. **At most one** package statement is
allowed per source file (zero or one; never more). The parser accepts the
first `package pack1;`, then expects either an import or a type declaration
— getting a second `package` instead is an immediate compile error.

```text
$ javac Test.java
Test.java:2: error: class, interface, or enum expected
package pack2;
^
1 error
```

> ⚠️ **Modern Java — the wording of this classic error changed in Java 16.**
> Verified across `--release` levels on JDK 26:
>
> | `--release` | Message |
> |---|---|
> | 8–15 | `class, interface, or enum expected` |
> | 16+ | `class, interface, enum, or record expected` |
>
> Records arrived in Java 16 (JEP 395) as a fourth kind of top-level type
> declaration, so the compiler's recovery message grew a fourth noun. The
> rule Sir teaches — one package statement, then a type declaration is
> expected — is unchanged; only the exact wording of the message is newer.

### 54:32 — Conclusion 2: package must be the first non-comment statement

```java
import java.util.*;
package pack1;

public class A {
}
```

**100% invalid.** Comments may appear anywhere, but if a package statement is
present at all, it must be the **first non-comment statement** in the file.
Package-then-import is fine; import-then-package is not — the compiler is
past the import and expecting a type declaration, and a stray `package`
triggers the same family of error as Conclusion 1.

```java
import java.util.*;
package pack1;

public class A {
}
// javac Test.java
// CE: class, interface, or enum expected   (at the `package pack1;` line)
```

```java
package pack1;
import java.util.*;

public class A {
    public static void main(String[] args) {
        System.out.println("package then import is OK");
    }
}
```

```java
// comments anywhere are fine
package pack1;

import java.util.*;

public class A {
}
```

If there is **no** package statement at all, there is no such rule — an
import or a class can freely be the first line.

---

## 58:58 — Valid Java source-file structure

**Order matters:**

1. Package statement — **at most one** (zero or one).
2. Import statements — **any number**, including zero.
3. Class, interface, or enum declarations — **any number**, including zero.

```java
package pack1;

import java.util.ArrayList;
import java.io.File;

class A {
}

interface I {
}

enum E {
}
```

Sir specifically flags the third line as the trap: most students guess "at
least one" type declaration is required. It is not — the true answer is
**any number**, which the empty-file demo below proves.

## 1:02:04 — An empty source file is a valid Java program

Sir builds five variants of `Test.java` — empty; only a package line; only an
import line; package plus import; and only a class — and compiles each live.
All five compile.

```java
// 1. Test.java, completely empty
// javac Test.java
// compiles fine — an empty source file is a valid Java program
```

```java
package pack1;
// 2. only a package statement — valid
```

```java
import java.util.*;
// 3. only an import statement — valid
```

```java
package pack1;
import java.util.*;
// 4. package + import, no type — valid
```

```java
class Test {
}
// 5. only a class — the one nobody doubts
```

Verified: `javac` on a zero-byte `Test.java` exits `0` with no output. If the
empty file is valid, every less-empty variant above is automatically valid
too — so "at least one type declaration" was never the rule. The correct
answer is **any number**, including zero.

> ⚠️ **Modern Java — a package now also has to live in exactly one module.**
> This video predates the **Java 9** module system (JPMS). A package itself
> did not change, but the language gained a companion file,
> `module-info.java`, that declares a module's exported/required packages —
> and once code is organized into modules, the **same package name cannot be
> split across two modules on the module path** (a "split package," which
> fails at compile or launch time). None of that applies to unmodularized
> classpath code, which is exactly what this lecture (and most legacy OCJP
> material) still runs as.

---

## Exam and interview points

1. **Main purpose of a package**: resolve naming conflicts — `java.util.Date`
   and `java.sql.Date` coexist only because packages give each a distinct
   identity.
2. **Four advantages**: naming-conflict resolution, modularity,
   maintainability, security (default-access classes are invisible outside
   their own package).
3. **Naming convention**: internet domain name in reverse
   (`com.icicibank.loan.housing`) — unique by construction, unlike a company
   or product name.
4. **`javac Test.java` compiles fine** even with a package statement — the
   `.class` file just lands in the current working directory, not a package
   tree. Use `javac -d .` (or another destination) to get the real folder
   structure.
5. **`-d` creates missing package subfolders automatically** — and, verified
   on current `javac`, it will create the destination path itself too. The
   one thing it truly cannot create is an OS-level object like an unmounted
   drive letter.
6. **Running a packaged class requires the fully qualified name** —
   `java com.durgasoft.scjp.Test`, never a bare `java Test` from inside the
   package folder.
7. **At most one package statement per file** — a second one is a compile
   error reading `class, interface, or enum expected` (or, since Java 16,
   `class, interface, enum, or record expected`) at the offending line, not
   some "duplicate package" message.
8. **If present, `package` must be the first non-comment statement** — an
   import (or anything else) before it is the same class-of-error as two
   package statements.
9. **Valid source-file order**: package (0–1) → imports (any number) →
   types (any number, including zero).
10. **An empty `.java` file is a valid, compilable Java program** — the
    classic trick question behind "how many classes must a source file
    contain?"

---

**Next:** Video 034 — Class Modifier: `final`
