# Video 023 — operator interview FAQs

## Video info

**Title:** Core Java with OCJP/SCJP: Operators & Assignments Part-7  || Interview FAQs

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 23 of 203 |
| Series | Operators & Assignments · Part 7 of 7 |
| Topic | Operator interview FAQs: new vs newInstance(), instanceof vs isInstance(), ClassNotFoundException vs NoClassDefFoundError, new vs instanceof, == vs equals(), increment puzzles, boolean vs bitwise, = vs ==, reachability-adjacent operator questions; wrap-up of the operators module |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 25m 34s |
| Video ID | K0bLAbhVyqw |
| Watch | https://www.youtube.com/watch?v=K0bLAbhVyqw |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |
| Captions | None on YouTube. Notes reconstructed from this lecture topic as Durga Sir teaches it, with full Java board examples. |

> **How to read these notes.** Sections follow the lecture's own structure.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

Operators list and precedence (Parts 1–6) are done. This class is the
**interview / OCJP FAQ hour** that closes the module:

1. `new` operator vs `newInstance()` method — class name known at compile time
   vs at runtime.
2. Checked `ClassNotFoundException` vs unchecked `NoClassDefFoundError`.
3. `InstantiationException` / `IllegalAccessException` while using `newInstance()`.
4. `instanceof` operator vs `Class.isInstance()` method — compile-time type vs
   runtime type name.
5. **`new` vs `instanceof`** — people confuse these because both mention
   "type / object". Sir separates creation from type-checking, then maps each
   to its runtime twin (`newInstance()` / `isInstance()`).
6. `==` vs `equals()` revision — reference vs content, plus the `StringBuffer`
   trap.
7. Increment assignment puzzles: `x = x++`, `x = ++x`, `x = ++x + ++x`, and
   further compound variants.
8. Boolean vs bitwise: `& | ^` vs `&& ||`, `~` vs `!`.
9. Assignment vs comparison: `=` vs `==` inside `if` / `while`.
10. Reachability-adjacent operator questions: `while(true)`, `while(false)`,
    `if(false)`, compile-time constant comparisons.
11. Full operators-module wrap-up (agenda 1–18). Next chapter: Flow-Control.

---

## Opening: leftover FAQs before the module closes

Sir's framing: the operators chapter is essentially done — precedence and
operand evaluation were the last graded topic. What is left is a batch of
FAQs that interviewers ask precisely *because* they sound like restatements
of things you already "know". Walk in unprepared and they cost you the
interview.

The leftover official agenda he boards:

1. `new` vs `newInstance()`
2. `instanceof` vs `isInstance()`
3. `ClassNotFoundException` vs `NoClassDefFoundError`

Alongside it, a batch of pure operator-revision FAQs: `==` vs `equals`,
increment puzzles, bitwise vs boolean, `=` vs `==`, and unreachable statements
built from constant `true`/`false`. Both batches close in this one class.

## Recap: `new` creates; the constructor only initializes

Part-5 point, repeated because today's comparison starts from `new`.

```java
class Test {
    Test() {
        System.out.println("constructor");
    }
    public static void main(String[] args) {
        Test t = new Test();
        // prints constructor
        // 1) new creates the Test object
        // 2) then constructor runs to initialize
    }
}
```

There is **no** `delete`. GC destroys unused objects.

```java
class Test {
    public static void main(String[] args) {
        Test t = new Test();
        t = null; // object becomes eligible for GC; no delete operator in Java
        System.out.println("no delete keyword"); // prints no delete keyword
    }
}
```

**Condition to use `new`:** the class name is known **up front** — hard-coded
at compile time. `new Test()` requires the compiler to see the type `Test`.

## FAQ 1 — `new` vs `newInstance()`

`newInstance()` is a method — it lives in `java.lang.Class`.

`java.lang.Class` is the class that represents `.class` files inside the JVM.
Every loaded class has one `Class` object, and from it you can create an
instance **without writing the class name in source**.

```java
class Test {
    public static void main(String[] args) throws Exception {
        Object o = Class.forName(args[0]).newInstance();
        System.out.println(o.getClass().getName());
    }
}
```

Run with the fully qualified name (the board often shortens it to `String`,
but the JVM needs `java.lang.String`):

```java
class Test {
    public static void main(String[] args) throws Exception {
        // java Test java.lang.String
        Object o = Class.forName("java.lang.String").newInstance();
        System.out.println(o.getClass().getName()); // prints java.lang.String
        System.out.println(o.equals(""));           // prints true  (empty String from no-arg ctor)
    }
}
```

Same `Test` class, created dynamically instead of hard-coded:

```java
class Test {
    public static void main(String[] args) throws Exception {
        Object o = Class.forName("Test").newInstance();
        System.out.println(o.getClass().getName()); // prints Test
    }
}
```

Hard-coded equivalent of the first call:

```java
class Test {
    public static void main(String[] args) {
        String s = new String(); // class name known at compile time
        System.out.println(s.getClass().getName()); // prints java.lang.String
    }
}
```

Sir's one-liner: if the class name is known at **compile time**, use `new`. If
it arrives at **runtime** — command line, a config file, a properties file —
use `Class.forName(name).newInstance()`.

