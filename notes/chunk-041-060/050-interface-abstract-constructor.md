# Video 050 — Interface, Abstract Class, Constructor: Recap

## Video info

**Title:** Java -  Interface  and Abstract class Loopholes Part-7 ||Interface, Abstract class, constructor

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | Video 50 of 203 |
| Series | Interface and Abstract class Loopholes · Part 7 |
| Topic | Interface, Abstract class, constructor |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 11m 12s |
| Video ID | U7uOLV5yOP0 |
| Watch | https://www.youtube.com/watch?v=U7uOLV5yOP0 |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This is the closing video of the **Interface and Abstract class Loopholes**
stretch (videos 044–049): `new` vs constructor, abstract-class objects, child
object vs parent constructor, the abstract-class constructor, and the
interface constructor. Nothing new is taught here — it is a twelve-statement
exam-bit drill that recaps the whole stretch in two passes:

1. **Listen pass (00:25–03:34):** Sir reads each of twelve true/false
   statements and gives the answer as he goes.
2. **Board pass (03:34–10:40):** the same twelve statements, copied onto the
   board one at a time with a tick (valid) or cross (invalid) next to each —
   the exact form the OCJP bit question takes.

Treat this note as the answer key for the whole stretch: if a statement here
is unclear, the video number in its explanation is where it was first taught
in full.

---

### 00:25 — Format: listen first, answers follow

Sir's framing: this is exactly the shape an OCJP bit takes — a statement,
and you mark it valid or invalid. Twelve statements follow, each already
covered across videos 044–049; this drill is only testing whether the
wording sticks.

### 00:40 — Bit 1: "constructor's purpose is to create an object" — invalid

**Invalid.** A constructor's job is to **initialize** an object, not to
create it — creation is `new`'s job (video 044).

```java
class Test {
    Test() {
        // initializes the object new already created — does not create it
    }

    public static void main(String[] args) {
        Test t = new Test();   // compiles fine; new creates, Test() initializes
    }
}
```

### 01:03 — Bit 2: "constructor initializes, does not create" — valid

**Valid.** This is the corrected wording of Bit 1, and the one to remember.

### 01:11 — Bit 3: "object creation completes only once the constructor finishes" — invalid

**Invalid.** `new` is what creates the object; once `new` completes, the
object already exists, and the constructor then runs to initialize it. The
constructor finishing does not gate creation — creation already happened.

```java
class Test {
    int x;

    Test() {
        x = 10;   // initialization only; the object already existed by now
    }

    public static void main(String[] args) {
        Test t = new Test();
        // 1. new creates the object
        // 2. constructor runs to initialize it
    }
}
```

### 01:34 — Bit 4: "first the object is created, then the constructor executes" — valid

**Valid.** This is the correct order, restated from video 044.

### 01:39 — Bit 5: "new creates, constructor initializes" — valid

**Valid.** Already covered in full in video 044.

```java
class Test {
    Test() {
        System.out.println("constructor: initialize");
    }

    public static void main(String[] args) {
        Test t = new Test();   // prints "constructor: initialize"
        // new created t; Test() initialized t
    }
}
```

### 01:51 — Bit 6: "can't create an abstract-class object directly, but indirectly we can" — invalid

**Invalid.** Neither directly nor indirectly can an abstract class be
instantiated (video 047).

```java
abstract class Test {
}

class Demo {
    public static void main(String[] args) {
        Test t = new Test();
        // CE: Test is abstract; cannot be instantiated
    }
}
```

A child object is sometimes mistaken for an "indirect" abstract-class
object. It is not — it is a `C` object, referred to through a `P` reference:

```java
abstract class P {
}

class C extends P {
    public static void main(String[] args) {
        P p = new C();   // a C object, referred to via type P
        // still not an abstract-class object created "indirectly"
    }
}
```

The same holds for the other common "indirect" attempt — an anonymous
subclass created inline at the `new` site:

```java
abstract class P {
    abstract void show();
}

class Demo {
    public static void main(String[] args) {
        P p = new P() {                       // anonymous subclass of P
            void show() { System.out.println("anon"); }
        };
        System.out.println(p.getClass());     // class Demo$1 — NOT class P
    }
}
```

`p.getClass()` prints `Demo$1`, a compiler-generated subclass — never `P`
itself. `new P() { ... }` still creates a subclass object, exactly like the
`C` example; it only *looks* like `new AbstractClass()` at the call site.

### 02:07 — Bit 7: "creating a child object automatically creates a parent object" — invalid

**Invalid.** Creating a child object automatically runs the **parent
constructor**; it never creates a separate parent object (videos 045–046).

### 02:25 — Bit 8: "creating a child object automatically executes the abstract-class constructor" — valid

**Valid.** The abstract-class constructor runs whenever a child object is
created — that is the only time it ever runs.

```java
abstract class P {
    P() {
        System.out.println("abstract parent constructor");
    }
}

class C extends P {
    C() {
        System.out.println("child constructor");
    }

    public static void main(String[] args) {
        C c = new C();
        // prints: abstract parent constructor
        // prints: child constructor
        // P's constructor ran; no P object was ever created
    }
}
```

### 02:41 — Bit 9: "creating a child object automatically creates a parent object" — invalid

**Invalid**, same statement and same answer as Bit 7 — restated to lock it
in before Bit 10 pairs it with the correct version.

### 02:53 — Bit 10: "parent constructor executes, but parent object is not created" — valid

**Valid.** This is Bit 7/9 corrected: parent **constructor** runs, parent
**object** never exists.

### 03:02 — Bit 11: "no abstract-class object means no constructor for abstract classes" — invalid

