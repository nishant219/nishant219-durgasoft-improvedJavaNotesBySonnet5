# Video 010 — Types of Variables Part 1

## Video info

| Field | Detail |
|---|---|
| Playlist | Core Java with OCJP/SCJP — Durga Sir |
| Position | Video 10 of 203 |
| Series | Language Fundamentals · Part 10 of 16 |
| Topic | Types of variables part 1 — primitive vs reference; instance vs static |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 1h 08m 38s |
| Watch | https://www.youtube.com/watch?v=Nw7NyvuwOTM |
| Playlist | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

1. Why "types of variables" is an interview *and* day-to-day programming topic
2. **Division 1** — based on the *type of value* a variable represents: primitive vs reference
3. **Division 2** — based on *position of declaration* and *behaviour*: instance vs static vs local (local is started in video 011)
4. Instance variables: definition, the `Student` example, copies, where to declare them, creation/destruction/scope, heap storage, access rules, default values, other names
5. Static variables: the college-name example, why not instance, copies, where to declare them, the class-loading cinema, method-area storage, access rules, default values, other names
6. The classic exam program: change `t1.x` / `t1.y`, print `t2.x` / `t2.y`

---

## 00:05 — Why this topic exists

Durga flags types of variables as **the most valuable topic for the interview
room**, and equally important for day-to-day programming. There are two
divisions:

1. Based on the **type of value** represented by a variable.
2. Based on **position of declaration** and **behaviour** — this is the one
   interviewers and daily coding actually care about.

## 00:41 — Division 1: based on the type of value

Based on the type of value a variable represents, **all variables fall into
two types**. Nothing else exists in this division.

#### Primitive variables

Variables used to represent **primitive values**.

```java
int x = 10;
```

`x` exists to hold the `int` primitive value `10` — a **primitive variable**.

> **Board:** Can be used to represent primitive values. Example: `int x = 10;`

#### Reference variables

Variables used to **refer to objects**.

```java
Student s = new Student();
```

`s` points to a `Student` object — a **reference variable**.

> **Board:** Can be used to refer objects. Example: `Student s = new Student();`

| Kind | Used for | Example |
|---|---|---|
| Primitive variable | a primitive value | `int x = 10;` |
| Reference variable | referring to an object | `Student s = new Student();` |

That is the entire first division — every variable is one of these two.

## 05:35 — Division 2: based on position and behaviour

**More important** than division 1, for interviews and for writing real
programs. Based on **where** a variable is declared (directly inside the
class? inside a method?) and on its **behaviour**, all variables fall into
**three types**:

1. Instance variables
2. Static variables
3. Local variables

This video finishes instance and static. Local variables continue in video 011.

## 07:47 — Instance variables — the `Student` example

```java
class Student {
    String name;
    int rollNumber;
}
```

Every student is required to have a name and a roll number. Create many
objects:

| Object | name | rollNumber |
|---|---|---|
| s1 | "Ravi" | 101 |
| s2 | "Durga" | 102 |
| … | … | … |
| s600 | "Shiva" | 600 |

The value of `name` **varies from object to object**. So does `rollNumber`.

> **Board:** If the value of a variable is varied from object to object, such
> a type of variable is called an **instance variable**.

**Copies:** for every object, a **separate copy** of each instance variable is
created — 600 students in the room means 600 copies of `name` and 600 copies
of `rollNumber`.

Two points to lock in:

1. Value varies from object to object → instance variable.
2. For every object, a separate copy of the instance variable is created.

### 12:34 — Where instance variables must be declared

Instance variables must be declared **within the class directly**, but
**outside of any method, block, or constructor**.

```java
class Test {
    int x = 10;   // instance variable — declared in the class directly
}
```

Contrast — declared inside a method, constructor, or block, it is **local**,
not instance:

```java
class Test {
    void m1() {
        int x = 10;          // local — inside a method
    }

    Test() {
        int x = 10;          // local — inside a constructor
    }

    {
        int x = 10;          // local — inside an instance block
    }

    static {
        int x = 10;          // local — inside a static block
    }

    void m2() {
        for (int i = 0; i < 10; i++) {   // i is local to the for loop (a block)
        }
    }
}
```

Any variable declared inside a method, constructor, or block (static block,
instance block, `for` loop, `if` block, …) is **local**. That is why instance
variables must sit in the class body itself.

### 14:47 — Creation, destruction, and scope of instance variables