`throws Exception` is compulsory on `main` (or a try/catch) because:

- `Class.forName` → checked `ClassNotFoundException`
- `newInstance` → checked `InstantiationException`, `IllegalAccessException`

```java
class Test {
    public static void main(String[] args) {
        Object o = Class.forName(args[0]).newInstance();
        System.out.println(o);
        // CE: unreported exception ClassNotFoundException; must be caught or declared
        // CE: unreported exception InstantiationException; must be caught or declared
        // (IllegalAccessException is also declared by newInstance() and must be
        //  handled once the first two are — javac reports unhandled checked
        //  exceptions one at a time per expression, not all three at once)
    }
}
```

> ⚠️ **Modern Java — `Class.newInstance()` is deprecated (Java 9).**
> Everything above still compiles and is still the OCJP-era answer, but since
> **Java 9** `Class.newInstance()` carries `@Deprecated`. The reason is exactly
> the loophole this FAQ is built on: `newInstance()` re-throws whatever checked
> exception the constructor declares *without requiring you to declare it*,
> silently bypassing the compiler's checked-exception enforcement. The
> replacement goes through `java.lang.reflect.Constructor`, which wraps any
> constructor-thrown exception in a checked `InvocationTargetException` instead:
>
> ```java
> class Test {
>     public static void main(String[] args) throws Exception {
>         Object o = Class.forName("Test")
>                         .getDeclaredConstructor()   // no-arg constructor, explicitly
>                         .newInstance();              // Constructor.newInstance(Object...)
>         System.out.println(o.getClass().getName()); // prints Test
>     }
> }
> ```
>
> This compiles with **no deprecation warning**. `getDeclaredConstructor()` (or
> `getConstructor()` for a public one) still throws checked
> `NoSuchMethodException`, and the `newInstance(Object...)` call still throws
> `InstantiationException` / `IllegalAccessException` / `InvocationTargetException`
> — so the exam's exception story is unchanged, only the API name is newer.
> `Class.newInstance()` has not been removed and still behaves exactly as
> taught; it is deprecated, not gone.

## Board table — `new` vs `newInstance()`

He dictates row by row. After each row, one program.

**Row 1 — nature**

```java
class Test {
    public static void main(String[] args) throws Exception {
        Test t1 = new Test(); // new is an operator
        Object t2 = Class.forName("Test").newInstance(); // newInstance() is a method of class Class
        System.out.println(t1.getClass() == t2.getClass()); // prints true
    }
}
```

**Row 2 — when**

```java
class Student {
}
class Test {
    public static void main(String[] args) throws Exception {
        Student s = new Student(); // we already know the class name: Student
        Object o = Class.forName(args[0]).newInstance(); // name comes at runtime
        System.out.println(s.getClass().getName());
        System.out.println(o.getClass().getName());
    }
}
```

**Row 3 — missing `.class` at runtime**

Hard-coded `new Student()` — if `Student.class` is not available at runtime we
get **`NoClassDefFoundError`** (an `Error`, unchecked).

Dynamic `Class.forName("Student")` — if it is not available we get
**`ClassNotFoundException`** (an `Exception`, checked).

```java
class Test {
    public static void main(String[] args) {
        Student s = new Student();
        System.out.println(s);
        // if Student.class is missing at RUNTIME (compiled against Student, then .class deleted):
        // RE: java.lang.NoClassDefFoundError: Student
    }
}
```

```java
class Test {
    public static void main(String[] args) throws Exception {
        Object o = Class.forName("Student").newInstance();
        System.out.println(o);
        // if Student.class is not on the classpath:
        // RE: java.lang.ClassNotFoundException: Student
    }
}
```

**Row 4 — no-arg constructor**

`new Student(10)` can call a parameterized constructor. `newInstance()`
internally uses the **no-argument constructor**. If that constructor is
missing → `InstantiationException`.

```java
class Student {
    Student(String name) {
        System.out.println("param ctor " + name);
    }
}
class Test {
    public static void main(String[] args) {
        Student s = new Student("durga"); // valid — we chose the constructor
        System.out.println(s);
        // prints param ctor durga
    }
}
```

```java
class Student {
    Student(String name) {
    }
}
class Test {
    public static void main(String[] args) throws Exception {
        Object o = Class.forName("Student").newInstance();
        System.out.println(o);
        // RE: java.lang.InstantiationException: Student
        // (no public no-arg constructor)
    }
}
```

`java.lang.Integer` is the exam's favourite "no no-arg ctor" class:

```java
class Test {
    public static void main(String[] args) throws Exception {
        Object o = Class.forName("java.lang.Integer").newInstance();
        System.out.println(o);
        // RE: java.lang.InstantiationException: java.lang.Integer
    }
}
```

