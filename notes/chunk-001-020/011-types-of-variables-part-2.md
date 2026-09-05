# Video 011 — Types of Variables Part 2

## Video info

**Title:** Core Java with OCJP/SCJP: Language Fundamentals Part-11 || Types of Variables :part-2

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 11 of 203 |
| Series | Language Fundamentals · Part 11 of 16 |
| Topic | Types of variables part 2 — local variables, modifiers, thread safety, combinations, uninitialized arrays |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 27m 12s |
| Video ID | CQMaVTO0Cfk |
| Watch | https://www.youtube.com/watch?v=CQMaVTO0Cfk |
| Playlist link | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Recap: instance and static variables were covered last session; this video
   finishes the third kind, **local variables**.
2. What a local variable is, where it lives, and its four names — temporary,
   stack, and automatic variables.
3. Creation and destruction: a fresh copy per block execution and per method
   call — the seed of "locals are thread-safe."
4. Two scope traps the exam loves: a `for` loop's `j` after the loop, and a
   `try` block's `j` used in `catch` or after.
5. The JVM gives locals **no default values** — the real rule is "initialize
   before use," not "always initialize."
6. `int x;` followed by `println("hello")` compiles; followed by `println(x)`
   it does not.
7. The command-line `if (args.length > 0) x = 10;` trap, and why the compiler
   will not take your word for it.
8. `if` / `else` where both branches assign `x` — definite assignment is
   satisfied, so it compiles.
9. Two programming-practice notes: never initialize a local only inside
   `if`/`else`; initialize at declaration instead.
10. The only modifier a local variable can take is **`final`** — every other
    modifier is `illegal start of expression`.
11. "No modifier ⇒ default access" is a rule for instance and static members
    only — it does not apply to locals.
12. Summary tables: default-value rules and thread safety, across instance /
    static / local.
13. Every variable is (instance | static | local) **and** (primitive |
    reference) — six possible combinations.
14. **Uninitialized arrays** at instance, static, and local level — `null`,
    `NullPointerException`, compile error, and why a *created* array's
    elements always default, no matter what kind of variable holds it.

---

## 00:06 — What a local variable is

Last session covered **instance** and **static** variables. The remaining
kind is **local variables**.

Sometimes, to meet a **temporary** requirement, a variable is declared inside
a method, inside a block, or inside a constructor — never at class level.
Such a variable is a **local variable**.

```java
void m1() {
    int x = 10;          // local to the method
}

Test() {
    int x = 10;          // local to the constructor
}

{
    int x = 10;          // local to this instance block
}

static {
    int x = 10;          // local to this static block
}

for (int i = 0; i < 10; i++) {
    System.out.println(i);   // i is local to the for loop
}
```

You can access a local variable only within the method, block, or constructor
where it was declared. It is not permanent class-level or object-level data —
that is why it is also called a **temporary variable**. It is stored in
**stack** memory — that is why it is also called a **stack variable**. And it
is "sometimes available, sometimes not": inside the `for` loop's curly braces
it exists, outside them it is gone automatically — that is why it is also
called an **automatic variable**.

| Name | Why |
|---|---|
| local variable | declared inside a method, block, or constructor |
| temporary variable | not permanent data — only while that block runs |
| stack variable | stored in stack memory |
| automatic variable | available inside the block, automatically gone outside |

This matches the memory-area pattern from video 010: instance → heap,
static → method area, local → **stack**.

> ⚠️ **Modern Java — you can skip writing the type.**
> Every declaration above spells out the type (`int x`). Since **Java 10**
> (JEP 286), a local variable's type can be **inferred** from its initializer
> using `var`:
>
> ```java
> var x = 10;              // inferred: int
> for (var i = 0; i < 3; i++) { }   // inferred: int
> final var y = 20;        // final still applies — inference and final combine
> // var z;                 // CE: cannot infer type for local variable z
> //                           (cannot use 'var' on variable without initializer)
> ```
>
> `var` is not a type and not a new kind of variable — it is still a local
> variable, still stack-stored, still block-scoped, still subject to every
> rule in this lecture. Two restrictions worth knowing: it needs an
> initializer on the same statement, and it exists only for **local**
> variables — fields, method parameters, and return types must still name a
> real type. (`var` is a contextual keyword, per the identifier rules from
> video 001 — it can still name a variable, just never a type.)