- Created **at the time of object creation**.
- Destroyed **at the time of object destruction**.

An instance variable is always **part of the object**: when the student
object is created, that student's `name` and `rollNumber` come into
existence; when the object is gone, so are they.

> **Hence: the scope of an instance variable is exactly the same as the scope
> of the object.** If the object is in memory, the instance variable is
> there. If the object is not there, the instance variable is gone.

> ⚠️ **Modern Java — "at the time of object destruction" is not a moment you
> can pin down, and Java no longer even offers the hook that pretended to be
> one.**
> Java has no destructor. An object (and the instance variables riding inside
> it) becomes eligible for collection the moment nothing reachable points to
> it, but the garbage collector reclaims it at an **unspecified later time**
> — possibly never, if the JVM exits first. `Object.finalize()` used to be
> sold as "the destructor," a method the GC calls once before reclaiming an
> object:
>
> ```java
> class Res {
>     @Override
>     protected void finalize() throws Throwable {   // deprecated since Java 9
>         System.out.println("cleaning up");
>     }
> }
> ```
>
> `finalize()` has been **deprecated for removal since Java 9** and, from
> **Java 18** (JEP 421), finalization is **disabled by default** — the
> callback simply does not run unless you opt back in with
> `--finalization=enabled`. The replacement for "run this when a resource is
> no longer needed" is deterministic: `try`-with-resources / `Closeable`
> for anything with a lifetime you control, and `java.lang.ref.Cleaner` for
> the rare case where you must react to unreachability itself. The teaching
> point stands — scope tracks the object — but "destruction" was always a
> GC-timed event, never a language guarantee.

### 17:10 — Where instance variables are stored

Objects live in **heap** memory. An instance variable is part of the object,
so it is stored **in the heap, as part of the object**.

Interview line: *In which memory area are instance variables stored?* → heap,
as part of the object.

### 18:13 — Accessing instance variables (static area vs instance area)

```java
class Test {
    int x = 10;

    public static void main(String[] args) {
        System.out.println(x);   // CE
    }
}
```

**Invalid.** Verified on JDK 26:

```text
error: non-static variable x cannot be referenced from a static context
        System.out.println(x);
                           ^
```

Why: `main` is a **static** method — no way related to an object. An
instance variable is always **part of** an object, and `main` can run before
any object exists. No object, no instance variable, so direct `x` from
`main` is illegal.

**Fix — access via an object reference from the static area:**

```java
class Test {
    int x = 10;

    public static void main(String[] args) {
        Test t = new Test();
        System.out.println(t.x);   // valid — prints 10
    }
}
```

**From the instance area you can access instance variables directly:**

```java
class Test {
    int x = 10;

    public void m1() {                 // instance method — always called on an object
        System.out.println(x);         // valid — that object's x
    }
}
```

An instance method is always tied to an object, so that object's `x` is
available with no extra reference.

> **Board:**
> - We **can't** access instance variables **directly from static area**.
> - But we **can** access them **by using object reference**.
> - We **can** access instance variables **directly from instance area**.

### 25:02 — Default values for instance variables

For instance variables, initialization is **not required**. The **JVM always
provides default values**.

```java
class Test {
    int x;
    double d;
    boolean b;
    String s;

    public static void main(String[] args) {
        Test t1 = new Test();
        System.out.println(t1.x);   // 0
        System.out.println(t1.d);   // 0.0
        System.out.println(t1.b);   // false
        System.out.println(t1.s);   // null
    }
}
```

| Variable | Type | Default |
|---|---|---|
| `t1.x` | `int` | `0` |
| `t1.d` | `double` | `0.0` |
| `t1.b` | `boolean` | `false` |
| `t1.s` | `String` (reference) | `null` |

> **Board:** For instance variables, JVM will always provide default values,
> and we are not required to perform initialization explicitly.

### 28:57 — Other names for instance variables

Also known as:

- **object-level variables**
- **attributes** — a C++-style word; every object has state and behaviour,
  and **state** is the values of its attributes
- **properties** — attributes ≈ properties

## 30:21 — Static variables — the college-name example

```java
class Student {
    String name;
    int rollNumber;
    String collegeName;
}
```

Create 600 student objects:

| Object | name | rollNumber | collegeName |
|---|---|---|---|
| first | "Durga" | 101 | "DurgaSoft" |
| second | "Shiva" | 102 | "DurgaSoft" |
| third | "Ravi" | 103 | "DurgaSoft" |
| … | … | … | "DurgaSoft" |

