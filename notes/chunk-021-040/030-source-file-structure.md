# Video 030 — Java Source File Structure

## Video info

**Title:** Core Java With OCJP/SCJP: Declarations and Access Modifiers Part-1 || Java Source File Structure

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 30 of 203 |
| Series | Declarations and Access Modifiers · Part 1 of 11 |
| Topic | Java source file structure; public class vs file name; multiple mains; import as typing shortcut |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 06m 36s |
| Video ID | O3kDqVEbfMk |
| Watch | https://www.youtube.com/watch?v=O3kDqVEbfMk |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

New block: **Declarations and Access Modifiers**. Four lines of agenda, but
Sir warns it is roughly **20 hours** of material:

1. Java source file structure — 5 to 6 hours
2. Class level modifiers — 4 to 5 hours
3. Member level modifiers — 4 to 5 hours
4. Interfaces — 4 to 5 hours

This video covers source-file structure end to end, then introduces
**import** (fully qualified name vs short name). Don't underestimate four
lines of agenda.

---

## 02:14 — How many classes can a Java program contain?

Board heading: **Java source file structure**.

A Java program can contain **any number of classes**:

```java
class A {
}

class B {
}

class C {
}
```

If several classes live in one file, which one names the file? Some people
assume it's whichever class contains `main` — if `main` is inside `B`, save
as `B.java`.

**That assumption is wrong. The class that contains `main` and the file name
are nowhere related — there is no link at all.** Any name works, even one
that matches none of the declared classes:

```java
// save as A.java   — valid
// save as B.java   — valid
// save as C.java   — valid
// save as D.java   — valid  (even though there is no class D)
```

### 04:51 — At most one class can be public

How many classes can be declared `public`? **At most one** — zero or one,
never more.

- If there **is** a public class, its name **must** match the file name, or
  it's a compile-time error.
- If there is **no** public class, any file name is fine.

### 07:30 — Live compile: proving it

No public class, saved as `D.java`:

```java
class A {
}

class B {
}

class C {
}
```

```text
javac D.java   // compiles fine
```

Now make `B` public, same file name:

```java
class A {
}

public class B {
}

class C {
}
// file: D.java
// javac D.java
// CE: class B is public, should be declared in a file named B.java
```

The compiler is exact about it — verified on current `javac`, the message
is unchanged in decades: `class B is public, should be declared in a file
named B.java`. Rename the file to `B.java` and it compiles.

Make a second class public in that same file:

```java
class A {
}

public class B {
}

public class C {
}
// file: B.java
// javac B.java
// CE: class C is public, should be declared in a file named C.java
```

`B` public with file `B.java` is no violation — the problem is `C` also
public while the file is still `B.java`. **More than one public class in a
file is always a compile error.**

### 11:17 — The three cases, boarded

> *A Java program can contain any number of classes but at most one class can
> be declared as public. If there is a public class then name of the program
> and name of the public class must be matched, otherwise we will get
> compile-time error.*

| Case | Rule | Result |
|---|---|---|
| No public class | any file name | always valid |
| One public class (say `B`) | file name must be `B.java` | any other name → CE |
| Two public classes (`B` and `C`) in one file | impossible to satisfy both | always CE, regardless of file name |

---

## 19:26 — Multiple mains: the class name still isn't tied to `main`

Some people still believe the class with `main` decides the file name. Sir
kills the idea with a second example:

```java
class A {
    public static void main(String[] args) {
        System.out.println("A class main");
    }
}

class B {
    public static void main(String[] args) {
        System.out.println("B class main");
    }
}

class C {
    public static void main(String[] args) {
        System.out.println("C class main");
    }
}

class D {
}
```

`A`, `B`, and `C` each have their own `main`; `D` has none. There is no public
class, so the file name is free — saved as `D.java`.

### 21:50 — `javac` compiles a program; `java` runs a class

Compiling generates **one `.class` file per class declared**, regardless of
the source file's name:

```text
javac D.java
// generates: A.class  B.class  C.class  D.class
```

There is no `Durga.class` invented from the source file's name — `.class`
files are named after the classes present in the program, never after the
program itself.

**The `javac` argument is a file name (the program). The `java` argument is a
class name.** You compile a Java *source file*; you run a Java *class*.

```text
java A     // A class main
java B     // B class main
java C     // C class main
```

Whichever class you name to `java`, **that class's `main`** runs. `D` has no
`main`:

```text
java D
```

And there is no such class file at all:

```text
java Durga
```

Sir runs this on a JDK he sets `PATH` to explicitly, flagging that the exact
wording changes release to release:

> "version to version there is a small change... let me stick to 1.6 version"

On JDK 1.6:

```text
java D
// Exception in thread "main" java.lang.NoSuchMethodError: main

java Durga
// Exception in thread "main" java.lang.NoClassDefFoundError: Durga
```

> ⚠️ **Modern Java — both of these launcher messages changed in Java 7.**
> Sir explicitly calls out that the wording is version-dependent, and it is.
> Compiled and run on current OpenJDK (26) with the exact same four-class
> program:
>
> ```text
> $ java D
> Error: Main method not found in class D, please define the main method as:
>    public static void main(String[] args)
> or a JavaFX application class must extend javafx.application.Application
>
> $ java Durga
> Error: Could not find or load main class Durga
> Caused by: java.lang.ClassNotFoundException: Durga
> ```
>
> Since **Java 7**, the launcher (`java`) catches the missing-`main` and
> missing-class cases itself and prints a friendly diagnostic instead of
> letting the JVM throw a raw `NoSuchMethodError` / `NoClassDefFoundError` up
> through `main`. The underlying reason (no `main` method; no matching
> `.class` on the classpath) is identical — only the message format changed.
> If you see the raw exception-style messages today, you are almost
> certainly reading an old textbook or, like Sir here, deliberately running
> an old JDK.

### 32:13 — Conclusions

Board heading: **conclusions**.

1. Compiling a Java program generates a **separate `.class` file for every
   class** it declares. Four classes here → four class files.
2. You **compile** a Java program (a source file); you **run** a Java
   `.class` file (a class).
3. Executing a class runs *that class's* `main`. If it has none: a runtime
   error, not a compile error.
4. If the named `.class` file doesn't exist at all: a different runtime
   error, again not a compile error.

---

## 37:25 — Why one class per file is best practice

You **can** put many classes in one source file — it is not good practice.
Readability and maintainability suffer.

Sir's story: an application needs **~250 classes**, dumped into three files
arbitrarily:

```text
File1.java  — 150 classes
File2.java  —  75 classes
File3.java  —  25 classes
```

Given `Account a = new Account(); a.getInfo();`, finding where `Account` is
implemented means opening `File1.java`, then `File2.java`, then finally
`File3.java`. Next week it's `Loan` — same search, three files deep, every
time. That is the whole cost: no way to guess which file holds which class.

**Fix: one class per source file, file name matching class name.**

```java
// Account.java
class Account {
}
```

```java
// Loan.java
class Loan {
}
```

```java
// Customer.java
class Customer {
}
```

`Account` lives in `Account.java`, full stop — the same convention the JDK
itself uses (`String` in `String.java`, `Object` in `Object.java`).

> *It is not recommended to declare multiple classes in a single source
> file. It is highly recommended to declare only one class per source file
> and keep the name of the program the same as the class name. The main
> advantage of this approach is that readability and maintainability of the
> code will be improved.*

---

## 45:46 — Why `ArrayList` needs a package name

Sir spends the rest of the video here, without naming the destination up
front.

```java
class Test {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();
    }
}
```

Does this compile? **No:**

```text
javac Test.java
// CE: cannot find symbol
//   symbol:   class ArrayList
//   location: class Test
```

Doubt raised: if the compiler doesn't know `ArrayList`, how did it even
recognise the symbol as a **class**? Maybe it's guessing from `new`. Sir
rules that out by using the identifier three different ways and reading the
error each time:

```java
System.out.println(ArrayList);
// cannot find symbol: variable ArrayList

ArrayList();
// cannot find symbol: method ArrayList()

ArrayList l = new ArrayList();
// cannot find symbol: class ArrayList
```

Verified on current `javac` — the three messages are exactly this specific:
the compiler reports back whichever role (class/variable/method) the token
was used in. **Conclusion: the compiler genuinely does not know `ArrayList`
at all.** It is asking, plainly: you're using a class called `ArrayList` —
where is it?

### 50:40 — Fully qualified name

Sir's analogy: someone on a forum asks "where is SCJP training available?"
The complete, unambiguous answer is a full path — World → Asia → India →
Telangana → Hyderabad → S.R. Nagar → DurgaSoft. Start from the world and no
follow-up question is possible.