---

## 06:17 — Creation, destruction, scope, and why locals get little help

A local variable is **created** while the block in which it was declared is
executing — the method, the static block, the constructor, the `for` loop.
It is **destroyed** the moment that block's execution completes. Call `m1()`,
use its locals in later lines, `m1()` returns — those locals are gone. Call
`m1()` again and a **new** local is created; after that call, it too is gone.

**Call `m1()` ten times and the local variable is created ten times** — not
once. For every execution of the block, a fresh local is created; after the
block, it is gone.

If threads `t1`, `t2`, and `t3` each call `m1()`, each thread gets **its own**
copy of the local — a separate copy is created per thread. That is the seed
of why local variables are considered **thread-safe** (the full table comes
later, at 54:59).

**Scope, in one sentence:** the scope of a local variable is exactly the
scope of the block in which it was declared.

Where each kind of variable sits in the picture:

- **Static variable** → part of the **class** (class-level data)
- **Instance variable** → part of the **object** (object-level data)
- **Local variable** → part of the **method** / **block** / `for` / `if`
  (temporary)

Instance and static are "standard," permanent data; locals are not — they are
temporary. That is why **the JVM gives local variables almost no support**,
in two specific, exam-relevant ways:

1. **No default values.** For instance and static, skipping initialization
   means the JVM supplies a default. There is no such concept for locals —
   you must initialize explicitly (with a refinement at 22:30).
2. **No portable scope.** An instance variable exists wherever its object
   exists; a static variable exists wherever its class exists. A local exists
   only inside its own `if` / `for` / `try` — nowhere else. Scope mistakes
   here are dangerous, and the exam knows it.

### 12:57 — Scope trap 1: `j` after a `for` loop

```java
class Test {
    public static void main(String[] args) {
        int i = 0;
        for (int j = 0; j < 3; j++) {
            i = i + j;
        }
        System.out.println(i + "..." + j);   // CE — see below
    }
}
```

The obvious answer looks tempting: if the loop ran, `i` would end up `0 + 1 +
2 = 3`, and `j` would be `3` once the condition `j < 3` finally fails. Those
values never print, because **the code does not compile**:

```text
cannot find symbol
symbol:   variable j
location: class Test
```

`i` is a local variable of **`main`** — reachable anywhere inside `main`.
`j` is a local variable of the **`for` loop** — reachable only inside it.
Outside the loop, `j` simply does not exist as far as the compiler is
concerned: before it can compile a use of `j`, it needs to know where `j`
lives, and `j`'s scope ended at the loop's closing brace.

### 16:02 — Scope trap 2: `j` declared inside `try`

A compulsory possibility on the exam, straight from the SCJP practice book:

```java
class Test {
    public static void main(String[] args) {
        try {
            int j = Integer.parseInt("ten");   // throws NumberFormatException
        } catch (NumberFormatException e) {
            j = 10;                            // CE
        }
        System.out.println(j);                 // CE
    }
}
```

`"ten"` is not a number, so converting it with `Integer.parseInt` throws
**`NumberFormatException`** at run time (Sir's first guess on the board is
`ClassCastException`; he corrects it immediately to `NumberFormatException`,
which is what the method actually declares). The intent is: if that happens,
set `j = 10` in the `catch` and print it.

**It will not compile.** `j` is a local variable of the **`try` block**.
Outside that block — including inside `catch`, and after the whole
`try`/`catch` — `j` is not visible. Two `cannot find symbol` errors result,
one at `j = 10` and one at the final `println`:

```text
cannot find symbol
symbol:   variable j
location: class Test
```

Scope for local variables is genuinely dangerous — it is sometimes available,
sometimes not, and the exam is built to catch you assuming otherwise.

---

## 21:05 — Defaults: the JVM won't help you here

Default values exist **only for instance and static variables**, never for
local variables:

> **Board:** For local variables, the JVM won't provide default values.
> Initialization must be performed explicitly.