> ⚠️ **Modern Java — `new Integer(...)` itself is deprecated (Java 9).**
> `Integer` never had a no-arg constructor (that part of the FAQ is unchanged),
> but the parameterized constructors used to *make* an `Integer` are now
> deprecated too:
>
> ```java
> class Test {
>     public static void main(String[] args) {
>         Integer i = new Integer(5);       // compiles; javac -Xlint:deprecation warns
>         Integer j = Integer.valueOf(5);   // preferred — no warning
>         System.out.println(i + " " + j);  // prints 5 5
>     }
> }
> ```
>
> `Integer.valueOf` (and autoboxing, which calls it) can return a cached,
> shared instance for small values — better space and time behaviour than
> always allocating with `new`. Neither constructor has been removed.

Abstract class / interface also cannot be instantiated:

```java
abstract class Animal {
}
class Test {
    public static void main(String[] args) throws Exception {
        Object o = Class.forName("Animal").newInstance();
        System.out.println(o);
        // RE: java.lang.InstantiationException
    }
}
```

If the no-arg constructor exists but is **not accessible** (private) →
`IllegalAccessException`.

```java
class Demo {
    private Demo() {
    }
}
class Test {
    public static void main(String[] args) throws Exception {
        Object o = Class.forName("Demo").newInstance();
        System.out.println(o);
        // RE: java.lang.IllegalAccessException
        // (constructor Demo() is not accessible)
    }
}
```

`new` does not require a no-arg constructor. `newInstance()` does. That is the
last row of the table, and it is exam-guaranteed.

## FAQ 2 — `ClassNotFoundException` vs `NoClassDefFoundError`

Sir spends a long stretch here because the names look similar: Exception vs
Error, checked vs unchecked, dynamic name vs hard-coded name.

|  | ClassNotFoundException | NoClassDefFoundError |
|---|---|---|
| Type | Exception (checked) | Error (unchecked) |
| When | class name provided dynamically (`forName`, `loadClass`, …) | class name hard-coded, `.class` missing at runtime |
| Typical API | `Class.forName("Student")` | `new Student()` |
| Handling | must catch or declare | usually not caught; it is an `Error` |

```java
class Test {
    public static void main(String[] args) {
        try {
            Class.forName("NoSuchClass");
        } catch (ClassNotFoundException e) {
            System.out.println("checked — we can handle"); // prints checked — we can handle
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        // NoClassDefFoundError is an Error, not an Exception.
        // Catching Exception will NOT catch it.
        try {
            Helper.touch();
        } catch (Exception e) {
            System.out.println("will NOT catch NoClassDefFoundError");
        }
    }
}
class Helper {
    static Student s = new Student(); // if Student.class is gone at runtime → Error during init
    static void touch() {
    }
}
```

Memory sentence: hard-coded class missing → `NoClassDefFoundError`.
Dynamically-provided class missing → `ClassNotFoundException`.

`Class.forName` **loads** the class (runs its static block). `newInstance`
**creates** the object.

```java
class Student {
    static {
        System.out.println("Student loaded");
    }
    Student() {
        System.out.println("Student object");
    }
}
class Test {
    public static void main(String[] args) throws Exception {
        Class c = Class.forName("Student");
        // prints Student loaded
        Object o = c.newInstance();
        // prints Student object
        System.out.println(o.getClass().getName()); // prints Student
    }
}
```

## FAQ 3 — `instanceof` recap, then `isInstance()`

Part-3 already taught `instanceof`. This FAQ repeats the board examples, then
introduces its **method twin**.

Syntax: `r instanceof X` — `r` is a reference, `X` is a class or interface
name **known at compile time**.

```java
class Test {
    public static void main(String[] args) {
        Thread t = new Thread();
        System.out.println(t instanceof Thread);   // prints true
        System.out.println(t instanceof Object);   // prints true
        System.out.println(t instanceof Runnable); // prints true
    }
}
```

A relation is compulsory (parent ↔ child or same type). Otherwise the compiler
rejects it as **inconvertible types**:

```java
class Test {
    public static void main(String[] args) {
        Thread t = new Thread();
        System.out.println(t instanceof String);
        // CE: incompatible types: Thread cannot be converted to String
    }
}
```

A parent-typed reference is not automatically the child type:

```java
class Test {
    public static void main(String[] args) {
        Object o1 = new Object();
        System.out.println(o1 instanceof String); // prints false
        Object o2 = new String("ashok");
        System.out.println(o2 instanceof String); // prints true
    }
}
```