`name` and `rollNumber` vary from object to object. `collegeName` is **fixed
for all objects**.

> **Board:** If the value of a variable is **not varied from object to
> object**, it is **never recommended** to declare that variable as an
> instance variable. We have to declare such a variable **at class level**
> using the **`static`** modifier.

The problem with keeping `collegeName` as instance: 600 objects means 600
copies of the identical string `"DurgaSoft"` — unnecessary memory waste,
performance down. Declare it `static` instead, so only **one copy** exists at
class level, **shared** by every object:

```java
class Student {
    String name;                 // instance — varies per object
    int rollNumber;              // instance — varies per object
    static String collegeName;   // static — one copy, shared
}
```

### 36:12 — Copies: instance vs static

|  | Instance | Static |
|---|---|---|
| Copies | A separate copy for every object | A single copy at class level, shared by every object of the class |

That is the basic difference Durga asks students to recite.

### 38:04 — Where static variables must be declared

Same place as instance variables, plus the word `static`: within the class
directly, outside of any method, block, or constructor.

```java
class Test {
    static int x = 10;   // correct place
}
```

The only difference from an instance declaration is the modifier `static`.

### 39:17 — Creation, destruction, and scope of static variables

- Created **at the time of class loading**.
- Destroyed **at the time of class unloading**.

> **Hence: the scope of a static variable is exactly the same as the scope of
> the `.class` file.**

The immediate student doubt: *when* does a class load and unload? That is the
next cinema.

### 41:25 — The `java Test` cinema — when static variables are born and die

Command: `java Test` — "execute this class." Internally it is not one step.
The sequence:

1. **Start JVM** — it is responsible for the whole job, so it starts first.
2. **Create and start the main thread** — the main thread does the rest of
   the work on the JVM's behalf.
3. **Locate `Test.class`** — the main thread searches for the class file. If
   it is not there:

   ```text
   Exception in thread "main" java.lang.NoClassDefFoundError: Test
   ```

   (`main` appears in the message because the **main thread** did the
   looking.)
4. **Load `Test.class`** — once located, load it. **Static variables are
   created at this step.**
5. **Execute the `main` method.**
6. **Unload `Test.class`** — once `main` finishes, the job with that class
   file is done. **Static variables are destroyed at this step.**
7. **Terminate the main thread** — its job is complete.
8. **Shut down the JVM.**

So: static variables are created at class loading and destroyed at class
unloading — concrete, not magic.

> ⚠️ **Modern Java — the missing-class error message changed in Java 7, and
> it no longer comes from inside the main thread.**
> `Exception in thread "main" java.lang.NoClassDefFoundError: Test` is the
> genuine Java 6 message for this scenario. From **Java 7 onward** the
> launcher checks for the main class **before it starts the main thread at
> all**, and reports a different, friendlier error. Verified on JDK 26:
>
> ```text
> $ java Test
> Error: Could not find or load main class Test
> Caused by: java.lang.ClassNotFoundException: Test
> ```
>
> There is no `"main"` in that message any more, because there is no main
> thread yet to blame — the class-lookup failure now happens one step earlier
> in the cinema, between steps 2 and 3. `NoClassDefFoundError` still exists
> and still fires the classic way, but only for a **different** scenario:
> a class that compiled fine and linked at first, then goes missing from the
> classpath on a *later* reference (a genuine linkage error, not a missing
> main class).

> ❗ **Correction — "class loading" is really three separate phases, and
> static initializers do not necessarily run at step 4.**
> The JVM specification (JLS §12, JVMS §5.5) splits what Sir calls "loading"
> into **loading**, **linking** (verification, preparation, resolution), and
> **initialization**. Default values (`0`, `0.0`, `false`, `null`) are
> assigned to static fields during **linking** — that part does happen
> essentially as soon as the class comes into the JVM, matching the lecture.
> But a static field's **explicit initializer or assignment** runs only
> during **initialization**, and initialization is **lazy**: it is deferred
> until the class's first *active use* (a static method call, a
> non-constant static field access, `new`, …), not necessarily right when the
> class is located. Proof:
>
> ```java
> class Holder {
>     static { System.out.println("Holder initialized"); }
>     static int x = 42;
> }
>
> public class Demo {
>     public static void main(String[] args) {
>         System.out.println("main started");
>         Holder h = null;              // a mere reference type — no active use
>         System.out.println("declared, not yet initialized");
>         System.out.println(Holder.x); // first active use — triggers init now
>     }
> }
> ```
>
> ```text
> main started
> declared, not yet initialized
> Holder initialized
> 42
> ```
>
> For the *simple* single-class programs this lecture uses, `main` itself is
> the first active use of `Test`, so "created at class loading" and "created
> at class initialization" land on the same instant and Sir's simplified
> timeline is not wrong for those examples. The distinction matters once a
> program has more than one class: a static variable in a class nobody has
> actively used yet has its **slot** ready (default value) but has not run
> its **initializer**.