That statement is immediately refined. The next two examples are the real,
exam-accurate version of it.

```java
class Test {
    public static void main(String[] args) {
        int x;
        System.out.println("hello");
    }
}
```

This **compiles**, output `hello`. `x` was never initialized, but it was also
never **used**. You must initialize a local before *using* it — if you never
use it, there is nothing to initialize.

```java
class Test {
    public static void main(String[] args) {
        int x;
        System.out.println(x);
    }
}
```

This is **invalid**:

```text
variable x might not have been initialized
```

**Corrected board rule:** for local variables, the JVM won't provide default
values. Initialization is compulsory **before using** that variable — if you
are not using it, initialization is not required.

| Code | Result |
|---|---|
| `int x;` `System.out.println("hello");` | compiles; prints `hello` |
| `int x;` `System.out.println(x);` | CE: `variable x might not have been initialized` |

### 28:22 — The command-line `if` without `else`

```java
class Test {
    public static void main(String[] args) {
        int x;
        if (args.length > 0) {
            x = 10;
        }
        System.out.println(x);
    }
}
```

If a command-line argument is passed, `args.length > 0` is true, `x` becomes
`10`, and the program prints it. The compiler still **refuses**. Durga's
story for why: you tell the compiler "if we pass arguments, `x` is `10`." The
compiler asks back — and if you don't pass any, what is `x` then? You
initialize `x` **sometimes, not always**, then try to print it regardless.
The joke that follows: a promise of "I'll definitely pass an argument every
time" doesn't move the compiler, because three months ago somebody with an
equally innocent face made the same promise, didn't keep it, and the JVM hit
an uninitialized variable at run time — and the JVM held the compiler
responsible, "because the compiler is the assistant of the JVM." The
compiler will not take that risk on your word:

```text
variable x might not have been initialized
```

The compiler does not care what you intend to do at run time. It only checks
whether `x` is **definitely assigned on every path** through the method.

### 32:13 — `if` / `else` where both branches assign

```java
class Test {
    public static void main(String[] args) {
        int x;
        if (args.length > 0) {
            x = 10;
        } else {
            x = 20;
        }
        System.out.println(x);
    }
}
```

Now `x` is **always** initialized — if arguments are passed, `x` is `10`;
otherwise, `x` is `20`. The code compiles.

| Command | Meaning | Output |
|---|---|---|
| `java Test a` | passing a command-line argument | `10` |
| `java Test` | no command-line argument | `20` |
| `java Test a b` | still `args.length > 0` | `10` |

The `if`-only version is a compile error; the `if`/`else` version compiles,
and its output depends on whether arguments were actually passed.

---

## 34:18 — Two programming-practice notes

**Note 1.** It is **never recommended** to perform a local's initialization
only inside a logical block (`if`, `else`, …). Those blocks may or may not
execute at run time — there is no guarantee. Skip the command-line argument,
and the `if` body never runs.

**Note 2.** It is **highly recommended** to initialize a local **at the time
of declaration**, at least with a sensible default:

```java
int x = 0;
if (args.length > 0) {
    x = 10;
}
System.out.println(x);   // compiles: no args → 0, with args → 10
```

This is the same idiom you already write in real code:

```java
Connection con = null;
String s = null;
```

Writing `= null` explicitly is exactly how you sidestep "might not have been
initialized" — the JVM will never default a local for you, so **you** supply
the default at declaration.

---

## 41:29 — Modifiers on local variables

```java
class Test {
    int x = 10;                 // instance
    static int y = 20;          // static

    public static void main(String[] args) {
        int j = 30;             // local
    }
}
```

For **instance** members (and identically for **static**):

| Modifier | Access (preview of access modifiers, taught in full later) |
|---|---|
| `public` | anywhere |
| `private` | only within the class |
| default (no modifier) | anywhere in the current package |
| `protected` | current package anywhere; outside the package only in child classes |

Those modifiers change the **scope / accessibility** of instance and static
members. A local's scope is already fixed to its own method — `public int j`
does not let you use `j` outside that method. So `public`, `private`,
`protected`, and default access are **not applicable** to local variables.

**The only applicable modifier for a local variable is `final`.** Any other
modifier is a compile-time error:

```java
class Test {
    public static void main(String[] args) {
        public    int x = 10;    // CE
        private   int x = 10;    // CE
        protected int x = 10;    // CE
        static    int x = 10;    // CE
        transient int x = 10;    // CE
        volatile  int x = 10;    // CE

        final int x = 10;        // valid
    }
}
```

Every illegal case produces the same message:

```text
illegal start of expression
```

Compiled and confirmed on JDK 26: `public`, `private`, `protected`, `static`,
`transient`, and `volatile` all fail this way on a local; `final` is fine.

> ⚠️ **Modern Java — `final` on a local got a lot more important after this
> recording.**
> Two changes since Java 8 lean directly on the fact that `final` (or merely
> *effectively final* — never reassigned after its first value) is legal on a
> local:
>
> ```java
> import java.io.*;
>
> class TwrTest {
>     public static void main(String[] args) throws Exception {
>         Reader r = new StringReader("hi");   // effectively final
>
>         Runnable capture = () -> System.out.println(r);  // Java 8: lambdas
>                                                            // may only capture
>                                                            // effectively-final locals
>
>         try (r) {                             // Java 9+: try-with-resources can
>             System.out.println(r.read());     // reuse an existing effectively-final
>         }                                      // variable — no re-declaration needed
>     }
> }
> ```
>
> Neither feature existed when this was recorded, but neither one changes
> Sir's rule — they are *consumers* of it. A lambda or try-with-resources can
> only reach outside its own body for a local that satisfies exactly the
> constraint this section teaches.

### 48:45 — "No modifier ⇒ default access" does not apply to locals

If an instance variable carries no modifier, it gets **default** (package)
access — reachable anywhere in the current package. The same is true for a
static variable with no modifier.

```java
void m1() {
    int j = 30;
}
```

Is `j` "default" access, then? If it were, you could reach it anywhere in the
current package — but you cannot access `j` outside `m1`, package or no
package. So: **the "no modifier means default access" rule applies only to
instance and static variables, never to local variables.** A local's scope is
always its block; the package-wide and class-wide access rules simply do not
exist for it.

---

## 52:27 — Summary conclusions: defaults and thread safety

**Defaults.** For instance and static variables, the JVM provides default
values — explicit initialization is not required. For local variables, the
JVM provides none — initialization is compulsory, and specifically required
**before using** that variable.

**Thread safety.** An instance variable is part of an object, and a single
object can be accessed by multiple threads at once — so instance variables
are **not thread-safe**. A static variable has only one copy at the class
level, and that one copy can likewise be accessed by multiple threads at
once — so static variables are **also not thread-safe**. A local variable,
by contrast, gets a **separate copy per thread**: if `t1` and `t2` both call
a method with `int x = 10;`, a modification by `t1` is never reflected in
`t2`'s copy — so local variables **are thread-safe**.

| Type of variable | Thread-safe? |
|---|---|
| instance variable | no |
| static variable | no |
| local variable | yes |

Worth being precise about what "thread-safe" means here: it is the **storage
location** that is thread-confined, because each thread has its own stack
frame. If that local happens to be a *reference* pointing at a shared mutable
object (an object also reachable from elsewhere), the object itself carries
none of that safety — only the reference variable does. The rule protects the
variable, not necessarily whatever it points to.

---

## 1:00:09 — Six combinations: instance/static/local × primitive/reference

Every variable in Java is **compulsorily** one of instance, static, or local.
Every variable is **also** either a primitive or a reference. Crossing the
two divisions from video 010 gives six possible combinations:

1. instance primitive
2. instance reference
3. static primitive
4. static reference
5. local primitive
6. local reference

```java
class Test {
    int x = 10;                    // instance + primitive
    static String s = "durga";     // static + reference

    public static void main(String[] args) {
        int[] y = new int[3];      // local + reference (every array is an object)
    }
}
```

| Variable | instance / static / local | primitive / reference | Combination |
|---|---|---|---|
| `x` | instance | primitive (`int`) | instance primitive |
| `s` | static | reference (`String` object) | static reference |
| `y` | local | reference (array is an object) | local reference |