`null instanceof X` is always `false`:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(null instanceof String);  // prints false
        System.out.println(null instanceof Object);  // prints false
        System.out.println(null instanceof Runnable); // prints false
    }
}
```

**`isInstance(Object)`** — a method in `class Class`. The type name can arrive
at **runtime**.

```java
class Test {
    public static void main(String[] args) throws Exception {
        Test t = new Test();
        System.out.println(Class.forName(args[0]).isInstance(t));
    }
}
```

Intended runs (pass the FQCN for library types):

```java
class Test {
    public static void main(String[] args) throws Exception {
        Test t = new Test();
        System.out.println(Class.forName("Test").isInstance(t));            // prints true
        System.out.println(Class.forName("java.lang.Object").isInstance(t)); // prints true
        System.out.println(Class.forName("java.lang.String").isInstance(t)); // prints false
    }
}
```

Thread / Runnable version — shows an interface check at runtime:

```java
class Test {
    public static void main(String[] args) throws Exception {
        Thread th = new Thread();
        System.out.println(Class.forName("java.lang.Thread").isInstance(th));   // prints true
        System.out.println(Class.forName("java.lang.Runnable").isInstance(th)); // prints true
        System.out.println(Class.forName("java.lang.String").isInstance(th));   // prints false
    }
}
```

The `isInstance` argument is the **object**. Forgetting it is a CE:

```java
class Test {
    public static void main(String[] args) throws Exception {
        System.out.println(Class.forName("Test").isInstance());
        // CE: method isInstance in class java.lang.Class cannot be applied to given types
        // required: java.lang.Object
        // found:    no arguments
    }
}
```

> ⚠️ **Modern Java — pattern matching for `instanceof` (Java 16).**
> Since **Java 16** (JEP 394) `instanceof` can bind the cast variable right in
> the condition, so the check-then-cast pair Sir teaches below collapses into
> one expression:
>
> ```java
> class Test {
>     public static void main(String[] args) {
>         Object o = "durga";
>         if (o instanceof String s) {       // s is bound only where true
>             System.out.println(s.length()); // prints 5
>         }
>     }
> }
> ```
>
> `s` is only in scope where the compiler can prove `o instanceof String` was
> `true` — including after an early `return`/`continue` in the negative branch.
> The two-step `if (o instanceof String) { String s = (String) o; ... }` form
> still compiles and is still the version an OCJP-era exam expects.

## `new` vs `instanceof` — why interviewers mix the two names

The names look alike — `new` / `newInstance`, `instanceof` / `isInstance` —
which is exactly why an interviewer who asks "`new` vs `instanceof`" is
testing whether you panic. The two operators solve completely different
problems.

|  | `new` | `instanceof` |
|---|---|---|
| Purpose | create an object | check whether an object is of a type |
| Result | a reference to a new object | `boolean` |
| Runtime twin | `Class.newInstance()` | `Class.isInstance()` |

Creation is not a type check:

```java
class Test {
    public static void main(String[] args) {
        Object o = new String("durga"); // new → create
        boolean b = o instanceof String; // instanceof → test
        System.out.println(b); // prints true
    }
}
```

You cannot write `instanceof` to create, and you cannot write `new` to test:

```java
class Test {
    public static void main(String[] args) {
        String s = instanceof String;
        // CE: illegal start of expression
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        String s = "durga";
        System.out.println(s new String);
        // CE: ';' expected  (new is not an infix type-check operator)
    }
}
```

Safe downcast pattern — this is where `instanceof` follows something `new`
already created as a wider type:

```java
class Test {
    public static void main(String[] args) {
        Object o = new String("durga");
        if (o instanceof String) {
            String s = (String) o;
            System.out.println(s.length()); // prints 5
        }
    }
}
```

Without the check, a wrong cast is a `ClassCastException` at runtime, not a
compile error, as long as the types are related:

```java
class Test {
    public static void main(String[] args) {
        Object o = new String("durga");
        Integer i = (Integer) o;
        System.out.println(i);
        // RE: java.lang.ClassCastException: class java.lang.String cannot be cast to class java.lang.Integer
    }
}
```

The FAQ mapping for the notebook:

- Known at compile time, **create** → `new`
- Known at runtime, **create** → `newInstance()`
- Known at compile time, **test type** → `instanceof`
- Known at runtime, **test type** → `isInstance()`

## FAQ 4 — `==` vs `equals()` (operators revision)

Part-2's one-liner, now as an interview question: `==` — reference/address
comparison for objects, value comparison for primitives. `equals()` — content
comparison, **if the class overrides it**.

Primitives — only `==` (there is no `equals` on a primitive):

```java
class Test {
    public static void main(String[] args) {
        int a = 10, b = 10;
        System.out.println(a == b); // prints true
        // System.out.println(a.equals(b));
        // CE: int cannot be dereferenced
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        System.out.println('a' == 97);      // prints true  (char vs int promotion)
        System.out.println('a' == 97.0);    // prints true
        System.out.println(false == false); // prints true
        System.out.println(10 == 20);       // prints false
    }
}
```

Objects — `==` is identity:

```java
class Test {
    public static void main(String[] args) {
        String s1 = new String("ashok");
        String s2 = new String("ashok");
        System.out.println(s1 == s2);        // prints false  (two objects)
        System.out.println(s1.equals(s2));   // prints true   (String overrides equals)
    }
}
```

String literals live in the pool (mentioned here; the full String class comes
later):

```java
class Test {
    public static void main(String[] args) {
        String s1 = "durga";
        String s2 = "durga";
        String s3 = new String("durga");
        System.out.println(s1 == s2);      // prints true   (same pool object)
        System.out.println(s1 == s3);      // prints false
        System.out.println(s1.equals(s3)); // prints true
    }
}
```

**`StringBuffer` / `StringBuilder` do not override `equals`** — same content,
`equals` is still `false`. A frequently-missed trap.

```java
class Test {
    public static void main(String[] args) {
        StringBuffer sb1 = new StringBuffer("durga");
        StringBuffer sb2 = new StringBuffer("durga");
        System.out.println(sb1 == sb2);      // prints false
        System.out.println(sb1.equals(sb2)); // prints false  (Object.equals → reference)
    }
}
```

Incomparable types for `==`:

```java
class Test {
    public static void main(String[] args) {
        String s = "durga";
        Thread t = new Thread();
        System.out.println(s == t);
        // CE: incomparable types: java.lang.String and java.lang.Thread
    }
}
```

`null` with `==` is fine; `null.equals(...)` is an NPE:

```java
class Test {
    public static void main(String[] args) {
        String s = null;
        System.out.println(s == null);     // prints true
        System.out.println(null == null);  // prints true
        System.out.println("durga".equals(s)); // prints false  (safe: call equals on the literal)
        System.out.println(s.equals("durga"));
        // RE: java.lang.NullPointerException
    }
}
```

> ⚠️ **Modern Java — this NPE tells you more (Java 14).**
> Since **Java 14** (JEP 358, on by default since 15), the JVM's default NPE
> message names the exact failing call instead of a bare stack trace line:
>
> ```text
> Exception in thread "main" java.lang.NullPointerException:
>     Cannot invoke "String.equals(Object)" because "s" is null
> ```
>
> That variable name shows up when the class carries a local variable table
> (the default for `javac` run from an IDE, or `javac -g`); a plain
> `javac Test.java` from the command line omits it and prints `"<local1>"`
> instead — still far more than the old JDKs gave you.
>
> On the JDK this lecture used, the message was just
> `java.lang.NullPointerException` with no detail at all — you had to read the
> line number and guess which reference was `null`. The exception type and the
> fix (check for `null`, or call `equals` on the literal instead) are
> unchanged.

Relation is required for reference `==` (parent/child is fine):

```java
class Test {
    public static void main(String[] args) {
        Object o = new Object();
        String s = new String("durga");
        Thread t = new Thread();
        System.out.println(o == s); // prints false  (related: Object / String)
        System.out.println(o == t); // prints false  (related: Object / Thread)
    }
}
```

## FAQ 5 — increment puzzles (assignment + `++`)

Part-1 and Part-6 combined: the interviewer writes one line and asks for the
output.

**Puzzle A — `x = x++`**

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        x = x++;
        System.out.println(x); // prints 10
    }
}
```