### 49:50 — Where static variables are stored — method area, not stack

Durga calls out the trap by name: do not say "stack" just because "static"
and "stack" sound alike.

- **Static variables** → **method area** — another memory area, alongside heap.
- **Instance variables** → **heap**, as part of the object (already covered).
- **Local variables** → **stack** (preview of video 011 — that is why locals
  are also called stack variables).

> **Board:** Static variables will be stored in method area.

### 51:15 — How to access static variables

```java
class Test {
    static int x = 10;

    public static void main(String[] args) {
        Test t = new Test();
        System.out.println(t.x);      // valid — via object reference
        System.out.println(Test.x);   // valid — via class name (recommended)
        System.out.println(x);        // valid — same class, directly
    }
}
```

All three are valid. Rules:

1. Static variables can be accessed **either by object reference or by class
   name**.
2. **Recommended: class name.** An object reference is the natural way to
   reach an *instance* variable; using it for a static variable hurts
   readability, since it looks like instance data.
3. **Within the same class**, the class name is optional — access the static
   variable directly.

### 55:32 — Static variables from static area and from instance area

```java
class Test {
    static int x = 10;

    public static void main(String[] args) {
        System.out.println(x);   // valid — static variable from static area
    }

    public void m1() {
        System.out.println(x);   // valid — static variable from instance area
    }
}
```

Both valid: static variables are created at **class loading**, before `main`
runs and before any object exists, so they are reachable from anywhere.
Contrast with instance variables, which cannot be accessed directly from a
static area.

> **Board:** We can access static variables directly from both instance and
> static areas.

### 58:21 — Default values for static variables

Same story as instance variables — the JVM gives even *more* support to
class-level data, not less.

```java
class Test {
    static int x;
    static double d;
    static String s;

    public static void main(String[] args) {
        System.out.println(x);   // 0
        System.out.println(d);   // 0.0
        System.out.println(s);   // null
    }
}
```

> **Board:** For static variables, JVM will provide default values, and we
> are not required to perform initialization explicitly.

### 1:01:36 — Other names for static variables

Also known as:

- **class-level variables**
- **fields**

(Instance = object-level / attributes. Static = class-level / fields.)

