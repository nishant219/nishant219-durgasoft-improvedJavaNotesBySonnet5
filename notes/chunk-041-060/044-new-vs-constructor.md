# Video 044 — new vs Constructor

## Video info

**Title:** Core Java With OCJP/SCJP: Interface  and Abstract class Loopholes Part-1 || new vs Constructor

| Field | Detail |
|---|---|
| Playlist | java tutorial by durga sir |
| Position | 44 of 203 |
| Series | Interface and Abstract class Loopholes · Part 1 |
| Topic | new vs Constructor |
| Instructor | Durga Sir (Durga Software Solutions) |
| Duration | 15m 59s |
| Video ID | WyE3t9geWNY |
| Watch | https://www.youtube.com/watch?v=WyE3t9geWNY |
| Playlist URL | https://www.youtube.com/playlist?list=PLd3UqWTnYXOmx_J1774ukG_rvrpyWczm0 |

> **How to read these notes.** Sections follow the lecture's own timestamps.
> Two kinds of callout interrupt the lecture where it needs it:
> **⚠️ Modern Java** — what Sir taught was right for Java 6/7, and has since
> changed. **❗ Correction** — what was stated is not accurate, then or now.
> Everything else is Sir's teaching, cleaned up.

## What this lecture covers

This video opens the **Interface and Abstract class Loopholes** stretch, but it
does **not** answer any of the loopholes yet. Sir only reads five loophole
questions onto the board as the agenda for the whole stretch, then spends the
rest of the class on a single prerequisite: the difference between `new` and a
constructor. Videos 046–048 come back and answer the five questions. Video 045
(*Child Object Vs Parent Constructor-1*) has no captions and is not covered in
this note set.

The five questions, so you have them in one place before they get answered
piece by piece over the next few videos:

1. We can't create an object for an abstract class, but an abstract class can
   contain a constructor. What is the need — what is it for?
2. We can't create an object for an abstract class **directly** — but can we
   create one **indirectly**? Valid or not?
3. Textbooks claim: creating a child class object automatically creates a
   parent class object. Valid or not?
4. We can't create an object for an abstract class *or* an interface, but an
   abstract class can contain a constructor and an interface cannot. Why?
5. Both an interface and an abstract class can be restricted to only abstract
   methods. So what does an interface give you that an abstract class doesn't
   — can one concept just replace the other?

Before any of that can be answered, one distinction has to be nailed down
first: **what does `new` do, and what does a constructor do?** Most learners
conflate the two — this video exists to separate them.

---

## 00:40 — The doubts on the table

Sir opens by naming the doubts students carry into this topic, without
resolving any of them yet:

- We never create an object for an abstract class — so why is an abstract
  class allowed to **have** a constructor at all?
- Some people believe an abstract class's object can be created
  **indirectly**, even though direct creation (`new AbstractClass()`) is
  refused. Is that actually possible?
- An interface can't contain a constructor; an abstract class can. Both are
  equally impossible to instantiate directly. So why does one get a
  constructor and the other doesn't?
- A claim repeated across textbooks and websites: creating a child class
  object automatically creates a parent class object too. True or not?

None of these get answered here — Sir flags them as the loopholes this
multi-video stretch (roughly an hour to an hour and a half of material) will
work through.

```java
abstract class Person {
    Person() {
        // legal: an abstract class can declare a constructor
    }
}

class Test {
    public static void main(String[] args) {
        Person p = new Person();
        // CE: Person is abstract; cannot be instantiated
    }
}
```

Compiling this confirms both halves of the doubt: the constructor declaration
is accepted, and the direct `new Person()` is rejected with exactly the error
Sir is building toward — `Person is abstract; cannot be instantiated`.

---

## 02:28 — Board: the five loophole questions

Sir has a student read the five questions aloud, verbatim, as the agenda:

1. We can't create an object for abstract class, but abstract class can
   contain a constructor. What is the need?
2. We can't create an object for abstract class directly, but indirectly we
   can create it. Is it valid or not?
3. Whenever we create a child class object, automatically a parent class
   object will be created. Is it valid or not?
4. We can't create an object for abstract class or interface, but abstract
   class can contain a constructor and interface doesn't. Why?