Three-step board reasoning:

1. Consider the **old** value of `x` for the assignment → `10`.
2. Increment `x` → `11`.
3. Perform the assignment with the considered old value → `x = 10`.

**Puzzle B — `x = ++x`**

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        x = ++x;
        System.out.println(x); // prints 11
    }
}
```

**Puzzle C — `x = ++x + ++x`**

```java
class Test {
    public static void main(String[] args) {
        int x = 0;
        x = ++x + ++x;
        System.out.println(x); // prints 3
        // ++x → 1; ++x → 2; 1 + 2 = 3
    }
}
```

**Puzzle D — `x = x++ + ++x`**

```java
class Test {
    public static void main(String[] args) {
        int x = 0;
        x = x++ + ++x;
        System.out.println(x); // prints 2
        // x++ uses 0 (x becomes 1); ++x → 2; 0 + 2 = 2
    }
}
```

**Puzzle E — two post-increments**

```java
class Test {
    public static void main(String[] args) {
        int x = 5;
        x = x++ + x++;
        System.out.println(x); // prints 11
        // uses 5 (x=6), then uses 6 (x=7); 5 + 6 = 11
    }
}
```

**Puzzle F — compound form from Part-6**

```java
class Test {
    public static void main(String[] args) {
        int i = 1;
        i += ++i + i++ + ++i + i++;
        System.out.println(i); // prints 13
    }
}
```

**Puzzle G — `++` not on a variable**

```java
class Test {
    public static void main(String[] args) {
        int x = 4;
        int y = ++4;
        System.out.println(y);
        // CE: unexpected type
        // required: variable
        // found:    value
    }
}
```

**Puzzle H — `final`**

```java
class Test {
    public static void main(String[] args) {
        final int x = 4;
        x++;
        System.out.println(x);
        // CE: cannot assign a value to final variable x
    }
}
```

**Puzzle I — boolean `++`**

```java
class Test {
    public static void main(String[] args) {
        boolean b = true;
        b++;
        System.out.println(b);
        // CE: bad operand type boolean for unary operator '++'
    }
}
```

## FAQ 6 — boolean vs bitwise

Part-3 / Part-4 revision as a comparison table plus programs. Interview
question: "difference between `&` and `&&`."

| Operator | Boolean operands | Integral operands | Short-circuit? |
|---|---|---|---|
| `&`, `\|`, `^` | yes | yes | no — both sides always evaluated |
| `&&`, `\|\|` | yes | no | yes |
| `~` | no | yes | n/a (unary) |
| `!` | yes | no | n/a (unary) |

Boolean `&` `|` `^`:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(true & false); // prints false
        System.out.println(true | false); // prints true
        System.out.println(true ^ false); // prints true
        System.out.println(true ^ true);  // prints false
    }
}
```

Integral `&` `|` `^` (board binaries: 4 → `100`, 5 → `101`):