Yes — an instance variable can be either primitive or reference, and so can a
static variable, and so can a local variable. All six combinations exist and
are all legal.

---

## 1:08:37 — Uninitialized arrays

The behavior when you **declare** an array but do not create it — and how
that behavior differs between instance, static, and local level. This part
matters.

### Instance level

```java
class Test {
    int[] x;   // instance, reference — array is an object

    public static void main(String[] args) {
        Test t = new Test();
        System.out.println(t.x);
        System.out.println(t.x[0]);
    }
}
```

An instance variable always gets a JVM default; `x` is a **reference**, so
its default is **`null`**.

- `t.x` → `null`
- `t.x[0]` → asking `null` for its first element → runtime
  `NullPointerException`

> ⚠️ **Modern Java — the NullPointerException now tells you exactly what was
> null.**
> Since **Java 14** (JEP 358, opt-in; default from **Java 15**), the JVM
> synthesizes a detailed message identifying the null expression, instead of
> a bare `NullPointerException`:
>
> ```text
> Exception in thread "main" java.lang.NullPointerException:
>     Cannot load from int array because "t.x" is null
>         at Test.main(Test.java:6)
> ```
>
> Verified on JDK 26 — compiled with `-g` the message names the exact
> reference (`"t.x"`); compiled without it, it still names the slot
> (`"<local1>.x"`), so either way it is far more useful than the plain
> exception Sir demonstrates here. The feature can be turned off with
> `-XX:-ShowCodeDetailsInExceptionMessages` if you ever need the old message.

Now create the array:

```java
class Test {
    int[] x = new int[3];

    public static void main(String[] args) {
        Test t = new Test();
        System.out.println(t.x);
        System.out.println(t.x[0]);
    }
}
```

`x` is initialized and points to an array object.

- Printing a reference calls `toString()`: the array's class-name code
  `[I` (`[` = array, `I` = `int`), `@`, and a hex hash code, e.g. `[I@3e25a5`.
- Once an array is **created**, every element is initialized with its type's
  default — `0` for `int`. So `t.x[0]` → `0`.

### Static level

Same numbers, but no object reference is needed — access directly.

```java
class Test {
    static int[] x;

    public static void main(String[] args) {
        System.out.println(x);      // null  (JVM default for a static reference)
        System.out.println(x[0]);   // NullPointerException
    }
}
```

```java
class Test {
    static int[] x = new int[3];

    public static void main(String[] args) {
        System.out.println(x);      // [I@<hash>
        System.out.println(x[0]);   // 0
    }
}
```

Static also gets a JVM default, so an uninitialized `x` is still `null` and
`x[0]` is still an NPE. Once created, the array's `toString()` prints its
`[I@hash` form and `x[0]` is `0`.

### Local level — the behavior changes

```java
class Test {
    public static void main(String[] args) {
        int[] x;
        System.out.println(x);      // CE
        System.out.println(x[0]);   // CE
    }
}
```

The JVM gives locals **no default values**. Both lines are compile errors:

```text
variable x might not have been initialized
```

Now create the array:

```java
class Test {
    public static void main(String[] args) {
        int[] x = new int[3];
        System.out.println(x);      // [I@<hash>   — x is initialized with the object
        System.out.println(x[0]);   // 0           — NOT a compile error
    }
}
```

The tempting wrong guess is that `x[0]` is still a compile error because `x`
is local. It is not — the output is `0`. Once an array is created, **every
element is initialized with its default value, whether the array itself is
local, static, or instance**. `x` is the local variable; `x[0]` is **part of
the array object**. Array-element defaults dominate over whatever kind of
variable is holding the reference.

Side by side, the full picture for `int[] x`:

| Declaration | `System.out.println(x)` | `System.out.println(x[0])` |
|---|---|---|
| `instance int[] x;` | `null` | `NullPointerException` |
| `instance int[] x = new int[3];` | `[I@<hashcode>` | `0` |
| `static int[] x;` | `null` | `NullPointerException` |
| `static int[] x = new int[3];` | `[I@<hashcode>` | `0` |
| `local int[] x;` | CE: variable `x` might not have been initialized | CE: same |
| `local int[] x = new int[3];` | `[I@<hashcode>` | `0` |