5. Interface can take only abstract methods; abstract class can also take
   only abstract methods, by choice. Then what's the point of interface — can
   abstract class just replace it?

This is the complete list for the whole loopholes arc, not five answers packed
into this 16-minute video.

---

## 03:50 — Constructor vs `new`: get this straight first

Before touching any of the five questions, Sir insists on one prerequisite:
know the purpose of the `new` keyword and the purpose of a constructor, and
know that they are two **different** jobs.

### 04:00 — Board: `Student s = new Student("Durga", 101);`

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }
}

class Test {
    public static void main(String[] args) {
        Student s = new Student("Durga", 101);
    }
}
```

Ask a class what this line does and most people say "it creates an object."
Sir's correction: it does **two** things — creation, and initialization — and
most people can't say which keyword is responsible for which.

- **`new`** — its whole job is to **create the object**.
- **the constructor call** (`Student("Durga", 101)`) — its whole job is to
  **initialize** that object.

The common wrong belief is that the constructor creates the object. It
doesn't. `new` creates it; the constructor only fills it in.

---

## 05:25 — The `Student` class and its constructor

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }
}
```

Two instance variables, `name` and `rollNumber` — every student needs a name
and a roll number, and every object gets its own separate copy of both. The
block with the class's own name and no return type is the constructor.

---

## 06:33 — Two things happen on that one line

Walking through `Student s = new Student("Durga", 101);` piece by piece:

| Piece | Responsible for | 
|---|---|
| `new` | **creating** the object |
| `Student("Durga", 101)` (the constructor call) | **initializing** the object |

Two separate jobs on one line: `new` builds the object; the constructor call
that immediately follows it fills that object in.

---

## 07:27 — What `new` actually does: object + default values

Internally, `new` allocates the `Student` object and its two instance
variables, and those variables start out at their **default values** — not at
`"Durga"` and `101` yet:

- `name` defaults to `null` (any reference type's default).
- `rollNumber` defaults to `0` (any numeric primitive's default).

Only after that does the constructor body run and overwrite the defaults with
the values you actually passed in.

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        System.out.println("before init: " + this.name + ", " + this.rollNumber);
        this.name = name;
        this.rollNumber = rollNumber;
    }
}

class Test {
    public static void main(String[] args) {
        Student s = new Student("Durga", 101);
        // prints: before init: null, 0
    }
}
```

This is checkable, not just a claim: printing the fields at the top of the
constructor body — before the two assignment statements run — really does
print `null, 0`. `new` has already built the object with default values by
the time the constructor body starts executing.

> ⚠️ **Modern Java — bytecode proof, if you want to see it directly.**
> `javap -c` on this class shows exactly the two-step split Sir describes,
> unchanged since Java 6 and unchanged today:
> ```text
> new           #7      // class Student   <- allocate the object
> dup
> ldc           #9      // String Durga
> bipush        101
> invokespecial #11     // Student."<init>":(Ljava/lang/String;I)V   <- run the constructor
> ```
> The `new` bytecode instruction allocates and zero/null-initializes the
> object; the *separate* `invokespecial <init>` instruction is what runs the
> constructor body. Two opcodes, two jobs — the JVM literally enforces the
> distinction Sir is teaching.

---

## 08:02 — Immediately after creation, the constructor runs

As soon as the object exists, the constructor executes on it — no gap, no
other step in between. Two arguments come in (`"Durga"` and `101`), and this
particular constructor call runs *on* the object `new` just built, to perform
its initialization.

Inside the body, `this.name = name;` reads as: *the current object's* `name`
field is set to the `name` parameter you were handed. Same idea for
`this.rollNumber = rollNumber;`. Before this line ran, `this.name` was `null`
(the default `new` set) and `this.rollNumber` was `0`; after it runs, they are
`"Durga"` and `101`.

The purpose of `new` is to create an object. The purpose of the constructor is
to perform initialization of an object — **not** to create it. That
distinction is the entire point of this video.

---

## 09:20 — Which runs first: `new` or the constructor?

`new` always runs first. Only once the object exists is there anything to
initialize — so `new` creates it, and only *then* does the constructor run to
fill it in.

Sir's memory hook: a baby has to be born before anyone thinks about a naming
ceremony. Nobody holds the naming ceremony first and waits for the baby to
show up afterward. Object creation is the birth; the constructor call is the
naming ceremony. Order is fixed: `new` (create), then constructor
(initialize).

---

## 10:18 — Board dictation: the two jobs, and the order

Sir dictates this slowly, three times over, for students to copy into their
notes:

> **The main objective of `new` is to create an object.**
> **The main purpose of a constructor is to initialize that object.**
> **First the object is created using `new`; only then is initialization
> performed, by the constructor.**

This is the whole lesson compressed to three lines — everything before and
after this point in the video is elaboration on exactly these three
sentences.

---

## 12:22 — Same example, rewritten to make it stick

```java
class Student {
    String name;
    int rollNumber;