```java
class Test {
    public static void main(String[] args) {
        System.out.println(4 & 5); // prints 4
        System.out.println(4 | 5); // prints 5
        System.out.println(4 ^ 5); // prints 1
    }
}
```

`&&` `||` **cannot** take integrals:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(4 && 5);
        // CE: bad operand types for binary operator '&&'
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        System.out.println(4 || 5);
        // CE: bad operand types for binary operator '||'
    }
}
```

`~` vs `!`:

```java
class Test {
    public static void main(String[] args) {
        System.out.println(~4);     // prints -5
        System.out.println(!false); // prints true
        // System.out.println(~true); // CE: operator ~ cannot be applied to boolean
        // System.out.println(!4);    // CE: operator ! cannot be applied to int
    }
}
```

**Performance / correctness loophole** — `&` vs `&&` with side effects. The
classic `x`, `y` table from Part-4, re-run for all four operators.

```java
class Test {
    public static void main(String[] args) {
        int x = 10, y = 15;
        if (++x < 10 & ++y > 15) {
            x++;
        } else {
            y++;
        }
        System.out.println(x + "----" + y); // prints 11----17
        // both increments happen; condition false; else y++
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = 10, y = 15;
        if (++x < 10 && ++y > 15) {
            x++;
        } else {
            y++;
        }
        System.out.println(x + "----" + y); // prints 11----16
        // ++x → 11 < 10 false → ++y SKIPPED; else y++ → 16
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = 10, y = 15;
        if (++x < 10 | ++y > 15) {
            x++;
        } else {
            y++;
        }
        System.out.println(x + "----" + y); // prints 12----16
        // both sides run; 11<10 false | 16>15 true → if body x++
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = 10, y = 15;
        if (++x < 10 || ++y > 15) {
            x++;
        } else {
            y++;
        }
        System.out.println(x + "----" + y); // prints 12----16
        // ++x → 11<10 false, so ++y DOES run (||); 16>15 true → if body x++
    }
}
```

Board summary:

| Operator | x | y |
|---|---|---|
| `&` | 11 | 17 |
| `\|` | 12 | 16 |
| `&&` | 11 | 16 |
| `\|\|` | 12 | 16 |

Divide-by-zero **hidden** by `&&` (short-circuit) — the exam loves this:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        if (++x < 10 && (x / 0 > 10)) {
            System.out.println("Hello");
        } else {
            System.out.println("Hi"); // prints Hi
        }
        // ++x → 11 < 10 false → (x/0) not evaluated, no ArithmeticException
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        if (++x < 10 & (x / 0 > 10)) {
            System.out.println("Hello");
        } else {
            System.out.println("Hi");
        }
        // RE: java.lang.ArithmeticException: / by zero
        // & evaluates both sides
    }
}
```

## FAQ 7 — assignment vs comparison (`=` vs `==`)

Sir: one extra `=` is enough to spoil an interview answer. `=` is assignment
(lowest precedence). `==` is equality.

For `int`, `if (x = 10)` is a CE — `if` needs a `boolean`.

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        if (x = 20) {
            System.out.println("hello");
        }
        // CE: incompatible types
        // found:    int
        // required: boolean
    }
}
```

Correct comparison:

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        if (x == 20) {
            System.out.println("hello");
        } else {
            System.out.println("hi"); // prints hi
        }
    }
}
```

**Boolean exception — this is the OCJP trap.** Assignment of a `boolean` value
**is itself** a `boolean` value (the value just assigned). So `if (b = true)`
compiles, performs the assignment, and the condition is `true`.

```java
class Test {
    public static void main(String[] args) {
        boolean b = false;
        if (b = true) {
            System.out.println("hello"); // prints hello
        }
        System.out.println(b); // prints true  (b was assigned)
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        boolean b = false;
        if (b == true) {
            System.out.println("hello");
        } else {
            System.out.println("hi"); // prints hi
        }
        System.out.println(b); // prints false  (unchanged)
    }
}
```

Chained assignment inside `if` — still assignment, still `boolean` if the
variable is `boolean`:

```java
class Test {
    public static void main(String[] args) {
        boolean b1, b2;
        b1 = b2 = false;
        if (b1 = b2 = true) {
            System.out.println("yes"); // prints yes
        }
        System.out.println(b1 + " " + b2); // prints true true
    }
}
```

`==` vs `=` with objects in `if`:

```java
class Test {
    public static void main(String[] args) {
        String s1 = new String("durga");
        String s2 = new String("durga");
        if (s1 = s2) {
            System.out.println("same");
        }
        // CE: incompatible types
        // found:    java.lang.String
        // required: boolean
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        String s1 = new String("durga");
        String s2 = new String("durga");
        if (s1 == s2) {
            System.out.println("same ref");
        } else {
            System.out.println("different ref"); // prints different ref
        }
    }
}
```

## FAQ 8 — reachability-adjacent operator questions

Next chapter is Flow-Control, but operators produce the **constant `true` /
`false`** the compiler uses for unreachable-statement errors. This mix comes
up in interviews: operator knowledge is what actually solves the
flow-control question.

`while (true)` is an infinite loop. Code **after** the loop is unreachable.