**Invalid.** Direct and indirect instantiation are both refused, but the
abstract class can still declare a constructor — to initialize instance
variables that a concrete **child** object will carry (video 047).

```java
abstract class P {
    String name;
    int age;

    P(String name, int age) {
        this.name = name;
        this.age = age;   // initializes fields the child object will hold
    }
}

class C extends P {
    C(String name, int age) {
        super(name, age);
    }

    public static void main(String[] args) {
        C c = new C("durga", 30);
        // P's constructor is legal and it did run
        // still no P object was ever created — only c, a C object
    }
}
```

### 03:23 — Bit 12: "an interface can contain a constructor" — invalid

**Invalid.** The constructor concept does not apply to interfaces at all
(video 048): every interface field is implicitly `public static final`, so
there is never an instance variable for a constructor to initialize.

```java
interface X {
    X() {
        // CE: <identifier> expected
        // an interface constructor isn't restricted — it's not a
        // recognized construct in an interface body at all
    }
}
```

> ⚠️ **Modern Java — interfaces gained bodies, but never gained state.**
> Since this lecture (Java 6/7), interfaces picked up **default methods**
> (Java 8), **static methods** (Java 8), and **private methods** (Java 9) —
> real, runnable code inside an interface. None of that adds an instance
> variable: every interface field is still implicitly `static final`, so the
> reasoning above is untouched — `interface X { X() { } }` is still a
> compile error today, exactly as it was in Java 6. See video 048 for the
> full argument.

### 03:34 — Board pass: the same twelve, tick or cross

From here Sir copies the identical twelve statements onto the board, one at
a time, marking each with a tick (valid) or a cross (invalid) — the drill
format an OCJP bit question actually uses. The statements and answers are
unchanged from the listen pass above; only the presentation differs, so the
timestamps below are grouped by board item rather than re-explained.

- **03:46** — heading: *"Which of the following are valid."*
- **04:01 (Board 1)** — *purpose of constructor is to create an object* → **cross**.
- **04:32 (Board 2)** — *initialize, not create* → **tick**.
- **05:01 (Board 3)** — *object creation completes only once constructor completes* → **cross**.
- **05:23 (Board 4)** — *object created first, then constructor executes* → **tick**.
- **05:45 (Board 5)** — *new creates, constructor initializes* → **tick**.
- **06:16 (Board 6)** — *no direct abstract object, but indirect yes* → **cross**.
- **06:54 (Board 7)** — *child object creates parent object internally* → **cross**.
- **07:27 (Board 8)** — *child object executes abstract-class constructor* → **tick**, "because the abstract class constructor is for child-object initialization only."
- **08:18 (Board 9)** — *child object creates parent object* → **cross**.
- **08:55 (Board 10)** — *parent constructor executes, parent object not created* → **tick**.
- **09:49 (Board 11)** — *no abstract object ⇒ no constructor for abstract class* → **cross**, "because abstract class can contain constructor."
- **10:31 (Board 12)** — *interface can contain constructor* → **cross**, "because constructor concept not applicable for interfaces."

### 10:40 — Close

That is the full set of loopholes on interface, abstract class, constructor,
and the `new` operator across this stretch of the course.

**Bits 1–12, as answered across both passes**

| # | Statement | Mark |
|---|---|---|
| 1 | Purpose of constructor is to create an object | Cross — invalid |
| 2 | Purpose of constructor is to initialize an object but not to create object | Tick — valid |
| 3 | Once constructor completes, then only object creation completes | Cross — invalid (`new` creates) |
| 4 | First object will be created and then constructor will be executed | Tick — valid |
| 5 | `new` creates the object; constructor initializes that object | Tick — valid |
| 6 | Cannot create abstract-class object directly, but indirectly we can | Cross — invalid (neither direct nor indirect) |
| 7 | Creating child object automatically creates parent object internally | Cross — invalid |
| 8 | Creating child object automatically executes abstract-class constructor | Tick — valid (for child initialization) |
| 9 | Creating child object automatically creates parent object | Cross — invalid |
| 10 | Creating child object executes parent constructor, but parent object will not be created | Tick — valid |
| 11 | No abstract-class object (direct or indirect), hence constructor not applicable for abstract class | Cross — invalid (abstract class can contain constructor) |
| 12 | Interface can contain constructor | Cross — invalid (constructor not applicable for interfaces) |

---

## Exam and interview points

1. **`new` creates, the constructor initializes.** That split is the single
   idea every other bit in this drill is built on top of.
2. **An abstract class cannot be instantiated, directly or indirectly** —
   `new AbstractClass()` is a compile error, and no trick (child object,
   anonymous subclass) actually produces an object of the abstract type
   itself. `new P() { ... }` against an abstract `P` compiles to a generated
   subclass (`Outer$1`), never a `P`.
3. **Creating a child object runs the parent's constructor; it never creates
   a separate parent object.** This exact wording flip (constructor vs.
   object) is the trap repeated four times in this drill (Bits 7–10).
4. **An abstract class can — and often must — declare a constructor**,
   because it can hold instance variables that a concrete subclass needs
   initialized; that constructor only ever runs via `super(...)` from a
   child, never via a direct `new` on the abstract type.
5. **An interface can never declare a constructor**, in any Java version,
   because every interface field is implicitly `public static final` — there
   is no instance variable for a constructor to initialize. Default, static,
   and private interface methods (Java 8/9) add behavior, not state, so this
   remains unchanged.
6. **This is the exact form OCJP bit questions take**: a plain-English
   statement, mark it valid or invalid. Practicing the twelve here is
   practicing the question format, not just the content.

---

**Next:** Video 051 — OOPs introduction and data hiding