> ❗ **Careful — "field" is not exclusive to static variables.**
> In the official vocabulary (JLS §8.3, and `java.lang.reflect.Field`'s own
> javadoc: *"the reflected field may be a class \[static\] field or an
> instance field"*), **field is the umbrella term for any class-or-instance
> member variable** — instance variables are *instance fields*, static
> variables are *static fields* (or *class fields*). Calling only the static
> ones "fields," as the lecture's word list does, understates the term. If an
> interviewer asks "what's a field," the accurate answer is "either kind of
> member variable" — instance included.

## 1:02:31 — Exam program: one static copy vs a separate instance copy

Keep in mind: instance = object-level, separate copy per object; static =
class-level, one copy shared by all.

```java
class Test {
    static int x = 10;
    int y = 20;

    public static void main(String[] args) {
        Test t1 = new Test();
        t1.x = 888;
        t1.y = 999;
        Test t2 = new Test();
        System.out.println(t2.x + "..." + t2.y);
    }
}
```

**Output: `888...20`.** Verified on JDK 26. Walk-through:

1. **Static is created first**, at class loading — `x = 10` already exists
   before any object does (one class-level copy).
2. `Test t1 = new Test();` — object `t1` is created; a **separate** copy of
   instance variable `y` is created for it, initialized to `20`.
3. `t1.x = 888;` — there is only **one** `x`. Changing it through `t1`
   changes the **shared** copy: class-level `x` is now `888`.
4. `t1.y = 999;` — this changes **only `t1`'s** `y`. Other objects are
   unaffected.
5. `Test t2 = new Test();` — a **new** object gets a **new** copy of instance
   `y`, initialized to `20`. **No new copy of `x`** is created — there is
   still only one.
6. `t2.x` → `888` (the shared copy, already changed). `t2.y` → `20` (this
   object's own, untouched copy).

Options an exam might throw at you: `888`/`20` ✅, `10`/`20` (as if `t1.x =
888` never happened), `888`/`999` (as if `y` were shared too), `10`/`999`
(mixing both up backwards).

> **Exam line to repeat:** a static variable has only one copy — change it
> through any object reference and the change shows up everywhere. An
> instance variable has a separate copy per object — changing it for one
> object never reflects in another, because each object owns its own copy.

## Code from the lecture

```java
class Test {
    int x = 10;              // instance
    static int sx = 10;      // static

    public static void main(String[] args) {
        // System.out.println(x);           // CE: non-static variable x cannot be referenced from a static context
        Test t = new Test();
        System.out.println(t.x);            // 10 — instance via object reference
        System.out.println(t.sx);           // 10 — legal but not recommended
        System.out.println(Test.sx);        // 10 — recommended
        System.out.println(sx);             // 10 — same class, directly
        t.m1();
    }

    public void m1() {
        System.out.println(x);              // 10 — instance from instance area
        System.out.println(sx);             // 10 — static from instance area
    }
}
```

```java
class Test {
    int x;
    double d;
    boolean b;
    String s;

    public static void main(String[] args) {
        Test t1 = new Test();
        System.out.println(t1.x);   // 0
        System.out.println(t1.d);   // 0.0
        System.out.println(t1.b);   // false
        System.out.println(t1.s);   // null
    }
}
```

```java
class Test {
    static int x;
    static double d;
    static String s;

    public static void main(String[] args) {
        System.out.println(x);   // 0
        System.out.println(d);   // 0.0
        System.out.println(s);   // null
    }
}
```

```java
class Test {
    static int x = 10;
    int y = 20;

    public static void main(String[] args) {
        Test t1 = new Test();
        t1.x = 888;
        t1.y = 999;
        Test t2 = new Test();
        System.out.println(t2.x + "..." + t2.y);   // 888...20
    }
}
```

```java
class Student {
    String name;                 // instance — object level
    int rollNumber;              // instance
    static String collegeName;   // static — class level, one shared copy
}
```

All five compile and run as annotated — verified against JDK 26.

## Exam and interview points

1. **Two independent divisions.** (primitive | reference) and (instance |
   static | local) are separate axes — every variable is one from each
   division. Combinations arrive in video 011.
2. **Instance ≠ "declared in a class file."** Inside a method, constructor,
   or block, a variable is **local**, no matter how it looks otherwise.
3. **`System.out.println(x)` for instance `x` inside `main` is a compile-time
   error**, not a runtime one: `non-static variable x cannot be referenced
   from a static context`.
4. **From `main`, `t.x` is the legal way to reach an instance variable** —
   object reference from a static context.
5. **Instance default values exist; local default values do not** (video
   011). Do not mix these up. `boolean` defaults to `false`, not `0`;
   references default to `null`.
6. **Static is stored in the method area, never the stack.** Stack is for
   locals only; instance lives in the heap as part of the object.
7. **`t.x` for a static `x` compiles** — legal, but poor style. Prefer
   `Test.x`. Within the same class, the bare name is enough, even from an
   instance method.
8. **Static variables are created at class loading (well, at the class's
   linking + first active use — see the correction above) and destroyed at
   class unloading** — which is why `main` can print a static field before
   any object exists.
9. **`java Test` with no `Test.class`** gives `NoClassDefFoundError` on Java
   6/7-era JDKs; a **current** JDK instead prints `Error: Could not find or
   load main class Test`, caught before the main thread is even created.
   Know both — an OCJP-era question bank still expects the old wording.
10. **`t1.x = 888; t1.y = 999;` then print `t2.x` and `t2.y` → `888` and
    `20`**, never `999`. A static change is global; an instance change is
    per object.
11. **Instance variables** = object-level variables / attributes /
    properties. **Static variables** = class-level variables — and, more
    precisely, both kinds are "fields"; static ones are *static fields*,
    instance ones are *instance fields*.
12. **"Destroyed at object destruction" is GC-timed, not deterministic.**
    Java has no destructor; `finalize()` is deprecated since Java 9 and
    disabled by default since Java 18. Use try-with-resources or
    `java.lang.ref.Cleaner` for real cleanup logic.

---

**Next:** Video 011 — Types of Variables Part 2