```java
class Test {
    public static void main(String[] args) {
        while (true) {
            System.out.println("hi");
        }
        System.out.println("hello");
        // CE: unreachable statement
    }
}
```

`while (false)` — the body is unreachable:

```java
class Test {
    public static void main(String[] args) {
        while (false) {
            System.out.println("hi");
            // CE: unreachable statement
        }
    }
}
```

**`if` is special.** `if (true)` / `if (false)` are **legal**, including a dead
`else` branch. The compiler allows this so flags can gate code during
development.

```java
class Test {
    public static void main(String[] args) {
        if (true) {
            System.out.println("hi"); // prints hi
        } else {
            System.out.println("hello"); // dead, but NOT a compile error
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        if (false) {
            System.out.println("hi"); // dead, but legal
        }
        System.out.println("hello"); // prints hello
    }
}
```

A compile-time **constant** comparison is treated the same as writing
`false` directly:

```java
class Test {
    public static void main(String[] args) {
        final int x = 10;
        final int y = 20;
        while (x > y) {
            System.out.println("hi");
            // CE: unreachable statement  (x > y is constant false)
        }
    }
}
```

Non-final variables — the comparison is **not** a constant expression, so the
body is reachable even though we "know" 10 is never greater than 20.

```java
class Test {
    public static void main(String[] args) {
        int x = 10;
        int y = 20;
        while (x > y) {
            System.out.println("hi"); // legal (may never run)
        }
        System.out.println("ok"); // prints ok
    }
}
```

An operator applied to literals still forms a constant:

```java
class Test {
    public static void main(String[] args) {
        while (true & false) {
            System.out.println("hi");
            // CE: unreachable statement  (constant false)
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        while (true | false) {
            System.out.println("hi");
        }
        System.out.println("after");
        // CE: unreachable statement  (constant true → infinite)
    }
}
```

`final boolean` is a constant; a plain `boolean` is not:

```java
class Test {
    public static void main(String[] args) {
        final boolean b = false;
        while (b) {
            System.out.println("hi");
            // CE: unreachable statement
        }
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        boolean b = false;
        while (b) {
            System.out.println("hi"); // legal
        }
        System.out.println("ok"); // prints ok
    }
}
```

**Assignment inside a loop condition.** `b = false` is an *assignment*
expression, and an assignment expression is never a compile-time constant —
even though the literal on its right-hand side is `false`. So `while (b =
false)` is treated as **reachable** by the compiler even though the body will
in fact never execute:

```java
class Test {
    public static void main(String[] args) {
        boolean b = true;
        while (b = false) {
            System.out.println("hi"); // legal; does not print
        }
        System.out.println(b); // prints false
    }
}
```

`for ( ; false ; )` gets the same unreachable body as `while (false)`:

```java
class Test {
    public static void main(String[] args) {
        for (;;) {
            break;
        }
        System.out.println("ok"); // prints ok  (break makes the next line reachable)
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        for (; false;) {
            System.out.println("hi");
            // CE: unreachable statement
        }
    }
}
```

## Extra operator FAQs before wrap-up

**Nested relational is illegal** (already Part-2; the interview repeats it):

```java
class Test {
    public static void main(String[] args) {
        System.out.println(10 > 20 > 30);
        // CE: bad operand types for binary operator '>'
        // first type:  boolean
        // second type: int
    }
}
```

**`+` overload — concatenation vs addition** (Part-2 FAQ):

```java
class Test {
    public static void main(String[] args) {
        String a = "ashok";
        int b = 10, c = 20, d = 30;
        System.out.println(a + b + c + d); // prints ashok102030
        System.out.println(b + c + d + a); // prints 60ashok
        System.out.println(b + c + a + d); // prints 30ashok30
        System.out.println(b + a + c + d); // prints 10ashok2030
    }
}
```