### 1:25:27 — The closing note

Once an array is created, every element is by default initialized with the
default value **irrespective of whether the array itself is instance,
static, or local**. That closes the topic: instance, static, and local
variables; initialized versus uninitialized; and the array-element special
case that overrides all three.

---

## Exam and interview points

1. **Local variables are also called temporary, stack, and automatic
   variables** — one name per property: lifetime, storage location, and the
   "sometimes in scope" behavior.
2. **Calling a method ten times creates its locals ten times, not once.**
   Each call gets a fresh copy; each return destroys it.
3. **Locals are thread-safe because each thread gets its own copy** — but
   that safety belongs to the storage location, not to whatever object a
   local *reference* points to.
4. **`for (int j = 0; j < 3; j++) { … } System.out.println(j);` is `cannot
   find symbol`**, not "`j` is `3`." `j`'s scope ends at the loop's closing
   brace.
5. **`int j` declared inside `try` is invisible in `catch` and after the
   `try`.** Same `cannot find symbol` error, in both places. The example's
   exception is **`NumberFormatException`** from `Integer.parseInt("ten")`,
   not `ClassCastException` — a slip worth catching if an interviewer makes
   it too.
6. **An uninitialized local that is never read is legal:** `int x;
   System.out.println("hello");` compiles. The rule is "initialize before
   *use*," not "initialize, period."
7. **An uninitialized local that *is* read fails with `variable x might not
   have been initialized`** — a distinct message from `cannot find symbol`.
   Know which trap produces which wording.
8. **The compiler never trusts "I promise to pass that argument."**
   `if (args.length > 0) x = 10;` followed by `System.out.println(x);` is a
   compile error even if you always remember to pass an argument at run
   time — definite assignment is checked on every possible path, not on your
   intentions.
9. **`if`/`else` where both branches assign compiles**, and its output
   depends on the actual command line: `java Test` prints `20`, `java Test a`
   prints `10`.
10. **Never initialize a local only inside a logical block.** Initialize at
    declaration instead (`int x = 0;`, `String s = null;`) — the same reason
    real code writes `Connection con = null;`.
11. **The only modifier a local variable can take is `final`.**
    `public`/`private`/`protected`/`static`/`transient`/`volatile` on a local
    all produce `illegal start of expression` — verified on JDK 26 — not a
    friendlier "modifier not allowed" message.
12. **"No modifier ⇒ default access" applies only to instance and static
    members.** A local's scope is fixed to its block regardless of any
    modifier you could imagine writing on it.
13. **An array variable (`int[] y`) is always a reference**, even though its
    element type is primitive — every array in Java is an object. The
    combination is local/instance/static **reference**, never "primitive
    array."
14. **Uninitialized instance/static `int[] x`:** printing `x` gives `null`;
    printing `x[0]` throws `NullPointerException` at **run time**, not a
    compile error.
15. **Uninitialized *local* `int[] x`:** both `x` and `x[0]` are **compile
    errors** — `variable x might not have been initialized` — because locals
    get no JVM default at all, not even `null`.
16. **Once an array is created, `x[0]` is `0` regardless of whether `x` is
    local, static, or instance.** Array-element defaults are a property of
    the array object, independent of what kind of variable references it.
17. **Since Java 10, `var` can infer a local's type** from its initializer
    (`var x = 10;`), but it changes nothing about scope, defaults, or thread
    safety — it only removes the need to spell the type out, and only for
    locals (not fields, not parameters, not return types).
18. **Since Java 14/15, `NullPointerException` messages name the null
    expression** (JEP 358) — the classic `t.x[0]` NPE from this lecture now
    reads `Cannot load from int array because "t.x" is null` instead of a
    bare stack trace.
19. **`final`/effectively-final locals underpin two Java 8/9 features**:
    lambdas may only capture effectively-final locals (Java 8), and
    try-with-resources can reuse an existing effectively-final variable
    without re-declaring it (Java 9) — neither existed at recording time, but
    both are direct consequences of the modifier rule taught here.

---

**Next:** Video 012 — var-arg methods