That is a **fully qualified name (FQN)**. Tell the compiler the same way:
`java` package → `util` subpackage → `ArrayList` class.

```java
class Test {
    public static void main(String[] args) {
        java.util.ArrayList l = new java.util.ArrayList();
    }
}
// compiles
```

### 55:50 — The cost of writing FQN every time

Second analogy: a classmate named **Veera Subba Prasad Sastri**. Say the
full name in every sentence and the name is all anyone hears. Agree once
that "Sastri" means him, and the conversation becomes readable again.

**Problem with FQN everywhere: it inflates the code and kills readability.**
Type `java.util.ArrayList` a hundred times and you've typed it a hundred
times. The fix is the same contract as the nickname — declare the mapping
once, then use the short form.

### 59:19 — The import statement

Board heading: **import statement**.

```java
import java.util.ArrayList;

class Test {
    public static void main(String[] args) {
        ArrayList l = new ArrayList();   // short name
    }
}
// compiles
```

Write the `import` once; every later use of `ArrayList` in that file means
`java.util.ArrayList`, no FQN required.

> *The problem with usage of fully qualified name every time is it increases
> length of the code and reduces readability... hence import statement acts
> as a typing shortcut.*

> ⚠️ **Modern Java — two ways the source-file rules got more forgiving.**
> Everything above is still exactly how a `.java` file compiled with `javac`
> behaves today (verified above). But since this recording, the *launcher*
> gained two shortcuts that bend the public-class-must-match-filename rule:
>
> - **JEP 330 (Java 11) — single-file source-code launch.** `java Foo.java`
>   compiles the file in memory and runs it in one step, **no separate
>   `javac` needed** — and the file name no longer has to match the public
>   class inside it:
>
>   ```text
>   $ cat scratch.java
>   public class Hello {
>       public static void main(String[] args) {
>           System.out.println("hi");
>       }
>   }
>   $ java scratch.java
>   hi
>   ```
>
>   This only works when launching directly from source (`java Foo.java`,
>   no explicit `javac` step); a compiled `Hello.class` from `javac` still
>   enforces the classic rule.
>
> - **JEP 512 (Java 25) — compact source files.** For a short program you no
>   longer need the `class` wrapper or the full `public static void main`
>   signature at all:
>
>   ```java
>   // compact.java
>   void main() {
>       System.out.println("compact source file, instance main");
>   }
>   ```
>
>   ```text
>   $ java compact.java
>   compact source file, instance main
>   ```
>
> Both are aimed at scripts and beginners' first programs, not at real
> multi-file projects — the OCJP rules in this lecture (one file, compiled
> with `javac`, one public class matching the file name) are still exactly
> what production code and the exam expect.

---

## Exam and interview points

1. **Any number of classes per file, at most one `public`.** Zero public
   classes → any file name. One public class → file name must match it
   exactly. Two or more public classes → always a compile error, no file
   name fixes it.
2. **The class containing `main` has no special relationship to the file
   name.** That belief is the most common wrong assumption on this topic.
3. **`javac` compiles a file; `java` runs a class.** Compiling a 4-class file
   produces 4 `.class` files, named after the classes, never after the
   source file.
4. **Missing `main`, or a missing `.class` file, is a *runtime* error, not a
   compile error.** Historically `NoSuchMethodError`/`NoClassDefFoundError`;
   since Java 7, the friendlier "Main method not found" / "Could not find or
   load main class" — know both wordings, and that only the message changed.
5. **One class per file, file name = class name, is best practice** (not a
   compiler rule for non-public classes) — it's the difference between
   finding `Account` instantly and grepping three files.
6. **The compiler has zero built-in knowledge of `ArrayList` or any other
   library class.** An unqualified name that isn't imported fails with
   `cannot find symbol`, exactly like a typo in your own class name would.
7. **Import is a typing shortcut, nothing more.** `java.util.ArrayList` and
   `ArrayList` (with the import) compile to the identical class reference —
   import buys readability, not new capability. Fully qualified name always
   works as a substitute for an import, in a single spot.
8. **Modern nuance worth naming in an interview:** `java Foo.java` (JEP 330,
   Java 11) can skip the `javac` step and drops the filename-matches-public-
   class rule for that launch mode; JEP 512 (Java 25) lets a short program
   skip the class wrapper and static `main` signature entirely. Neither
   changes how a normal, `javac`-compiled multi-file project behaves.

---

**Next:** Video 031 — import and static import