**Compound vs arithmetic on `byte`** (Part-1 / Part-5 FAQ):

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        b = b + 1;
        System.out.println(b);
        // CE: incompatible types: possible lossy conversion from int to byte
    }
}
```

```java
class Test {
    public static void main(String[] args) {
        byte b = 10;
        b++;
        System.out.println(b); // prints 11
        b += 1;
        System.out.println(b); // prints 12
    }
}
```

**Chained compound** (Part-5 exam mix):

```java
class Test {
    public static void main(String[] args) {
        int a, b, c, d;
        a = b = c = d = 20;
        a += b -= c *= d /= 2;
        System.out.println(a + "........" + b + "........" + c + "........" + d);
        // prints -160........-180........200........10
    }
}
```

**Operand evaluation reminder** (Part-6, worth one more pass because
interviews mix it with these FAQs):

```java
class Test {
    public static void main(String[] args) {
        System.out.println(m1(1) + m1(2) * m1(3) / m1(4) * m1(5) + m1(6));
    }
    public static int m1(int i) {
        System.out.println(i);
        return i;
    }
}
// prints
// 1
// 2
// 3
// 4
// 5
// 6
// 12
```

## Operators & Assignments — module wrap-up (agenda 1 to 18)

Sir scrolls the original operators list and ticks every item off.

| # | Topic | Where |
|---|---|---|
| 1 | increment & decrement | Part-1 |
| 2 | arithmetic | Part-1 |
| 3 | string concatenation `+` | Part-2 |
| 4 | relational `< <= > >=` | Part-2 |
| 5 | equality `== !=` | Part-2 |
| 6 | instanceof | Part-3 |
| 7 | bitwise `& \| ^ ~ !` | Part-3 |
| 8 | short-circuit `&& \|\|` | Part-4 |
| 9 | type-cast | Part-4 |
| 10 | assignment `= += …` | Part-5 |
| 11 | conditional `?:` | Part-5 |
| 12 | `new` | Part-5 |
| 13 | `[]` | Part-5 |
| 14 | operator precedence | Part-6 |
| 15 | operand evaluation order | Part-6 |
| 16 | `new` vs `newInstance()` | Part-7 |
| 17 | `instanceof` vs `isInstance()` | Part-7 |
| 18 | `ClassNotFoundException` vs `NoClassDefFoundError` | Part-7 |

Closing dictation:

- Operators have precedence; operands are always evaluated left → right.
- `new` / `instanceof` are compile-time-name tools; `newInstance` / `isInstance`
  are their runtime-name equivalents.
- Hard-coded missing class → `NoClassDefFoundError`. Dynamically missing
  class → `ClassNotFoundException`.
- `==` vs `equals`: identity vs content (and content comparison only if
  `equals` is overridden).
- `&` always evaluates both sides; `&&` may skip the right side — a
  difference that is both a performance choice and, with side effects like
  `x / 0`, a correctness one.
- `if (b = true)` is valid Java. `if (x = 10)` for `int x` is a CE.
- `while (false)` is CE unreachable; `if (false)` is not.

That closes Operators & Assignments. Flow-Control starts next: `if`, `switch`,
loops, `break`, `continue`.

## Rules (as he states them)

1. `new` is an operator that creates an object when the class name is known
   up front.
2. `newInstance()` is a method of `java.lang.Class` that creates an object
   when the class name arrives at runtime. The corresponding class **must**
   have an accessible no-arg constructor.
3. `Class.forName(name)` loads the class; a missing name is a checked
   `ClassNotFoundException`.
4. Hard-coded `new X()` with `X.class` missing at runtime is an unchecked
   `NoClassDefFoundError`.
5. `instanceof` needs a compile-time type with a relation to the reference;
   `null instanceof X` is always `false`.
6. `Class.isInstance(obj)` is the runtime-type version of `instanceof`.
7. `==` on objects is reference comparison; `String.equals` is content;
   `StringBuffer.equals` is still reference.
8. `x = x++` assigns the old value back. `x = ++x + ++x` evaluates operands
   left to right, then assigns.
9. `& | ^` work on `boolean` and integrals; `&& ||` only on `boolean`; `~`
   only on integrals; `!` only on `boolean`.
10. `if` / `while` need a `boolean`. A `boolean` assignment expression is a
    `boolean`; an `int` assignment expression is not.
11. Unreachable: a `while (false)` body, and code after `while (true)`.
    `if (false)` is allowed.

## Exam and interview points

1. `Class.forName("String")` is **not** `java.lang.String` — the default
   package name resolves to nothing, so it throws `ClassNotFoundException`.
   Use the fully qualified `java.lang.String`.
2. `newInstance()` on `Integer`, an abstract class, or any class without a
   no-arg constructor throws `InstantiationException`, not
   `ClassNotFoundException`.
3. A private constructor makes `newInstance()` throw `IllegalAccessException`,
   not `InstantiationException`.
4. Catching `Exception` does **not** catch `NoClassDefFoundError` — it is an
   `Error`, and `Error` is not a subtype of `Exception`.
5. `t instanceof String` when `t` is declared `Thread` is a **compile error**
   (inconvertible types), not `false` — the relation must exist at compile
   time.
6. `sb1.equals(sb2)` for two `StringBuffer("durga")` objects is **false** —
   `StringBuffer` never overrode `equals`.
7. `x = x++` prints the **old** value of `x`, not the incremented one.
8. `if (b = true)` compiles and enters the `if` — assigning a `boolean` value
   produces a `boolean`, which `int` assignment does not.
9. `if (x = 10)` for `int x` is a CE requiring `boolean`.
10. `while (false) { }` is a CE (unreachable body); `if (false) { }` is legal.
11. `&&` can skip a `/ 0` that would otherwise throw; `&` cannot, because it
    always evaluates both sides.
12. `4 && 5` is a CE (`&&` only takes `boolean`); `4 & 5` evaluates to `4`.
13. `Class.newInstance()` is deprecated since **Java 9** — know both the
    legacy call and its replacement, `getDeclaredConstructor().newInstance()`,
    for a current interview.
14. `new Integer(...)` is deprecated since **Java 9** in favour of
    `Integer.valueOf(...)`, which can reuse a cached instance.
15. `if (o instanceof String s)` — Java 16 pattern-matching `instanceof` — is
    the modern one-line form of the classic check-then-cast idiom.

---

**Next:** Video 024 — Flow-Control introduction