    Student(String name, int rollNumber) {
        this.name = name;
        this.rollNumber = rollNumber;
    }
}

class Test {
    public static void main(String[] args) {
        Student s = new Student("Durga", 101);
        // new Student(...)       -> new: responsible for creating the object
        // Student("Durga", 101)  -> constructor: responsible for initializing it
    }
}
```

`this.name = name;` and `this.rollNumber = rollNumber;` are plain assignment
statements, and assignment is what initialization *is*. The constructor's job,
in full, is: run these assignments against the object `new` already built.
Nothing more. Whenever an object is created with `new`, the matching
constructor is automatically invoked right after to do exactly this.

> ⚠️ **Modern Java — a record gets you the same split, with less to write.**
> A class whose whole job is "hold a fixed set of fields, assign them once in
> the constructor, no other behavior" is exactly what a **record** (Java 16,
> JEP 395) is for:
> ```java
> record Student(String name, int rollNumber) { }
>
> Student s = new Student("Durga", 101);   // new still creates; the canonical
>                                           // constructor still just assigns
> s.name();        // "Durga"   — accessor, not a getName() method
> s.rollNumber();  // 101
> ```
> The compiler generates the same `this.name = name; this.rollNumber =
> rollNumber;` canonical constructor Sir wrote by hand, plus accessors,
> `equals`/`hashCode`/`toString`. `new`-creates-then-constructor-initializes
> still applies exactly as taught — a record doesn't change that model, it
> just writes the boilerplate for you. For OCJP-era code, and for a class that
> needs mutable fields or extra behavior, Sir's hand-written form is still
> correct and still what you'll see.

---

## 15:05 — Point number one: the constructor does not create the object

Sir's closing line, stated as the takeaway to carry forward: most people
believe a constructor's job is to create the object. It is not. A
constructor's job is to **initialize** an object that `new` has already
created. This is flagged explicitly as "point number one" — the first fact
the rest of the loopholes stretch will build on.

---

## Exam and interview points

1. **`new` creates; the constructor initializes.** These are two different
   responsibilities on one line — `Student s = new Student("Durga", 101);` —
   not one job split into two words.
2. **`new` always runs before the constructor.** There is nothing to
   initialize until the object exists.
3. **Instance variables hold their default values the instant `new` finishes**
   allocating — `null` for references, `0`/`0.0`/`false` for primitives — and
   *before* the constructor body has run a single statement. You can prove
   this by printing a field at the top of the constructor.
4. **The constructor body is just assignment statements.** `this.field =
   parameter;` is initialization, not creation — `this.field` refers to the
   object `new` already built.
5. **An abstract class can declare a constructor even though it can never be
   `new`-ed directly** — that's the first loophole question this stretch will
   go on to answer (videos 046–048), not something this video resolves.
6. **An interface still cannot declare a constructor at all** — `interface
   IFace { IFace() { } }` is a compile error (`<identifier> expected`),
   unchanged from Java 6 through current Java, unaffected by default/static/
   private interface methods added later.
7. **A record's canonical constructor is the same `new`-then-initialize model**
   with the assignments auto-generated — know both forms for interviews: the
   hand-written constructor is still what most legacy code and the OCJP exam
   expect.

---

**Next:** Video 045 — Child Object Vs Parent Constructor-1 (no captions
available for this note set; the loopholes agenda continues in earnest at
Video 046)
